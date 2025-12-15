# =============================================================================
# LangGraph Pipeline - Refinement Mode
# =============================================================================
# Multi-expert review system for Markmap refinement.
#
# Workflow:
#   1. Load baseline Markmap
#   2. Expert Review (Round 1): Each expert independently suggests improvements
#   3. Full Discussion (Round 2): Experts vote on all suggestions
#   4. Consensus Calculation: Programmatic (code, not AI)
#   5. Writer applies adopted improvements
#   6. Post-processing and translation
#
# API Calls: 2N + 1 (where N = number of experts)
# Sequential Batches: 3 (fixed, regardless of N)
# =============================================================================

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import StateGraph, END

from .agents.expert import create_experts, Suggestion, AdoptionList
from .agents.writer import create_writer
from .agents.translator import create_translators, TranslatorAgent
from .consensus import (
    calculate_consensus,
    get_adopted_suggestions,
    ConsensusResult,
)
from .output.html_converter import save_all_markmaps, MarkMapHTMLConverter
from .post_processing import clean_translated_content

__all__ = [
    "run_pipeline",
    "run_pipeline_async",
    "build_markmap_graph",
    "load_baseline_markmap",
    "handle_versioning_mode",
]
from .post_processing import PostProcessor
from .debug_output import get_debug_manager, reset_debug_manager
from .config_loader import ConfigLoader
from .resume import (
    scan_previous_runs,
    select_run_interactive,
    ask_reuse_stage,
    load_consensus_from_run,
    load_expert_responses_from_run,
    load_writer_output_from_run,
    generate_regen_run_id,
    RunInfo,
)


class WorkflowState(TypedDict, total=False):
    """State schema for the refinement workflow."""
    
    # Input data
    baseline_markmap: str
    ontology: dict[str, Any]
    problems: dict[str, Any]
    patterns: dict[str, Any]
    roadmaps: dict[str, Any]
    
    # Phase 1: Expert Review
    current_phase: str  # "review" or "discussion"
    expert_suggestions: dict[str, list[Suggestion]]  # expert_id -> suggestions
    expert_raw_responses: dict[str, str]
    
    # Phase 2: Discussion
    adoption_lists: dict[str, AdoptionList]  # expert_id -> adoption list
    discussion_raw_responses: dict[str, str]
    
    # Phase 3: Consensus
    consensus_result: ConsensusResult
    adopted_suggestions: list[Suggestion]
    
    # Phase 4: Writer
    final_markmap: str
    writer_outputs: dict[str, str]
    
    # Phase 5: Translation
    translated_outputs: dict[str, str]
    translator_configs: list[dict]
    
    # Phase 6: Post-processing & Output
    final_outputs: dict[str, str]
    
    # Metadata
    messages: list[str]
    errors: list[str]


def load_baseline_markmap(config: dict[str, Any]) -> str:
    """
    Load the baseline Markmap from file.
    
    Behavior depends on versioning mode:
    - continue: Load from latest version (vN) if exists, else fall back to baseline.path
    - reset: Load from baseline.path (original source)
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Baseline Markmap content as string
    """
    input_config = config.get("input", {})
    baseline_config = input_config.get("baseline", {})
    baseline_path = baseline_config.get("path", "neetcode_ontology_ai_en.md")
    
    # Check versioning mode
    versioning = config.get("output", {}).get("versioning", {})
    versioning_enabled = versioning.get("enabled", False)
    versioning_mode = versioning.get("mode", "continue")
    
    base_dir = Path(__file__).parent.parent.parent.parent  # Go to neetcode root
    
    # For continue mode, try to load from latest version first
    if versioning_enabled and versioning_mode == "continue":
        converter = MarkMapHTMLConverter(config)
        latest_path = converter._get_latest_version_path("en")
        
        if latest_path and latest_path.exists():
            print(f"  📂 Continue mode: Loading from {latest_path.parent.name}/{latest_path.name}")
            return latest_path.read_text(encoding="utf-8")
        else:
            print("  📂 Continue mode: No previous version found, using baseline")
    
    # Load from configured baseline path
    full_path = base_dir / "docs" / "mindmaps" / baseline_path
    
    if full_path.exists():
        return full_path.read_text(encoding="utf-8")
    
    # Try alternative paths
    alt_paths = [
        base_dir / "docs" / "mindmaps" / "neetcode_ontology_ai_en.md",
        base_dir / "docs" / "mindmaps" / "neetcode_general_ai_en.md",
    ]
    
    for alt_path in alt_paths:
        if alt_path.exists():
            print(f"  ⚠ Using alternative baseline: {alt_path.name}")
            return alt_path.read_text(encoding="utf-8")
    
    # Fallback: check if we should generate from scratch
    if baseline_config.get("fallback_to_generate", True):
        print("  ⚠ No baseline found, will need to generate from scratch")
        return ""
    
    raise FileNotFoundError(f"Baseline Markmap not found: {full_path}")


def handle_versioning_mode(config: dict[str, Any]) -> bool:
    """
    Handle versioning mode before running the pipeline.
    
    For reset mode, prompts user to confirm deletion of old versions.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True to continue, False to abort (user cancelled reset)
    """
    versioning = config.get("output", {}).get("versioning", {})
    versioning_enabled = versioning.get("enabled", False)
    versioning_mode = versioning.get("mode", "continue")
    
    if not versioning_enabled:
        return True
    
    if versioning_mode == "reset":
        converter = MarkMapHTMLConverter(config)
        return converter.handle_reset_mode()
    
    # Continue mode - just show info
    converter = MarkMapHTMLConverter(config)
    existing = converter._get_existing_versions()
    if existing:
        print(f"  📂 Continue mode: {len(existing)} existing version(s)")
        print(f"      Latest: {existing[-1].name}")
    
    return True


def build_markmap_graph(config: dict[str, Any] | None = None) -> StateGraph:
    """
    Build the LangGraph workflow for Markmap refinement.
    
    Workflow:
    1. Initialize and load baseline
    2. Expert Review (Round 1) - N parallel calls
    3. Full Discussion (Round 2) - N parallel calls
    4. Consensus Calculation (code)
    5. Writer (1 call)
    6. Translation (if needed)
    7. Post-processing and save
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Compiled LangGraph workflow
    """
    config = config or ConfigLoader.get_config()
    workflow_config = config.get("workflow", {})
    naming_config = config.get("output", {}).get("naming", {})
    
    consensus_threshold = workflow_config.get("consensus_threshold", 0.67)
    min_votes = workflow_config.get("min_votes")
    
    # Get languages config
    languages_config = naming_config.get("languages", {})
    if isinstance(languages_config, list):
        languages_config = {lang: {"mode": "generate"} for lang in languages_config}
    
    # Create the state graph
    graph = StateGraph(WorkflowState)
    
    # =========================================================================
    # Node Functions
    # =========================================================================
    
    def initialize(state: WorkflowState) -> WorkflowState:
        """Initialize workflow state and load baseline."""
        print("\n[Phase 0] Initialization...")
        
        # Check if resuming from a previous run
        resume_config = state.get("_resume_config", {})
        
        if resume_config:
            # Resume mode: load state from previous run
            print("  🔄 Resume mode: Loading state from previous run...")
            resume_run_dir = Path(resume_config["run_dir"])
            reuse_stages = resume_config.get("reuse_stages", {})
            
            # Initialize debug output manager with new regen directory
            original_run_id = resume_run_dir.name
            new_run_id = generate_regen_run_id(original_run_id)
            debug_output_dir = Path(__file__).parent.parent.parent / "outputs" / "debug"
            new_run_dir = debug_output_dir / new_run_id
            reset_debug_manager()
            debug = get_debug_manager(config, run_dir=str(new_run_dir))
            print(f"  📁 New run directory: {new_run_id}")
            
            # Load previous state if stages are being reused
            if reuse_stages.get("expert_review"):
                prev_run = RunInfo(resume_run_dir)
                expert_responses = load_expert_responses_from_run(prev_run)
                if expert_responses and "expert_review" in expert_responses:
                    # Note: We can't fully restore state, but we can skip the phase
                    print("  ⏭️  Will reuse expert_review outputs")
            
            if reuse_stages.get("full_discussion"):
                print("  ⏭️  Will reuse full_discussion outputs")
            
            if reuse_stages.get("consensus"):
                prev_run = RunInfo(resume_run_dir)
                consensus_data = load_consensus_from_run(prev_run)
                if consensus_data:
                    # Reconstruct consensus result
                    from .consensus import ConsensusResult
                    state["consensus_result"] = ConsensusResult(
                        adopted=consensus_data.get("adopted", []),
                        rejected=consensus_data.get("rejected", []),
                        vote_counts=consensus_data.get("vote_counts", {}),
                        required_votes=0,
                        num_experts=0,
                    )
                    print("  ✓ Loaded consensus from previous run")
        else:
            # Fresh run
            reset_debug_manager()
            debug = get_debug_manager(config)
        
        if not state.get("current_phase"):
            state["current_phase"] = "review"
        if "messages" not in state:
            state["messages"] = []
        if "errors" not in state:
            state["errors"] = []
        if "writer_outputs" not in state:
            state["writer_outputs"] = {}
        if "translated_outputs" not in state:
            state["translated_outputs"] = {}
        if "final_outputs" not in state:
            state["final_outputs"] = {}
        if "expert_suggestions" not in state:
            state["expert_suggestions"] = {}
        if "expert_raw_responses" not in state:
            state["expert_raw_responses"] = {}
        if "adoption_lists" not in state:
            state["adoption_lists"] = {}
        if "discussion_raw_responses" not in state:
            state["discussion_raw_responses"] = {}
        
        # Store translator configs
        if "translator_configs" not in state:
            state["translator_configs"] = create_translators(config)
        
        if debug.enabled:
            print(f"  📊 Debug output enabled")
        
        # Load baseline if not already in state
        if not state.get("baseline_markmap"):
            try:
                baseline = load_baseline_markmap(config)
                state["baseline_markmap"] = baseline
                print(f"  ✓ Loaded baseline ({len(baseline)} chars, ~{len(baseline.splitlines())} lines)")
                
                # Save baseline to debug
                if debug.enabled:
                    debug.save_baseline(baseline, "loaded", "en")
            except FileNotFoundError as e:
                state["errors"].append(str(e))
                print(f"  ✗ {e}")
        
        return state
    
    def run_expert_review(state: WorkflowState) -> WorkflowState:
        """
        Phase 1: Expert Review (Round 1).
        
        Each expert independently reviews the baseline and suggests improvements.
        This phase runs N parallel API calls.
        """
        print("\n[Phase 1] Expert Review (Independent)...")
        
        # Check if we should skip this phase (resume mode)
        resume_config = state.get("_resume_config", {})
        if resume_config:
            reuse_stages = resume_config.get("reuse_stages", {})
            if reuse_stages.get("expert_review"):
                print("  ⏭️  Reusing expert_review from previous run")
                # Copy all files related to expert_review to new directory
                resume_run_dir = Path(resume_config["run_dir"])
                prev_run = RunInfo(resume_run_dir)
                debug = get_debug_manager(config)
                if debug.enabled:
                    import shutil
                    # Copy all expert_review related files
                    expert_review_files = prev_run.get_stage_files("expert_review")
                    if expert_review_files:
                        for file_info in expert_review_files:
                            try:
                                dest = debug.run_dir / file_info["filename"]
                                shutil.copy2(file_info["path"], dest)
                                print(f"  💾 Copied: {file_info['filename']}")
                            except Exception as e:
                                print(f"  ⚠ Failed to copy {file_info['filename']}: {e}")
                    else:
                        print("  ⚠ No expert_review files found in previous run")
                return state
        
        debug = get_debug_manager(config)
        
        state["current_phase"] = "review"
        experts = create_experts(config)
        
        # Run all experts (can be parallelized with async)
        for expert in experts:
            try:
                state = expert.review(state)
                suggestions = state.get("expert_suggestions", {}).get(expert.agent_id, [])
                print(f"  {expert.emoji} {expert.name}: {len(suggestions)} suggestions")
                
                # Save debug output
                if debug.enabled and expert.agent_id in state.get("expert_raw_responses", {}):
                    debug.save_optimizer_suggestion(
                        state["expert_raw_responses"][expert.agent_id],
                        expert.name,
                        1,
                        "review"
                    )
            except Exception as e:
                error_msg = f"Error in {expert.name}: {e}"
                state["errors"].append(error_msg)
                print(f"  ✗ {error_msg}")
        
        # Count total suggestions
        total_suggestions = sum(
            len(s) for s in state.get("expert_suggestions", {}).values()
        )
        print(f"\n  Total: {total_suggestions} suggestions collected")
        
        return state
    
    def run_full_discussion(state: WorkflowState) -> WorkflowState:
        """
        Phase 2: Full Discussion (Round 2).
        
        Each expert sees all suggestions and votes on them.
        This phase runs N parallel API calls.
        """
        print("\n[Phase 2] Full Discussion...")
        
        # Check if we should skip this phase (resume mode)
        resume_config = state.get("_resume_config", {})
        if resume_config:
            reuse_stages = resume_config.get("reuse_stages", {})
            if reuse_stages.get("full_discussion"):
                print("  ⏭️  Reusing full_discussion from previous run")
                # Copy all files related to full_discussion to new directory
                resume_run_dir = Path(resume_config["run_dir"])
                prev_run = RunInfo(resume_run_dir)
                debug = get_debug_manager(config)
                if debug.enabled:
                    import shutil
                    # Copy all full_discussion related files
                    discussion_files = prev_run.get_stage_files("full_discussion")
                    if discussion_files:
                        for file_info in discussion_files:
                            try:
                                dest = debug.run_dir / file_info["filename"]
                                shutil.copy2(file_info["path"], dest)
                                print(f"  💾 Copied: {file_info['filename']}")
                            except Exception as e:
                                print(f"  ⚠ Failed to copy {file_info['filename']}: {e}")
                    else:
                        print("  ⚠ No full_discussion files found in previous run")
                return state
        
        debug = get_debug_manager(config)
        
        state["current_phase"] = "discussion"
        experts = create_experts(config)
        
        print("  Each expert reviewing all suggestions...")
        
        # Run all experts for discussion
        for expert in experts:
            try:
                state = expert.discuss(state)
                adoption_list = state.get("adoption_lists", {}).get(expert.agent_id)
                if adoption_list:
                    print(f"  {expert.emoji} {expert.name}: {len(adoption_list.adopted_ids)} adopted")
                
                # Save debug output
                if debug.enabled and expert.agent_id in state.get("discussion_raw_responses", {}):
                    debug.save_optimizer_suggestion(
                        state["discussion_raw_responses"][expert.agent_id],
                        expert.name,
                        2,
                        "discussion"
                    )
            except Exception as e:
                error_msg = f"Error in {expert.name} discussion: {e}"
                state["errors"].append(error_msg)
                print(f"  ✗ {error_msg}")
        
        return state
    
    def run_consensus(state: WorkflowState) -> WorkflowState:
        """
        Phase 3: Consensus Calculation (Code, not AI).
        
        Uses majority voting to determine which suggestions are adopted.
        """
        print("\n[Phase 3] Consensus Calculation...")
        
        # Check if we should skip this phase (resume mode)
        resume_config = state.get("_resume_config", {})
        if resume_config:
            reuse_stages = resume_config.get("reuse_stages", {})
            
            resume_run_dir = Path(resume_config["run_dir"])
            prev_run = RunInfo(resume_run_dir)
            
            # If explicitly marked to reuse, load it
            if reuse_stages.get("consensus"):
                print("  ⏭️  Reusing consensus from previous run")
                # Consensus should already be loaded in initialize()
                # Copy all consensus files to new directory
                debug = get_debug_manager(config)
                if debug.enabled:
                    import shutil
                    # Copy all consensus related files
                    consensus_files = prev_run.get_stage_files("consensus")
                    if consensus_files:
                        for file_info in consensus_files:
                            try:
                                dest = debug.run_dir / file_info["filename"]
                                shutil.copy2(file_info["path"], dest)
                                print(f"  💾 Copied: {file_info['filename']}")
                            except Exception as e:
                                print(f"  ⚠ Failed to copy {file_info['filename']}: {e}")
                    # Also save consensus data if available in state
                    if "consensus_result" in state:
                        consensus_result = state["consensus_result"]
                        consensus_data = {
                            "adopted": consensus_result.adopted,
                            "rejected": consensus_result.rejected,
                            "vote_counts": consensus_result.vote_counts,
                            "threshold": consensus_threshold,
                            "_reused_from": prev_run.run_id,
                        }
                        debug.save_consensus(consensus_data)
                return state
            
            # If not in reuse list but output exists, ask user
            if prev_run.has_stage_output("consensus") and "consensus" not in reuse_stages:
                from ..resume import ask_reuse_stage
                should_reuse = ask_reuse_stage("consensus", prev_run)
                if should_reuse:
                    consensus_data = load_consensus_from_run(prev_run)
                    if consensus_data:
                        from .consensus import ConsensusResult
                        state["consensus_result"] = ConsensusResult(
                            adopted=consensus_data.get("adopted", []),
                            rejected=consensus_data.get("rejected", []),
                            vote_counts=consensus_data.get("vote_counts", {}),
                            required_votes=0,
                            num_experts=0,
                        )
                        print("  ✓ Loaded consensus from previous run")
                        # Copy all consensus files to new directory
                        debug = get_debug_manager(config)
                        if debug.enabled:
                            import shutil
                            # Copy all consensus related files
                            consensus_files = prev_run.get_stage_files("consensus")
                            if consensus_files:
                                for file_info in consensus_files:
                                    try:
                                        dest = debug.run_dir / file_info["filename"]
                                        shutil.copy2(file_info["path"], dest)
                                        print(f"  💾 Copied: {file_info['filename']}")
                                    except Exception as e:
                                        print(f"  ⚠ Failed to copy {file_info['filename']}: {e}")
                            # Also save consensus data
                            consensus_data["_reused_from"] = prev_run.run_id
                            debug.save_consensus(consensus_data)
                        # Mark as reused so we don't ask again
                        reuse_stages["consensus"] = True
                        return state
        
        debug = get_debug_manager(config)
        
        adoption_lists = state.get("adoption_lists", {})
        all_suggestions = state.get("expert_suggestions", {})
        
        # Calculate consensus
        consensus_result = calculate_consensus(
            adoption_lists=adoption_lists,
            all_suggestions=all_suggestions,
            threshold=consensus_threshold,
            min_votes=min_votes,
        )
        
        # Get full suggestion objects for adopted ones
        adopted_suggestions = get_adopted_suggestions(consensus_result, all_suggestions)
        
        state["consensus_result"] = consensus_result
        state["adopted_suggestions"] = adopted_suggestions
        
        # Print results
        print(f"\n  Threshold: {consensus_threshold:.0%} ({consensus_result.required_votes}/{consensus_result.num_experts})")
        print(f"\n  ✅ Adopted: {len(consensus_result.adopted)} improvements")
        for sid in consensus_result.adopted:
            votes = consensus_result.vote_counts.get(sid, 0)
            print(f"     {sid}: {votes}/{consensus_result.num_experts} votes")
        
        print(f"\n  ❌ Rejected: {len(consensus_result.rejected)} suggestions")
        for sid in consensus_result.rejected:
            votes = consensus_result.vote_counts.get(sid, 0)
            print(f"     {sid}: {votes}/{consensus_result.num_experts} votes")
        
        # Save consensus to debug
        if debug.enabled:
            debug.save_consensus({
                "adopted": consensus_result.adopted,
                "rejected": consensus_result.rejected,
                "vote_counts": consensus_result.vote_counts,
                "threshold": consensus_threshold,
            })
        
        return state
    
    def run_writer(state: WorkflowState) -> WorkflowState:
        """
        Phase 4: Writer (1 API call).
        
        Applies adopted improvements to the baseline.
        """
        print("\n[Phase 4] Writing...")
        
        # Check if we should reuse writer output (resume mode)
        resume_config = state.get("_resume_config", {})
        if resume_config:
            reuse_stages = resume_config.get("reuse_stages", {})
            resume_run_dir = Path(resume_config["run_dir"])
            prev_run = RunInfo(resume_run_dir)
            
            # If explicitly marked to reuse, load it
            if reuse_stages.get("writer"):
                print("  ⏭️  Reusing writer from previous run")
                # Copy all writer related files to new directory
                debug = get_debug_manager(config)
                if debug.enabled:
                    import shutil
                    # Copy all writer related files (LLM input/output, writer output)
                    writer_files = prev_run.get_stage_files("writer")
                    if writer_files:
                        for file_info in writer_files:
                            try:
                                dest = debug.run_dir / file_info["filename"]
                                shutil.copy2(file_info["path"], dest)
                                print(f"  💾 Copied: {file_info['filename']}")
                            except Exception as e:
                                print(f"  ⚠ Failed to copy {file_info['filename']}: {e}")
                    # Load writer output content for state
                    writer_output = load_writer_output_from_run(prev_run)
                    if writer_output:
                        state["final_markmap"] = writer_output
                        state["writer_outputs"]["general_en"] = writer_output
                        print(f"  ✓ Loaded writer output ({len(writer_output)} chars)")
                    else:
                        print("  ⚠ Could not load writer output content")
                return state
            
            # If not in reuse list but output exists, ask user
            elif prev_run.has_stage_output("writer") and "writer" not in reuse_stages:
                from ..resume import ask_reuse_stage
                should_reuse = ask_reuse_stage("writer", prev_run)
                if should_reuse:
                    writer_output = load_writer_output_from_run(prev_run)
                    if writer_output:
                        state["final_markmap"] = writer_output
                        state["writer_outputs"]["general_en"] = writer_output
                        print(f"  ✓ Loaded writer output ({len(writer_output)} chars)")
                        # Copy all writer files to new directory
                        debug = get_debug_manager(config)
                        if debug.enabled:
                            import shutil
                            # Copy all writer related files
                            writer_files = prev_run.get_stage_files("writer")
                            if writer_files:
                                for file_info in writer_files:
                                    try:
                                        dest = debug.run_dir / file_info["filename"]
                                        shutil.copy2(file_info["path"], dest)
                                        print(f"  💾 Copied: {file_info['filename']}")
                                    except Exception as e:
                                        print(f"  ⚠ Failed to copy {file_info['filename']}: {e}")
                        # Mark as reused
                        reuse_stages["writer"] = True
                        return state
        
        debug = get_debug_manager(config)
        
        adopted = state.get("adopted_suggestions", [])
        
        if not adopted:
            print("  ⚠ No improvements to apply, using baseline as-is")
            state["final_markmap"] = state.get("baseline_markmap", "")
            state["writer_outputs"]["general_en"] = state["final_markmap"]
            return state
        
        print(f"  Applying {len(adopted)} improvements to baseline...")
        
        writer = create_writer(config)
        
        try:
            state = writer.process(state)
            final_markmap = state.get("final_markmap", "")
            state["writer_outputs"]["general_en"] = final_markmap
            
            print(f"  ✓ Refined Markmap generated ({len(final_markmap)} chars)")
            
            # Save debug output
            if debug.enabled:
                debug.save_writer_output(final_markmap, "general_en")
                
        except Exception as e:
            error_msg = f"Writer error: {e}"
            state["errors"].append(error_msg)
            print(f"  ✗ {error_msg}")
            # Fallback to baseline
            state["final_markmap"] = state.get("baseline_markmap", "")
            state["writer_outputs"]["general_en"] = state["final_markmap"]
        
        return state
    
    def run_translations(state: WorkflowState) -> WorkflowState:
        """
        Phase 5: Translate outputs for translate-mode languages.
        """
        translator_configs = state.get("translator_configs", [])
        
        if not translator_configs:
            return state
        
        print("\n[Phase 5] Translating outputs...")
        
        # Check if we should skip this phase (resume mode)
        resume_config = state.get("_resume_config", {})
        if resume_config:
            reuse_stages = resume_config.get("reuse_stages", {})
            if reuse_stages.get("translate"):
                print("  ⏭️  Skipping (reusing from previous run)")
                # Translation outputs should be loaded from previous run
                # TODO: Load translation outputs if needed
                return state
        
        debug = get_debug_manager(config)
        
        writer_outputs = state.get("writer_outputs", {})
        translated = {}
        
        for tr_config in translator_configs:
            source_lang = tr_config["source_lang"]
            target_lang = tr_config["target_lang"]
            model = tr_config["model"]
            
            translator = TranslatorAgent(
                source_language=source_lang,
                target_language=target_lang,
                model=model,
                config=config,
            )
            
            for output_key, content in writer_outputs.items():
                # Parse output_key format: "{type}_{lang}" (e.g., "general_en")
                parts = output_key.rsplit("_", 1)
                if len(parts) == 2 and parts[1] == source_lang:
                    target_key = f"{parts[0]}_{target_lang}"
                elif source_lang in output_key:
                    # Fallback: only replace if it's at the end of the string
                    if output_key.endswith(f"_{source_lang}"):
                        target_key = output_key[:-len(f"_{source_lang}")] + f"_{target_lang}"
                    else:
                        continue  # Skip if source_lang appears but not at the end
                else:
                    continue  # Skip if source_lang not found
                
                # Translate the content
                try:
                    if debug.enabled:
                        debug.save_translation(content, output_key, target_key, is_before=True)
                    
                    translated_content = translator.translate(content, "general")
                    # Clean up LLM artifacts
                    translated_content = clean_translated_content(translated_content)
                    translated[target_key] = translated_content
                    print(f"  ✓ Translated: {output_key} → {target_key}")
                    
                    if debug.enabled:
                        debug.save_translation(translated_content, output_key, target_key, is_before=False)
                except Exception as e:
                    print(f"  ✗ Translation failed: {e}")
                    state["errors"].append(f"Translation error: {e}")
        
        state["translated_outputs"] = translated
        return state
    
    def run_post_processing(state: WorkflowState) -> WorkflowState:
        """
        Phase 6: Post-processing.
        
        Apply text transformations (e.g., LC → LeetCode).
        """
        print("\n[Phase 6] Post-processing...")
        debug = get_debug_manager(config)
        
        processor = PostProcessor(config)
        
        # Merge writer outputs and translations
        all_outputs = {}
        all_outputs.update(state.get("writer_outputs", {}))
        all_outputs.update(state.get("translated_outputs", {}))
        
        # Apply post-processing
        final_outputs = {}
        for key, content in all_outputs.items():
            if debug.enabled:
                debug.save_post_processing(content, key, is_before=True)
            
            processed = processor.process(content)
            final_outputs[key] = processed
            print(f"  ✓ Processed: {key}")
            
            if debug.enabled:
                debug.save_post_processing(processed, key, is_before=False)
        
        state["final_outputs"] = final_outputs
        return state
    
    def save_outputs(state: WorkflowState) -> WorkflowState:
        """
        Phase 7: Save all outputs to files.
        """
        print("\n[Phase 7] Saving outputs...")
        
        final_outputs = state.get("final_outputs", {})
        
        if not final_outputs:
            print("  ⚠ No outputs to save")
            return state
        
        try:
            saved = save_all_markmaps(final_outputs, config)
            state["messages"].append(f"Saved {len(saved)} output files")
            print(f"  ✓ Saved {len(saved)} output files")
        except Exception as e:
            error_msg = f"Error saving outputs: {e}"
            state["errors"].append(error_msg)
            print(f"  ✗ {error_msg}")
        
        return state
    
    # =========================================================================
    # Build Graph
    # =========================================================================
    
    # Add nodes
    graph.add_node("initialize", initialize)
    graph.add_node("expert_review", run_expert_review)
    graph.add_node("full_discussion", run_full_discussion)
    graph.add_node("consensus", run_consensus)
    graph.add_node("write", run_writer)
    graph.add_node("translate", run_translations)
    graph.add_node("post_process", run_post_processing)
    graph.add_node("save", save_outputs)
    
    # Add edges (linear flow for refinement mode)
    graph.set_entry_point("initialize")
    graph.add_edge("initialize", "expert_review")
    graph.add_edge("expert_review", "full_discussion")
    graph.add_edge("full_discussion", "consensus")
    graph.add_edge("consensus", "write")
    graph.add_edge("write", "translate")
    graph.add_edge("translate", "post_process")
    graph.add_edge("post_process", "save")
    graph.add_edge("save", END)
    
    return graph.compile()


async def run_pipeline_async(
    data: dict[str, Any],
    config: dict[str, Any] | None = None,
) -> WorkflowState:
    """
    Run the pipeline asynchronously.
    
    Args:
        data: Input data with ontology, problems, patterns, roadmaps
        config: Configuration dictionary
        
    Returns:
        Final workflow state
    """
    graph = build_markmap_graph(config)
    
    initial_state: WorkflowState = {
        "baseline_markmap": data.get("baseline_markmap", ""),
        "ontology": data.get("ontology", {}),
        "problems": data.get("problems", {}),
        "patterns": data.get("patterns", {}),
        "roadmaps": data.get("roadmaps", {}),
    }
    
    result = await graph.ainvoke(initial_state)
    return result


def run_pipeline(
    data: dict[str, Any],
    config: dict[str, Any] | None = None,
) -> WorkflowState:
    """
    Run the pipeline synchronously.
    
    Args:
        data: Input data with ontology, problems, patterns, roadmaps
        config: Configuration dictionary
        
    Returns:
        Final workflow state
    """
    graph = build_markmap_graph(config)
    
    initial_state: WorkflowState = {
        "baseline_markmap": data.get("baseline_markmap", ""),
        "ontology": data.get("ontology", {}),
        "problems": data.get("problems", {}),
        "patterns": data.get("patterns", {}),
        "roadmaps": data.get("roadmaps", {}),
    }
    
    result = graph.invoke(initial_state)
    return result

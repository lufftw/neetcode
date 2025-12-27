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
from datetime import datetime
from .post_processing import clean_translated_content

__all__ = [
    "run_pipeline",
    "run_pipeline_async",
    "build_markmap_graph",
    "load_baseline_markmap",
    "handle_versioning_mode",
]
from .post_processing import PostProcessor, preprocess_for_llm
from .debug_output import get_debug_manager, reset_debug_manager
from .config_loader import ConfigLoader
from .resume import (
    scan_previous_runs,
    select_run_interactive,
    ask_reuse_stage,
    load_consensus_from_run,
    load_expert_responses_from_run,
    load_writer_output_from_run,
    load_translation_outputs_from_run,
    load_post_processing_outputs_from_run,
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
    
    # Resume configuration (internal)
    _resume_config: dict[str, Any]


def _save_post_processing_comparison(
    comparison_data: dict[str, dict[str, str]],
    config: dict[str, Any]
) -> None:
    """
    Save post-processing before/after comparison to markdown file.
    
    Args:
        comparison_data: Dict mapping output key to {"before": str, "after": str}
        config: Configuration dictionary
    """
    if not comparison_data:
        return
    
    # Get output directory from config
    output_config = config.get("output", {})
    final_dirs = output_config.get("final_dirs", {})
    markdown_dir = final_dirs.get("markdown", "outputs/final")
    
    base_dir = Path(__file__).parent.parent.parent.parent
    output_path = base_dir / markdown_dir
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create comparison file
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    comparison_file = output_path / f"post-processing-comparison-{timestamp}.md"
    
    content_parts = [
        "# Post-Processing Link Comparison",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "This file shows the before/after comparison of post-processing link generation.",
        "",
        "---",
        "",
    ]
    
    for key, data in comparison_data.items():
        before = data.get("before", "")
        after = data.get("after", "")
        
        content_parts.extend([
            f"## {key}",
            "",
            "### Before (原始內容)",
            "",
            "```markdown",
            before[:5000] + ("..." if len(before) > 5000 else ""),  # Limit length
            "```",
            "",
            "### After (後處理後)",
            "",
            "```markdown",
            after[:5000] + ("..." if len(after) > 5000 else ""),  # Limit length
            "```",
            "",
            "---",
            "",
        ])
    
    try:
        comparison_file.write_text("\n".join(content_parts), encoding="utf-8")
        print(f"  📄 Post-processing comparison saved: {comparison_file.name}")
    except Exception as e:
        print(f"  ⚠ Failed to save comparison: {e}")


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
    baseline_path = baseline_config.get("path", "neetcode-ontology-ai-en.md")
    
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
        base_dir / "docs" / "mindmaps" / "neetcode-ontology-ai-en.md",
        base_dir / "docs" / "mindmaps" / "neetcode-general-ai-en.md",
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


def handle_versioning_mode(config: dict[str, Any], skip_if_resume: bool = False) -> bool:
    """
    Handle versioning mode before running the pipeline.
    
    For reset mode, prompts user to confirm deletion of old versions.
    
    Args:
        config: Configuration dictionary
        skip_if_resume: If True and in resume mode, skip versioning checks
                       (resume mode reuses debug outputs, versioning is separate)
        
    Returns:
        True to continue, False to abort (user cancelled reset)
    """
    # Check if we're in resume mode
    if skip_if_resume:
        # In resume mode, versioning is separate from pipeline execution
        # We'll still show info but won't prompt for reset
        versioning = config.get("output", {}).get("versioning", {})
        versioning_enabled = versioning.get("enabled", False)
        if versioning_enabled:
            versioning_mode = versioning.get("mode", "continue")
            if versioning_mode == "reset":
                print("  ℹ️  Resume mode: Versioning reset will apply to final output only")
                print("      (Debug outputs are reused from previous run)")
            else:
                converter = MarkMapHTMLConverter(config)
                existing = converter._get_existing_versions()
                if existing:
                    print(f"  📂 Continue mode: {len(existing)} existing version(s)")
                    print(f"      Latest: {existing[-1].name}")
        return True
    
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
                
                # Apply preprocessing to simplify links and reduce tokens
                original_len = len(baseline)
                baseline = preprocess_for_llm(baseline)
                simplified_len = len(baseline)
                
                state["baseline_markmap"] = baseline
                print(f"  ✓ Loaded baseline ({original_len} → {simplified_len} chars, saved {original_len - simplified_len} chars)")
                print(f"    ~{len(baseline.splitlines())} lines after simplification")
                
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
                resume_run_dir = Path(resume_config["run_dir"])
                prev_run = RunInfo(resume_run_dir)
                debug = get_debug_manager(config)
                
                # Load expert responses from previous run
                expert_data = load_expert_responses_from_run(prev_run)
                if expert_data and "expert_review" in expert_data:
                    # Parse and load expert suggestions into state
                    from .agents.expert import parse_suggestions_from_response
                    expert_suggestions = {}
                    expert_raw_responses = {}
                    
                    for expert_id, raw_response in expert_data["expert_review"].items():
                        suggestions = parse_suggestions_from_response(raw_response, expert_id)
                        expert_suggestions[expert_id] = suggestions
                        expert_raw_responses[expert_id] = raw_response
                        print(f"  ✓ Loaded {expert_id}: {len(suggestions)} suggestions")
                    
                    state["expert_suggestions"] = expert_suggestions
                    state["expert_raw_responses"] = expert_raw_responses
                    
                    # Copy files to new debug directory
                    if debug.enabled:
                        import shutil
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
                    print("  ⚠ Could not load expert responses from previous run")
                    print("  → Running expert review fresh...")
                    # Fall through to run fresh
                    pass
                
                if state.get("expert_suggestions"):
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
                    debug.save_expert_review(
                        state["expert_raw_responses"][expert.agent_id],
                        expert.name,
                        suggestions,
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
                resume_run_dir = Path(resume_config["run_dir"])
                prev_run = RunInfo(resume_run_dir)
                debug = get_debug_manager(config)
                
                # Load discussion responses and parse adoption lists
                expert_data = load_expert_responses_from_run(prev_run)
                if expert_data and "full_discussion" in expert_data:
                    from .agents.expert import parse_adoption_list_from_response, AdoptionList
                    adoption_lists = {}
                    discussion_raw_responses = {}
                    
                    for expert_id, raw_response in expert_data["full_discussion"].items():
                        adopted_ids = parse_adoption_list_from_response(raw_response)
                        adoption_lists[expert_id] = AdoptionList(
                            expert_id=expert_id,
                            adopted_ids=adopted_ids
                        )
                        discussion_raw_responses[expert_id] = raw_response
                        print(f"  ✓ Loaded {expert_id}: {len(adopted_ids)} adopted")
                    
                    state["adoption_lists"] = adoption_lists
                    state["discussion_raw_responses"] = discussion_raw_responses
                    
                    # Copy files to new debug directory
                    if debug.enabled:
                        import shutil
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
                    print("  ⚠ Could not load discussion responses from previous run")
                    print("  → Running full discussion fresh...")
                    pass
                
                if state.get("adoption_lists"):
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
                    debug.save_discussion(
                        state["discussion_raw_responses"][expert.agent_id],
                        expert.name,
                        adoption_list,
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
        
        Output:
        - Raw markdown (no post-processing applied)
        - Saved to debug output for inspection
        - Stored in writer_outputs for translation phase
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
        
        Translates writer outputs (raw markdown, no post-processing).
        Both original and translated outputs are saved to debug.
        
        Input: writer_outputs (raw markdown from writer)
        Output: translated_outputs (raw markdown, no post-processing)
        """
        translator_configs = state.get("translator_configs", [])
        
        if not translator_configs:
            return state
        
        print("\n[Phase 5] Translating outputs...")
        
        # Check if we should skip this phase (resume mode)
        resume_config = state.get("_resume_config", {})
        if resume_config:
            reuse_stages = resume_config.get("reuse_stages", {})
            resume_run_dir = Path(resume_config["run_dir"])
            prev_run = RunInfo(resume_run_dir)
            
            # If explicitly marked to reuse, load it
            if reuse_stages.get("translation"):
                print("  ⏭️  Reusing translations from previous run")
                # Copy all translation related files to new directory
                debug = get_debug_manager(config)
                if debug.enabled:
                    import shutil
                    # Copy all translation related files
                    translation_files = prev_run.get_stage_files("translation")
                    if translation_files:
                        for file_info in translation_files:
                            try:
                                dest = debug.run_dir / file_info["filename"]
                                shutil.copy2(file_info["path"], dest)
                                print(f"  💾 Copied: {file_info['filename']}")
                            except Exception as e:
                                print(f"  ⚠ Failed to copy {file_info['filename']}: {e}")
                    # Load translation outputs for state
                    translated_outputs = load_translation_outputs_from_run(prev_run)
                    if translated_outputs:
                        state["translated_outputs"] = translated_outputs
                        print(f"  ✓ Loaded {len(translated_outputs)} translation(s)")
                        for key in translated_outputs.keys():
                            print(f"    - {key}")
                        return state
                    else:
                        print("  ⚠ Could not load translation outputs from previous run")
                        print("  ℹ️  Will continue to translation phase to generate translations")
                        # Don't return - continue to translation phase
                else:
                    # Debug not enabled, try to load anyway
                    translated_outputs = load_translation_outputs_from_run(prev_run)
                    if translated_outputs:
                        state["translated_outputs"] = translated_outputs
                        print(f"  ✓ Loaded {len(translated_outputs)} translation(s)")
                        for key in translated_outputs.keys():
                            print(f"    - {key}")
                        return state
                    else:
                        print("  ⚠ Could not load translation outputs from previous run")
                        print("  ℹ️  Will continue to translation phase to generate translations")
            
            # If not in reuse list but output exists, ask user
            elif prev_run.has_stage_output("translation") and "translation" not in reuse_stages:
                from ..resume import ask_reuse_stage
                should_reuse = ask_reuse_stage("translation", prev_run)
                if should_reuse:
                    translated_outputs = load_translation_outputs_from_run(prev_run)
                    if translated_outputs:
                        state["translated_outputs"] = translated_outputs
                        print(f"  ✓ Loaded {len(translated_outputs)} translation(s)")
                        for key in translated_outputs.keys():
                            print(f"    - {key}")
                        # Copy all translation files to new directory
                        debug = get_debug_manager(config)
                        if debug.enabled:
                            import shutil
                            # Copy all translation related files
                            translation_files = prev_run.get_stage_files("translation")
                            if translation_files:
                                for file_info in translation_files:
                                    try:
                                        dest = debug.run_dir / file_info["filename"]
                                        shutil.copy2(file_info["path"], dest)
                                        print(f"  💾 Copied: {file_info['filename']}")
                                    except Exception as e:
                                        print(f"  ⚠ Failed to copy {file_info['filename']}: {e}")
                        # Mark as reused
                        reuse_stages["translation"] = True
                        return state
        
        debug = get_debug_manager(config)
        
        writer_outputs = state.get("writer_outputs", {})
        translated = {}
        
        for tr_config in translator_configs:
            source_lang = tr_config["source_lang"]
            target_lang = tr_config["target_lang"]
            model = tr_config["model"]
            
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
                
                # Translate the content using unified translation function
                try:
                    if debug.enabled:
                        debug.save_translation(content, output_key, target_key, is_before=True)
                    
                    # Import unified translation function from translate_only.py
                    import sys
                    import importlib.util
                    
                    # Get path to translate_only.py
                    translate_only_path = Path(__file__).parent.parent.parent / "translate_only.py"
                    
                    if translate_only_path.exists():
                        # Dynamically import translate_content function
                        spec = importlib.util.spec_from_file_location("translate_only", translate_only_path)
                        translate_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(translate_module)
                        translate_content = translate_module.translate_content
                        
                        translated_content = translate_content(
                            content=content,
                            source_lang=source_lang,
                            target_lang=target_lang,
                            model=model,
                            config=config,
                            output_key=f"{output_key} → {target_key}",
                        )
                    else:
                        # Fallback: use translator directly (old behavior)
                        translator = TranslatorAgent(
                            source_language=source_lang,
                            target_language=target_lang,
                            model=model,
                            config=config,
                        )
                        translated_content = translator.translate(content, "general")
                        translated_content = clean_translated_content(translated_content)
                        if not translated_content or len(translated_content.strip()) == 0:
                            raise ValueError(f"Translation returned empty content")
                        print(f"  ✓ Translated: {output_key} → {target_key}")
                    
                    translated[target_key] = translated_content
                    
                    if debug.enabled:
                        debug.save_translation(translated_content, output_key, target_key, is_before=False)
                except Exception as e:
                    error_msg = f"Translation failed for {output_key} → {target_lang}: {e}"
                    print(f"  ✗ {error_msg}")
                    state["errors"].append(error_msg)
        
        state["translated_outputs"] = translated
        
        # Debug: Show translation results
        if translated:
            print(f"\n  ✓ Translation complete: {len(translated)} output(s) translated")
            for key in translated.keys():
                print(f"    - {key}")
        else:
            print("\n  ⚠ No translations generated - check translator configs")
        
        return state
    
    def run_post_processing(state: WorkflowState) -> WorkflowState:
        """
        Phase 6: Post-processing.
        
        Apply text transformations to both English and translated outputs.
        
        Process:
        1. Takes raw markdown from writer_outputs (English)
        2. Takes raw markdown from translated_outputs (e.g., Chinese)
        3. Applies link normalization to both:
           - Convert 'LeetCode 11' → '[LeetCode 11 - Title](url) · [Solution](github_url)'
           - Normalize LeetCode URLs
        4. Generates comparison file (before/after)
        
        Output: final_outputs (post-processed markdown for both languages)
        """
        print("\n[Phase 6] Post-processing...")
        debug = get_debug_manager(config)
        
        # Merge writer outputs (English, raw) and translations (e.g., Chinese, raw)
        # Post-processing will normalize links for BOTH English and translated outputs
        writer_outputs = state.get("writer_outputs", {})
        translated_outputs = state.get("translated_outputs", {})
        
        all_outputs = {}
        all_outputs.update(writer_outputs)  # English: raw markdown
        all_outputs.update(translated_outputs)  # Translated: raw markdown
        
        # Debug: Show what will be processed
        writer_keys = list(writer_outputs.keys())
        translated_keys = list(translated_outputs.keys())
        print(f"\n  📋 Post-processing summary:")
        print(f"    English outputs: {len(writer_keys)}")
        if writer_keys:
            for key in writer_keys:
                print(f"      - {key}")
        print(f"    Translated outputs: {len(translated_keys)}")
        if translated_keys:
            for key in translated_keys:
                print(f"      - {key}")
        else:
            print("      ⚠ No translated outputs found - zh-TW will not be post-processed!")
            print("      ℹ️  Make sure translation phase completed successfully")
            # In resume mode, check if we should have translations
            if resume_config:
                print("      🔍 Resume mode: Checking if translations should be loaded...")
                reuse_stages = resume_config.get("reuse_stages", {})
                if reuse_stages.get("translation"):
                    print("      ⚠ Translation marked for reuse but not found in state!")
                    print("      ℹ️  Try re-running translation phase or check previous run")
        
        print(f"    Total outputs to process: {len(all_outputs)}")
        
        # Critical check: If we have writer outputs but no translations, warn
        if writer_keys and not translated_keys:
            print("\n  ⚠️  WARNING: English outputs exist but no translations found!")
            print("     This means zh-TW files will NOT be generated.")
            print("     Possible causes:")
            print("     1. Translation phase was skipped or failed")
            print("     2. Translation phase was not executed")
            print("     3. In resume mode: translations not loaded from previous run")
        
        # Check if resuming and ask user whether to run post-processing
        resume_config = state.get("_resume_config", {})
        reuse_stages = resume_config.get("reuse_stages", {}) if resume_config else {}
        
        # If in resume mode and post_processing is marked for reuse, check for existing output
        if resume_config and reuse_stages.get("post_processing"):
            run_dir = resume_config.get("run_dir")
            if run_dir:
                prev_run = RunInfo(Path(run_dir))
                if prev_run.has_stage_output("post_processing"):
                    cached_outputs = load_post_processing_outputs_from_run(prev_run)
                    if cached_outputs:
                        # Check if cached outputs include all current outputs (including translations)
                        current_outputs = set(all_outputs.keys())
                        cached_keys = set(cached_outputs.keys())
                        
                        # Debug: Show what's in cache vs what we need
                        print(f"\n  📦 Cached post-processing outputs: {sorted(cached_keys)}")
                        print(f"  📋 Current outputs to process: {sorted(current_outputs)}")
                        
                        missing = current_outputs - cached_keys
                        if missing:
                            print(f"  ⚠ Missing outputs in cache: {sorted(missing)}")
                            print(f"  ℹ️  Will re-run post-processing to include missing outputs")
                            # Don't reuse, continue to post-processing
                        else:
                            should_reuse = ask_reuse_stage("post_processing", prev_run)
                            if should_reuse:
                                print("  ⏭️  Reusing post-processing output from previous run")
                                # Merge cached with any new outputs (shouldn't happen, but safe)
                                final_cached = cached_outputs.copy()
                                final_cached.update(all_outputs)  # Add any new outputs
                                state["final_outputs"] = final_cached
                                return state
                    else:
                        print("  ⚠ Post-processing outputs not found in previous run; re-running post-processing")
        
        # Ask user if they want to run post-processing
        print("\n  Post-processing will:")
        print("    - Convert 'LeetCode 11' → '[LeetCode 11 - Title](url) · [Solution](github_url)'")
        print("    - Normalize LeetCode URLs")
        print("    - Generate comparison file")
        
        while True:
            choice = input("  Run post-processing? [Y/n]: ").strip().lower()
            if choice in ['', 'y', 'yes']:
                break
            elif choice in ['n', 'no']:
                print("  ⏭️  Skipping post-processing")
                # Use writer/translation outputs as final outputs
                state["final_outputs"] = all_outputs
                return state
            else:
                print("  ⚠ Please enter 'y' or 'n'")
        
        # Pass problems data to PostProcessor for link generation
        problems_data = state.get("problems", {})
        if not problems_data:
            print("  ⚠ Warning: No problems data in state - Solution links will not be added")
        else:
            print(f"  ℹ️  Loaded {len(problems_data)} problems for Solution link generation")
        processor = PostProcessor(config, problems=problems_data)
        
        # Apply post-processing
        final_outputs = {}
        post_processing_comparison = {}  # Store before/after for comparison
        
        if not all_outputs:
            print("  ⚠ No outputs to process!")
            state["final_outputs"] = {}
            return state
        
        print(f"\n  🔄 Processing {len(all_outputs)} output(s)...")
        for key, content in all_outputs.items():
            if debug.enabled:
                debug.save_post_processing(content, key, is_before=True)
            
            # Show which language is being processed
            lang_indicator = "🌐" if "zh-TW" in key or "zh" in key.lower() else "🇺🇸"
            print(f"  {lang_indicator} Processing: {key} ({len(content)} chars)")
            
            processed = processor.process(content)
            final_outputs[key] = processed
            
            # Store comparison for later saving
            post_processing_comparison[key] = {
                "before": content,
                "after": processed
            }
            
            print(f"  ✓ Processed: {key} -> {len(processed)} chars")
            
            if debug.enabled:
                debug.save_post_processing(processed, key, is_before=False)
        
        print(f"\n  ✓ Post-processing complete: {len(final_outputs)} output(s) processed")
        
        # Save post-processing comparison to markdown file
        _save_post_processing_comparison(post_processing_comparison, config)
        
        state["final_outputs"] = final_outputs
        return state
    
    def save_outputs(state: WorkflowState) -> WorkflowState:
        """
        Phase 7: Save all outputs to files.
        
        Uses the standalone convert_to_html.py tool for HTML conversion.
        """
        print("\n[Phase 7] Saving outputs...")
        
        final_outputs = state.get("final_outputs", {})
        
        if not final_outputs:
            print("  ⚠ No outputs to save")
            # Debug: Check what's in state
            writer_outputs = state.get("writer_outputs", {})
            translated_outputs = state.get("translated_outputs", {})
            print(f"    writer_outputs keys: {list(writer_outputs.keys())}")
            print(f"    translated_outputs keys: {list(translated_outputs.keys())}")
            return state
        
        # Debug: Show what will be saved
        print(f"  📦 Saving {len(final_outputs)} output(s):")
        for key in final_outputs.keys():
            lang_indicator = "🌐" if "zh-TW" in key or "zh" in key.lower() else "🇺🇸"
            print(f"    {lang_indicator} {key}")
        
        try:
            saved = save_all_markmaps(final_outputs, config)
            state["messages"].append(f"Saved {len(saved)} output files")
            
            # Show what was actually saved
            print(f"\n  ✓ Saved {len(saved)} output file(s):")
            for output_key, file_paths in saved.items():
                # save_all_markmaps returns: {"md": Path, "html": Path}
                md_file = file_paths.get("md", "N/A")
                html_file = file_paths.get("html", "N/A")
                print(f"    - {output_key}:")
                if isinstance(md_file, Path):
                    print(f"      MD: {md_file.name}")
                else:
                    print(f"      MD: {md_file}")
                if isinstance(html_file, Path):
                    print(f"      HTML: {html_file.name}")
                else:
                    print(f"      HTML: {html_file}")
        except Exception as e:
            error_msg = f"Error saving outputs: {e}"
            state["errors"].append(error_msg)
            print(f"  ✗ {error_msg}")
            import traceback
            traceback.print_exc()
        
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
    
    # Pass resume config if available
    if "_resume_config" in data:
        initial_state["_resume_config"] = data["_resume_config"]
    
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
    
    # Pass resume config if available
    if "_resume_config" in data:
        initial_state["_resume_config"] = data["_resume_config"]
    
    result = graph.invoke(initial_state)
    return result

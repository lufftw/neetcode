# =============================================================================
# LangGraph Pipeline
# =============================================================================
# Structure Specification based multi-agent system for Markmap generation.
#
# Workflow:
#   - Planners produce Structure Spec (YAML), not Markdown
#   - Strategists discuss content strategy, not formatting
#   - Integrator consolidates with consensus detection
#   - Evaluators assess Structure Spec quality
#   - Writer is the ONLY agent producing Markdown
# =============================================================================

from __future__ import annotations

import asyncio
from typing import Any, TypedDict

from langgraph.graph import StateGraph, END

from .agents.planner import create_planners
from .agents.strategist import create_strategists
from .agents.integrator import create_integrator
from .agents.evaluator import create_evaluators, aggregate_evaluations
from .agents.writer import create_writer
from .agents.translator import create_translators, TranslatorAgent
from .schema import StructureSpec, validate_final_output
from .memory.stm import update_stm
from .output.html_converter import save_all_markmaps
from .post_processing import PostProcessor
from .debug_output import get_debug_manager, reset_debug_manager
from .config_loader import ConfigLoader


class WorkflowState(TypedDict, total=False):
    """State schema for the LangGraph workflow."""
    
    # Input data
    ontology: dict[str, Any]
    problems: dict[str, Any]
    patterns: dict[str, Any]
    roadmaps: dict[str, Any]
    
    # Phase 1: Structure Generation
    structure_spec_generalist_en: StructureSpec
    structure_spec_specialist_en: StructureSpec
    current_structure_spec: StructureSpec
    raw_planner_response: str
    
    # Phase 2: Content Strategy Optimization
    current_round: int
    max_discussion_rounds: int
    current_phase: str  # "divergent" or "convergent"
    suggestions_round_1: list[dict]
    suggestions_round_2: list[dict]
    suggestions_round_3: list[dict]
    other_suggestions: str
    previous_consensus: list[Any]
    previous_conflicts: list[Any]
    integration_result: dict[str, Any]
    should_continue_discussion: bool
    
    # Phase 3: Evaluation
    evaluator_results: dict[str, dict]
    evaluator_suggestions: list[str]
    evaluation_approved: bool
    
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


def build_markmap_graph(config: dict[str, Any] | None = None) -> StateGraph:
    """
    Build the LangGraph workflow for Markmap generation.
    
    Workflow:
    1. Generate Structure Specifications (Planners)
    2. Optimize content strategy (Strategists + Integrator, N rounds)
    3. Evaluate structure quality (Evaluators)
    4. Render final Markmap (Writer)
    5. Translate if needed
    6. Post-process and save
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Compiled LangGraph workflow
    """
    config = config or ConfigLoader.get_config()
    workflow_config = config.get("workflow", {})
    naming_config = config.get("output", {}).get("naming", {})
    
    max_discussion_rounds = workflow_config.get("max_discussion_rounds", 3)
    consensus_threshold = workflow_config.get("consensus_threshold", 0.8)
    
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
        """Initialize workflow state."""
        state["current_round"] = 0
        state["max_discussion_rounds"] = max_discussion_rounds
        state["current_phase"] = "divergent"
        state["messages"] = []
        state["errors"] = []
        state["writer_outputs"] = {}
        state["translated_outputs"] = {}
        state["final_outputs"] = {}
        state["should_continue_discussion"] = True
        state["previous_consensus"] = []
        state["previous_conflicts"] = []
        
        # Store translator configs
        state["translator_configs"] = create_translators(config)
        
        # Initialize debug output manager
        reset_debug_manager()
        debug = get_debug_manager(config)
        if debug.enabled:
            print(f"\n📊 Debug output enabled")
        
        update_stm("Workflow initialized", category="system")
        return state
    
    def generate_structure_specs(state: WorkflowState) -> WorkflowState:
        """
        Phase 1: Generate Structure Specifications.
        
        Planners produce Structure Spec (YAML), not Markdown.
        """
        print("\n[Phase 1] Generating Structure Specifications...")
        debug = get_debug_manager(config)
        
        # Print data summary
        problems = state.get("problems", {})
        ontology = state.get("ontology", {})
        patterns = state.get("patterns", {})
        
        print(f"  📊 Input data summary:")
        print(f"     Problems: {len(problems)} loaded")
        print(f"     Ontology: {len(ontology)} categories")
        print(f"     Patterns: {len(patterns)} pattern docs")
        
        planners = create_planners(config)
        
        first_spec = None
        for planner_id, planner in planners.items():
            try:
                state = planner.process(state)
                print(f"  ✓ {planner_id} completed")
                update_stm(f"Structure Spec: {planner_id}", category="generation")
                
                # Track first successful spec
                spec_key = f"structure_spec_{planner.agent_id}"
                if spec_key in state and first_spec is None:
                    first_spec = state[spec_key]
                
                # Save debug output
                if debug.enabled and "raw_planner_response" in state:
                    debug.save_baseline(
                        state["raw_planner_response"],
                        planner_id.split("_")[0],
                        "en"
                    )
                    
            except Exception as e:
                error_msg = f"Error in {planner_id}: {e}"
                state["errors"].append(error_msg)
                print(f"  ✗ {error_msg}")
        
        # Set current spec to first successful one
        if first_spec:
            state["current_structure_spec"] = first_spec
        
        return state
    
    def run_strategist_round(state: WorkflowState) -> WorkflowState:
        """
        Phase 2: Run strategist optimization round.
        
        Strategists suggest content strategy improvements.
        Integrator consolidates suggestions.
        """
        current_round = state.get("current_round", 0) + 1
        state["current_round"] = current_round
        
        # First round is divergent, later rounds are convergent
        state["current_phase"] = "divergent" if current_round == 1 else "convergent"
        
        print(f"\n[Phase 2] Strategy round {current_round}/{max_discussion_rounds}...")
        debug = get_debug_manager(config)
        
        strategists = create_strategists(config)
        integrator = create_integrator(config)
        
        # Initialize suggestions for this round
        suggestions_key = f"suggestions_round_{current_round}"
        state[suggestions_key] = []
        
        # Run all strategists (can be parallelized in async version)
        for strategist in strategists:
            try:
                state = strategist.process(state)
                print(f"    ✓ {strategist.name}")
                
                # Save debug output
                if suggestions_key in state and state[suggestions_key]:
                    debug.save_optimizer_suggestion(
                        str(state[suggestions_key][-1]),
                        strategist.name,
                        current_round,
                        "structure_spec"
                    )
            except Exception as e:
                print(f"    ✗ {strategist.name}: {e}")
        
        # Run integrator
        try:
            state = integrator.process(state)
            print(f"    ✓ Integrator consolidated")
            
            # Save debug output
            if "integration_result" in state:
                debug.save_summarizer_output(
                    str(state["integration_result"]),
                    current_round,
                    "structure_spec"
                )
        except Exception as e:
            print(f"    ✗ Integrator: {e}")
        
        update_stm(f"Strategy round {current_round} completed", category="optimization")
        return state
    
    def should_continue_strategy(state: WorkflowState) -> str:
        """Decide whether to continue strategy rounds or proceed to evaluation."""
        current_round = state.get("current_round", 0)
        max_rounds = state.get("max_discussion_rounds", 3)
        should_continue = state.get("should_continue_discussion", True)
        
        if not should_continue:
            print(f"    → Consensus reached, proceeding to evaluation")
            return "evaluate"
        
        if current_round >= max_rounds:
            print(f"    → Max rounds reached, proceeding to evaluation")
            return "evaluate"
        
        return "strategize"
    
    def run_evaluation(state: WorkflowState) -> WorkflowState:
        """
        Phase 3: Evaluate the Structure Specification.
        
        Evaluators assess structure quality, not formatting.
        """
        print("\n[Phase 3] Evaluating Structure Specification...")
        debug = get_debug_manager(config)
        
        evaluators = create_evaluators(config)
        state["evaluator_results"] = {}
        
        for evaluator in evaluators:
            try:
                state = evaluator.process(state)
                print(f"  ✓ {evaluator.name} evaluated")
                
                # Save debug output
                if evaluator.agent_id in state.get("evaluator_results", {}):
                    debug.save_judge_evaluation(
                        state["evaluator_results"][evaluator.agent_id],
                        evaluator.name,
                        "structure_spec"
                    )
            except Exception as e:
                print(f"  ✗ {evaluator.name}: {e}")
        
        # Aggregate evaluations
        avg_score, all_approved, suggestions = aggregate_evaluations(
            state.get("evaluator_results", {})
        )
        
        state["evaluation_approved"] = all_approved
        state["evaluator_suggestions"] = suggestions
        
        print(f"  → Average score: {avg_score:.1f}/10")
        print(f"  → Approved: {all_approved}")
        
        # Save consensus
        debug.save_consensus({
            "average_score": avg_score,
            "approved": all_approved,
            "suggestions": suggestions,
        })
        
        update_stm("Evaluation completed", category="evaluation")
        return state
    
    def run_writer(state: WorkflowState) -> WorkflowState:
        """
        Phase 4: Render final Markmap.
        
        Writer transforms Structure Spec into Markdown.
        This is the ONLY place that produces Markdown.
        """
        print("\n[Phase 4] Rendering final Markmap...")
        debug = get_debug_manager(config)
        
        writer = create_writer(config)
        
        try:
            # Save writer input
            debug.save_writer_input(
                str(state.get("current_structure_spec", "")),
                list(state.get("evaluator_results", {}).values()),
                state.get("evaluator_suggestions", []),
                "structure_spec"
            )
            
            state = writer.process(state)
            
            # Get the output
            final_markmap = state.get("final_markmap", "")
            
            # Validate output
            is_valid, validation_errors = validate_final_output(final_markmap)
            if not is_valid:
                print(f"  ⚠ Validation warnings: {validation_errors}")
            
            # Store in writer_outputs
            state["writer_outputs"]["general_en"] = final_markmap
            
            # Save writer output
            debug.save_writer_output(final_markmap, "general_en")
            
            print(f"  ✓ Markmap rendered ({len(final_markmap)} chars)")
            
        except Exception as e:
            print(f"  ✗ Writer error: {e}")
            state["errors"].append(f"Writer error: {e}")
        
        update_stm("Writer completed", category="writing")
        return state
    
    def run_translations(state: WorkflowState) -> WorkflowState:
        """
        Phase 5: Translate outputs for translate-mode languages.
        """
        translator_configs = state.get("translator_configs", [])
        
        if not translator_configs:
            return state
        
        print("\n[Phase 5] Translating outputs...")
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
                if source_lang in output_key:
                    target_key = output_key.replace(source_lang, target_lang)
                    
                    try:
                        debug.save_translation(content, output_key, target_key, is_before=True)
                        
                        translated_content = translator.translate(content, "general")
                        translated[target_key] = translated_content
                        print(f"  ✓ Translated: {output_key} → {target_key}")
                        
                        debug.save_translation(translated_content, output_key, target_key, is_before=False)
                    except Exception as e:
                        print(f"  ✗ Translation failed: {e}")
                        state["errors"].append(f"Translation error: {e}")
        
        state["translated_outputs"] = translated
        update_stm("Translations completed", category="translation")
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
            debug.save_post_processing(content, key, is_before=True)
            
            processed = processor.process(content)
            final_outputs[key] = processed
            print(f"  ✓ Processed: {key}")
            
            debug.save_post_processing(processed, key, is_before=False)
        
        state["final_outputs"] = final_outputs
        update_stm("Post-processing completed", category="post_processing")
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
    graph.add_node("generate_specs", generate_structure_specs)
    graph.add_node("strategize", run_strategist_round)
    graph.add_node("evaluate", run_evaluation)
    graph.add_node("write", run_writer)
    graph.add_node("translate", run_translations)
    graph.add_node("post_process", run_post_processing)
    graph.add_node("save", save_outputs)
    
    # Add edges
    graph.set_entry_point("initialize")
    graph.add_edge("initialize", "generate_specs")
    graph.add_edge("generate_specs", "strategize")
    
    # Conditional edge for strategy loop
    graph.add_conditional_edges(
        "strategize",
        should_continue_strategy,
        {
            "strategize": "strategize",
            "evaluate": "evaluate",
        }
    )
    
    graph.add_edge("evaluate", "write")
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
        "ontology": data.get("ontology", {}),
        "problems": data.get("problems", {}),
        "patterns": data.get("patterns", {}),
        "roadmaps": data.get("roadmaps", {}),
    }
    
    result = graph.invoke(initial_state)
    return result


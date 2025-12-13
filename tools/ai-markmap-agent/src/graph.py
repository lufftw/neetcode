# =============================================================================
# LangGraph Pipeline
# =============================================================================
# Main workflow orchestration using LangGraph.
# Coordinates all agents through the multi-agent pipeline.
# =============================================================================

from __future__ import annotations

import asyncio
from typing import Any, TypedDict

from langgraph.graph import StateGraph, END

from .agents.generator import GeneralistAgent, SpecialistAgent, TranslatorAgent, create_generators, create_translators
from .agents.optimizer import OptimizerAgent, create_optimizers
from .agents.summarizer import SummarizerAgent
from .agents.judge import JudgeAgent, create_judges, aggregate_votes
from .compression.compressor import get_compressor
from .memory.stm import update_stm, get_recent_stm
from .output.html_converter import MarkMapHTMLConverter, save_all_markmaps
from .config_loader import ConfigLoader


class WorkflowState(TypedDict, total=False):
    """State schema for the LangGraph workflow."""
    
    # Input data
    ontology: dict[str, Any]
    problems: dict[str, Any]
    patterns: dict[str, Any]
    roadmaps: dict[str, Any]
    
    # Baseline outputs (for "generate" mode languages only)
    baseline_general_en: str
    baseline_general_zh_TW: str  # Note: - replaced with _ for valid Python
    baseline_specialist_en: str
    baseline_specialist_zh_TW: str
    
    # Current state for optimization
    current_markmap: str
    current_type: str  # "general" or "specialist"
    current_language: str  # "en" or "zh-TW"
    current_round: int
    total_rounds: int
    
    # Optimization history
    optimization_history: list[dict]
    suggestions_round_1: list[dict]
    suggestions_round_2: list[dict]
    suggestions_round_3: list[dict]
    
    # Round outputs
    markmap_round_1: str
    markmap_round_2: str
    markmap_round_3: str
    
    # Final outputs
    candidates: dict[str, str]  # Only "generate" mode outputs (for optimization)
    translated_outputs: dict[str, str]  # "translate" mode outputs
    judge_evaluations: dict[str, dict]
    final_outputs: dict[str, str]  # All outputs (generated + translated)
    
    # Translation config
    translator_configs: list[dict]
    
    # Metadata
    messages: list[str]
    errors: list[str]


def build_markmap_graph(config: dict[str, Any] | None = None) -> StateGraph:
    """
    Build the LangGraph workflow for Markmap generation.
    
    The workflow:
    1. Generate baselines (parallel: 2 types × 2 languages = 4)
    2. For each baseline:
       a. Run optimization rounds
       b. Optimizers debate and suggest improvements
       c. Summarizer consolidates suggestions
    3. Judges evaluate final outputs
    4. Save all 4 final files
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Compiled LangGraph workflow
    """
    config = config or ConfigLoader.get_config()
    workflow_config = config.get("workflow", {})
    naming_config = config.get("output", {}).get("naming", {})
    
    # Get languages and types from config
    languages = naming_config.get("languages", ["en", "zh-TW"])
    types_config = naming_config.get("types", {
        "general": {"generator": "generalist"},
        "specialist": {"generator": "specialist"},
    })
    
    total_rounds = workflow_config.get("optimization_rounds", 3)
    
    # Create the state graph
    graph = StateGraph(WorkflowState)
    
    # =========================================================================
    # Node Functions
    # =========================================================================
    
    def initialize(state: WorkflowState) -> WorkflowState:
        """Initialize workflow state."""
        state["current_round"] = 0
        state["total_rounds"] = total_rounds
        state["optimization_history"] = []
        state["messages"] = []
        state["errors"] = []
        state["final_outputs"] = {}
        state["translated_outputs"] = {}
        
        # Store translator configs for later use
        state["translator_configs"] = create_translators(config)
        
        update_stm("Workflow initialized", category="system")
        return state
    
    def generate_baselines(state: WorkflowState) -> WorkflowState:
        """Generate all 4 baseline Markmaps in parallel."""
        print("\n[Phase 1] Generating baselines...")
        
        generators = create_generators(config)
        
        for agent_id, agent in generators.items():
            try:
                state = agent.process(state)
                print(f"  ✓ {agent_id} completed")
                update_stm(f"Baseline generated: {agent_id}", category="generation")
            except Exception as e:
                error_msg = f"Error in {agent_id}: {e}"
                state["errors"].append(error_msg)
                print(f"  ✗ {error_msg}")
        
        return state
    
    def prepare_optimization(state: WorkflowState) -> WorkflowState:
        """Prepare state for optimization rounds."""
        # Get the list of baselines to optimize
        baselines = {}
        
        for output_type in types_config.keys():
            for lang in languages:
                lang_key = lang.replace("-", "_")
                baseline_key = f"baseline_{output_type}_{lang_key}"
                if baseline_key in state and state[baseline_key]:
                    output_key = f"{output_type}_{lang}"
                    baselines[output_key] = state[baseline_key]
        
        state["candidates"] = baselines
        return state
    
    def run_optimization_round(state: WorkflowState) -> WorkflowState:
        """Run a single optimization round with all optimizers."""
        current_round = state.get("current_round", 0) + 1
        state["current_round"] = current_round
        
        print(f"\n[Phase 2] Optimization round {current_round}/{total_rounds}...")
        
        optimizers = create_optimizers(config)
        summarizer = SummarizerAgent(config)
        
        # Process each candidate
        for output_key, markmap in state.get("candidates", {}).items():
            print(f"  Optimizing: {output_key}")
            
            # Set current markmap for this candidate
            state["current_markmap"] = markmap
            
            # Get suggestions from all optimizers
            suggestions_key = f"suggestions_round_{current_round}"
            state[suggestions_key] = []
            
            for optimizer in optimizers:
                try:
                    state = optimizer.process(state)
                    print(f"    ✓ {optimizer.name}")
                except Exception as e:
                    print(f"    ✗ {optimizer.name}: {e}")
            
            # Summarizer consolidates suggestions
            try:
                state = summarizer.process(state)
                print(f"    ✓ Summarizer consolidated")
                
                # Update the candidate with improved version
                state["candidates"][output_key] = state["current_markmap"]
            except Exception as e:
                print(f"    ✗ Summarizer: {e}")
        
        update_stm(f"Optimization round {current_round} completed", category="optimization")
        return state
    
    def should_continue_optimization(state: WorkflowState) -> str:
        """Decide whether to continue optimization or proceed to judging."""
        current_round = state.get("current_round", 0)
        total = state.get("total_rounds", 3)
        
        if current_round < total:
            return "optimize"
        return "judge"
    
    def run_judging(state: WorkflowState) -> WorkflowState:
        """Run judges to evaluate final candidates."""
        print("\n[Phase 3] Judging...")
        
        judges = create_judges(config)
        state["judge_evaluations"] = {}
        
        for judge in judges:
            try:
                state = judge.process(state)
                print(f"  ✓ {judge.name} evaluated")
            except Exception as e:
                print(f"  ✗ {judge.name}: {e}")
        
        # Enable debate if configured
        if workflow_config.get("enable_debate", False):
            print("  Running judge debate...")
            for judge in judges:
                try:
                    for candidate, markmap in state.get("candidates", {}).items():
                        result = judge.debate(markmap, state.get("judge_evaluations", {}))
                        state["judge_evaluations"][judge.agent_id][candidate].update(result)
                except Exception as e:
                    print(f"    ✗ Debate error: {e}")
        
        return state
    
    def run_translations(state: WorkflowState) -> WorkflowState:
        """Translate optimized outputs for translate-mode languages."""
        translator_configs = state.get("translator_configs", [])
        
        if not translator_configs:
            return state
        
        print("\n[Phase 4] Translating outputs...")
        
        candidates = state.get("candidates", {})
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
            
            # Translate each output type (general, specialist)
            for output_type in types_config.keys():
                source_key = f"{output_type}_{source_lang}"
                target_key = f"{output_type}_{target_lang}"
                
                if source_key in candidates:
                    try:
                        translated_content = translator.translate(
                            candidates[source_key],
                            output_type,
                        )
                        translated[target_key] = translated_content
                        print(f"  ✓ Translated: {source_key} → {target_key}")
                    except Exception as e:
                        print(f"  ✗ Translation failed {source_key} → {target_key}: {e}")
                        state["errors"].append(f"Translation error: {e}")
        
        state["translated_outputs"] = translated
        update_stm("Translations completed", category="translation")
        return state
    
    def finalize_outputs(state: WorkflowState) -> WorkflowState:
        """Finalize and prepare outputs for saving."""
        print("\n[Phase 5] Finalizing outputs...")
        
        # Merge generated (optimized) and translated outputs
        final_outputs = {}
        
        # Add optimized outputs (from generate mode)
        for key, content in state.get("candidates", {}).items():
            final_outputs[key] = content
        
        # Add translated outputs (from translate mode)
        for key, content in state.get("translated_outputs", {}).items():
            final_outputs[key] = content
        
        state["final_outputs"] = final_outputs
        
        # Log final scores if available
        if state.get("judge_evaluations"):
            winner, score, details = aggregate_votes(state["judge_evaluations"])
            print(f"  Judge consensus score: {score:.1f}/100")
            update_stm(f"Final score: {score:.1f}/100", category="evaluation")
        
        update_stm("Outputs finalized", category="system")
        return state
    
    def save_outputs(state: WorkflowState) -> WorkflowState:
        """Save all final outputs to files."""
        print("\n[Phase 6] Saving outputs...")
        
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
    graph.add_node("generate_baselines", generate_baselines)
    graph.add_node("prepare_optimization", prepare_optimization)
    graph.add_node("optimize", run_optimization_round)
    graph.add_node("judge", run_judging)
    graph.add_node("translate", run_translations)  # New: translate after judging
    graph.add_node("finalize", finalize_outputs)
    graph.add_node("save", save_outputs)
    
    # Add edges
    # Flow: initialize → generate → prepare → optimize (loop) → judge → translate → finalize → save
    graph.set_entry_point("initialize")
    graph.add_edge("initialize", "generate_baselines")
    graph.add_edge("generate_baselines", "prepare_optimization")
    graph.add_edge("prepare_optimization", "optimize")
    
    # Conditional edge for optimization loop
    graph.add_conditional_edges(
        "optimize",
        should_continue_optimization,
        {
            "optimize": "optimize",
            "judge": "judge",
        }
    )
    
    graph.add_edge("judge", "translate")  # After judging, translate
    graph.add_edge("translate", "finalize")
    graph.add_edge("finalize", "save")
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


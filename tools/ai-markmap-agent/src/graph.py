# =============================================================================
# LangGraph Pipeline V2
# =============================================================================
# Main workflow orchestration using LangGraph.
# V2 Features:
#   - Draft mode for baselines (no links)
#   - Multi-round debate between judges
#   - Dedicated Writer for final output with links
#   - Post-processing (LC → LeetCode)
# =============================================================================

from __future__ import annotations

import asyncio
from typing import Any, TypedDict

from langgraph.graph import StateGraph, END

from .agents.generator import (
    GeneralistAgent,
    SpecialistAgent,
    TranslatorAgent,
    create_generators,
    create_translators,
)
from .agents.optimizer import OptimizerAgent, create_optimizers
from .agents.summarizer import SummarizerAgent
from .agents.judge import JudgeAgent, create_judges, aggregate_votes, run_debate
from .agents.writer import WriterAgent, create_writer
from .compression.compressor import get_compressor
from .memory.stm import update_stm, get_recent_stm
from .output.html_converter import MarkMapHTMLConverter, save_all_markmaps
from .post_processing import PostProcessor, apply_post_processing
from .config_loader import ConfigLoader


class WorkflowState(TypedDict, total=False):
    """State schema for the LangGraph workflow V2."""
    
    # Input data
    ontology: dict[str, Any]
    problems: dict[str, Any]
    patterns: dict[str, Any]
    roadmaps: dict[str, Any]
    
    # Baseline outputs (Draft mode - no links)
    baseline_general_en: str
    baseline_general_zh_TW: str
    baseline_specialist_en: str
    baseline_specialist_zh_TW: str
    
    # Current state for optimization
    current_markmap: str
    current_type: str
    current_language: str
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
    
    # Candidates (optimized outputs)
    candidates: dict[str, str]
    
    # Judge evaluation results (V2)
    judge_evaluations: dict[str, dict]
    selected_markmap: dict[str, str]  # Per output_key: selected draft
    judge_feedback: dict[str, list[dict]]  # Per output_key: feedback list
    consensus_suggestions: dict[str, list[str]]  # Per output_key: suggestions
    
    # Writer outputs (V2)
    writer_outputs: dict[str, str]  # Final markmaps with links
    
    # Translation outputs
    translated_outputs: dict[str, str]
    translator_configs: list[dict]
    
    # Final outputs (after post-processing)
    final_outputs: dict[str, str]
    
    # Metadata
    messages: list[str]
    errors: list[str]


def build_markmap_graph(config: dict[str, Any] | None = None) -> StateGraph:
    """
    Build the LangGraph workflow V2 for Markmap generation.
    
    V2 Workflow:
    1. Generate baselines (Draft mode - no links)
    2. Optimization rounds (structure, naming, organization)
    3. Judge evaluation & debate (select best, provide feedback)
    4. Writer (apply feedback, add links, format)
    5. Translation (if needed)
    6. Post-processing (LC → LeetCode)
    7. Save outputs
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Compiled LangGraph workflow
    """
    config = config or ConfigLoader.get_config()
    workflow_config = config.get("workflow", {})
    naming_config = config.get("output", {}).get("naming", {})
    
    # Get languages config
    languages_config = naming_config.get("languages", {})
    if isinstance(languages_config, list):
        # Old format compatibility
        languages_config = {lang: {"mode": "generate"} for lang in languages_config}
    
    # Get types config
    types_config = naming_config.get("types", {
        "general": {"generator": "generalist"},
        "specialist": {"generator": "specialist"},
    })
    
    total_rounds = workflow_config.get("optimization_rounds", 3)
    enable_debate = workflow_config.get("enable_debate", True)
    max_debate_rounds = workflow_config.get("max_debate_rounds", 3)
    consensus_threshold = workflow_config.get("debate_consensus_threshold", 0.8)
    
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
        state["candidates"] = {}
        state["final_outputs"] = {}
        state["translated_outputs"] = {}
        state["writer_outputs"] = {}
        state["selected_markmap"] = {}
        state["judge_feedback"] = {}
        state["consensus_suggestions"] = {}
        
        # Store translator configs
        state["translator_configs"] = create_translators(config)
        
        update_stm("Workflow V2 initialized", category="system")
        return state
    
    def generate_baselines(state: WorkflowState) -> WorkflowState:
        """
        Phase 1: Generate baseline Markmaps in Draft mode.
        
        Draft mode means no concrete links - just structure and problem IDs.
        Links are added later by the Writer.
        """
        print("\n[Phase 1] Generating baselines (Draft mode)...")
        
        generators = create_generators(config)
        
        for agent_id, agent in generators.items():
            try:
                state = agent.process(state)
                print(f"  ✓ {agent_id} completed")
                update_stm(f"Draft baseline: {agent_id}", category="generation")
            except Exception as e:
                error_msg = f"Error in {agent_id}: {e}"
                state["errors"].append(error_msg)
                print(f"  ✗ {error_msg}")
        
        return state
    
    def prepare_optimization(state: WorkflowState) -> WorkflowState:
        """Prepare state for optimization rounds."""
        baselines = {}
        
        for output_type in types_config.keys():
            for lang, lang_config in languages_config.items():
                # Only include "generate" mode languages
                if lang_config.get("mode", "generate") != "generate":
                    continue
                if not lang_config.get("enabled", True):
                    continue
                
                lang_key = lang.replace("-", "_")
                baseline_key = f"baseline_{output_type}_{lang_key}"
                
                if baseline_key in state and state[baseline_key]:
                    output_key = f"{output_type}_{lang}"
                    baselines[output_key] = state[baseline_key]
        
        state["candidates"] = baselines
        return state
    
    def run_optimization_round(state: WorkflowState) -> WorkflowState:
        """
        Phase 2: Run optimization round.
        
        Optimizers suggest structural improvements.
        Summarizer consolidates suggestions.
        """
        current_round = state.get("current_round", 0) + 1
        state["current_round"] = current_round
        
        print(f"\n[Phase 2] Optimization round {current_round}/{total_rounds}...")
        
        optimizers = create_optimizers(config)
        summarizer = SummarizerAgent(config)
        
        for output_key, markmap in state.get("candidates", {}).items():
            print(f"  Optimizing: {output_key}")
            
            state["current_markmap"] = markmap
            suggestions_key = f"suggestions_round_{current_round}"
            state[suggestions_key] = []
            
            for optimizer in optimizers:
                try:
                    state = optimizer.process(state)
                    print(f"    ✓ {optimizer.name}")
                except Exception as e:
                    print(f"    ✗ {optimizer.name}: {e}")
            
            try:
                state = summarizer.process(state)
                print(f"    ✓ Summarizer consolidated")
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
        """
        Phase 3: Judge evaluation and debate.
        
        Judges evaluate candidates, debate to reach consensus,
        and provide structured feedback for the Writer.
        """
        print("\n[Phase 3] Evaluation & Debate...")
        
        judges = create_judges(config)
        candidates = state.get("candidates", {})
        
        if not judges:
            print("  ⚠ No judges configured")
            return state
        
        # Initial evaluation
        state["judge_evaluations"] = {}
        for judge in judges:
            try:
                state = judge.process(state)
                print(f"  ✓ {judge.name} evaluated")
            except Exception as e:
                print(f"  ✗ {judge.name}: {e}")
        
        # Run debate if enabled
        if enable_debate and len(judges) >= 2:
            print("  Running debate...")
            
            debate_result = run_debate(
                judges=judges,
                candidates=candidates,
                evaluations=state.get("judge_evaluations", {}),
                max_rounds=max_debate_rounds,
                consensus_threshold=consensus_threshold,
            )
            
            # Store results for each candidate
            for output_key in candidates.keys():
                state["selected_markmap"][output_key] = candidates[output_key]
                state["judge_feedback"][output_key] = debate_result.get("judge_feedback", [])
                state["consensus_suggestions"][output_key] = debate_result.get("consensus_suggestions", [])
            
            print(f"  ✓ Debate completed ({debate_result.get('debate_rounds', 0)} rounds)")
            print(f"  ✓ Consensus score: {debate_result.get('winning_score', 0):.1f}/100")
        else:
            # No debate - use initial evaluations
            winner, score, details = aggregate_votes(state.get("judge_evaluations", {}))
            print(f"  ✓ Evaluation score: {score:.1f}/100")
            
            for output_key in candidates.keys():
                state["selected_markmap"][output_key] = candidates[output_key]
                # Collect feedback from all judges
                feedback = []
                for judge_id, judge_evals in state.get("judge_evaluations", {}).items():
                    if output_key in judge_evals:
                        feedback.append({
                            "judge_id": judge_id,
                            "score": judge_evals[output_key].get("score", 0),
                            "strengths": judge_evals[output_key].get("strengths", []),
                            "improvements": judge_evals[output_key].get("improvements", []),
                        })
                state["judge_feedback"][output_key] = feedback
                state["consensus_suggestions"][output_key] = []
        
        update_stm("Judging completed", category="evaluation")
        return state
    
    def run_writer(state: WorkflowState) -> WorkflowState:
        """
        Phase 4: Final Markmap Writing.
        
        Writer takes the selected structure, applies judge feedback,
        adds proper links (GitHub/LeetCode), and formats output.
        """
        print("\n[Phase 4] Writing final Markmaps...")
        
        writer = create_writer(config)
        selected = state.get("selected_markmap", {})
        problems = state.get("problems", {})
        
        writer_outputs = {}
        
        for output_key, markmap in selected.items():
            print(f"  Writing: {output_key}")
            
            try:
                # Prepare state for writer
                writer_state = {
                    "selected_markmap": markmap,
                    "judge_feedback": state.get("judge_feedback", {}).get(output_key, []),
                    "consensus_suggestions": state.get("consensus_suggestions", {}).get(output_key, []),
                    "problems": problems,
                }
                
                writer_state = writer.process(writer_state)
                writer_outputs[output_key] = writer_state.get("final_markmap", markmap)
                print(f"    ✓ {output_key} written")
                
            except Exception as e:
                print(f"    ✗ Writer error for {output_key}: {e}")
                writer_outputs[output_key] = markmap  # Fallback to draft
        
        state["writer_outputs"] = writer_outputs
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
            
            for output_type in types_config.keys():
                source_key = f"{output_type}_{source_lang}"
                target_key = f"{output_type}_{target_lang}"
                
                if source_key in writer_outputs:
                    try:
                        translated_content = translator.translate(
                            writer_outputs[source_key],
                            output_type,
                        )
                        translated[target_key] = translated_content
                        print(f"  ✓ Translated: {source_key} → {target_key}")
                    except Exception as e:
                        print(f"  ✗ Translation failed: {e}")
                        state["errors"].append(f"Translation error: {e}")
        
        state["translated_outputs"] = translated
        update_stm("Translations completed", category="translation")
        return state
    
    def run_post_processing(state: WorkflowState) -> WorkflowState:
        """
        Phase 6: Post-processing.
        
        Apply text transformations (e.g., LC → LeetCode) by code,
        ensuring 100% consistency.
        """
        print("\n[Phase 6] Post-processing...")
        
        processor = PostProcessor(config)
        
        # Merge writer outputs and translations
        all_outputs = {}
        all_outputs.update(state.get("writer_outputs", {}))
        all_outputs.update(state.get("translated_outputs", {}))
        
        # Apply post-processing
        final_outputs = {}
        for key, content in all_outputs.items():
            processed = processor.process(content)
            final_outputs[key] = processed
            print(f"  ✓ Processed: {key}")
        
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
    graph.add_node("generate_baselines", generate_baselines)
    graph.add_node("prepare_optimization", prepare_optimization)
    graph.add_node("optimize", run_optimization_round)
    graph.add_node("judge", run_judging)
    graph.add_node("write", run_writer)
    graph.add_node("translate", run_translations)
    graph.add_node("post_process", run_post_processing)
    graph.add_node("save", save_outputs)
    
    # Add edges
    # V2 Flow: init → generate → prepare → optimize (loop) → judge → write → translate → post_process → save
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
    
    graph.add_edge("judge", "write")
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
    Run the V2 pipeline asynchronously.
    
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
    Run the V2 pipeline synchronously.
    
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

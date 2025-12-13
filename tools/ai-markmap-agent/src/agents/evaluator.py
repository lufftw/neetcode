# =============================================================================
# Evaluator Agents (V3)
# =============================================================================
# Replaces Judge agents from V2.
# Evaluates Structure Specification quality, not Markdown.
# =============================================================================

from __future__ import annotations

import yaml
from typing import Any
from dataclasses import dataclass, field

from .base_agent import BaseAgent
from ..schema import StructureSpec, dump_structure_spec, extract_yaml_from_response


@dataclass
class EvaluationScore:
    """Evaluation score with breakdown."""
    overall: float = 0.0
    criteria_scores: dict[str, float] = field(default_factory=dict)
    strengths: list[str] = field(default_factory=list)
    improvements: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


@dataclass
class EvaluationResult:
    """Complete evaluation result from an evaluator."""
    evaluator_id: str
    evaluator_name: str
    score: EvaluationScore
    approved: bool = True
    reasoning: str = ""


class EvaluatorAgent(BaseAgent):
    """
    Base class for Evaluator agents.
    
    Evaluators assess the quality of the Structure Specification,
    focusing on structure and organization, not formatting.
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        criteria: list[str],
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
    ):
        super().__init__(agent_id, model_config, config)
        self.name = name
        self.criteria = criteria
    
    def _prepare_input_data(self, state: dict[str, Any]) -> dict[str, Any]:
        """Prepare input data for the evaluator prompt."""
        # Get structure spec
        spec = state.get("current_structure_spec")
        if isinstance(spec, StructureSpec):
            spec_yaml = dump_structure_spec(spec)
        elif isinstance(spec, dict):
            spec_yaml = yaml.dump(spec, default_flow_style=False)
        else:
            spec_yaml = str(spec)
        
        # Get pattern docs summary for validation
        patterns = state.get("patterns", {})
        pattern_summary = self._create_pattern_summary(patterns)
        
        # Get integration history
        integration_result = state.get("integration_result", {})
        
        return {
            "structure_spec": spec_yaml,
            "pattern_docs_summary": pattern_summary,
            "criteria": ", ".join(self.criteria),
            "integration_summary": yaml.dump(integration_result, default_flow_style=False),
        }
    
    def _create_pattern_summary(self, patterns: dict[str, Any]) -> str:
        """Create a summary of pattern docs for validation."""
        if not patterns:
            return "No pattern documentation available."
        
        lines = []
        for pattern_name, pattern_data in patterns.items():
            lines.append(f"{pattern_name}:")
            
            if isinstance(pattern_data, dict):
                sub_patterns = pattern_data.get("sub_patterns", [])
                if sub_patterns:
                    lines.append("  sub_patterns:")
                    for sp in sub_patterns[:5]:
                        if isinstance(sp, dict):
                            lines.append(f"    - {sp.get('name', 'Unknown')}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _parse_response(self, response: str) -> EvaluationResult:
        """Parse evaluator response into EvaluationResult."""
        try:
            yaml_content = extract_yaml_from_response(response)
            data = yaml.safe_load(yaml_content)
            
            if isinstance(data, dict):
                eval_data = data.get("evaluation", data)
                
                score = EvaluationScore(
                    overall=float(eval_data.get("overall_score", eval_data.get("score", 0))),
                    criteria_scores=eval_data.get("criteria_scores", {}),
                    strengths=eval_data.get("strengths", []),
                    improvements=eval_data.get("improvements", []),
                    suggestions=eval_data.get("suggestions", []),
                )
                
                return EvaluationResult(
                    evaluator_id=self.agent_id,
                    evaluator_name=self.name,
                    score=score,
                    approved=eval_data.get("approved", score.overall >= 7.0),
                    reasoning=eval_data.get("reasoning", ""),
                )
        except Exception as e:
            print(f"    ⚠ Failed to parse evaluation: {e}")
        
        # Return minimal result on parse failure
        return EvaluationResult(
            evaluator_id=self.agent_id,
            evaluator_name=self.name,
            score=EvaluationScore(overall=5.0),
            approved=False,
            reasoning="Failed to parse evaluation response",
        )
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Process state and evaluate Structure Specification.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with evaluation result
        """
        # Prepare input
        input_data = self._prepare_input_data(state)
        
        # Invoke LLM
        response = self.invoke(input_data)
        
        # Parse response
        result = self._parse_response(response)
        
        # Store evaluation
        evaluations_key = "evaluator_results"
        if evaluations_key not in state:
            state[evaluations_key] = {}
        
        state[evaluations_key][self.agent_id] = {
            "evaluator_name": result.evaluator_name,
            "overall_score": result.score.overall,
            "criteria_scores": result.score.criteria_scores,
            "strengths": result.score.strengths,
            "improvements": result.score.improvements,
            "suggestions": result.score.suggestions,
            "approved": result.approved,
            "reasoning": result.reasoning,
        }
        
        return state


class StructureEvaluator(EvaluatorAgent):
    """
    Structure Evaluator - focuses on structural quality.
    """
    
    def __init__(
        self,
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
    ):
        super().__init__(
            agent_id="structure_evaluator",
            name="Structure Evaluator",
            criteria=["logical_organization", "appropriate_depth", "balanced_sections"],
            model_config=model_config,
            config=config,
        )


class ContentEvaluator(EvaluatorAgent):
    """
    Content Evaluator - focuses on content quality.
    """
    
    def __init__(
        self,
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
    ):
        super().__init__(
            agent_id="content_evaluator",
            name="Content Evaluator",
            criteria=["coverage", "learning_progression", "practical_value"],
            model_config=model_config,
            config=config,
        )


def create_evaluators(config: dict[str, Any]) -> list[EvaluatorAgent]:
    """
    Create evaluator agents based on configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of evaluator agents
    """
    evaluators = []
    models_config = config.get("models", {})
    
    # Get evaluator configs or use judges as fallback
    evaluator_configs = models_config.get("evaluator", models_config.get("judges", []))
    
    # If still no configs, create defaults
    if not evaluator_configs:
        evaluator_configs = [
            {
                "id": "structure_evaluator",
                "name": "Structure Evaluator",
                "model": "gpt-4",
                "behavior_prompt": "prompts/evaluators/structure_evaluator_behavior.md",
                "criteria": ["logical_organization", "appropriate_depth", "balanced_sections"],
            },
            {
                "id": "content_evaluator",
                "name": "Content Evaluator",
                "model": "gpt-4",
                "behavior_prompt": "prompts/evaluators/content_evaluator_behavior.md",
                "criteria": ["coverage", "learning_progression", "practical_value"],
            },
        ]
    
    for eval_config in evaluator_configs:
        eval_id = eval_config.get("id", "unknown")
        
        if "structure" in eval_id.lower():
            evaluator = StructureEvaluator(
                model_config=eval_config,
                config=config,
            )
        elif "content" in eval_id.lower():
            evaluator = ContentEvaluator(
                model_config=eval_config,
                config=config,
            )
        else:
            evaluator = EvaluatorAgent(
                agent_id=eval_id,
                name=eval_config.get("name", eval_id),
                criteria=eval_config.get("criteria", []),
                model_config=eval_config,
                config=config,
            )
        
        evaluators.append(evaluator)
    
    return evaluators


def aggregate_evaluations(
    evaluations: dict[str, dict[str, Any]],
) -> tuple[float, bool, list[str]]:
    """
    Aggregate evaluations from multiple evaluators.
    
    Args:
        evaluations: Dictionary of evaluator results
        
    Returns:
        Tuple of (average_score, all_approved, combined_suggestions)
    """
    if not evaluations:
        return 0.0, False, []
    
    scores = []
    all_approved = True
    combined_suggestions = []
    
    for eval_id, eval_result in evaluations.items():
        scores.append(eval_result.get("overall_score", 0.0))
        if not eval_result.get("approved", False):
            all_approved = False
        combined_suggestions.extend(eval_result.get("suggestions", []))
    
    average_score = sum(scores) / len(scores) if scores else 0.0
    
    # Remove duplicate suggestions
    unique_suggestions = list(dict.fromkeys(combined_suggestions))
    
    return average_score, all_approved, unique_suggestions


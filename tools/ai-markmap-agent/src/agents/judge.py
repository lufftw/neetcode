# =============================================================================
# Judge Agents
# =============================================================================
# Final evaluation and selection of the best Markmap output.
# Multiple judges with different criteria vote on the final result.
# =============================================================================

from __future__ import annotations

import json
from typing import Any

from .base_agent import BaseAgent


class JudgeAgent(BaseAgent):
    """
    Judge agent for final Markmap evaluation.
    
    Each judge evaluates based on specific criteria:
    - Quality Judge: Structure, naming, technical accuracy
    - Completeness Judge: Coverage, practical value, depth balance
    """
    
    def __init__(
        self,
        judge_config: dict[str, Any],
        config: dict[str, Any] | None = None,
    ):
        """
        Initialize a judge agent.
        
        Args:
            judge_config: Configuration for this specific judge
            config: Full configuration dict
        """
        super().__init__(
            agent_id=judge_config.get("id", "judge"),
            model_config=judge_config,
            config=config,
        )
        
        self.name = judge_config.get("name", "Judge")
        self.criteria = judge_config.get("criteria", [])
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Evaluate all candidate Markmaps and vote.
        
        Args:
            state: Workflow state with candidate markmaps
            
        Returns:
            Updated state with evaluation results
        """
        candidates = state.get("candidates", {})
        
        if not candidates:
            # If no candidates, use the final round result
            total_rounds = state.get("total_rounds", 3)
            for i in range(total_rounds, 0, -1):
                key = f"markmap_round_{i}"
                if key in state:
                    candidates = {"final_optimized": state[key]}
                    break
        
        # Evaluate each candidate
        evaluations = {}
        for candidate_name, markmap in candidates.items():
            score, reasoning = self.evaluate(markmap)
            evaluations[candidate_name] = {
                "score": score,
                "reasoning": reasoning,
                "judge_id": self.agent_id,
                "judge_name": self.name,
                "criteria": self.criteria,
            }
        
        # Store evaluations
        if "judge_evaluations" not in state:
            state["judge_evaluations"] = {}
        state["judge_evaluations"][self.agent_id] = evaluations
        
        return state
    
    def evaluate(self, markmap: str) -> tuple[float, str]:
        """
        Evaluate a single Markmap.
        
        Args:
            markmap: Markmap content to evaluate
            
        Returns:
            Tuple of (score 0-100, reasoning string)
        """
        input_data = {
            "markmap": markmap,
            "criteria": ", ".join(self.criteria),
        }
        
        response = self.invoke(input_data)
        
        # Parse response for score and reasoning
        return self._parse_evaluation(response)
    
    def _parse_evaluation(self, response: str) -> tuple[float, str]:
        """
        Parse evaluation response for score and reasoning.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Tuple of (score, reasoning)
        """
        # Try to extract JSON score
        try:
            # Look for JSON block
            if "```json" in response:
                json_start = response.index("```json") + 7
                json_end = response.index("```", json_start)
                json_str = response[json_start:json_end].strip()
                data = json.loads(json_str)
                return float(data.get("score", 70)), data.get("reasoning", response)
        except (ValueError, json.JSONDecodeError):
            pass
        
        # Try to find score pattern
        import re
        score_match = re.search(r"(?:score|rating)[:\s]*(\d+(?:\.\d+)?)", response.lower())
        if score_match:
            return float(score_match.group(1)), response
        
        # Default score
        return 70.0, response
    
    def debate(
        self,
        markmap: str,
        other_evaluations: dict[str, dict],
    ) -> dict[str, Any]:
        """
        Respond to other judges' evaluations (debate mode).
        
        Args:
            markmap: Markmap being evaluated
            other_evaluations: Evaluations from other judges
            
        Returns:
            Updated evaluation after considering others
        """
        # Format other evaluations
        others = []
        for judge_id, evals in other_evaluations.items():
            if judge_id != self.agent_id:
                for candidate, eval_data in evals.items():
                    others.append(
                        f"{eval_data.get('judge_name', 'Judge')} rated {candidate}: "
                        f"{eval_data.get('score', 0)}/100\n"
                        f"Reasoning: {eval_data.get('reasoning', '')[:300]}"
                    )
        
        input_data = {
            "markmap": markmap,
            "criteria": ", ".join(self.criteria),
            "other_evaluations": "\n\n".join(others),
            "mode": "debate",
        }
        
        response = self.invoke(input_data)
        score, reasoning = self._parse_evaluation(response)
        
        return {
            "score": score,
            "reasoning": reasoning,
            "after_debate": True,
        }


def create_judges(config: dict[str, Any] | None = None) -> list[JudgeAgent]:
    """
    Create all judge agents based on configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of judge agents
    """
    from ..config_loader import ConfigLoader
    
    config = config or ConfigLoader.get_config()
    judge_configs = config.get("models", {}).get("judges", [])
    
    judges = []
    for judge_config in judge_configs:
        judge = JudgeAgent(judge_config=judge_config, config=config)
        judges.append(judge)
    
    return judges


def aggregate_votes(
    evaluations: dict[str, dict[str, dict]],
) -> tuple[str, float, dict]:
    """
    Aggregate votes from all judges to select the best candidate.
    
    Args:
        evaluations: Dictionary of judge_id -> {candidate -> evaluation}
        
    Returns:
        Tuple of (winning_candidate, average_score, detailed_results)
    """
    # Aggregate scores for each candidate
    candidate_scores: dict[str, list[float]] = {}
    
    for judge_id, judge_evals in evaluations.items():
        for candidate, eval_data in judge_evals.items():
            if candidate not in candidate_scores:
                candidate_scores[candidate] = []
            candidate_scores[candidate].append(eval_data.get("score", 0))
    
    # Calculate averages
    results = {}
    for candidate, scores in candidate_scores.items():
        avg = sum(scores) / len(scores) if scores else 0
        results[candidate] = {
            "average_score": avg,
            "individual_scores": scores,
            "vote_count": len(scores),
        }
    
    # Find winner
    if not results:
        return "", 0.0, {}
    
    winner = max(results.keys(), key=lambda k: results[k]["average_score"])
    winning_score = results[winner]["average_score"]
    
    return winner, winning_score, results


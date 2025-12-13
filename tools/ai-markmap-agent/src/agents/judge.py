# =============================================================================
# Judge Agents
# =============================================================================
# Final evaluation and selection of the best Markmap output.
# Multiple judges with different criteria vote on the final result.
# Supports multi-round debate for consensus building.
# =============================================================================

from __future__ import annotations

import json
import re
from typing import Any

from .base_agent import BaseAgent


class JudgeAgent(BaseAgent):
    """
    Judge agent for final Markmap evaluation.
    
    Each judge evaluates based on specific criteria and can participate
    in multi-round debates to reach consensus with other judges.
    
    V2 Features:
    - Structured feedback (strengths, improvements)
    - Multi-round debate support
    - Consensus suggestions generation
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
        self.persona_name = judge_config.get("persona_name", self.name)
        self.criteria = judge_config.get("criteria", [])
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Evaluate all candidate Markmaps and provide structured feedback.
        
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
            eval_result = self.evaluate(markmap)
            evaluations[candidate_name] = {
                **eval_result,
                "judge_id": self.agent_id,
                "judge_name": self.name,
                "persona_name": self.persona_name,
                "criteria": self.criteria,
            }
        
        # Store evaluations
        if "judge_evaluations" not in state:
            state["judge_evaluations"] = {}
        state["judge_evaluations"][self.agent_id] = evaluations
        
        return state
    
    def evaluate(self, markmap: str) -> dict[str, Any]:
        """
        Evaluate a single Markmap with structured feedback.
        
        Args:
            markmap: Markmap content to evaluate
            
        Returns:
            Dict with score, strengths, improvements, reasoning
        """
        criteria_str = ", ".join(self.criteria)
        
        prompt = f"""As {self.persona_name} ({self.name}), evaluate this Markmap based on these criteria: {criteria_str}

## Markmap to Evaluate

{markmap}

## Your Task

Provide a structured evaluation in JSON format:

```json
{{
  "score": 85,
  "strengths": [
    "Clear hierarchy structure",
    "Good pattern organization"
  ],
  "improvements": [
    "Section X should be split into sub-categories",
    "Missing complexity annotations for problems"
  ],
  "reasoning": "Overall assessment..."
}}
```

Be specific in your improvements - they will be applied by the Writer.
Score should be 0-100 based on your criteria."""

        messages = [{"role": "user", "content": prompt}]
        response = self._call_llm(messages)
        
        return self._parse_structured_evaluation(response)
    
    def _parse_structured_evaluation(self, response: str) -> dict[str, Any]:
        """
        Parse structured evaluation response.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Structured evaluation dict
        """
        # Try to extract JSON
        try:
            if "```json" in response:
                json_start = response.index("```json") + 7
                json_end = response.index("```", json_start)
                json_str = response[json_start:json_end].strip()
                data = json.loads(json_str)
                return {
                    "score": float(data.get("score", 70)),
                    "strengths": data.get("strengths", []),
                    "improvements": data.get("improvements", []),
                    "reasoning": data.get("reasoning", ""),
                }
            
            # Try parsing entire response as JSON
            data = json.loads(response)
            return {
                "score": float(data.get("score", 70)),
                "strengths": data.get("strengths", []),
                "improvements": data.get("improvements", []),
                "reasoning": data.get("reasoning", ""),
            }
        except (ValueError, json.JSONDecodeError):
            pass
        
        # Fallback: try to find score pattern
        score_match = re.search(r"(?:score|rating)[:\s]*(\d+(?:\.\d+)?)", response.lower())
        score = float(score_match.group(1)) if score_match else 70.0
        
        return {
            "score": score,
            "strengths": [],
            "improvements": [],
            "reasoning": response,
        }
    
    def debate(
        self,
        markmap: str,
        other_evaluations: dict[str, dict],
        candidate_name: str = "candidate",
    ) -> dict[str, Any]:
        """
        Respond to other judges' evaluations (debate mode).
        
        After seeing other judges' feedback, reconsider your evaluation
        and potentially adjust score or add new suggestions.
        
        Args:
            markmap: Markmap being evaluated
            other_evaluations: Evaluations from other judges
            candidate_name: Name of the candidate being evaluated
            
        Returns:
            Updated evaluation after considering others
        """
        # Format other judges' feedback
        others_summary = []
        for judge_id, evals in other_evaluations.items():
            if judge_id != self.agent_id and candidate_name in evals:
                eval_data = evals[candidate_name]
                judge_name = eval_data.get("persona_name", eval_data.get("judge_name", "Judge"))
                score = eval_data.get("score", 0)
                strengths = eval_data.get("strengths", [])
                improvements = eval_data.get("improvements", [])
                
                summary = f"**{judge_name}** (Score: {score}/100)\n"
                if strengths:
                    summary += "Strengths:\n" + "\n".join(f"  - {s}" for s in strengths) + "\n"
                if improvements:
                    summary += "Improvements:\n" + "\n".join(f"  - {i}" for i in improvements)
                
                others_summary.append(summary)
        
        criteria_str = ", ".join(self.criteria)
        
        prompt = f"""As {self.persona_name} ({self.name}), you are in a debate with other judges about this Markmap.

## Markmap Under Evaluation

{markmap}

## Other Judges' Evaluations

{chr(10).join(others_summary)}

## Your Previous Criteria: {criteria_str}

## Your Task

After considering the other judges' perspectives:
1. Do you agree or disagree with their assessments?
2. Should you adjust your score?
3. Are there any additional improvements you now see?
4. What suggestions should ALL judges agree on (consensus)?

Respond in JSON format:

```json
{{
  "score": 82,
  "score_adjustment_reason": "Adjusted after considering Prof. Torres' point about coverage",
  "agree_with": ["Coverage issue raised by Completeness Judge"],
  "disagree_with": ["I still believe structure is adequate despite Structure Judge's concern"],
  "additional_improvements": ["New suggestion after debate..."],
  "consensus_suggestions": ["Suggestions all judges should agree on..."]
}}
```"""

        messages = [{"role": "user", "content": prompt}]
        response = self._call_llm(messages)
        
        return self._parse_debate_response(response)
    
    def _parse_debate_response(self, response: str) -> dict[str, Any]:
        """Parse debate response."""
        try:
            if "```json" in response:
                json_start = response.index("```json") + 7
                json_end = response.index("```", json_start)
                json_str = response[json_start:json_end].strip()
                data = json.loads(json_str)
                return {
                    "score": float(data.get("score", 70)),
                    "score_adjustment_reason": data.get("score_adjustment_reason", ""),
                    "agree_with": data.get("agree_with", []),
                    "disagree_with": data.get("disagree_with", []),
                    "additional_improvements": data.get("additional_improvements", []),
                    "consensus_suggestions": data.get("consensus_suggestions", []),
                    "after_debate": True,
                }
        except (ValueError, json.JSONDecodeError):
            pass
        
        return {
            "score": 70.0,
            "after_debate": True,
            "raw_response": response,
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


def run_debate(
    judges: list[JudgeAgent],
    candidates: dict[str, str],
    evaluations: dict[str, dict[str, dict]],
    max_rounds: int = 3,
    consensus_threshold: float = 0.8,
) -> dict[str, Any]:
    """
    Run multi-round debate between judges.
    
    Args:
        judges: List of judge agents
        candidates: Dict of candidate_name -> markmap content
        evaluations: Initial evaluations from judges
        max_rounds: Maximum debate rounds
        consensus_threshold: Agreement threshold to end debate early
        
    Returns:
        Dict with final evaluations, consensus suggestions, and selected winner
    """
    current_evaluations = evaluations.copy()
    all_consensus_suggestions = []
    
    for round_num in range(1, max_rounds + 1):
        print(f"    Debate round {round_num}/{max_rounds}...")
        
        # Check if consensus reached
        if _check_consensus(current_evaluations, consensus_threshold):
            print(f"    ✓ Consensus reached at round {round_num}")
            break
        
        # Each judge debates
        for judge in judges:
            for candidate_name, markmap in candidates.items():
                debate_result = judge.debate(
                    markmap,
                    current_evaluations,
                    candidate_name,
                )
                
                # Update evaluation with debate result
                if judge.agent_id in current_evaluations:
                    if candidate_name in current_evaluations[judge.agent_id]:
                        current_evaluations[judge.agent_id][candidate_name].update({
                            "score": debate_result.get("score", 70),
                            "after_debate": True,
                        })
                        
                        # Collect consensus suggestions
                        consensus = debate_result.get("consensus_suggestions", [])
                        all_consensus_suggestions.extend(consensus)
                        
                        # Add additional improvements
                        additional = debate_result.get("additional_improvements", [])
                        existing = current_evaluations[judge.agent_id][candidate_name].get("improvements", [])
                        current_evaluations[judge.agent_id][candidate_name]["improvements"] = existing + additional
    
    # Aggregate final results
    winner, score, details = aggregate_votes(current_evaluations)
    
    # Collect all feedback for the winner
    judge_feedback = []
    for judge_id, judge_evals in current_evaluations.items():
        if winner in judge_evals:
            feedback = {
                "judge_id": judge_id,
                "judge_name": judge_evals[winner].get("judge_name", ""),
                "score": judge_evals[winner].get("score", 0),
                "strengths": judge_evals[winner].get("strengths", []),
                "improvements": judge_evals[winner].get("improvements", []),
            }
            judge_feedback.append(feedback)
    
    # Deduplicate consensus suggestions
    unique_consensus = list(set(all_consensus_suggestions))
    
    return {
        "winner": winner,
        "winning_score": score,
        "judge_feedback": judge_feedback,
        "consensus_suggestions": unique_consensus,
        "final_evaluations": current_evaluations,
        "debate_rounds": round_num,
    }


def _check_consensus(
    evaluations: dict[str, dict[str, dict]],
    threshold: float,
) -> bool:
    """Check if judges have reached consensus on scores."""
    # Get all scores for each candidate
    candidate_scores: dict[str, list[float]] = {}
    
    for judge_id, judge_evals in evaluations.items():
        for candidate, eval_data in judge_evals.items():
            if candidate not in candidate_scores:
                candidate_scores[candidate] = []
            candidate_scores[candidate].append(eval_data.get("score", 0))
    
    # Check score variance for each candidate
    for candidate, scores in candidate_scores.items():
        if len(scores) < 2:
            continue
        
        avg = sum(scores) / len(scores)
        max_diff = max(abs(s - avg) for s in scores)
        
        # If any score differs by more than (1-threshold)*100, no consensus
        allowed_diff = (1 - threshold) * 100
        if max_diff > allowed_diff:
            return False
    
    return True


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
    candidate_feedback: dict[str, list[dict]] = {}
    
    for judge_id, judge_evals in evaluations.items():
        for candidate, eval_data in judge_evals.items():
            if candidate not in candidate_scores:
                candidate_scores[candidate] = []
                candidate_feedback[candidate] = []
            
            candidate_scores[candidate].append(eval_data.get("score", 0))
            candidate_feedback[candidate].append({
                "judge_id": judge_id,
                "judge_name": eval_data.get("judge_name", ""),
                "score": eval_data.get("score", 0),
                "strengths": eval_data.get("strengths", []),
                "improvements": eval_data.get("improvements", []),
            })
    
    # Calculate averages
    results = {}
    for candidate, scores in candidate_scores.items():
        avg = sum(scores) / len(scores) if scores else 0
        results[candidate] = {
            "average_score": avg,
            "individual_scores": scores,
            "vote_count": len(scores),
            "feedback": candidate_feedback.get(candidate, []),
        }
    
    # Find winner
    if not results:
        return "", 0.0, {}
    
    winner = max(results.keys(), key=lambda k: results[k]["average_score"])
    winning_score = results[winner]["average_score"]
    
    return winner, winning_score, results


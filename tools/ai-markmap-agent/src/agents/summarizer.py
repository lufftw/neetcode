# =============================================================================
# Summarizer Agent
# =============================================================================
# Consolidates feedback from all optimizers into an improved Markmap.
# =============================================================================

from __future__ import annotations

from typing import Any

from .base_agent import BaseAgent


class SummarizerAgent(BaseAgent):
    """
    Summarizer agent that consolidates optimization feedback.
    
    Takes suggestions from all optimizers and produces an improved
    version of the Markmap that incorporates the best ideas.
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize the Summarizer agent.
        
        Args:
            config: Full configuration dict
        """
        from ..config_loader import ConfigLoader
        
        config = config or ConfigLoader.get_config()
        model_config = config.get("models", {}).get("summarizer", {})
        
        super().__init__(
            agent_id="summarizer",
            model_config=model_config,
            config=config,
        )
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Consolidate all optimizer suggestions into an improved Markmap.
        
        Args:
            state: Workflow state with current markmap and suggestions
            
        Returns:
            Updated state with improved markmap
        """
        current_markmap = state.get("current_markmap", "")
        round_num = state.get("current_round", 1)
        
        # Get suggestions from this round
        suggestions_key = f"suggestions_round_{round_num}"
        suggestions = state.get(suggestions_key, [])
        
        # Prepare input
        input_data = {
            "current_markmap": current_markmap,
            "round_number": round_num,
            "suggestions": self._format_suggestions(suggestions),
        }
        
        # Generate improved markmap
        improved_markmap = self.invoke(input_data)
        
        # Update state
        state["current_markmap"] = improved_markmap
        state[f"markmap_round_{round_num}"] = improved_markmap
        
        # Increment round counter
        state["current_round"] = round_num + 1
        
        return state
    
    def _format_suggestions(self, suggestions: list[dict]) -> str:
        """
        Format all suggestions for the consolidation prompt.
        
        Args:
            suggestions: List of suggestion dictionaries
            
        Returns:
            Formatted suggestions string
        """
        if not suggestions:
            return "No suggestions received."
        
        formatted = []
        for s in suggestions:
            formatted.append(
                f"## {s.get('persona', 'Expert')} ({s.get('focus', 'general')})\n\n"
                f"{s.get('suggestions', '')}"
            )
        
        return "\n\n---\n\n".join(formatted)
    
    def summarize_round(
        self,
        markmap: str,
        suggestions: list[dict[str, Any]],
        round_num: int,
    ) -> str:
        """
        Summarize a single optimization round.
        
        Args:
            markmap: Current markmap
            suggestions: All suggestions from this round
            round_num: Round number
            
        Returns:
            Improved markmap incorporating suggestions
        """
        input_data = {
            "current_markmap": markmap,
            "round_number": round_num,
            "suggestions": self._format_suggestions(suggestions),
        }
        
        return self.invoke(input_data)


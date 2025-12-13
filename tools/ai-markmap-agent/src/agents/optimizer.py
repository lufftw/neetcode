# =============================================================================
# Optimizer Agents
# =============================================================================
# Multiple optimizer agents that debate and refine the Markmap.
# Each optimizer has a unique perspective and focus area.
# =============================================================================

from __future__ import annotations

from typing import Any

from .base_agent import BaseAgent


class OptimizerAgent(BaseAgent):
    """
    Optimizer agent for refining and improving Markmaps.
    
    Each optimizer has a unique perspective:
    - Architect: System design, modularity, clean architecture
    - Professor: Algorithms, correctness, academic rigor
    - API Designer: Developer experience, usability
    """
    
    def __init__(
        self,
        optimizer_config: dict[str, Any],
        config: dict[str, Any] | None = None,
    ):
        """
        Initialize an optimizer agent.
        
        Args:
            optimizer_config: Configuration for this specific optimizer
            config: Full configuration dict
        """
        super().__init__(
            agent_id=optimizer_config.get("id", "optimizer"),
            model_config=optimizer_config,
            config=config,
        )
        
        self.name = optimizer_config.get("name", "Optimizer")
        self.persona_name = optimizer_config.get("persona_name", "Expert")
        self.focus = optimizer_config.get("focus", "general")
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Review and suggest improvements to the current Markmap.
        
        Args:
            state: Workflow state with current markmap and history
            
        Returns:
            Updated state with optimization suggestions
        """
        # Get current markmap being optimized
        current_markmap = state.get("current_markmap", "")
        round_num = state.get("current_round", 1)
        previous_feedback = state.get("optimization_history", [])
        
        # Prepare input for the optimizer
        input_data = {
            "current_markmap": current_markmap,
            "round_number": round_num,
            "previous_feedback": self._format_feedback(previous_feedback),
            "focus_area": self.focus,
        }
        
        # Get optimization suggestions
        suggestions = self.invoke(input_data)
        
        # Add to optimization history
        feedback_entry = {
            "round": round_num,
            "optimizer_id": self.agent_id,
            "optimizer_name": self.name,
            "persona": self.persona_name,
            "focus": self.focus,
            "suggestions": suggestions,
        }
        
        if "optimization_history" not in state:
            state["optimization_history"] = []
        state["optimization_history"].append(feedback_entry)
        
        # Store individual suggestion for this round
        suggestions_key = f"suggestions_round_{round_num}"
        if suggestions_key not in state:
            state[suggestions_key] = []
        state[suggestions_key].append(feedback_entry)
        
        return state
    
    def _format_feedback(self, feedback_history: list[dict]) -> str:
        """
        Format previous feedback for context.
        
        Args:
            feedback_history: List of previous feedback entries
            
        Returns:
            Formatted feedback string
        """
        if not feedback_history:
            return "No previous feedback."
        
        formatted = []
        for entry in feedback_history[-6:]:  # Keep last 6 entries
            formatted.append(
                f"[Round {entry.get('round', '?')}] "
                f"{entry.get('persona', 'Expert')} ({entry.get('focus', 'general')}):\n"
                f"{entry.get('suggestions', '')[:500]}..."
            )
        
        return "\n\n".join(formatted)
    
    def debate(
        self,
        markmap: str,
        other_suggestions: list[dict[str, Any]],
        round_num: int,
    ) -> str:
        """
        Respond to other optimizers' suggestions (debate mode).
        
        Args:
            markmap: Current markmap
            other_suggestions: Suggestions from other optimizers
            round_num: Current round number
            
        Returns:
            Response/counter-suggestions
        """
        # Format other suggestions
        others = []
        for s in other_suggestions:
            if s.get("optimizer_id") != self.agent_id:
                others.append(
                    f"{s.get('persona', 'Expert')} suggests:\n{s.get('suggestions', '')}"
                )
        
        input_data = {
            "current_markmap": markmap,
            "round_number": round_num,
            "other_suggestions": "\n\n".join(others),
            "focus_area": self.focus,
            "mode": "debate",
        }
        
        return self.invoke(input_data)


def create_optimizers(config: dict[str, Any] | None = None) -> list[OptimizerAgent]:
    """
    Create all optimizer agents based on configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of optimizer agents
    """
    from ..config_loader import ConfigLoader
    
    config = config or ConfigLoader.get_config()
    optimizer_configs = config.get("models", {}).get("optimizer", [])
    
    optimizers = []
    for opt_config in optimizer_configs:
        optimizer = OptimizerAgent(optimizer_config=opt_config, config=config)
        optimizers.append(optimizer)
    
    return optimizers


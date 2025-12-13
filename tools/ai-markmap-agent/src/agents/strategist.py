# =============================================================================
# Content Strategist Agents (V3)
# =============================================================================
# Replaces Optimizer agents from V2.
# Discusses content strategy, not formatting.
# =============================================================================

from __future__ import annotations

import yaml
from typing import Any

from .base_agent import BaseAgent
from ..schema import StructureSpec, dump_structure_spec, extract_yaml_from_response


class ContentStrategistAgent(BaseAgent):
    """
    Base class for Content Strategist agents.
    
    Strategists analyze and suggest improvements to the Structure Specification,
    focusing on content organization, not formatting.
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        focus: str,
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
    ):
        super().__init__(agent_id, model_config, config)
        self.name = name
        self.focus = focus
    
    def _prepare_input_data(
        self,
        state: dict[str, Any],
        round_number: int = 1,
        phase: str = "divergent",
        other_suggestions: str = "",
    ) -> dict[str, Any]:
        """Prepare input data for the strategist prompt."""
        # Get current structure spec
        current_spec = state.get("current_structure_spec")
        if isinstance(current_spec, StructureSpec):
            spec_yaml = dump_structure_spec(current_spec)
        elif isinstance(current_spec, dict):
            spec_yaml = yaml.dump(current_spec, default_flow_style=False)
        else:
            spec_yaml = str(current_spec)
        
        # Get pattern docs summary
        patterns = state.get("patterns", {})
        pattern_summary = self._create_pattern_summary(patterns)
        
        return {
            "structure_spec": spec_yaml,
            "pattern_docs_summary": pattern_summary,
            "round_number": round_number,
            "phase": phase,
            "other_suggestions": other_suggestions or "None (first round)",
        }
    
    def _create_pattern_summary(self, patterns: dict[str, Any]) -> str:
        """Create a summary of pattern docs for strategists."""
        if not patterns:
            return "No pattern documentation available."
        
        lines = []
        for pattern_name, pattern_data in patterns.items():
            lines.append(f"{pattern_name}:")
            
            if isinstance(pattern_data, dict):
                sub_patterns = pattern_data.get("sub_patterns", [])
                if sub_patterns:
                    lines.append("  sub_patterns:")
                    for sp in sub_patterns[:5]:  # Limit for token efficiency
                        if isinstance(sp, dict):
                            lines.append(f"    - name: {sp.get('name', 'Unknown')}")
                            probs = sp.get("problems", [])[:5]
                            lines.append(f"      problems: [{', '.join(probs)}]")
                
                base = pattern_data.get("base_template", "")
                if base:
                    lines.append(f"  base_template: {base}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _parse_response(self, response: str) -> dict[str, Any]:
        """Parse strategist response."""
        try:
            yaml_content = extract_yaml_from_response(response)
            return yaml.safe_load(yaml_content)
        except Exception:
            # Return raw response if parsing fails
            return {"raw_response": response}
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Process state and generate suggestions.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with suggestions added
        """
        round_number = state.get("current_round", 1)
        phase = state.get("current_phase", "divergent")
        other_suggestions = state.get("other_suggestions", "")
        
        # Prepare input
        input_data = self._prepare_input_data(
            state,
            round_number=round_number,
            phase=phase,
            other_suggestions=other_suggestions,
        )
        
        # Invoke LLM
        response = self.invoke(input_data)
        
        # Parse response
        parsed = self._parse_response(response)
        
        # Store suggestion
        suggestions_key = f"suggestions_round_{round_number}"
        if suggestions_key not in state:
            state[suggestions_key] = []
        
        state[suggestions_key].append({
            "strategist_id": self.agent_id,
            "strategist_name": self.name,
            "focus": self.focus,
            "response": parsed,
            "raw_response": response,
        })
        
        return state


class ArchitectStrategist(ContentStrategistAgent):
    """
    Architecture Strategist - focuses on structure and modularity.
    """
    
    def __init__(
        self,
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
    ):
        super().__init__(
            agent_id="architect_strategist",
            name="Architecture Strategist",
            focus="structure_modularity",
            model_config=model_config,
            config=config,
        )


class ProfessorStrategist(ContentStrategistAgent):
    """
    Professor Strategist - focuses on correctness and completeness.
    """
    
    def __init__(
        self,
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
    ):
        super().__init__(
            agent_id="professor_strategist",
            name="Academic Strategist",
            focus="correctness_completeness",
            model_config=model_config,
            config=config,
        )


class UXStrategist(ContentStrategistAgent):
    """
    UX Strategist - focuses on user experience.
    """
    
    def __init__(
        self,
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
    ):
        super().__init__(
            agent_id="ux_strategist",
            name="UX Strategist",
            focus="user_experience",
            model_config=model_config,
            config=config,
        )


def create_strategists(config: dict[str, Any]) -> list[ContentStrategistAgent]:
    """
    Create strategist agents based on configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of strategist agents
    """
    strategists = []
    models_config = config.get("models", {})
    
    # Get strategist configs
    strategist_configs = models_config.get("content_strategist", [])
    
    # If using old config format, try optimizer config
    if not strategist_configs:
        strategist_configs = models_config.get("optimizer", [])
    
    # If still no configs, create defaults
    if not strategist_configs:
        strategist_configs = [
            {
                "id": "architect_strategist",
                "name": "Architecture Strategist",
                "model": "gpt-4",
                "focus": "structure_modularity",
                "persona_prompt": "prompts/strategists/architect_strategist_persona.md",
                "behavior_prompt": "prompts/strategists/architect_strategist_behavior.md",
            },
            {
                "id": "professor_strategist",
                "name": "Academic Strategist",
                "model": "gpt-4",
                "focus": "correctness_completeness",
                "persona_prompt": "prompts/strategists/professor_strategist_persona.md",
                "behavior_prompt": "prompts/strategists/professor_strategist_behavior.md",
            },
            {
                "id": "ux_strategist",
                "name": "UX Strategist",
                "model": "gpt-4",
                "focus": "user_experience",
                "persona_prompt": "prompts/strategists/ux_strategist_persona.md",
                "behavior_prompt": "prompts/strategists/ux_strategist_behavior.md",
            },
        ]
    
    for strategist_config in strategist_configs:
        strategist_id = strategist_config.get("id", "unknown")
        focus = strategist_config.get("focus", "general")
        
        # Create appropriate strategist based on ID/focus
        if "architect" in strategist_id.lower() or focus == "structure_modularity":
            strategist = ArchitectStrategist(
                model_config=strategist_config,
                config=config,
            )
        elif "professor" in strategist_id.lower() or focus == "correctness_completeness":
            strategist = ProfessorStrategist(
                model_config=strategist_config,
                config=config,
            )
        elif "ux" in strategist_id.lower() or focus == "user_experience":
            strategist = UXStrategist(
                model_config=strategist_config,
                config=config,
            )
        else:
            # Generic strategist
            strategist = ContentStrategistAgent(
                agent_id=strategist_id,
                name=strategist_config.get("name", strategist_id),
                focus=focus,
                model_config=strategist_config,
                config=config,
            )
        
        strategists.append(strategist)
    
    return strategists


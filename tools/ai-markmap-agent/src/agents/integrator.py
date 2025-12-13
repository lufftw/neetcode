# =============================================================================
# Integrator Agent (V3)
# =============================================================================
# Replaces Summarizer from V2.
# Integrates strategist suggestions and updates Structure Spec.
# =============================================================================

from __future__ import annotations

import yaml
from math import ceil
from collections import defaultdict
from typing import Any
from dataclasses import dataclass, field

from .base_agent import BaseAgent
from ..schema import (
    StructureSpec,
    parse_structure_spec,
    dump_structure_spec,
    extract_yaml_from_response,
)


@dataclass
class ConflictInfo:
    """Information about a conflict between strategists."""
    id: str
    topic: str
    positions: dict[str, str] = field(default_factory=dict)
    relevant_strategists: list[str] = field(default_factory=list)


@dataclass
class ConsensusInfo:
    """Information about a consensus reached."""
    topic: str
    decision: str
    agreed_by: list[str] = field(default_factory=list)
    agreement_ratio: float = 1.0


@dataclass
class IntegrationResult:
    """Result of integrating strategist suggestions."""
    consensus: list[ConsensusInfo] = field(default_factory=list)
    conflicts: list[ConflictInfo] = field(default_factory=list)
    updated_spec: StructureSpec | None = None
    round_number: int = 1


class IntegratorAgent(BaseAgent):
    """
    Integrator agent that consolidates strategist suggestions.
    
    Responsibilities:
    - Collect suggestions from all strategists
    - Identify consensus (high agreement)
    - Identify conflicts (low agreement)
    - Update Structure Specification with consensus decisions
    - Prepare conflict list for next round
    """
    
    def __init__(
        self,
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
        consensus_threshold: float = 0.8,
    ):
        super().__init__(
            agent_id="integrator",
            model_config=model_config,
            config=config,
        )
        self.consensus_threshold = consensus_threshold
        self.name = "Integrator"
    
    def _prepare_input_data(
        self,
        state: dict[str, Any],
        round_number: int = 1,
    ) -> dict[str, Any]:
        """Prepare input data for the integrator prompt."""
        # Get current structure spec
        current_spec = state.get("current_structure_spec")
        if isinstance(current_spec, StructureSpec):
            spec_yaml = dump_structure_spec(current_spec)
        elif isinstance(current_spec, dict):
            spec_yaml = yaml.dump(current_spec, default_flow_style=False)
        else:
            spec_yaml = str(current_spec)
        
        # Get all strategist suggestions for this round
        suggestions_key = f"suggestions_round_{round_number}"
        suggestions = state.get(suggestions_key, [])
        
        # Format suggestions for prompt
        suggestions_text = self._format_suggestions(suggestions)
        
        # Get previous consensus/conflicts if any
        previous_consensus = state.get("previous_consensus", [])
        previous_conflicts = state.get("previous_conflicts", [])
        
        return {
            "structure_spec": spec_yaml,
            "strategist_suggestions": suggestions_text,
            "round_number": round_number,
            "num_strategists": len(suggestions),
            "consensus_threshold": self.consensus_threshold,
            "previous_consensus": self._format_consensus(previous_consensus),
            "previous_conflicts": self._format_conflicts(previous_conflicts),
        }
    
    def _format_suggestions(self, suggestions: list[dict[str, Any]]) -> str:
        """Format strategist suggestions for the prompt."""
        if not suggestions:
            return "No suggestions received."
        
        lines = []
        for s in suggestions:
            lines.append(f"## {s.get('strategist_name', 'Unknown')}")
            lines.append(f"Focus: {s.get('focus', 'general')}")
            lines.append("")
            
            response = s.get("response", {})
            if isinstance(response, dict):
                lines.append("```yaml")
                lines.append(yaml.dump(response, default_flow_style=False))
                lines.append("```")
            else:
                lines.append(str(response))
            
            lines.append("")
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_consensus(self, consensus: list[ConsensusInfo]) -> str:
        """Format previous consensus for prompt."""
        if not consensus:
            return "None"
        
        lines = []
        for c in consensus:
            lines.append(f"- {c.topic}: {c.decision}")
        return "\n".join(lines)
    
    def _format_conflicts(self, conflicts: list[ConflictInfo]) -> str:
        """Format previous conflicts for prompt."""
        if not conflicts:
            return "None"
        
        lines = []
        for c in conflicts:
            lines.append(f"- {c.topic}:")
            for strategist, position in c.positions.items():
                lines.append(f"    {strategist}: {position}")
        return "\n".join(lines)
    
    def _parse_response(self, response: str) -> dict[str, Any]:
        """Parse integrator response."""
        try:
            yaml_content = extract_yaml_from_response(response)
            return yaml.safe_load(yaml_content)
        except Exception:
            return {"raw_response": response}
    
    def _extract_updated_spec(
        self,
        parsed_response: dict[str, Any],
        current_spec: StructureSpec,
    ) -> StructureSpec:
        """Extract updated spec from integrator response."""
        # Check if response contains updated_structure_spec
        updated_spec_data = parsed_response.get("updated_structure_spec")
        
        if updated_spec_data and isinstance(updated_spec_data, dict):
            try:
                return StructureSpec.from_dict(updated_spec_data)
            except Exception as e:
                print(f"    ⚠ Failed to parse updated spec: {e}")
        
        # Return current spec if no update found
        return current_spec
    
    def _extract_consensus_and_conflicts(
        self,
        parsed_response: dict[str, Any],
    ) -> tuple[list[ConsensusInfo], list[ConflictInfo]]:
        """Extract consensus and conflicts from integrator response."""
        consensus = []
        conflicts = []
        
        # Extract from round_result if present
        round_result = parsed_response.get("round_result", parsed_response)
        
        # Parse consensus
        consensus_data = round_result.get("consensus", [])
        for c in consensus_data:
            if isinstance(c, dict):
                consensus.append(ConsensusInfo(
                    topic=c.get("topic", ""),
                    decision=str(c.get("decision", "")),
                    agreed_by=c.get("agreed_by", []),
                    agreement_ratio=c.get("agreement_ratio", 1.0),
                ))
        
        # Parse conflicts
        conflicts_data = round_result.get("conflicts", [])
        for c in conflicts_data:
            if isinstance(c, dict):
                conflicts.append(ConflictInfo(
                    id=c.get("id", f"conflict_{len(conflicts)}"),
                    topic=c.get("topic", ""),
                    positions=c.get("positions", {}),
                    relevant_strategists=c.get("relevant_strategists", []),
                ))
        
        return consensus, conflicts
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Process state and integrate suggestions.
        
        Args:
            state: Current workflow state with strategist suggestions
            
        Returns:
            Updated state with integrated spec and conflict list
        """
        round_number = state.get("current_round", 1)
        
        # Prepare input
        input_data = self._prepare_input_data(state, round_number)
        
        # Invoke LLM
        response = self.invoke(input_data)
        
        # Parse response
        parsed = self._parse_response(response)
        
        # Get current spec
        current_spec = state.get("current_structure_spec")
        if not isinstance(current_spec, StructureSpec):
            if isinstance(current_spec, dict):
                current_spec = StructureSpec.from_dict(current_spec)
            else:
                # Create empty spec
                current_spec = StructureSpec()
        
        # Extract updated spec
        updated_spec = self._extract_updated_spec(parsed, current_spec)
        
        # Extract consensus and conflicts
        consensus, conflicts = self._extract_consensus_and_conflicts(parsed)
        
        # Update state
        state["current_structure_spec"] = updated_spec
        state["integration_result"] = {
            "round": round_number,
            "consensus": [{"topic": c.topic, "decision": c.decision} for c in consensus],
            "conflicts": [{"id": c.id, "topic": c.topic, "positions": c.positions} for c in conflicts],
        }
        state["previous_consensus"] = consensus
        state["previous_conflicts"] = conflicts
        state["raw_integrator_response"] = response
        
        # Check if we should continue to next round
        if not conflicts:
            state["should_continue_discussion"] = False
            print(f"    ✓ Full consensus reached at round {round_number}")
        else:
            state["should_continue_discussion"] = True
            print(f"    ⚠ {len(conflicts)} conflicts remaining")
        
        return state


def calculate_consensus(
    suggestions: list[dict[str, Any]],
    threshold: float = 0.8,
) -> tuple[list[ConsensusInfo], list[ConflictInfo]]:
    """
    Calculate consensus from strategist suggestions.
    
    This is a helper function for algorithmic consensus detection.
    
    Args:
        suggestions: List of strategist suggestions
        threshold: Consensus threshold (0.0 - 1.0)
        
    Returns:
        Tuple of (consensus list, conflicts list)
    """
    n = len(suggestions)
    if n == 0:
        return [], []
    
    required_agreement = ceil(n * threshold)
    
    # Collect all topics mentioned
    all_topics: set[str] = set()
    topic_positions: dict[str, dict[str, str]] = defaultdict(dict)
    
    for s in suggestions:
        strategist_id = s.get("strategist_id", "unknown")
        response = s.get("response", {})
        
        # Extract suggestions from response
        if isinstance(response, dict):
            sugg_list = response.get("suggestions", [])
            for sugg in sugg_list:
                if isinstance(sugg, dict):
                    topic = sugg.get("target", sugg.get("type", "unknown"))
                    position = sugg.get("proposed", sugg.get("position", "unknown"))
                    all_topics.add(topic)
                    topic_positions[topic][strategist_id] = str(position)
    
    consensus = []
    conflicts = []
    conflict_count = 0
    
    for topic in all_topics:
        positions = topic_positions[topic]
        
        # Group by position
        position_groups: dict[str, list[str]] = defaultdict(list)
        for strategist_id, position in positions.items():
            position_groups[position].append(strategist_id)
        
        # Find max agreement
        max_agreement = max(len(v) for v in position_groups.values()) if position_groups else 0
        
        if max_agreement >= required_agreement:
            # Consensus reached
            winning = max(position_groups.items(), key=lambda x: len(x[1]))
            consensus.append(ConsensusInfo(
                topic=topic,
                decision=winning[0],
                agreed_by=winning[1],
                agreement_ratio=max_agreement / n,
            ))
        else:
            # Conflict
            conflict_count += 1
            conflicts.append(ConflictInfo(
                id=f"conflict_{conflict_count}",
                topic=topic,
                positions=positions,
                relevant_strategists=list(positions.keys()),
            ))
    
    return consensus, conflicts


def create_integrator(config: dict[str, Any]) -> IntegratorAgent:
    """
    Create an integrator agent based on configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Integrator agent
    """
    models_config = config.get("models", {})
    workflow_config = config.get("workflow", {})
    
    # Get integrator config or use summarizer config as fallback
    integrator_config = models_config.get("integrator", models_config.get("summarizer", {}))
    
    # If still no config, create default
    if not integrator_config:
        integrator_config = {
            "model": "gpt-4o",
            "persona_prompt": "prompts/integrator/integrator_persona.md",
            "behavior_prompt": "prompts/integrator/integrator_behavior.md",
            "temperature": 0.5,
            "max_tokens": 4096,
        }
    
    consensus_threshold = workflow_config.get("consensus_threshold", 0.8)
    
    return IntegratorAgent(
        model_config=integrator_config,
        config=config,
        consensus_threshold=consensus_threshold,
    )


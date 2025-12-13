# =============================================================================
# Structure Planner Agents (V3)
# =============================================================================
# Replaces Generator agents from V2.
# Produces Structure Specification (YAML), not Markdown.
# =============================================================================

from __future__ import annotations

from typing import Any

from .base_agent import BaseAgent
from ..schema import StructureSpec, parse_structure_spec, extract_yaml_from_response
from ..compression.compressor import compress_data_for_agent


class StructurePlannerAgent(BaseAgent):
    """
    Base class for Structure Planner agents.
    
    Planners design the organizational structure of the Markmap,
    outputting a Structure Specification in YAML format.
    """
    
    def __init__(
        self,
        agent_id: str,
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
        language: str = "en",
    ):
        super().__init__(agent_id, model_config, config)
        self.language = language
        self.name = model_config.get("name", agent_id)
    
    def _prepare_input_data(self, state: dict[str, Any]) -> dict[str, Any]:
        """Prepare input data for the planner prompt."""
        # Get compressed data for token efficiency
        problems = state.get("problems", {})
        ontology = state.get("ontology", {})
        roadmaps = state.get("roadmaps", {})
        patterns = state.get("patterns", {})
        
        # Compress data for planner (simplified problem list)
        compressed_problems = compress_data_for_agent(
            problems,
            agent_type="planner",
            config=self.config,
        )
        
        # Format pattern docs (full for planner)
        pattern_docs = self._format_pattern_docs(patterns)
        
        return {
            "problems": compressed_problems,
            "ontology": self._format_ontology(ontology),
            "pattern_docs": pattern_docs,
            "roadmaps": self._format_roadmaps(roadmaps),
            "language": self.language,
        }
    
    def _format_ontology(self, ontology: dict[str, Any]) -> str:
        """Format ontology for prompt."""
        if not ontology:
            return "No ontology data available."
        
        lines = []
        for category, data in ontology.items():
            lines.append(f"# {category}")
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        lines.append(f"  {key}: {', '.join(str(v) for v in value[:5])}")
                    else:
                        lines.append(f"  {key}: {value}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_pattern_docs(self, patterns: dict[str, Any]) -> str:
        """Format pattern documentation for prompt."""
        if not patterns:
            return "No pattern documentation available."
        
        lines = []
        for pattern_name, pattern_data in patterns.items():
            lines.append(f"## {pattern_name}")
            
            if isinstance(pattern_data, dict):
                # Extract sub-patterns
                sub_patterns = pattern_data.get("sub_patterns", [])
                if sub_patterns:
                    lines.append("Sub-patterns:")
                    for sp in sub_patterns:
                        if isinstance(sp, dict):
                            sp_name = sp.get("name", "Unknown")
                            sp_problems = sp.get("problems", [])
                            lines.append(f"  - {sp_name}: {', '.join(sp_problems)}")
                        else:
                            lines.append(f"  - {sp}")
                
                # Extract base template
                base = pattern_data.get("base_template", "")
                if base:
                    lines.append(f"Base template: {base}")
                
                # Extract description
                desc = pattern_data.get("description", "")
                if desc:
                    lines.append(f"Description: {desc}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_roadmaps(self, roadmaps: dict[str, Any]) -> str:
        """Format roadmaps for prompt."""
        if not roadmaps:
            return "No roadmaps available."
        
        lines = []
        for name, data in roadmaps.items():
            lines.append(f"# {name}")
            if isinstance(data, dict):
                desc = data.get("description", "")
                if desc:
                    lines.append(f"  Description: {desc}")
                problems = data.get("problems", [])
                if problems:
                    lines.append(f"  Problems: {len(problems)} total")
            lines.append("")
        
        return "\n".join(lines)
    
    def _parse_response(self, response: str) -> StructureSpec:
        """Parse LLM response into StructureSpec."""
        yaml_content = extract_yaml_from_response(response)
        return parse_structure_spec(yaml_content)
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Process state and generate Structure Specification.
        
        Args:
            state: Current workflow state with problems, ontology, etc.
            
        Returns:
            Updated state with structure_spec added
        """
        # Prepare input
        input_data = self._prepare_input_data(state)
        
        # Invoke LLM
        response = self.invoke(input_data)
        
        # Parse response into StructureSpec
        try:
            spec = self._parse_response(response)
            state[f"structure_spec_{self.agent_id}"] = spec
            state["current_structure_spec"] = spec
            state["raw_planner_response"] = response
        except Exception as e:
            print(f"    ⚠ Failed to parse StructureSpec: {e}")
            state["errors"] = state.get("errors", [])
            state["errors"].append(f"Planner {self.agent_id} parse error: {e}")
            # Store raw response for debugging
            state["raw_planner_response"] = response
        
        return state


class GeneralistPlannerAgent(StructurePlannerAgent):
    """
    Generalist planner - broad understanding, holistic organization.
    
    Good at:
    - Seeing the big picture
    - Cross-pattern relationships
    - Balanced organization
    """
    
    def __init__(
        self,
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
        language: str = "en",
    ):
        super().__init__(
            agent_id=f"generalist_planner_{language}",
            model_config=model_config,
            config=config,
            language=language,
        )


class SpecialistPlannerAgent(StructurePlannerAgent):
    """
    Specialist planner - deep technical understanding.
    
    Good at:
    - Technical accuracy
    - Pattern-specific organization
    - Algorithm relationships
    """
    
    def __init__(
        self,
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
        language: str = "en",
    ):
        super().__init__(
            agent_id=f"specialist_planner_{language}",
            model_config=model_config,
            config=config,
            language=language,
        )


def create_planners(config: dict[str, Any]) -> dict[str, StructurePlannerAgent]:
    """
    Create planner agents based on configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary of planner agents keyed by agent_id
    """
    planners = {}
    models_config = config.get("models", {})
    naming_config = config.get("output", {}).get("naming", {})
    
    # Get languages config
    languages_config = naming_config.get("languages", {})
    if isinstance(languages_config, list):
        languages_config = {lang: {"mode": "generate"} for lang in languages_config}
    
    # Get types config
    types_config = naming_config.get("types", {
        "general": {"generator": "generalist"},
        "specialist": {"generator": "specialist"},
    })
    
    for output_type, type_config in types_config.items():
        generator_type = type_config.get("generator", "generalist")
        
        # Get model config for this planner type (use planner-specific config)
        planner_config_key = f"{generator_type}_planner"
        generator_config = models_config.get(planner_config_key, models_config.get(generator_type, {}))
        
        for lang, lang_config in languages_config.items():
            # Only create planners for "generate" mode languages
            if lang_config.get("mode", "generate") != "generate":
                continue
            if not lang_config.get("enabled", True):
                continue
            
            # Get language-specific config or default
            lang_key = lang.replace("-", "_")
            model_config = generator_config.get(lang, generator_config.get("en", {}))
            
            # Create the appropriate planner
            if generator_type == "generalist":
                planner = GeneralistPlannerAgent(
                    model_config=model_config,
                    config=config,
                    language=lang,
                )
            else:
                planner = SpecialistPlannerAgent(
                    model_config=model_config,
                    config=config,
                    language=lang,
                )
            
            agent_id = f"{generator_type}_{lang}"
            planners[agent_id] = planner
    
    return planners


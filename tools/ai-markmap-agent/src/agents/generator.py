# =============================================================================
# Generator Agents
# =============================================================================
# Generalist and Specialist agents for baseline Markmap generation.
# =============================================================================

from __future__ import annotations

import json
from typing import Any

from .base_agent import BaseAgent
from ..data_compressor import DataCompressor


class GeneralistAgent(BaseAgent):
    """
    Generalist agent for broad, comprehensive Markmap generation.
    
    Focus: Knowledge organization, accessibility, intuitive structure.
    """
    
    def __init__(
        self,
        language: str,
        config: dict[str, Any] | None = None,
    ):
        """
        Initialize the Generalist agent.
        
        Args:
            language: Target language ("en" or "zh-TW")
            config: Full configuration dict
        """
        from ..config_loader import ConfigLoader
        
        config = config or ConfigLoader.get_config()
        model_config = config["models"]["generalist"].get(
            "zh" if language == "zh-TW" else "en",
            config["models"]["generalist"]["en"]
        )
        
        super().__init__(
            agent_id=f"generalist_{language}",
            model_config=model_config,
            config=config,
        )
        
        self.language = language
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Generate a baseline Markmap from the input data.
        
        Args:
            state: Workflow state with metadata, ontology, etc.
            
        Returns:
            Updated state with generated markmap
        """
        # Use data compressor for token-efficient transmission
        compressor = DataCompressor(self.config)
        
        # Compress all data sources
        compressed = compressor.compress_all(
            problems=state.get("problems", {}),
            ontology=state.get("ontology", {}),
            roadmaps=state.get("roadmaps", {}),
        )
        
        # Prepare input data for the prompt (compressed format)
        input_data = {
            "metadata": compressed["problems"],
            "ontology": compressed["ontology"],
            "roadmaps": compressed.get("roadmaps", ""),
            "language": self.language,
        }
        
        # Generate markmap
        markmap_content = self.invoke(input_data)
        
        # Update state
        lang_key = self.language.replace("-", "_")
        key = f"baseline_general_{lang_key}"
        state[key] = markmap_content
        
        return state


class SpecialistAgent(BaseAgent):
    """
    Specialist agent for technically precise Markmap generation.
    
    Focus: Engineering details, technical accuracy, structural rigor.
    """
    
    def __init__(
        self,
        language: str,
        config: dict[str, Any] | None = None,
    ):
        """
        Initialize the Specialist agent.
        
        Args:
            language: Target language ("en" or "zh-TW")
            config: Full configuration dict
        """
        from ..config_loader import ConfigLoader
        
        config = config or ConfigLoader.get_config()
        model_config = config["models"]["specialist"].get(
            "zh" if language == "zh-TW" else "en",
            config["models"]["specialist"]["en"]
        )
        
        super().__init__(
            agent_id=f"specialist_{language}",
            model_config=model_config,
            config=config,
        )
        
        self.language = language
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Generate a baseline Markmap from the input data.
        
        Args:
            state: Workflow state with metadata, ontology, etc.
            
        Returns:
            Updated state with generated markmap
        """
        # Use data compressor for token-efficient transmission
        compressor = DataCompressor(self.config)
        
        # Compress all data sources
        compressed = compressor.compress_all(
            problems=state.get("problems", {}),
            ontology=state.get("ontology", {}),
            roadmaps=state.get("roadmaps", {}),
        )
        
        # Prepare input data for the prompt (compressed format)
        input_data = {
            "metadata": compressed["problems"],
            "ontology": compressed["ontology"],
            "roadmaps": compressed.get("roadmaps", ""),
            "language": self.language,
        }
        
        # Generate markmap
        markmap_content = self.invoke(input_data)
        
        # Update state
        lang_key = self.language.replace("-", "_")
        key = f"baseline_specialist_{lang_key}"
        state[key] = markmap_content
        
        return state


def create_generators(config: dict[str, Any] | None = None) -> dict[str, BaseAgent]:
    """
    Create all generator agents based on config.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary of generator agents keyed by their ID
    """
    from ..config_loader import ConfigLoader
    
    config = config or ConfigLoader.get_config()
    naming = config.get("output", {}).get("naming", {})
    languages = naming.get("languages", ["en", "zh-TW"])
    
    generators = {}
    
    for lang in languages:
        # Create generalist
        gen_agent = GeneralistAgent(language=lang, config=config)
        generators[gen_agent.agent_id] = gen_agent
        
        # Create specialist
        spec_agent = SpecialistAgent(language=lang, config=config)
        generators[spec_agent.agent_id] = spec_agent
    
    return generators


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


class TranslatorAgent(BaseAgent):
    """
    Translator agent for converting Markmaps between languages.
    
    Translates the content while preserving structure, links, and formatting.
    """
    
    def __init__(
        self,
        source_language: str,
        target_language: str,
        model: str = "gpt-4o",
        config: dict[str, Any] | None = None,
    ):
        """
        Initialize the Translator agent.
        
        Args:
            source_language: Source language (e.g., "en")
            target_language: Target language (e.g., "zh-TW")
            model: Model to use for translation
            config: Full configuration dict
        """
        from ..config_loader import ConfigLoader
        
        config = config or ConfigLoader.get_config()
        
        # Create model config for translator
        model_config = {
            "model": model,
            "temperature": 0.3,  # Lower temperature for translation accuracy
            "max_tokens": 8192,
        }
        
        super().__init__(
            agent_id=f"translator_{source_language}_to_{target_language}",
            model_config=model_config,
            config=config,
        )
        
        self.source_language = source_language
        self.target_language = target_language
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Process state for translation (required by BaseAgent).
        
        Note: Translation is typically called directly via translate() method,
        not through the process() workflow interface.
        """
        # This method exists to satisfy the abstract base class requirement
        # Actual translation is done via the translate() method
        return state
    
    def translate(self, content: str, output_type: str) -> str:
        """
        Translate Markmap content from source to target language.
        
        Args:
            content: Markdown content to translate
            output_type: Type of output ("general" or "specialist")
            
        Returns:
            Translated markdown content
        """
        target_name = "繁體中文" if self.target_language == "zh-TW" else self.target_language
        
        prompt = f"""Translate the following Markmap markdown content from English to {target_name}.

CRITICAL RULES:
1. Preserve ALL markdown formatting exactly (headers, lists, links, checkboxes, code blocks)
2. DO NOT translate:
   - URLs (keep all links exactly as-is)
   - Code/variable names inside backticks
   - Problem IDs (e.g., "LC 125", "0003")
   - Technical terms that are commonly kept in English (e.g., "Two Pointers", "Sliding Window" - but add Chinese translation in parentheses)
3. Translate:
   - Section headings
   - Descriptions and explanations
   - Comments
4. Keep the same tree structure and indentation
5. Output ONLY the translated markdown, no explanations

Content to translate:

{content}"""
        
        messages = self._build_messages(prompt)
        
        # Save LLM input
        self._save_llm_call_input(messages, "translate")
        
        response = self.llm.invoke(messages)
        
        # Save LLM output
        self._save_llm_call_output(response.content, "translate")
        
        return response.content


def create_generators(config: dict[str, Any] | None = None) -> dict[str, BaseAgent]:
    """
    Create generator agents based on config.
    
    Only creates generators for languages with mode="generate".
    Languages with mode="translate" will be handled separately.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary of generator agents keyed by their ID
    """
    from ..config_loader import ConfigLoader
    
    config = config or ConfigLoader.get_config()
    naming = config.get("output", {}).get("naming", {})
    languages_config = naming.get("languages", {})
    
    # Handle both old format (list) and new format (dict with mode)
    if isinstance(languages_config, list):
        # Old format: ["en", "zh-TW"] - treat all as generate mode
        languages = {lang: {"mode": "generate"} for lang in languages_config}
    else:
        languages = languages_config
    
    generators = {}
    
    for lang, lang_settings in languages.items():
        # Skip if disabled
        if not lang_settings.get("enabled", True):
            continue
        
        # Only create generators for "generate" mode languages
        mode = lang_settings.get("mode", "generate")
        if mode != "generate":
            continue
        
        # Create generalist
        gen_agent = GeneralistAgent(language=lang, config=config)
        generators[gen_agent.agent_id] = gen_agent
        
        # Create specialist
        spec_agent = SpecialistAgent(language=lang, config=config)
        generators[spec_agent.agent_id] = spec_agent
    
    return generators


def create_translators(config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """
    Create translator configurations based on config.
    
    Returns info about which languages need translation.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of translator configs with source_lang, target_lang, model
    """
    from ..config_loader import ConfigLoader
    
    config = config or ConfigLoader.get_config()
    naming = config.get("output", {}).get("naming", {})
    languages_config = naming.get("languages", {})
    
    # Handle old format
    if isinstance(languages_config, list):
        return []  # Old format doesn't support translate mode
    
    translators = []
    
    for lang, lang_settings in languages_config.items():
        # Skip if disabled
        if not lang_settings.get("enabled", True):
            continue
        
        mode = lang_settings.get("mode", "generate")
        if mode == "translate":
            translators.append({
                "target_lang": lang,
                "source_lang": lang_settings.get("source_lang", "en"),
                "model": lang_settings.get("translator_model", "gpt-4o"),
            })
    
    return translators


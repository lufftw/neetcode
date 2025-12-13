# =============================================================================
# Translator Agent
# =============================================================================
# Translates Markmap content between languages.
# =============================================================================

from __future__ import annotations

from typing import Any

from .base_agent import BaseAgent


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


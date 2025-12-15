# =============================================================================
# Translator Agent
# =============================================================================
# Translates Markmap content between languages.
# Prompts are loaded from prompts/translator/*.md files.
# =============================================================================

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base_agent import BaseAgent

# Prompt file paths (relative to project root)
PROMPT_DIR = Path(__file__).parent.parent.parent / "prompts" / "translator"
ZH_TW_PROMPT_FILE = PROMPT_DIR / "zh_tw_translator_behavior.md"
GENERIC_PROMPT_FILE = PROMPT_DIR / "generic_translator_behavior.md"


class TranslatorAgent(BaseAgent):
    """
    Translator agent for converting Markmaps between languages.
    
    Translates the content while preserving structure, links, and formatting.
    Prompts are loaded from external .md files for easy customization.
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
        
        # Initialize prompt cache BEFORE super().__init__() 
        # because parent class may call _load_prompt
        self._prompt_cache: dict[str, str] = {}
        
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
    
    def _load_translation_prompt(self, prompt_file: Path) -> str:
        """Load translation prompt from file with caching."""
        key = str(prompt_file)
        if key not in self._prompt_cache:
            if not prompt_file.exists():
                raise FileNotFoundError(f"Translation prompt file not found: {prompt_file}")
            self._prompt_cache[key] = prompt_file.read_text(encoding="utf-8")
        return self._prompt_cache[key]
    
    def translate(self, content: str, output_type: str) -> str:
        """
        Translate Markmap content from source to target language.
        
        Args:
            content: Markdown content to translate
            output_type: Type of output ("general" or "specialist")
            
        Returns:
            Translated markdown content
        """
        # Load appropriate prompt based on target language
        if self.target_language == "zh-TW":
            prompt_template = self._load_translation_prompt(ZH_TW_PROMPT_FILE)
        else:
            prompt_template = self._load_translation_prompt(GENERIC_PROMPT_FILE)
            prompt_template = prompt_template.replace(
                "the target language",
                self.target_language
            )
        
        # Validate prompt template
        if not prompt_template or len(prompt_template.strip()) == 0:
            raise ValueError(
                f"Translation prompt template is empty. "
                f"Target language: {self.target_language}, "
                f"Prompt file: {ZH_TW_PROMPT_FILE if self.target_language == 'zh-TW' else GENERIC_PROMPT_FILE}"
            )
        
        # Build full prompt with content
        prompt = f"""{prompt_template}

---

## Content to Translate

{content}"""
        
        # Validate full prompt
        if not prompt or len(prompt.strip()) == 0:
            raise ValueError(
                f"Built prompt is empty. "
                f"Template length: {len(prompt_template)}, "
                f"Content length: {len(content)}"
            )
        
        messages = self._build_messages(prompt)
        
        # Save LLM input
        self._save_llm_call_input(messages, "translate")
        
        # Call LLM
        response = self.llm.invoke(messages)
        
        # Validate response
        if response is None:
            raise ValueError(
                f"LLM returned None response. "
                f"Model: {self.model_config.get('model')}, "
                f"Source: {self.source_language} → Target: {self.target_language}"
            )
        
        # Extract content from response
        # Handle different response types (AIMessage, str, etc.)
        if hasattr(response, 'content'):
            content = response.content
        elif isinstance(response, str):
            content = response
        else:
            # Try to get content via dict access or other methods
            try:
                content = str(response)
            except Exception as e:
                raise ValueError(
                    f"Unable to extract content from response. "
                    f"Response type: {type(response)}, "
                    f"Error: {e}"
                )
        
        # Validate content
        if content is None:
            raise ValueError(
                f"LLM response content is None. "
                f"Model: {self.model_config.get('model')}, "
                f"Source: {self.source_language} → Target: {self.target_language}. "
                f"Check API response in debug output files."
            )
        
        # Convert to string if needed
        content_str = str(content) if not isinstance(content, str) else content
        
        # Save LLM output
        self._save_llm_call_output(content_str, "translate")
        
        return content_str


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


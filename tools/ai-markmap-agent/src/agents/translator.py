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
    
    NOTE: This is a PROMPT-DRIVEN translator, not a true agent architecture.
    It loads prompt templates from external .md files, combines them with content,
    and makes a single LLM API call. No multi-turn conversation, tool usage, or
    state management is involved.
    
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
        # Validate input content
        if content is None:
            raise ValueError(
                f"Input content is None. "
                f"Cannot translate empty content."
            )
        
        if not isinstance(content, str):
            raise TypeError(
                f"Input content must be a string, got {type(content).__name__}."
            )
        
        content_str = content.strip()
        if not content_str or len(content_str) == 0:
            raise ValueError(
                f"Input content is empty or contains only whitespace. "
                f"Content length: {len(content)} chars (after strip: {len(content_str)} chars)."
            )
        
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
        prompt_template_str = prompt_template.strip() if prompt_template else ""
        if not prompt_template or len(prompt_template_str) == 0:
            prompt_file = ZH_TW_PROMPT_FILE if self.target_language == "zh-TW" else GENERIC_PROMPT_FILE
            raise ValueError(
                f"Translation prompt template is empty or contains only whitespace.\n"
                f"  Target language: {self.target_language}\n"
                f"  Prompt file: {prompt_file}\n"
                f"  Template length: {len(prompt_template) if prompt_template else 0} chars "
                f"(after strip: {len(prompt_template_str)} chars)\n"
                f"  Check if prompt file exists and contains valid content."
            )
        
        # Build full prompt with content
        prompt = f"""{prompt_template_str}

---

## Content to Translate

{content_str}"""
        
        # Validate full prompt
        prompt_str = prompt.strip()
        if not prompt or len(prompt_str) == 0:
            raise ValueError(
                f"Built prompt is empty or contains only whitespace.\n"
                f"  Template length: {len(prompt_template_str)} chars\n"
                f"  Content length: {len(content_str)} chars\n"
                f"  Combined prompt length: {len(prompt)} chars (after strip: {len(prompt_str)} chars)"
            )
        
        # Check prompt size (warn if too large)
        prompt_size = len(prompt)
        max_tokens = self.model_config.get("max_tokens", 8192)
        # Rough estimate: 1 token ≈ 4 characters
        estimated_tokens = prompt_size / 4
        
        if estimated_tokens > max_tokens * 0.8:  # Warn if > 80% of max_tokens
            print(f"   ⚠️  Warning: Prompt size ({prompt_size:,} chars, ~{estimated_tokens:.0f} tokens) "
                  f"may exceed model context limit (max_tokens: {max_tokens})")
        
        messages = self._build_messages(prompt)
        
        # Save LLM input
        self._save_llm_call_input(messages, "translate")
        
        # Show progress info
        model_name = self.model_config.get("model", "unknown")
        content_size = len(content_str)
        print(f"   📤 Sending request to {model_name}...")
        print(f"      Prompt: {prompt_size:,} chars, Content: {content_size:,} chars")
        print(f"      This may take 30-120 seconds depending on content size...")
        
        # Call LLM with timeout handling
        import time
        start_time = time.time()
        try:
            response = self.llm.invoke(messages)
            elapsed = time.time() - start_time
            print(f"   ⏱️  API call completed in {elapsed:.1f} seconds")
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"   ❌ API call failed after {elapsed:.1f} seconds")
            raise
        
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
        
        # Save LLM output BEFORE validation
        # This ensures we can debug empty responses by checking the saved file
        self._save_llm_call_output(content_str, "translate")
        
        # Validate content is not empty
        if not content_str or len(content_str.strip()) == 0:
            model_name = self.model_config.get('model', 'unknown')
            prompt_size = len(prompt) if 'prompt' in locals() else 0
            max_tokens = self.model_config.get("max_tokens", 8192)
            estimated_tokens = prompt_size / 4 if prompt_size > 0 else 0
            
            error_msg = (
                f"LLM returned empty response.\n"
                f"  Model: {model_name}\n"
                f"  Source: {self.source_language} → Target: {self.target_language}\n"
                f"  Response length: {len(content_str)} chars\n"
                f"  Prompt size: {prompt_size:,} chars (~{estimated_tokens:.0f} tokens, max_tokens: {max_tokens})\n"
                f"  Debug output has been saved (check debug files for actual API response).\n"
                f"  Possible causes:\n"
                f"    1. Invalid model name '{model_name}' (verify it's a valid model for your API provider)\n"
                f"    2. Prompt too large: {prompt_size:,} chars may exceed model context limit\n"
                f"    3. API quota/rate limit exceeded\n"
                f"    4. API returned empty content due to content filtering or safety checks\n"
                f"    5. Prompt format issue causing model to reject the request\n"
                f"    6. Network/API connection issue"
            )
            raise ValueError(error_msg)
        
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


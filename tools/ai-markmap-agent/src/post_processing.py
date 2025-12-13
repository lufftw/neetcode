# =============================================================================
# Post-Processing Module
# =============================================================================
# Applies text transformations to final output.
# Done by code (not LLM) for 100% consistency.
# =============================================================================

from __future__ import annotations

import re
from typing import Any


class PostProcessor:
    """
    Applies post-processing transformations to Markmap content.
    
    Transformations are defined in config and applied by code,
    ensuring 100% consistency without relying on LLM.
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize the post-processor.
        
        Args:
            config: Configuration dictionary
        """
        from .config_loader import ConfigLoader
        
        config = config or ConfigLoader.get_config()
        workflow_config = config.get("workflow", {})
        post_config = workflow_config.get("post_processing", {})
        
        # Load text replacement rules
        self.text_replacements = post_config.get("text_replacements", [])
        
        # Default rules if none configured
        if not self.text_replacements:
            self.text_replacements = [
                # Replace "LC" abbreviation with full "LeetCode"
                {"pattern": r"\bLC[-\s]?(\d+)", "replacement": r"LeetCode \1"},
                # Ensure consistent spacing after LeetCode
                {"pattern": r"LeetCode(\d+)", "replacement": r"LeetCode \1"},
            ]
    
    def process(self, content: str) -> str:
        """
        Apply all post-processing transformations.
        
        Args:
            content: Markmap markdown content
            
        Returns:
            Processed content with all transformations applied
        """
        result = content
        
        for rule in self.text_replacements:
            pattern = rule.get("pattern", "")
            replacement = rule.get("replacement", "")
            
            if pattern and replacement:
                try:
                    result = re.sub(pattern, replacement, result)
                except re.error as e:
                    print(f"  ⚠ Invalid regex pattern '{pattern}': {e}")
        
        return result
    
    def process_batch(self, contents: dict[str, str]) -> dict[str, str]:
        """
        Apply post-processing to multiple contents.
        
        Args:
            contents: Dict of key -> content
            
        Returns:
            Dict of key -> processed content
        """
        return {key: self.process(content) for key, content in contents.items()}


def apply_post_processing(
    content: str,
    config: dict[str, Any] | None = None,
) -> str:
    """
    Convenience function to apply post-processing.
    
    Args:
        content: Content to process
        config: Optional configuration
        
    Returns:
        Processed content
    """
    processor = PostProcessor(config)
    return processor.process(content)


def apply_lc_to_leetcode(content: str) -> str:
    """
    Replace LC abbreviation with full LeetCode.
    
    This is the most common transformation.
    
    Args:
        content: Content with potential "LC" abbreviations
        
    Returns:
        Content with "LeetCode" instead of "LC"
    
    Examples:
        "LC-125" -> "LeetCode 125"
        "LC 125" -> "LeetCode 125"
        "LC125" -> "LeetCode 125"
    """
    # Pattern matches LC followed by optional dash/space and digits
    result = re.sub(r"\bLC[-\s]?(\d+)", r"LeetCode \1", content)
    # Ensure consistent spacing
    result = re.sub(r"LeetCode(\d+)", r"LeetCode \1", result)
    return result


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


def clean_translated_content(content: str) -> str:
    """
    Clean up translated content by removing LLM artifacts.
    
    Removes:
    - Leading/trailing whitespace
    - Multiple consecutive empty lines
    - Markdown code fence wrappers if present
    
    Preserves:
    - YAML frontmatter (--- at start if followed by title/markmap)
    - Internal --- separators (section dividers)
    
    Args:
        content: Raw translated content from LLM
        
    Returns:
        Cleaned content
    """
    # Remove markdown code fence if LLM wrapped the output
    content = content.strip()
    if content.startswith("```markdown"):
        content = content[len("```markdown"):].strip()
    if content.startswith("```md"):
        content = content[len("```md"):].strip()
    if content.startswith("```"):
        content = content[3:].strip()
    if content.endswith("```"):
        content = content[:-3].strip()
    
    lines = content.split("\n")
    
    # Remove leading empty lines only (not ---)
    while lines and lines[0].strip() == "":
        lines.pop(0)
    
    # Check if content has YAML frontmatter (starts with --- followed by key:)
    has_frontmatter = False
    if lines:
        first_line = lines[0].strip()
        if first_line == "---":
            has_frontmatter = True
        elif ":" in first_line and not first_line.startswith("#"):
            # Content starts with YAML key (e.g., "title:") but missing ---
            # Add the opening --- back
            lines.insert(0, "---")
            has_frontmatter = True
    
    # Remove trailing empty lines and standalone ---
    while lines and lines[-1].strip() == "":
        lines.pop()
    # Only remove trailing --- if it's truly standalone (not closing frontmatter)
    while lines and lines[-1].strip() == "---":
        # Check if this is a section separator or just trailing artifact
        # If the line before is empty or another ---, it's an artifact
        if len(lines) >= 2 and lines[-2].strip() in ("", "---"):
            lines.pop()
        else:
            break
    
    # Collapse multiple empty lines into single empty line
    result = []
    prev_empty = False
    for line in lines:
        is_empty = line.strip() == ""
        if is_empty and prev_empty:
            continue  # Skip consecutive empty lines
        result.append(line)
        prev_empty = is_empty
    
    return "\n".join(result)


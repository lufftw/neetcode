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
    
    def __init__(self, config: dict[str, Any] | None = None, problems: dict[str, Any] | None = None):
        """
        Initialize the post-processor.
        
        Args:
            config: Configuration dictionary
            problems: Problem metadata dictionary (for link generation)
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
        
        # Store problems data for link generation
        self.problems = problems or {}
        self.problems_lookup = self._build_problems_lookup(self.problems)
        
        # Load URL templates
        urls_config = config.get("urls", {})
        self.github_template = urls_config.get("github", {}).get(
            "solution_template",
            "https://github.com/lufftw/neetcode/blob/main/{solution_file}"
        )
    
    def _build_problems_lookup(self, problems: dict[str, Any]) -> dict[str, dict]:
        """Build a lookup dictionary for problems by ID."""
        lookup = {}
        
        for key, value in problems.items():
            if isinstance(value, dict):
                problem_id = value.get("id", key)
                # Normalize ID to 4 digits
                if isinstance(problem_id, str) and problem_id.isdigit():
                    problem_id = problem_id.zfill(4)
                lookup[problem_id] = value
                # Also store without leading zeros for flexibility
                try:
                    lookup[str(int(problem_id))] = value
                except (ValueError, TypeError):
                    pass
        
        return lookup
    
    def process(self, content: str) -> str:
        """
        Apply all post-processing transformations.
        
        Args:
            content: Markmap markdown content
            
        Returns:
            Processed content with all transformations applied
        """
        result = content
        
        # Step 1: Apply text replacement rules (LC -> LeetCode)
        for rule in self.text_replacements:
            pattern = rule.get("pattern", "")
            replacement = rule.get("replacement", "")
            
            if pattern and replacement:
                try:
                    result = re.sub(pattern, replacement, result)
                except re.error as e:
                    print(f"  ⚠ Invalid regex pattern '{pattern}': {e}")
        
        # Step 2: Convert plain text "LeetCode XXX" to links using our metadata
        result = self._convert_plain_leetcode_to_links(result)
        
        # Step 3: Normalize LeetCode links (fix wrong URLs)
        result = self._normalize_leetcode_links(result)
        
        # Step 4: Add GitHub solution links automatically
        result = self._add_github_solution_links(result)
        
        return result
    
    def _normalize_leetcode_links(self, content: str) -> str:
        """
        Normalize LeetCode problem links to correct format.
        
        Fixes:
        - https://leetcode.com/problems/0011_container_with_most_water/
          -> https://leetcode.com/problems/container-with-most-water/description/
        - https://leetcode.com/problems/{slug}/
          -> https://leetcode.com/problems/{normalized-slug}/description/
        """
        # Pattern to match LeetCode URLs in markdown links
        # Matches: [text](https://leetcode.com/problems/...)
        def normalize_url(match: re.Match) -> str:
            link_text = match.group(1)  # Text inside []
            url = match.group(2)  # The URL part
            
            # Skip if already has /description/
            if "/description/" in url:
                return match.group(0)
            
            # Extract slug from URL
            # Pattern: https://leetcode.com/problems/{slug}/
            slug_match = re.search(r'/problems/([^/]+)/?', url)
            if not slug_match:
                return match.group(0)
            
            slug = slug_match.group(1)
            
            # Convert slug format: 0011_container_with_most_water -> container-with-most-water
            # Or if already in correct format, use as-is
            normalized_slug = self._normalize_slug(slug)
            
            # Reconstruct URL with /description/
            new_url = f"https://leetcode.com/problems/{normalized_slug}/description/"
            return f"[{link_text}]({new_url})"
        
        # Match markdown links: [text](https://leetcode.com/problems/...)
        pattern = r'\[([^\]]+)\]\((https://leetcode\.com/problems/[^)]+)\)'
        result = re.sub(pattern, normalize_url, content)
        
        return result
    
    def _normalize_slug(self, slug: str) -> str:
        """
        Normalize problem slug to LeetCode format.
        
        Examples:
        - 0011_container_with_most_water -> container-with-most-water
        - container-with-most-water -> container-with-most-water (already correct)
        """
        # Remove leading digits and underscore if present
        slug = re.sub(r'^\d+_', '', slug)
        
        # Convert underscores to hyphens
        slug = slug.replace('_', '-')
        
        return slug
    
    def _convert_plain_leetcode_to_links(self, content: str) -> str:
        """
        Convert plain text "LeetCode XXX" or "LeetCode XXX - Title" to proper links.
        
        Only converts if we have metadata for the problem.
        AI should provide links for problems we don't have.
        
        Patterns handled:
        - "LeetCode 11" -> "[LeetCode 11 - Container With Most Water](url)"
        - "LeetCode 11 - Container With Most Water" -> "[LeetCode 11 - Container With Most Water](url)"
        - "[LeetCode 11 - Wrong Title](wrong_url)" -> "[LeetCode 11 - Container With Most Water](correct_url)"
        """
        # First, handle existing markdown links with LeetCode - replace with our data
        def replace_existing_link(match: re.Match) -> str:
            link_text = match.group(1)  # Text inside []
            url = match.group(2)  # The URL
            
            # Extract problem ID
            id_match = re.search(r'LeetCode\s+(\d+)', link_text)
            if not id_match:
                return match.group(0)
            
            problem_id = id_match.group(1)
            problem = self.problems_lookup.get(problem_id.zfill(4)) or self.problems_lookup.get(problem_id)
            
            if not problem:
                # We don't have this problem - keep AI's link
                return match.group(0)
            
            # Use our metadata
            title = problem.get("title", "")
            problem_url = problem.get("url", "")
            
            if not problem_url:
                return match.group(0)
            
            # Ensure URL ends with /description/
            if not problem_url.endswith("/description/"):
                problem_url = problem_url.rstrip("/") + "/description/"
            
            return f"[LeetCode {problem_id} - {title}]({problem_url})"
        
        # Pattern: [LeetCode XXX...](url)
        result = re.sub(
            r'\[(LeetCode\s+\d+[^\]]*)\]\(([^)]+)\)',
            replace_existing_link,
            content
        )
        
        # Now handle plain text "LeetCode XXX" that's NOT already a link
        def convert_plain_text(match: re.Match) -> str:
            full_match = match.group(0)
            problem_id = match.group(1)
            title_part = match.group(2) if match.group(2) else ""
            
            # Look up in our metadata
            problem = self.problems_lookup.get(problem_id.zfill(4)) or self.problems_lookup.get(problem_id)
            
            if not problem:
                # We don't have this problem - keep as plain text
                # (AI should have provided a link if it's important)
                return full_match
            
            # Use our metadata
            title = problem.get("title", "")
            url = problem.get("url", "")
            
            if not url:
                return full_match
            
            # Ensure URL ends with /description/
            if not url.endswith("/description/"):
                url = url.rstrip("/") + "/description/"
            
            return f"[LeetCode {problem_id} - {title}]({url})"
        
        # Pattern: Plain text "LeetCode XXX" or "LeetCode XXX - Title" 
        # But NOT inside [] (which would be a link)
        # Negative lookbehind for [ and negative lookahead for ]( 
        result = re.sub(
            r'(?<!\[)LeetCode\s+(\d+)(\s*[-–—:]\s*[^(\[\]\n]+)?(?!\]\()',
            convert_plain_text,
            result
        )
        
        return result
    
    def _add_github_solution_links(self, content: str) -> str:
        """
        Automatically add GitHub solution links when seeing "LeetCode {id}".
        
        Pattern: [LeetCode {id} - {title}](leetcode_url)
        Result: [LeetCode {id} - {title}](leetcode_url) | [Solution](github_url)
        
        Note: Only adds if not already present (avoids duplicates).
        """
        # Pattern to match: [LeetCode {id} - {title}](url)
        def add_solution_link(match: re.Match) -> str:
            full_text = match.group(0)
            link_text = match.group(1)  # The text inside []
            url = match.group(2)  # The URL
            
            # Skip if already has GitHub solution link
            if "| [Solution](" in full_text or "| [solution](" in full_text:
                return full_text
            
            # Extract problem ID from link text
            id_match = re.search(r'LeetCode\s+(\d+)', link_text)
            if not id_match:
                return full_text
            
            problem_id = id_match.group(1)
            
            # Look up problem in our data
            problem = self.problems_lookup.get(problem_id.zfill(4)) or self.problems_lookup.get(problem_id)
            if not problem:
                return full_text
            
            # Check if solution_file exists
            files = problem.get("files", {})
            solution_file = files.get("solution", "")
            if not solution_file:
                return full_text
            
            # Generate GitHub URL
            github_url = self.github_template.format(solution_file=solution_file)
            
            # Add GitHub link after LeetCode link
            # Format: [LeetCode {id} - {title}](leetcode_url) | [Solution](github_url)
            return f"{full_text} | [Solution]({github_url})"
        
        # Match markdown links with "LeetCode" in the text
        # Pattern: [LeetCode {id} - ...](url)
        pattern = r'\[(LeetCode\s+\d+[^\]]*)\]\(([^)]+)\)'
        result = re.sub(pattern, add_solution_link, content)
        
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


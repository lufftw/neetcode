# =============================================================================
# Post-Processing Module
# =============================================================================
# Applies text transformations to final output.
# Done by code (not LLM) for 100% consistency.
#
# Also provides input preprocessing to simplify content before sending to LLM,
# reducing token usage.
# =============================================================================

from __future__ import annotations

import re
from typing import Any


def simplify_leetcode_links(content: str) -> str:
    """
    Simplify LeetCode markdown links to plain text format.
    
    This reduces input tokens by removing URLs and solution links,
    while preserving the problem title for LLM context.
    Post-processing will add the links back automatically.
    
    Transformations:
    - `[LeetCode 79 – Word Search](url) · [Solution](github_url)` → `LeetCode 79 – Word Search`
    - `[LeetCode 79 – Word Search](url)` → `LeetCode 79 – Word Search`
    - `[LeetCode 79](url) · [Solution](github_url)` → `LeetCode 79`
    - `[LeetCode 79](url)` → `LeetCode 79`
    """
    # Pattern: [LeetCode N...](url) with optional Solution link
    # Capture the link text (group 1) and discard the rest
    content = re.sub(
        r'\[(LeetCode\s+\d+[^\]]*)\]\([^)]+\)(\s*(?:·|\xb7|\|)\s*\[Solution\]\([^)]+\))?',
        r'\1',
        content,
        flags=re.IGNORECASE
    )
    return content


def preprocess_for_llm(content: str) -> str:
    """
    Preprocess content before sending to LLM to reduce token usage.
    
    This function:
    1. Simplifies LeetCode links to plain text (LeetCode N – Title)
    2. Removes redundant whitespace
    """
    content = simplify_leetcode_links(content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content


class PostProcessor:
    """
    Applies post-processing transformations to Markmap content.
    
    Transformations are defined in config and applied by code,
    ensuring 100% consistency without relying on LLM.
    
    Processing Steps:
    1. Text replacements (LC → LeetCode)
    2. Remove plain text "· Solution" artifacts
    3. Convert all LeetCode references to complete links with Solution
    """
    
    def __init__(self, config: dict[str, Any] | None = None, problems: dict[str, Any] | None = None):
        """
        Initialize the post-processor.
        
        Args:
            config: Configuration dictionary
            problems: Problem metadata dictionary (for link generation)
        """
        from .config_loader import ConfigLoader
        from .leetcode_api import merge_leetcode_api_data
        
        config = config or ConfigLoader.get_config()
        workflow_config = config.get("workflow", {})
        post_config = workflow_config.get("post_processing", {})
        
        # Load text replacement rules
        self.text_replacements = post_config.get("text_replacements", [])
        if not self.text_replacements:
            self.text_replacements = [
                {"pattern": r"\bLC[-\s]?(\d+)", "replacement": r"LeetCode \1"},
                {"pattern": r"LeetCode(\d+)", "replacement": r"LeetCode \1"},
            ]
        
        # Merge with LeetCode API cache data
        self.problems = merge_leetcode_api_data(problems or {})
        self.problems_lookup = self._build_problems_lookup(self.problems)
        
        # Load URL templates
        urls_config = config.get("urls", {})
        self.github_template = urls_config.get("github", {}).get(
            "solution_template",
            "https://github.com/lufftw/neetcode/blob/main/{solution_file}"
        )
        
        # Stats
        self._stats = {"converted": 0, "with_solution": 0}
    
    def _build_problems_lookup(self, problems: dict[str, Any]) -> dict[str, dict]:
        """Build a lookup dictionary for problems by ID."""
        lookup = {}
        
        for key, value in problems.items():
            if not isinstance(value, dict):
                continue
            
            # Get problem ID
            problem_id = value.get("id") or value.get("leetcode_id")
            if not problem_id:
                match = re.match(r'^(\d+)_', key)
                if match:
                    problem_id = match.group(1)
            if not problem_id:
                problem_id = key
            
            problem_id_str = str(problem_id)
            if not problem_id_str.isdigit():
                continue
            
            # Normalize the problem data structure
            normalized = self._normalize_problem_data(value)
            
            # Store with multiple key formats
            normalized_id = problem_id_str.zfill(4)
            int_id = str(int(problem_id_str))
            
            for key_format in [normalized_id, int_id]:
                if key_format not in lookup:
                    lookup[key_format] = normalized
                elif normalized.get("solution_file") and not lookup[key_format].get("solution_file"):
                    # Prefer entry with solution file
                    lookup[key_format] = normalized
        
        solutions_count = sum(1 for p in lookup.values() if p.get("solution_file"))
        if solutions_count > 0:
            print(f"  ℹ️  PostProcessor: {len(lookup)} problems loaded, {solutions_count} with solutions")
        
        return lookup
    
    def _normalize_problem_data(self, data: dict) -> dict:
        """
        Normalize problem data to a consistent structure.
        
        Handles both formats:
        - {"solution_file": "path"} (direct)
        - {"files": {"solution": "path"}} (nested)
        """
        normalized = {
            "url": data.get("url", ""),
            "title": data.get("title", ""),
            "solution_file": None,
        }
        
        # Get solution file from either format
        if data.get("solution_file"):
            normalized["solution_file"] = data["solution_file"]
        elif data.get("files", {}).get("solution"):
            normalized["solution_file"] = data["files"]["solution"]
        
        return normalized
    
    def process(self, content: str) -> str:
        """
        Apply all post-processing transformations.
        
        Steps:
        1. Text replacements (LC → LeetCode)
        2. Remove plain text "· Solution" artifacts  
        3. Convert all LeetCode references to complete links
        """
        self._stats = {"converted": 0, "with_solution": 0}
        
        # Step 1: Text replacements
        result = self._apply_text_replacements(content)
        
        # Step 2: Remove plain text Solution artifacts
        result = self._remove_solution_artifacts(result)
        
        # Step 3: Convert all LeetCode references to complete links
        result = self._convert_to_complete_links(result)
        
        # Print stats
        if self._stats["converted"] > 0:
            print(f"  ✓ Converted {self._stats['converted']} LeetCode references, {self._stats['with_solution']} with Solution links")
        
        return result
    
    def _apply_text_replacements(self, content: str) -> str:
        """Apply text replacement rules (e.g., LC → LeetCode)."""
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
    
    def _remove_solution_artifacts(self, content: str) -> str:
        """
        Remove plain text "· Solution" that LLM may have added.
        
        When preprocessing simplifies "[LeetCode X](url) · [Solution](url)" to
        "LeetCode X", the LLM may output "· Solution" as plain text.
        """
        return re.sub(r'\s*(?:·|\xb7|\|)\s*Solution(?!\])', '', content, flags=re.IGNORECASE)
    
    def _convert_to_complete_links(self, content: str) -> str:
        """
        Convert all LeetCode references to complete links with Solution.
        
        Handles:
        - Plain text: "LeetCode 11" or "LeetCode 11 - Title"
        - Existing links: "[LeetCode 11](url)" with or without Solution
        
        Output: [LeetCode {id} - {title}](url) · [Solution](github_url)
        """
        # First pass: Handle existing markdown links (with or without Solution)
        result = re.sub(
            r'\[(LeetCode\s+\d+[^\]]*)\]\(([^)]+)\)(\s*(?:·|\xb7|\|)?\s*\[Solution\]\([^)]+\))?',
            self._replace_link,
            content,
            flags=re.IGNORECASE
        )
        
        # Second pass: Handle plain text LeetCode references
        result = re.sub(
            r'(?<!\[)LeetCode\s+(\d+)(\s*[-–—:]\s*[^\[\]\n(]+)?(?!\]\()',
            self._replace_plain_text,
            result
        )
        
        return result
    
    def _replace_link(self, match: re.Match) -> str:
        """Replace existing LeetCode markdown link with complete link."""
        link_text = match.group(1)
        # Group 3 would be existing Solution link - we ignore it and regenerate
        
        id_match = re.search(r'LeetCode\s+(\d+)', link_text)
        if not id_match:
            return match.group(0)
        
        problem_id = id_match.group(1)
        return self._build_complete_link(problem_id)
    
    def _replace_plain_text(self, match: re.Match) -> str:
        """Replace plain text LeetCode reference with complete link."""
        problem_id = match.group(1)
        return self._build_complete_link(problem_id)
    
    def _build_complete_link(self, problem_id: str) -> str:
        """
        Build complete link: [LeetCode {id} - {title}](url) · [Solution](github_url)
        
        Returns plain text if problem not found in lookup.
        """
        problem = self.problems_lookup.get(problem_id.zfill(4)) or self.problems_lookup.get(problem_id)
        
        if not problem:
            return f"LeetCode {problem_id}"
        
        url = problem.get("url", "")
        if not url:
            return f"LeetCode {problem_id}"
        
        # Ensure URL ends with /description/
        if not url.endswith("/description/"):
            url = url.rstrip("/") + "/description/"
        
        # Build link text with title
        title = problem.get("title", "")
        link_text = f"LeetCode {problem_id} - {title}" if title else f"LeetCode {problem_id}"
        leetcode_link = f"[{link_text}]({url})"
        
        self._stats["converted"] += 1
        
        # Add Solution link if available
        solution_file = problem.get("solution_file")
        if solution_file:
            github_url = self.github_template.format(solution_file=solution_file)
            self._stats["with_solution"] += 1
            return f"{leetcode_link} · [Solution]({github_url})"
        
        return leetcode_link
    
    def process_batch(self, contents: dict[str, str]) -> dict[str, str]:
        """Apply post-processing to multiple contents."""
        return {key: self.process(content) for key, content in contents.items()}


def apply_post_processing(content: str, config: dict[str, Any] | None = None) -> str:
    """Convenience function to apply post-processing."""
    processor = PostProcessor(config)
    return processor.process(content)


def apply_lc_to_leetcode(content: str) -> str:
    """Replace LC abbreviation with full LeetCode."""
    result = re.sub(r"\bLC[-\s]?(\d+)", r"LeetCode \1", content)
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
    """
    content = content.strip()
    
    # Remove markdown code fence wrappers
    for prefix in ["```markdown", "```md", "```"]:
        if content.startswith(prefix):
            content = content[len(prefix):].strip()
            break
    if content.endswith("```"):
        content = content[:-3].strip()
    
    lines = content.split("\n")
    
    # Remove leading empty lines
    while lines and lines[0].strip() == "":
        lines.pop(0)
    
    # Check for YAML frontmatter
    if lines:
        first_line = lines[0].strip()
        if first_line != "---" and ":" in first_line and not first_line.startswith("#"):
            lines.insert(0, "---")
    
    # Remove trailing empty lines and standalone ---
    while lines and lines[-1].strip() == "":
        lines.pop()
    while lines and lines[-1].strip() == "---":
        if len(lines) >= 2 and lines[-2].strip() in ("", "---"):
            lines.pop()
        else:
            break
    
    # Collapse multiple empty lines
    result = []
    prev_empty = False
    for line in lines:
        is_empty = line.strip() == ""
        if is_empty and prev_empty:
            continue
        result.append(line)
        prev_empty = is_empty
    
    return "\n".join(result)

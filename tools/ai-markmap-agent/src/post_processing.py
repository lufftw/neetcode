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
    
    Args:
        content: Markdown content with LeetCode links
        
    Returns:
        Simplified content with plain text LeetCode references (with titles preserved)
    """
    # Pattern 1: [LeetCode N – Title](url) · [Solution](url) → LeetCode N – Title
    # Pattern 2: [LeetCode N – Title](url) | [Solution](url) → LeetCode N – Title (backward compat)
    # Capture the entire link text to preserve the title
    # Use \xb7 for middle dot (·) and handle both | and · separators
    content = re.sub(
        r'\[(LeetCode\s+\d+[^\]]*)\]\([^)]+\)\s*(?:·|\xb7|\|)\s*\[Solution\]\([^)]+\)',
        r'\1',
        content,
        flags=re.IGNORECASE
    )
    
    # Pattern 3: [LeetCode N – Title](url) → LeetCode N – Title (without solution link)
    # Capture the entire link text to preserve the title
    content = re.sub(
        r'\[(LeetCode\s+\d+[^\]]*)\]\([^)]+\)',
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
    
    Args:
        content: Raw markdown content
        
    Returns:
        Simplified content ready for LLM input (with titles preserved)
    """
    # Simplify LeetCode links
    content = simplify_leetcode_links(content)
    
    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content


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
        from .leetcode_api import merge_leetcode_api_data
        
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
        
        # Merge with LeetCode API cache data
        # This ensures we have URLs and slugs even if local TOML files don't have them
        self.problems = merge_leetcode_api_data(problems or {})
        self.problems_lookup = self._build_problems_lookup(self.problems)
        
        # Debug: Count problems with solution files
        if self.problems_lookup:
            solutions_count = sum(
                1 for p in self.problems_lookup.values()
                if p.get("files", {}).get("solution")
            )
            if solutions_count > 0:
                print(f"  ℹ️  PostProcessor: {solutions_count} problems have solution files")
        
        # Load URL templates
        urls_config = config.get("urls", {})
        self.github_template = urls_config.get("github", {}).get(
            "solution_template",
            "https://github.com/lufftw/neetcode/blob/main/{solution_file}"
        )
    
    def _build_problems_lookup(self, problems: dict[str, Any]) -> dict[str, dict]:
        """Build a lookup dictionary for problems by ID."""
        lookup = {}
        debug_samples = []  # Store first few for debugging
        
        for key, value in problems.items():
            if isinstance(value, dict):
                # Try to get ID from various sources
                problem_id = value.get("id") or value.get("leetcode_id")
                
                # If no ID found, try to extract from key (slug format: "0079_word_search")
                if not problem_id:
                    # Extract ID from slug if it starts with digits
                    match = re.match(r'^(\d+)_', key)
                    if match:
                        problem_id = match.group(1)
                
                # If still no ID, use key as fallback (but this is less reliable)
                if not problem_id:
                    problem_id = key
                
                # Normalize ID to string
                if isinstance(problem_id, int):
                    problem_id_str = str(problem_id)
                elif not isinstance(problem_id, str):
                    problem_id_str = str(problem_id)
                else:
                    problem_id_str = problem_id
                
                # Store with multiple formats for maximum compatibility
                if problem_id_str.isdigit():
                    # Store as 4-digit format: "0011"
                    normalized_id = problem_id_str.zfill(4)
                    # Only store if not exists, or if current value has files (prefer TOML data over API data)
                    if normalized_id not in lookup:
                        lookup[normalized_id] = value
                    else:
                        # Prefer value with files (TOML data) over value without files (API data)
                        existing = lookup[normalized_id]
                        existing_has_files = bool(existing.get("files", {}).get("solution"))
                        current_has_files = bool(value.get("files", {}).get("solution"))
                        if current_has_files and not existing_has_files:
                            lookup[normalized_id] = value
                    
                    # Store as integer string (no leading zeros): "11"
                    int_id = str(int(problem_id_str))
                    if int_id != normalized_id:
                        if int_id not in lookup:
                            lookup[int_id] = value
                        else:
                            # Prefer value with files
                            existing = lookup[int_id]
                            existing_has_files = bool(existing.get("files", {}).get("solution"))
                            current_has_files = bool(value.get("files", {}).get("solution"))
                            if current_has_files and not existing_has_files:
                                lookup[int_id] = value
                    
                    # Also store original format if different
                    if problem_id_str != normalized_id and problem_id_str != int_id:
                        if problem_id_str not in lookup:
                            lookup[problem_id_str] = value
                        else:
                            # Prefer value with files
                            existing = lookup[problem_id_str]
                            existing_has_files = bool(existing.get("files", {}).get("solution"))
                            current_has_files = bool(value.get("files", {}).get("solution"))
                            if current_has_files and not existing_has_files:
                                lookup[problem_id_str] = value
                    
                    # Debug: Store sample for first few problems
                    if len(debug_samples) < 3:
                        has_solution = bool(value.get("files", {}).get("solution"))
                        debug_samples.append({
                            "key": key,
                            "id": problem_id_str,
                            "normalized": normalized_id,
                            "has_solution": has_solution,
                            "files_keys": list(value.get("files", {}).keys()) if value.get("files") else []
                        })
        
        # Debug output
        if debug_samples:
            print(f"  ℹ️  Problems lookup: {len(lookup)} entries built from {len(problems)} problems")
            for sample in debug_samples:
                sol_status = "✓" if sample["has_solution"] else "✗"
                print(f"    {sol_status} {sample['key']} -> ID:{sample['id']} (lookup keys: {sample['normalized']}, {str(int(sample['id']))})")
                if sample["files_keys"]:
                    print(f"      files keys: {sample['files_keys']}")
        
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
        
        # Step 2: Remove plain text "· Solution" (LLM artifacts from preprocessing)
        # This handles cases where LLM outputs "· Solution" as plain text
        result = self._remove_plain_solution_text(result)
        
        # Step 3: Convert LeetCode references to complete links (with Solution)
        # One-step: LeetCode 11 → [LeetCode 11 - Title](url) · [Solution](github_url)
        result = self._convert_plain_leetcode_to_links(result)
        
        # Step 4: Normalize LeetCode links (fix wrong URLs)
        result = self._normalize_leetcode_links(result)
        
        # Step 5: Add GitHub solution links for any remaining links without Solution
        # (handles edge cases not covered by Step 3)
        result = self._add_github_solution_links(result)
        
        return result
    
    def _remove_plain_solution_text(self, content: str) -> str:
        """
        Remove plain text "· Solution" that LLM may have added.
        
        When preprocessing simplifies "[LeetCode X](url) · [Solution](url)" to
        "LeetCode X", the LLM may learn to output "· Solution" as plain text.
        This method removes such artifacts before we add proper Solution links.
        
        Patterns removed:
        - "· Solution" (plain text, not a link)
        - "| Solution" (old separator, plain text)
        """
        # Remove "· Solution" or "| Solution" that is NOT part of a markdown link
        # Negative lookahead ensures we don't match "[Solution]"
        # Use (?:·|\xb7|\|) to match middle dot (both forms) and pipe
        result = re.sub(r'\s*(?:·|\xb7|\|)\s*Solution(?!\])', '', content, flags=re.IGNORECASE)
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
        Convert plain text "LeetCode XXX" to complete links with Solution.
        
        One-step conversion: LeetCode 11 → [LeetCode 11 - Title](url) · [Solution](github_url)
        
        Patterns handled:
        - "LeetCode 11" → complete link with Solution
        - "LeetCode 11 - Title" → complete link with Solution
        - "[LeetCode 11](url)" → corrected link with Solution
        """
        # First, handle existing markdown links with LeetCode - replace with our data
        def replace_existing_link(match: re.Match) -> str:
            link_text = match.group(1)  # Text inside []
            url = match.group(2)  # The URL
            
            # Extract problem ID (ignore title part)
            id_match = re.search(r'LeetCode\s+(\d+)', link_text)
            if not id_match:
                return match.group(0)
            
            problem_id = id_match.group(1)
            problem = self.problems_lookup.get(problem_id.zfill(4)) or self.problems_lookup.get(problem_id)
            
            if not problem:
                # We don't have this problem - keep AI's link
                return match.group(0)
            
            # Build complete link with Solution
            return self._build_complete_link(problem_id, problem)
        
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
            
            # Look up in our metadata
            problem = self.problems_lookup.get(problem_id.zfill(4)) or self.problems_lookup.get(problem_id)
            
            if not problem:
                # We don't have this problem - keep as plain text
                return full_match
            
            # Build complete link with Solution
            return self._build_complete_link(problem_id, problem)
        
        # Pattern: Plain text "LeetCode XXX" or "LeetCode XXX - Title" 
        # But NOT inside [] (which would be a link)
        # Negative lookbehind for [ and negative lookahead for ]( 
        result = re.sub(
            r'(?<!\[)LeetCode\s+(\d+)(\s*[-–—:]\s*[^(\[\]\n]+)?(?!\]\()',
            convert_plain_text,
            result
        )
        
        return result
    
    def _build_complete_link(self, problem_id: str, problem: dict) -> str:
        """
        Build complete link with LeetCode URL and Solution link.
        
        Output: [LeetCode {id} - {title}](url) · [Solution](github_url)
        """
        # Get LeetCode URL
        url = problem.get("url", "")
        if not url:
            return f"LeetCode {problem_id}"
        
        # Ensure URL ends with /description/
        if not url.endswith("/description/"):
            url = url.rstrip("/") + "/description/"
        
        # Build link text with title
        title = problem.get("title", "")
        if title:
            link_text = f"LeetCode {problem_id} - {title}"
        else:
            link_text = f"LeetCode {problem_id}"
        
        leetcode_link = f"[{link_text}]({url})"
        
        # Add Solution link if available
        solution_file = problem.get("solution_file", "")
        if solution_file:
            github_url = f"https://github.com/lufftw/neetcode/blob/main/{solution_file}"
            return f"{leetcode_link} · [Solution]({github_url})"
        
        return leetcode_link
    
    def _add_github_solution_links(self, content: str) -> str:
        """
        Automatically add GitHub solution links when seeing "LeetCode {id}".
        
        Pattern: [LeetCode {id}](leetcode_url)
        Result: [LeetCode {id}](leetcode_url) · [Solution](github_url)
        
        Note: Only adds if not already present (avoids duplicates).
        """
        # Debug: Check if we have problems data
        if not self.problems_lookup:
            print("  ⚠ Post-processing: No problems data loaded (cannot add Solution links)")
            return content
        
        # Count matches for debugging
        matches_found = 0
        links_added = 0
        
        # Pattern to match: [LeetCode {id}](url)
        def add_solution_link(match: re.Match) -> str:
            nonlocal matches_found, links_added
            matches_found += 1
            
            full_text = match.group(0)
            link_text = match.group(1)  # The text inside []
            url = match.group(2)  # The URL
            
            # Skip if already has GitHub solution link
            if "· [Solution](" in full_text or "· [solution](" in full_text or "| [Solution](" in full_text or "| [solution](" in full_text:
                return full_text
            
            # Extract problem ID from link text
            id_match = re.search(r'LeetCode\s+(\d+)', link_text)
            if not id_match:
                return full_text
            
            problem_id = id_match.group(1)
            
            # Look up problem in our data
            # Try multiple ID formats for maximum compatibility
            problem = None
            lookup_keys = [
                problem_id.zfill(4),  # "0011"
                problem_id,          # "11"
            ]
            if problem_id.isdigit():
                lookup_keys.append(str(int(problem_id)).zfill(4))  # "0011" (from "11")
                lookup_keys.append(str(int(problem_id)))          # "11" (normalized)
            
            for key in lookup_keys:
                problem = self.problems_lookup.get(key)
                if problem:
                    break
            
            if not problem:
                # Debug: Show which ID was not found
                if matches_found <= 5:  # Only show first few to avoid spam
                    print(f"    ⚠ LeetCode {problem_id}: Problem not found in lookup (tried: {lookup_keys[:2]})")
                return full_text
            
            # Check if solution_file exists
            files = problem.get("files", {})
            if not files:
                if matches_found <= 5:
                    print(f"    ⚠ LeetCode {problem_id}: No 'files' key in problem data")
                return full_text
            
            solution_file = files.get("solution", "")
            if not solution_file:
                if matches_found <= 5:
                    print(f"    ⚠ LeetCode {problem_id}: No solution file (files={list(files.keys())})")
                return full_text
            
            # Generate GitHub URL
            github_url = self.github_template.format(solution_file=solution_file)
            
            # Add GitHub link after LeetCode link
            # Format: [LeetCode {id}](leetcode_url) · [Solution](github_url)
            links_added += 1
            if links_added <= 5:  # Show first few successful additions
                print(f"    ✓ Added Solution link for LeetCode {problem_id}")
            return f"{full_text} · [Solution]({github_url})"
        
        # Match markdown links with "LeetCode" in the text
        # Pattern: [LeetCode {id}](url) or [LeetCode {id} - ...](url)
        # Note: [^\]]* matches any character except ], so it handles "LeetCode 11" or "LeetCode 11 - Title"
        pattern = r'\[(LeetCode\s+\d+[^\]]*)\]\(([^)]+)\)'
        result = re.sub(pattern, add_solution_link, content)
        
        # Debug summary
        if matches_found > 0:
            print(f"  ℹ️  Found {matches_found} LeetCode links, added {links_added} Solution links")
        else:
            print("  ⚠ No LeetCode links found in content (pattern may not match)")
        
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


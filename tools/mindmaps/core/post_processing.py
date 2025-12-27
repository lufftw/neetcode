# tools/mindmaps/post_processing.py
"""Post-processing for mindmap content - adds LeetCode and Solution links."""

from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT
from .data import ProblemData


def load_leetcode_cache() -> dict[str, dict[str, Any]] | None:
    """
    Load LeetCode API cache data and build lookup by frontend_question_id.
    
    The cache file uses internal question_id as keys, but we need to lookup
    by frontend_question_id (the number users see, like "LeetCode 1").
    
    Returns:
        Dict with frontend_question_id (zero-padded) as keys, or None if cache doesn't exist
    """
    cache_file = PROJECT_ROOT / "tools" / "leetcode-api" / "crawler" / ".cache" / "leetcode_problems.json"
    if not cache_file.exists():
        return None
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            raw_cache = json.load(f)
        
        # Build lookup by frontend_question_id (the number users see)
        lookup = {}
        for _, problem in raw_cache.items():
            frontend_id = problem.get("frontend_question_id")
            if frontend_id:
                # Store with zero-padded key for consistent lookup
                key = str(frontend_id).zfill(4)
                lookup[key] = problem
                # Also store without padding
                lookup[str(frontend_id)] = problem
        
        return lookup
    except (json.JSONDecodeError, IOError):
        return None


def merge_leetcode_api_data(
    problems_dict: dict[str, ProblemData],
    api_problems: dict[str, dict[str, Any]] | None = None
) -> dict[str, dict[str, Any]]:
    """
    Convert ProblemData objects to dict and merge with API cache data.
    
    Args:
        problems_dict: Dict of ProblemData objects
        api_problems: LeetCode API cache data (optional, will load if None)
    
    Returns:
        Dict of problem data ready for post-processing
    """
    if api_problems is None:
        api_problems = load_leetcode_cache()
    
    # Convert ProblemData to dict format
    result = {}
    for problem_id, problem in problems_dict.items():
        problem_dict = {
            "id": problem.id,
            "leetcode_id": problem.leetcode_id,
            "title": problem.title,
            "slug": problem.slug,
            "url": problem.url,
            "difficulty": problem.difficulty,
            "files": {
                "solution": problem.solution_file,
            }
        }
        result[problem_id] = problem_dict
    
    # Merge with API cache data
    if api_problems:
        for problem_id, problem_data in result.items():
            # Normalize ID for lookup - try multiple formats
            normalized_ids = []
            if isinstance(problem_id, str):
                # If key is "0079_word_search", extract "0079"
                match = re.match(r'^(\d+)_', problem_id)
                if match:
                    normalized_ids.append(match.group(1).zfill(4))
                elif problem_id.isdigit():
                    normalized_ids.append(problem_id.zfill(4))
                else:
                    normalized_ids.append(problem_id)
            else:
                normalized_ids.append(str(problem_id).zfill(4))
            
            # Also try using leetcode_id from problem_data
            leetcode_id = problem_data.get("leetcode_id")
            if leetcode_id:
                normalized_ids.append(str(leetcode_id).zfill(4))
            
            # Try to find API data
            api_data = None
            for nid in normalized_ids:
                api_data = api_problems.get(nid)
                if api_data:
                    break
            
            if api_data:
                # Use API cache data as source of truth for consistency
                # Title from API cache takes priority (ensures consistency)
                api_title = api_data.get("title", "")
                if api_title:
                    problem_data["title"] = api_title
                
                # Supplement missing fields from API
                if not problem_data.get("url"):
                    problem_data["url"] = api_data.get("url", "")
                if not problem_data.get("slug"):
                    problem_data["slug"] = api_data.get("slug", "")
                if not problem_data.get("difficulty"):
                    problem_data["difficulty"] = api_data.get("difficulty", "")
    
    return result


class PostProcessor:
    """
    Post-processes mindmap content to add LeetCode and Solution links.
    
    Converts plain text "LeetCode 11" to links and adds Solution links automatically.
    Uses rule-based processing (not LLM) for 100% consistency.
    """
    
    def __init__(
        self,
        problems: dict[str, ProblemData],
        github_template: str | None = None
    ):
        """
        Initialize post-processor.
        
        Args:
            problems: Dict of ProblemData objects
            github_template: GitHub URL template (default: from config)
        """
        # Convert ProblemData to dict and merge with API cache
        self.problems = merge_leetcode_api_data(problems)
        self.problems_lookup = self._build_problems_lookup(self.problems)
        
        # GitHub URL template
        if github_template is None:
            from .config import get_config
            config = get_config()
            github_template = f"{config.github_repo_url}/blob/{config.github_branch}/{{solution_file}}"
        self.github_template = github_template
    
    def _build_problems_lookup(self, problems: dict[str, dict[str, Any]]) -> dict[str, dict]:
        """Build lookup dictionary for problems by ID (supports multiple ID formats)."""
        lookup = {}
        
        for key, value in problems.items():
            if not isinstance(value, dict):
                continue
            
            # Get problem ID from various sources
            problem_id = value.get("id") or value.get("leetcode_id")
            
            # Extract from key if needed (e.g., "0079_word_search" -> "0079")
            if not problem_id:
                match = re.match(r'^(\d+)_', key)
                if match:
                    problem_id = match.group(1)
            
            if not problem_id:
                continue
            
            # Normalize to string
            if isinstance(problem_id, int):
                problem_id_str = str(problem_id)
            else:
                problem_id_str = str(problem_id)
            
            # Store with multiple formats for compatibility
            if problem_id_str.isdigit():
                # 4-digit format: "0011"
                normalized_id = problem_id_str.zfill(4)
                if normalized_id not in lookup:
                    lookup[normalized_id] = value
                
                # Integer string: "11"
                int_id = str(int(problem_id_str))
                if int_id != normalized_id and int_id not in lookup:
                    lookup[int_id] = value
        
        return lookup
    
    def process(self, content: str) -> str:
        """
        Apply post-processing transformations.
        
        Steps:
        1. Text replacement (LC -> LeetCode)
        2. Convert plain text to links
        3. Normalize LeetCode URLs
        4. Add Solution links
        
        Args:
            content: Markdown content to process
        
        Returns:
            Processed content with standardized links
        """
        result = content
        
        # Step 1: Text replacement
        result = re.sub(r"\bLC[-\s]?(\d+)", r"LeetCode \1", result)
        result = re.sub(r"LeetCode(\d+)", r"LeetCode \1", result)
        
        # Step 2: Convert plain text to links
        result = self._convert_plain_leetcode_to_links(result)
        
        # Step 3: Normalize LeetCode links
        result = self._normalize_leetcode_links(result)
        
        # Step 4: Add Solution links
        result = self._add_github_solution_links(result)
        
        return result
    
    def _convert_plain_leetcode_to_links(self, content: str) -> str:
        """Convert plain text 'LeetCode XXX' to proper links."""
        # First, handle existing markdown links - replace with our data
        def replace_existing_link(match: re.Match) -> str:
            link_text = match.group(1)
            url = match.group(2)
            
            # Extract problem ID
            id_match = re.search(r'LeetCode\s+(\d+)', link_text)
            if not id_match:
                return match.group(0)
            
            problem_id = id_match.group(1)
            problem = self.problems_lookup.get(problem_id.zfill(4)) or self.problems_lookup.get(problem_id)
            
            if not problem:
                return match.group(0)
            
            problem_url = problem.get("url", "")
            if not problem_url:
                return match.group(0)
            
            # Ensure URL ends with /description/
            if not problem_url.endswith("/description/"):
                problem_url = problem_url.rstrip("/") + "/description/"
            
            # Include title in link: [LeetCode {id} - {title}](url)
            title = problem.get("title", "")
            if title:
                return f"[LeetCode {problem_id} - {title}]({problem_url})"
            return f"[LeetCode {problem_id}]({problem_url})"
        
        # Replace existing links
        result = re.sub(
            r'\[(LeetCode\s+\d+[^\]]*)\]\(([^)]+)\)',
            replace_existing_link,
            content
        )
        
        # Now handle plain text "LeetCode XXX" that's NOT already a link
        # Also handle cases with difficulty icon: "🟢 LeetCode 11 - Title"
        def convert_plain_text(match: re.Match) -> str:
            full_match = match.group(0)
            difficulty_icon = match.group(1)  # Group 1: difficulty icon (optional)
            problem_id = match.group(2)      # Group 2: problem ID
            
            # Look up in our metadata
            problem = self.problems_lookup.get(problem_id.zfill(4)) or self.problems_lookup.get(problem_id)
            
            if not problem:
                return full_match
            
            url = problem.get("url", "")
            if not url:
                return full_match
            
            # Ensure URL ends with /description/
            if not url.endswith("/description/"):
                url = url.rstrip("/") + "/description/"
            
            # Include title in link: [LeetCode {id} - {title}](url) (preserve icon if present)
            icon_prefix = f"{difficulty_icon} " if difficulty_icon else ""
            title = problem.get("title", "")
            if title:
                return f"{icon_prefix}[LeetCode {problem_id} - {title}]({url})"
            return f"{icon_prefix}[LeetCode {problem_id}]({url})"
        
        # Pattern: Plain text "LeetCode XXX" or "LeetCode XXX - Title"
        # Also match optional difficulty icon: "🟢 LeetCode 11 - Title"
        # But NOT inside [] (which would be a link)
        # Group 1: difficulty icon (optional)
        # Group 2: problem ID
        # Group 3: title part (optional, not used)
        result = re.sub(
            r'(?<!\[)([🟢🟡🔴⚪])?\s*LeetCode\s+(\d+)(\s*[-–—:]\s*[^(\[\]\n]+)?(?!\]\()',
            convert_plain_text,
            result
        )
        
        return result
    
    def _normalize_leetcode_links(self, content: str) -> str:
        """Normalize LeetCode problem links to correct format."""
        def normalize_url(match: re.Match) -> str:
            link_text = match.group(1)
            url = match.group(2)
            
            # Skip if already has /description/
            if "/description/" in url:
                return match.group(0)
            
            # Extract slug from URL
            slug_match = re.search(r'/problems/([^/]+)/?', url)
            if not slug_match:
                return match.group(0)
            
            slug = slug_match.group(1)
            
            # Normalize slug: 0011_container_with_most_water -> container-with-most-water
            normalized_slug = self._normalize_slug(slug)
            
            # Reconstruct URL with /description/
            new_url = f"https://leetcode.com/problems/{normalized_slug}/description/"
            return f"[{link_text}]({new_url})"
        
        # Match markdown links: [text](https://leetcode.com/problems/...)
        pattern = r'\[([^\]]+)\]\((https://leetcode\.com/problems/[^)]+)\)'
        result = re.sub(pattern, normalize_url, content)
        
        return result
    
    def _normalize_slug(self, slug: str) -> str:
        """Normalize problem slug to LeetCode format."""
        # Remove leading digits and underscore if present
        slug = re.sub(r'^\d+_', '', slug)
        # Convert underscores to hyphens
        slug = slug.replace('_', '-')
        return slug
    
    def _add_github_solution_links(self, content: str) -> str:
        """Automatically add GitHub solution links when seeing 'LeetCode {id}'."""
        if not self.problems_lookup:
            return content
        
        def add_solution_link(match: re.Match) -> str:
            full_text = match.group(0)
            link_text = match.group(1)
            url = match.group(2)
            
            # Skip if already has GitHub solution link
            if "· [Solution](" in full_text or "· [solution](" in full_text or "| [Solution](" in full_text or "| [solution](" in full_text:
                return full_text
            
            # Extract problem ID
            id_match = re.search(r'LeetCode\s+(\d+)', link_text)
            if not id_match:
                return full_text
            
            problem_id = id_match.group(1)
            
            # Look up problem
            problem = None
            lookup_keys = [
                problem_id.zfill(4),  # "0011"
                problem_id,           # "11"
            ]
            if problem_id.isdigit():
                lookup_keys.append(str(int(problem_id)).zfill(4))
                lookup_keys.append(str(int(problem_id)))
            
            for key in lookup_keys:
                problem = self.problems_lookup.get(key)
                if problem:
                    break
            
            if not problem:
                return full_text
            
            # Check if solution file exists
            files = problem.get("files", {})
            solution_file = files.get("solution", "") if files else ""
            
            if not solution_file:
                return full_text
            
            # Generate GitHub URL
            github_url = self.github_template.format(solution_file=solution_file)
            
            # Add GitHub link after LeetCode link
            return f"{full_text} · [Solution]({github_url})"
        
        # Match markdown links with "LeetCode" in the text
        pattern = r'\[(LeetCode\s+\d+[^\]]*)\]\(([^)]+)\)'
        result = re.sub(pattern, add_solution_link, content)
        
        return result


def post_process_content(
    content: str,
    problems: dict[str, ProblemData],
    github_template: str | None = None
) -> str:
    """
    Convenience function to post-process mindmap content.
    
    Args:
        content: Markdown content to process
        problems: Dict of ProblemData objects
        github_template: Optional GitHub URL template
    
    Returns:
        Processed content with standardized links
    """
    processor = PostProcessor(problems, github_template)
    return processor.process(content)


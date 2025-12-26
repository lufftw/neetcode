#!/usr/bin/env python3
"""
Auto-fix File-Level Docstring for solution files

This tool automatically fixes solution file docstrings to comply with
review-code.md specification.

Usage:
    python tools/review-code/fix_docstring.py [--range START END] [--file FILE] [--dry-run] [--fetch-online]
    
Examples:
    # Fix all files
    python tools/review-code/fix_docstring.py
    
    # Fix files in range (e.g., 0077-0142)
    python tools/review-code/fix_docstring.py --range 0077 0142
    
    # Fix specific file
    python tools/review-code/fix_docstring.py --file 0077_combinations.py
    
    # Dry run (show what would be changed without modifying files)
    python tools/review-code/fix_docstring.py --dry-run
    
    # Fetch missing Problem and Link from LeetCode API cache
    python tools/review-code/fix_docstring.py --fetch-online
    
    # Combine: preview with online fetching
    python tools/review-code/fix_docstring.py --range 0077 0142 --fetch-online --dry-run
"""

import re
import sys
import argparse
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Tuple, List

# Project root directory
ROOT = Path(__file__).parent.parent.parent
SOLUTIONS_DIR = ROOT / "solutions"
TOOLS_DIR = ROOT / "tools"
CACHE_FILE = TOOLS_DIR / ".cache" / "leetcode_problems.json"

GRAPHQL_URL = "https://leetcode.com/graphql"

class LeetCodeDataFetcher:
    """Fetch LeetCode problem data from cache or online via GraphQL."""
    
    def __init__(self):
        self.cache = None
        self._load_cache()
    
    def _load_cache(self) -> None:
        """Load LeetCode problems cache."""
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.cache = None
    
    def _fetch_online(self, slug: str) -> Optional[Dict]:
        """Fetch problem data online using GraphQL."""
        query = """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            title
            content
            constraints: mysqlConstraints
          }
        }
        """
        variables = {"titleSlug": slug}
        try:
            response = requests.post(
                GRAPHQL_URL,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json().get("data", {}).get("question")
            if data:
                return {
                    "title": data.get("title"),
                    "description_html": data.get("content"),
                    "constraints_html": data.get("constraints")
                }
        except Exception:
            return None
        return None
    
    def get_problem_info(self, problem_id: str) -> Optional[Dict[str, str]]:
        """Get problem info from cache by ID (e.g., '0077')."""
        if not self.cache:
            return None
        
        def normalize_url(url: str, slug: str) -> str:
            """Normalize URL to remove /description/ suffix if present."""
            if not url:
                return f"https://leetcode.com/problems/{slug}/"
            url = url.rstrip('/')
            if url.endswith('/description'):
                url = url[:-11]
            if not url.endswith('/'):
                url += '/'
            return url
        
        # Try exact match first
        problem = self.cache.get(problem_id)
        if problem:
            slug = problem.get('slug', '')
            url = normalize_url(problem.get('url', ''), slug)
            return {
                'title': problem.get('title', ''),
                'slug': slug,
                'url': url,
            }
        
        # Try without leading zeros
        problem_id_int = problem_id.lstrip('0') or '0'
        for key, value in self.cache.items():
            if value.get('question_id') == int(problem_id_int):
                slug = value.get('slug', '')
                url = normalize_url(value.get('url', ''), slug)
                return {
                    'title': value.get('title', ''),
                    'slug': slug,
                    'url': url,
                }
        
        return None
    
    def get_description_and_constraints(self, slug: str) -> Tuple[List[str], List[str]]:
        """Fetch description and constraints from online (fallback to cache if needed)."""
        online_data = self._fetch_online(slug)
        if online_data:
            from bs4 import BeautifulSoup
            
            def parse_html_to_lines(html: str) -> List[str]:
                if not html:
                    return []
                soup = BeautifulSoup(html, "html.parser")
                lines = []
                for elem in soup.descendants:
                    if isinstance(elem, str) and elem.strip():
                        lines.append(elem.strip())
                    elif elem.name in ['br', 'p', 'li']:
                        lines.append("")  # empty line for separation
                # Clean up: join consecutive non-empty, keep structure
                cleaned = []
                current = []
                for line in lines:
                    if line:
                        current.append(line)
                    elif current:
                        cleaned.append(" ".join(current))
                        current = []
                if current:
                    cleaned.append(" ".join(current))
                return cleaned
            
            desc_lines = parse_html_to_lines(online_data.get("description_html"))
            const_lines = []
            const_html = online_data.get("constraints_html")
            if const_html:
                soup = BeautifulSoup(const_html, "html.parser")
                for li in soup.find_all('li'):
                    text = li.get_text(strip=True)
                    if text:
                        const_lines.append(f"- {text}")
            
            return desc_lines, const_lines
        
        return [], []

class DocstringFixer:
    """Fix docstrings to comply with review-code.md format."""
    
    def __init__(self, dry_run: bool = False, fetch_online: bool = False):
        self.dry_run = dry_run
        self.fetch_online = fetch_online
        self.fixed_count = 0
        self.skipped_count = 0
        self.errors = []
        self.leetcode_fetcher = LeetCodeDataFetcher()
    
    # ... (extract_problem_id_from_filename, extract_docstring, parse_docstring remain unchanged)
    
    def build_docstring(self, parsed: Dict, replace_mode: bool = False) -> str:
        """Build properly formatted docstring from parsed fields."""
        parts = []
        
        problem_text = parsed["problem"] or "[MISSING - NEEDS MANUAL FIX]"
        parts.append(f"Problem: {problem_text}")
        
        link_text = parsed["link"] or "[MISSING - NEEDS MANUAL FIX]"
        parts.append(f"Link: {link_text}")
        
        parts.append("")
        
        if parsed["description"]:
            parts.extend(parsed["description"])
            parts.append("")
        
        if not replace_mode:
            for field_name, field_value in parsed["optional_fields"].items():
                if field_value:
                    value_lines = field_value.split('\n')
                    parts.append(f"{field_name}: {value_lines[0]}")
                    for line in value_lines[1:]:
                        if line.strip():
                            parts.append(line)
        
        if parsed["constraints"]:
            parts.append("Constraints:")
            for constraint in parsed["constraints"]:
                parts.append(constraint)
        else:
            parts.append("Constraints:")
            parts.append("- [MISSING - NEEDS MANUAL FIX]")
        
        return '\n'.join(parts)
    
    def fix_file(self, file_path: Path, replace_mode: bool = False) -> Tuple[bool, List[str]]:
        """Fix docstring in a single file."""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return False, [f"Failed to read file: {e}"]
        
        docstring_info = self.extract_docstring(content)
        if not docstring_info:
            return False, ["No docstring found"]
        
        start_pos, end_pos, old_docstring = docstring_info
        
        parsed = self.parse_docstring(old_docstring)
        
        problem_id = self.extract_problem_id_from_filename(file_path.name)
        leetcode_info = None
        slug = None
        if problem_id:
            leetcode_info = self.leetcode_fetcher.get_problem_info(problem_id)
            if leetcode_info:
                slug = leetcode_info.get('slug')
        
        # Always update Problem and Link if available (in replace_mode or if missing)
        if leetcode_info:
            if replace_mode or not parsed["problem"]:
                parsed["problem"] = leetcode_info.get('title', '')
                issues.append("Updated Problem from cache" if not replace_mode else "Replaced Problem from cache")
            
            if replace_mode or not parsed["link"]:
                parsed["link"] = leetcode_info.get('url', '')
                issues.append("Updated Link from cache" if not replace_mode else "Replaced Link from cache")
        
        # In replace_mode, fetch description and constraints online
        if replace_mode and slug and self.fetch_online:
            desc_lines, const_lines = self.leetcode_fetcher.get_description_and_constraints(slug)
            if desc_lines:
                parsed["description"] = desc_lines
                issues.append("Fetched description online")
            if const_lines:
                parsed["constraints"] = const_lines
                issues.append("Fetched constraints online")
        
        # Determine if fixes needed (for non-replace mode)
        if replace_mode:
            new_docstring = self.build_docstring(parsed, replace_mode=True)
            fix_reasons = ["Complete replacement"] + issues
        else:
            needs_fix = False
            fix_reasons = []
            
            if parsed["has_decorative_separators"]:
                needs_fix = True
                fix_reasons.append("Has decorative separators")
            
            if not parsed["problem"]:
                needs_fix = True
                fix_reasons.append("Missing Problem field")
            
            if not parsed["link"]:
                needs_fix = True
                fix_reasons.append("Missing Link field")
            
            if not parsed["constraints"]:
                needs_fix = True
                fix_reasons.append("Missing Constraints section")
            
            if not needs_fix:
                return True, ["No fixes needed"]
            
            new_docstring = self.build_docstring(parsed, replace_mode=False)
            fix_reasons += issues
        
        new_content = (
            content[:start_pos] +
            '"""\n' +
            new_docstring +
            '\n"""' +
            content[end_pos:]
        )
        
        if not self.dry_run:
            try:
                file_path.write_text(new_content, encoding='utf-8')
                self.fixed_count += 1
                return True, fix_reasons
            except Exception as e:
                return False, [f"Failed to write file: {e}"]
        else:
            self.fixed_count += 1
            return True, fix_reasons + ["(DRY RUN - no changes made)"]
    
    # ... (fix_range, fix_single_file, fix_all, print_summary remain unchanged)

# main() remains the same, with --fetch-online default=True

if __name__ == "__main__":
    sys.exit(main())
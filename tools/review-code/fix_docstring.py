#!/usr/bin/env python3
"""
Auto-fix File-Level Docstring for solution files

This tool automatically fixes solution file docstrings to comply with
review-code.md specification by fetching data from LeetCode.

Features:
    - Uses SQLite cache for improved performance
    - Generates complete docstrings with Examples, Constraints, Note, Follow-up
    - Preserves <img> tags in examples
    - Supports multi-line explanations

Usage:
    python tools/review-code/fix_docstring.py --range START END [--delay-min SEC] [--delay-max SEC]
    
Examples:
    # Fix files in range (e.g., 0077-0142)
    python tools/review-code/fix_docstring.py --range 77 142
    
    # Fix single file (e.g., 0202)
    python tools/review-code/fix_docstring.py --range 202 202
    
    # Set custom delay range to avoid rate limiting
    python tools/review-code/fix_docstring.py --range 77 142 --delay-min 3.0 --delay-max 8.0
    
    # Force refresh from network (bypass cache)
    python tools/review-code/fix_docstring.py --range 77 77 --force-refresh
"""

import re
import sys
import argparse
import json
import time
import random
from pathlib import Path
from typing import Optional, Dict, Tuple, List

# Add leetcode-api to path for imports
_LEETCODE_API_PATH = Path(__file__).parent.parent / "leetcode-api"
if str(_LEETCODE_API_PATH) not in sys.path:
    sys.path.insert(0, str(_LEETCODE_API_PATH))

from leetscrape_fetcher import get_full_docstring_data

# Project root directory
ROOT = Path(__file__).parent.parent.parent
SOLUTIONS_DIR = ROOT / "solutions"
CACHE_FILE = ROOT / "tools" / ".cache" / "leetcode_problems.json"


class DocstringBuilder:
    """Build docstrings according to review-code.md specification."""
    
    INDENT = "    "  # 4-space indentation for examples
    
    @classmethod
    def build(cls, data: dict) -> str:
        """
        Build a complete docstring from structured data.
        
        Args:
            data: Dictionary from get_full_docstring_data() containing:
                  - title, url, description, examples, constraints, follow_ups, note
        
        Returns:
            Formatted docstring content (without triple quotes)
        """
        parts = []
        
        # Problem and Link (required)
        parts.append(f"Problem: {data.get('title', '')}")
        parts.append(f"Link: {data.get('url', '')}")
        parts.append("")
        
        # Description
        description = data.get('description', [])
        if description:
            parts.extend(description)
            parts.append("")
        
        # Examples (all of them, with img tags preserved)
        examples = data.get('examples', [])
        for ex in examples:
            parts.append(f"Example {ex['number']}:")
            
            # Preserve <img> tag if present
            if ex.get('img'):
                parts.append(f"{cls.INDENT}{ex['img']}")
            
            # Input
            if ex.get('input'):
                parts.append(f"{cls.INDENT}Input: {ex['input']}")
            
            # Output
            if ex.get('output'):
                parts.append(f"{cls.INDENT}Output: {ex['output']}")
            
            # Explanation (may be multi-line, align to first line)
            if ex.get('explanation'):
                expl_lines = ex['explanation'].split('\n')
                parts.append(f"{cls.INDENT}Explanation: {expl_lines[0]}")
                # Continuation lines aligned to "Explanation: " (13 chars + 4 indent = 17)
                continuation_indent = cls.INDENT + " " * 13
                for line in expl_lines[1:]:
                    if line.strip():
                        parts.append(f"{continuation_indent}{line.strip()}")
            
            parts.append("")
        
        # Constraints
        parts.append("Constraints:")
        constraints = data.get('constraints', [])
        if constraints:
            parts.extend(constraints)
        else:
            parts.append("- [MISSING - NEEDS MANUAL FIX]")
        
        # Note (optional, with blank line before)
        note = data.get('note')
        if note:
            parts.append("")
            parts.append(f"Note: {note}")
        
        # Follow-up (optional, with blank line before)
        follow_ups = data.get('follow_ups', [])
        if follow_ups:
            parts.append("")
            for follow_up in follow_ups:
                parts.append(f"Follow-up: {follow_up}")
        
        return '\n'.join(parts)


class DocstringFixer:
    """Fix docstrings to comply with review-code.md format."""
    
    def __init__(self, delay_min: float = 3.0, delay_max: float = 8.0, force_refresh: bool = False):
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.force_refresh = force_refresh
        self.cache = self._load_cache()
        self.fixed_count = 0
        self.skipped_count = 0
        self.cached_count = 0
        self.errors: List[Tuple[str, str]] = []
    
    def _load_cache(self) -> Optional[Dict]:
        """Load LeetCode problems cache (for slug lookup)."""
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return None
    
    def _random_delay(self) -> None:
        """Sleep for a random duration to avoid rate limiting."""
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)
    
    def _get_problem_info(self, problem_id: str) -> Optional[Dict[str, str]]:
        """Get problem info from cache by ID (e.g., '0077' or '77')."""
        if not self.cache:
            return None
        
        # Normalize problem ID
        problem_id_int = int(problem_id.lstrip('0') or '0')
        
        for key, value in self.cache.items():
            if value.get('question_id') == problem_id_int:
                slug = value.get('slug', '')
                url = f"https://leetcode.com/problems/{slug}/"
                return {
                    'title': value.get('title', ''),
                    'slug': slug,
                    'url': url,
                }
        return None
    
    def fix_file(self, file_path: Path) -> Tuple[bool, str]:
        """Fix docstring in a single file."""
        # Extract problem ID from filename
        match = re.match(r'^(\d{4})_', file_path.name)
        if not match:
            return False, "Invalid filename format"
        
        problem_id = match.group(1)
        
        # Get problem info from cache (for slug lookup)
        info = self._get_problem_info(problem_id)
        if not info:
            return False, "Problem not found in cache"
        
        slug = info['slug']
        
        # Check if we need to fetch from network (rate limiting only for network calls)
        from question_api import get_default_api
        api = get_default_api()
        is_cached = api.exists(slug)
        
        if not is_cached or self.force_refresh:
            print(f"  Fetching {slug}...", end=" ", flush=True)
            self._random_delay()
        else:
            print(f"  Using cached {slug}...", end=" ", flush=True)
            self.cached_count += 1
        
        # Get full docstring data using new API
        data = get_full_docstring_data(slug)
        
        if not data.get('title'):
            print("(fetch failed)")
            return False, "Failed to fetch question data"
        
        print(f"({len(data.get('examples', []))} examples, {len(data.get('constraints', []))} constraints)")
        
        # Build new docstring
        new_docstring = DocstringBuilder.build(data)
        
        # Read file and replace docstring
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return False, f"Failed to read: {e}"
        
        # Find and replace docstring
        docstring_pattern = re.compile(r'^""".*?"""', re.MULTILINE | re.DOTALL)
        match = docstring_pattern.search(content)
        
        if not match:
            return False, "No docstring found"
        
        new_content = (
            content[:match.start()] +
            '"""\n' + new_docstring + '\n"""' +
            content[match.end():]
        )
        
        # Write back
        try:
            file_path.write_text(new_content, encoding='utf-8')
            return True, "Updated"
        except Exception as e:
            return False, f"Failed to write: {e}"
    
    def fix_range(self, start_num: int, end_num: int) -> None:
        """Fix files in a numeric range."""
        pattern = re.compile(r'^(\d{4})_')
        
        for file_path in sorted(SOLUTIONS_DIR.glob("*.py")):
            m = pattern.match(file_path.name)
            if not m:
                continue
            
            num = int(m.group(1))
            if start_num <= num <= end_num:
                success, msg = self.fix_file(file_path)
                if success:
                    print(f"[OK] {file_path.name}: {msg}")
                    self.fixed_count += 1
                else:
                    print(f"[ERROR] {file_path.name}: {msg}")
                    self.errors.append((file_path.name, msg))
    
    def print_summary(self) -> None:
        """Print summary of fixes."""
        print("\n" + "=" * 50)
        print(f"Summary: Fixed {self.fixed_count} files")
        print(f"  - From cache: {self.cached_count}")
        print(f"  - From network: {self.fixed_count - self.cached_count}")
        if self.errors:
            print(f"Errors: {len(self.errors)}")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Auto-fix File-Level Docstring for solution files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--range", nargs=2, metavar=("START", "END"), type=int,
                        required=True, help="Fix files in numeric range (e.g., --range 77 142)")
    parser.add_argument("--delay-min", type=float, default=3.0,
                        help="Minimum delay between network requests in seconds (default: 3.0)")
    parser.add_argument("--delay-max", type=float, default=8.0,
                        help="Maximum delay between network requests in seconds (default: 8.0)")
    parser.add_argument("--force-refresh", action="store_true",
                        help="Force refresh from network, bypassing SQLite cache")
    
    args = parser.parse_args()
    
    if args.delay_min > args.delay_max:
        print("Error: delay-min must be <= delay-max")
        return 1
    
    start, end = args.range
    print(f"\nProcessing {start:04d} ~ {end:04d}")
    print(f"Delay: {args.delay_min:.1f}s ~ {args.delay_max:.1f}s")
    print(f"Force refresh: {args.force_refresh}\n")
    
    fixer = DocstringFixer(
        delay_min=args.delay_min, 
        delay_max=args.delay_max,
        force_refresh=args.force_refresh
    )
    fixer.fix_range(start, end)
    fixer.print_summary()
    
    return 0 if not fixer.errors else 1


if __name__ == "__main__":
    sys.exit(main())

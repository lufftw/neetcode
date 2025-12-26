#!/usr/bin/env python3
"""
Auto-fix File-Level Docstring for solution files

This tool automatically fixes solution file docstrings to comply with
review-code.md specification by fetching data from LeetCode.

Usage:
    python tools/review-code/fix_docstring.py --range START END [--delay-min SEC] [--delay-max SEC]
    
Examples:
    # Fix files in range (e.g., 0077-0142)
    python tools/review-code/fix_docstring.py --range 77 142
    
    # Fix single file (e.g., 0202)
    python tools/review-code/fix_docstring.py --range 202 202
    
    # Set custom delay range to avoid rate limiting
    python tools/review-code/fix_docstring.py --range 77 142 --delay-min 3.0 --delay-max 8.0
"""

import re
import sys
import argparse
import json
import time
import random
from pathlib import Path
from typing import Optional, Dict, Tuple, List

from leetscrape_fetcher import get_description_and_constraints

# Project root directory
ROOT = Path(__file__).parent.parent.parent
SOLUTIONS_DIR = ROOT / "solutions"
CACHE_FILE = ROOT / "tools" / ".cache" / "leetcode_problems.json"


class DocstringFixer:
    """Fix docstrings to comply with review-code.md format."""
    
    def __init__(self, delay_min: float = 3.0, delay_max: float = 8.0):
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.cache = self._load_cache()
        self.fixed_count = 0
        self.skipped_count = 0
        self.errors: List[Tuple[str, str]] = []
    
    def _load_cache(self) -> Optional[Dict]:
        """Load LeetCode problems cache."""
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
    
    def _build_docstring(self, title: str, url: str, description: List[str], constraints: List[str]) -> str:
        """Build properly formatted docstring."""
        parts = [f"Problem: {title}", f"Link: {url}", ""]
        
        if description:
            parts.extend(description)
            parts.append("")
        
        parts.append("Constraints:")
        if constraints:
            parts.extend(constraints)
        else:
            parts.append("- [MISSING - NEEDS MANUAL FIX]")
        
        return '\n'.join(parts)
    
    def fix_file(self, file_path: Path) -> Tuple[bool, str]:
        """Fix docstring in a single file."""
        # Extract problem ID from filename
        match = re.match(r'^(\d{4})_', file_path.name)
        if not match:
            return False, "Invalid filename format"
        
        problem_id = match.group(1)
        
        # Get problem info from cache
        info = self._get_problem_info(problem_id)
        if not info:
            return False, "Problem not found in cache"
        
        title = info['title']
        url = info['url']
        slug = info['slug']
        
        # Fetch description and constraints online
        print(f"  Fetching {slug}...", end=" ", flush=True)
        self._random_delay()
        desc_lines, const_lines = get_description_and_constraints(slug)
        
        if not const_lines:
            print("(no constraints found)")
        else:
            print(f"({len(const_lines)} constraints)")
        
        # Build new docstring
        new_docstring = self._build_docstring(title, url, desc_lines, const_lines)
        
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
                        help="Minimum delay between requests in seconds (default: 3.0)")
    parser.add_argument("--delay-max", type=float, default=8.0,
                        help="Maximum delay between requests in seconds (default: 8.0)")
    
    args = parser.parse_args()
    
    if args.delay_min > args.delay_max:
        print("Error: delay-min must be <= delay-max")
        return 1
    
    start, end = args.range
    print(f"\nProcessing {start:04d} ~ {end:04d}")
    print(f"Delay: {args.delay_min:.1f}s ~ {args.delay_max:.1f}s\n")
    
    fixer = DocstringFixer(delay_min=args.delay_min, delay_max=args.delay_max)
    fixer.fix_range(start, end)
    fixer.print_summary()
    
    return 0 if not fixer.errors else 1


if __name__ == "__main__":
    sys.exit(main())

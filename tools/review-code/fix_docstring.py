#!/usr/bin/env python3
"""
Auto-fix File-Level Docstring for solution files

This tool automatically fixes solution file docstrings to comply with
README.md specification by fetching data from LeetCode.

Features:
    - Uses SQLite cache for improved performance
    - Generates complete docstrings with Examples, Constraints, Topics, Hints, Note, Follow-up
    - Preserves <img> tags in examples
    - Supports multi-line explanations
    - Topics: Comma-separated topic tags
    - Hints: Numbered format (Hint 1:, Hint 2:, etc.) with blank lines between

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
import time
import random
from pathlib import Path
from typing import Optional, Dict, Tuple, List

# Add tools directory to path for imports
_TOOLS_PATH = Path(__file__).parent.parent
if str(_TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(_TOOLS_PATH))

# Add leetcode-api to path for imports
_LEETCODE_API_PATH = Path(__file__).parent.parent / "leetcode-api"
if str(_LEETCODE_API_PATH) not in sys.path:
    sys.path.insert(0, str(_LEETCODE_API_PATH))

from docstring.formatter import get_full_docstring_data

# Use leetcode_datasource package for problem index lookup
from leetcode_datasource import LeetCodeDataSource

# Project root directory
ROOT = Path(__file__).parent.parent.parent
SOLUTIONS_DIR = ROOT / "solutions"

# Initialize datasource for problem index lookups
_datasource: Optional[LeetCodeDataSource] = None


def get_datasource() -> LeetCodeDataSource:
    """Get or initialize the LeetCodeDataSource singleton."""
    global _datasource
    if _datasource is None:
        _datasource = LeetCodeDataSource()
    return _datasource


class DocstringBuilder:
    """Build docstrings according to README.md specification."""
    
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
        
        # Topics (recommended, with blank line before)
        topics = data.get('topics', '')
        if topics:
            parts.append("")
            parts.append(f"Topics: {topics}")
        
        # Hints (optional, with blank line before, numbered format)
        hints = data.get('hints', [])
        if hints:
            parts.append("")
            for hint in hints:
                parts.append(hint)
                parts.append("")  # Blank line between each hint
            # Remove the trailing blank line (will be added by note/follow-up or end)
            if parts and parts[-1] == "":
                parts.pop()
        
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
    """Fix docstrings to comply with README.md format."""
    
    def __init__(self, delay_min: float = 3.0, delay_max: float = 8.0, force_refresh: bool = False):
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.force_refresh = force_refresh
        self.ds = get_datasource()
        
        # Check if problem_index is populated
        stats = self.ds.stats()
        if stats.get('problem_index_count', 0) == 0:
            print("Problem index is empty. Syncing from LeetCode API...")
            count = self.ds.sync_problem_list()
            print(f"Synced {count} problems to problem_index")
            print()
        
        self.fixed_count = 0
        self.skipped_count = 0
        self.cached_count = 0
        self.errors: List[Tuple[str, str]] = []
    
    def _random_delay(self) -> None:
        """Sleep for a random duration to avoid rate limiting."""
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)
    
    def _get_problem_info(self, problem_id: str) -> Optional[Dict[str, str]]:
        """Get problem info from problem_index by ID (e.g., '0077' or '77').
        
        Uses leetcode_datasource package for fast lookup via problem_index table.
        """
        # Normalize problem ID
        problem_id_int = int(problem_id.lstrip('0') or '0')
        
        # Use leetcode_datasource package
        info = self.ds.get_problem_info(problem_id_int)
        if info:
            return {
                'title': info.title,
                'slug': info.title_slug,
                'url': info.url or f"https://leetcode.com/problems/{info.title_slug}/",
            }
        return None
    
    def _is_paid_only_content(self, data: dict) -> bool:
        """Check if the question content indicates paid-only access."""
        description = data.get('description', [])
        if not description:
            return False
        
        # Check if description contains paid-only message
        desc_text = ' '.join(description).lower()
        paid_keywords = [
            'only for paid',
            'premium members',
            'subscribe to unlock',
            'paid subscribers',
        ]
        return any(kw in desc_text for kw in paid_keywords)
    
    def _prompt_paid_only(self, file_path: Path, data: dict) -> bool:
        """
        Prompt user for paid-only question.
        
        Returns:
            True if user wants to overwrite, False to skip
        """
        print()
        print("=" * 60)
        print(f"[PAID ONLY] {file_path.name}")
        print(f"  Title: {data.get('title', 'Unknown')}")
        print(f"  URL: {data.get('url', 'Unknown')}")
        print()
        print("  This question is only for paid LeetCode subscribers.")
        print("  The docstring will contain limited information.")
        print("=" * 60)
        
        while True:
            response = input("  Overwrite File-Level Docstring? [y/N]: ").strip().lower()
            if response in ('y', 'yes'):
                return True
            elif response in ('n', 'no', ''):
                return False
            print("  Please enter 'y' or 'n'")
    
    def fix_file(self, file_path: Path) -> Tuple[bool, str]:
        """Fix docstring in a single file."""
        # Extract problem ID from filename
        match = re.match(r'^(\d{4})_', file_path.name)
        if not match:
            return False, "Invalid filename format"
        
        problem_id = match.group(1)
        
        # Get problem info from problem_index (for slug lookup)
        info = self._get_problem_info(problem_id)
        if not info:
            return False, f"Problem {problem_id} not found in problem_index. Try: ds.sync_problem_list(refresh=True)"
        
        slug = info['slug']
        
        # Check if data exists in local SQLite cache (using leetcode_datasource)
        is_cached = self.ds.exists(slug)
        
        # Only apply delay for network requests, skip delay for local cache
        if is_cached and not self.force_refresh:
            # Local cache hit - no delay needed
            print(f"  [cache] {slug}...", end=" ", flush=True)
            self.cached_count += 1
        else:
            # Network fetch required - apply delay to avoid rate limiting
            print(f"  [network] {slug}...", end=" ", flush=True)
            self._random_delay()
        
        # Get full docstring data (uses cache if available, otherwise fetches)
        data = get_full_docstring_data(slug)
        
        if not data.get('title'):
            print("(fetch failed)")
            return False, "Failed to fetch question data"
        
        hints_count = len(data.get('hints', []))
        topics = data.get('topics', '')
        topics_count = len(topics.split(',')) if topics else 0
        print(f"({len(data.get('examples', []))} examples, {len(data.get('constraints', []))} constraints, {topics_count} topics, {hints_count} hints)")
        
        # Check if this is a paid-only question with limited content
        if self._is_paid_only_content(data):
            if not self._prompt_paid_only(file_path, data):
                self.skipped_count += 1
                return False, "Skipped (paid-only, user declined)"
        
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
        network_count = self.fixed_count - self.cached_count
        
        print("\n" + "=" * 50)
        print(f"Summary: Fixed {self.fixed_count} files")
        print(f"  - From cache (no delay): {self.cached_count}")
        print(f"  - From network (with delay): {network_count}")
        if self.skipped_count > 0:
            print(f"Skipped: {self.skipped_count} (paid-only, user declined)")
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

#!/usr/bin/env python3
"""
Auto-fix File-Level Docstring for solution files

This tool automatically fixes solution file docstrings to comply with
review-code.md specification.

Usage:
    python tools/review-code/fix_docstring.py [--range START END] [--file FILE] [--dry-run] [--fetch-online] [--delay-min SEC] [--delay-max SEC]
    
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
    
    # Set custom delay range to avoid anti-crawling (1-5 seconds)
    python tools/review-code/fix_docstring.py --range 0077 0142 --delay-min 1.0 --delay-max 5.0
    
    # Combine: preview with online fetching and custom delay
    python tools/review-code/fix_docstring.py --range 0077 0142 --fetch-online --dry-run --delay-min 2.0 --delay-max 4.0
"""

import re
import sys
import argparse
import json
import requests
import time
import random
from pathlib import Path
from typing import Optional, Dict, Tuple, List

# Import leetscrape_fetcher for fetching description and constraints
from leetscrape_fetcher import get_description_and_constraints as leetscrape_get_desc_and_const

# Project root directory
ROOT = Path(__file__).parent.parent.parent
SOLUTIONS_DIR = ROOT / "solutions"
TOOLS_DIR = ROOT / "tools"
CACHE_FILE = TOOLS_DIR / ".cache" / "leetcode_problems.json"

GRAPHQL_URL = "https://leetcode.com/graphql"

class LeetCodeDataFetcher:
    """Fetch LeetCode problem data from cache or online via GraphQL."""
    
    def __init__(self, delay_min: float = 1.0, delay_max: float = 3.0):
        """
        Initialize LeetCode data fetcher.
        
        Args:
            delay_min: Minimum delay in seconds between requests (default: 1.0)
            delay_max: Maximum delay in seconds between requests (default: 3.0)
        """
        self.cache = None
        self.delay_min = delay_min
        self.delay_max = delay_max
        self._load_cache()
    
    def _random_delay(self) -> None:
        """Sleep for a random duration between delay_min and delay_max to avoid anti-crawling."""
        if self.delay_min > 0 and self.delay_max > 0:
            delay = random.uniform(self.delay_min, self.delay_max)
            time.sleep(delay)
    
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
        # Add random delay before making request to avoid anti-crawling
        self._random_delay()
        
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
        """Fetch description and constraints using leetscrape_fetcher module."""
        # Add random delay before making request to avoid anti-crawling
        self._random_delay()
        
        # Use leetscrape_fetcher which has proper HTML parsing logic
        return leetscrape_get_desc_and_const(slug)

class DocstringFixer:
    """Fix docstrings to comply with review-code.md format."""
    
    def __init__(self, dry_run: bool = False, fetch_online: bool = False, 
                 delay_min: float = 1.0, delay_max: float = 3.0):
        """
        Initialize docstring fixer.
        
        Args:
            dry_run: If True, don't modify files (default: False)
            fetch_online: If True, fetch data from LeetCode online (default: False)
            delay_min: Minimum delay in seconds between requests (default: 1.0)
            delay_max: Maximum delay in seconds between requests (default: 3.0)
        """
        self.dry_run = dry_run
        self.fetch_online = fetch_online
        self.fixed_count = 0
        self.skipped_count = 0
        self.errors = []
        self.leetcode_fetcher = LeetCodeDataFetcher(delay_min=delay_min, delay_max=delay_max)
    
    def extract_problem_id_from_filename(self, filename: str) -> Optional[str]:
        """Extract problem ID from filename (e.g., '0077_combinations.py' -> '0077')."""
        match = re.match(r'^(\d{4})_', filename)
        return match.group(1) if match else None
    
    def extract_docstring(self, content: str) -> Optional[Tuple[int, int, str]]:
        """Extract docstring from file content."""
        match = re.search(r'^"""', content, re.MULTILINE)
        if not match:
            return None
        start_pos = match.start()
        remaining = content[start_pos + 3:]
        end_match = re.search(r'"""', remaining)
        if not end_match:
            return None
        end_pos = start_pos + 3 + end_match.end()
        docstring = content[start_pos + 3:end_pos - 3]
        return (start_pos, end_pos, docstring)
    
    def parse_docstring(self, docstring: str) -> Dict:
        """Parse docstring into structured fields."""
        result = {
            "problem": None,
            "link": None,
            "description": [],
            "optional_fields": {},
            "constraints": [],
            "has_decorative_separators": False,
        }
        
        lines = docstring.split('\n')
        current_section = None
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if re.match(r'^={3,}$|^-{3,}$', stripped):
                result["has_decorative_separators"] = True
                i += 1
                continue
            
            if re.match(r'^Problem:\s*(.+)$', line, re.IGNORECASE):
                result["problem"] = re.match(r'^Problem:\s*(.+)$', line, re.IGNORECASE).group(1).strip()
                i += 1
                continue
            
            if re.match(r'^Link:\s*(.+)$', line, re.IGNORECASE):
                result["link"] = re.match(r'^Link:\s*(.+)$', line, re.IGNORECASE).group(1).strip()
                i += 1
                continue
            
            optional_match = re.match(r'^(Sub-Pattern|Key Insight|API Kernel|Pattern|Family|Delta from .+?):\s*(.*)$', line, re.IGNORECASE)
            if optional_match:
                field_name = optional_match.group(1)
                field_value = optional_match.group(2).strip()
                value_lines = [field_value] if field_value else []
                i += 1
                while i < len(lines) and lines[i].strip() and not re.match(r'^(Problem|Link|Constraints?|Sub-Pattern|Key Insight|API Kernel|Pattern|Family|Delta from):', lines[i], re.IGNORECASE):
                    if not lines[i].strip().startswith('-'):
                        value_lines.append(lines[i].strip())
                    else:
                        break
                    i += 1
                result["optional_fields"][field_name] = '\n'.join(value_lines)
                continue
            
            if re.match(r'^Constraints?:?\s*$', line, re.IGNORECASE):
                current_section = "constraints"
                i += 1
                continue
            
            if current_section == "constraints" and re.match(r'^-\s*(.+)$', stripped):
                result["constraints"].append(stripped)
                i += 1
                continue
            
            if result["link"] and not current_section and stripped:
                if not re.match(r'^(Sub-Pattern|Key Insight|API Kernel|Pattern|Family|Constraints?|Delta from):', line, re.IGNORECASE):
                    result["description"].append(line.rstrip())
            
            i += 1
        
        result["description"] = [l for l in result["description"] if l.strip()]
        return result
    
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
    
    def _has_missing_placeholder(self, items: List[str]) -> bool:
        """Check if items contain [MISSING - NEEDS MANUAL FIX] placeholder."""
        for item in items:
            if "[MISSING" in item or "NEEDS MANUAL FIX" in item:
                return True
        return False
    
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
        
        # Check if constraints have placeholder that needs fixing
        constraints_need_fix = (
            not parsed["constraints"] or 
            self._has_missing_placeholder(parsed["constraints"])
        )
        
        # Fetch description and constraints online if needed
        if slug and self.fetch_online and (replace_mode or constraints_need_fix):
            desc_lines, const_lines = self.leetcode_fetcher.get_description_and_constraints(slug)
            if desc_lines and (replace_mode or not parsed["description"]):
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
            
            if not parsed["constraints"] or self._has_missing_placeholder(parsed["constraints"]):
                needs_fix = True
                fix_reasons.append("Missing or placeholder Constraints")
            
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
    
    def fix_range(self, start_num: int, end_num: int, replace_mode: bool = False) -> None:
        """Fix files in a numeric range."""
        pattern = re.compile(r'^(\d{4})_')
        for file_path in sorted(SOLUTIONS_DIR.glob("*.py")):
            m = pattern.match(file_path.name)
            if not m:
                continue
            num = int(m.group(1))
            if start_num <= num <= end_num:
                success, issues = self.fix_file(file_path, replace_mode=replace_mode)
                if success:
                    if issues[0] != "No fixes needed":
                        print(f"[OK] {file_path.name}: {', '.join(issues)}")
                    else:
                        self.skipped_count += 1
                else:
                    print(f"[ERROR] {file_path.name}: {', '.join(issues)}")
                    self.errors.append((file_path.name, issues))
    
    def fix_single_file(self, filename: str, replace_mode: bool = False) -> None:
        """Fix a single file."""
        file_path = SOLUTIONS_DIR / filename
        if not file_path.exists():
            print(f"Error: File not found: {filename}")
            return
        success, issues = self.fix_file(file_path, replace_mode=replace_mode)
        if success:
            if issues[0] != "No fixes needed":
                print(f"[OK] {file_path.name}: {', '.join(issues)}")
            else:
                print(f"[SKIPPED] {file_path.name}: No fixes needed")
        else:
            print(f"[ERROR] {file_path.name}: {', '.join(issues)}")
    
    def fix_all(self) -> None:
        """Fix all files in solutions directory."""
        for file_path in sorted(SOLUTIONS_DIR.glob("*.py")):
            success, issues = self.fix_file(file_path)
            if success:
                if issues[0] != "No fixes needed":
                    print(f"[OK] {file_path.name}: {', '.join(issues)}")
                else:
                    self.skipped_count += 1
            else:
                print(f"[ERROR] {file_path.name}: {', '.join(issues)}")
                self.errors.append((file_path.name, issues))
    
    def print_summary(self) -> None:
        """Print summary of fixes."""
        print("\n" + "=" * 60)
        print("Summary:")
        print(f"  Fixed: {self.fixed_count}")
        print(f"  Skipped: {self.skipped_count}")
        if self.errors:
            print(f"  Errors: {len(self.errors)}")
            for name, msgs in self.errors:
                print(f"    - {name}: {', '.join(msgs)}")
        if self.dry_run:
            print("\n  (DRY RUN - no files modified)")
        print("=" * 60)

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Auto-fix File-Level Docstring for solution files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--range", nargs=2, metavar=("START", "END"), type=int,
                        help="Fix files in numeric range")
    parser.add_argument("--file", type=str, help="Fix a specific file")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only")
    parser.add_argument("--fetch-online", action="store_true", default=True,
                        help="Fetch Problem/Link/Description/Constraints from LeetCode (default: True)")
    parser.add_argument("--no-fetch", action="store_true", help="Disable online fetching")
    parser.add_argument("--delay-min", type=float, default=1.0,
                        help="Minimum delay in seconds between requests (default: 1.0)")
    parser.add_argument("--delay-max", type=float, default=3.0,
                        help="Maximum delay in seconds between requests (default: 3.0)")
    
    args = parser.parse_args()
    fetch_online = args.fetch_online and not args.no_fetch
    
    # Validate delay parameters
    if args.delay_min < 0 or args.delay_max < 0:
        print("Error: Delay values must be non-negative")
        return 1
    if args.delay_min > args.delay_max:
        print("Error: delay-min must be <= delay-max")
        return 1
    
    fixer = DocstringFixer(
        dry_run=args.dry_run, 
        fetch_online=fetch_online,
        delay_min=args.delay_min,
        delay_max=args.delay_max
    )
    
    if args.file:
        fixer.fix_single_file(args.file, replace_mode=False)
    elif args.range:
        start, end = args.range
        print(f"\nProcessing {start:04d} ~ {end:04d} (replace mode + online fetch)\n")
        fixer.fix_range(start, end, replace_mode=True)
    else:
        # Interactive mode: prompt for range
        print("\n" + "=" * 60)
        print("File-Level Docstring Auto-Fix Tool")
        print("=" * 60)
        print("\nPlease enter the range of files to fix:")
        
        while True:
            try:
                min_num = int(input("Min (inclusive): ").strip())
                break
            except ValueError:
                print("Invalid number.")
        
        while True:
            try:
                max_num = int(input("Max (inclusive): ").strip())
                if max_num >= min_num:
                    break
                print(f"Max must be >= {min_num}")
            except ValueError:
                print("Invalid number.")
        
        print(f"\nProcessing {min_num:04d} ~ {max_num:04d} (replace mode + online fetch)\n")
        fixer.fix_range(min_num, max_num, replace_mode=True)
    
    fixer.print_summary()
    return 0 if not fixer.errors else 1


if __name__ == "__main__":
    sys.exit(main())
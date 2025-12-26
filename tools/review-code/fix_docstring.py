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
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Tuple, List, Dict

# Project root directory
ROOT = Path(__file__).parent.parent.parent
SOLUTIONS_DIR = ROOT / "solutions"
TOOLS_DIR = ROOT / "tools"
CACHE_FILE = TOOLS_DIR / ".cache" / "leetcode_problems.json"


class LeetCodeDataFetcher:
    """Fetch LeetCode problem data from cache or API."""
    
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
    
    def get_problem_info(self, problem_id: str) -> Optional[Dict[str, str]]:
        """Get problem info from cache by ID (e.g., '0077')."""
        if not self.cache:
            return None
        
        def normalize_url(url: str, slug: str) -> str:
            """Normalize URL to remove /description/ suffix if present."""
            if not url:
                return f"https://leetcode.com/problems/{slug}/"
            # Remove /description/ suffix if present
            url = url.rstrip('/')
            if url.endswith('/description'):
                url = url[:-11]  # Remove '/description'
            # Ensure ends with single /
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
    
    def fetch_constraints_from_web(self, slug: str) -> List[str]:
        """Fetch constraints from LeetCode problem page (basic attempt)."""
        # Note: This is a simplified version. Full implementation would require
        # parsing HTML or using GraphQL API which requires authentication.
        # For now, return empty list and let user fill manually.
        return []


class DocstringFixer:
    """Fix docstrings to comply with review-code.md format."""
    
    def __init__(self, dry_run: bool = False, fetch_online: bool = False):
        self.dry_run = dry_run
        self.fetch_online = fetch_online
        self.fixed_count = 0
        self.skipped_count = 0
        self.errors = []
        self.leetcode_fetcher = LeetCodeDataFetcher() if fetch_online else None
    
    def extract_problem_id_from_filename(self, filename: str) -> Optional[str]:
        """Extract problem ID from filename (e.g., '0077_combinations.py' -> '0077')."""
        match = re.match(r'^(\d{4})_', filename)
        if match:
            return match.group(1)
        return None
    
    def extract_docstring(self, content: str) -> Optional[Tuple[int, int, str]]:
        """Extract docstring from file content.
        
        Returns:
            Tuple of (start_pos, end_pos, docstring_content) or None
        """
        # Find first docstring (triple quotes)
        match = re.search(r'^"""', content, re.MULTILINE)
        if not match:
            return None
        
        start_pos = match.start()
        
        # Find closing triple quotes
        # Look for """ that's not part of opening
        remaining = content[start_pos + 3:]
        end_match = re.search(r'"""', remaining)
        if not end_match:
            return None
        
        end_pos = start_pos + 3 + end_match.end()
        docstring = content[start_pos + 3:end_pos - 3]
        
        return (start_pos, end_pos, docstring)
    
    def parse_docstring(self, docstring: str) -> Dict[str, any]:
        """Parse docstring into structured fields."""
        result = {
            "problem": None,
            "link": None,
            "description": [],
            "optional_fields": {},  # Sub-Pattern, Key Insight, etc.
            "constraints": [],
            "has_decorative_separators": False,
            "raw_lines": docstring.split('\n')
        }
        
        lines = docstring.split('\n')
        current_section = None
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Check for decorative separators
            if re.match(r'^={3,}$', stripped) or re.match(r'^-{3,}$', stripped):
                result["has_decorative_separators"] = True
                i += 1
                continue
            
            # Problem field
            if re.match(r'^Problem:\s*(.+)$', line, re.IGNORECASE):
                match = re.match(r'^Problem:\s*(.+)$', line, re.IGNORECASE)
                result["problem"] = match.group(1).strip()
                i += 1
                continue
            
            # Link field
            if re.match(r'^Link:\s*(.+)$', line, re.IGNORECASE):
                match = re.match(r'^Link:\s*(.+)$', line, re.IGNORECASE)
                result["link"] = match.group(1).strip()
                i += 1
                continue
            
            # Optional extension fields
            optional_field_match = re.match(r'^(Sub-Pattern|Key Insight|API Kernel|Pattern|Family|Delta from .+?):\s*(.+)$', line, re.IGNORECASE)
            if optional_field_match:
                field_name = optional_field_match.group(1)
                field_value = optional_field_match.group(2).strip()
                # Collect multi-line values
                value_lines = [field_value]
                i += 1
                while i < len(lines) and lines[i].strip() and not re.match(r'^(Problem|Link|Constraints?|Sub-Pattern|Key Insight|API Kernel|Pattern|Family|Delta from):', lines[i], re.IGNORECASE):
                    if not re.match(r'^-', lines[i].strip()):  # Not a constraint bullet
                        value_lines.append(lines[i].strip())
                    else:
                        break
                    i += 1
                result["optional_fields"][field_name] = '\n'.join(value_lines)
                continue
            
            # Constraints section
            if re.match(r'^Constraints?:?\s*$', line, re.IGNORECASE):
                current_section = "constraints"
                i += 1
                continue
            
            # Collect constraint bullets
            if current_section == "constraints" and re.match(r'^-\s*(.+)$', stripped):
                result["constraints"].append(stripped)
                i += 1
                continue
            
            # Description (content between Link and optional fields/Constraints)
            if result["link"] and not current_section and stripped:
                # Skip if it's an optional field we already handled
                if not re.match(r'^(Sub-Pattern|Key Insight|API Kernel|Pattern|Family|Constraints?|Delta from):', line, re.IGNORECASE):
                    result["description"].append(line.rstrip())
            
            i += 1
        
        # Clean up description
        result["description"] = [line for line in result["description"] if line.strip()]
        
        return result
    
    def build_docstring(self, parsed: Dict, replace_mode: bool = False) -> str:
        """Build properly formatted docstring from parsed fields.
        
        Args:
            parsed: Parsed docstring fields
            replace_mode: If True, completely replace with generated content (ignore existing optional fields)
        """
        parts = []
        
        # Problem (required)
        problem_text = parsed["problem"] or "[MISSING - NEEDS MANUAL FIX]"
        parts.append(f"Problem: {problem_text}")
        
        # Link (required)
        link_text = parsed["link"] or "[MISSING - NEEDS MANUAL FIX]"
        parts.append(f"Link: {link_text}")
        
        # Empty line
        parts.append("")
        
        # Description - preserve if it exists (in both modes)
        if parsed["description"]:
            parts.extend(parsed["description"])
            parts.append("")
        
        # Optional extension fields (before Constraints) - only in non-replace mode
        if not replace_mode:
            for field_name, field_value in parsed["optional_fields"].items():
                if field_value:
                    # Handle multi-line values
                    value_lines = field_value.split('\n')
                    parts.append(f"{field_name}: {value_lines[0]}")
                    for line in value_lines[1:]:
                        if line.strip():
                            parts.append(line)
        
        # Constraints
        if parsed["constraints"]:
            parts.append("Constraints:")
            for constraint in parsed["constraints"]:
                parts.append(constraint)
        else:
            # Add placeholder if missing
            parts.append("Constraints:")
            parts.append("- [MISSING - NEEDS MANUAL FIX]")
        
        return '\n'.join(parts)
    
    def fix_file(self, file_path: Path, replace_mode: bool = False) -> Tuple[bool, List[str]]:
        """Fix docstring in a single file.
        
        Args:
            file_path: Path to the solution file
            replace_mode: If True, completely replace docstring with generated content
        
        Returns:
            Tuple of (success, list of issues/warnings)
        """
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return False, [f"Failed to read file: {e}"]
        
        # Extract docstring
        docstring_info = self.extract_docstring(content)
        if not docstring_info:
            return False, ["No docstring found"]
        
        start_pos, end_pos, old_docstring = docstring_info
        
        # Parse docstring
        parsed = self.parse_docstring(old_docstring)
        
        # In replace mode, always fetch from LeetCode if available
        if replace_mode or (self.fetch_online and self.leetcode_fetcher):
            problem_id = self.extract_problem_id_from_filename(file_path.name)
            if problem_id and self.leetcode_fetcher:
                leetcode_info = self.leetcode_fetcher.get_problem_info(problem_id)
                if leetcode_info:
                    # Always replace Problem and Link in replace mode
                    if replace_mode or not parsed["problem"]:
                        parsed["problem"] = leetcode_info.get('title', '')
                        if replace_mode:
                            issues.append("Replaced Problem from LeetCode cache")
                        else:
                            issues.append("Filled Problem from LeetCode cache")
                    
                    if replace_mode or not parsed["link"]:
                        parsed["link"] = leetcode_info.get('url', '')
                        if parsed["link"]:
                            if replace_mode:
                                issues.append("Replaced Link from LeetCode cache")
                            else:
                                issues.append("Filled Link from LeetCode cache")
        
        # In replace mode, always rebuild
        if replace_mode:
            new_docstring = self.build_docstring(parsed, replace_mode=True)
            fix_reasons = ["Complete replacement"] + issues
        else:
            # Check if fixes are needed
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
            
            # Build new docstring
            new_docstring = self.build_docstring(parsed, replace_mode=False)
        
        # Reconstruct file content
        new_content = (
            content[:start_pos] +
            '"""\n' +
            new_docstring +
            '\n"""' +
            content[end_pos:]
        )
        
        # Write file if not dry run
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
        """Fix files in a numeric range.
        
        Args:
            start_num: Start number (inclusive)
            end_num: End number (inclusive)
            replace_mode: If True, completely replace docstrings
        """
        pattern = re.compile(r'^(\d{4})_')
        
        for file_path in sorted(SOLUTIONS_DIR.glob("*.py")):
            match = pattern.match(file_path.name)
            if not match:
                continue
            
            file_num = int(match.group(1))
            if start_num <= file_num <= end_num:
                success, issues = self.fix_file(file_path, replace_mode=replace_mode)
                if success:
                    if issues and issues[0] != "No fixes needed":
                        print(f"[OK] {file_path.name}: {', '.join(issues)}")
                    else:
                        self.skipped_count += 1
                else:
                    print(f"[ERROR] {file_path.name}: {', '.join(issues)}")
                    self.errors.append((file_path.name, issues))
    
    def fix_single_file(self, filename: str, replace_mode: bool = False) -> None:
        """Fix a single file by name.
        
        Args:
            filename: Name of the file to fix
            replace_mode: If True, completely replace docstring
        """
        file_path = SOLUTIONS_DIR / filename
        if not file_path.exists():
            print(f"Error: File not found: {filename}")
            return
        
        success, issues = self.fix_file(file_path, replace_mode=replace_mode)
        if success:
            if issues and issues[0] != "No fixes needed":
                print(f"[OK] {file_path.name}: {', '.join(issues)}")
            else:
                print(f"[OK] {file_path.name}: No fixes needed")
        else:
            print(f"[ERROR] {file_path.name}: {', '.join(issues)}")
    
    def fix_all(self) -> None:
        """Fix all solution files."""
        for file_path in sorted(SOLUTIONS_DIR.glob("*.py")):
            success, issues = self.fix_file(file_path)
            if success:
                if issues and issues[0] != "No fixes needed":
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
        print(f"  Skipped (no changes needed): {self.skipped_count}")
        if self.errors:
            print(f"  Errors: {len(self.errors)}")
            for filename, issues in self.errors:
                print(f"    - {filename}: {', '.join(issues)}")
        if self.dry_run:
            print("\n  (DRY RUN - no files were actually modified)")
        print("=" * 60)


def prompt_for_range() -> Tuple[int, int]:
    """Prompt user to input min and max range."""
    print("\n" + "=" * 60)
    print("File-Level Docstring Auto-Fix Tool")
    print("=" * 60)
    print("\nPlease enter the range of files to fix:")
    
    while True:
        try:
            min_input = input("Min (inclusive): ").strip()
            min_num = int(min_input)
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    while True:
        try:
            max_input = input("Max (inclusive): ").strip()
            max_num = int(max_input)
            if max_num < min_num:
                print(f"Max must be >= Min ({min_num}). Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return min_num, max_num


def main():
    parser = argparse.ArgumentParser(
        description="Auto-fix File-Level Docstring for solution files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--range",
        nargs=2,
        metavar=("START", "END"),
        type=int,
        help="Fix files in numeric range (e.g., --range 77 142)"
    )
    
    parser.add_argument(
        "--file",
        type=str,
        help="Fix a specific file (e.g., --file 0077_combinations.py)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files"
    )
    
    parser.add_argument(
        "--fetch-online",
        action="store_true",
        default=True,  # Default to True for automatic fetching
        help="Fetch Problem and Link from LeetCode API cache (default: True)"
    )
    
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Disable online fetching (opposite of --fetch-online)"
    )
    
    args = parser.parse_args()
    
    # Handle --no-fetch flag
    fetch_online = args.fetch_online and not args.no_fetch
    
    fixer = DocstringFixer(dry_run=args.dry_run, fetch_online=fetch_online)
    
    # If no arguments provided, prompt for range
    if not args.file and not args.range:
        if args.dry_run:
            print("Note: Running in dry-run mode. No files will be modified.")
        min_num, max_num = prompt_for_range()
        print(f"\nProcessing files from {min_num:04d} to {max_num:04d}...")
        print("(All File-Level Docstrings will be completely replaced with generated content)\n")
        fixer.fix_range(min_num, max_num, replace_mode=True)
    elif args.file:
        fixer.fix_single_file(args.file)
    elif args.range:
        start, end = args.range
        print(f"Processing files from {start:04d} to {end:04d}...")
        print("(All File-Level Docstrings will be completely replaced with generated content)\n")
        fixer.fix_range(start, end, replace_mode=True)
    else:
        fixer.fix_all()
    
    fixer.print_summary()
    
    return 0 if not fixer.errors else 1


if __name__ == "__main__":
    sys.exit(main())


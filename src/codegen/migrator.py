"""
Test Format Migrator - Migrate existing tests to canonical JSON literal format.

This module converts existing test files (.in/.out) from various formats
to the canonical JSON literal format.

Canonical Format:
- Input: Each line is a JSON/Python literal (e.g., [1,2,3], 9, "abc")
- Output: Single-line JSON literal
- Boolean: true/false (JSON style, lowercase)
- Arrays: [0,1,2] (no spaces after commas)
- Strings: "abc" (double quotes)

Usage:
    python -m codegen.migrator 0001_two_sum      # Migrate single problem
    python -m codegen.migrator --all             # Migrate all problems
    python -m codegen.migrator --all --dry-run   # Preview changes
"""

import sys
import re
import json
import shutil
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from enum import Enum

# Setup paths
_PROJECT_ROOT = Path(__file__).parent.parent.parent
_TOOLS_PATH = _PROJECT_ROOT / "tools" / "leetcode-api"
_CODEGEN_PATH = _PROJECT_ROOT / "packages" / "codegen"

if str(_TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(_TOOLS_PATH))
if str(_CODEGEN_PATH) not in sys.path:
    sys.path.insert(0, str(_CODEGEN_PATH))


class FormatType(Enum):
    """Detected format type of a test file."""
    CANONICAL = "canonical"           # Already in JSON literal format
    SPACE_SEPARATED = "space_sep"     # Space-separated values
    COMMA_SEPARATED = "comma_sep"     # Comma-separated (no brackets)
    MIXED = "mixed"                   # Mixed format
    UNKNOWN = "unknown"


@dataclass
class MigrationResult:
    """Result of migrating a single test file."""
    file_path: Path
    original_format: FormatType = FormatType.UNKNOWN
    migrated: bool = False
    original_content: str = ""
    new_content: str = ""
    error: str = ""
    
    def __repr__(self) -> str:
        status = "OK" if self.migrated else ("SKIP" if not self.error else "ERROR")
        return f"MigrationResult({self.file_path.name}: {status})"


@dataclass  
class ProblemMigration:
    """Result of migrating all test files for a problem."""
    problem_id: str
    results: List[MigrationResult] = field(default_factory=list)
    total_files: int = 0
    migrated_count: int = 0
    skipped_count: int = 0
    error_count: int = 0
    
    def summary(self) -> str:
        return f"{self.problem_id}: {self.migrated_count} migrated, {self.skipped_count} skipped, {self.error_count} errors"


def detect_format(content: str) -> FormatType:
    """
    Detect the format type of test file content.
    
    Args:
        content: File content
        
    Returns:
        FormatType enum
    """
    lines = content.strip().split('\n')
    if not lines:
        return FormatType.UNKNOWN
    
    has_brackets = False
    has_space_sep = False
    has_comma_only = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for JSON literal (starts with [ or {)
        if line.startswith('[') or line.startswith('{'):
            has_brackets = True
        # Check for space-separated numbers
        elif re.match(r'^-?\d+(\s+-?\d+)+$', line):
            has_space_sep = True
        # Check for comma-separated without brackets
        elif re.match(r'^-?\d+(,-?\d+)+$', line):
            has_comma_only = True
    
    if has_brackets and not has_space_sep:
        return FormatType.CANONICAL
    elif has_space_sep and not has_brackets:
        return FormatType.SPACE_SEPARATED
    elif has_comma_only:
        return FormatType.COMMA_SEPARATED
    elif has_brackets and has_space_sep:
        return FormatType.MIXED
    
    # Check if it's a simple value (number, string, boolean)
    if len(lines) == 1:
        line = lines[0].strip()
        if re.match(r'^-?\d+\.?\d*$', line):  # Number
            return FormatType.CANONICAL
        if line.lower() in ('true', 'false'):  # Boolean
            return FormatType.CANONICAL
        if line.startswith('"') or line.startswith("'"):  # Quoted string
            return FormatType.CANONICAL
    
    return FormatType.UNKNOWN


def convert_line_to_canonical(line: str, is_output: bool = False) -> str:
    """
    Convert a single line to canonical format.
    
    Args:
        line: Input line
        is_output: Whether this is an output line
        
    Returns:
        Canonical format string
    """
    line = line.strip()
    if not line:
        return line
    
    # Already a JSON literal?
    if line.startswith('[') or line.startswith('{'):
        # Normalize: remove spaces after commas, use double quotes
        try:
            # Try to parse and re-serialize
            parsed = json.loads(line.replace("'", '"'))
            return json.dumps(parsed, separators=(',', ':'))
        except json.JSONDecodeError:
            # Try Python literal
            import ast
            try:
                parsed = ast.literal_eval(line)
                return json.dumps(parsed, separators=(',', ':'))
            except (ValueError, SyntaxError):
                # Can't parse, return as-is but normalize quotes
                return line.replace("'", '"')
    
    # Boolean?
    if line.lower() == 'true':
        return 'true'
    if line.lower() == 'false':
        return 'false'
    
    # Number?
    if re.match(r'^-?\d+\.?\d*$', line):
        return line
    
    # Space-separated numbers?
    if re.match(r'^-?\d+(\s+-?\d+)+$', line):
        parts = line.split()
        try:
            nums = [int(p) for p in parts]
            return json.dumps(nums, separators=(',', ':'))
        except ValueError:
            try:
                nums = [float(p) for p in parts]
                return json.dumps(nums, separators=(',', ':'))
            except ValueError:
                pass
    
    # Space-separated strings/chars?
    if ' ' in line and not line.startswith('"'):
        parts = line.split()
        # Check if all parts are single chars
        if all(len(p) == 1 for p in parts):
            return json.dumps(parts, separators=(',', ':'))
    
    # Comma-separated without brackets?
    if ',' in line and not line.startswith('['):
        parts = [p.strip() for p in line.split(',')]
        try:
            nums = [int(p) for p in parts]
            return json.dumps(nums, separators=(',', ':'))
        except ValueError:
            try:
                nums = [float(p) for p in parts]
                return json.dumps(nums, separators=(',', ':'))
            except ValueError:
                # String array
                return json.dumps(parts, separators=(',', ':'))
    
    # Plain string (no quotes)
    if not (line.startswith('"') or line.startswith("'")):
        # Don't add quotes for simple strings that look like identifiers
        # These are likely meant to be raw strings
        return line
    
    return line


def convert_to_canonical(content: str, is_output: bool = False) -> str:
    """
    Convert test file content to canonical format.
    
    Args:
        content: Original file content
        is_output: Whether this is an output file
        
    Returns:
        Canonical format content
    """
    lines = content.strip().split('\n')
    converted_lines = []
    
    for line in lines:
        converted = convert_line_to_canonical(line, is_output)
        converted_lines.append(converted)
    
    return '\n'.join(converted_lines)


def migrate_file(file_path: Path, dry_run: bool = False, backup: bool = True) -> MigrationResult:
    """
    Migrate a single test file to canonical format.
    
    Args:
        file_path: Path to the test file
        dry_run: If True, don't write changes
        backup: If True, create backup before modifying
        
    Returns:
        MigrationResult with details
    """
    result = MigrationResult(file_path=file_path, migrated=False)
    
    if not file_path.exists():
        result.error = "File not found"
        return result
    
    try:
        original = file_path.read_text(encoding='utf-8')
        result.original_content = original
    except Exception as e:
        result.error = f"Read error: {e}"
        return result
    
    # Detect format
    result.original_format = detect_format(original)
    
    # Already canonical?
    if result.original_format == FormatType.CANONICAL:
        result.new_content = original
        return result  # migrated=False means no change needed
    
    # Convert
    is_output = file_path.suffix == '.out'
    try:
        converted = convert_to_canonical(original, is_output)
        result.new_content = converted
    except Exception as e:
        result.error = f"Conversion error: {e}"
        return result
    
    # No change?
    if converted.strip() == original.strip():
        return result
    
    # Write if not dry run
    if not dry_run:
        try:
            # Backup
            if backup:
                backup_path = file_path.with_suffix(file_path.suffix + '.bak')
                shutil.copy2(file_path, backup_path)
            
            # Write new content
            file_path.write_text(converted + '\n', encoding='utf-8')
            result.migrated = True
        except Exception as e:
            result.error = f"Write error: {e}"
            return result
    else:
        result.migrated = True  # Would have migrated
    
    return result


def migrate_problem(problem_id: str, tests_dir: Optional[Path] = None,
                    dry_run: bool = False, backup: bool = True) -> ProblemMigration:
    """
    Migrate all test files for a problem.
    
    Args:
        problem_id: Problem ID (e.g., "0001_two_sum")
        tests_dir: Tests directory path
        dry_run: If True, don't write changes
        backup: If True, create backups
        
    Returns:
        ProblemMigration with results
    """
    tests_dir = tests_dir or (_PROJECT_ROOT / "tests")
    result = ProblemMigration(problem_id=problem_id)
    
    # Find all test files for this problem
    test_files = sorted(tests_dir.glob(f"{problem_id}_*.in")) + \
                 sorted(tests_dir.glob(f"{problem_id}_*.out"))
    
    result.total_files = len(test_files)
    
    for test_file in test_files:
        file_result = migrate_file(test_file, dry_run=dry_run, backup=backup)
        result.results.append(file_result)
        
        if file_result.error:
            result.error_count += 1
        elif file_result.migrated:
            result.migrated_count += 1
        else:
            result.skipped_count += 1
    
    return result


def migrate_all(tests_dir: Optional[Path] = None, solutions_dir: Optional[Path] = None,
                dry_run: bool = False, backup: bool = True,
                limit: Optional[int] = None) -> List[ProblemMigration]:
    """
    Migrate all test files.
    
    Args:
        tests_dir: Tests directory path
        solutions_dir: Solutions directory path (to get problem list)
        dry_run: If True, don't write changes
        backup: If True, create backups
        limit: Maximum number of problems to process
        
    Returns:
        List of ProblemMigration results
    """
    tests_dir = tests_dir or (_PROJECT_ROOT / "tests")
    solutions_dir = solutions_dir or (_PROJECT_ROOT / "solutions")
    
    results = []
    
    # Get unique problem IDs from solution files
    problem_ids = set()
    for solution_file in solutions_dir.glob("*.py"):
        if not solution_file.name.startswith("_"):
            problem_ids.add(solution_file.stem)
    
    count = 0
    for problem_id in sorted(problem_ids):
        print(f"Processing {problem_id}...", end=" ", flush=True)
        
        result = migrate_problem(problem_id, tests_dir, dry_run, backup)
        results.append(result)
        
        print(f"[{result.migrated_count}/{result.total_files}]")
        
        count += 1
        if limit and count >= limit:
            break
    
    return results


def generate_report(results: List[ProblemMigration]) -> str:
    """Generate a summary report."""
    lines = []
    lines.append("=" * 60)
    lines.append("MIGRATION REPORT")
    lines.append("=" * 60)
    
    total_files = sum(r.total_files for r in results)
    total_migrated = sum(r.migrated_count for r in results)
    total_skipped = sum(r.skipped_count for r in results)
    total_errors = sum(r.error_count for r in results)
    
    lines.append(f"Problems processed: {len(results)}")
    lines.append(f"Total files: {total_files}")
    lines.append(f"  Migrated: {total_migrated}")
    lines.append(f"  Skipped (already canonical): {total_skipped}")
    lines.append(f"  Errors: {total_errors}")
    lines.append("")
    
    # Show problems with migrations
    lines.append("Problems with changes:")
    for r in results:
        if r.migrated_count > 0:
            lines.append(f"  {r.summary()}")
    
    # Show errors
    if total_errors > 0:
        lines.append("")
        lines.append("Errors:")
        for r in results:
            for fr in r.results:
                if fr.error:
                    lines.append(f"  {fr.file_path.name}: {fr.error}")
    
    return "\n".join(lines)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Migrate test files to canonical JSON literal format"
    )
    parser.add_argument(
        "problem_id",
        nargs="?",
        default=None,
        help="Problem ID to migrate (e.g., 0001_two_sum)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="migrate_all",
        help="Migrate all problems"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup files"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of problems (with --all)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("DRY RUN - No files will be modified\n")
    
    backup = not args.no_backup
    
    if args.migrate_all:
        results = migrate_all(
            dry_run=args.dry_run,
            backup=backup,
            limit=args.limit
        )
        print()
        print(generate_report(results))
        
    elif args.problem_id:
        result = migrate_problem(
            args.problem_id,
            dry_run=args.dry_run,
            backup=backup
        )
        print(result.summary())
        
        if args.verbose:
            for fr in result.results:
                status = "MIGRATED" if fr.migrated else ("ERROR" if fr.error else "SKIP")
                print(f"  {fr.file_path.name}: {status} ({fr.original_format.value})")
                if fr.migrated and args.verbose:
                    print(f"    Before: {fr.original_content[:50]}...")
                    print(f"    After:  {fr.new_content[:50]}...")
    else:
        print("Error: Specify a problem_id or use --all")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()


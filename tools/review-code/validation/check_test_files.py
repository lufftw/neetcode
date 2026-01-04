#!/usr/bin/env python3
"""
Check and fix double newline ending errors in test files under tests/ directory.

Checks all .in and .out files to find files ending with two newlines (\n\n).

Features:
1. List problematic files
2. Fix these files (remove extra newline)

Exit Codes:
- 0: All files OK or fix successful
- 1: Errors found but not fixed

Usage:
    python tools/review-code/validation/check_test_files.py              # List problematic files
    python tools/review-code/validation/check_test_files.py --fix        # List and fix
    python tools/review-code/validation/check_test_files.py --verbose    # Show detailed info
"""
import sys
from pathlib import Path
from typing import List


PROJECT_ROOT = Path(__file__).parent.parent
TESTS_DIR = PROJECT_ROOT / "tests"


def check_file(file_path: Path) -> bool:
    """
    Check if file ends with two newlines.
    
    Returns:
        True if file ends with \n\n (problematic)
        False if file is OK
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            # Check if ends with \n\n
            return data.endswith(b'\n\n')
    except Exception as e:
        print(f"Error: Cannot read file {file_path}: {e}", file=sys.stderr)
        return False


def fix_file(file_path: Path) -> bool:
    """
    Fix file: remove extra newline at end, keep only one.
    
    Returns:
        True if fix successful
        False if fix failed
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # If ends with \n\n, remove one \n
        if data.endswith(b'\n\n'):
            # Remove last \n
            fixed_data = data[:-1]
            
            with open(file_path, 'wb') as f:
                f.write(fixed_data)
            return True
        return False
    except Exception as e:
        print(f"Error: Cannot fix file {file_path}: {e}", file=sys.stderr)
        return False


def find_test_files() -> List[Path]:
    """Find all .in and .out test files."""
    if not TESTS_DIR.exists():
        print(f"Error: tests directory does not exist: {TESTS_DIR}", file=sys.stderr)
        return []
    
    test_files = []
    for ext in ['.in', '.out']:
        test_files.extend(TESTS_DIR.glob(f'*{ext}'))
    
    return sorted(test_files)


def main():
    """Main function."""
    # Parse arguments
    fix_mode = '--fix' in sys.argv or '-f' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    # Find all test files
    test_files = find_test_files()
    
    if not test_files:
        print("No test files found.")
        return 0
    
    if verbose:
        print(f"Checking {len(test_files)} test files...")
    
    # Check files
    problematic_files = []
    for file_path in test_files:
        if check_file(file_path):
            problematic_files.append(file_path)
    
    # Show results
    if not problematic_files:
        print("✓ All test files are OK (no double newline endings).")
        return 0
    
    print(f"\nFound {len(problematic_files)} files ending with two newlines:\n")
    for file_path in problematic_files:
        rel_path = file_path.relative_to(PROJECT_ROOT)
        print(f"  {rel_path}")
    
    # Fix mode
    if fix_mode:
        print(f"\nFixing {len(problematic_files)} files...")
        fixed_count = 0
        failed_count = 0
        
        for file_path in problematic_files:
            if fix_file(file_path):
                fixed_count += 1
                if verbose:
                    rel_path = file_path.relative_to(PROJECT_ROOT)
                    print(f"  ✓ Fixed: {rel_path}")
            else:
                failed_count += 1
                rel_path = file_path.relative_to(PROJECT_ROOT)
                print(f"  ✗ Fix failed: {rel_path}", file=sys.stderr)
        
        print(f"\nFix complete: {fixed_count} succeeded, {failed_count} failed")
        return 0 if failed_count == 0 else 1
    else:
        print("\nTip: Use --fix to automatically fix these issues.")
        return 1


if __name__ == '__main__':
    sys.exit(main())


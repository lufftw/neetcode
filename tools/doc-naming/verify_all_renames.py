#!/usr/bin/env python3
"""
Verify that all old filename references have been replaced.

For each renamed file, checks if any old filename references remain in the repository.
All checks should return "No old references found".
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


def load_mapping() -> Dict[str, str]:
    """Load the rename mapping from JSON file."""
    mapping_file = Path("rename_mapping.json")
    if not mapping_file.exists():
        print(f"ERROR: {mapping_file} not found.")
        print("Run rename_docs_to_kebab_case.py first to generate the mapping.")
        return {}
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_old_references(old_path: str) -> Tuple[bool, List[str]]:
    """
    Check if old filename references still exist in the repository.
    
    Returns:
        (is_clean, files_with_references)
        - is_clean: True if no references found, False otherwise
        - files_with_references: List of files containing the old reference
    """
    old_name = Path(old_path).name
    
    try:
        # Use git grep to find files containing the old filename
        result = subprocess.run(
            ['git', 'grep', '-l', old_name],
            capture_output=True,
            text=True,
            check=False  # Don't raise on non-zero exit
        )
        
        if result.returncode == 0 and result.stdout.strip():
            # Found references
            files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
            # Exclude mapping files (they are supposed to contain old filenames)
            excluded_files = {'rename_mapping.json', 'rename_mapping.txt'}
            files = [f for f in files if f not in excluded_files]
            if files:
                return (False, files)
            else:
                # Only found in mapping files, which is expected
                return (True, [])
        else:
            # No references found (exit code 1 means no matches)
            return (True, [])
    
    except Exception as e:
        print(f"  WARNING: Error checking '{old_name}': {e}")
        return (False, [f"Error: {e}"])


def main():
    """Main entry point."""
    print("=" * 70)
    print("Verifying All Renamed Files - Old References Check")
    print("=" * 70)
    print()
    
    mapping = load_mapping()
    if not mapping:
        return 1
    
    print(f"Checking {len(mapping)} renamed files...")
    print()
    
    all_clean = True
    issues: List[Tuple[str, List[str]]] = []
    
    # Sort by old path for consistent output
    for old_path in sorted(mapping.keys()):
        old_name = Path(old_path).name
        new_path = mapping[old_path]
        new_name = Path(new_path).name
        
        is_clean, files_with_refs = check_old_references(old_path)
        
        if is_clean:
            print(f"OK {old_name:50s} -> No old references found")
        else:
            all_clean = False
            print(f"FAIL {old_name:50s} -> Found {len(files_with_refs)} file(s) with old references:")
            for file in files_with_refs:
                print(f"    - {file}")
            issues.append((old_name, files_with_refs))
        print()
    
    # Summary
    print("=" * 70)
    if all_clean:
        print("SUCCESS: All renamed files have no old references remaining!")
        print("=" * 70)
        return 0
    else:
        print(f"FAILED: Found old references in {len(issues)} renamed file(s)")
        print("=" * 70)
        print("\nFiles that still contain old references:")
        for old_name, files in issues:
            print(f"\n  {old_name}:")
            for file in files:
                print(f"    - {file}")
        print("\nPlease update these references manually or run fix_remaining_references.py")
        return 1


if __name__ == '__main__':
    exit(main())


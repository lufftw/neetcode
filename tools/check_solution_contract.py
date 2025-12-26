#!/usr/bin/env python3
"""
Check solution files against solution-contract.md specification

Validation items (based on solution-contract.md lines 197-222):
- Problem: (Required) Problem title
- Link: (Required) LeetCode URL
- Description: (Recommended) Brief problem statement
- Constraints: (Recommended) Key constraints affecting algorithm choice
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

# Project root directory
ROOT = Path(__file__).parent.parent
SOLUTIONS_DIR = ROOT / "solutions"


def extract_docstring_fields(file_path: Path) -> Dict[str, str]:
    """Extract docstring fields from file"""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {"error": str(e)}
    
    # Find first docstring (triple quotes)
    docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
    if not docstring_match:
        return {"error": "No docstring found"}
    
    docstring = docstring_match.group(1)
    
    # Extract fields
    fields = {}
    
    # Problem: field
    problem_match = re.search(r'^Problem:\s*(.+?)$', docstring, re.MULTILINE)
    if problem_match:
        fields["Problem"] = problem_match.group(1).strip()
    
    # Link: field
    link_match = re.search(r'^Link:\s*(.+?)$', docstring, re.MULTILINE)
    if link_match:
        fields["Link"] = link_match.group(1).strip()
    
    # Description (may not be explicitly marked, check for descriptive text)
    # If there's content after Problem and Link, it might be Description
    lines = docstring.split('\n')
    description_lines = []
    found_problem = False
    found_link = False
    
    for line in lines:
        if re.match(r'^Problem:\s*', line):
            found_problem = True
            continue
        if re.match(r'^Link:\s*', line):
            found_link = True
            continue
        if found_problem and found_link:
            stripped = line.strip()
            if stripped and not re.match(r'^Constraints?:', stripped, re.IGNORECASE):
                description_lines.append(stripped)
            elif re.match(r'^Constraints?:', stripped, re.IGNORECASE):
                break
    
    if description_lines:
        fields["Description"] = ' '.join(description_lines)
    
    # Constraints field
    constraints_match = re.search(r'^Constraints?:?\s*\n((?:- .+?\n?)+)', docstring, re.MULTILINE | re.IGNORECASE)
    if constraints_match:
        fields["Constraints"] = constraints_match.group(1).strip()
    
    return fields


def check_solution_file(file_path: Path) -> Tuple[bool, List[str]]:
    """Check if a single solution file conforms to the contract"""
    issues = []
    fields = extract_docstring_fields(file_path)
    
    if "error" in fields:
        issues.append(f"Failed to read file: {fields['error']}")
        return False, issues
    
    # Check required fields
    if "Problem" not in fields:
        issues.append("Missing required field: Problem")
    elif not fields["Problem"]:
        issues.append("Problem field is empty")
    
    if "Link" not in fields:
        issues.append("Missing required field: Link")
    elif not fields["Link"]:
        issues.append("Link field is empty")
    elif not fields["Link"].startswith("http"):
        issues.append(f"Link format may be incorrect: {fields['Link']}")
    
    # Check recommended fields (warnings only, not treated as errors)
    recommendations = []
    if "Description" not in fields or not fields["Description"]:
        recommendations.append("Consider adding Description")
    
    if "Constraints" not in fields or not fields["Constraints"]:
        recommendations.append("Consider adding Constraints")
    
    if recommendations:
        issues.append(f"Recommended fields: {', '.join(recommendations)}")
    
    is_valid = len([i for i in issues if not i.startswith("Recommended fields")]) == 0
    return is_valid, issues


def main():
    """Main function"""
    if not SOLUTIONS_DIR.exists():
        print(f"Error: Solutions directory not found: {SOLUTIONS_DIR}", file=sys.stderr)
        sys.exit(1)
    
    # Get all .py files (exclude _runner.py and __pycache__)
    solution_files = sorted([
        f for f in SOLUTIONS_DIR.glob("*.py")
        if f.name != "_runner.py" and not f.name.startswith("__")
    ])
    
    if not solution_files:
        print("No solution files found", file=sys.stderr)
        sys.exit(1)
    
    print(f"Checking {len(solution_files)} solution files...\n")
    
    invalid_files = []
    valid_count = 0
    
    for file_path in solution_files:
        is_valid, issues = check_solution_file(file_path)
        file_name = file_path.name
        
        if not is_valid:
            invalid_files.append((file_name, issues))
        else:
            valid_count += 1
    
    # Output results
    if invalid_files:
        print("=" * 80)
        print(f"Found {len(invalid_files)} files that do not conform to the contract:\n")
        
        for file_name, issues in invalid_files:
            print(f"[X] {file_name}")
            for issue in issues:
                if issue.startswith("Recommended fields"):
                    print(f"   [W] {issue}")
                else:
                    print(f"   - {issue}")
            print()
        
        print("=" * 80)
        print(f"\nSummary:")
        print(f"  [OK] Conforming: {valid_count}")
        print(f"  [X] Non-conforming: {len(invalid_files)}")
        print(f"  [Total] {len(solution_files)}")
        
        sys.exit(1)
    else:
        print("=" * 80)
        print(f"[OK] All {len(solution_files)} files conform to the contract!")
        print("=" * 80)
        sys.exit(0)


if __name__ == "__main__":
    main()


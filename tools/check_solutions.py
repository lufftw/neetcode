#!/usr/bin/env python3
"""
Check solution files for compliance with Pure Polymorphic Architecture.

Validates:
- SOLUTIONS dictionary structure (exists, has 'class' field)
- Architecture compliance (no wrapper functions, uses get_solver)
- Code format (Solution comment format, complexity comments)
"""
import re
from pathlib import Path
from typing import List, Dict, Tuple

PROJECT_ROOT = Path(__file__).parent.parent
SOLUTIONS_DIR = PROJECT_ROOT / "solutions"


class SolutionChecker:
    """Check solution files for architecture compliance."""
    
    def __init__(self):
        self.issues: List[Dict] = []
    
    def check_file(self, filepath: Path) -> Dict:
        """Check a single solution file."""
        if filepath.name == '_runner.py':
            return {'file': filepath.name, 'issues': [], 'status': 'ok'}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        issues = []
        
        # Architecture checks
        arch_issues = self._check_architecture(content)
        issues.extend(arch_issues)
        
        # Format checks
        format_issues = self._check_format(lines)
        issues.extend(format_issues)
        
        # Complexity checks
        complexity_issues = self._check_complexity(lines)
        issues.extend(complexity_issues)
        
        return {
            'file': filepath.name,
            'issues': issues,
            'status': 'ok' if not issues else 'error'
        }
    
    def _check_architecture(self, content: str) -> List[Dict]:
        """Check architecture compliance."""
        issues = []
        
        # Check SOLUTIONS dictionary exists
        if 'SOLUTIONS' not in content:
            return [{'type': 'missing_solutions', 'message': 'Missing SOLUTIONS dictionary'}]
        
        # Check SOLUTIONS contains 'class' field
        solutions_match = re.search(r'SOLUTIONS\s*=\s*\{', content)
        if solutions_match:
            solutions_section = content[solutions_match.start():]
            if '"class":' not in solutions_section and "'class':" not in solutions_section:
                issues.append({
                    'type': 'missing_class_field',
                    'message': 'SOLUTIONS missing "class" field'
                })
        
        # Check for wrapper functions
        wrapper_functions = re.findall(r'def\s+(solve_\w+)\s*\(', content)
        if wrapper_functions:
            issues.append({
                'type': 'has_wrapper_functions',
                'message': f'Wrapper functions found: {", ".join(wrapper_functions)}'
            })
        
        # Check solve() uses get_solver()
        if 'get_solver' not in content:
            issues.append({
                'type': 'not_using_get_solver',
                'message': 'solve() not using get_solver()'
            })
        
        # Check import
        if 'from _runner import get_solver' not in content:
            issues.append({
                'type': 'missing_import',
                'message': 'Missing import: from _runner import get_solver'
            })
        
        return issues
    
    def _check_format(self, lines: List[str]) -> List[Dict]:
        """Check Solution comment format."""
        issues = []
        for i, line in enumerate(lines, 1):
            if re.match(r'^#\s*Solution:\s', line) or re.match(r'^#\s*Solution\s+-\s+', line):
                issues.append({
                    'type': 'wrong_solution_format',
                    'line': i,
                    'message': f'Line {i}: Should use "Solution 1:" format'
                })
        return issues
    
    def _check_complexity(self, lines: List[str]) -> List[Dict]:
        """Check Time/Space complexity comments."""
        issues = []
        for i in range(len(lines)):
            line = lines[i]
            if re.match(r'^#\s*Solution\s+\d*:?\s', line):
                has_time = False
                has_space = False
                
                # Look ahead up to 15 lines for complexity comments
                for j in range(i + 1, min(i + 16, len(lines))):
                    next_line = lines[j]
                    if re.match(r'^#\s*Solution', next_line) or re.match(r'^class\s+Solution', next_line):
                        break
                    
                    if re.search(r'Time:\s*O\(', next_line, re.IGNORECASE):
                        has_time = True
                    if re.search(r'Space:\s*O\(', next_line, re.IGNORECASE):
                        has_space = True
                
                if not has_time or not has_space:
                    if not has_time and not has_space:
                        issues.append({
                            'type': 'missing_complexity',
                            'line': i + 1,
                            'message': f'Line {i+1}: Missing Time and Space complexity'
                        })
                    elif not has_time:
                        issues.append({
                            'type': 'missing_complexity',
                            'line': i + 1,
                            'message': f'Line {i+1}: Missing Time complexity'
                        })
                    elif not has_space:
                        issues.append({
                            'type': 'missing_complexity',
                            'line': i + 1,
                            'message': f'Line {i+1}: Missing Space complexity'
                        })
        
        return issues
    
    def check_all(self) -> List[Dict]:
        """Check all solution files."""
        results = []
        for filepath in sorted(SOLUTIONS_DIR.glob('*.py')):
            result = self.check_file(filepath)
            results.append(result)
            if result['status'] == 'error':
                self.issues.append(result)
        return results
    
    def print_report(self, results: List[Dict]) -> int:
        """Print check report and return error count."""
        total = len(results)
        ok_count = sum(1 for r in results if r['status'] == 'ok')
        error_count = total - ok_count
        
        print("=" * 80)
        print("Solution Files Check Report")
        print("=" * 80)
        print(f"Total files: {total}")
        print(f"✓ OK: {ok_count}")
        print(f"✗ Errors: {error_count}")
        print()
        
        if error_count > 0:
            architecture_issues, format_issues, complexity_issues = self._group_issues(results)
            
            if architecture_issues:
                self._print_issue_group("1. Architecture Issues:", architecture_issues)
            
            if format_issues:
                self._print_issue_group("2. Format Issues:", format_issues)
            
            if complexity_issues:
                self._print_issue_group("3. Missing Complexity Comments:", complexity_issues)
        
        print()
        print("=" * 80)
        return error_count
    
    def _group_issues(self, results: List[Dict]) -> Tuple[List, List, List]:
        """Group issues by type."""
        architecture_issues = []
        format_issues = []
        complexity_issues = []
        
        arch_types = ['missing_solutions', 'missing_class_field', 'has_wrapper_functions', 
                     'not_using_get_solver', 'missing_import']
        
        for result in results:
            if result['status'] == 'error':
                for issue in result['issues']:
                    if issue['type'] in arch_types:
                        architecture_issues.append((result['file'], issue))
                    elif issue['type'] == 'wrong_solution_format':
                        format_issues.append((result['file'], issue))
                    elif issue['type'] == 'missing_complexity':
                        complexity_issues.append((result['file'], issue))
        
        return architecture_issues, format_issues, complexity_issues
    
    def _print_issue_group(self, title: str, issues: List[Tuple[str, Dict]]):
        """Print a group of issues."""
        print(title)
        print("-" * 80)
        current_file = None
        for filename, issue in issues:
            if filename != current_file:
                print(f"\n📄 {filename}")
                current_file = filename
            print(f"  ❌ {issue['message']}")


def main():
    """Main entry point."""
    checker = SolutionChecker()
    results = checker.check_all()
    error_count = checker.print_report(results)
    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    exit(main())


#!/usr/bin/env python3
"""
Check solution files for compliance with Pure Polymorphic Architecture.

Validates:
- SOLUTIONS dictionary structure (exists, has 'class' field)
- Architecture compliance (no wrapper functions, uses get_solver)
- Code format (Solution comment format, complexity comments)

Exit Codes:
- 0: All checks passed
- 1: Errors found

Usage:
    python tools/check_solutions.py
    python tools/check_solutions.py --verbose
    python tools/check_solutions.py --list-warnings  # List files with warnings only
    python tools/check_solutions.py --show-warnings  # Show warnings with suggestions
    python tools/check_solutions.py --fix  # Auto-fix simple issues (future)
"""
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


PROJECT_ROOT = Path(__file__).parent.parent
SOLUTIONS_DIR = PROJECT_ROOT / "solutions"


@dataclass
class FormatIssue:
    """Represents a format issue found in a solution file."""
    file: str
    line: int
    issue_type: str
    message: str
    severity: str = "error"  # error, warning
    suggestion: Optional[str] = None


@dataclass
class FileCheckResult:
    """Result of checking a single file."""
    file: str
    issues: List[FormatIssue] = field(default_factory=list)
    
    @property
    def status(self) -> str:
        errors = [i for i in self.issues if i.severity == "error"]
        return "error" if errors else "ok"
    
    @property
    def error_count(self) -> int:
        return len([i for i in self.issues if i.severity == "error"])
    
    @property
    def warning_count(self) -> int:
        return len([i for i in self.issues if i.severity == "warning"])


class SolutionChecker:
    """Check solution files for architecture and format compliance."""
    
    # Issue types grouped by category
    ARCHITECTURE_ISSUES = {
        'missing_solutions',
        'missing_class_field', 
        'has_wrapper_functions',
        'not_using_get_solver',
        'missing_import',
    }
    
    FORMAT_ISSUES = {
        'wrong_solution_format',
        'missing_solution_comment',
    }
    
    COMPLEXITY_ISSUES = {
        'missing_time_complexity',
        'missing_space_complexity',
        'missing_complexity',
    }
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.all_issues: List[FormatIssue] = []
    
    def check_file(self, filepath: Path) -> FileCheckResult:
        """Check a single solution file."""
        if filepath.name == '_runner.py':
            return FileCheckResult(file=filepath.name)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        result = FileCheckResult(file=filepath.name)
        
        # Architecture checks
        result.issues.extend(self._check_architecture(filepath.name, content))
        
        # Format checks
        result.issues.extend(self._check_format(filepath.name, lines))
        
        # Complexity checks
        result.issues.extend(self._check_complexity(filepath.name, lines))
        
        # Solution comment placement checks
        result.issues.extend(self._check_solution_comment_placement(filepath.name, lines))
        
        return result
    
    def _check_architecture(self, filename: str, content: str) -> List[FormatIssue]:
        """Check architecture compliance."""
        issues = []
        
        # Check SOLUTIONS dictionary exists
        if 'SOLUTIONS' not in content:
            issues.append(FormatIssue(
                file=filename,
                line=0,
                issue_type='missing_solutions',
                message='Missing SOLUTIONS dictionary',
                suggestion='Add SOLUTIONS = { "default": { "class": "Solution", ... } }'
            ))
            return issues
        
        # Check SOLUTIONS contains 'class' field
        solutions_match = re.search(r'SOLUTIONS\s*=\s*\{', content)
        if solutions_match:
            solutions_section = content[solutions_match.start():]
            if '"class":' not in solutions_section and "'class':" not in solutions_section:
                issues.append(FormatIssue(
                    file=filename,
                    line=self._find_line_number(content, 'SOLUTIONS'),
                    issue_type='missing_class_field',
                    message='SOLUTIONS missing "class" field',
                    suggestion='Add "class": "SolutionClassName" to each solution entry'
                ))
        
        # Check for wrapper functions (solve_* pattern)
        wrapper_functions = re.findall(r'def\s+(solve_\w+)\s*\(', content)
        if wrapper_functions:
            issues.append(FormatIssue(
                file=filename,
                line=self._find_line_number(content, f'def {wrapper_functions[0]}'),
                issue_type='has_wrapper_functions',
                message=f'Wrapper functions found: {", ".join(wrapper_functions)}',
                suggestion='Remove wrapper functions and use polymorphic SOLUTIONS pattern'
            ))
        
        # Check solve() uses get_solver()
        if 'get_solver' not in content:
            issues.append(FormatIssue(
                file=filename,
                line=self._find_line_number(content, 'def solve'),
                issue_type='not_using_get_solver',
                message='solve() not using get_solver()',
                suggestion='Use: solver = get_solver(SOLUTIONS)'
            ))
        
        # Check import
        if 'from _runner import get_solver' not in content:
            issues.append(FormatIssue(
                file=filename,
                line=1,
                issue_type='missing_import',
                message='Missing import: from _runner import get_solver',
                suggestion='Add: from _runner import get_solver'
            ))
        
        return issues
    
    def _check_format(self, filename: str, lines: List[str]) -> List[FormatIssue]:
        """Check Solution comment format."""
        issues = []
        for i, line in enumerate(lines, 1):
            # Check for wrong format: "Solution:" or "Solution -"
            if re.match(r'^#\s*Solution:\s', line):
                issues.append(FormatIssue(
                    file=filename,
                    line=i,
                    issue_type='wrong_solution_format',
                    message=f'Line {i}: Use "Solution 1:" format (not "Solution:")',
                    suggestion='Change to: # Solution 1: Description'
                ))
            elif re.match(r'^#\s*Solution\s+-\s+', line):
                issues.append(FormatIssue(
                    file=filename,
                    line=i,
                    issue_type='wrong_solution_format',
                    message=f'Line {i}: Use "Solution 1:" format (not "Solution -")',
                    suggestion='Change to: # Solution 1: Description'
                ))
        return issues
    
    def _check_complexity(self, filename: str, lines: List[str]) -> List[FormatIssue]:
        """Check Time/Space complexity comments."""
        issues = []
        for i in range(len(lines)):
            line = lines[i]
            # Match "# Solution 1:" or "# Solution 2:" etc.
            if re.match(r'^#\s*Solution\s+\d+:?\s', line):
                has_time = False
                has_space = False
                
                # Look ahead up to 15 lines for complexity comments
                for j in range(i + 1, min(i + 16, len(lines))):
                    next_line = lines[j]
                    # Stop if we hit another Solution comment or class definition
                    if re.match(r'^#\s*Solution', next_line) or re.match(r'^class\s+Solution', next_line):
                        break
                    
                    if re.search(r'Time:\s*O\(', next_line, re.IGNORECASE):
                        has_time = True
                    if re.search(r'Space:\s*O\(', next_line, re.IGNORECASE):
                        has_space = True
                
                if not has_time and not has_space:
                    issues.append(FormatIssue(
                        file=filename,
                        line=i + 1,
                        issue_type='missing_complexity',
                        message=f'Line {i+1}: Missing Time and Space complexity',
                        suggestion='Add: # Time: O(...), Space: O(...)'
                    ))
                elif not has_time:
                    issues.append(FormatIssue(
                        file=filename,
                        line=i + 1,
                        issue_type='missing_time_complexity',
                        message=f'Line {i+1}: Missing Time complexity',
                        suggestion='Add: # Time: O(...)'
                    ))
                elif not has_space:
                    issues.append(FormatIssue(
                        file=filename,
                        line=i + 1,
                        issue_type='missing_space_complexity',
                        message=f'Line {i+1}: Missing Space complexity',
                        suggestion='Add: # Space: O(...)'
                    ))
        
        return issues
    
    def _check_solution_comment_placement(self, filename: str, lines: List[str]) -> List[FormatIssue]:
        """Check that Solution comments are BEFORE class definitions, not inside."""
        issues = []
        
        # Find all class definitions that look like solution classes
        class_pattern = re.compile(r'^class\s+(Solution\w*)\s*[:\(]')
        solution_comment_pattern = re.compile(r'^#\s*Solution\s+\d+:')
        
        for i, line in enumerate(lines):
            match = class_pattern.match(line)
            if match:
                class_name = match.group(1)
                class_line = i + 1
                
                # Look backwards for a Solution comment
                # Strategy: Two-phase search
                # Phase 1: Look in immediate vicinity (20 lines)
                # Phase 2: If not found, check further (up to 50 lines) but only
                #          if intermediate lines are comments/blanks
                has_comment_before = False
                comment_line = None
                
                # Phase 1: Immediate vicinity (first 20 lines)
                for j in range(i - 1, max(-1, i - 20), -1):
                    if solution_comment_pattern.match(lines[j]):
                        has_comment_before = True
                        comment_line = j
                        break
                    # Stop if we hit another class or function definition
                    if re.match(r'^(class|def)\s+', lines[j]):
                        break
                
                # Phase 2: Extended search (lines 20-50) if not found in phase 1
                if not has_comment_before:
                    for j in range(i - 20, max(-1, i - 50), -1):
                        if solution_comment_pattern.match(lines[j]):
                            # Verify all lines between comment and class are comments/blanks
                            all_comments_or_blanks = True
                            for k in range(j + 1, i):
                                line_content = lines[k].strip()
                                # Allow: blank lines, comment lines (starting with #), or separator lines
                                if line_content and not line_content.startswith('#'):
                                    all_comments_or_blanks = False
                                    break
                            
                            if all_comments_or_blanks:
                                has_comment_before = True
                                comment_line = j
                                break
                        
                        # Stop if we hit another class or function definition
                        if re.match(r'^(class|def)\s+', lines[j]):
                            break
                
                # Check if comment is inside the class (wrong placement)
                has_comment_inside = False
                for j in range(i + 1, min(len(lines), i + 10)):
                    if re.match(r'^\s+#\s*Solution\s+\d+:', lines[j]):
                        has_comment_inside = True
                        break
                    if re.match(r'^class\s+', lines[j]):
                        break
                
                if has_comment_inside and not has_comment_before:
                    issues.append(FormatIssue(
                        file=filename,
                        line=class_line,
                        issue_type='missing_solution_comment',
                        message=f'Line {class_line}: Class {class_name} has Solution comment inside class instead of before',
                        suggestion='Move "# Solution N:" comment to BEFORE the class definition'
                    ))
                elif not has_comment_before and class_name != 'ListNode' and 'Helper' not in class_name:
                    # Only warn for Solution-like classes, not helper classes
                    if 'Solution' in class_name:
                        issues.append(FormatIssue(
                            file=filename,
                            line=class_line,
                            issue_type='missing_solution_comment',
                            message=f'Line {class_line}: Class {class_name} missing Solution comment before definition',
                            suggestion='Add "# Solution N: Description" comment before class',
                            severity='warning'
                        ))
        
        return issues
    
    def _find_line_number(self, content: str, pattern: str) -> int:
        """Find line number of a pattern in content."""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if pattern in line:
                return i
        return 0
    
    def check_all(self) -> List[FileCheckResult]:
        """Check all solution files."""
        results = []
        for filepath in sorted(SOLUTIONS_DIR.glob('*.py')):
            result = self.check_file(filepath)
            results.append(result)
            self.all_issues.extend(result.issues)
        return results
    
    def print_report(self, results: List[FileCheckResult]) -> Tuple[int, int]:
        """Print check report and return (error_count, warning_count)."""
        total = len(results)
        ok_count = sum(1 for r in results if r.status == 'ok')
        error_count = sum(r.error_count for r in results)
        warning_count = sum(r.warning_count for r in results)
        
        print("=" * 80)
        print("Solution Files Check Report")
        print("=" * 80)
        print(f"Total files: {total}")
        print(f"✓ OK: {ok_count}")
        print(f"✗ Errors: {error_count}")
        print(f"⚠ Warnings: {warning_count}")
        print()
        
        if error_count > 0 or (warning_count > 0 and self.verbose):
            # Group issues by category
            arch_issues = []
            format_issues = []
            complexity_issues = []
            
            for result in results:
                for issue in result.issues:
                    if self.verbose or issue.severity == 'error':
                        if issue.issue_type in self.ARCHITECTURE_ISSUES:
                            arch_issues.append(issue)
                        elif issue.issue_type in self.FORMAT_ISSUES:
                            format_issues.append(issue)
                        elif issue.issue_type in self.COMPLEXITY_ISSUES:
                            complexity_issues.append(issue)
            
            if arch_issues:
                self._print_issue_group("1. Architecture Issues", arch_issues)
            
            if format_issues:
                self._print_issue_group("2. Format Issues", format_issues)
            
            if complexity_issues:
                self._print_issue_group("3. Complexity Comment Issues", complexity_issues)
        
        print()
        print("=" * 80)
        
        return error_count, warning_count
    
    def _print_issue_group(self, title: str, issues: List[FormatIssue]):
        """Print a group of issues."""
        print(f"\n{title}")
        print("-" * 80)
        
        current_file = None
        for issue in issues:
            if issue.file != current_file:
                print(f"\n📄 {issue.file}")
                current_file = issue.file
            
            severity_icon = "❌" if issue.severity == "error" else "⚠️"
            print(f"  {severity_icon} {issue.message}")
            if self.verbose and issue.suggestion:
                print(f"     💡 Suggestion: {issue.suggestion}")


def main():
    """Main entry point."""
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    list_warnings = '--list-warnings' in sys.argv
    show_warnings = '--show-warnings' in sys.argv
    
    checker = SolutionChecker(verbose=verbose)
    results = checker.check_all()
    
    if list_warnings:
        # Just list files with warnings (filename only)
        warning_files = [r.file for r in results if r.warning_count > 0]
        for filename in sorted(warning_files):
            print(filename)
        return 0
    
    if show_warnings:
        # Show warnings with detailed information and suggestions
        warning_results = [r for r in results if r.warning_count > 0]
        if not warning_results:
            print("No warnings found.")
            return 0
        
        print("Files with warnings:")
        print("=" * 80)
        for result in sorted(warning_results, key=lambda x: x.file):
            print(f"\n📄 {result.file}")
            print("-" * 80)
            for issue in result.issues:
                if issue.severity == 'warning':
                    print(f"  ⚠️  Line {issue.line}: {issue.message}")
                    if issue.suggestion:
                        print(f"     💡 Suggestion: {issue.suggestion}")
        print("\n" + "=" * 80)
        return 0
    
    error_count, warning_count = checker.print_report(results)
    
    # Exit with error only if there are errors (not warnings)
    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

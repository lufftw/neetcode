#!/usr/bin/env python3
"""
Unit tests for solution file format checking.

This module tests ONLY solution file format compliance:
- Solution comment format (must use "Solution 1:" format)
- Time/Space complexity comments presence
- SOLUTIONS dictionary structure (exists, has 'class' field)
- Architecture compliance (no wrapper functions, uses get_solver)
- Solution comment placement (before class, not inside)

Note: This is separate from:
- Runner component tests (.dev/tests/)
- Solution correctness tests (.dev/tests_solutions/)
"""
import unittest
import re
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).parent.parent.parent
SOLUTIONS_DIR = PROJECT_ROOT / "solutions"


class TestSolutionFormat(unittest.TestCase):
    """Test solution file format compliance."""
    
    @classmethod
    def setUpClass(cls):
        """Get all solution files once."""
        cls.solution_files = [f for f in SOLUTIONS_DIR.glob('*.py') 
                              if f.name != '_runner.py']
    
    def test_solution_comment_format(self):
        """
        Test that Solution comments use 'Solution 1:' format.
        
        Invalid formats:
        - "# Solution: Description"  (missing number)
        - "# Solution - Description" (wrong separator)
        
        Valid format:
        - "# Solution 1: Description"
        - "# Solution 2: Alternative approach"
        """
        errors = []
        for filepath in self.solution_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                if re.match(r'^#\s*Solution:\s', line):
                    errors.append(f"{filepath.name}:{i} - Use 'Solution 1:' format (not 'Solution:')")
                elif re.match(r'^#\s*Solution\s+-\s+', line):
                    errors.append(f"{filepath.name}:{i} - Use 'Solution 1:' format (not 'Solution -')")
        
        self.assertEqual(len(errors), 0, 
                        f"Found {len(errors)} format errors:\n" + "\n".join(errors))
    
    def test_complexity_comments(self):
        """
        Test that Solution classes have Time and Space complexity comments.
        
        Each "# Solution N:" block should have:
        - "# Time: O(...)" within 15 lines
        - "# Space: O(...)" within 15 lines
        """
        errors = []
        for filepath in self.solution_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i in range(len(lines)):
                line = lines[i]
                if re.match(r'^#\s*Solution\s+\d+:?\s', line):
                    has_time = False
                    has_space = False
                    
                    # Check next 15 lines for complexity comments
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
                            errors.append(f"{filepath.name}:{i+1} - Missing Time and Space")
                        elif not has_time:
                            errors.append(f"{filepath.name}:{i+1} - Missing Time")
                        elif not has_space:
                            errors.append(f"{filepath.name}:{i+1} - Missing Space")
        
        self.assertEqual(len(errors), 0,
                        f"Found {len(errors)} missing complexity comments:\n" + "\n".join(errors))
    
    def test_solutions_dictionary_exists(self):
        """
        Test that SOLUTIONS dictionary exists in each solution file.
        
        Required for Pure Polymorphic Architecture.
        """
        errors = []
        for filepath in self.solution_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'SOLUTIONS' not in content:
                errors.append(f"{filepath.name} - Missing SOLUTIONS dictionary")
        
        self.assertEqual(len(errors), 0,
                        f"Found {len(errors)} files missing SOLUTIONS:\n" + "\n".join(errors))
    
    def test_solutions_dictionary_structure(self):
        """
        Test that SOLUTIONS dictionary has required fields.
        
        Required structure:
        SOLUTIONS = {
            "default": {
                "class": "ClassName",  # Required
                "method": "methodName",
                ...
            }
        }
        """
        errors = []
        for filepath in self.solution_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'SOLUTIONS' not in content:
                continue  # Already tested in test_solutions_dictionary_exists
            
            solutions_match = re.search(r'SOLUTIONS\s*=\s*\{', content)
            if solutions_match:
                solutions_section = content[solutions_match.start():]
                if '"class":' not in solutions_section and "'class':" not in solutions_section:
                    errors.append(f"{filepath.name} - SOLUTIONS missing 'class' field")
        
        self.assertEqual(len(errors), 0,
                        f"Found {len(errors)} SOLUTIONS structure errors:\n" + "\n".join(errors))
    
    def test_no_wrapper_functions(self):
        """
        Test that no wrapper functions exist.
        
        Wrapper functions (solve_*, solve_two_sum, etc.) are deprecated.
        Use polymorphic SOLUTIONS pattern instead.
        """
        errors = []
        for filepath in self.solution_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            wrapper_functions = re.findall(r'def\s+(solve_\w+)\s*\(', content)
            if wrapper_functions:
                errors.append(f"{filepath.name} - Wrapper functions: {', '.join(wrapper_functions)}")
        
        self.assertEqual(len(errors), 0,
                        f"Found {len(errors)} files with wrapper functions:\n" + "\n".join(errors))
    
    def test_uses_get_solver(self):
        """
        Test that solve() functions use get_solver().
        
        Required pattern:
            from _runner import get_solver
            
            def solve():
                solver = get_solver(SOLUTIONS)
                result = solver.method(...)
        """
        errors = []
        for filepath in self.solution_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'SOLUTIONS' in content:
                if 'get_solver' not in content:
                    errors.append(f"{filepath.name} - Not using get_solver()")
                elif 'from _runner import get_solver' not in content:
                    errors.append(f"{filepath.name} - Missing import: from _runner import get_solver")
        
        self.assertEqual(len(errors), 0,
                        f"Found {len(errors)} files not using get_solver:\n" + "\n".join(errors))
    
    def test_solution_comment_before_class(self):
        """
        Test that Solution comments are BEFORE class definitions.
        
        Correct:
            # Solution 1: Hash Map
            # Time: O(n), Space: O(n)
            class Solution:
                ...
        
        Incorrect:
            class Solution:
                # Solution 1: Hash Map  <-- Inside class!
                ...
        """
        errors = []
        warnings = []
        
        for filepath in self.solution_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            class_pattern = re.compile(r'^class\s+(Solution\w*)\s*[:\(]')
            solution_comment_pattern = re.compile(r'^#\s*Solution\s+\d+:')
            
            for i, line in enumerate(lines):
                match = class_pattern.match(line)
                if match:
                    class_name = match.group(1)
                    
                    # Skip helper classes
                    if class_name == 'ListNode' or 'Helper' in class_name:
                        continue
                    
                    # Look backwards for a Solution comment
                    has_comment_before = False
                    for j in range(i - 1, max(-1, i - 20), -1):
                        if solution_comment_pattern.match(lines[j]):
                            has_comment_before = True
                            break
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
                        errors.append(
                            f"{filepath.name}:{i+1} - {class_name} has Solution comment inside class"
                        )
                    elif not has_comment_before and 'Solution' in class_name:
                        warnings.append(
                            f"{filepath.name}:{i+1} - {class_name} missing Solution comment before definition"
                        )
        
        # Errors are failures, warnings are just noted
        self.assertEqual(len(errors), 0,
                        f"Found {len(errors)} misplaced Solution comments:\n" + "\n".join(errors))
    
    def test_all_solution_classes_have_comments(self):
        """
        Test that all Solution* classes have corresponding Solution comments.
        
        Each class like SolutionTwoPointers, SolutionFloyd, etc. should have
        a "# Solution N:" comment before it.
        """
        warnings = []
        
        for filepath in self.solution_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            class_pattern = re.compile(r'^class\s+(Solution\w*)\s*[:\(]')
            solution_comment_pattern = re.compile(r'^#\s*Solution\s+\d+:')
            
            solution_classes = []
            for i, line in enumerate(lines):
                match = class_pattern.match(line)
                if match:
                    class_name = match.group(1)
                    # Skip base Solution class if it's the only one
                    if class_name != 'ListNode' and 'Helper' not in class_name:
                        solution_classes.append((i, class_name))
            
            # Count Solution comments
            solution_comments = 0
            for line in lines:
                if solution_comment_pattern.match(line):
                    solution_comments += 1
            
            # If we have multiple solution classes, we should have matching comments
            if len(solution_classes) > 1:
                if solution_comments < len(solution_classes):
                    warnings.append(
                        f"{filepath.name} - Has {len(solution_classes)} Solution classes but only {solution_comments} Solution comments"
                    )
        
        # This is informational, not a hard failure
        if warnings:
            print(f"\nNote: {len(warnings)} files may need more Solution comments:")
            for w in warnings[:5]:  # Show first 5
                print(f"  {w}")
            if len(warnings) > 5:
                print(f"  ... and {len(warnings) - 5} more")


class TestSolutionFormatHelpers(unittest.TestCase):
    """Test helper functions for format checking."""
    
    def test_solution_comment_regex(self):
        """Test regex patterns for Solution comments."""
        valid_patterns = [
            "# Solution 1: Two Pointers",
            "# Solution 2: Hash Map Approach",
            "# Solution 1: Description",
            "#   Solution 1: With spaces",
        ]
        
        invalid_patterns = [
            "# Solution: Missing number",
            "# Solution - Wrong separator",
            "## Solution 1: Wrong prefix",
            "# solution 1: lowercase",  # Could be valid but unusual
        ]
        
        pattern = re.compile(r'^#\s*Solution\s+\d+:')
        
        for p in valid_patterns:
            self.assertIsNotNone(pattern.match(p), f"Should match: {p}")
    
    def test_complexity_regex(self):
        """Test regex patterns for complexity comments."""
        valid_time = [
            "# Time: O(n)",
            "# Time: O(n log n)",
            "# Time: O(n²)",
            "#   Time: O(1)",
        ]
        
        valid_space = [
            "# Space: O(n)",
            "# Space: O(1)",
            "#   Space: O(n)",
        ]
        
        time_pattern = re.compile(r'Time:\s*O\(', re.IGNORECASE)
        space_pattern = re.compile(r'Space:\s*O\(', re.IGNORECASE)
        
        for p in valid_time:
            self.assertIsNotNone(time_pattern.search(p), f"Should match time: {p}")
        
        for p in valid_space:
            self.assertIsNotNone(space_pattern.search(p), f"Should match space: {p}")


if __name__ == '__main__':
    unittest.main()

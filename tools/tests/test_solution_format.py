#!/usr/bin/env python3
"""
Unit tests for solution file format checking.

Validates:
- Solution comment format (must use "Solution 1:" format)
- Time/Space complexity comments presence
- SOLUTIONS dictionary structure (exists, has 'class' field)
- Architecture compliance (no wrapper functions, uses get_solver)
"""
import unittest
import re
from pathlib import Path

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
        """Test that Solution comments use 'Solution 1:' format."""
        errors = []
        for filepath in self.solution_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                if re.match(r'^#\s*Solution:\s', line):
                    errors.append(f"{filepath.name}:{i} - Use 'Solution 1:' format")
                elif re.match(r'^#\s*Solution\s+-\s+', line):
                    errors.append(f"{filepath.name}:{i} - Use 'Solution 1:' format")
        
        self.assertEqual(len(errors), 0, 
                        f"Found {len(errors)} format errors:\n" + "\n".join(errors))
    
    def test_complexity_comments(self):
        """Test that Solution classes have Time and Space complexity."""
        errors = []
        for filepath in self.solution_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i in range(len(lines)):
                line = lines[i]
                if re.match(r'^#\s*Solution\s+\d*:?\s', line):
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
    
    def test_solutions_dictionary_structure(self):
        """Test that SOLUTIONS dictionary has required fields."""
        errors = []
        for filepath in self.solution_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'SOLUTIONS' not in content:
                errors.append(f"{filepath.name} - Missing SOLUTIONS dictionary")
                continue
            
            solutions_match = re.search(r'SOLUTIONS\s*=\s*\{', content)
            if solutions_match:
                solutions_section = content[solutions_match.start():]
                if '"class":' not in solutions_section and "'class':" not in solutions_section:
                    errors.append(f"{filepath.name} - SOLUTIONS missing 'class' field")
        
        self.assertEqual(len(errors), 0,
                        f"Found {len(errors)} SOLUTIONS structure errors:\n" + "\n".join(errors))
    
    def test_no_wrapper_functions(self):
        """Test that no wrapper functions exist."""
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
        """Test that solve() functions use get_solver()."""
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


if __name__ == '__main__':
    unittest.main()


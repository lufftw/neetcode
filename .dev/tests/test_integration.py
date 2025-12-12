# tests_unit/test_integration.py
"""
Integration tests for the neetcode runner system.

These tests verify end-to-end workflows to ensure all components
work together correctly.
"""
import pytest
import sys
import os
import subprocess
import tempfile
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from runner import case_runner, test_runner
from runner.util import write_file, read_file


@pytest.mark.integration
class TestCaseRunnerIntegration:
    """Integration tests for case_runner."""
    
    @pytest.fixture
    def simple_problem_setup(self, tmp_path):
        """Create a simple problem setup for testing."""
        # Create directories
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Create a simple solution that echoes input
        solution_code = """#!/usr/bin/env python3
import sys

def solve():
    for line in sys.stdin:
        print(line.strip())

if __name__ == "__main__":
    solve()
"""
        solution_file = solutions_dir / "echo_problem.py"
        write_file(str(solution_file), solution_code)
        
        # Create test cases
        test_cases = [
            ("echo_problem_1.in", "Hello World"),
            ("echo_problem_2.in", "Line 1\\nLine 2\\nLine 3"),
            ("echo_problem_3.in", ""),
        ]
        
        for filename, content in test_cases:
            test_file = tests_dir / filename
            write_file(str(test_file), content)
        
        return {
            'tmp_path': tmp_path,
            'solutions_dir': solutions_dir,
            'tests_dir': tests_dir
        }
    
    def test_run_single_case_successfully(self, simple_problem_setup):
        """Test running a single case end-to-end."""
        env = simple_problem_setup
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            # Run case 1
            solution_path = "solutions/echo_problem.py"
            input_path = "tests/echo_problem_1.in"
            
            result = subprocess.run(
                [sys.executable, solution_path],
                input="Hello World",
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert "Hello World" in result.stdout
        finally:
            os.chdir(original_cwd)
    
    def test_run_multiple_cases(self, simple_problem_setup):
        """Test running multiple cases."""
        env = simple_problem_setup
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            solution_path = "solutions/echo_problem.py"
            
            # Test case 1
            result1 = subprocess.run(
                [sys.executable, solution_path],
                input="Hello World",
                capture_output=True,
                text=True
            )
            assert "Hello World" in result1.stdout
            
            # Test case 2
            result2 = subprocess.run(
                [sys.executable, solution_path],
                input="Line 1\nLine 2\nLine 3",
                capture_output=True,
                text=True
            )
            assert "Line 1" in result2.stdout
            assert "Line 2" in result2.stdout
            assert "Line 3" in result2.stdout
        finally:
            os.chdir(original_cwd)


@pytest.mark.integration
class TestTestRunnerIntegration:
    """Integration tests for test_runner."""
    
    @pytest.fixture
    def two_sum_setup(self, tmp_path):
        """Create a Two Sum problem setup."""
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Create Two Sum solution
        solution_code = """#!/usr/bin/env python3
import sys
import ast

def solve():
    nums = ast.literal_eval(sys.stdin.readline().strip())
    target = int(sys.stdin.readline().strip())
    
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            print([seen[complement], i])
            return
        seen[num] = i
    print([])

if __name__ == "__main__":
    solve()
"""
        solution_file = solutions_dir / "0001_two_sum.py"
        write_file(str(solution_file), solution_code)
        
        # Create test cases
        test_cases = [
            ("0001_two_sum_1.in", "[2, 7, 11, 15]\n9", "0001_two_sum_1.out", "[0, 1]"),
            ("0001_two_sum_2.in", "[3, 2, 4]\n6", "0001_two_sum_2.out", "[1, 2]"),
            ("0001_two_sum_3.in", "[3, 3]\n6", "0001_two_sum_3.out", "[0, 1]"),
        ]
        
        for in_name, in_content, out_name, out_content in test_cases:
            write_file(str(tests_dir / in_name), in_content)
            write_file(str(tests_dir / out_name), out_content)
        
        return {
            'tmp_path': tmp_path,
            'solutions_dir': solutions_dir,
            'tests_dir': tests_dir
        }
    
    def test_run_all_test_cases(self, two_sum_setup):
        """Test running all test cases for a problem."""
        env = two_sum_setup
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            # Get all input files
            import glob
            input_files = sorted(glob.glob("tests/0001_two_sum_*.in"))
            
            assert len(input_files) == 3
            
            passed = 0
            for in_path in input_files:
                out_path = in_path.replace(".in", ".out")
                
                ok, elapsed_ms, actual, expected, validation_mode = test_runner.run_one_case(
                    "0001_two_sum",
                    in_path,
                    out_path,
                    method=None,
                    benchmark=False,
                    compare_mode="exact",
                    module=None
                )
                
                if ok:
                    passed += 1
            
            assert passed == 3
        finally:
            os.chdir(original_cwd)


@pytest.mark.integration
class TestMultiSolutionIntegration:
    """Integration tests for multi-solution problems."""
    
    @pytest.fixture
    def multi_solution_setup(self, tmp_path):
        """Create a problem with multiple solutions."""
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Create solution with multiple methods (polymorphic pattern)
        solution_code = """#!/usr/bin/env python3
import sys
import os

SOLUTIONS = {
    'default': {
        'class': 'SolutionOptimized',
        'method': 'twoSum',
        'complexity': 'O(n)',
        'description': 'Hash table approach'
    },
    'brute_force': {
        'class': 'SolutionBruteForce',
        'method': 'twoSum',
        'complexity': 'O(n²)',
        'description': 'Brute force approach'
    },
    'optimized': {
        'class': 'SolutionOptimized',
        'method': 'twoSum',
        'complexity': 'O(n)',
        'description': 'Hash table approach'
    }
}

class SolutionBruteForce:
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

class SolutionOptimized:
    def twoSum(self, nums, target):
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []

def solve():
    import ast
    nums = ast.literal_eval(sys.stdin.readline().strip())
    target = int(sys.stdin.readline().strip())
    
    method_key = os.environ.get('SOLUTION_METHOD', 'default')
    info = SOLUTIONS.get(method_key, SOLUTIONS['default'])
    
    # Polymorphic invocation
    solver = globals()[info['class']]()
    result = getattr(solver, info['method'])(nums, target)
    
    print(result)

if __name__ == "__main__":
    solve()
"""
        solution_file = solutions_dir / "multi_solution.py"
        write_file(str(solution_file), solution_code)
        
        # Create test case
        write_file(str(tests_dir / "multi_solution_1.in"), "[2, 7, 11, 15]\n9")
        write_file(str(tests_dir / "multi_solution_1.out"), "[0, 1]")
        
        return {
            'tmp_path': tmp_path,
            'solutions_dir': solutions_dir,
            'tests_dir': tests_dir
        }
    
    def test_load_solutions_metadata(self, multi_solution_setup):
        """Test loading SOLUTIONS metadata (polymorphic format)."""
        env = multi_solution_setup
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            module, solutions_meta, compare_mode = test_runner.load_solution_module("multi_solution")
            
            assert module is not None
            assert solutions_meta is not None
            assert 'default' in solutions_meta
            assert 'brute_force' in solutions_meta
            assert 'optimized' in solutions_meta
            # Verify polymorphic format
            assert solutions_meta['brute_force']['class'] == 'SolutionBruteForce'
            assert solutions_meta['brute_force']['method'] == 'twoSum'
            assert solutions_meta['brute_force']['complexity'] == 'O(n²)'
            assert solutions_meta['optimized']['class'] == 'SolutionOptimized'
            assert solutions_meta['optimized']['complexity'] == 'O(n)'
        finally:
            os.chdir(original_cwd)
    
    def test_run_specific_method(self, multi_solution_setup):
        """Test running a specific solution method."""
        env = multi_solution_setup
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            # Test brute_force method
            ok, elapsed_ms, actual, expected, validation_mode = test_runner.run_one_case(
                "multi_solution",
                "tests/multi_solution_1.in",
                "tests/multi_solution_1.out",
                method="brute_force",
                benchmark=False,
                compare_mode="exact",
                module=None
            )
            
            assert ok is True
            assert "[0, 1]" in actual
        finally:
            os.chdir(original_cwd)


@pytest.mark.integration
class TestCompareModesIntegration:
    """Integration tests for different comparison modes."""
    
    @pytest.fixture
    def compare_modes_setup(self, tmp_path):
        """Create problems with different comparison modes."""
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Problem with sorted mode
        sorted_solution = """#!/usr/bin/env python3
import sys

COMPARE_MODE = 'sorted'

def solve():
    n = int(sys.stdin.readline().strip())
    # Return all permutations of [1, 2, ..., n] (simplified)
    result = [[n, n-1], [n-1, n]] if n >= 2 else [[n]]
    print(result)

if __name__ == "__main__":
    solve()
"""
        write_file(str(solutions_dir / "sorted_problem.py"), sorted_solution)
        write_file(str(tests_dir / "sorted_problem_1.in"), "2")
        write_file(str(tests_dir / "sorted_problem_1.out"), "[[1, 2], [2, 1]]")
        
        # Problem with set mode
        set_solution = """#!/usr/bin/env python3
import sys

COMPARE_MODE = 'set'

def solve():
    n = int(sys.stdin.readline().strip())
    # Return subsets (order doesn't matter, duplicates ignored)
    result = [[1], [2], [1], [2]]  # Duplicates
    print(result)

if __name__ == "__main__":
    solve()
"""
        write_file(str(solutions_dir / "set_problem.py"), set_solution)
        write_file(str(tests_dir / "set_problem_1.in"), "2")
        write_file(str(tests_dir / "set_problem_1.out"), "[[1], [2]]")
        
        return {
            'tmp_path': tmp_path,
            'solutions_dir': solutions_dir,
            'tests_dir': tests_dir
        }
    
    def test_sorted_compare_mode(self, compare_modes_setup):
        """Test sorted comparison mode."""
        env = compare_modes_setup
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            module, solutions_meta, compare_mode = test_runner.load_solution_module("sorted_problem")
            assert compare_mode == "sorted"
            
            ok, elapsed_ms, actual, expected, validation_mode = test_runner.run_one_case(
                "sorted_problem",
                "tests/sorted_problem_1.in",
                "tests/sorted_problem_1.out",
                method=None,
                benchmark=False,
                compare_mode=compare_mode,
                module=module
            )
            
            # Should pass with sorted comparison
            assert ok is True
            assert validation_mode == "sorted"
        finally:
            os.chdir(original_cwd)
    
    def test_set_compare_mode(self, compare_modes_setup):
        """Test set comparison mode."""
        env = compare_modes_setup
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            module, solutions_meta, compare_mode = test_runner.load_solution_module("set_problem")
            assert compare_mode == "set"
            
            ok, elapsed_ms, actual, expected, validation_mode = test_runner.run_one_case(
                "set_problem",
                "tests/set_problem_1.in",
                "tests/set_problem_1.out",
                method=None,
                benchmark=False,
                compare_mode=compare_mode,
                module=module
            )
            
            # Should pass with set comparison (duplicates ignored)
            assert ok is True
            assert validation_mode == "set"
        finally:
            os.chdir(original_cwd)


@pytest.mark.integration
class TestJudgeFuncIntegration:
    """Integration tests for JUDGE_FUNC."""
    
    @pytest.fixture
    def judge_func_setup(self, tmp_path):
        """Create a problem with JUDGE_FUNC."""
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Problem with custom judge function
        solution_code = """#!/usr/bin/env python3
import sys

def JUDGE_FUNC(actual, expected, input_data):
    '''Custom judge: check if sum equals target'''
    if not isinstance(actual, list) or len(actual) != 2:
        return False
    
    import ast
    lines = input_data.strip().split('\\n')
    nums = ast.literal_eval(lines[0])
    target = int(lines[1])
    
    i, j = actual[0], actual[1]
    if i < 0 or i >= len(nums) or j < 0 or j >= len(nums):
        return False
    
    return nums[i] + nums[j] == target

def solve():
    import ast
    nums = ast.literal_eval(sys.stdin.readline().strip())
    target = int(sys.stdin.readline().strip())
    
    # Find any valid pair
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                print([i, j])
                return
    print([])

if __name__ == "__main__":
    solve()
"""
        write_file(str(solutions_dir / "judge_problem.py"), solution_code)
        write_file(str(tests_dir / "judge_problem_1.in"), "[2, 7, 11, 15]\n9")
        write_file(str(tests_dir / "judge_problem_1.out"), "[0, 1]")
        
        return {
            'tmp_path': tmp_path,
            'solutions_dir': solutions_dir,
            'tests_dir': tests_dir
        }
    
    def test_judge_func_validation(self, judge_func_setup):
        """Test JUDGE_FUNC validation."""
        env = judge_func_setup
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            module, solutions_meta, compare_mode = test_runner.load_solution_module("judge_problem")
            assert hasattr(module, 'JUDGE_FUNC')
            
            ok, elapsed_ms, actual, expected, validation_mode = test_runner.run_one_case(
                "judge_problem",
                "tests/judge_problem_1.in",
                "tests/judge_problem_1.out",
                method=None,
                benchmark=False,
                compare_mode=compare_mode,
                module=module
            )
            
            assert ok is True
            assert validation_mode == "judge"
        finally:
            os.chdir(original_cwd)
    
    def test_judge_func_without_expected(self, judge_func_setup):
        """Test JUDGE_FUNC without .out file (judge-only mode)."""
        env = judge_func_setup
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            module, solutions_meta, compare_mode = test_runner.load_solution_module("judge_problem")
            
            # Use non-existent .out file
            ok, elapsed_ms, actual, expected, validation_mode = test_runner.run_one_case(
                "judge_problem",
                "tests/judge_problem_1.in",
                "tests/judge_problem_nonexistent.out",
                method=None,
                benchmark=False,
                compare_mode=compare_mode,
                module=module
            )
            
            # Should still validate using JUDGE_FUNC
            assert ok is True
            assert validation_mode == "judge-only"
            assert expected is None
        finally:
            os.chdir(original_cwd)


@pytest.mark.integration
class TestEndToEndWorkflow:
    """End-to-end workflow tests."""
    
    @pytest.fixture
    def complete_setup(self, tmp_path):
        """Create a complete problem setup."""
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        generators_dir = tmp_path / "generators"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        generators_dir.mkdir()
        
        # Create solution
        solution_code = """#!/usr/bin/env python3
import sys

def solve():
    n = int(sys.stdin.readline().strip())
    print(n * 2)

if __name__ == "__main__":
    solve()
"""
        write_file(str(solutions_dir / "complete_problem.py"), solution_code)
        
        # Create test cases
        write_file(str(tests_dir / "complete_problem_1.in"), "5")
        write_file(str(tests_dir / "complete_problem_1.out"), "10")
        write_file(str(tests_dir / "complete_problem_2.in"), "0")
        write_file(str(tests_dir / "complete_problem_2.out"), "0")
        
        return {
            'tmp_path': tmp_path,
            'solutions_dir': solutions_dir,
            'tests_dir': tests_dir,
            'generators_dir': generators_dir
        }
    
    def test_complete_workflow(self, complete_setup):
        """Test complete workflow from loading to validation."""
        env = complete_setup
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            # 1. Load solution module
            module, solutions_meta, compare_mode = test_runner.load_solution_module("complete_problem")
            assert module is not None
            
            # 2. Find test files
            import glob
            input_files = sorted(glob.glob("tests/complete_problem_*.in"))
            assert len(input_files) == 2
            
            # 3. Run all test cases
            passed = 0
            for in_path in input_files:
                out_path = in_path.replace(".in", ".out")
                
                ok, elapsed_ms, actual, expected, validation_mode = test_runner.run_one_case(
                    "complete_problem",
                    in_path,
                    out_path,
                    method=None,
                    benchmark=True,
                    compare_mode=compare_mode,
                    module=module
                )
                
                if ok:
                    passed += 1
                
                # Verify timing was measured
                assert elapsed_ms >= 0
            
            # 4. Verify all passed
            assert passed == 2
        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


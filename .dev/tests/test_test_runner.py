# tests_unit/test_test_runner.py
"""
Characterization tests for runner/test_runner.py

These tests capture the current behavior of the test runner
to ensure refactoring doesn't break existing functionality.
"""
import pytest
import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import importlib.util

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from runner import test_runner


class TestNormalizeOutput:
    """Test normalize_output function."""
    
    def test_basic_normalization(self):
        """Test basic output normalization."""
        assert test_runner.normalize_output("hello\n") == "hello"
        assert test_runner.normalize_output("hello") == "hello"
    
    def test_multiline_normalization(self):
        """Test multiline output normalization."""
        input_str = "line1  \nline2  \n"
        expected = "line1\nline2"
        assert test_runner.normalize_output(input_str) == expected
    
    def test_trailing_whitespace(self):
        """Test trailing whitespace removal."""
        assert test_runner.normalize_output("hello  \n") == "hello"
        assert test_runner.normalize_output("  hello  ") == "hello"


class TestLoadSolutionModule:
    """Test load_solution_module function."""
    
    def test_nonexistent_solution_returns_none(self):
        """Test that nonexistent solution returns None."""
        module, solutions_meta, compare_mode = test_runner.load_solution_module("nonexistent_problem")
        assert module is None
        assert solutions_meta is None
        assert compare_mode == "exact"
    
    def test_default_compare_mode(self, tmp_path):
        """Test that default compare mode is 'exact'."""
        # Create a minimal solution file
        solution_dir = tmp_path / "solutions"
        solution_dir.mkdir()
        solution_file = solution_dir / "test_problem.py"
        solution_file.write_text("def solve(): pass")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            module, solutions_meta, compare_mode = test_runner.load_solution_module("test_problem")
            assert compare_mode == "exact"
        finally:
            os.chdir(original_cwd)
    
    def test_custom_compare_mode(self, tmp_path):
        """Test loading custom COMPARE_MODE."""
        # Create solution with custom COMPARE_MODE
        solution_dir = tmp_path / "solutions"
        solution_dir.mkdir()
        solution_file = solution_dir / "test_problem.py"
        solution_file.write_text("COMPARE_MODE = 'sorted'\ndef solve(): pass")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            module, solutions_meta, compare_mode = test_runner.load_solution_module("test_problem")
            assert compare_mode == "sorted"
        finally:
            os.chdir(original_cwd)
    
    def test_solutions_metadata(self, tmp_path):
        """Test loading SOLUTIONS metadata (polymorphic format)."""
        # Create solution with SOLUTIONS metadata using polymorphic pattern
        solution_dir = tmp_path / "solutions"
        solution_dir.mkdir()
        solution_file = solution_dir / "test_problem.py"
        solution_code = """
SOLUTIONS = {
    'default': {'class': 'Solution', 'method': 'solve', 'complexity': 'O(n)'},
    'optimized': {'class': 'SolutionOptimized', 'method': 'solve', 'complexity': 'O(log n)'}
}

class Solution:
    def solve(self): pass

class SolutionOptimized:
    def solve(self): pass
"""
        solution_file.write_text(solution_code)
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            module, solutions_meta, compare_mode = test_runner.load_solution_module("test_problem")
            assert solutions_meta is not None
            assert 'default' in solutions_meta
            assert 'optimized' in solutions_meta
            assert solutions_meta['default']['class'] == 'Solution'
            assert solutions_meta['optimized']['class'] == 'SolutionOptimized'
        finally:
            os.chdir(original_cwd)


class TestLoadGeneratorModule:
    """Test load_generator_module function."""
    
    def test_nonexistent_generator_returns_none(self):
        """Test that nonexistent generator returns None."""
        module = test_runner.load_generator_module("nonexistent_problem")
        assert module is None
    
    def test_generator_without_generate_function(self, tmp_path):
        """Test that generator without generate() returns None."""
        # Create generator without generate function
        gen_dir = tmp_path / "generators"
        gen_dir.mkdir()
        gen_file = gen_dir / "test_problem.py"
        gen_file.write_text("def other_function(): pass")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            module = test_runner.load_generator_module("test_problem")
            assert module is None
        finally:
            os.chdir(original_cwd)
    
    def test_valid_generator(self, tmp_path):
        """Test loading valid generator."""
        # Create valid generator
        gen_dir = tmp_path / "generators"
        gen_dir.mkdir()
        gen_file = gen_dir / "test_problem.py"
        gen_file.write_text("def generate(n, seed=None): yield 'test'")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            module = test_runner.load_generator_module("test_problem")
            assert module is not None
            assert hasattr(module, 'generate')
        finally:
            os.chdir(original_cwd)


class TestTruncateInput:
    """Test truncate_input function."""
    
    def test_short_input_not_truncated(self):
        """Test that short input is not truncated."""
        input_data = "short input"
        result = test_runner.truncate_input(input_data, max_length=100)
        assert result == "short input"
    
    def test_long_input_truncated(self):
        """Test that long input is truncated."""
        input_data = "x" * 300
        result = test_runner.truncate_input(input_data, max_length=200)
        assert len(result) > 200  # Includes "... (N chars total)"
        assert "..." in result
        assert "300 chars total" in result
    
    def test_exact_length_not_truncated(self):
        """Test that input at exact max length is not truncated."""
        input_data = "x" * 200
        result = test_runner.truncate_input(input_data, max_length=200)
        assert result == input_data


class TestFormatValidationLabel:
    """Test format_validation_label function."""
    
    def test_exact_mode_label(self):
        """Test label for exact mode."""
        assert test_runner.format_validation_label("exact") == "[exact]"
    
    def test_sorted_mode_label(self):
        """Test label for sorted mode."""
        assert test_runner.format_validation_label("sorted") == "[sorted]"
    
    def test_judge_mode_label(self):
        """Test label for judge mode."""
        assert test_runner.format_validation_label("judge") == "[judge]"
    
    def test_judge_only_mode_label(self):
        """Test label for judge-only mode."""
        assert test_runner.format_validation_label("judge-only") == "[judge-only]"


class TestRunOneCase:
    """Test run_one_case function."""
    
    @pytest.fixture
    def test_environment(self, tmp_path):
        """Create test environment."""
        # Create directories
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Create solution file
        solution_file = solutions_dir / "test_problem.py"
        solution_code = """#!/usr/bin/env python3
import sys

def solve():
    line = sys.stdin.readline().strip()
    print(line)

if __name__ == "__main__":
    solve()
"""
        solution_file.write_text(solution_code)
        
        # Create test files
        input_file = tests_dir / "test_problem_1.in"
        input_file.write_text("test input\n")
        
        output_file = tests_dir / "test_problem_1.out"
        output_file.write_text("test input\n")
        
        return {
            'tmp_path': tmp_path,
            'solutions_dir': solutions_dir,
            'tests_dir': tests_dir,
            'input_file': str(input_file),
            'output_file': str(output_file)
        }
    
    def test_successful_case_run(self, test_environment):
        """Test successful case execution."""
        env = test_environment
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            ok, elapsed_ms, actual, expected, validation_mode, *_ = test_runner.run_one_case(
                "test_problem",
                env['input_file'],
                env['output_file'],
                method=None,
                benchmark=True,
                compare_mode="exact",
                module=None
            )
            
            assert ok is True
            assert elapsed_ms >= 0
            assert actual.strip() == "test input"
            assert expected.strip() == "test input"
            assert validation_mode == "exact"
        finally:
            os.chdir(original_cwd)
    
    def test_missing_output_file_without_judge(self, test_environment):
        """Test handling of missing output file without JUDGE_FUNC."""
        env = test_environment
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            # Use non-existent output file
            ok, elapsed_ms, actual, expected, validation_mode, *_ = test_runner.run_one_case(
                "test_problem",
                env['input_file'],
                "nonexistent.out",
                method=None,
                benchmark=False,
                compare_mode="exact",
                module=None
            )
            
            # Should skip when no .out and no JUDGE_FUNC
            assert ok is None
            assert validation_mode == "skip"
        finally:
            os.chdir(original_cwd)
    
    def test_with_judge_func(self, test_environment):
        """Test case execution with JUDGE_FUNC."""
        env = test_environment
        
        # Create mock module with JUDGE_FUNC
        class MockModule:
            @staticmethod
            def JUDGE_FUNC(actual, expected, input_data):
                return actual == expected
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            ok, elapsed_ms, actual, expected, validation_mode, *_ = test_runner.run_one_case(
                "test_problem",
                env['input_file'],
                env['output_file'],
                method=None,
                benchmark=False,
                compare_mode="exact",
                module=MockModule()
            )
            
            assert ok is True
            assert validation_mode == "judge"
        finally:
            os.chdir(original_cwd)


class TestSaveFailedCase:
    """Test save_failed_case function."""
    
    def test_save_first_failed_case(self, tmp_path):
        """Test saving the first failed case."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        
        input_data = "failed input data\n"
        saved_path = test_runner.save_failed_case("test_problem", input_data, str(tests_dir))
        
        assert os.path.exists(saved_path)
        assert "test_problem_failed_1.in" in saved_path
        
        with open(saved_path, 'r') as f:
            content = f.read()
        assert content == "failed input data\n"
    
    def test_save_multiple_failed_cases(self, tmp_path):
        """Test saving multiple failed cases increments counter."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        
        # Save first failed case
        input_data1 = "failed input 1\n"
        saved_path1 = test_runner.save_failed_case("test_problem", input_data1, str(tests_dir))
        assert "test_problem_failed_1.in" in saved_path1
        
        # Save second failed case
        input_data2 = "failed input 2\n"
        saved_path2 = test_runner.save_failed_case("test_problem", input_data2, str(tests_dir))
        assert "test_problem_failed_2.in" in saved_path2
        
        # Verify both files exist
        assert os.path.exists(saved_path1)
        assert os.path.exists(saved_path2)
    
    def test_save_without_trailing_newline(self, tmp_path):
        """Test that newline is added if missing."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        
        input_data = "no newline"
        saved_path = test_runner.save_failed_case("test_problem", input_data, str(tests_dir))
        
        with open(saved_path, 'r') as f:
            content = f.read()
        assert content == "no newline\n"


class TestRunMethodTests:
    """Test run_method_tests function."""
    
    def test_method_results_structure(self):
        """Test that run_method_tests returns correct structure."""
        method_name = "default"
        method_info = {
            "method": "default",
            "complexity": "O(n)",
            "description": "Test method"
        }
        
        # Mock with no input files
        result = test_runner.run_method_tests(
            problem="test_problem",
            method_name=method_name,
            method_info=method_info,
            input_files=[],
            benchmark=False,
            compare_mode="exact",
            module=None,
            generator_module=None,
            generate_count=0,
            seed=None,
            save_failed=False,
            tests_dir="tests"
        )
        
        # Verify structure
        assert result["method"] == "default"
        assert result["display_name"] == "default"
        assert result["complexity"] == "O(n)"
        assert result["description"] == "Test method"
        assert result["passed"] == 0
        assert result["total"] == 0
        assert result["skipped"] == 0
        assert result["gen_passed"] == 0
        assert result["gen_total"] == 0
        assert isinstance(result["cases"], list)
        assert isinstance(result["times"], list)
        assert isinstance(result["validation_summary"], dict)


class TestPrintBenchmarkSummary:
    """Test print_benchmark_summary function."""
    
    def test_benchmark_summary_without_generated(self, capsys):
        """Test benchmark summary without generated tests."""
        results = [
            {
                "method": "default",
                "complexity": "O(n)",
                "passed": 3,
                "total": 3,
                "times": [10.0, 15.0, 20.0],
                "gen_total": 0
            },
            {
                "method": "optimized",
                "complexity": "O(log n)",
                "passed": 3,
                "total": 3,
                "times": [5.0, 7.0, 8.0],
                "gen_total": 0
            }
        ]
        
        test_runner.print_benchmark_summary(results)
        
        captured = capsys.readouterr()
        assert "Performance Comparison" in captured.out
        assert "default" in captured.out
        assert "optimized" in captured.out
        assert "O(n)" in captured.out
        assert "O(log n)" in captured.out
    
    def test_benchmark_summary_with_generated(self, capsys):
        """Test benchmark summary with generated tests."""
        results = [
            {
                "method": "default",
                "complexity": "O(n)",
                "passed": 3,
                "total": 3,
                "times": [10.0, 15.0, 20.0],
                "gen_passed": 5,
                "gen_total": 5
            }
        ]
        
        test_runner.print_benchmark_summary(results)
        
        captured = capsys.readouterr()
        assert "Performance Comparison" in captured.out
        assert "Static" in captured.out
        assert "Generated" in captured.out


@pytest.mark.edge_case
class TestEdgeCases:
    """Test edge cases for test_runner."""
    
    def test_empty_input_file(self, tmp_path):
        """Test handling of empty input file."""
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Create solution
        solution_file = solutions_dir / "test_problem.py"
        solution_file.write_text("import sys\nprint(sys.stdin.read())")
        
        # Create empty input
        input_file = tests_dir / "test_problem_1.in"
        input_file.write_text("")
        
        output_file = tests_dir / "test_problem_1.out"
        output_file.write_text("")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            
            ok, elapsed_ms, actual, expected, validation_mode, *_ = test_runner.run_one_case(
                "test_problem",
                str(input_file),
                str(output_file),
                method=None,
                benchmark=False,
                compare_mode="exact",
                module=None
            )
            
            # Should handle empty input gracefully
            assert ok is True or ok is False  # Either pass or fail, but not crash
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="Windows subprocess has encoding issues with emoji"
    )
    def test_unicode_in_files(self, tmp_path):
        """Test handling of Unicode in test files."""
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Create solution that echoes input
        solution_file = solutions_dir / "test_problem.py"
        solution_code = """#!/usr/bin/env python3
import sys
print(sys.stdin.read().strip())
"""
        solution_file.write_text(solution_code)
        
        # Create input with Unicode (no emoji for Windows compatibility)
        input_file = tests_dir / "test_problem_1.in"
        input_file.write_text("Hello 世界\n", encoding='utf-8')
        
        output_file = tests_dir / "test_problem_1.out"
        output_file.write_text("Hello 世界\n", encoding='utf-8')
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            
            ok, elapsed_ms, actual, expected, validation_mode, *_ = test_runner.run_one_case(
                "test_problem",
                str(input_file),
                str(output_file),
                method=None,
                benchmark=False,
                compare_mode="exact",
                module=None
            )
            
            assert ok is True
            assert "世界" in actual
        finally:
            os.chdir(original_cwd)
    
    def test_unicode_cjk_in_files(self, tmp_path):
        """Test handling of CJK characters in test files (Windows compatible)."""
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Create solution that echoes input
        solution_file = solutions_dir / "test_problem.py"
        solution_code = """#!/usr/bin/env python3
import sys
print(sys.stdin.read().strip())
"""
        solution_file.write_text(solution_code)
        
        # Create input with CJK characters (no emoji)
        input_file = tests_dir / "test_problem_1.in"
        input_file.write_text("Hello 世界 你好\n", encoding='utf-8')
        
        output_file = tests_dir / "test_problem_1.out"
        output_file.write_text("Hello 世界 你好\n", encoding='utf-8')
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            
            ok, elapsed_ms, actual, expected, validation_mode, *_ = test_runner.run_one_case(
                "test_problem",
                str(input_file),
                str(output_file),
                method=None,
                benchmark=False,
                compare_mode="exact",
                module=None
            )
            
            assert ok is True
            assert "世界" in actual
            assert "你好" in actual
        finally:
            os.chdir(original_cwd)
    
    def test_very_long_output(self, tmp_path):
        """Test handling of very long output."""
        long_output = "x" * 10000
        truncated = test_runner.truncate_input(long_output, max_length=200)
        
        assert len(truncated) < len(long_output)
        assert "..." in truncated
        assert "10000 chars total" in truncated


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


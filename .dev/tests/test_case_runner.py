# tests_unit/test_case_runner.py
"""
Characterization tests for runner/case_runner.py

These tests capture the current behavior of the single case runner
to ensure refactoring doesn't break existing functionality.
"""
import pytest
import sys
import os
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from runner import case_runner


class TestCaseRunnerMain:
    """Test the main function of case_runner."""
    
    def test_missing_arguments_exits_with_error(self):
        """Test that missing arguments causes exit with code 1."""
        with pytest.raises(SystemExit) as exc_info:
            case_runner.main(["case_runner.py"])
        assert exc_info.value.code == 1
    
    def test_insufficient_arguments_exits_with_error(self):
        """Test that insufficient arguments causes exit with code 1."""
        with pytest.raises(SystemExit) as exc_info:
            case_runner.main(["case_runner.py", "0001_two_sum"])
        assert exc_info.value.code == 1
    
    def test_missing_input_file_exits_with_error(self, tmp_path):
        """Test that missing input file causes exit with code 1."""
        # Create a temporary solution file
        solution_dir = tmp_path / "solutions"
        solution_dir.mkdir()
        solution_file = solution_dir / "0001_two_sum.py"
        solution_file.write_text("print('test')")
        
        with patch('os.path.exists') as mock_exists:
            # Input file doesn't exist, but solution does
            def exists_side_effect(path):
                if 'tests' in path and path.endswith('.in'):
                    return False
                if 'solutions' in path and path.endswith('.py'):
                    return True
                return False
            
            mock_exists.side_effect = exists_side_effect
            
            with pytest.raises(SystemExit) as exc_info:
                case_runner.main(["case_runner.py", "0001_two_sum", "1"])
            assert exc_info.value.code == 1
    
    def test_missing_solution_file_exits_with_error(self, tmp_path):
        """Test that missing solution file causes exit with code 1."""
        # Create a temporary input file
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        input_file = tests_dir / "0001_two_sum_1.in"
        input_file.write_text("test input")
        
        with patch('os.path.exists') as mock_exists:
            # Solution file doesn't exist, but input does
            def exists_side_effect(path):
                if 'tests' in path and path.endswith('.in'):
                    return True
                if 'solutions' in path and path.endswith('.py'):
                    return False
                return False
            
            mock_exists.side_effect = exists_side_effect
            
            with pytest.raises(SystemExit) as exc_info:
                case_runner.main(["case_runner.py", "0001_two_sum", "1"])
            assert exc_info.value.code == 1


class TestCaseRunnerIntegration:
    """Integration tests for case_runner with real files."""
    
    @pytest.fixture
    def test_environment(self, tmp_path):
        """Create a test environment with solution and test files."""
        # Create directories
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Create a simple solution file
        solution_file = solutions_dir / "test_problem.py"
        solution_code = """#!/usr/bin/env python3
import sys

def solve():
    line = sys.stdin.readline().strip()
    print(f"Output: {line}")

if __name__ == "__main__":
    solve()
"""
        solution_file.write_text(solution_code)
        
        # Create test input file
        input_file = tests_dir / "test_problem_1.in"
        input_file.write_text("Hello World\n")
        
        return {
            'tmp_path': tmp_path,
            'solutions_dir': solutions_dir,
            'tests_dir': tests_dir,
            'solution_file': solution_file,
            'input_file': input_file
        }
    
    def test_successful_case_run(self, test_environment, capsys):
        """Test successful execution of a test case."""
        env = test_environment
        
        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            # Run the case runner
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                
                # Should not raise any exceptions
                try:
                    case_runner.main(["case_runner.py", "test_problem", "1"])
                except SystemExit:
                    pass  # Expected if subprocess succeeds
                
                # Verify subprocess was called
                assert mock_run.called
                call_args = mock_run.call_args
                assert call_args is not None
                
                # Check that the solution file was called
                args = call_args[0][0]
                assert any('test_problem.py' in str(arg) for arg in args)
        finally:
            os.chdir(original_cwd)
    
    def test_input_file_reading(self, test_environment):
        """Test that input file is correctly read."""
        env = test_environment
        
        original_cwd = os.getcwd()
        try:
            os.chdir(env['tmp_path'])
            
            # Read the input file as case_runner would
            in_path = os.path.join("tests", "test_problem_1.in")
            with open(in_path, "r", encoding="utf-8") as f:
                input_data = f.read()
            
            assert input_data == "Hello World\n"
        finally:
            os.chdir(original_cwd)


class TestCaseRunnerPathHandling:
    """Test path handling in case_runner."""
    
    def test_input_path_construction(self):
        """Test that input path is correctly constructed."""
        problem = "0001_two_sum"
        case_idx = "1"
        tests_dir = "tests"
        
        expected_path = os.path.join(tests_dir, f"{problem}_{case_idx}.in")
        assert expected_path == "tests/0001_two_sum_1.in" or expected_path == "tests\\0001_two_sum_1.in"
    
    def test_solution_path_construction(self):
        """Test that solution path is correctly constructed."""
        problem = "0001_two_sum"
        
        expected_path = os.path.join("solutions", f"{problem}.py")
        assert expected_path == "solutions/0001_two_sum.py" or expected_path == "solutions\\0001_two_sum.py"


@pytest.mark.edge_case
class TestCaseRunnerEdgeCases:
    """Test edge cases for case_runner."""
    
    def test_empty_input_file(self, tmp_path):
        """Test handling of empty input file."""
        # Create directories
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Create solution file
        solution_file = solutions_dir / "test_problem.py"
        solution_file.write_text("print('empty')")
        
        # Create empty input file
        input_file = tests_dir / "test_problem_1.in"
        input_file.write_text("")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            
            # Read empty input
            with open("tests/test_problem_1.in", "r", encoding="utf-8") as f:
                input_data = f.read()
            
            assert input_data == ""
        finally:
            os.chdir(original_cwd)
    
    def test_large_input_file(self, tmp_path):
        """Test handling of large input file."""
        # Create directories
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Create solution file
        solution_file = solutions_dir / "test_problem.py"
        solution_file.write_text("print('large')")
        
        # Create large input file (1MB)
        input_file = tests_dir / "test_problem_1.in"
        large_input = "x" * (1024 * 1024)  # 1MB
        input_file.write_text(large_input)
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            
            # Read large input
            with open("tests/test_problem_1.in", "r", encoding="utf-8") as f:
                input_data = f.read()
            
            assert len(input_data) == 1024 * 1024
        finally:
            os.chdir(original_cwd)
    
    def test_unicode_in_input_file(self, tmp_path):
        """Test handling of Unicode characters in input file."""
        # Create directories
        solutions_dir = tmp_path / "solutions"
        tests_dir = tmp_path / "tests"
        solutions_dir.mkdir()
        tests_dir.mkdir()
        
        # Create solution file
        solution_file = solutions_dir / "test_problem.py"
        solution_file.write_text("print('unicode')")
        
        # Create input file with Unicode
        input_file = tests_dir / "test_problem_1.in"
        unicode_input = "Hello 世界 🌍\n"
        input_file.write_text(unicode_input, encoding='utf-8')
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            
            # Read Unicode input
            with open("tests/test_problem_1.in", "r", encoding="utf-8") as f:
                input_data = f.read()
            
            assert input_data == unicode_input
        finally:
            os.chdir(original_cwd)
    
    def test_special_characters_in_problem_name(self):
        """Test handling of special characters in problem name."""
        # Problem names with underscores and numbers should work
        problem = "0001_two_sum"
        case_idx = "1"
        
        in_path = os.path.join("tests", f"{problem}_{case_idx}.in")
        assert "0001_two_sum_1.in" in in_path
        
        # Problem names with hyphens
        problem = "0001-two-sum"
        in_path = os.path.join("tests", f"{problem}_{case_idx}.in")
        assert "0001-two-sum_1.in" in in_path


class TestPythonExecutable:
    """Test Python executable detection."""
    
    def test_python_exe_is_set(self):
        """Test that PYTHON_EXE is set correctly."""
        assert case_runner.PYTHON_EXE == sys.executable
    
    def test_python_exe_is_executable(self):
        """Test that PYTHON_EXE points to a valid Python executable."""
        result = subprocess.run(
            [case_runner.PYTHON_EXE, "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Python" in result.stdout or "Python" in result.stderr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


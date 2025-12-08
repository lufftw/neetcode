# tests_unit/test_util.py
"""
Characterization tests for runner/util.py

These tests capture the current behavior of utility functions
to ensure refactoring doesn't break existing functionality.
"""
import pytest
import os
import sys
import tempfile
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from runner.util import (
    normalize_output,
    compare_outputs,
    compare_result,
    _compare_sorted,
    _compare_set,
    get_solution_path,
    get_test_input_path,
    get_test_output_path,
    read_file,
    write_file,
    file_exists,
)


class TestNormalizeOutput:
    """Test normalize_output function behavior."""
    
    def test_basic_normalization(self):
        """Test basic whitespace normalization."""
        assert normalize_output("hello\n") == "hello"
        assert normalize_output("hello") == "hello"
        assert normalize_output("  hello  \n") == "hello"
    
    def test_multiline_normalization(self):
        """Test multiline output normalization."""
        input_str = "line1  \nline2  \nline3  \n"
        expected = "line1\nline2\nline3"
        assert normalize_output(input_str) == expected
    
    def test_trailing_whitespace_removal(self):
        """Test that trailing whitespace on each line is removed."""
        input_str = "hello world  \nfoo bar  "
        expected = "hello world\nfoo bar"
        assert normalize_output(input_str) == expected
    
    def test_empty_string(self):
        """Test empty string handling."""
        assert normalize_output("") == ""
        assert normalize_output("\n") == ""
        assert normalize_output("  \n  \n  ") == ""
    
    def test_preserves_internal_whitespace(self):
        """Test that internal whitespace is preserved."""
        assert normalize_output("hello  world") == "hello  world"
        assert normalize_output("a    b    c") == "a    b    c"


class TestCompareOutputs:
    """Test compare_outputs function behavior."""
    
    def test_exact_mode_basic(self):
        """Test exact comparison mode."""
        assert compare_outputs("hello", "hello", "exact") is True
        assert compare_outputs("hello", "world", "exact") is False
        assert compare_outputs("[1, 2]", "[1, 2]", "exact") is True
        assert compare_outputs("[1, 2]", "[2, 1]", "exact") is False
    
    def test_exact_mode_with_whitespace(self):
        """Test exact mode handles whitespace normalization."""
        assert compare_outputs("hello\n", "hello", "exact") is True
        assert compare_outputs("hello  \n", "hello", "exact") is True
    
    def test_sorted_mode_simple_list(self):
        """Test sorted comparison for simple lists."""
        assert compare_outputs("[2, 1, 3]", "[1, 2, 3]", "sorted") is True
        assert compare_outputs("[1, 2]", "[2, 1]", "sorted") is True
        assert compare_outputs("[1, 2]", "[1, 3]", "sorted") is False
    
    def test_sorted_mode_nested_list(self):
        """Test sorted comparison for nested lists (e.g., N-Queens)."""
        actual = "[['.Q..', '...Q'], ['Q...', '..Q.']]"
        expected = "[['Q...', '..Q.'], ['.Q..', '...Q']]"
        assert compare_outputs(actual, expected, "sorted") is True
    
    def test_sorted_mode_different_length(self):
        """Test sorted mode rejects different lengths."""
        assert compare_outputs("[1, 2]", "[1, 2, 3]", "sorted") is False
    
    def test_set_mode_simple_list(self):
        """Test set comparison for simple lists."""
        assert compare_outputs("[1, 2, 2, 3]", "[3, 2, 1]", "set") is True
        assert compare_outputs("[1, 2]", "[2, 1, 1]", "set") is True
    
    def test_set_mode_nested_list(self):
        """Test set comparison for nested lists."""
        actual = "[[1, 2], [3, 4], [1, 2]]"
        expected = "[[3, 4], [1, 2]]"
        assert compare_outputs(actual, expected, "set") is True
    
    def test_invalid_mode_falls_back_to_exact(self):
        """Test that invalid mode falls back to exact comparison."""
        assert compare_outputs("hello", "hello", "invalid") is True
        assert compare_outputs("hello", "world", "invalid") is False


class TestCompareSorted:
    """Test _compare_sorted helper function."""
    
    def test_simple_list(self):
        """Test sorting simple lists."""
        assert _compare_sorted([3, 1, 2], [1, 2, 3]) is True
        assert _compare_sorted([1, 2], [2, 1]) is True
        assert _compare_sorted([1, 2], [1, 3]) is False
    
    def test_nested_list(self):
        """Test sorting nested lists."""
        actual = [['b', 'a'], ['d', 'c']]
        expected = [['d', 'c'], ['b', 'a']]
        assert _compare_sorted(actual, expected) is True
    
    def test_empty_list(self):
        """Test empty list comparison."""
        assert _compare_sorted([], []) is True
    
    def test_different_lengths(self):
        """Test lists with different lengths."""
        assert _compare_sorted([1, 2], [1, 2, 3]) is False
    
    def test_non_list_types(self):
        """Test non-list types."""
        assert _compare_sorted(42, 42) is True
        assert _compare_sorted("hello", "hello") is True
        assert _compare_sorted(42, 43) is False


class TestCompareSet:
    """Test _compare_set helper function."""
    
    def test_simple_list_with_duplicates(self):
        """Test set comparison ignores duplicates."""
        assert _compare_set([1, 2, 2, 3], [3, 2, 1]) is True
        assert _compare_set([1, 1, 1], [1]) is True
    
    def test_nested_list(self):
        """Test set comparison for nested lists."""
        actual = [[1, 2], [3, 4], [1, 2]]
        expected = [[3, 4], [1, 2]]
        assert _compare_set(actual, expected) is True
    
    def test_different_elements(self):
        """Test set comparison rejects different elements."""
        assert _compare_set([1, 2], [2, 3]) is False
    
    def test_empty_list(self):
        """Test empty list comparison."""
        assert _compare_set([], []) is True
    
    def test_non_list_types(self):
        """Test non-list types."""
        assert _compare_set(42, 42) is True
        assert _compare_set("hello", "hello") is True


class TestCompareResult:
    """Test compare_result function with JUDGE_FUNC support."""
    
    def test_exact_mode_without_judge(self):
        """Test exact comparison without JUDGE_FUNC."""
        actual = "[1, 2, 3]"
        expected = "[1, 2, 3]"
        input_data = "test input"
        
        # Module without JUDGE_FUNC
        class MockModule:
            pass
        
        module = MockModule()
        assert compare_result(actual, expected, input_data, module, "exact") is True
    
    def test_sorted_mode_without_judge(self):
        """Test sorted comparison without JUDGE_FUNC."""
        actual = "[2, 1, 3]"
        expected = "[1, 2, 3]"
        input_data = "test input"
        
        class MockModule:
            pass
        
        module = MockModule()
        assert compare_result(actual, expected, input_data, module, "sorted") is True
    
    def test_with_judge_func_passing(self):
        """Test comparison with JUDGE_FUNC that passes."""
        actual = "[1, 2, 3]"
        expected = "[1, 2, 3]"
        input_data = "3"
        
        class MockModule:
            @staticmethod
            def JUDGE_FUNC(actual_obj, expected_obj, input_str):
                return len(actual_obj) == int(input_str)
        
        module = MockModule()
        assert compare_result(actual, expected, input_data, module, "exact") is True
    
    def test_with_judge_func_failing(self):
        """Test comparison with JUDGE_FUNC that fails."""
        actual = "[1, 2]"
        expected = "[1, 2, 3]"
        input_data = "3"
        
        class MockModule:
            @staticmethod
            def JUDGE_FUNC(actual_obj, expected_obj, input_str):
                return len(actual_obj) == int(input_str)
        
        module = MockModule()
        assert compare_result(actual, expected, input_data, module, "exact") is False
    
    def test_judge_func_with_none_expected(self):
        """Test JUDGE_FUNC with None expected (judge-only mode)."""
        actual = "[[1, 2], [3, 4]]"
        expected = None
        input_data = "4"
        
        class MockModule:
            @staticmethod
            def JUDGE_FUNC(actual_obj, expected_obj, input_str):
                # Validate that actual is a valid N-Queens solution
                return expected_obj is None and len(actual_obj) == 2
        
        module = MockModule()
        assert compare_result(actual, expected, input_data, module, "exact") is True
    
    def test_judge_func_with_unparseable_output(self):
        """Test JUDGE_FUNC with output that can't be parsed."""
        actual = "not a list"
        expected = "also not a list"
        input_data = "test"
        
        class MockModule:
            @staticmethod
            def JUDGE_FUNC(actual_obj, expected_obj, input_str):
                # Should receive strings when parsing fails
                return isinstance(actual_obj, str) and actual_obj == "not a list"
        
        module = MockModule()
        assert compare_result(actual, expected, input_data, module, "exact") is True


class TestPathHelpers:
    """Test path helper functions."""
    
    def test_get_solution_path(self):
        """Test solution path generation."""
        path = get_solution_path("0001_two_sum")
        assert path.endswith("solutions/0001_two_sum.py") or path.endswith("solutions\\0001_two_sum.py")
        assert "0001_two_sum.py" in path
    
    def test_get_test_input_path(self):
        """Test test input path generation."""
        path = get_test_input_path("0001_two_sum", 1)
        assert "0001_two_sum_1.in" in path
        
        path = get_test_input_path("0001_two_sum", "1")
        assert "0001_two_sum_1.in" in path
    
    def test_get_test_output_path(self):
        """Test test output path generation."""
        path = get_test_output_path("0001_two_sum", 1)
        assert "0001_two_sum_1.out" in path
        
        path = get_test_output_path("0001_two_sum", "1")
        assert "0001_two_sum_1.out" in path
    
    def test_custom_tests_dir(self):
        """Test custom tests directory."""
        path = get_test_input_path("0001_two_sum", 1, "custom_tests")
        assert "custom_tests" in path
        assert "0001_two_sum_1.in" in path


class TestFileOperations:
    """Test file operation functions."""
    
    def test_read_write_file(self):
        """Test reading and writing files."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_path = f.name
        
        try:
            # Write
            content = "Hello, World!\nLine 2"
            write_file(temp_path, content)
            
            # Read
            read_content = read_file(temp_path)
            assert read_content == content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_file_exists(self):
        """Test file existence check."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            assert file_exists(temp_path) is True
            os.unlink(temp_path)
            assert file_exists(temp_path) is False
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_read_file_with_unicode(self):
        """Test reading files with Unicode characters."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_path = f.name
            f.write("Hello 世界 🌍")
        
        try:
            content = read_file(temp_path)
            assert content == "Hello 世界 🌍"
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


@pytest.mark.edge_case
class TestEdgeCases:
    """Test edge cases for utility functions."""
    
    def test_normalize_output_edge_cases(self):
        """Test normalize_output with edge cases."""
        # Multiple consecutive newlines
        assert normalize_output("\n\n\n") == ""
        
        # Only whitespace
        assert normalize_output("   ") == ""
        
        # Mixed whitespace
        assert normalize_output("\t\n  \r\n") == ""
    
    def test_compare_outputs_edge_cases(self):
        """Test compare_outputs with edge cases."""
        # Empty strings
        assert compare_outputs("", "", "exact") is True
        
        # Whitespace only
        assert compare_outputs("  \n", "", "exact") is True
        
        # Invalid Python syntax in sorted mode (should fall back to exact)
        assert compare_outputs("not [a list", "not [a list", "sorted") is True
        assert compare_outputs("not [a list", "different", "sorted") is False
    
    def test_compare_sorted_edge_cases(self):
        """Test _compare_sorted with edge cases."""
        # Single element
        assert _compare_sorted([1], [1]) is True
        
        # Nested empty lists
        assert _compare_sorted([[]], [[]]) is True
        
        # Same type elements
        assert _compare_sorted([3, 1, 2], [1, 2, 3]) is True
        assert _compare_sorted(["c", "a", "b"], ["a", "b", "c"]) is True
        
        # Note: Mixed types (int + str) cannot be sorted in Python 3
        # This is expected behavior, not a bug
    
    def test_compare_set_edge_cases(self):
        """Test _compare_set with edge cases."""
        # Single element
        assert _compare_set([1], [1, 1, 1]) is True
        
        # Empty nested lists
        assert _compare_set([[]], [[]]) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


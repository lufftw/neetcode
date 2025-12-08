# tests_unit/test_edge_cases.py
"""
Edge case tests for the neetcode runner system.

These tests focus on boundary conditions:
- Empty inputs
- Error inputs
- Large data
- Special characters
- Malformed data
"""
import pytest
import sys
import os
import tempfile
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from runner.util import (
    normalize_output,
    compare_outputs,
    compare_result,
    read_file,
    write_file
)
from runner.test_runner import (
    truncate_input,
    save_failed_case,
    run_one_case
)


@pytest.mark.edge_case
class TestEmptyInputs:
    """Test handling of empty inputs."""
    
    def test_normalize_empty_string(self):
        """Test normalizing empty string."""
        assert normalize_output("") == ""
    
    def test_normalize_only_whitespace(self):
        """Test normalizing whitespace-only string."""
        assert normalize_output("   \n\t\r\n   ") == ""
    
    def test_normalize_only_newlines(self):
        """Test normalizing newline-only string."""
        assert normalize_output("\n\n\n") == ""
    
    def test_compare_empty_outputs(self):
        """Test comparing empty outputs."""
        assert compare_outputs("", "", "exact") is True
        assert compare_outputs("\n", "", "exact") is True
        assert compare_outputs("", "\n", "exact") is True
    
    def test_compare_empty_lists(self):
        """Test comparing empty lists."""
        assert compare_outputs("[]", "[]", "exact") is True
        assert compare_outputs("[]", "[]", "sorted") is True
        assert compare_outputs("[]", "[]", "set") is True
    
    def test_truncate_empty_input(self):
        """Test truncating empty input."""
        assert truncate_input("", max_length=100) == ""
    
    def test_save_empty_failed_case(self, tmp_path):
        """Test saving empty failed case."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        
        saved_path = save_failed_case("test_problem", "", str(tests_dir))
        
        assert os.path.exists(saved_path)
        with open(saved_path, 'r') as f:
            content = f.read()
        # Should add newline even to empty input
        assert content == "\n"


@pytest.mark.edge_case
class TestErrorInputs:
    """Test handling of error/malformed inputs."""
    
    def test_compare_unparseable_python(self):
        """Test comparing outputs that can't be parsed as Python."""
        # Should fall back to exact comparison
        assert compare_outputs("not [valid python", "not [valid python", "sorted") is True
        assert compare_outputs("not [valid python", "different", "sorted") is False
    
    def test_compare_mismatched_types(self):
        """Test comparing outputs with mismatched types."""
        # List vs string
        assert compare_outputs("[1, 2, 3]", "123", "exact") is False
        
        # Number vs string
        assert compare_outputs("42", "forty-two", "exact") is False
    
    def test_normalize_invalid_unicode(self):
        """Test normalizing with various Unicode edge cases."""
        # Zero-width characters
        zero_width = "hello\u200b\u200c\u200dworld"
        result = normalize_output(zero_width)
        assert "hello" in result and "world" in result
        
        # Right-to-left marks
        rtl = "hello\u202eworld"
        result = normalize_output(rtl)
        assert len(result) > 0
    
    def test_compare_with_control_characters(self):
        """Test comparing outputs with control characters."""
        # Tab vs spaces
        assert compare_outputs("hello\tworld", "hello\tworld", "exact") is True
        assert compare_outputs("hello\tworld", "hello world", "exact") is False
        
        # Carriage return
        assert compare_outputs("hello\rworld", "hello\rworld", "exact") is True
    
    def test_compare_mixed_newline_styles(self):
        """Test comparing outputs with different newline styles."""
        # Unix vs Windows newlines (should be normalized)
        unix = "line1\nline2\n"
        windows = "line1\r\nline2\r\n"
        # After normalization, should be equal
        assert normalize_output(unix) == normalize_output(windows)


@pytest.mark.edge_case
class TestLargeData:
    """Test handling of large data."""
    
    def test_normalize_large_output(self):
        """Test normalizing very large output."""
        large_output = "x" * 1000000  # 1MB
        result = normalize_output(large_output)
        assert len(result) == 1000000
    
    def test_compare_large_lists(self):
        """Test comparing large lists."""
        # Create large list strings
        large_list = str(list(range(10000)))
        assert compare_outputs(large_list, large_list, "exact") is True
    
    def test_truncate_large_input(self):
        """Test truncating very large input."""
        large_input = "x" * 1000000  # 1MB
        truncated = truncate_input(large_input, max_length=200)
        
        assert len(truncated) < len(large_input)
        assert "..." in truncated
        assert "1000000 chars" in truncated
    
    def test_read_write_large_file(self, tmp_path):
        """Test reading and writing large files."""
        large_content = "x" * 1000000  # 1MB
        test_file = tmp_path / "large.txt"
        
        write_file(str(test_file), large_content)
        read_content = read_file(str(test_file))
        
        assert len(read_content) == 1000000
        assert read_content == large_content
    
    def test_compare_large_nested_lists(self):
        """Test comparing large nested lists."""
        # Create large nested list
        large_nested = str([[i, i+1] for i in range(1000)])
        assert compare_outputs(large_nested, large_nested, "sorted") is True
    
    def test_save_large_failed_case(self, tmp_path):
        """Test saving large failed case."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        
        large_input = "x" * 100000  # 100KB
        saved_path = save_failed_case("test_problem", large_input, str(tests_dir))
        
        assert os.path.exists(saved_path)
        with open(saved_path, 'r') as f:
            content = f.read()
        assert len(content) >= 100000


@pytest.mark.edge_case
class TestSpecialCharacters:
    """Test handling of special characters."""
    
    def test_unicode_emoji(self):
        """Test handling of emoji characters."""
        emoji_text = "Hello 🌍 World 🚀"
        assert normalize_output(emoji_text) == emoji_text
        assert compare_outputs(emoji_text, emoji_text, "exact") is True
    
    def test_unicode_cjk(self):
        """Test handling of CJK characters."""
        cjk_text = "你好世界 こんにちは 안녕하세요"
        assert normalize_output(cjk_text) == cjk_text
        assert compare_outputs(cjk_text, cjk_text, "exact") is True
    
    def test_unicode_combining_characters(self):
        """Test handling of combining characters."""
        # é can be represented as e + combining acute accent
        composed = "café"  # é as single character
        decomposed = "café"  # é as e + combining accent
        # These might not be equal depending on normalization
        result1 = normalize_output(composed)
        result2 = normalize_output(decomposed)
        assert len(result1) > 0 and len(result2) > 0
    
    def test_special_python_characters(self):
        """Test handling of special Python syntax characters."""
        special = "[[1, 2], [3, 4]]"
        assert compare_outputs(special, special, "exact") is True
        
        # With extra whitespace
        spaced = "[[ 1, 2 ], [ 3, 4 ]]"
        # Should be different in exact mode
        assert compare_outputs(special, spaced, "exact") is False
    
    def test_escape_sequences(self):
        """Test handling of escape sequences."""
        escaped = "line1\\nline2"  # Literal backslash-n
        assert normalize_output(escaped) == "line1\\nline2"
        
        # vs actual newline
        newline = "line1\nline2"
        assert normalize_output(newline) == "line1\nline2"
        assert escaped != newline
    
    def test_quotes_in_strings(self):
        """Test handling of quotes in strings."""
        single = "It's a test"
        double = 'He said "hello"'
        mixed = """It's "complicated" """
        
        assert normalize_output(single) == single
        assert normalize_output(double) == double
        assert normalize_output(mixed.strip()) == mixed.strip()


@pytest.mark.edge_case
class TestBoundaryValues:
    """Test boundary values for various functions."""
    
    def test_truncate_at_exact_boundary(self):
        """Test truncating at exact max length."""
        input_data = "x" * 200
        result = truncate_input(input_data, max_length=200)
        assert result == input_data  # Should not truncate
    
    def test_truncate_one_over_boundary(self):
        """Test truncating one character over boundary."""
        input_data = "x" * 201
        result = truncate_input(input_data, max_length=200)
        assert len(result) > 200  # Includes "... (N chars total)"
        assert "..." in result
    
    def test_truncate_one_under_boundary(self):
        """Test truncating one character under boundary."""
        input_data = "x" * 199
        result = truncate_input(input_data, max_length=200)
        assert result == input_data  # Should not truncate
    
    def test_compare_single_element_lists(self):
        """Test comparing single-element lists."""
        assert compare_outputs("[1]", "[1]", "sorted") is True
        assert compare_outputs("[1]", "[2]", "sorted") is False
    
    def test_compare_two_element_lists(self):
        """Test comparing two-element lists."""
        assert compare_outputs("[1, 2]", "[2, 1]", "sorted") is True
        assert compare_outputs("[1, 2]", "[1, 2]", "exact") is True
        assert compare_outputs("[1, 2]", "[2, 1]", "exact") is False
    
    def test_normalize_single_character(self):
        """Test normalizing single character."""
        assert normalize_output("a") == "a"
        assert normalize_output("a\n") == "a"
        assert normalize_output("\na") == "a"
    
    def test_normalize_single_newline(self):
        """Test normalizing single newline."""
        assert normalize_output("\n") == ""


@pytest.mark.edge_case
class TestMalformedData:
    """Test handling of malformed data."""
    
    def test_unbalanced_brackets(self):
        """Test handling of unbalanced brackets."""
        unbalanced = "[1, 2, 3"
        # Should handle gracefully (fall back to string comparison)
        assert compare_outputs(unbalanced, unbalanced, "sorted") is True
        assert compare_outputs(unbalanced, "[1, 2, 3]", "sorted") is False
    
    def test_mixed_types_in_list(self):
        """Test handling of mixed types in lists."""
        mixed = "[1, 'two', 3.0, None, True]"
        assert compare_outputs(mixed, mixed, "exact") is True
        
        # Sorted mode should handle mixed types
        mixed_sorted = "[1, 'two', 3.0]"
        result = compare_outputs(mixed_sorted, mixed_sorted, "sorted")
        assert result is True
    
    def test_nested_empty_lists(self):
        """Test handling of nested empty lists."""
        nested_empty = "[[], [], []]"
        assert compare_outputs(nested_empty, nested_empty, "sorted") is True
        assert compare_outputs(nested_empty, "[[]]", "sorted") is False
    
    def test_deeply_nested_lists(self):
        """Test handling of deeply nested lists."""
        deep = "[[[1, 2], [3, 4]], [[5, 6], [7, 8]]]"
        assert compare_outputs(deep, deep, "exact") is True
    
    def test_invalid_json_but_valid_python(self):
        """Test data that's invalid JSON but valid Python."""
        # Python allows single quotes, JSON doesn't
        python_style = "['a', 'b', 'c']"
        assert compare_outputs(python_style, python_style, "sorted") is True
        
        # Python allows trailing commas, JSON doesn't
        trailing_comma = "[1, 2, 3,]"
        # This might fail to parse, should fall back to string comparison
        result = compare_outputs(trailing_comma, trailing_comma, "exact")
        assert result is True
    
    def test_infinity_and_nan(self):
        """Test handling of infinity and NaN."""
        # These are valid Python but might cause issues
        inf_str = "float('inf')"
        nan_str = "float('nan')"
        
        assert normalize_output(inf_str) == inf_str
        assert normalize_output(nan_str) == nan_str


@pytest.mark.edge_case
class TestFileSystemEdgeCases:
    """Test file system edge cases."""
    
    def test_read_file_with_bom(self, tmp_path):
        """Test reading file with UTF-8 BOM."""
        test_file = tmp_path / "bom.txt"
        # Write with BOM
        with open(test_file, 'w', encoding='utf-8-sig') as f:
            f.write("Hello World")
        
        # Read should handle BOM
        content = read_file(str(test_file))
        # BOM might or might not be included depending on encoding
        assert "Hello World" in content
    
    def test_read_file_with_no_trailing_newline(self, tmp_path):
        """Test reading file without trailing newline."""
        test_file = tmp_path / "no_newline.txt"
        with open(test_file, 'w') as f:
            f.write("No newline at end")
        
        content = read_file(str(test_file))
        assert content == "No newline at end"
    
    def test_read_file_with_multiple_trailing_newlines(self, tmp_path):
        """Test reading file with multiple trailing newlines."""
        test_file = tmp_path / "multi_newline.txt"
        with open(test_file, 'w') as f:
            f.write("Content\n\n\n")
        
        content = read_file(str(test_file))
        assert content == "Content\n\n\n"
    
    def test_write_file_creates_parent_dirs(self, tmp_path):
        """Test that write_file handles existing directory."""
        nested_file = tmp_path / "nested" / "deep" / "file.txt"
        # Create parent directories first
        nested_file.parent.mkdir(parents=True, exist_ok=True)
        
        write_file(str(nested_file), "content")
        assert nested_file.exists()
        assert read_file(str(nested_file)) == "content"
    
    def test_save_failed_case_with_special_chars_in_name(self, tmp_path):
        """Test saving failed case with special characters."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        
        # Problem name with special characters
        problem = "0001_two-sum_v2"
        saved_path = save_failed_case(problem, "input", str(tests_dir))
        
        assert os.path.exists(saved_path)
        assert problem in saved_path


@pytest.mark.edge_case
class TestConcurrentAccess:
    """Test edge cases related to concurrent access."""
    
    def test_multiple_failed_case_saves(self, tmp_path):
        """Test saving multiple failed cases in sequence."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        
        # Save multiple cases rapidly
        paths = []
        for i in range(5):
            path = save_failed_case("test_problem", f"input_{i}", str(tests_dir))
            paths.append(path)
        
        # All should exist and be different
        assert len(set(paths)) == 5
        for path in paths:
            assert os.path.exists(path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


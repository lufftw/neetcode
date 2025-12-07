# runner/util.py
"""
Common Utilities for Test Runner.
"""
import os
import sys
from typing import Optional

# Project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default directories
SOLUTIONS_DIR = os.path.join(PROJECT_ROOT, "solutions")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "templates")


def normalize_output(s: str) -> str:
    """Normalize output by removing trailing whitespace and extra newlines."""
    lines = s.strip().splitlines()
    lines = [line.rstrip() for line in lines]
    return "\n".join(lines)


def get_solution_path(problem: str) -> str:
    """Get solution file path."""
    return os.path.join(SOLUTIONS_DIR, f"{problem}.py")


def get_test_input_path(problem: str, case_idx: int | str, tests_dir: Optional[str] = None) -> str:
    """Get test input file path."""
    base_dir = tests_dir or TESTS_DIR
    return os.path.join(base_dir, f"{problem}_{case_idx}.in")


def get_test_output_path(problem: str, case_idx: int | str, tests_dir: Optional[str] = None) -> str:
    """Get test output file path."""
    base_dir = tests_dir or TESTS_DIR
    return os.path.join(base_dir, f"{problem}_{case_idx}.out")


def read_file(path: str) -> str:
    """Read file contents."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    """Write content to file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def file_exists(path: str) -> bool:
    """Check if file exists."""
    return os.path.exists(path)


def compare_outputs(actual: str, expected: str, compare_mode: str = "exact") -> bool:
    """
    Compare two outputs with different comparison modes.
    
    Args:
        actual: Actual output
        expected: Expected output
        compare_mode: Comparison mode
            - "exact": Exact string match (default)
            - "sorted": Sort before comparison (for "return in any order" problems)
            - "set": Set comparison (for unique elements, order doesn't matter)
    
    Returns:
        bool: Whether outputs match
    
    Examples:
        # N-Queens: order doesn't matter
        >>> compare_outputs("[['.Q..'], ['..Q.']]", "[['..Q.'], ['.Q..']]", "sorted")
        True
        
        # Two Sum: exact match required
        >>> compare_outputs("[0, 1]", "[1, 0]", "exact")
        False
    """
    import ast
    
    actual_norm = normalize_output(actual)
    expected_norm = normalize_output(expected)
    
    # Exact comparison
    if compare_mode == "exact":
        return actual_norm == expected_norm
    
    # Try to parse as Python objects for advanced comparison
    try:
        actual_obj = ast.literal_eval(actual_norm)
        expected_obj = ast.literal_eval(expected_norm)
        
        if compare_mode == "sorted":
            return _compare_sorted(actual_obj, expected_obj)
        
        elif compare_mode == "set":
            return _compare_set(actual_obj, expected_obj)
    
    except (ValueError, SyntaxError):
        # Fall back to exact comparison if parsing fails
        pass
    
    return actual_norm == expected_norm


def _compare_sorted(actual: any, expected: any) -> bool:
    """
    Sort and compare, supporting nested lists.
    
    Handles:
        - List[List[str]]: N-Queens, Permutations
        - List[List[int]]: Combination Sum, Subsets
        - List[int/str]: Simple lists
    """
    if not isinstance(actual, list) or not isinstance(expected, list):
        return actual == expected
    
    if len(actual) != len(expected):
        return False
    
    # Empty list
    if not actual:
        return True
    
    # Nested list (e.g., N-Queens: List[List[str]])
    if isinstance(actual[0], list):
        # Convert inner lists to tuples for sorting
        try:
            actual_sorted = sorted(tuple(x) for x in actual)
            expected_sorted = sorted(tuple(x) for x in expected)
            return actual_sorted == expected_sorted
        except TypeError:
            # Fall back to direct comparison if sorting fails
            return actual == expected
    
    # Single-level list
    try:
        return sorted(actual) == sorted(expected)
    except TypeError:
        return actual == expected


def _compare_set(actual: any, expected: any) -> bool:
    """Set comparison, ignoring duplicates and order."""
    if not isinstance(actual, list) or not isinstance(expected, list):
        return actual == expected
    
    # Nested list - convert to set of tuples
    if actual and isinstance(actual[0], list):
        try:
            actual_set = set(tuple(x) for x in actual)
            expected_set = set(tuple(x) for x in expected)
            return actual_set == expected_set
        except TypeError:
            return actual == expected
    
    # Single-level list
    try:
        return set(actual) == set(expected)
    except TypeError:
        return actual == expected


def compare_result(actual_str: str, expected_str: str, input_str: str,
                   module, compare_mode: str = "exact") -> bool:
    """
    Integrated comparison logic supporting JUDGE_FUNC and COMPARE_MODE.
    
    Priority:
        1. JUDGE_FUNC (user-defined validation function)
        2. COMPARE_MODE (framework-provided: exact/sorted/set)
    
    Args:
        actual_str: Actual program output (raw string)
        expected_str: Expected output (raw string)
        input_str: Input data (raw string)
        module: Loaded solution module
        compare_mode: Comparison mode ("exact" | "sorted" | "set")
    
    Returns:
        bool: Whether the answer is correct
    
    JUDGE_FUNC Signature:
        def judge(actual, expected, input_data) -> bool
        
        - If actual/expected can be parsed by ast.literal_eval, pass parsed objects
        - If parsing fails, pass raw strings
        - input_data is always raw string
    
    Examples:
        # Decision Problem validation (object mode)
        def judge(actual: list, expected: list, input_data: str) -> bool:
            n = int(input_data)
            return is_valid_solution(actual, n)
        
        # Custom format comparison (string mode)
        def judge(actual: str, expected: str, input_data: str) -> bool:
            return parse_linked_list(actual) == parse_linked_list(expected)
    """
    import ast
    
    actual_norm = normalize_output(actual_str)
    expected_norm = normalize_output(expected_str)
    
    # ========== Priority 1: JUDGE_FUNC ==========
    judge_func = getattr(module, 'JUDGE_FUNC', None) if module else None
    
    if judge_func:
        # Try to parse as Python objects
        try:
            actual_obj = ast.literal_eval(actual_norm)
            expected_obj = ast.literal_eval(expected_norm)
            # Parsing succeeded -> pass objects
            return judge_func(actual_obj, expected_obj, input_str)
        except (ValueError, SyntaxError):
            # Parsing failed -> pass raw strings
            return judge_func(actual_norm, expected_norm, input_str)
    
    # ========== Priority 2: COMPARE_MODE ==========
    return compare_outputs(actual_norm, expected_norm, compare_mode)


def print_diff(expected: str, actual: str) -> None:
    """Print diff between expected and actual output."""
    exp_norm = normalize_output(expected)
    act_norm = normalize_output(actual)
    
    print("--- Expected ---")
    print(exp_norm)
    print("--- Actual   ---")
    print(act_norm)


def get_python_exe() -> str:
    """Get current Python executable path."""
    return sys.executable


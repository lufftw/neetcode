# runner/utils/compare.py
"""
Output Comparison Utilities.

Provides different comparison modes for validating solution outputs:
- exact: Exact string match
- sorted: Sort before comparison (for "return in any order" problems)
- set: Set comparison (for unique elements, order doesn't matter)
- JUDGE_FUNC: Custom validation function
"""
import ast
from typing import Optional, Any


def normalize_output(s: str) -> str:
    """Normalize output by removing trailing whitespace and extra newlines."""
    lines = s.strip().splitlines()
    lines = [line.rstrip() for line in lines]
    return "\n".join(lines)


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


def _compare_sorted(actual: Any, expected: Any) -> bool:
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


def _compare_set(actual: Any, expected: Any) -> bool:
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


def compare_result(actual_str: str, expected_str: Optional[str], input_str: str,
                   module: Any, compare_mode: str = "exact") -> bool:
    """
    Integrated comparison logic supporting JUDGE_FUNC and COMPARE_MODE.
    
    Priority:
        1. JUDGE_FUNC (user-defined validation function)
        2. COMPARE_MODE (framework-provided: exact/sorted/set)
    
    Args:
        actual_str: Actual program output (raw string)
        expected_str: Expected output (raw string, or None if .out doesn't exist)
        input_str: Input data (raw string)
        module: Loaded solution module
        compare_mode: Comparison mode ("exact" | "sorted" | "set")
    
    Returns:
        bool: Whether the answer is correct
    
    JUDGE_FUNC Signature:
        def judge(actual, expected, input_data) -> bool
        
        - If actual/expected can be parsed by ast.literal_eval, pass parsed objects
        - If parsing fails, pass raw strings
        - expected is None when .out file doesn't exist (judge-only mode)
        - input_data is always raw string
    """
    actual_norm = normalize_output(actual_str)
    expected_norm = normalize_output(expected_str) if expected_str is not None else None
    
    # ========== Priority 1: JUDGE_FUNC ==========
    judge_func = getattr(module, 'JUDGE_FUNC', None) if module else None
    
    if judge_func:
        # Try to parse actual as Python object
        try:
            actual_obj = ast.literal_eval(actual_norm)
        except (ValueError, SyntaxError):
            actual_obj = actual_norm
        
        # Try to parse expected as Python object (if exists)
        if expected_norm is not None:
            try:
                expected_obj = ast.literal_eval(expected_norm)
            except (ValueError, SyntaxError):
                expected_obj = expected_norm
        else:
            # No .out file -> expected is None (judge-only mode)
            expected_obj = None
        
        return judge_func(actual_obj, expected_obj, input_str)
    
    # ========== Priority 2: COMPARE_MODE ==========
    # COMPARE_MODE requires .out file
    if expected_norm is None:
        # This shouldn't happen if test_runner handles it correctly
        return False
    
    return compare_outputs(actual_norm, expected_norm, compare_mode)


__all__ = [
    'normalize_output',
    'compare_outputs',
    'compare_result',
    '_compare_sorted',
    '_compare_set',
]


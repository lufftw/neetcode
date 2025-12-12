# runner/util.py
"""
Common Utilities for Test Runner.

This module re-exports utilities from submodules for backward compatibility.
New code should import directly from the specific submodules:
    - runner.compare: Output comparison functions
    - runner.paths: Path helper functions
    - runner.io_utils: File I/O operations
"""
import os
import inspect
import warnings
from typing import Any, Dict


def get_solver(solutions_meta: Dict[str, Any]) -> Any:
    """
    Get the solver instance for the currently selected solution method.
    
    Automatically reads SOLUTION_METHOD from environment and returns
    the appropriate class instance. Uses inspect to auto-capture caller's
    globals, so no need to pass globals() explicitly.
    
    Args:
        solutions_meta: The SOLUTIONS dictionary from the solution file
    
    Returns:
        An instance of the selected solution class
    
    Example:
        from runner.util import get_solver
        
        def solve():
            solver = get_solver(SOLUTIONS)
            result = solver.twoSum(nums, target)  # Natural LeetCode-style call
            print(result)
    """
    # Auto-capture caller's globals (no need to pass explicitly)
    caller_globals = inspect.currentframe().f_back.f_globals
    
    method_key = os.environ.get('SOLUTION_METHOD', 'default')
    info = solutions_meta.get(method_key, solutions_meta['default'])
    
    return caller_globals[info['class']]()


def get_solution_info(solutions_meta: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get the solution info for the currently selected method.
    
    Useful when you need access to the info dict (e.g., for logging).
    
    Args:
        solutions_meta: The SOLUTIONS dictionary from the solution file
    
    Returns:
        The info dict for the selected method (contains 'class', 'method', etc.)
    
    Example:
        info = get_solution_info(SOLUTIONS)
        print(f"Running: {info['class']}.{info['method']}")
    """
    method_key = os.environ.get('SOLUTION_METHOD', 'default')
    return solutions_meta.get(method_key, solutions_meta['default'])


def invoke_solution(solutions_meta: Dict[str, Any], caller_globals: Dict[str, Any], *args, **kwargs) -> Any:
    """
    [DEPRECATED] Use get_solver() instead for better readability.
    
    Example migration:
        # Before (deprecated)
        result = invoke_solution(SOLUTIONS, globals(), nums, val)
        
        # After (recommended)
        solver = get_solver(SOLUTIONS)
        result = solver.removeElement(nums, val)
    """
    warnings.warn(
        "invoke_solution() is deprecated. Use get_solver() instead:\n"
        "  solver = get_solver(SOLUTIONS)\n"
        "  result = solver.methodName(args)",
        DeprecationWarning,
        stacklevel=2
    )
    
    method_key = os.environ.get('SOLUTION_METHOD', 'default')
    info = solutions_meta.get(method_key, solutions_meta['default'])
    
    solver = caller_globals[info['class']]()
    method = getattr(solver, info['method'])
    return method(*args, **kwargs)


# Re-export from compare.py
from runner.compare import (
    normalize_output,
    compare_outputs,
    compare_result,
    _compare_sorted,
    _compare_set,
)

# Re-export from paths.py
from runner.paths import (
    PROJECT_ROOT,
    SOLUTIONS_DIR,
    TESTS_DIR,
    TEMPLATES_DIR,
    get_solution_path,
    get_test_input_path,
    get_test_output_path,
)

# Re-export from io_utils.py
from runner.io_utils import (
    read_file,
    write_file,
    file_exists,
    print_diff,
    get_python_exe,
)

# Define __all__ for explicit exports
__all__ = [
    # polymorphic invocation
    'get_solver',
    'get_solution_info',
    'invoke_solution',  # deprecated, kept for backward compatibility
    # compare
    'normalize_output',
    'compare_outputs',
    'compare_result',
    '_compare_sorted',
    '_compare_set',
    # paths
    'PROJECT_ROOT',
    'SOLUTIONS_DIR',
    'TESTS_DIR',
    'TEMPLATES_DIR',
    'get_solution_path',
    'get_test_input_path',
    'get_test_output_path',
    # io_utils
    'read_file',
    'write_file',
    'file_exists',
    'print_diff',
    'get_python_exe',
]

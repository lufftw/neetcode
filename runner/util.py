# runner/util.py
"""
Common Utilities for Test Runner.

This module re-exports utilities from submodules for backward compatibility.
New code should import directly from the specific submodules:
    - runner.compare: Output comparison functions
    - runner.paths: Path helper functions
    - runner.io_utils: File I/O operations
"""

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

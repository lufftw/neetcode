# runner/utils/__init__.py
"""
Utility modules for the test runner.

Provides common utilities for module loading, output comparison,
solution parsing, and path handling.
"""
from runner.utils.loader import load_solution_module, load_generator_module
from runner.utils.compare import compare_result, normalize_output
from runner.utils.parser import (
    parse_class_headers,
    get_approach_info,
    build_method_mapping,
)
from runner.utils.paths import (
    PROJECT_ROOT,
    SOLUTIONS_DIR,
    TESTS_DIR,
    get_project_root,
    get_solutions_dir,
    get_tests_dir,
    get_solution_path,
)

__all__ = [
    # loader
    'load_solution_module',
    'load_generator_module',
    # compare
    'compare_result',
    'normalize_output',
    # parser
    'parse_class_headers',
    'get_approach_info',
    'build_method_mapping',
    # paths
    'PROJECT_ROOT',
    'SOLUTIONS_DIR',
    'TESTS_DIR',
    'get_project_root',
    'get_solutions_dir',
    'get_tests_dir',
    'get_solution_path',
]


# runner/utils/paths.py
"""
Path Utilities for Test Runner.

Provides helper functions for constructing file paths.
"""
import os
from typing import Optional

# Project root directory (runner/utils/paths.py -> runner/utils -> runner -> project_root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Default directories
SOLUTIONS_DIR = os.path.join(PROJECT_ROOT, "solutions")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
GENERATORS_DIR = os.path.join(PROJECT_ROOT, "generators")
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "templates")


def get_project_root() -> str:
    """Get project root directory."""
    return PROJECT_ROOT


def get_solutions_dir() -> str:
    """Get solutions directory."""
    return SOLUTIONS_DIR


def get_tests_dir() -> str:
    """Get tests directory."""
    return TESTS_DIR


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


__all__ = [
    'PROJECT_ROOT',
    'SOLUTIONS_DIR',
    'TESTS_DIR',
    'GENERATORS_DIR',
    'TEMPLATES_DIR',
    'get_project_root',
    'get_solutions_dir',
    'get_tests_dir',
    'get_solution_path',
    'get_test_input_path',
    'get_test_output_path',
]


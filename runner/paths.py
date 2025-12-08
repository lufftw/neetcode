# runner/paths.py
"""
Path Utilities for Test Runner.

Provides helper functions for constructing file paths.
"""
import os
from typing import Optional

# Project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default directories
SOLUTIONS_DIR = os.path.join(PROJECT_ROOT, "solutions")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "templates")


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


# runner/core/__init__.py
"""
Core execution modules for the test runner.

Provides:
- Single case execution (executor)
- Method-level test orchestration (method_runner)
"""
from runner.core.executor import (
    PYTHON_EXE,
    run_one_case,
    run_generated_case,
)
from runner.core.method_runner import (
    run_method_tests,
    run_legacy_tests,
)

__all__ = [
    # executor
    'PYTHON_EXE',
    'run_one_case',
    'run_generated_case',
    # method_runner
    'run_method_tests',
    'run_legacy_tests',
]


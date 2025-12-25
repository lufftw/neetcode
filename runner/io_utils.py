# runner/io_utils.py
"""
I/O Utilities for Test Runner.

Provides file read/write operations and output formatting.
"""
import os
import sys


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


def print_diff(expected: str, actual: str) -> None:
    """Print diff between expected and actual output."""
    from runner.utils.compare import normalize_output
    
    exp_norm = normalize_output(expected)
    act_norm = normalize_output(actual)
    
    print("--- Expected ---")
    print(exp_norm)
    print("--- Actual   ---")
    print(act_norm)


def get_python_exe() -> str:
    """Get current Python executable path."""
    return sys.executable


# runner/display/reporter.py
"""
Core Reporter - Basic formatting and utility functions for test output.

Provides:
- Input truncation for display
- Validation mode labels
- Failed case saving
- Unicode support detection
"""
import sys
import os
from typing import List, Dict, Any, Optional


def supports_unicode() -> bool:
    """Check if terminal supports Unicode box-drawing characters."""
    try:
        encoding = sys.stdout.encoding or 'utf-8'
        for char in '═║╔╗╚╝╠╣█░':
            char.encode(encoding)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


def get_box_chars() -> dict:
    """Get appropriate box-drawing characters based on terminal support."""
    u = supports_unicode()
    return {
        'TL': '╔' if u else '+',
        'TR': '╗' if u else '+',
        'BL': '╚' if u else '+',
        'BR': '╝' if u else '+',
        'H': '═' if u else '=',
        'V': '║' if u else '|',
        'ML': '╠' if u else '+',
        'MR': '╣' if u else '+',
        'BAR_FULL': '█' if u else '#',
        'BAR_EMPTY': '░' if u else '.',
        'ARROW': '→' if u else '->',
    }


def truncate_input(input_data: str, max_length: int = 200) -> str:
    """Truncate long input for display."""
    if len(input_data) <= max_length:
        return input_data
    return input_data[:max_length] + f"... ({len(input_data)} chars)"


def format_validation_label(validation_mode: str) -> str:
    """Format validation mode as a label."""
    return f"[{validation_mode}]"


def save_failed_case(problem: str, input_data: str, tests_dir: str) -> str:
    """Save a failed generated case to tests/ folder."""
    n = 1
    while os.path.exists(os.path.join(tests_dir, f"{problem}_failed_{n}.in")):
        n += 1
    filepath = os.path.join(tests_dir, f"{problem}_failed_{n}.in")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(input_data if input_data.endswith('\n') else input_data + '\n')
    return filepath


__all__ = [
    'supports_unicode',
    'get_box_chars',
    'truncate_input',
    'format_validation_label',
    'save_failed_case',
]


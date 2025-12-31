"""
Practice Workspace - Stateful management of practice files.

This package manages:
    - Practice file history (_history/ directory)
    - History listing and restore operations

Usage:
    from packages.practice_workspace import (
        save_to_history,
        list_history,
        restore_from_history,
    )
    
    # Save current practice to history
    history_path = save_to_history(practice_path)
    
    # List all history versions
    versions = list_history(problem_id)
    
    # Restore a specific version
    restore_from_history(problem_id, timestamp="20251231_143022")
"""

from .history import (
    save_to_history,
    list_history,
    get_history_entries,
    HistoryEntry,
)
from .restore import (
    restore_from_history,
    restore_latest,
)
from .utils import (
    get_practice_path,
    get_history_dir,
    parse_timestamp,
    format_relative_time,
)

__all__ = [
    # History operations
    "save_to_history",
    "list_history",
    "get_history_entries",
    "HistoryEntry",
    # Restore operations
    "restore_from_history",
    "restore_latest",
    # Utilities
    "get_practice_path",
    "get_history_dir",
    "parse_timestamp",
    "format_relative_time",
]


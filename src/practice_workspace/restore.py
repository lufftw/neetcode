"""
Practice history restore operations.

Handles restoring practice files from history.
"""

from pathlib import Path
from typing import Optional

from .history import (
    get_history_entries,
    get_latest_history,
    get_history_by_timestamp,
    get_history_by_index,
    save_to_history,
    HistoryEntry,
)
from .utils import get_practice_path


class RestoreResult:
    """Result of a restore operation."""
    
    def __init__(
        self,
        success: bool,
        message: str,
        restored_from: Optional[HistoryEntry] = None,
        practice_path: Optional[Path] = None,
    ):
        self.success = success
        self.message = message
        self.restored_from = restored_from
        self.practice_path = practice_path
    
    def __repr__(self) -> str:
        return f"RestoreResult(success={self.success})"


def restore_from_history(
    problem_id: int,
    timestamp: Optional[str] = None,
    index: Optional[int] = None,
    save_current: bool = True,
) -> RestoreResult:
    """
    Restore a practice file from history.
    
    Args:
        problem_id: LeetCode frontend question ID
        timestamp: Specific timestamp to restore (YYYYMMDD_HHMMSS)
        index: 1-based index from history listing
        save_current: Save current practice to history before restoring
        
    Returns:
        RestoreResult with success status and details
        
    Note:
        If neither timestamp nor index is provided, restores the latest.
    """
    # Find the entry to restore
    entry: Optional[HistoryEntry] = None
    
    if timestamp:
        entry = get_history_by_timestamp(problem_id, timestamp)
        if not entry:
            return RestoreResult(
                success=False,
                message=f"History entry not found for timestamp: {timestamp}",
            )
    elif index:
        entry = get_history_by_index(problem_id, index)
        if not entry:
            entries = get_history_entries(problem_id)
            return RestoreResult(
                success=False,
                message=f"Invalid index {index}. Valid range: 1-{len(entries)}",
            )
    else:
        # Default to latest
        entry = get_latest_history(problem_id)
        if not entry:
            return RestoreResult(
                success=False,
                message=f"No history found for problem {problem_id}",
            )
    
    # Get practice path
    practice_path = get_practice_path(problem_id)
    
    # Save current if requested and file exists
    if save_current and practice_path.exists():
        save_to_history(practice_path)
    
    # Restore from history
    content = entry.path.read_text(encoding="utf-8")
    
    # Ensure parent directory exists
    practice_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write restored content
    practice_path.write_text(content, encoding="utf-8")
    
    return RestoreResult(
        success=True,
        message=f"✅ Restored: {practice_path}\n   (from: {entry.timestamp_str})",
        restored_from=entry,
        practice_path=practice_path,
    )


def restore_latest(
    problem_id: int,
    save_current: bool = True,
) -> RestoreResult:
    """
    Restore the latest history version.
    
    Args:
        problem_id: LeetCode frontend question ID
        save_current: Save current practice to history before restoring
        
    Returns:
        RestoreResult with success status and details
    """
    return restore_from_history(
        problem_id,
        timestamp=None,
        index=None,
        save_current=save_current,
    )


def interactive_restore(problem_id: int) -> RestoreResult:
    """
    Interactive restore - prompts user to select version.
    
    Args:
        problem_id: LeetCode frontend question ID
        
    Returns:
        RestoreResult with success status and details
    """
    from .history import list_history
    
    entries = get_history_entries(problem_id)
    
    if not entries:
        return RestoreResult(
            success=False,
            message=f"No history found for problem {problem_id}",
        )
    
    # Print history listing
    print(list_history(problem_id))
    print()
    
    # Prompt for selection
    default = len(entries)
    try:
        selection = input(f"Select version to restore [{default}]: ").strip()
        
        if not selection:
            index = default
        else:
            index = int(selection)
    except (ValueError, EOFError):
        return RestoreResult(
            success=False,
            message="Invalid selection",
        )
    
    return restore_from_history(problem_id, index=index)


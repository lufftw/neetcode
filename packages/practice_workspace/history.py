"""
Practice history management.

Handles saving practice files to history and listing history entries.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .utils import (
    get_history_dir,
    get_practice_stem,
    parse_timestamp,
    format_relative_time,
    extract_timestamp_from_backup,
    generate_backup_filename,
)


@dataclass
class HistoryEntry:
    """A history entry for a practice file."""
    
    path: Path
    timestamp: datetime
    timestamp_str: str
    relative_time: str
    index: int  # 1-based index for display
    
    def __repr__(self) -> str:
        return f"HistoryEntry(timestamp={self.timestamp_str}, path={self.path.name})"


def save_to_history(
    practice_path: Path,
    timestamp: Optional[datetime] = None,
) -> Path:
    """
    Save a practice file to history.
    
    Args:
        practice_path: Path to the practice file to save
        timestamp: Optional timestamp (default: now)
        
    Returns:
        Path to the saved history file
    """
    if not practice_path.exists():
        raise FileNotFoundError(f"Practice file not found: {practice_path}")
    
    # Ensure history directory exists
    history_dir = get_history_dir()
    history_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate backup filename
    backup_name = generate_backup_filename(practice_path.name, timestamp)
    history_path = history_dir / backup_name
    
    # Copy content
    content = practice_path.read_text(encoding="utf-8")
    history_path.write_text(content, encoding="utf-8")
    
    return history_path


def get_history_entries(problem_id: int) -> List[HistoryEntry]:
    """
    Get all history entries for a problem.
    
    Args:
        problem_id: LeetCode frontend question ID
        
    Returns:
        List of HistoryEntry objects, sorted oldest to newest
    """
    history_dir = get_history_dir()
    
    if not history_dir.exists():
        return []
    
    stem = get_practice_stem(problem_id)
    pattern = f"{stem}.py.*.bak"
    
    entries = []
    for path in history_dir.glob(pattern):
        timestamp_str = extract_timestamp_from_backup(path.name)
        if timestamp_str:
            timestamp = parse_timestamp(timestamp_str)
            if timestamp:
                entries.append(HistoryEntry(
                    path=path,
                    timestamp=timestamp,
                    timestamp_str=timestamp_str,
                    relative_time=format_relative_time(timestamp),
                    index=0,  # Will be set after sorting
                ))
    
    # Sort oldest to newest
    entries.sort(key=lambda e: e.timestamp)
    
    # Assign indices (1-based)
    for i, entry in enumerate(entries, 1):
        entry.index = i
    
    return entries


def list_history(problem_id: int) -> str:
    """
    List history for a problem in human-readable format.
    
    Args:
        problem_id: LeetCode frontend question ID
        
    Returns:
        Formatted history listing string
    """
    entries = get_history_entries(problem_id)
    stem = get_practice_stem(problem_id)
    
    if not entries:
        return f"No history found for {stem}"
    
    lines = [f"Practice history for {stem}:", ""]
    
    for entry in entries:
        marker = " ← latest" if entry.index == len(entries) else ""
        lines.append(
            f"  [{entry.index}] {entry.timestamp_str}  ({entry.relative_time}){marker}"
        )
    
    lines.append("")
    lines.append(f"Total: {len(entries)} version{'s' if len(entries) != 1 else ''}")
    
    return "\n".join(lines)


def get_latest_history(problem_id: int) -> Optional[HistoryEntry]:
    """
    Get the most recent history entry for a problem.
    
    Args:
        problem_id: LeetCode frontend question ID
        
    Returns:
        Latest HistoryEntry, or None if no history
    """
    entries = get_history_entries(problem_id)
    return entries[-1] if entries else None


def get_history_by_timestamp(
    problem_id: int,
    timestamp_str: str,
) -> Optional[HistoryEntry]:
    """
    Get a specific history entry by timestamp.
    
    Args:
        problem_id: LeetCode frontend question ID
        timestamp_str: Timestamp string (YYYYMMDD_HHMMSS)
        
    Returns:
        HistoryEntry if found, None otherwise
    """
    entries = get_history_entries(problem_id)
    
    for entry in entries:
        if entry.timestamp_str == timestamp_str:
            return entry
    
    return None


def get_history_by_index(
    problem_id: int,
    index: int,
) -> Optional[HistoryEntry]:
    """
    Get a history entry by its 1-based index.
    
    Args:
        problem_id: LeetCode frontend question ID
        index: 1-based index from history listing
        
    Returns:
        HistoryEntry if found, None otherwise
    """
    entries = get_history_entries(problem_id)
    
    if 1 <= index <= len(entries):
        return entries[index - 1]
    
    return None


def clear_history(problem_id: int) -> int:
    """
    Clear all history for a problem.
    
    Args:
        problem_id: LeetCode frontend question ID
        
    Returns:
        Number of entries deleted
    """
    entries = get_history_entries(problem_id)
    
    count = 0
    for entry in entries:
        try:
            entry.path.unlink()
            count += 1
        except OSError:
            pass
    
    return count


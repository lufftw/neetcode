"""
Practice Workspace utilities.

Common utilities for history and restore operations.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


def get_practice_dir() -> Path:
    """Get the practices directory path."""
    from codegen.core.config import load_config
    config = load_config()
    return config.practices_path


def get_history_dir() -> Path:
    """Get the practice history directory path."""
    from codegen.core.config import load_config
    config = load_config()
    return config.history_path


def get_practice_path(problem_id: int) -> Path:
    """
    Get the practice file path for a problem.
    
    Args:
        problem_id: LeetCode frontend question ID
        
    Returns:
        Path to the practice file
    """
    from codegen.practice.generator import get_practice_path as _get_path
    return _get_path(problem_id)


def get_practice_stem(problem_id: int) -> str:
    """
    Get the practice file stem (filename without extension).
    
    Args:
        problem_id: LeetCode frontend question ID
        
    Returns:
        File stem (e.g., "0001_two_sum")
    """
    from leetcode_datasource import LeetCodeDataSource
    
    ds = LeetCodeDataSource()
    slug = ds.get_slug(problem_id)
    
    if slug:
        slug = slug.replace("-", "_")
        return f"{problem_id:04d}_{slug}"
    
    return f"{problem_id:04d}_unknown"


def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
    """
    Parse a timestamp string to datetime.
    
    Args:
        timestamp_str: Timestamp in format "YYYYMMDD_HHMMSS"
        
    Returns:
        datetime object, or None if parsing fails
    """
    try:
        return datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
    except ValueError:
        return None


def format_timestamp(dt: datetime) -> str:
    """
    Format a datetime to timestamp string.
    
    Args:
        dt: datetime object
        
    Returns:
        Timestamp string in format "YYYYMMDD_HHMMSS"
    """
    return dt.strftime("%Y%m%d_%H%M%S")


def format_relative_time(dt: datetime) -> str:
    """
    Format datetime as relative time string.
    
    Args:
        dt: datetime object
        
    Returns:
        Human-readable relative time (e.g., "2 hours ago")
    """
    now = datetime.now()
    delta = now - dt
    
    if delta < timedelta(minutes=1):
        return "just now"
    elif delta < timedelta(hours=1):
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif delta < timedelta(days=1):
        hours = int(delta.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif delta < timedelta(days=30):
        days = delta.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif delta < timedelta(days=365):
        months = delta.days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = delta.days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"


def extract_timestamp_from_backup(filename: str) -> Optional[str]:
    """
    Extract timestamp from backup filename.
    
    Args:
        filename: Backup filename (e.g., "0001_two_sum.py.20251231_143022.bak")
        
    Returns:
        Timestamp string, or None if not found
    """
    import re
    
    # Pattern: stem.timestamp.bak
    match = re.search(r'\.(\d{8}_\d{6})\.bak$', filename)
    if match:
        return match.group(1)
    return None


def generate_backup_filename(filename: str, timestamp: Optional[datetime] = None) -> str:
    """
    Generate backup filename.
    
    Args:
        filename: Original filename with extension (e.g., "0001_two_sum.py")
        timestamp: datetime for backup (default: now)
        
    Returns:
        Backup filename (e.g., "0001_two_sum.py.20251231_143022.bak")
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    ts_str = format_timestamp(timestamp)
    return f"{filename}.{ts_str}.bak"


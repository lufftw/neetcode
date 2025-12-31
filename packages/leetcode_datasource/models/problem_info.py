"""
ProblemInfo data model for problem_index table.

This is a minimal metadata model for quick ID lookups and basic info.
For full question data, use the Question model.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ProblemInfo:
    """Minimal problem metadata from problem_index table.
    
    This model stores data from LeetCode's /api/problems/all/ endpoint.
    Used for:
        - ID resolution (frontend_id ↔ slug)
        - Quick metadata lookups (title, difficulty, etc.)
        - Checking if a problem is paid-only before fetching
    
    Note: This is NOT the full question data. Use Question for that.
    """
    
    # === Primary Keys ===
    frontend_question_id: int           # Problem number on website (1, 2, 922...)
    title_slug: str                     # URL slug ("two-sum")
    
    # === Secondary ID ===
    question_id: Optional[int] = None   # LeetCode internal ID (may be None)
    
    # === Basic Metadata ===
    title: str = ""                     # "Two Sum"
    difficulty: str = ""                # "Easy", "Medium", "Hard"
    difficulty_level: int = 0           # 1, 2, 3
    paid_only: bool = False             # True if premium-only
    url: str = ""                       # Full LeetCode URL
    
    # === Statistics ===
    total_acs: int = 0                  # Total accepted submissions
    total_submitted: int = 0            # Total submissions
    is_new_question: bool = False       # Marked as new on LeetCode
    
    # === Cache Metadata ===
    updated_at: Optional[str] = None    # ISO 8601 timestamp
    
    def __repr__(self) -> str:
        return (
            f"ProblemInfo(frontend_id={self.frontend_question_id}, "
            f"slug='{self.title_slug}', title='{self.title}', "
            f"difficulty='{self.difficulty}')"
        )
    
    @property
    def acceptance_rate(self) -> float:
        """Calculate acceptance rate from submission stats."""
        if self.total_submitted == 0:
            return 0.0
        return (self.total_acs / self.total_submitted) * 100


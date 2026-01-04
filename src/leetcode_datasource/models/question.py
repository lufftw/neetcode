"""
Question data model for LeetCode problems.

Field names follow LeetScrape convention for compatibility.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Question:
    """LeetCode question data model.
    
    Field names follow LeetScrape convention for compatibility.
    
    Primary lookup keys:
        - titleSlug: URL slug (e.g., "two-sum")
        - frontend_question_id: Problem number on website (e.g., 1, 922)
    
    Note: QID (internal question_id) is stored for reference but NOT exposed
    as a lookup interface since it's LeetCode's internal ID.
    """
    
    # === Required Fields ===
    QID: int                              # Internal question ID (for reference only)
    frontend_question_id: int             # Problem number shown on website (1, 2, 922...)
    title: str                            # "Two Sum"
    titleSlug: str                        # "two-sum"
    difficulty: str                       # "Easy", "Medium", "Hard"
    
    # === Content Fields ===
    Body: str = ""                        # HTML problem description
    Code: str = ""                        # Code template/stubs
    Hints: List[str] = field(default_factory=list)
    
    # === Metadata Fields ===
    acceptanceRate: float = 0.0
    topicTags: str = ""                   # Comma-separated: "array,hash-table"
    categorySlug: str = ""                # "algorithms", "database", etc.
    isPaidOnly: bool = False
    
    # === Relationship Fields ===
    SimilarQuestions: List[int] = field(default_factory=list)
    Companies: Optional[List[str]] = None
    
    # === Cache Metadata (Internal) ===
    _schema_version: str = "1.0"
    _cached_at: Optional[str] = None
    _from_cache: bool = False
    
    def __repr__(self) -> str:
        return (
            f"Question(frontend_id={self.frontend_question_id}, "
            f"slug='{self.titleSlug}', title='{self.title}', "
            f"difficulty='{self.difficulty}')"
        )


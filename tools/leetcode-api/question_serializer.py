#!/usr/bin/env python3
"""
Question Serializer - Convert between LeetScrape Question and storage format.

This module handles bidirectional conversion:
    - Question object → Dict (for SQLite storage)
    - Dict (from SQLite) → Question-compatible object

Design Principle:
    The deserialized object MUST be API-compatible with LeetScrape's Question,
    so callers don't need to know if data came from network or local cache.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class Question:
    """
    Question object compatible with LeetScrape's Question class.
    
    This class mirrors the LeetScrape Question interface, allowing
    code to work seamlessly with both network-fetched and cached data.
    
    Schema matches LeetScrape JSON format:
    https://raw.githubusercontent.com/nikhil-ravi/LeetScrape/refs/heads/main/example/data/all.json
    
    Attributes:
        - QID: Question ID (int, e.g., 1)
        - title: Problem title (e.g., "Two Sum")
        - titleSlug: URL slug (e.g., "two-sum")
        - difficulty: "Easy", "Medium", or "Hard"
        - acceptanceRate: Acceptance rate as float
        - paidOnly: Whether question requires premium (bool)
        - topicTags: Comma-separated tags (str, e.g., "array,hash-table")
        - categorySlug: Category (e.g., "algorithms")
        - Hints: List of hint strings
        - Companies: List of company names or None
        - SimilarQuestions: List of QIDs (int)
        - Code: Code template string (not dict!)
        - Body: HTML problem description
        - isPaidOnly: Same as paidOnly (for compatibility)
    """
    QID: int = 0
    title: str = ""
    titleSlug: str = ""
    difficulty: str = ""
    acceptanceRate: float = 0.0
    paidOnly: bool = False
    topicTags: str = ""
    categorySlug: str = ""
    Hints: List[str] = field(default_factory=list)
    Companies: Optional[List[str]] = None
    SimilarQuestions: List[int] = field(default_factory=list)
    Code: str = ""
    Body: str = ""
    isPaidOnly: bool = False
    
    # Additional metadata (not in original LeetScrape, but useful)
    _from_cache: bool = field(default=False, repr=False)
    _cached_at: Optional[str] = field(default=None, repr=False)


class QuestionSerializer:
    """
    Serializer for converting between Question objects and storage format.
    
    Schema matches LeetScrape JSON format:
    https://raw.githubusercontent.com/nikhil-ravi/LeetScrape/refs/heads/main/example/data/all.json
    
    This class is responsible for:
        1. Converting LeetScrape Question → Dict (for storage)
        2. Converting Dict (from storage) → Question-compatible object
    """
    
    @staticmethod
    def from_leetscrape(q: Any) -> Dict[str, Any]:
        """
        Convert a LeetScrape Question object to storage dictionary.
        
        Args:
            q: LeetScrape Question object (from GetQuestion.scrape())
            
        Returns:
            Dictionary suitable for QuestionStore.save()
        """
        # Extract hints (list of strings)
        hints = []
        if hasattr(q, 'Hints') and q.Hints:
            hints = q.Hints if isinstance(q.Hints, list) else []
        
        # Extract companies (list or None)
        companies = None
        if hasattr(q, 'Companies') and q.Companies:
            companies = q.Companies if isinstance(q.Companies, list) else None
        
        # Extract similar questions (list of int QIDs)
        similar = []
        if hasattr(q, 'SimilarQuestions') and q.SimilarQuestions:
            similar = q.SimilarQuestions if isinstance(q.SimilarQuestions, list) else []
        
        # topicTags is a comma-separated string in LeetScrape, not a list
        topic_tags = ''
        if hasattr(q, 'topicTags') and q.topicTags:
            topic_tags = q.topicTags if isinstance(q.topicTags, str) else ''
        
        # Code is a string in LeetScrape, not a dict
        code = ''
        if hasattr(q, 'Code') and q.Code:
            code = q.Code if isinstance(q.Code, str) else ''
        
        return {
            'qid': int(getattr(q, 'QID', 0) or 0),
            'title': getattr(q, 'title', '') or '',
            'title_slug': getattr(q, 'titleSlug', '') or '',
            'difficulty': getattr(q, 'difficulty', '') or '',
            'acceptance_rate': float(getattr(q, 'acceptanceRate', 0.0) or 0.0),
            'paid_only': bool(getattr(q, 'paidOnly', False)),
            'topic_tags': topic_tags,
            'category_slug': getattr(q, 'categorySlug', '') or '',
            'hints': hints,
            'companies': companies,
            'similar_questions': similar,
            'code': code,
            'body': getattr(q, 'Body', '') or '',
            'is_paid_only': bool(getattr(q, 'isPaidOnly', False)),
        }
    
    @staticmethod
    def to_question(data: Dict[str, Any]) -> Question:
        """
        Convert a storage dictionary to a Question object.
        
        The returned Question object is API-compatible with LeetScrape's Question,
        allowing transparent use in code that expects LeetScrape objects.
        
        Args:
            data: Dictionary from QuestionStore.get_by_slug() or similar
            
        Returns:
            Question object with same interface as LeetScrape Question
        """
        return Question(
            QID=int(data.get('qid', 0)),
            title=data.get('title', ''),
            titleSlug=data.get('title_slug', ''),
            difficulty=data.get('difficulty', ''),
            acceptanceRate=float(data.get('acceptance_rate', 0.0)),
            paidOnly=bool(data.get('paid_only', False)),
            topicTags=data.get('topic_tags', ''),
            categorySlug=data.get('category_slug', ''),
            Hints=data.get('hints', []),
            Companies=data.get('companies'),  # Can be None
            SimilarQuestions=data.get('similar_questions', []),
            Code=data.get('code', ''),
            Body=data.get('body', ''),
            isPaidOnly=bool(data.get('is_paid_only', False)),
            _from_cache=True,
            _cached_at=data.get('updated_at'),
        )
    
    @staticmethod
    def is_valid(data: Dict[str, Any]) -> bool:
        """
        Check if storage data is valid and complete.
        
        Args:
            data: Dictionary from QuestionStore
            
        Returns:
            True if data contains required fields
        """
        required = ['title_slug', 'title', 'body']
        return all(data.get(field) for field in required)


# Convenience functions
def serialize(question: Any) -> Dict[str, Any]:
    """Serialize a LeetScrape Question to storage format."""
    return QuestionSerializer.from_leetscrape(question)


def deserialize(data: Dict[str, Any]) -> Question:
    """Deserialize storage data to a Question object."""
    return QuestionSerializer.to_question(data)


if __name__ == "__main__":
    # Test with mock data matching LeetScrape format
    test_data = {
        'qid': 1,
        'title': 'Two Sum',
        'title_slug': 'two-sum',
        'difficulty': 'Easy',
        'acceptance_rate': 50.15,
        'paid_only': False,
        'topic_tags': 'array,hash-table',
        'category_slug': 'algorithms',
        'hints': ['Try using a hash map'],
        'companies': None,
        'similar_questions': [15, 18, 167],
        'code': 'class Solution:\n    def twoSum(self, nums, target):',
        'body': '<p>Given an array of integers...</p>',
        'is_paid_only': False,
        'updated_at': '2025-01-01T00:00:00',
    }
    
    q = deserialize(test_data)
    print(f"Question: {q.title} ({q.titleSlug})")
    print(f"Difficulty: {q.difficulty}")
    print(f"QID: {q.QID}")
    print(f"Acceptance Rate: {q.acceptanceRate}%")
    print(f"Topic Tags: {q.topicTags}")
    print(f"Category: {q.categorySlug}")
    print(f"Similar Questions: {q.SimilarQuestions}")
    print(f"From cache: {q._from_cache}")


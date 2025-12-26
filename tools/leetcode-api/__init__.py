"""
LeetCode API - Local cache and API for LeetCode question data.

This package provides:
    - SQLite-backed question storage
    - Transparent caching with LeetScrape fallback
    - Question objects compatible with LeetScrape

Usage:
    from tools.leetcode_api import get_question
    
    q = get_question("two-sum")
    print(q.title)       # "Two Sum"
    print(q.difficulty)  # "Easy"
    print(q.Body)        # HTML problem description
"""

from .question_api import (
    get_question,
    get_question_by_id,
    get_default_api,
    QuestionAPI,
)
from .question_serializer import (
    Question,
    QuestionSerializer,
    serialize,
    deserialize,
)
from .question_store import (
    QuestionStore,
    get_default_store,
)

__all__ = [
    # API
    'get_question',
    'get_question_by_id',
    'get_default_api',
    'QuestionAPI',
    # Serializer
    'Question',
    'QuestionSerializer',
    'serialize',
    'deserialize',
    # Store
    'QuestionStore',
    'get_default_store',
]


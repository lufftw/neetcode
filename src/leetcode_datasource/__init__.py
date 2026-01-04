"""
LeetCode DataSource - Unified data layer for LeetCode questions.

This package provides:
    - Question data model
    - Cache and persistent storage
    - Pluggable network fetcher (default: LeetScrape)

Usage:
    from leetcode_datasource import LeetCodeDataSource
    
    ds = LeetCodeDataSource()
    q = ds.get_by_slug("two-sum")
    print(q.title)  # "Two Sum"
    
    q = ds.get_by_frontend_id(1)
    print(q.titleSlug)  # "two-sum"
"""

from .datasource import LeetCodeDataSource
from .config import DataSourceConfig
from .models.question import Question
from .models.problem_info import ProblemInfo
from .exceptions import (
    LeetCodeDataSourceError,
    QuestionNotFoundError,
    NetworkError,
    ParseError,
    ConfigError,
)

__all__ = [
    # Main class
    "LeetCodeDataSource",
    "DataSourceConfig",
    # Data models
    "Question",
    "ProblemInfo",
    # Exceptions
    "LeetCodeDataSourceError",
    "QuestionNotFoundError",
    "NetworkError",
    "ParseError",
    "ConfigError",
]


# tools/mindmaps/post_processing.py
"""Post-processing for mindmap content - adds LeetCode and Solution links.

This module re-exports all post-processing functions and classes from core.post_processing
to maintain backward compatibility with existing imports.
"""

# Re-export everything from core.post_processing
from .core.post_processing import (
    get_datasource,
    load_leetcode_cache,
    _get_problem_info_from_datasource,
    merge_leetcode_api_data,
    PostProcessor,
    post_process_content,
)

__all__ = [
    "get_datasource",
    "load_leetcode_cache",
    "_get_problem_info_from_datasource",
    "merge_leetcode_api_data",
    "PostProcessor",
    "post_process_content",
]


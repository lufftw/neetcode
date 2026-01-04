# tools/mindmaps/link_post_processor.py
"""
Link Post-Processor Module

Reference implementation from ai-markmap-agent/src/post_processing.py.
This module adds links after mindmap generation to save tokens.

Processing flow:
1. Convert plain text "LeetCode 11" to complete links
2. Add Solution links (if available)
3. Normalize link formats

Preprocessing functions are also provided to simplify LeetCode links
before sending to LLM, reducing token usage.
"""

from __future__ import annotations

import re
from typing import Any

from .core.post_processing import (
    PostProcessor as CorePostProcessor,
    post_process_content as core_post_process_content,
)
from .core.data import ProblemData
from . import load_problems


def simplify_leetcode_links(content: str) -> str:
    """
    Simplify LeetCode markdown links to plain text format.
    
    This reduces input tokens by removing URLs and solution links,
    while preserving the problem title for LLM context.
    Post-processing will add the links back automatically.
    
    Transformations:
    - `[LeetCode 79 – Word Search](url) · [Solution](github_url)` → `LeetCode 79 – Word Search`
    - `[LeetCode 79 – Word Search](url)[Solution](github_url)` → `LeetCode 79 – Word Search`
    - `[LeetCode 79 – Word Search](url)` → `LeetCode 79 – Word Search`
    - `[LeetCode 79](url) · [Solution](github_url)` → `LeetCode 79`
    - `[LeetCode 79](url)` → `LeetCode 79`
    
    Args:
        content: Markdown content with LeetCode links
    
    Returns:
        Content with links simplified to plain text
    """
    # Pattern: [LeetCode N...](url) with optional Solution link
    # Handles: with separator (· or |), without separator, or no Solution at all
    content = re.sub(
        r'\[(LeetCode\s+\d+[^\]]*)\]\([^)]+\)(\s*(?:·|\xb7|\|)?\s*\[Solution\]\([^)]+\))?',
        r'\1',
        content,
        flags=re.IGNORECASE
    )
    return content


def preprocess_for_llm(content: str) -> str:
    """
    Preprocess content before sending to LLM to reduce token usage.
    
    This function:
    1. Simplifies LeetCode links to plain text (LeetCode N – Title)
    2. Removes redundant whitespace
    
    Args:
        content: Content to preprocess
    
    Returns:
        Preprocessed content with simplified links and normalized whitespace
    """
    content = simplify_leetcode_links(content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content


def add_links_to_mindmap(content: str, problems: dict[str, ProblemData] | None = None) -> str:
    """
    Add links to mindmap content (post-processing).
    
    This function references ai-markmap-agent implementation,
    adding links after generation to save tokens.
    
    Args:
        content: Generated mindmap markdown content (without links)
        problems: Problem data dictionary (auto-loaded if None)
    
    Returns:
        Mindmap content with links added
    """
    if problems is None:
        problems = load_problems()
    
    # Use core module's PostProcessor
    return core_post_process_content(content, problems)


class LinkPostProcessor:
    """
    Link post-processor (reference implementation from ai-markmap-agent).
    
    This class provides the same functionality as ai-markmap-agent/src/post_processing.py,
    but adapted to the existing tools/mindmaps structure.
    """
    
    def __init__(self, problems: dict[str, ProblemData] | None = None):
        """
        Initialize post-processor.
        
        Args:
            problems: Problem data dictionary (auto-loaded if None)
        """
        if problems is None:
            problems = load_problems()
        
        # Use core module's PostProcessor
        self.processor = CorePostProcessor(problems)
    
    def process(self, content: str) -> str:
        """
        Process content and add links.
        
        Args:
            content: Markdown content to process
        
        Returns:
            Processed content with links added
        """
        return self.processor.process(content)
    
    def process_batch(self, contents: dict[str, str]) -> dict[str, str]:
        """
        Batch process multiple contents.
        
        Args:
            contents: Content dictionary (key: language code, value: content)
        
        Returns:
            Dictionary of processed contents with links added
        """
        return {key: self.process(content) for key, content in contents.items()}


#!/usr/bin/env python3
"""
LeetCode Scraper Module

This module provides functions to fetch LeetCode problem descriptions
and constraints using the leetscrape library.
"""

from typing import List, Tuple


def get_description_and_constraints(slug: str) -> Tuple[List[str], List[str]]:
    """
    Fetch description and constraints online using leetscrape and convert to plain text lines.
    
    Args:
        slug: The LeetCode problem slug (e.g., 'combinations')
    
    Returns:
        A tuple of (description_lines, constraint_lines) where each is a list of strings.
        Returns empty lists if leetscrape is not available or if an error occurs.
    """
    try:
        from leetscrape import GetQuestion
    except ImportError:
        return [], []

    try:
        q = GetQuestion(titleSlug=slug)
        q.scrape()
        
        # Process description: split by newlines and filter empty lines
        desc_lines = []
        if q.question_content:
            desc_lines = [line.strip() for line in q.question_content.split("\n") if line.strip()]
        
        # Process constraints: remove leading "- " if present, then add it back consistently
        const_lines = []
        if q.constraints:
            # Strip leading "- " from each constraint, then add it back
            const_lines = [f"- {c[2:].strip()}" if c.strip().startswith("- ") else f"- {c.strip()}" 
                          for c in q.constraints if c.strip()]
        
        return desc_lines, const_lines
    except Exception:
        return [], []


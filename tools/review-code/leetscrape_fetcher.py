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
        
        # Process description from Body: split by newlines and filter empty lines
        desc_lines = []
        if hasattr(q, 'Body') and q.Body:
            desc_lines = [line.strip() for line in q.Body.split("\n") if line.strip()]
        
        # Process constraints: check for Constraints attribute or parse from Body
        const_lines = []
        constraints_start = None
        
        # Try to get constraints from Constraints attribute if available
        if hasattr(q, 'Constraints') and q.Constraints:
            if isinstance(q.Constraints, list):
                const_lines = [f"- {c[2:].strip()}" if c.strip().startswith("- ") else f"- {c.strip()}" 
                              for c in q.Constraints if c.strip()]
            elif isinstance(q.Constraints, str):
                # If Constraints is a string, split by newlines
                const_lines = [f"- {c[2:].strip()}" if c.strip().startswith("- ") else f"- {c.strip()}" 
                              for c in q.Constraints.split("\n") if c.strip()]
        # If no Constraints attribute, try to extract from Body
        elif desc_lines:
            # Look for "Constraints:" section in description
            for i, line in enumerate(desc_lines):
                if line.lower().startswith("constraints:"):
                    constraints_start = i
                    break
            
            if constraints_start is not None:
                # Extract constraints lines (until next section or end)
                for line in desc_lines[constraints_start + 1:]:
                    if line.strip().startswith("-"):
                        const_lines.append(line.strip())
                    elif line.strip() and not line.strip().startswith("-"):
                        # Stop if we hit a non-constraint line (new section)
                        break
                
                # Remove constraints section from description
                desc_lines = desc_lines[:constraints_start]
        
        return desc_lines, const_lines
    except Exception as e:
        # For debugging, you can uncomment the next line
        # import traceback; traceback.print_exc()
        return [], []


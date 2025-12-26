#!/usr/bin/env python3
"""
LeetCode Scraper Module

This module provides functions to fetch LeetCode problem descriptions
and constraints using the leetscrape library.
"""

from typing import List, Tuple
import re
import html


def _extract_text_from_html(html_content: str) -> str:
    """
    Extract plain text from HTML, preserving structure for constraints.
    
    Args:
        html_content: HTML string
    
    Returns:
        Plain text string with HTML tags removed
    """
    if not html_content:
        return ""
    
    # Decode HTML entities
    text = html.unescape(html_content)
    
    # Remove script and style tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Replace block elements with newlines (but preserve <li> content structure)
    text = re.sub(r'</(p|div|h[1-6]|pre|br)[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<(p|div|h[1-6]|pre)[^>]*>', '\n', text, flags=re.IGNORECASE)
    
    # Handle <li> tags specially - add newline before and mark for constraint extraction
    text = re.sub(r'</li>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<li[^>]*>', '', text, flags=re.IGNORECASE)
    
    # Remove all remaining HTML tags (including <code>, <strong>, etc.)
    # But preserve their text content
    text = re.sub(r'<[^>]+>', '', text)
    
    # Clean up whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double
    text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single
    
    return text.strip()


def _extract_brief_description(html_body: str) -> List[str]:
    """
    Extract brief problem description from HTML Body.
    
    According to review-code.md format:
    - Should contain only the problem statement
    - Should NOT include Examples
    - Should NOT include Constraints
    - Should stop before "Example" or "Constraints" sections
    
    Args:
        html_body: HTML content from q.Body
    
    Returns:
        List of description lines (plain text)
    """
    if not html_body:
        return []
    
    # Convert HTML to text
    text = _extract_text_from_html(html_body)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    # Find where to stop (Example or Constraints section)
    stop_keywords = ["example", "constraints:", "follow-up:", "follow-up"]
    description_lines = []
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Stop if we hit Example, Constraints, or Follow-up
        if any(line_lower.startswith(kw) for kw in stop_keywords):
            break
        
        # Skip empty lines at the start
        if not description_lines and not line:
            continue
        
        description_lines.append(line)
    
    return description_lines


def _extract_constraints(html_body: str) -> List[str]:
    """
    Extract constraints from HTML Body.
    
    According to review-code.md format:
    - Constraints should be in format: "- {constraint text}"
    - Should extract from <ul><li> tags in HTML
    - Each constraint should start with "- "
    
    Args:
        html_body: HTML content from q.Body
    
    Returns:
        List of constraint lines, each starting with "- "
    """
    if not html_body:
        return []
    
    # Find the Constraints section in HTML
    # Look for <p><strong>Constraints:</strong></p> followed by <ul><li>...</li></ul>
    constraints_pattern = r'<p>\s*<strong[^>]*>\s*Constraints?:\s*</strong>\s*</p>\s*<ul>(.*?)</ul>'
    match = re.search(constraints_pattern, html_body, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return []
    
    ul_content = match.group(1)
    
    # Extract all <li> items
    li_pattern = r'<li[^>]*>(.*?)</li>'
    li_matches = re.findall(li_pattern, ul_content, re.DOTALL | re.IGNORECASE)
    
    constraints = []
    for li_content in li_matches:
        # Handle <sup> tags: convert <sup>n</sup> to ^n
        li_content = re.sub(r'<sup[^>]*>(.*?)</sup>', r'^\1', li_content, flags=re.IGNORECASE)
        
        # Extract text from <li>, handling nested tags like <code>
        # Remove HTML tags but preserve text content
        constraint_text = re.sub(r'<[^>]+>', '', li_content)
        constraint_text = html.unescape(constraint_text)
        
        # Clean up whitespace (preserve single spaces, normalize multiple spaces)
        constraint_text = re.sub(r'\s+', ' ', constraint_text).strip()
        
        if constraint_text:
            # Ensure it starts with "- "
            if not constraint_text.startswith("-"):
                constraint_text = f"- {constraint_text}"
            constraints.append(constraint_text)
    
    return constraints


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
        q = GetQuestion(titleSlug=slug).scrape()
        
        # Debug: print available attributes
        # print(f"Available attributes: {[attr for attr in dir(q) if not attr.startswith('_')]}")
        
        # Extract description and constraints according to review-code.md format
        desc_lines = []
        const_lines = []
        
        if hasattr(q, 'Body') and q.Body:
            # Extract brief description (stops before Examples/Constraints)
            desc_lines = _extract_brief_description(q.Body)
            
            # Extract constraints from HTML <ul><li> structure
            const_lines = _extract_constraints(q.Body)
        
        # Fallback: Try to get constraints from Constraints attribute if HTML extraction failed
        if not const_lines and hasattr(q, 'Constraints') and q.Constraints:
            if isinstance(q.Constraints, list):
                const_lines = [f"- {c[2:].strip()}" if c.strip().startswith("- ") else f"- {c.strip()}" 
                              for c in q.Constraints if c.strip()]
            elif isinstance(q.Constraints, str):
                # If Constraints is a string, try to extract from HTML
                const_lines = _extract_constraints(q.Constraints)
                if not const_lines:
                    # Fallback to simple text extraction
                    constraints_text = _extract_text_from_html(q.Constraints)
                    const_lines = [f"- {c[2:].strip()}" if c.strip().startswith("- ") else f"- {c.strip()}" 
                                  for c in constraints_text.split("\n") if c.strip()]
        
        return desc_lines, const_lines
    except Exception as e:
        # For debugging, you can uncomment the next line
        # import traceback; traceback.print_exc()
        return [], []

if __name__ == "__main__":
    slug = input("Enter LeetCode problem slug (e.g. two-sum): ").strip()
    desc, constraints = get_description_and_constraints(slug)
    print("=== Description ===")
    print('\n'.join(desc))
    print("\n=== Constraints ===")
    print('\n'.join(constraints) if constraints else "(None found)")


#!/usr/bin/env python3
"""
LeetCode Scraper Module

This module provides functions to fetch LeetCode problem descriptions
and constraints, with SQLite caching for improved performance.

Architecture:
    - Uses question_api for unified data access (cache + network)
    - Provides backward-compatible extraction functions
    - HTML parsing utilities for docstring generation
"""

from typing import List, Tuple, Optional, Any
import re
import html
import sys
from pathlib import Path

# Add leetcode-api to path for imports
_LEETCODE_API_PATH = Path(__file__).parent.parent / "leetcode-api"
if str(_LEETCODE_API_PATH) not in sys.path:
    sys.path.insert(0, str(_LEETCODE_API_PATH))

from question_api import get_question, Question


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
    stop_keywords = ["example", "constraints:", "follow-up:", "follow-up", "note:"]
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
    - <sup> tags should be converted to ^ notation
    
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


def _extract_examples(html_body: str) -> List[dict]:
    """
    Extract all examples from HTML Body.
    
    According to review-code.md format:
    - Include ALL examples from LeetCode
    - Preserve <img> tags
    - Use 4-space indentation for Input/Output/Explanation
    - Explanation may span multiple lines
    
    Args:
        html_body: HTML content from q.Body
    
    Returns:
        List of example dicts with keys: number, img, input, output, explanation
    """
    if not html_body:
        return []
    
    examples = []
    
    # Pattern to find Example blocks
    # Examples usually start with <p><strong>Example N:</strong></p>
    example_pattern = r'<p>\s*<strong[^>]*>\s*Example\s*(\d+):\s*</strong>\s*</p>(.*?)(?=<p>\s*<strong[^>]*>\s*(?:Example|Constraints?|Follow[\s-]?up|Note):|$)'
    matches = re.findall(example_pattern, html_body, re.DOTALL | re.IGNORECASE)
    
    for num, content in matches:
        example = {'number': int(num), 'img': None, 'input': '', 'output': '', 'explanation': ''}
        
        # Extract <img> tag if present (preserve entire tag)
        img_match = re.search(r'(<img[^>]*>)', content, re.IGNORECASE)
        if img_match:
            example['img'] = img_match.group(1)
        
        # Extract Input
        input_match = re.search(r'<strong[^>]*>\s*Input:\s*</strong>\s*(.*?)(?=<strong|$)', content, re.DOTALL | re.IGNORECASE)
        if input_match:
            input_text = re.sub(r'<[^>]+>', '', input_match.group(1))
            example['input'] = html.unescape(input_text).strip()
        
        # Extract Output
        output_match = re.search(r'<strong[^>]*>\s*Output:\s*</strong>\s*(.*?)(?=<strong|$)', content, re.DOTALL | re.IGNORECASE)
        if output_match:
            output_text = re.sub(r'<[^>]+>', '', output_match.group(1))
            example['output'] = html.unescape(output_text).strip()
        
        # Extract Explanation (may span multiple lines)
        expl_match = re.search(r'<strong[^>]*>\s*Explanation:\s*</strong>\s*(.*?)(?=<p>|<strong>|$)', content, re.DOTALL | re.IGNORECASE)
        if expl_match:
            expl_text = re.sub(r'<[^>]+>', '', expl_match.group(1))
            example['explanation'] = html.unescape(expl_text).strip()
        
        examples.append(example)
    
    return examples


def _extract_follow_up(html_body: str) -> List[str]:
    """
    Extract follow-up questions from HTML Body.
    
    Args:
        html_body: HTML content from q.Body
    
    Returns:
        List of follow-up question strings
    """
    if not html_body:
        return []
    
    follow_ups = []
    
    # Pattern for Follow-up or Follow up
    followup_pattern = r'<p>\s*<strong[^>]*>\s*Follow[\s-]?up[^:]*:\s*</strong>\s*(.*?)</p>'
    matches = re.findall(followup_pattern, html_body, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        text = re.sub(r'<[^>]+>', '', match)
        text = html.unescape(text).strip()
        if text:
            follow_ups.append(text)
    
    return follow_ups


def _extract_note(html_body: str) -> Optional[str]:
    """
    Extract Note section from HTML Body.
    
    Args:
        html_body: HTML content from q.Body
    
    Returns:
        Note text or None if not present
    """
    if not html_body:
        return None
    
    # Pattern for Note section
    note_pattern = r'<p>\s*<strong[^>]*>\s*Note:\s*</strong>\s*(.*?)</p>'
    match = re.search(note_pattern, html_body, re.DOTALL | re.IGNORECASE)
    
    if match:
        text = re.sub(r'<[^>]+>', '', match.group(1))
        return html.unescape(text).strip() or None
    
    return None


def get_question_data(slug: str, force_refresh: bool = False) -> Optional[Question]:
    """
    Get complete question data for a LeetCode problem.
    
    This is the primary interface for accessing question data.
    Uses SQLite cache for improved performance.
    
    Args:
        slug: The LeetCode problem slug (e.g., 'two-sum')
        force_refresh: If True, bypass cache and fetch fresh data
    
    Returns:
        Question object with all data, or None if not found
    """
    return get_question(slug, force_refresh)


def get_description_and_constraints(slug: str) -> Tuple[List[str], List[str]]:
    """
    Fetch description and constraints for a LeetCode problem.
    
    This is the backward-compatible interface. Uses SQLite cache internally.
    
    Args:
        slug: The LeetCode problem slug (e.g., 'combinations')
    
    Returns:
        A tuple of (description_lines, constraint_lines) where each is a list of strings.
        Returns empty lists if data is not available.
    """
    q = get_question(slug)
    
    if not q or not q.Body:
        return [], []
    
    desc_lines = _extract_brief_description(q.Body)
    const_lines = _extract_constraints(q.Body)
    
    return desc_lines, const_lines


def get_full_docstring_data(slug: str) -> dict:
    """
    Get all data needed for generating a complete File-Level Docstring.
    
    Returns structured data according to review-code.md specification:
    - description: List of description lines
    - examples: List of example dicts (with img, input, output, explanation)
    - constraints: List of constraint lines (starting with "- ")
    - follow_ups: List of follow-up question strings
    - note: Optional note string
    
    Args:
        slug: The LeetCode problem slug
    
    Returns:
        Dictionary with all docstring components
    """
    q = get_question(slug)
    
    if not q:
        return {
            'title': '',
            'url': '',
            'description': [],
            'examples': [],
            'constraints': [],
            'follow_ups': [],
            'note': None,
        }
    
    return {
        'title': q.title,
        'url': f'https://leetcode.com/problems/{q.titleSlug}/',
        'description': _extract_brief_description(q.Body),
        'examples': _extract_examples(q.Body),
        'constraints': _extract_constraints(q.Body),
        'follow_ups': _extract_follow_up(q.Body),
        'note': _extract_note(q.Body),
    }


if __name__ == "__main__":
    slug = input("Enter LeetCode problem slug (e.g. two-sum): ").strip()
    
    print("\n=== Using get_description_and_constraints (backward-compatible) ===")
    desc, constraints = get_description_and_constraints(slug)
    print("Description:")
    print('\n'.join(desc) if desc else "(None found)")
    print("\nConstraints:")
    print('\n'.join(constraints) if constraints else "(None found)")
    
    print("\n=== Using get_full_docstring_data (new API) ===")
    data = get_full_docstring_data(slug)
    print(f"Title: {data['title']}")
    print(f"URL: {data['url']}")
    print(f"Examples: {len(data['examples'])}")
    for ex in data['examples']:
        print(f"  Example {ex['number']}:")
        if ex['img']:
            print(f"    {ex['img']}")
        print(f"    Input: {ex['input'][:50]}..." if len(ex['input']) > 50 else f"    Input: {ex['input']}")
        print(f"    Output: {ex['output']}")
    print(f"Follow-ups: {data['follow_ups']}")
    print(f"Note: {data['note']}")

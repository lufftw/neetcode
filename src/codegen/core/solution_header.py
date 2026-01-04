"""
Solution header renderer.

Generates file-level docstrings for solution files based on problem metadata.
"""

import html
import re
from typing import Literal, Optional, Union

from leetcode_datasource import Question, ProblemInfo


HeaderLevel = Literal["minimal", "standard", "full"]


def render_solution_header(
    meta: Union[Question, ProblemInfo],
    level: HeaderLevel = "full",
) -> str:
    """
    Render solution file's header (file-level docstring).
    
    Args:
        meta: Problem metadata (Question or ProblemInfo from leetcode_datasource)
        level: Data level ("minimal" | "standard" | "full")
            - minimal: title, slug, difficulty, url
            - standard: + topics, constraints
            - full: + examples, hints, follow-up, notes (default)
    
    Returns:
        str: Formatted docstring (including triple quotes)
    
    Example:
        >>> from leetcode_datasource import LeetCodeDataSource
        >>> ds = LeetCodeDataSource()
        >>> q = ds.get_by_frontend_id(1)
        >>> header = render_solution_header(q)
        >>> print(header[:50])
        \"\"\"
        Problem: Two Sum
        Link: https://leetcode
    """
    lines = ['"""']
    
    # Title and link (all levels)
    title = _get_title(meta)
    url = _get_url(meta)
    
    lines.append(f"Problem: {title}")
    lines.append(f"Link: {url}")
    lines.append("")
    
    # Body content (standard and full)
    if level in ("standard", "full") and isinstance(meta, Question):
        body = _clean_html_body(meta.Body)
        if body:
            lines.append(body)
            lines.append("")
    
    # Topics (standard and full)
    if level in ("standard", "full"):
        topics = _get_topics(meta)
        if topics:
            lines.append(f"Topics: {topics}")
            lines.append("")
    
    # Hints (full only)
    if level == "full" and isinstance(meta, Question):
        hints = meta.Hints or []
        for i, hint in enumerate(hints, 1):
            cleaned_hint = _clean_html(hint)
            if cleaned_hint:
                lines.append(f"Hint {i}: {cleaned_hint}")
                lines.append("")
    
    # Close docstring
    # Remove trailing empty lines before closing
    while lines and lines[-1] == "":
        lines.pop()
    
    lines.append('"""')
    
    return "\n".join(lines)


def _get_title(meta: Union[Question, ProblemInfo]) -> str:
    """Get title from Question or ProblemInfo."""
    return meta.title


def _get_url(meta: Union[Question, ProblemInfo]) -> str:
    """Get URL from Question or ProblemInfo."""
    if isinstance(meta, Question):
        return f"https://leetcode.com/problems/{meta.titleSlug}/"
    else:
        return meta.url or f"https://leetcode.com/problems/{meta.title_slug}/"


def _get_topics(meta: Union[Question, ProblemInfo]) -> str:
    """Get topics string from Question or ProblemInfo."""
    if isinstance(meta, Question):
        # topicTags is comma-separated slug format: "array,hash-table"
        if meta.topicTags:
            # Convert slugs to title case
            topics = meta.topicTags.split(",")
            return ", ".join(t.replace("-", " ").title() for t in topics)
    return ""


def _clean_html_body(html_body: str) -> str:
    """
    Clean HTML problem description to plain text.
    
    Handles:
    - HTML entity decoding
    - Tag removal
    - Example formatting
    - Constraint extraction
    """
    if not html_body:
        return ""
    
    text = html_body
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Convert specific tags to text markers
    text = re.sub(r'<strong[^>]*>|<b>', '', text)
    text = re.sub(r'</strong>|</b>', '', text)
    text = re.sub(r'<em[^>]*>|<i>', '', text)
    text = re.sub(r'</em>|</i>', '', text)
    text = re.sub(r'<code>', '', text)
    text = re.sub(r'</code>', '', text)
    text = re.sub(r'<sup>', '^', text)
    text = re.sub(r'</sup>', '', text)
    text = re.sub(r'<sub>', '_', text)
    text = re.sub(r'</sub>', '', text)
    
    # Handle lists
    text = re.sub(r'<li>', '- ', text)
    text = re.sub(r'</li>', '\n', text)
    text = re.sub(r'<ul>|</ul>|<ol>|</ol>', '\n', text)
    
    # Handle paragraphs and line breaks
    text = re.sub(r'<p[^>]*>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<div[^>]*>', '\n', text)
    text = re.sub(r'</div>', '\n', text)
    
    # Handle preformatted text
    text = re.sub(r'<pre[^>]*>', '\n', text)
    text = re.sub(r'</pre>', '\n', text)
    
    # Remove images (keep alt text if available)
    text = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*>', r'\1', text)
    text = re.sub(r'<img[^>]*>', '', text)
    
    # Remove remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    # Process lines
    lines = text.strip().split('\n')
    result_lines = []
    in_example = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if result_lines and result_lines[-1] != "":
                result_lines.append("")
            continue
        
        # Format examples with indentation
        if line.startswith("Example"):
            in_example = True
            result_lines.append(line)
        elif in_example and (line.startswith("Input:") or 
                            line.startswith("Output:") or 
                            line.startswith("Explanation:")):
            result_lines.append(f"    {line}")
        elif line.startswith("Constraints:"):
            in_example = False
            result_lines.append("")
            result_lines.append(line)
        elif line.startswith("- ") and not in_example:
            # Constraint items
            result_lines.append(line)
        elif line.startswith("Follow-up:") or line.startswith("Follow up:"):
            in_example = False
            result_lines.append("")
            result_lines.append(line.replace("Follow up:", "Follow-up:"))
        else:
            in_example = False
            result_lines.append(line)
    
    return "\n".join(result_lines)


def _clean_html(text: str) -> str:
    """Simple HTML tag removal."""
    if not text:
        return ""
    
    text = html.unescape(text)
    text = re.sub(r'<code>', '', text)
    text = re.sub(r'</code>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


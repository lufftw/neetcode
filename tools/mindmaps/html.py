# tools/mindmaps/html.py
"""HTML generation for mind maps.

This module re-exports all HTML generation functions from core.html
to maintain backward compatibility with existing imports.
"""

# Re-export everything from core.html
from .core.html import (
    markdown_to_html_content,
    generate_html_mindmap,
    setup_pages_directory,
)

__all__ = [
    "markdown_to_html_content",
    "generate_html_mindmap",
    "setup_pages_directory",
]


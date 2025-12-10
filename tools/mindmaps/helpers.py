# tools/mindmaps/helpers.py
"""Helper functions for mind map generation."""

from __future__ import annotations
from .data import ProblemData


def markmap_frontmatter(title: str, color_freeze_level: int = 2) -> str:
    """Generate YAML frontmatter for markmap."""
    return f"""---
title: {title}
markmap:
  colorFreezeLevel: {color_freeze_level}
  maxWidth: 400
---
"""


def format_problem_entry(prob: ProblemData, show_complexity: bool = False) -> str:
    """Format a problem entry with link and metadata."""
    entry = prob.markdown_link(include_difficulty=True)
    if show_complexity and prob.solutions:
        complexity = prob.solutions[0].get("complexity", "")
        if complexity:
            entry += f" — `{complexity}`"
    return entry


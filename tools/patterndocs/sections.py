# tools/patterndocs/sections.py
"""Section numbering and TOC generation for pattern documentation."""

from __future__ import annotations


def generate_toc(sections_info: list[tuple[int, str, str]]) -> str:
    """Generate table of contents from sections info."""
    lines = ["## Table of Contents", ""]
    for section_num, title, anchor in sections_info:
        lines.append(f"{section_num}. [{title}](#{anchor})")
    return "\n".join(lines)


def create_anchor(section_num: int, title: str) -> str:
    """Create a markdown anchor from section number and title.
    
    Converts title to GitHub Flavored Markdown compatible anchor:
    - Lowercase
    - Spaces → hyphen
    - Remove special chars (parentheses, slashes, colons, +, etc.)
    - Keep multiple consecutive hyphens (GFM does NOT collapse them)
    - Remove leading number prefix (e.g., "4. " from "4. Title")
    """
    import re
    
    # Remove leading number prefix (e.g., "4. " or "4.")
    title = re.sub(r'^\d+\.\s*', '', title)
    
    anchor = f"{section_num}-{title.lower()}"
    # Replace spaces with hyphens
    anchor = anchor.replace(" ", "-")
    # Remove Unicode dashes (GFM removes them, not converts to hyphen)
    anchor = anchor.replace("–", "")  # en-dash (U+2013)
    anchor = anchor.replace("—", "")  # em-dash (U+2014)
    # Remove parentheses, slashes, colons, and other special characters
    anchor = re.sub(r'[()/:]', '', anchor)
    # Remove other non-word characters (keep only alphanumeric and hyphens)
    # Note: GFM does NOT collapse multiple hyphens, so we preserve them
    anchor = re.sub(r'[^\w\-]', '', anchor)
    return anchor.strip('-')


def add_section_numbers(content: str, section_num: int) -> tuple[str, list[tuple[int, str, str]]]:
    """
    Add section numbers to markdown content.
    
    Returns:
        (modified_content, sections_info)
    """
    lines = content.split("\n")
    result_lines = []
    sections_info = []
    current_section = section_num
    subsection_counter = 0
    
    for line in lines:
        if line.startswith("## ") and not line.startswith("### "):
            title = line[3:].strip()
            anchor = create_anchor(current_section, title)
            sections_info.append((current_section, title, anchor))
            result_lines.append(f"## {current_section}. {title}")
            subsection_counter = 0
            current_section += 1
        elif line.startswith("### ") and not line.startswith("#### "):
            subsection_counter += 1
            title = line[4:].strip()
            result_lines.append(f"### {current_section - 1}.{subsection_counter} {title}")
        else:
            result_lines.append(line)
    
    return "\n".join(result_lines), sections_info


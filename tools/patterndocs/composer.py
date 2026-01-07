# tools/patterndocs/composer.py
"""Document composition for pattern documentation."""

from __future__ import annotations
from pathlib import Path

from .data import PatternDocConfig
from .sections import generate_toc, add_section_numbers


def _strip_separators(content: str) -> str:
    """Remove leading and trailing '---' separators from content."""
    lines = content.split("\n")
    # Skip leading empty lines and separator
    while lines and (lines[0].strip() == "" or lines[0].strip() == "---"):
        lines.pop(0)
    # Skip trailing empty lines and separator
    while lines and (lines[-1].strip() == "" or lines[-1].strip() == "---"):
        lines.pop()
    return "\n".join(lines)


def compose_document(
    config: PatternDocConfig,
    header_files: list[Path],
    problem_files: list[Path],
    footer_files: list[Path],
) -> str:
    """Compose the final document from source files."""
    # Read all content and strip separators to avoid duplicates
    header_contents = [_strip_separators(f.read_text(encoding="utf-8")) for f in header_files]
    problem_contents = [_strip_separators(f.read_text(encoding="utf-8")) for f in problem_files]
    footer_contents = [_strip_separators(f.read_text(encoding="utf-8")) for f in footer_files]
    
    # First pass: collect section info for TOC
    all_sections_info: list[tuple[int, str, str]] = []
    current_section_num = 1
    
    for content in header_contents + problem_contents + footer_contents:
        _, sections_info = add_section_numbers(content, current_section_num)
        all_sections_info.extend(sections_info)
        if sections_info:
            current_section_num = sections_info[-1][0] + 1
    
    # Second pass: generate numbered content
    def process_contents(contents: list[str], start_num: int) -> tuple[list[str], int]:
        numbered = []
        num = start_num
        for content in contents:
            numbered_content, sections_info = add_section_numbers(content, num)
            numbered.append(numbered_content)
            if sections_info:
                num = sections_info[-1][0] + 1
        return numbered, num
    
    numbered_headers, next_num = process_contents(header_contents, 1)
    numbered_problems, next_num = process_contents(problem_contents, next_num)
    numbered_footers, _ = process_contents(footer_contents, next_num)
    
    # Compose final document
    final_sections = []
    
    # Process header - insert TOC after intro
    if numbered_headers:
        header = numbered_headers[0]
        lines = header.split("\n")
        intro_lines, rest_lines = [], []
        
        for i, line in enumerate(lines):
            if line.startswith("## ") and ". " in line[:10]:
                rest_lines = lines[i:]
                break
            intro_lines.append(line)
        
        if intro_lines:
            final_sections.append("\n".join(intro_lines).strip())
        
        final_sections.append(generate_toc(all_sections_info))
        final_sections.append("---")
        
        if rest_lines:
            final_sections.append("\n".join(rest_lines).strip())
    
    # Add problem and footer sections
    for content in numbered_problems:
        final_sections.extend(["---", content])
    for content in numbered_footers:
        final_sections.extend(["---", content])
    
    # Final footer
    final_sections.extend([
        "", "---", "",
        f"*Document generated for NeetCode Practice Framework — API Kernel: {config.kernel_id}*"
    ])
    
    return "\n\n".join(final_sections) + "\n"


# tools/patterndocs/files.py
"""File collection for pattern documentation."""

from __future__ import annotations
from pathlib import Path

# File ordering
STRUCTURAL_FILES_ORDER = ["_header.md"]
STRUCTURAL_FILES_FOOTER = ["_comparison.md", "_decision.md", "_templates.md"]


def collect_source_files(source_dir: Path) -> tuple[list[Path], list[Path], list[Path]]:
    """
    Collect and categorize source files.
    
    Returns:
        (header_files, problem_files, footer_files)
    """
    if not source_dir.exists():
        return [], [], []

    all_files = sorted(source_dir.glob("*.md"))
    header_files, footer_files, problem_files = [], [], []

    for f in all_files:
        name = f.name
        if name in STRUCTURAL_FILES_ORDER:
            header_files.append(f)
        elif name in STRUCTURAL_FILES_FOOTER:
            footer_files.append(f)
        elif name.startswith("_"):
            footer_files.append(f)
        else:
            problem_files.append(f)

    # Sort by predefined order
    header_files.sort(key=lambda f: STRUCTURAL_FILES_ORDER.index(f.name) 
                      if f.name in STRUCTURAL_FILES_ORDER else 999)
    footer_files.sort(key=lambda f: STRUCTURAL_FILES_FOOTER.index(f.name)
                      if f.name in STRUCTURAL_FILES_FOOTER else 999)
    problem_files.sort(key=lambda f: f.name)

    return header_files, problem_files, footer_files


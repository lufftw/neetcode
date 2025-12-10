#!/usr/bin/env python3
"""
Pattern Documentation Generator

Generates comprehensive pattern documentation by composing:
- Ontology definitions (api_kernels.toml, patterns.toml)
- Per-problem markdown snippets (meta/patterns/<kernel>/*.md)

Output: docs/patterns/<kernel>.md

Usage:
    python tools/generate_pattern_docs.py                    # Generate all
    python tools/generate_pattern_docs.py --pattern sliding_window
    python tools/generate_pattern_docs.py --validate         # Validate only
    python tools/generate_pattern_docs.py --list             # List available patterns
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Project root (adjust if script location changes)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Directory paths
ONTOLOGY_DIR = PROJECT_ROOT / "ontology"
META_PATTERNS_DIR = PROJECT_ROOT / "meta" / "patterns"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "patterns"

# File ordering for pattern composition
# Files starting with _ are structural, others are problem-specific
STRUCTURAL_FILES_ORDER = ["_header.md"]
STRUCTURAL_FILES_FOOTER = ["_comparison.md", "_decision.md", "_templates.md"]


# ---------------------------------------------------------------------------
# TOML Parser (minimal, no external dependencies)
# ---------------------------------------------------------------------------

def parse_toml_simple(content: str) -> dict[str, Any]:
    """
    Simple TOML parser for our specific use case.
    Handles [[array]] and key = "value" patterns.
    """
    result: dict[str, Any] = {}
    current_array_name: str | None = None
    current_item: dict[str, str] = {}

    for line in content.splitlines():
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        # Array header: [[array_name]]
        if line.startswith("[[") and line.endswith("]]"):
            # Save previous item if exists
            if current_array_name and current_item:
                if current_array_name not in result:
                    result[current_array_name] = []
                result[current_array_name].append(current_item)

            current_array_name = line[2:-2].strip()
            current_item = {}
            continue

        # Key-value pair: key = "value" or key = value
        if "=" in line:
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()

            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]

            if current_array_name:
                current_item[key] = value
            else:
                result[key] = value

    # Don't forget the last item
    if current_array_name and current_item:
        if current_array_name not in result:
            result[current_array_name] = []
        result[current_array_name].append(current_item)

    return result


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class APIKernel:
    """Represents an API Kernel from ontology."""
    id: str
    summary: str


@dataclass
class Pattern:
    """Represents a Pattern from ontology."""
    id: str
    api_kernel: str
    summary: str


@dataclass
class PatternDocConfig:
    """Configuration for generating a pattern document."""
    kernel_id: str
    kernel_summary: str
    source_dir: Path
    output_file: Path
    patterns: list[Pattern] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Ontology Loading
# ---------------------------------------------------------------------------

def load_api_kernels() -> dict[str, APIKernel]:
    """Load API kernels from ontology."""
    path = ONTOLOGY_DIR / "api_kernels.toml"
    if not path.exists():
        print(f"Warning: {path} not found")
        return {}

    content = path.read_text(encoding="utf-8")
    data = parse_toml_simple(content)

    kernels = {}
    for item in data.get("api_kernels", []):
        kernel = APIKernel(
            id=item.get("id", ""),
            summary=item.get("summary", ""),
        )
        kernels[kernel.id] = kernel

    return kernels


def load_patterns() -> dict[str, list[Pattern]]:
    """Load patterns from ontology, grouped by API kernel."""
    path = ONTOLOGY_DIR / "patterns.toml"
    if not path.exists():
        print(f"Warning: {path} not found")
        return {}

    content = path.read_text(encoding="utf-8")
    data = parse_toml_simple(content)

    patterns_by_kernel: dict[str, list[Pattern]] = {}
    for item in data.get("patterns", []):
        pattern = Pattern(
            id=item.get("id", ""),
            api_kernel=item.get("api_kernel", ""),
            summary=item.get("summary", ""),
        )
        if pattern.api_kernel not in patterns_by_kernel:
            patterns_by_kernel[pattern.api_kernel] = []
        patterns_by_kernel[pattern.api_kernel].append(pattern)

    return patterns_by_kernel


# ---------------------------------------------------------------------------
# Pattern Document Generation
# ---------------------------------------------------------------------------

def get_available_patterns() -> list[str]:
    """Get list of pattern directories that have source files."""
    if not META_PATTERNS_DIR.exists():
        return []

    patterns = []
    for path in META_PATTERNS_DIR.iterdir():
        if path.is_dir() and not path.name.startswith("."):
            # Check if it has at least a _header.md
            if (path / "_header.md").exists():
                patterns.append(path.name)

    return sorted(patterns)


def get_kernel_id_from_dir_name(dir_name: str) -> str:
    """Convert directory name to API Kernel ID."""
    # Mapping from directory names to kernel IDs
    mapping = {
        "sliding_window": "SubstringSlidingWindow",
        "bfs_grid": "GridBFSMultiSource",
        "backtracking": "BacktrackingExploration",
        "k_way_merge": "KWayMerge",
        "binary_search": "BinarySearchBoundary",
        "two_pointers": "TwoPointerPartition",
        "linked_list_reversal": "LinkedListInPlaceReversal",
        "monotonic_stack": "MonotonicStack",
        "prefix_sum": "PrefixSumRangeQuery",
        "tree_dfs": "TreeTraversalDFS",
        "tree_bfs": "TreeTraversalBFS",
        "dp_sequence": "DPSequence",
        "dp_interval": "DPInterval",
        "union_find": "UnionFindConnectivity",
        "trie": "TriePrefixSearch",
        "heap_top_k": "HeapTopK",
        "topological_sort": "TopologicalSort",
    }
    return mapping.get(dir_name, dir_name)


def collect_source_files(source_dir: Path) -> tuple[list[Path], list[Path], list[Path]]:
    """
    Collect and categorize source files.

    Returns:
        (header_files, problem_files, footer_files)
    """
    if not source_dir.exists():
        return [], [], []

    all_files = sorted(source_dir.glob("*.md"))

    header_files = []
    footer_files = []
    problem_files = []

    for f in all_files:
        name = f.name
        if name in STRUCTURAL_FILES_ORDER:
            header_files.append(f)
        elif name in STRUCTURAL_FILES_FOOTER:
            footer_files.append(f)
        elif name.startswith("_"):
            # Other structural files go to footer
            footer_files.append(f)
        else:
            # Problem files (e.g., 0003_base.md)
            problem_files.append(f)

    # Sort header and footer by predefined order
    header_files.sort(key=lambda f: STRUCTURAL_FILES_ORDER.index(f.name)
                      if f.name in STRUCTURAL_FILES_ORDER else 999)
    footer_files.sort(key=lambda f: STRUCTURAL_FILES_FOOTER.index(f.name)
                      if f.name in STRUCTURAL_FILES_FOOTER else 999)

    # Sort problem files by problem number
    problem_files.sort(key=lambda f: f.name)

    return header_files, problem_files, footer_files


def generate_toc(sections_info: list[tuple[int, str, str]]) -> str:
    """
    Generate table of contents from sections info.
    
    Args:
        sections_info: List of (section_num, title, anchor) tuples
    
    Returns:
        Formatted TOC markdown
    """
    lines = ["## Table of Contents", ""]
    
    for section_num, title, anchor in sections_info:
        lines.append(f"{section_num}. [{title}](#{anchor})")
    
    return "\n".join(lines)


def create_anchor(section_num: int, title: str) -> str:
    """Create a markdown anchor from section number and title."""
    # Format: "1-core-concepts" or "2-base-template-unique-characters-leetcode-3"
    anchor = f"{section_num}-{title.lower()}"
    anchor = anchor.replace(" ", "-")
    anchor = anchor.replace("(", "").replace(")", "")
    anchor = anchor.replace("/", "")
    anchor = anchor.replace(":", "")
    anchor = anchor.replace("--", "-")  # Clean double dashes
    return anchor


def add_section_numbers(content: str, section_num: int) -> tuple[str, list[tuple[int, str, str]]]:
    """
    Add section numbers to markdown content.
    
    Args:
        content: Markdown content
        section_num: Starting section number for ## headers
    
    Returns:
        (modified_content, sections_info)
        sections_info is list of (section_num, title, anchor) tuples
    """
    lines = content.split("\n")
    result_lines = []
    sections_info = []
    current_section = section_num
    subsection_counter = 0
    
    for line in lines:
        # Main section header: ## Title
        if line.startswith("## ") and not line.startswith("### "):
            title = line[3:].strip()
            anchor = create_anchor(current_section, title)
            sections_info.append((current_section, title, anchor))
            result_lines.append(f"## {current_section}. {title}")
            subsection_counter = 0
            current_section += 1
        # Subsection header: ### Title
        elif line.startswith("### ") and not line.startswith("#### "):
            subsection_counter += 1
            title = line[4:].strip()
            result_lines.append(f"### {current_section - 1}.{subsection_counter} {title}")
        else:
            result_lines.append(line)
    
    return "\n".join(result_lines), sections_info


def compose_document(
    config: PatternDocConfig,
    header_files: list[Path],
    problem_files: list[Path],
    footer_files: list[Path],
) -> str:
    """Compose the final document from source files."""
    all_sections_info: list[tuple[int, str, str]] = []
    
    # First pass: collect all sections and their info for TOC
    current_section_num = 1
    
    # Read all content first
    header_contents = [f.read_text(encoding="utf-8").strip() for f in header_files]
    problem_contents = [f.read_text(encoding="utf-8").strip() for f in problem_files]
    footer_contents = [f.read_text(encoding="utf-8").strip() for f in footer_files]
    
    # Collect section info from all content
    for content in header_contents + problem_contents + footer_contents:
        _, sections_info = add_section_numbers(content, current_section_num)
        all_sections_info.extend(sections_info)
        if sections_info:
            current_section_num = sections_info[-1][0] + 1
    
    # Second pass: generate numbered content
    numbered_header_contents = []
    numbered_problem_contents = []
    numbered_footer_contents = []
    
    current_section_num = 1
    
    for content in header_contents:
        numbered_content, sections_info = add_section_numbers(content, current_section_num)
        numbered_header_contents.append(numbered_content)
        if sections_info:
            current_section_num = sections_info[-1][0] + 1
    
    for content in problem_contents:
        numbered_content, sections_info = add_section_numbers(content, current_section_num)
        numbered_problem_contents.append(numbered_content)
        if sections_info:
            current_section_num = sections_info[-1][0] + 1
    
    for content in footer_contents:
        numbered_content, sections_info = add_section_numbers(content, current_section_num)
        numbered_footer_contents.append(numbered_content)
        if sections_info:
            current_section_num = sections_info[-1][0] + 1
    
    # Now compose the final document
    final_sections = []
    
    # Process header - insert TOC after intro, before first ## section
    if numbered_header_contents:
        header_content = numbered_header_contents[0]
        lines = header_content.split("\n")
        intro_lines = []
        rest_lines = []
        
        for i, line in enumerate(lines):
            # Look for the first numbered section header
            if line.startswith("## ") and ". " in line[:10]:
                rest_lines = lines[i:]
                break
            intro_lines.append(line)
        
        # Build document with TOC after intro
        if intro_lines:
            final_sections.append("\n".join(intro_lines).strip())
        
        # Generate and insert TOC
        toc = generate_toc(all_sections_info)
        final_sections.append(toc)
        final_sections.append("---")
        
        # Add the rest of the header content (Core Concepts section)
        if rest_lines:
            final_sections.append("\n".join(rest_lines).strip())
    
    # Add problem sections with separators
    for content in numbered_problem_contents:
        final_sections.append("---")
        final_sections.append(content)
    
    # Add footer sections with separators
    for content in numbered_footer_contents:
        final_sections.append("---")
        final_sections.append(content)
    
    # Final footer
    final_sections.append("")
    final_sections.append("---")
    final_sections.append("")
    final_sections.append(f"*Document generated for NeetCode Practice Framework — API Kernel: {config.kernel_id}*")
    
    return "\n\n".join(final_sections)


def generate_pattern_doc(pattern_name: str, dry_run: bool = False) -> bool:
    """
    Generate documentation for a specific pattern.

    Args:
        pattern_name: Name of the pattern directory (e.g., "sliding_window")
        dry_run: If True, validate only without writing

    Returns:
        True if successful, False otherwise
    """
    source_dir = META_PATTERNS_DIR / pattern_name
    output_file = OUTPUT_DIR / f"{pattern_name}.md"

    if not source_dir.exists():
        print(f"Error: Source directory not found: {source_dir}")
        return False

    # Load ontology
    kernels = load_api_kernels()
    patterns_by_kernel = load_patterns()

    # Get kernel info
    kernel_id = get_kernel_id_from_dir_name(pattern_name)
    kernel = kernels.get(kernel_id)

    if kernel:
        kernel_summary = kernel.summary
    else:
        print(f"Warning: Kernel '{kernel_id}' not found in ontology")
        kernel_summary = ""

    # Create config
    config = PatternDocConfig(
        kernel_id=kernel_id,
        kernel_summary=kernel_summary,
        source_dir=source_dir,
        output_file=output_file,
        patterns=patterns_by_kernel.get(kernel_id, []),
    )

    # Collect source files
    header_files, problem_files, footer_files = collect_source_files(source_dir)

    if not header_files:
        print(f"Error: No _header.md found in {source_dir}")
        return False

    print(f"Generating: {pattern_name}")
    print(f"  Source: {source_dir}")
    print(f"  Output: {output_file}")
    print(f"  API Kernel: {kernel_id}")
    print(f"  Header files: {len(header_files)}")
    print(f"  Problem files: {len(problem_files)}")
    print(f"  Footer files: {len(footer_files)}")

    # Compose document
    document = compose_document(config, header_files, problem_files, footer_files)

    if dry_run:
        print(f"  [DRY RUN] Would write {len(document)} characters")
        return True

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write output
    output_file.write_text(document, encoding="utf-8")
    print(f"  Written: {len(document)} characters")

    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate pattern documentation from source files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--pattern", "-p",
        help="Generate specific pattern (e.g., sliding_window)",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Generate all available patterns",
    )
    parser.add_argument(
        "--validate", "-v",
        action="store_true",
        help="Validate only, don't write files",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available patterns",
    )

    args = parser.parse_args()

    # List mode
    if args.list:
        patterns = get_available_patterns()
        if patterns:
            print("Available patterns:")
            for p in patterns:
                kernel_id = get_kernel_id_from_dir_name(p)
                print(f"  {p} -> {kernel_id}")
        else:
            print("No patterns found in meta/patterns/")
        return 0

    # Determine which patterns to generate
    if args.pattern:
        patterns_to_generate = [args.pattern]
    elif args.all:
        patterns_to_generate = get_available_patterns()
        if not patterns_to_generate:
            print("No patterns found to generate")
            return 1
    else:
        # Default: generate all
        patterns_to_generate = get_available_patterns()
        if not patterns_to_generate:
            parser.print_help()
            return 1

    # Generate
    success_count = 0
    fail_count = 0

    for pattern in patterns_to_generate:
        if generate_pattern_doc(pattern, dry_run=args.validate):
            success_count += 1
        else:
            fail_count += 1
        print()

    # Summary
    print(f"Summary: {success_count} succeeded, {fail_count} failed")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())



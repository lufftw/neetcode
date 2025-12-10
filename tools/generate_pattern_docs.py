#!/usr/bin/env python3
"""
Pattern Documentation Generator

Generates comprehensive pattern documentation by composing:
- Ontology definitions (api_kernels.toml, patterns.toml)
- Per-problem markdown snippets (meta/patterns/<kernel>/*.md)

Usage:
    python tools/generate_pattern_docs.py                    # Generate all
    python tools/generate_pattern_docs.py --pattern sliding_window
    python tools/generate_pattern_docs.py --validate         # Validate only
    python tools/generate_pattern_docs.py --list             # List available
"""

from __future__ import annotations

import argparse
import sys

from patterndocs import (
    PatternDocConfig,
    load_api_kernels,
    load_patterns,
    get_available_patterns,
    get_kernel_id_from_dir_name,
    collect_source_files,
    compose_document,
    META_PATTERNS_DIR,
    OUTPUT_DIR,
)


def generate_pattern_doc(pattern_name: str, dry_run: bool = False) -> bool:
    """Generate documentation for a specific pattern."""
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
    kernel_summary = kernel.summary if kernel else ""
    
    if not kernel:
        print(f"Warning: Kernel '{kernel_id}' not found in ontology")

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
    print(f"  Files: {len(header_files)} header, {len(problem_files)} problem, {len(footer_files)} footer")

    # Compose document
    document = compose_document(config, header_files, problem_files, footer_files)

    if dry_run:
        print(f"  [DRY RUN] Would write {len(document)} characters")
        return True

    # Write output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file.write_text(document, encoding="utf-8")
    print(f"  Written: {len(document)} characters")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate pattern documentation.")
    parser.add_argument("--pattern", "-p", help="Generate specific pattern")
    parser.add_argument("--all", "-a", action="store_true", help="Generate all patterns")
    parser.add_argument("--validate", "-v", action="store_true", help="Validate only")
    parser.add_argument("--list", "-l", action="store_true", help="List available patterns")

    args = parser.parse_args()

    if args.list:
        patterns = get_available_patterns()
        if patterns:
            print("Available patterns:")
            for p in patterns:
                print(f"  {p} -> {get_kernel_id_from_dir_name(p)}")
        else:
            print("No patterns found in meta/patterns/")
        return 0

    # Determine patterns to generate
    if args.pattern:
        patterns = [args.pattern]
    else:
        patterns = get_available_patterns()
        if not patterns:
            print("No patterns found to generate")
            return 1

    # Generate
    success, fail = 0, 0
    for pattern in patterns:
        if generate_pattern_doc(pattern, dry_run=args.validate):
            success += 1
        else:
            fail += 1
        print()

    print(f"Summary: {success} succeeded, {fail} failed")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

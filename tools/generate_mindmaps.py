#!/usr/bin/env python3
"""
Mind Map Generator for NeetCode Practice Framework

Generates Markmap-compatible mind maps from ontology and problem metadata.

Usage:
    python tools/generate_mindmaps.py                     # Generate all (MD only)
    python tools/generate_mindmaps.py --html              # Generate MD + HTML
    python tools/generate_mindmaps.py --type pattern      # Generate specific type
    python tools/generate_mindmaps.py --list              # List available types
    python tools/generate_mindmaps.py --convert file.md   # Convert MD to HTML
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mindmaps import (
    MINDMAP_TYPES,
    GENERATORS,
    DEFAULT_OUTPUT_DIR,
    PAGES_OUTPUT_DIR,
    META_DESCRIPTIONS_DIR,
    load_ontology,
    load_problems,
    generate_html_mindmap,
    setup_pages_directory,
    markmap_frontmatter,
    INDEX_HTML_TEMPLATE,
    CARD_TEMPLATE,
    get_config,
    post_process_content,
)

# Mind map metadata
TITLES = {
    "pattern-hierarchy": "Pattern Hierarchy",
    "family-derivation": "Family Derivation",
    "algorithm-usage": "Algorithm Usage",
    "data-structure": "Data Structure Usage",
    "company-coverage": "Company Coverage",
    "roadmap-paths": "Learning Roadmaps",
    "problem-relations": "Problem Relations",
    "solution-variants": "Solution Variants",
    "difficulty-topics": "Difficulty × Topics",
}

DESCRIPTIONS = {
    "pattern-hierarchy": ("📐", "API Kernels → Patterns → Problems hierarchy"),
    "family-derivation": ("👨‍👩‍👧‍👦", "Base templates and derived problem variants"),
    "algorithm-usage": ("⚡", "Which algorithms are used in which problems"),
    "data-structure": ("🏗️", "Data structures used across problems"),
    "company-coverage": ("🏢", "Problems frequently asked by companies"),
    "roadmap-paths": ("🗺️", "Learning roadmap structures"),
    "problem-relations": ("🔗", "Related problems network"),
    "solution-variants": ("🔀", "Problems with multiple solution approaches"),
    "difficulty-topics": ("📊", "Topics organized by difficulty level"),
}


def generate_all_mindmaps(
    output_dir: Path,
    types: list[str] | None = None,
    generate_html: bool = False,
    pages_dir: Path | None = None,
    use_autoloader: bool = False,
    enable_post_processing: bool = True,
) -> dict[str, str]:
    """Generate all or specified mindmaps."""
    print("Loading ontology...")
    ontology = load_ontology()
    print(f"  Loaded {len(ontology.api_kernels)} API kernels, {len(ontology.patterns)} patterns")

    print("Loading problems...")
    problems = load_problems()
    print(f"  Loaded {len(problems)} problems")

    if types is None:
        types = MINDMAP_TYPES

    output_dir.mkdir(parents=True, exist_ok=True)

    if generate_html:
        if pages_dir is None:
            pages_dir = PAGES_OUTPUT_DIR
        print(f"\nSetting up GitHub Pages: {pages_dir}")
        setup_pages_directory(pages_dir)

    results = {}
    for mm_type in types:
        if mm_type not in GENERATORS:
            print(f"Warning: Unknown type '{mm_type}'")
            continue

        print(f"\nGenerating: {mm_type}")
        content = GENERATORS[mm_type](ontology, problems)

        # Apply post-processing to add LeetCode and Solution links
        if enable_post_processing:
            print("  Applying post-processing (adding links)...")
            content = post_process_content(content, problems)

        output_file = output_dir / f"{mm_type}.md"
        output_file.write_text(content, encoding="utf-8")
        print(f"  Written: {output_file}")

        if generate_html and pages_dir:
            title = TITLES.get(mm_type, mm_type.replace("_", " ").title())
            # Get description from config file path, fallback to DESCRIPTIONS dict
            config = get_config()
            description_text = None
            if config.descriptions:
                description_path_str = config.descriptions.get(mm_type)
                if description_path_str:
                    # Treat as file path relative to tools/mindmaps/meta directory
                    description_path = META_DESCRIPTIONS_DIR / description_path_str
                    if description_path.exists() and description_path.is_file():
                        description_text = description_path.read_text(encoding="utf-8").strip()
            # Fallback to DESCRIPTIONS dict if file doesn't exist or not configured
            if not description_text:
                _, description_text = DESCRIPTIONS.get(mm_type, ("", ""))
            html = generate_html_mindmap(title, content, use_autoloader, description_text)
            html_file = pages_dir / "mindmaps" / f"{mm_type.replace('_', '-')}.html"
            html_file.write_text(html, encoding="utf-8")
            print(f"  Written: {html_file}")

        results[mm_type] = content

    return results


def convert_md_to_html(input_files: list[Path], output_dir: Path | None = None) -> None:
    """Convert MD files to HTML."""
    # Default output directory: docs/pages/mindmaps
    if output_dir is None:
        output_dir = PAGES_OUTPUT_DIR / "mindmaps"
    
    for input_file in input_files:
        if not input_file.exists():
            print(f"❌ File not found: {input_file}")
            continue
        
        content = input_file.read_text(encoding="utf-8")
        
        # Extract title and description from frontmatter
        title = input_file.stem.replace("_", " ").title()
        description = None
        if content.startswith("---"):
            in_frontmatter = True
            for line in content.split("\n")[1:]:
                if line.strip() == "---":
                    break
                if line.startswith("title:"):
                    title = line.replace("title:", "").strip().strip('"').strip("'")
                elif line.startswith("description:"):
                    description = line.replace("description:", "").strip().strip('"').strip("'")
        
        html_content = generate_html_mindmap(title, content, use_autoloader=False, description=description)
        
        output_file = output_dir / input_file.with_suffix(".html").name
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html_content, encoding="utf-8")
        print(f"✅ {input_file} → {output_file}")


def generate_index(output_dir: Path, generated_types: list[str]) -> None:
    """Generate index file for all mindmaps."""
    lines = [
        markmap_frontmatter("NeetCode Mind Maps Index", color_freeze_level=2),
        "# Mind Maps Index\n",
        "Visual mind maps of the NeetCode ontology and problem relationships.",
        "Use [markmap](https://markmap.js.org/) VSCode extension or web viewer.\n",
        "## Available Mind Maps\n",
    ]

    for mm_type in generated_types:
        icon, desc = DESCRIPTIONS.get(mm_type, ("", ""))
        title = f"{icon} {TITLES.get(mm_type, mm_type)}"
        lines.extend([f"### [{title}]({mm_type}.md)\n", f"{desc}\n"])

    lines.extend([
        "---\n",
        "## How to View\n",
        "### Option 1: VSCode Extension",
        "1. Install [markmap](https://marketplace.visualstudio.com/items?itemName=gera2ld.markmap-vscode)",
        "2. Open any `.md` file",
        "3. Click the markmap icon\n",
        "### Option 2: Web Viewer",
        "1. Go to [markmap.js.org](https://markmap.js.org/repl)",
        "2. Paste the markdown content\n",
        "---\n",
        "*Auto-generated by `tools/generate_mindmaps.py`*",
    ])

    (output_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nGenerated index: {output_dir / 'README.md'}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate mind maps from ontology.")
    parser.add_argument("--type", "-t", choices=MINDMAP_TYPES, help="Generate specific type")
    parser.add_argument("--all", "-a", action="store_true", help="Generate all types")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--html", action="store_true", help="Also generate HTML")
    parser.add_argument("--use-autoloader", action="store_true", help="Use markmap-autoloader")
    parser.add_argument("--pages-dir", type=Path, default=PAGES_OUTPUT_DIR)
    parser.add_argument("--list", "-l", action="store_true", help="List types")
    parser.add_argument("--convert", "-c", nargs="+", type=Path, help="Convert MD file(s) to HTML")
    parser.add_argument("--no-post-process", action="store_true", help="Disable post-processing (link addition)")

    args = parser.parse_args()

    # Convert mode
    if args.convert:
        # Use --output if specified, otherwise default to docs/pages/mindmaps
        output_dir = args.output if args.output != DEFAULT_OUTPUT_DIR else None
        convert_md_to_html(args.convert, output_dir)
        return 0

    if args.list:
        print("Available mindmap types:")
        for t in MINDMAP_TYPES:
            print(f"  {t}")
        return 0

    types = [args.type] if args.type else None
    results = generate_all_mindmaps(
        output_dir=args.output,
        types=types,
        generate_html=args.html,
        pages_dir=args.pages_dir if args.html else None,
        use_autoloader=args.use_autoloader,
        enable_post_processing=not args.no_post_process,
    )

    if results:
        generate_index(args.output, list(results.keys()))

    print(f"\n[OK] Generated {len(results)} mindmaps")
    print(f"   [MD] Markdown: {args.output}")
    if args.html:
        print(f"   [HTML] HTML: {args.pages_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

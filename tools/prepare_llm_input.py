#!/usr/bin/env python3
"""
Prepare Ontology Data for LLM Mind Map Generation

Formats your ontology data into a clean, LLM-friendly format that can be
copied and pasted into your prompt.

Recommended Model: GPT-5.1-codex (default) for best Markmap syntax understanding.

Usage:
    python tools/prepare_llm_input.py                    # Full output
    python tools/prepare_llm_input.py --compact          # Compact format
    python tools/prepare_llm_input.py --type patterns    # Specific type only
    python tools/prepare_llm_input.py --problems 10      # Include N problems
    python tools/prepare_llm_input.py --output data.txt  # Save to file
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from textwrap import dedent

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from mindmaps import load_ontology, load_problems
from mindmaps.data import ProblemData


def format_api_kernels(ontology, compact: bool = False) -> str:
    """Format API Kernels for LLM input."""
    lines = ["### API Kernels (核心演算法機制)", ""]
    
    if compact:
        for k in ontology.api_kernels:
            lines.append(f"- **{k.get('id')}**: {k.get('summary', '')}")
    else:
        for k in ontology.api_kernels:
            lines.extend([
                f"#### {k.get('id')}",
                f"- Summary: {k.get('summary', '')}",
                ""
            ])
    
    return "\n".join(lines)


def format_patterns(ontology, compact: bool = False) -> str:
    """Format Patterns grouped by API Kernel."""
    lines = ["### Patterns (解題模式)", ""]
    
    # Group by API Kernel
    by_kernel: dict[str, list] = {}
    for p in ontology.patterns:
        kernel = p.get("api_kernel", "Other")
        by_kernel.setdefault(kernel, []).append(p)
    
    for kernel, patterns in by_kernel.items():
        lines.append(f"#### {kernel}")
        for p in patterns:
            if compact:
                lines.append(f"- `{p.get('id')}`: {p.get('summary', '')}")
            else:
                lines.extend([
                    f"- **{p.get('id')}**",
                    f"  - {p.get('summary', '')}",
                ])
        lines.append("")
    
    return "\n".join(lines)


def format_algorithms(ontology, compact: bool = False) -> str:
    """Format Algorithms by kind."""
    lines = ["### Algorithms (演算法)", ""]
    
    # Group by kind
    by_kind: dict[str, list] = {}
    for a in ontology.algorithms:
        kind = a.get("kind", "other")
        by_kind.setdefault(kind, []).append(a)
    
    kind_labels = {
        "core": "🔷 Core Algorithms",
        "technique": "🔶 Techniques", 
        "paradigm": "🔹 Paradigms",
        "category": "📁 Categories",
    }
    
    for kind, algos in by_kind.items():
        lines.append(f"#### {kind_labels.get(kind, kind)}")
        for a in algos:
            parent = f" (parent: {a.get('parent')})" if a.get('parent') else ""
            if compact:
                lines.append(f"- `{a.get('id')}`{parent}: {a.get('summary', '')}")
            else:
                lines.extend([
                    f"- **{a.get('id')}**{parent}",
                    f"  - {a.get('summary', '')}",
                ])
        lines.append("")
    
    return "\n".join(lines)


def format_data_structures(ontology, compact: bool = False) -> str:
    """Format Data Structures."""
    lines = ["### Data Structures (資料結構)", ""]
    
    for ds in ontology.data_structures:
        parent = f" → {ds.get('parent')}" if ds.get('parent') else ""
        if compact:
            lines.append(f"- `{ds.get('id')}`{parent}: {ds.get('summary', '')}")
        else:
            lines.extend([
                f"- **{ds.get('id')}**{parent}",
                f"  - {ds.get('summary', '')}",
            ])
    
    return "\n".join(lines)


def format_families(ontology, compact: bool = False) -> str:
    """Format Problem Families."""
    lines = ["### Families (問題家族)", ""]
    
    for f in ontology.families:
        if compact:
            lines.append(f"- `{f.get('id')}`: {f.get('summary', '')}")
        else:
            lines.extend([
                f"- **{f.get('id')}**",
                f"  - {f.get('summary', '')}",
            ])
    
    return "\n".join(lines)


def format_topics(ontology, compact: bool = False) -> str:
    """Format Topics."""
    lines = ["### Topics (LeetCode 主題標籤)", ""]
    
    if compact:
        topic_ids = [t.get('id') for t in ontology.topics]
        lines.append(", ".join(f"`{t}`" for t in topic_ids))
    else:
        for t in ontology.topics:
            lines.append(f"- `{t.get('id')}`: {t.get('summary', '')}")
    
    return "\n".join(lines)


def format_roadmaps(ontology, compact: bool = False) -> str:
    """Format Roadmaps."""
    lines = ["### Roadmaps (學習路徑)", ""]
    
    for r in ontology.roadmaps:
        name = r.get('name', r.get('id'))
        url = r.get('url', '')
        if compact:
            lines.append(f"- **{name}**: {r.get('summary', '')}")
        else:
            url_part = f" ([link]({url}))" if url else ""
            lines.extend([
                f"- **{name}**{url_part}",
                f"  - {r.get('summary', '')}",
            ])
    
    return "\n".join(lines)


def format_difficulties(ontology) -> str:
    """Format Difficulties."""
    lines = ["### Difficulties (難度等級)", ""]
    
    icons = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    for d in ontology.difficulties:
        icon = icons.get(d.get('id'), "⚪")
        lines.append(f"- {icon} **{d.get('id').title()}** (Level {d.get('level', '?')}): {d.get('summary', '')}")
    
    return "\n".join(lines)


def format_companies(ontology, compact: bool = False) -> str:
    """Format Companies."""
    lines = ["### Companies (公司)", ""]
    
    if compact:
        company_names = [c.get('name', c.get('id')) for c in ontology.companies]
        lines.append(", ".join(company_names))
    else:
        for c in ontology.companies:
            lines.append(f"- **{c.get('name', c.get('id'))}** (`{c.get('id')}`)")
    
    return "\n".join(lines)


def format_problems(problems: dict[str, ProblemData], limit: int = 10) -> str:
    """Format Problem examples."""
    lines = ["### Problem Examples (題目範例)", ""]
    
    # Sort by leetcode_id
    sorted_probs = sorted(problems.values(), key=lambda p: p.leetcode_id)[:limit]
    
    diff_icons = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    
    for p in sorted_probs:
        icon = diff_icons.get(p.difficulty.lower(), "⚪")
        lines.extend([
            f"#### {p.leetcode_id}. {p.title} {icon}",
            f"- **URL**: {p.url}",
            f"- **Patterns**: {', '.join(f'`{x}`' for x in p.patterns) or 'N/A'}",
            f"- **API Kernels**: {', '.join(f'`{x}`' for x in p.api_kernels) or 'N/A'}",
            f"- **Data Structures**: {', '.join(f'`{x}`' for x in p.data_structures) or 'N/A'}",
            f"- **Algorithms**: {', '.join(f'`{x}`' for x in p.algorithms) or 'N/A'}",
            f"- **Related**: {', '.join(p.related_problems) or 'N/A'}",
            ""
        ])
    
    return "\n".join(lines)


def generate_llm_input(
    compact: bool = False,
    include_types: list[str] | None = None,
    problem_limit: int = 0,
) -> str:
    """Generate complete LLM input from ontology."""
    
    print("Loading ontology...", file=sys.stderr)
    ontology = load_ontology()
    
    problems = {}
    if problem_limit > 0:
        print("Loading problems...", file=sys.stderr)
        problems = load_problems()
    
    all_types = [
        "api_kernels", "patterns", "algorithms", "data_structures",
        "families", "topics", "difficulties", "companies", "roadmaps", "problems"
    ]
    
    if include_types is None:
        include_types = all_types
    
    formatters = {
        "api_kernels": lambda: format_api_kernels(ontology, compact),
        "patterns": lambda: format_patterns(ontology, compact),
        "algorithms": lambda: format_algorithms(ontology, compact),
        "data_structures": lambda: format_data_structures(ontology, compact),
        "families": lambda: format_families(ontology, compact),
        "topics": lambda: format_topics(ontology, compact),
        "difficulties": lambda: format_difficulties(ontology),
        "companies": lambda: format_companies(ontology, compact),
        "roadmaps": lambda: format_roadmaps(ontology, compact),
        "problems": lambda: format_problems(problems, problem_limit) if problems else "",
    }
    
    sections = []
    
    # Header
    sections.append(dedent("""
    # My Ontology Data for LeetCode Mind Map Generation
    
    Below is my knowledge graph data. Please use this to generate a Markmap mind map.
    
    > **Target Model**: GPT-5.1-codex (recommended for best Markmap syntax understanding)
    
    ---
    """).strip())
    
    for t in include_types:
        if t in formatters:
            content = formatters[t]()
            if content:
                sections.append(content)
    
    sections.append("\n---\n")
    
    return "\n\n".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare ontology data for LLM mind map generation."
    )
    parser.add_argument(
        "--compact", "-c", action="store_true",
        help="Use compact format (single line per item)"
    )
    parser.add_argument(
        "--type", "-t", action="append", dest="types",
        choices=["api_kernels", "patterns", "algorithms", "data_structures",
                 "families", "topics", "difficulties", "companies", "roadmaps", "problems"],
        help="Include only specific data types (can be repeated)"
    )
    parser.add_argument(
        "--problems", "-p", type=int, default=0,
        help="Include N problem examples (default: 0 = none)"
    )
    parser.add_argument(
        "--output", "-o", type=Path,
        help="Save output to file instead of stdout"
    )
    parser.add_argument(
        "--all", "-a", action="store_true",
        help="Include all data types including problems"
    )
    
    args = parser.parse_args()
    
    types = args.types
    problem_limit = args.problems
    
    if args.all:
        types = None
        problem_limit = 20
    
    output = generate_llm_input(
        compact=args.compact,
        include_types=types,
        problem_limit=problem_limit,
    )
    
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"✅ Saved to {args.output}", file=sys.stderr)
    else:
        print(output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())


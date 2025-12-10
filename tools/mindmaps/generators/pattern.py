# tools/mindmaps/generators/pattern.py
"""Pattern hierarchy mind map generator."""

from __future__ import annotations
from collections import defaultdict

from ..loader import OntologyData
from ..data import ProblemData
from ..helpers import markmap_frontmatter, format_problem_entry


def generate_pattern_hierarchy(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """Generate API Kernel → Patterns → Problems hierarchy."""
    lines = [
        markmap_frontmatter("Pattern Hierarchy - API Kernels → Patterns → Problems"),
        "# Pattern Hierarchy",
        "",
        "Algorithmic API Kernels and their pattern instantiations with example problems.",
        "",
    ]

    # Group patterns by kernel
    patterns_by_kernel: dict[str, list[dict]] = defaultdict(list)
    for p in ontology.patterns:
        patterns_by_kernel[p.get("api_kernel", "Unknown")].append(p)

    # Group problems by pattern
    problems_by_pattern: dict[str, list[ProblemData]] = defaultdict(list)
    for prob in problems.values():
        for pattern in prob.patterns:
            problems_by_pattern[pattern].append(prob)

    for kernel in ontology.api_kernels:
        kernel_id = kernel.get("id", "")
        kernel_desc = kernel.get("description", "")
        
        lines.append(f"## {kernel_id}")
        if kernel_desc:
            lines.extend(["", f"*{kernel_desc}*"])
        lines.append("")

        for pattern in patterns_by_kernel.get(kernel_id, []):
            pattern_id = pattern.get("id", "")
            pattern_desc = pattern.get("description", "")
            pattern_display = pattern_id.replace("_", " ").title()
            
            lines.append(f"### {pattern_display}")
            if pattern_desc:
                lines.extend(["", f"_{pattern_desc}_"])
            lines.append("")

            pattern_probs = problems_by_pattern.get(pattern_id, [])
            for prob in sorted(pattern_probs, key=lambda p: p.leetcode_id)[:8]:
                lines.append(f"- {format_problem_entry(prob, show_complexity=True)}")
            
            if not pattern_probs:
                lines.append("- *(No problems tagged yet)*")
            lines.append("")

    return "\n".join(lines)


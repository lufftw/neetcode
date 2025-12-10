# tools/mindmaps/generators/family.py
"""Family derivation mind map generator."""

from __future__ import annotations

from ..loader import OntologyData
from ..data import ProblemData
from ..helpers import markmap_frontmatter, format_problem_entry


def generate_family_derivation(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """Generate Problem Families with base/variant relationships."""
    lines = [
        markmap_frontmatter("Problem Family Derivation - Base Templates → Variants"),
        "# Problem Family Derivation",
        "",
        "Base template problems and their derived variants. Learn the base pattern first,",
        "then apply to variants with small modifications.",
        "",
    ]

    base_problems = [p for p in problems.values() if p.is_base_template]
    
    if not base_problems:
        lines.extend([
            "## No Base Templates Found",
            "",
            "- Add `is_base_template = true` to problem metadata to establish base templates.",
        ])
        return "\n".join(lines)

    for base in sorted(base_problems, key=lambda p: p.leetcode_id):
        kernel = base.base_for_kernel or "General"
        lines.extend([f"## {kernel}", ""])
        
        lines.extend([f"### 🎯 Base Template: {base.markdown_link(include_difficulty=False)}", ""])
        if base.solutions:
            notes = base.solutions[0].get("notes", "")
            if notes:
                lines.extend([f"> {notes}", ""])
        
        lines.extend(["### Derived Problems", ""])
        for derived_id in base.derived_problems:
            if derived_id in problems:
                lines.append(f"- {format_problem_entry(problems[derived_id], show_complexity=True)}")
            else:
                lines.append(f"- LeetCode {derived_id} *(metadata not yet added)*")
        
        if not base.derived_problems:
            lines.append("- *(No derived problems listed)*")
        lines.append("")

    return "\n".join(lines)


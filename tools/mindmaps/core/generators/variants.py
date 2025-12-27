# tools/mindmaps/generators/variants.py
"""Solution variants mind map generator."""

from __future__ import annotations

from ..loader import OntologyData
from ..data import ProblemData
from ..helpers import markmap_frontmatter


def generate_solution_variants(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """Generate Solution Variants for problems with multiple approaches."""
    lines = [
        markmap_frontmatter("Solution Variants - Multiple Approaches per Problem"),
        "# Solution Variants",
        "",
        "Problems with multiple solution approaches. Understanding different approaches",
        "deepens your algorithmic thinking.",
        "",
    ]

    multi_solution = sorted(
        [p for p in problems.values() if len(p.solutions) > 1],
        key=lambda p: (-len(p.solutions), p.leetcode_id)
    )

    if not multi_solution:
        lines.extend([
            "## No Multi-Solution Problems",
            "",
            "- Add multiple `[[solutions]]` sections to problem metadata.",
        ])
        return "\n".join(lines)

    for prob in multi_solution:
        lines.extend([
            f"## {prob.display_name}",
            "",
            f"**{prob.difficulty_icon} {prob.difficulty.title()}** — {len(prob.solutions)} approaches",
            "",
        ])
        
        link = prob.solution_link()
        if link:
            lines.extend([
                f'📁 <a href="{link}" target="_blank" rel="noopener noreferrer">View All Solutions</a>',
                "",
            ])
        
        for sol in prob.solutions:
            key = sol.get("key", "unknown")
            role = sol.get("role", "")
            sol_name = key.replace("_", " ").title()
            if role == "base":
                sol_name = f"🎯 {sol_name} (Base)"
            elif role == "variant":
                sol_name = f"🔄 {sol_name}"
            
            lines.append(f"### {sol_name}")
            variant = sol.get("variant", "")
            if variant:
                lines.extend(["", f"*Variant: {variant}*"])
            lines.append("")
            
            complexity = sol.get("complexity", "")
            delta = sol.get("delta", "")
            notes = sol.get("notes", "")
            
            if complexity:
                lines.append(f"- **Complexity:** `{complexity}`")
            if delta:
                lines.append(f"- **Delta from base:** {delta}")
            if notes:
                lines.append(f"- **Notes:** {notes}")
            if not (complexity or delta or notes):
                lines.append("- *(No additional notes)*")
            lines.append("")

    return "\n".join(lines)


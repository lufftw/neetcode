# tools/mindmaps/generators/relations.py
"""Problem relations mind map generator."""

from __future__ import annotations

from ..loader import OntologyData
from ..data import ProblemData
from ..helpers import markmap_frontmatter, format_problem_entry


def generate_problem_relations(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """Generate Related Problems network."""
    lines = [
        markmap_frontmatter("Problem Relations - Connected Problem Network"),
        "# Problem Relations Network",
        "",
        "Problems and their related problems. Practice related problems together to reinforce patterns.",
        "",
    ]

    problems_with_relations = sorted(
        [p for p in problems.values() if p.related_problems],
        key=lambda p: (-len(p.related_problems), p.leetcode_id)
    )

    for prob in problems_with_relations:
        lines.extend([
            f"## {prob.display_name}",
            "",
            f"**{prob.difficulty_icon} {prob.difficulty.title()}** — Topics: {', '.join(prob.topics[:3])}",
            "",
        ])
        
        link = prob.solution_link()
        if link:
            lines.extend([
                f'📁 <a href="{link}" target="_blank" rel="noopener noreferrer">View Solution</a>',
                "",
            ])
        
        lines.extend(["### Related Problems", ""])
        for related_id in prob.related_problems:
            if related_id in problems:
                lines.append(f"- {format_problem_entry(problems[related_id])}")
            else:
                lines.append(f"- LeetCode {related_id} *(metadata not yet added)*")
        lines.append("")

    return "\n".join(lines)


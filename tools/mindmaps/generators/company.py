# tools/mindmaps/generators/company.py
"""Company coverage mind map generator."""

from __future__ import annotations
from collections import defaultdict

from ..loader import OntologyData
from ..data import ProblemData
from ..config import DIFFICULTY_ICONS
from ..helpers import markmap_frontmatter


def generate_company_coverage(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """Generate Companies → Problems mapping."""
    lines = [
        markmap_frontmatter("Company Coverage - Companies → Interview Problems"),
        "# Company Interview Coverage",
        "",
        "Problems frequently asked by top tech companies. Prepare strategically!",
        "",
    ]

    problems_by_company: dict[str, list[ProblemData]] = defaultdict(list)
    for prob in problems.values():
        for company in prob.companies:
            problems_by_company[company].append(prob)

    for company, probs in sorted(problems_by_company.items(), key=lambda x: -len(x[1])):
        lines.extend([f"## {company.replace('_', ' ').title()} ({len(probs)} problems)", ""])
        
        by_diff: dict[str, list[ProblemData]] = defaultdict(list)
        for p in probs:
            by_diff[p.difficulty.lower()].append(p)
        
        for diff in ["easy", "medium", "hard"]:
            if by_diff[diff]:
                icon = DIFFICULTY_ICONS.get(diff, "")
                lines.extend([f"### {icon} {diff.title()}", ""])
                for prob in sorted(by_diff[diff], key=lambda p: p.leetcode_id):
                    lines.append(f"- {prob.markdown_link(include_difficulty=False)}")
                lines.append("")

    return "\n".join(lines)


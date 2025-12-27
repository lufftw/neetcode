# tools/mindmaps/generators/algorithm.py
"""Algorithm and data structure mind map generators."""

from __future__ import annotations
from collections import defaultdict

from ..loader import OntologyData
from ..data import ProblemData
from ..helpers import markmap_frontmatter, format_problem_entry


def generate_algorithm_usage(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """Generate Algorithms → Problems mapping."""
    lines = [
        markmap_frontmatter("Algorithm Usage - Algorithms → Problems"),
        "# Algorithm Usage",
        "",
        "Problems organized by the algorithms they use. Click links to view solution code.",
        "",
    ]

    problems_by_algo: dict[str, list[ProblemData]] = defaultdict(list)
    for prob in problems.values():
        for algo in prob.algorithms:
            problems_by_algo[algo].append(prob)

    diff_order = {"easy": 0, "medium": 1, "hard": 2}
    for algo, probs in sorted(problems_by_algo.items(), key=lambda x: -len(x[1])):
        lines.extend([f"## {algo.replace('_', ' ').title()} ({len(probs)} problems)", ""])
        sorted_probs = sorted(probs, key=lambda p: (diff_order.get(p.difficulty.lower(), 3), p.leetcode_id))
        for prob in sorted_probs:
            lines.append(f"- {format_problem_entry(prob)}")
        lines.append("")

    return "\n".join(lines)


def generate_data_structure(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """Generate Data Structures → Problems mapping."""
    lines = [
        markmap_frontmatter("Data Structure Usage - Data Structures → Problems"),
        "# Data Structure Usage",
        "",
        "Problems organized by the primary data structures they use.",
        "",
    ]

    problems_by_ds: dict[str, list[ProblemData]] = defaultdict(list)
    for prob in problems.values():
        for ds in prob.data_structures:
            problems_by_ds[ds].append(prob)

    diff_order = {"easy": 0, "medium": 1, "hard": 2}
    for ds, probs in sorted(problems_by_ds.items(), key=lambda x: -len(x[1])):
        lines.extend([f"## {ds.replace('_', ' ').title()} ({len(probs)} problems)", ""])
        sorted_probs = sorted(probs, key=lambda p: (diff_order.get(p.difficulty.lower(), 3), p.leetcode_id))
        for prob in sorted_probs:
            lines.append(f"- {format_problem_entry(prob)}")
        lines.append("")

    return "\n".join(lines)


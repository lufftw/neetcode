# tools/mindmaps/generators/roadmap.py
"""Roadmap paths mind map generator."""

from __future__ import annotations
from collections import defaultdict

from ..loader import OntologyData
from ..data import ProblemData
from ..config import DIFFICULTY_ICONS
from ..helpers import markmap_frontmatter, format_problem_entry


ROADMAP_INFO = {
    "neetcode_150": ("NeetCode 150", "Comprehensive coverage of essential patterns"),
    "blind_75": ("Blind 75", "The famous curated list for FAANG interviews"),
    "grind_75": ("Grind 75", "Updated Blind 75 with flexible scheduling"),
    "leetcode_top_100": ("LeetCode Top 100", "Most liked problems on LeetCode"),
    "sliding_window_path": ("Sliding Window Path", "Master the sliding window technique"),
    "graph_bfs_path": ("Graph BFS Path", "Breadth-first search patterns"),
}


def generate_roadmap_paths(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """Generate Learning Roadmaps structure."""
    lines = [
        markmap_frontmatter("Learning Roadmaps - Structured Problem Paths", color_freeze_level=3),
        "# Learning Roadmaps",
        "",
        "Curated problem sequences for different learning goals.",
        "",
    ]

    problems_by_roadmap: dict[str, list[ProblemData]] = defaultdict(list)
    for prob in problems.values():
        for roadmap in prob.roadmaps:
            problems_by_roadmap[roadmap].append(prob)

    for roadmap, probs in sorted(problems_by_roadmap.items()):
        display_name, description = ROADMAP_INFO.get(
            roadmap, (roadmap.replace("_", " ").title(), "")
        )
        lines.extend([f"## {display_name} ({len(probs)} problems)"])
        if description:
            lines.extend(["", f"*{description}*"])
        lines.append("")

        by_diff: dict[str, list[ProblemData]] = defaultdict(list)
        for p in probs:
            by_diff[p.difficulty.lower()].append(p)

        for diff in ["easy", "medium", "hard"]:
            if by_diff[diff]:
                icon = DIFFICULTY_ICONS.get(diff, "")
                lines.extend([f"### {icon} {diff.title()} ({len(by_diff[diff])})", ""])
                for prob in sorted(by_diff[diff], key=lambda p: p.leetcode_id):
                    lines.append(f"- {format_problem_entry(prob)}")
                lines.append("")

    return "\n".join(lines)


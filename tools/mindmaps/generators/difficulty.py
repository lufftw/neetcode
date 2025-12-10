# tools/mindmaps/generators/difficulty.py
"""Difficulty × Topics mind map generator."""

from __future__ import annotations
from collections import defaultdict

from ..loader import OntologyData
from ..data import ProblemData
from ..config import DIFFICULTY_ICONS
from ..helpers import markmap_frontmatter


def generate_difficulty_topics(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """Generate Difficulty × Topics matrix."""
    lines = [
        markmap_frontmatter("Difficulty × Topics - Topic Distribution by Difficulty"),
        "# Difficulty × Topics Matrix",
        "",
        "Topics organized by difficulty level. Start with Easy, progress to Hard.",
        "",
    ]

    by_diff_topic: dict[str, dict[str, list[ProblemData]]] = {
        "easy": defaultdict(list),
        "medium": defaultdict(list),
        "hard": defaultdict(list),
    }

    for prob in problems.values():
        diff = prob.difficulty.lower()
        if diff in by_diff_topic:
            for topic in prob.topics:
                by_diff_topic[diff][topic].append(prob)

    for diff in ["easy", "medium", "hard"]:
        icon = DIFFICULTY_ICONS.get(diff, "")
        total = sum(len(probs) for probs in by_diff_topic[diff].values())
        lines.extend([f"## {icon} {diff.title()} ({total} problems)", ""])

        for topic, probs in sorted(by_diff_topic[diff].items(), key=lambda x: -len(x[1])):
            lines.extend([f"### {topic.replace('_', ' ').title()} ({len(probs)})", ""])
            for prob in sorted(probs, key=lambda p: p.leetcode_id):
                lines.append(f"- {prob.markdown_link(include_difficulty=False)}")
            lines.append("")

    return "\n".join(lines)


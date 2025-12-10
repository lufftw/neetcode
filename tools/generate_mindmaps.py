#!/usr/bin/env python3
"""
Mind Map Generator for NeetCode Practice Framework

Generates multiple Markmap-compatible mind maps from ontology and problem metadata.
Output uses standard markdown with YAML frontmatter for markmap rendering.
Can also generate interactive HTML files for GitHub Pages deployment.

Usage:
    python tools/generate_mindmaps.py                     # Generate all mindmaps (MD only)
    python tools/generate_mindmaps.py --html              # Generate MD + HTML for GitHub Pages
    python tools/generate_mindmaps.py --type pattern      # Generate specific type
    python tools/generate_mindmaps.py --list              # List available types
    python tools/generate_mindmaps.py --output docs/mindmaps/  # Custom output dir

Mind Map Types:
    1. pattern_hierarchy  - API Kernel → Patterns → Problems
    2. family_derivation  - Problem Families with base/variant relationships
    3. algorithm_usage    - Algorithms → Problems
    4. data_structure     - Data Structures → Problems
    5. company_coverage   - Companies → Problems
    6. roadmap_paths      - Learning Roadmaps structure
    7. problem_relations  - Related problems network
    8. solution_variants  - Problems with multiple solutions
    9. difficulty_topics  - Difficulty × Topics matrix
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_DIR = PROJECT_ROOT / "ontology"
META_PROBLEMS_DIR = PROJECT_ROOT / "meta" / "problems"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "docs" / "mindmaps"
PAGES_OUTPUT_DIR = PROJECT_ROOT / "docs" / "pages"

# Mind map types
MINDMAP_TYPES = [
    "pattern_hierarchy",
    "family_derivation",
    "algorithm_usage",
    "data_structure",
    "company_coverage",
    "roadmap_paths",
    "problem_relations",
    "solution_variants",
    "difficulty_topics",
]

# Difficulty emoji indicators
DIFFICULTY_ICONS = {
    "easy": "🟢",
    "medium": "🟡",
    "hard": "🔴",
}


# ---------------------------------------------------------------------------
# TOML Parser (minimal implementation)
# ---------------------------------------------------------------------------

def parse_toml_simple(content: str) -> dict[str, Any]:
    """Simple TOML parser for our use case."""
    result: dict[str, Any] = {}
    current_array_name: str | None = None
    current_table_name: str | None = None
    current_item: dict[str, Any] = {}

    for line in content.splitlines():
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        # Array header: [[array_name]]
        if line.startswith("[[") and line.endswith("]]"):
            if current_array_name and current_item:
                if current_array_name not in result:
                    result[current_array_name] = []
                result[current_array_name].append(current_item)

            current_array_name = line[2:-2].strip()
            current_table_name = None
            current_item = {}
            continue

        # Table header: [table_name]
        if line.startswith("[") and line.endswith("]") and not line.startswith("[["):
            if current_array_name and current_item:
                if current_array_name not in result:
                    result[current_array_name] = []
                result[current_array_name].append(current_item)
                current_item = {}
                current_array_name = None

            current_table_name = line[1:-1].strip()
            if current_table_name not in result:
                result[current_table_name] = {}
            continue

        # Key-value pair
        if "=" in line:
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()

            # Parse value
            parsed_value = parse_toml_value(value)

            if current_array_name:
                current_item[key] = parsed_value
            elif current_table_name:
                result[current_table_name][key] = parsed_value
            else:
                result[key] = parsed_value

    # Don't forget the last item
    if current_array_name and current_item:
        if current_array_name not in result:
            result[current_array_name] = []
        result[current_array_name].append(current_item)

    return result


def parse_toml_value(value: str) -> Any:
    """Parse a TOML value."""
    # String
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]

    # Array
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        items = []
        for item in inner.split(","):
            item = item.strip()
            if item.startswith('"') and item.endswith('"'):
                items.append(item[1:-1])
            elif item:
                items.append(item)
        return items

    # Boolean
    if value == "true":
        return True
    if value == "false":
        return False

    # Number
    try:
        return int(value)
    except ValueError:
        pass

    return value


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

@dataclass
class OntologyData:
    """All ontology data."""
    api_kernels: list[dict] = field(default_factory=list)
    patterns: list[dict] = field(default_factory=list)
    families: list[dict] = field(default_factory=list)
    algorithms: list[dict] = field(default_factory=list)
    data_structures: list[dict] = field(default_factory=list)
    topics: list[dict] = field(default_factory=list)
    difficulties: list[dict] = field(default_factory=list)
    companies: list[dict] = field(default_factory=list)
    roadmaps: list[dict] = field(default_factory=list)


@dataclass
class ProblemData:
    """Problem metadata."""
    id: str
    title: str
    slug: str = ""
    leetcode_id: int = 0
    url: str = ""
    difficulty: str = ""
    topics: list[str] = field(default_factory=list)
    companies: list[str] = field(default_factory=list)
    roadmaps: list[str] = field(default_factory=list)
    api_kernels: list[str] = field(default_factory=list)
    patterns: list[str] = field(default_factory=list)
    families: list[str] = field(default_factory=list)
    data_structures: list[str] = field(default_factory=list)
    algorithms: list[str] = field(default_factory=list)
    related_problems: list[str] = field(default_factory=list)
    is_base_template: bool = False
    base_for_kernel: str = ""
    derived_problems: list[str] = field(default_factory=list)
    solutions: list[dict] = field(default_factory=list)
    # File locations
    solution_file: str = ""
    generator_file: str = ""
    
    @property
    def display_name(self) -> str:
        """Return formatted display name: LeetCode {number} - {title}"""
        num = self.leetcode_id if self.leetcode_id else int(self.id)
        return f"LeetCode {num} - {self.title}"
    
    @property
    def difficulty_icon(self) -> str:
        """Return difficulty indicator emoji."""
        return DIFFICULTY_ICONS.get(self.difficulty.lower(), "⚪")
    
    @property
    def solution_link(self) -> str:
        """Return relative link to solution file from docs/mindmaps/."""
        if self.solution_file:
            return f"../../{self.solution_file}"
        # Fallback: construct from slug
        if self.slug:
            return f"../../solutions/{self.slug}.py"
        return ""
    
    def markdown_link(self, include_difficulty: bool = True) -> str:
        """Return markdown link: [LeetCode N - Title](path)"""
        num = self.leetcode_id if self.leetcode_id else int(self.id)
        name = f"LeetCode {num} - {self.title}"
        link = self.solution_link
        
        if include_difficulty:
            icon = self.difficulty_icon
            if link:
                return f"{icon} [{name}]({link})"
            return f"{icon} {name}"
        else:
            if link:
                return f"[{name}]({link})"
            return name
    
    def leetcode_link(self) -> str:
        """Return markdown link to LeetCode problem page."""
        num = self.leetcode_id if self.leetcode_id else int(self.id)
        name = f"LeetCode {num} - {self.title}"
        if self.url:
            return f"[{name}]({self.url})"
        return name


def load_ontology() -> OntologyData:
    """Load all ontology files."""
    data = OntologyData()

    files_mapping = {
        "api_kernels.toml": "api_kernels",
        "patterns.toml": "patterns",
        "families.toml": "families",
        "algorithms.toml": "algorithms",
        "data_structures.toml": "data_structures",
        "topics.toml": "topics",
        "difficulties.toml": "difficulties",
        "companies.toml": "companies",
        "roadmaps.toml": "roadmaps",
    }

    for filename, attr in files_mapping.items():
        path = ONTOLOGY_DIR / filename
        if path.exists():
            content = path.read_text(encoding="utf-8")
            parsed = parse_toml_simple(content)
            # Get the array with the same name as attribute
            setattr(data, attr, parsed.get(attr, []))

    return data


def load_problems() -> dict[str, ProblemData]:
    """Load all problem metadata."""
    problems = {}

    if not META_PROBLEMS_DIR.exists():
        return problems

    for path in META_PROBLEMS_DIR.glob("*.toml"):
        content = path.read_text(encoding="utf-8")
        parsed = parse_toml_simple(content)

        # Get file locations
        files = parsed.get("files", {})
        
        problem = ProblemData(
            id=parsed.get("id", ""),
            title=parsed.get("title", ""),
            slug=parsed.get("slug", ""),
            leetcode_id=parsed.get("leetcode_id", 0),
            url=parsed.get("url", ""),
            difficulty=parsed.get("difficulty", ""),
            topics=parsed.get("topics", []),
            companies=parsed.get("companies", []),
            roadmaps=parsed.get("roadmaps", []),
            api_kernels=parsed.get("api_kernels", []),
            patterns=parsed.get("patterns", []),
            families=parsed.get("families", []),
            data_structures=parsed.get("data_structures", []),
            algorithms=parsed.get("algorithms", []),
            related_problems=parsed.get("related_problems", []),
            solutions=parsed.get("solutions", []),
            solution_file=files.get("solution", "") if isinstance(files, dict) else "",
            generator_file=files.get("generator", "") if isinstance(files, dict) else "",
        )

        # Pattern role
        pattern_role = parsed.get("pattern_role", {})
        if pattern_role:
            problem.is_base_template = pattern_role.get("is_base_template", False)
            problem.base_for_kernel = pattern_role.get("base_for_kernel", "")
            problem.derived_problems = pattern_role.get("derived_problems", [])

        problems[problem.id] = problem

    return problems


# ---------------------------------------------------------------------------
# Markmap Helpers
# ---------------------------------------------------------------------------

def markmap_frontmatter(title: str, color_freeze_level: int = 2) -> str:
    """Generate YAML frontmatter for markmap."""
    return f"""---
title: {title}
markmap:
  colorFreezeLevel: {color_freeze_level}
  maxWidth: 400
---
"""


def format_problem_entry(prob: ProblemData, show_complexity: bool = False) -> str:
    """Format a problem entry with link and metadata."""
    entry = prob.markdown_link(include_difficulty=True)
    
    if show_complexity and prob.solutions:
        sol = prob.solutions[0]
        complexity = sol.get("complexity", "")
        if complexity:
            entry += f" — `{complexity}`"
    
    return entry


# ---------------------------------------------------------------------------
# Mind Map Generators (Markmap Format)
# ---------------------------------------------------------------------------

def generate_pattern_hierarchy(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """
    Generate API Kernel → Patterns → Problems hierarchy.
    
    Shows the relationship between algorithmic kernels, their instantiation patterns,
    and the specific problems that use them.
    """
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
        kernel = p.get("api_kernel", "Unknown")
        patterns_by_kernel[kernel].append(p)

    # Group problems by pattern
    problems_by_pattern: dict[str, list[ProblemData]] = defaultdict(list)
    for prob in problems.values():
        for pattern in prob.patterns:
            problems_by_pattern[pattern].append(prob)

    for kernel in ontology.api_kernels:
        kernel_id = kernel.get("id", "")
        kernel_desc = kernel.get("description", "")
        
        # API Kernel as H2
        lines.append(f"## {kernel_id}")
        if kernel_desc:
            lines.append(f"")
            lines.append(f"*{kernel_desc}*")
        lines.append("")

        kernel_patterns = patterns_by_kernel.get(kernel_id, [])
        for pattern in kernel_patterns:
            pattern_id = pattern.get("id", "")
            pattern_desc = pattern.get("description", "")
            
            # Pattern as H3
            pattern_display = pattern_id.replace("_", " ").title()
            lines.append(f"### {pattern_display}")
            if pattern_desc:
                lines.append(f"")
                lines.append(f"_{pattern_desc}_")
            lines.append("")

            # Problems as list items
            pattern_probs = problems_by_pattern.get(pattern_id, [])
            for prob in sorted(pattern_probs, key=lambda p: p.leetcode_id)[:8]:
                lines.append(f"- {format_problem_entry(prob, show_complexity=True)}")
            
            if not pattern_probs:
                lines.append("- *(No problems tagged yet)*")
            lines.append("")

    return "\n".join(lines)


def generate_family_derivation(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """
    Generate Problem Families with base/variant relationships.
    
    Shows which problems are "base templates" and which are derived variants.
    """
    lines = [
        markmap_frontmatter("Problem Family Derivation - Base Templates → Variants"),
        "# Problem Family Derivation",
        "",
        "Base template problems and their derived variants. Learn the base pattern first,",
        "then apply to variants with small modifications.",
        "",
    ]

    # Find base templates
    base_problems = [p for p in problems.values() if p.is_base_template]
    
    if not base_problems:
        lines.append("## No Base Templates Found")
        lines.append("")
        lines.append("- Add `is_base_template = true` to problem metadata to establish base templates.")
        return "\n".join(lines)

    for base in sorted(base_problems, key=lambda p: p.leetcode_id):
        kernel = base.base_for_kernel or "General"
        
        lines.append(f"## {kernel}")
        lines.append("")
        
        # Base problem
        lines.append(f"### 🎯 Base Template: {base.markdown_link(include_difficulty=False)}")
        lines.append("")
        if base.solutions:
            notes = base.solutions[0].get("notes", "")
            if notes:
                lines.append(f"> {notes}")
                lines.append("")
        
        # Derived problems
        lines.append("### Derived Problems")
        lines.append("")
        for derived_id in base.derived_problems:
            if derived_id in problems:
                derived = problems[derived_id]
                lines.append(f"- {format_problem_entry(derived, show_complexity=True)}")
            else:
                lines.append(f"- LeetCode {derived_id} *(metadata not yet added)*")
        
        if not base.derived_problems:
            lines.append("- *(No derived problems listed)*")
        lines.append("")

    return "\n".join(lines)


def generate_algorithm_usage(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """
    Generate Algorithms → Problems mapping.
    
    Shows which algorithms are used across different problems.
    """
    lines = [
        markmap_frontmatter("Algorithm Usage - Algorithms → Problems"),
        "# Algorithm Usage",
        "",
        "Problems organized by the algorithms they use. Click links to view solution code.",
        "",
    ]

    # Group problems by algorithm
    problems_by_algo: dict[str, list[ProblemData]] = defaultdict(list)
    for prob in problems.values():
        for algo in prob.algorithms:
            problems_by_algo[algo].append(prob)

    # Sort by number of problems
    sorted_algos = sorted(problems_by_algo.items(), key=lambda x: -len(x[1]))

    for algo, probs in sorted_algos:
        algo_display = algo.replace("_", " ").title()
        count = len(probs)
        
        lines.append(f"## {algo_display} ({count} problems)")
        lines.append("")
        
        # Sort by difficulty then by ID
        diff_order = {"easy": 0, "medium": 1, "hard": 2}
        sorted_probs = sorted(probs, key=lambda p: (diff_order.get(p.difficulty.lower(), 3), p.leetcode_id))
        
        for prob in sorted_probs:
            lines.append(f"- {format_problem_entry(prob)}")
        lines.append("")

    return "\n".join(lines)


def generate_data_structure(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """
    Generate Data Structures → Problems mapping.
    
    Shows which data structures are used across different problems.
    """
    lines = [
        markmap_frontmatter("Data Structure Usage - Data Structures → Problems"),
        "# Data Structure Usage",
        "",
        "Problems organized by the primary data structures they use.",
        "",
    ]

    # Group problems by data structure
    problems_by_ds: dict[str, list[ProblemData]] = defaultdict(list)
    for prob in problems.values():
        for ds in prob.data_structures:
            problems_by_ds[ds].append(prob)

    # Sort by number of problems
    sorted_ds = sorted(problems_by_ds.items(), key=lambda x: -len(x[1]))

    for ds, probs in sorted_ds:
        ds_display = ds.replace("_", " ").title()
        count = len(probs)
        
        lines.append(f"## {ds_display} ({count} problems)")
        lines.append("")
        
        diff_order = {"easy": 0, "medium": 1, "hard": 2}
        sorted_probs = sorted(probs, key=lambda p: (diff_order.get(p.difficulty.lower(), 3), p.leetcode_id))
        
        for prob in sorted_probs:
            lines.append(f"- {format_problem_entry(prob)}")
        lines.append("")

    return "\n".join(lines)


def generate_company_coverage(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """
    Generate Companies → Problems mapping.
    
    Shows which companies frequently ask which problems.
    """
    lines = [
        markmap_frontmatter("Company Coverage - Companies → Interview Problems"),
        "# Company Interview Coverage",
        "",
        "Problems frequently asked by top tech companies. Prepare strategically!",
        "",
    ]

    # Group problems by company
    problems_by_company: dict[str, list[ProblemData]] = defaultdict(list)
    for prob in problems.values():
        for company in prob.companies:
            problems_by_company[company].append(prob)

    # Sort by number of problems, take top companies
    sorted_companies = sorted(problems_by_company.items(), key=lambda x: -len(x[1]))

    for company, probs in sorted_companies:
        company_display = company.replace("_", " ").title()
        count = len(probs)
        
        lines.append(f"## {company_display} ({count} problems)")
        lines.append("")
        
        # Group by difficulty
        by_diff: dict[str, list[ProblemData]] = defaultdict(list)
        for p in probs:
            by_diff[p.difficulty.lower()].append(p)
        
        for diff in ["easy", "medium", "hard"]:
            if by_diff[diff]:
                icon = DIFFICULTY_ICONS.get(diff, "")
                lines.append(f"### {icon} {diff.title()}")
                lines.append("")
                for prob in sorted(by_diff[diff], key=lambda p: p.leetcode_id):
                    lines.append(f"- {prob.markdown_link(include_difficulty=False)}")
                lines.append("")

    return "\n".join(lines)


def generate_roadmap_paths(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """
    Generate Learning Roadmaps structure.
    
    Shows different learning paths and their problem progressions.
    """
    lines = [
        markmap_frontmatter("Learning Roadmaps - Structured Problem Paths", color_freeze_level=3),
        "# Learning Roadmaps",
        "",
        "Curated problem sequences for different learning goals.",
        "",
    ]

    # Group problems by roadmap
    problems_by_roadmap: dict[str, list[ProblemData]] = defaultdict(list)
    for prob in problems.values():
        for roadmap in prob.roadmaps:
            problems_by_roadmap[roadmap].append(prob)

    # Define roadmap display names and descriptions
    roadmap_info = {
        "neetcode_150": ("NeetCode 150", "Comprehensive coverage of essential patterns"),
        "blind_75": ("Blind 75", "The famous curated list for FAANG interviews"),
        "grind_75": ("Grind 75", "Updated Blind 75 with flexible scheduling"),
        "leetcode_top_100": ("LeetCode Top 100", "Most liked problems on LeetCode"),
        "sliding_window_path": ("Sliding Window Path", "Master the sliding window technique"),
        "graph_bfs_path": ("Graph BFS Path", "Breadth-first search patterns"),
    }

    for roadmap, probs in sorted(problems_by_roadmap.items()):
        info = roadmap_info.get(roadmap, (roadmap.replace("_", " ").title(), ""))
        display_name, description = info
        
        lines.append(f"## {display_name} ({len(probs)} problems)")
        if description:
            lines.append(f"")
            lines.append(f"*{description}*")
        lines.append("")

        # Group by difficulty
        by_diff: dict[str, list[ProblemData]] = defaultdict(list)
        for p in probs:
            by_diff[p.difficulty.lower()].append(p)

        for diff in ["easy", "medium", "hard"]:
            if by_diff[diff]:
                icon = DIFFICULTY_ICONS.get(diff, "")
                lines.append(f"### {icon} {diff.title()} ({len(by_diff[diff])})")
                lines.append("")
                for prob in sorted(by_diff[diff], key=lambda p: p.leetcode_id):
                    lines.append(f"- {format_problem_entry(prob)}")
                lines.append("")

    return "\n".join(lines)


def generate_problem_relations(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """
    Generate Related Problems network.
    
    Shows how problems are connected to each other.
    """
    lines = [
        markmap_frontmatter("Problem Relations - Connected Problem Network"),
        "# Problem Relations Network",
        "",
        "Problems and their related problems. Practice related problems together to reinforce patterns.",
        "",
    ]

    # Only show problems with relations
    problems_with_relations = [p for p in problems.values() if p.related_problems]
    problems_with_relations.sort(key=lambda p: (-len(p.related_problems), p.leetcode_id))

    for prob in problems_with_relations:
        lines.append(f"## {prob.display_name}")
        lines.append("")
        lines.append(f"**{prob.difficulty_icon} {prob.difficulty.title()}** — Topics: {', '.join(prob.topics[:3])}")
        lines.append("")
        
        # Solution link
        if prob.solution_link:
            lines.append(f"📁 [View Solution]({prob.solution_link})")
            lines.append("")
        
        lines.append("### Related Problems")
        lines.append("")
        for related_id in prob.related_problems:
            if related_id in problems:
                related = problems[related_id]
                lines.append(f"- {format_problem_entry(related)}")
            else:
                lines.append(f"- LeetCode {related_id} *(metadata not yet added)*")
        lines.append("")

    return "\n".join(lines)


def generate_solution_variants(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """
    Generate Solution Variants for problems.
    
    Shows problems with multiple solution approaches.
    """
    lines = [
        markmap_frontmatter("Solution Variants - Multiple Approaches per Problem"),
        "# Solution Variants",
        "",
        "Problems with multiple solution approaches. Understanding different approaches",
        "deepens your algorithmic thinking.",
        "",
    ]

    # Find problems with multiple solutions
    multi_solution_problems = [p for p in problems.values() if len(p.solutions) > 1]
    multi_solution_problems.sort(key=lambda p: (-len(p.solutions), p.leetcode_id))

    if not multi_solution_problems:
        lines.append("## No Multi-Solution Problems")
        lines.append("")
        lines.append("- Add multiple `[[solutions]]` sections to problem metadata.")
        return "\n".join(lines)

    for prob in multi_solution_problems:
        lines.append(f"## {prob.display_name}")
        lines.append("")
        lines.append(f"**{prob.difficulty_icon} {prob.difficulty.title()}** — {len(prob.solutions)} approaches")
        lines.append("")
        
        if prob.solution_link:
            lines.append(f"📁 [View All Solutions]({prob.solution_link})")
            lines.append("")
        
        for sol in prob.solutions:
            key = sol.get("key", "unknown")
            role = sol.get("role", "")
            variant = sol.get("variant", "")
            complexity = sol.get("complexity", "")
            notes = sol.get("notes", "")
            delta = sol.get("delta", "")
            
            # Format solution name
            sol_name = key.replace("_", " ").title()
            if role == "base":
                sol_name = f"🎯 {sol_name} (Base)"
            elif role == "variant":
                sol_name = f"🔄 {sol_name}"
            
            lines.append(f"### {sol_name}")
            if variant:
                lines.append(f"")
                lines.append(f"*Variant: {variant}*")
            lines.append("")
            
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


def generate_difficulty_topics(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
    """
    Generate Difficulty × Topics matrix.
    
    Shows topics organized by difficulty level.
    """
    lines = [
        markmap_frontmatter("Difficulty × Topics - Topic Distribution by Difficulty"),
        "# Difficulty × Topics Matrix",
        "",
        "Topics organized by difficulty level. Start with Easy, progress to Hard.",
        "",
    ]

    # Group by difficulty, then by topic
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
        lines.append(f"## {icon} {diff.title()} ({total} problems)")
        lines.append("")

        # Sort topics by problem count
        sorted_topics = sorted(by_diff_topic[diff].items(), key=lambda x: -len(x[1]))

        for topic, probs in sorted_topics:
            topic_display = topic.replace("_", " ").title()
            lines.append(f"### {topic_display} ({len(probs)})")
            lines.append("")
            for prob in sorted(probs, key=lambda p: p.leetcode_id):
                lines.append(f"- {prob.markdown_link(include_difficulty=False)}")
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# HTML Generation for GitHub Pages
# ---------------------------------------------------------------------------

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - NeetCode Mind Maps</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ height: 100%; }}
        .markmap {{ width: 100%; height: 100%; }}
        .markmap > svg {{ width: 100%; height: 100%; }}
    </style>
    <script>
        window.markmap = {{
            autoLoader: {{
                toolbar: true,
                onReady: function() {{
                    setTimeout(function() {{
                        // Get markmap instance
                        var svg = document.querySelector('.markmap > svg');
                        var mm = svg?.__bindings__?.bindEls?.();
                        
                        document.querySelectorAll('.mm-toolbar').forEach(function(toolbar) {{
                            // Remove dark mode button
                            toolbar.querySelectorAll('.mm-toolbar-item').forEach(function(item) {{
                                var title = (item.title || '').toLowerCase();
                                if (title.includes('dark')) item.remove();
                            }});
                            
                            // Replace brand - smaller, subtle color
                            var brand = toolbar.querySelector('.mm-toolbar-brand');
                            if (brand) {{
                                brand.innerHTML = '🟡 NeetCode';
                                brand.href = '#';
                                brand.onclick = function(e) {{ e.preventDefault(); }};
                                brand.style.fontSize = '12px';
                                brand.style.color = '#666';
                            }}
                        }});
                    }}, 200);
                }}
            }}
        }};
        
        // Global functions for buttons
        function fitView() {{
            var svg = document.querySelector('.markmap > svg');
            if (svg && svg.mm) svg.mm.fit();
        }}
        function expandAll() {{
            var svg = document.querySelector('.markmap > svg');
            if (svg && svg.mm) {{
                var root = svg.mm.state.data;
                (function expand(n) {{
                    n.payload = Object.assign({{}}, n.payload, {{ fold: 0 }});
                    if (n.children) n.children.forEach(expand);
                }})(root);
                svg.mm.setData(root);
                svg.mm.fit();
            }}
        }}
        function collapseAll() {{
            var svg = document.querySelector('.markmap > svg');
            if (svg && svg.mm) {{
                var root = svg.mm.state.data;
                root.children && root.children.forEach(function collapse(n) {{
                    if (n.children && n.children.length) {{
                        n.payload = Object.assign({{}}, n.payload, {{ fold: 1 }});
                        n.children.forEach(collapse);
                    }}
                }});
                svg.mm.setData(root);
                svg.mm.fit();
            }}
        }}
    </script>
    <style>
        #topbar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
            background: #fff;
            border-bottom: 1px solid #e5e7eb;
            padding: 8px 16px;
            display: flex;
            gap: 8px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 13px;
        }}
        #topbar button {{
            padding: 4px 12px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            background: #fff;
            cursor: pointer;
        }}
        #topbar button:hover {{ background: #f3f4f6; }}
        .markmap {{ margin-top: 40px; height: calc(100% - 40px); }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
</head>
<body>
    <div id="topbar">
        <button onclick="fitView()">Fit View</button>
        <button onclick="expandAll()">Expand All</button>
        <button onclick="collapseAll()">Collapse All</button>
    </div>
    <div class="markmap">
{markdown_content}
    </div>
</body>
</html>
'''

INDEX_HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeetCode Mind Maps</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🧠 <span>NeetCode</span> Mind Maps</h1>
            <p class="subtitle">Interactive visualizations of algorithm patterns and problem relationships</p>
        </header>
        
        <section>
            <h2>Available Mind Maps</h2>
            <div class="grid">
{cards}
            </div>
        </section>
        
        <section class="tips">
            <h2>Navigation</h2>
            <ul>
                <li><strong>Drag</strong> — Move around</li>
                <li><strong>Scroll</strong> — Zoom in/out</li>
                <li><strong>Click node</strong> — Expand/collapse</li>
                <li><strong>Toolbar</strong> — Fit, zoom, fullscreen</li>
            </ul>
        </section>
        
        <footer>
            <p>Part of <a href="https://github.com/yourusername/neetcode">NeetCode Practice Framework</a></p>
            <p class="meta">Generated by <code>generate_mindmaps.py --html</code></p>
        </footer>
    </div>
</body>
</html>
'''

STYLE_CSS = ''':root {
    --bg: #ffffff;
    --bg-secondary: #f6f8fa;
    --border: #d0d7de;
    --text: #24292f;
    --text-muted: #57606a;
    --link: #0969da;
    --accent: #f59e0b;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
}

.container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 3rem 2rem;
}

header {
    text-align: center;
    margin-bottom: 3rem;
}

h1 {
    font-size: 2.2rem;
    margin-bottom: 0.5rem;
    color: var(--text);
}

h1 span {
    color: var(--accent);
}

.subtitle {
    color: var(--text-muted);
    font-size: 1rem;
}

h2 {
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
    color: var(--text);
    font-weight: 600;
}

section {
    margin-bottom: 3rem;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
}

.card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem;
    text-decoration: none;
    color: var(--text);
    transition: all 0.15s ease;
    display: block;
}

.card:hover {
    border-color: var(--link);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card .icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.card h3 {
    color: var(--link);
    margin-bottom: 0.25rem;
    font-size: 1rem;
    font-weight: 600;
}

.card p {
    color: var(--text-muted);
    font-size: 0.85rem;
    margin: 0;
}

.tips {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
}

.tips h2 {
    margin-bottom: 1rem;
}

.tips ul {
    list-style: none;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.75rem;
}

.tips li {
    color: var(--text-muted);
    font-size: 0.85rem;
}

footer {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 0.85rem;
}

footer a {
    color: var(--link);
    text-decoration: none;
}

footer a:hover {
    text-decoration: underline;
}

footer .meta {
    margin-top: 0.5rem;
    font-size: 0.8rem;
}

footer code {
    background: var(--bg-secondary);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.85em;
}
'''

CARD_TEMPLATE = '''                <a href="mindmaps/{filename}.html" class="card">
                    <div class="icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </a>'''


def markdown_to_html_content(markdown_content: str) -> str:
    """
    Extract the markdown content (without YAML frontmatter) for HTML embedding.
    """
    lines = markdown_content.split("\n")
    
    # Skip YAML frontmatter
    if lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                lines = lines[i + 1:]
                break
    
    # Clean up markdown for embedding
    content = "\n".join(lines)
    return content


def generate_html_mindmap(title: str, markdown_content: str) -> str:
    """Generate an HTML file with embedded markmap for a mind map."""
    # Extract content without frontmatter
    content = markdown_to_html_content(markdown_content)
    
    return HTML_TEMPLATE.format(
        title=title,
        markdown_content=content,
    )


def setup_pages_directory(pages_dir: Path) -> None:
    """Create the GitHub Pages directory structure."""
    # Create directories
    (pages_dir / "mindmaps").mkdir(parents=True, exist_ok=True)
    (pages_dir / "assets").mkdir(parents=True, exist_ok=True)
    
    # Write style.css
    style_path = pages_dir / "assets" / "style.css"
    style_path.write_text(STYLE_CSS, encoding="utf-8")
    print(f"  Written: {style_path}")


# ---------------------------------------------------------------------------
# Main Generator
# ---------------------------------------------------------------------------

GENERATORS = {
    "pattern_hierarchy": generate_pattern_hierarchy,
    "family_derivation": generate_family_derivation,
    "algorithm_usage": generate_algorithm_usage,
    "data_structure": generate_data_structure,
    "company_coverage": generate_company_coverage,
    "roadmap_paths": generate_roadmap_paths,
    "problem_relations": generate_problem_relations,
    "solution_variants": generate_solution_variants,
    "difficulty_topics": generate_difficulty_topics,
}


def generate_all_mindmaps(
    output_dir: Path,
    types: list[str] | None = None,
    generate_html: bool = False,
    pages_dir: Path | None = None,
) -> dict[str, str]:
    """Generate all or specified mindmaps."""
    # Load data
    print("Loading ontology...")
    ontology = load_ontology()
    print(f"  Loaded {len(ontology.api_kernels)} API kernels")
    print(f"  Loaded {len(ontology.patterns)} patterns")
    print(f"  Loaded {len(ontology.algorithms)} algorithms")

    print("Loading problems...")
    problems = load_problems()
    print(f"  Loaded {len(problems)} problems")

    # Determine which types to generate
    if types is None:
        types = MINDMAP_TYPES

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Setup pages directory if generating HTML
    if generate_html:
        if pages_dir is None:
            pages_dir = PAGES_OUTPUT_DIR
        print(f"\nSetting up GitHub Pages directory: {pages_dir}")
        setup_pages_directory(pages_dir)

    results = {}
    
    # Title mapping for HTML
    titles = {
        "pattern_hierarchy": "Pattern Hierarchy",
        "family_derivation": "Family Derivation",
        "algorithm_usage": "Algorithm Usage",
        "data_structure": "Data Structure Usage",
        "company_coverage": "Company Coverage",
        "roadmap_paths": "Learning Roadmaps",
        "problem_relations": "Problem Relations",
        "solution_variants": "Solution Variants",
        "difficulty_topics": "Difficulty × Topics",
    }
    
    for mindmap_type in types:
        if mindmap_type not in GENERATORS:
            print(f"Warning: Unknown mindmap type '{mindmap_type}'")
            continue

        print(f"\nGenerating: {mindmap_type}")
        generator = GENERATORS[mindmap_type]
        content = generator(ontology, problems)

        # Write Markdown file
        output_file = output_dir / f"{mindmap_type}.md"
        output_file.write_text(content, encoding="utf-8")
        print(f"  Written: {output_file}")

        # Write HTML file if requested
        if generate_html and pages_dir:
            title = titles.get(mindmap_type, mindmap_type.replace("_", " ").title())
            html_content = generate_html_mindmap(title, content)
            html_file = pages_dir / "mindmaps" / f"{mindmap_type}.html"
            html_file.write_text(html_content, encoding="utf-8")
            print(f"  Written: {html_file}")

        results[mindmap_type] = content

    # Generate index.html for GitHub Pages
    return results


def generate_index(output_dir: Path, generated_types: list[str]) -> None:
    """Generate index file for all mindmaps."""
    lines = [
        markmap_frontmatter("NeetCode Mind Maps Index", color_freeze_level=2),
        "# Mind Maps Index",
        "",
        "Visual mind maps of the NeetCode ontology and problem relationships.",
        "Use [markmap](https://markmap.js.org/) VSCode extension or web viewer to render these files.",
        "",
        "## Available Mind Maps",
        "",
    ]

    descriptions = {
        "pattern_hierarchy": ("📐 Pattern Hierarchy", "API Kernels → Patterns → Problems hierarchy"),
        "family_derivation": ("👨‍👩‍👧‍👦 Family Derivation", "Base templates and derived problem variants"),
        "algorithm_usage": ("⚡ Algorithm Usage", "Which algorithms are used in which problems"),
        "data_structure": ("🏗️ Data Structure Usage", "Data structures used across problems"),
        "company_coverage": ("🏢 Company Coverage", "Problems frequently asked by companies"),
        "roadmap_paths": ("🗺️ Learning Roadmaps", "Learning roadmap structures"),
        "problem_relations": ("🔗 Problem Relations", "Related problems network"),
        "solution_variants": ("🔀 Solution Variants", "Problems with multiple solution approaches"),
        "difficulty_topics": ("📊 Difficulty × Topics", "Topics organized by difficulty level"),
    }

    for mm_type in generated_types:
        info = descriptions.get(mm_type, (mm_type.replace("_", " ").title(), ""))
        title, desc = info
        lines.append(f"### [{title}]({mm_type}.md)")
        lines.append(f"")
        lines.append(f"{desc}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## How to View",
        "",
        "### Option 1: VSCode Extension",
        "1. Install [markmap](https://marketplace.visualstudio.com/items?itemName=gera2ld.markmap-vscode) extension",
        "2. Open any `.md` file",
        "3. Click the markmap icon in the top-right",
        "",
        "### Option 2: Web Viewer",
        "1. Go to [markmap.js.org](https://markmap.js.org/repl)",
        "2. Paste the markdown content",
        "",
        "---",
        "",
        "## Regenerate",
        "",
        "```bash",
        "python tools/generate_mindmaps.py",
        "```",
        "",
        "---",
        "",
        "*Auto-generated by `tools/generate_mindmaps.py`*",
    ])

    index_file = output_dir / "README.md"
    index_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nGenerated index: {index_file}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate mind maps from ontology and problem metadata.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/generate_mindmaps.py              # Generate Markdown only
  python tools/generate_mindmaps.py --html       # Generate Markdown + HTML for GitHub Pages
  python tools/generate_mindmaps.py -t pattern   # Generate specific type
        """,
    )
    parser.add_argument(
        "--type", "-t",
        choices=MINDMAP_TYPES,
        help="Generate specific mindmap type",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Generate all mindmap types (default)",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for Markdown files (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Also generate interactive HTML files for GitHub Pages",
    )
    parser.add_argument(
        "--pages-dir",
        type=Path,
        default=PAGES_OUTPUT_DIR,
        help=f"Output directory for GitHub Pages (default: {PAGES_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available mindmap types",
    )

    args = parser.parse_args()

    if args.list:
        print("Available mindmap types:")
        for mm_type in MINDMAP_TYPES:
            print(f"  {mm_type}")
        return 0

    types = [args.type] if args.type else None

    results = generate_all_mindmaps(
        output_dir=args.output,
        types=types,
        generate_html=args.html,
        pages_dir=args.pages_dir if args.html else None,
    )

    if results:
        generate_index(args.output, list(results.keys()))

    print(f"\n✅ Generated {len(results)} mindmaps")
    print(f"   📁 Markdown: {args.output}")
    if args.html:
        print(f"   🌐 HTML:     {args.pages_dir}")
        print(f"\n💡 To preview locally:")
        print(f"   cd {args.pages_dir}")
        print(f"   python -m http.server 8000")
        print(f"   # Then open http://localhost:8000")
    return 0


if __name__ == "__main__":
    sys.exit(main())

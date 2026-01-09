# tools/mindmaps/loader.py
"""Data loading for mind map generation."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from .config import ONTOLOGY_DIR, META_PROBLEMS_DIR
from .toml_parser import parse_toml_simple
from .data import ProblemData


@dataclass
class OntologyData:
    """All ontology data."""
    api_kernels: list[dict[str, Any]] = field(default_factory=list)
    patterns: list[dict[str, Any]] = field(default_factory=list)
    families: list[dict[str, Any]] = field(default_factory=list)
    algorithms: list[dict[str, Any]] = field(default_factory=list)
    data_structures: list[dict[str, Any]] = field(default_factory=list)
    topics: list[dict[str, Any]] = field(default_factory=list)
    difficulties: list[dict[str, Any]] = field(default_factory=list)
    companies: list[dict[str, Any]] = field(default_factory=list)
    roadmaps: list[dict[str, Any]] = field(default_factory=list)


def load_ontology() -> OntologyData:
    """Load all ontology files."""
    data = OntologyData()
    files = {
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
    for filename, attr in files.items():
        path = ONTOLOGY_DIR / filename
        if path.exists():
            parsed = parse_toml_simple(path.read_text(encoding="utf-8"))
            setattr(data, attr, parsed.get(attr, []))
    return data


def load_problems() -> dict[str, ProblemData]:
    """Load all problem metadata.

    Supports two TOML formats:
    - Legacy format: fields at top level (id, title, etc.)
    - New format: fields under [problem] section
    """
    problems = {}
    if not META_PROBLEMS_DIR.exists():
        return problems

    for path in META_PROBLEMS_DIR.glob("*.toml"):
        parsed = parse_toml_simple(path.read_text(encoding="utf-8"))

        # Support both formats: [problem] section or top-level fields
        if "problem" in parsed:
            # New format: fields under [problem] section
            problem_data = parsed["problem"]
            solution_data = parsed.get("solution", {})
            files = parsed.get("files", {})
        else:
            # Legacy format: fields at top level
            problem_data = parsed
            solution_data = parsed
            files = parsed.get("files", {})
        
        problem = ProblemData(
            id=problem_data.get("id", ""),
            title=problem_data.get("title", ""),
            slug=problem_data.get("slug", ""),
            leetcode_id=problem_data.get("leetcode_id", 0),
            url=problem_data.get("url", ""),
            difficulty=problem_data.get("difficulty", ""),
            topics=problem_data.get("topics", problem_data.get("tags", [])),
            companies=problem_data.get("companies", []),
            roadmaps=problem_data.get("roadmaps", []),
            api_kernels=solution_data.get("api_kernels", [solution_data.get("api_kernel", "")] if solution_data.get("api_kernel") else []),
            patterns=solution_data.get("patterns", [solution_data.get("pattern", "")] if solution_data.get("pattern") else []),
            families=problem_data.get("families", []),
            data_structures=problem_data.get("data_structures", []),
            algorithms=problem_data.get("algorithms", []),
            related_problems=problem_data.get("related_problems", []),
            solutions=problem_data.get("solutions", []),
            solution_file=files.get("solution", "") if isinstance(files, dict) else "",
            generator_file=files.get("generator", "") if isinstance(files, dict) else "",
        )

        role = parsed.get("pattern_role", {})
        if role:
            problem.is_base_template = role.get("is_base_template", False)
            problem.base_for_kernel = role.get("base_for_kernel", "")
            problem.derived_problems = role.get("derived_problems", [])
        
        problems[problem.id] = problem
    return problems


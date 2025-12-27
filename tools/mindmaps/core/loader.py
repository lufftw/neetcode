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
    """Load all problem metadata."""
    problems = {}
    if not META_PROBLEMS_DIR.exists():
        return problems

    for path in META_PROBLEMS_DIR.glob("*.toml"):
        parsed = parse_toml_simple(path.read_text(encoding="utf-8"))
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
        
        role = parsed.get("pattern_role", {})
        if role:
            problem.is_base_template = role.get("is_base_template", False)
            problem.base_for_kernel = role.get("base_for_kernel", "")
            problem.derived_problems = role.get("derived_problems", [])
        
        problems[problem.id] = problem
    return problems


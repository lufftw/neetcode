# tools/mindmaps/generators/__init__.py
"""Mind map generator functions."""

from .pattern import generate_pattern_hierarchy
from .family import generate_family_derivation
from .algorithm import generate_algorithm_usage, generate_data_structure
from .company import generate_company_coverage
from .roadmap import generate_roadmap_paths
from .relations import generate_problem_relations
from .variants import generate_solution_variants
from .difficulty import generate_difficulty_topics

GENERATORS = {
    "pattern-hierarchy": generate_pattern_hierarchy,
    "family-derivation": generate_family_derivation,
    "algorithm-usage": generate_algorithm_usage,
    "data-structure": generate_data_structure,
    "company-coverage": generate_company_coverage,
    "roadmap-paths": generate_roadmap_paths,
    "problem-relations": generate_problem_relations,
    "solution-variants": generate_solution_variants,
    "difficulty-topics": generate_difficulty_topics,
}

__all__ = [
    "GENERATORS",
    "generate_pattern_hierarchy",
    "generate_family_derivation",
    "generate_algorithm_usage",
    "generate_data_structure",
    "generate_company_coverage",
    "generate_roadmap_paths",
    "generate_problem_relations",
    "generate_solution_variants",
    "generate_difficulty_topics",
]


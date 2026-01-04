"""
Practice skeleton generator.

Generates practice files in practices/ directory,
reusing infrastructure from reference solutions.
"""

from .generator import generate_practice_skeleton
from .reuse import extract_infrastructure, clear_solution_body

__all__ = [
    "generate_practice_skeleton",
    "extract_infrastructure",
    "clear_solution_body",
]


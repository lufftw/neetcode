"""
Docstring Domain Module

This module is responsible for extracting and formatting docstring-relevant
content from LeetCode Question abstractions. It produces structured data
according to the docstring specification defined in README.md.

Key responsibilities:
    - Extracting description, examples, constraints from Question objects
    - Normalizing and formatting data for docstring generation
    - Remaining agnostic to data source and consuming tools

Non-responsibilities:
    - Code review decisions
    - File I/O or patching logic
    - CLI concerns

Usage:
    from tools.docstring.formatter import get_full_docstring_data

    docstring_data = get_full_docstring_data(question)
"""

from .formatter import (
    get_full_docstring_data,
    get_description_and_constraints,
    get_question_data,
)

__all__ = [
    "get_full_docstring_data",
    "get_description_and_constraints",
    "get_question_data",
]


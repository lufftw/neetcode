# Docstring Domain Module

This module is responsible for transforming LeetCode Question objects into structured docstring specifications.

## Purpose

The `docstring` module provides a **stable domain abstraction** for:

- Extracting docstring-relevant content from Question objects
- Normalizing and formatting data according to docstring specifications
- Producing structured, spec-aligned representations

## Key Characteristics

- **Domain independence**: Not tied to any specific consumer (review-code, generators, etc.)
- **Data source agnostic**: Works with any Question provider (cache, network, future sources)
- **Specification-driven**: Follows the docstring format defined in project README

## Module Structure

```
tools/docstring/
├── __init__.py      # Module exports
├── formatter.py     # Core formatting logic
└── README.md        # This file
```

## Usage

```python
from tools.docstring.formatter import get_full_docstring_data

# Get complete docstring data for a problem
data = get_full_docstring_data("two-sum")

# data contains:
# - title: Problem title
# - url: LeetCode URL
# - description: List of description lines
# - examples: List of example dicts
# - constraints: List of constraint lines
# - topics: Formatted topics string
# - hints: List of formatted hints
# - follow_ups: List of follow-up questions
# - note: Optional note string
```

## API Reference

### `get_full_docstring_data(slug: str) -> dict`

Returns all data needed for generating a complete File-Level Docstring.

**Parameters:**
- `slug`: LeetCode problem slug (e.g., 'two-sum')

**Returns:** Dictionary with all docstring components

### `get_description_and_constraints(slug: str) -> Tuple[List[str], List[str]]`

Legacy backward-compatible interface for fetching description and constraints.

**Parameters:**
- `slug`: LeetCode problem slug

**Returns:** Tuple of (description_lines, constraint_lines)

### `get_question_data(slug: str, force_refresh: bool = False) -> Optional[Question]`

Direct access to the underlying Question object.

**Parameters:**
- `slug`: LeetCode problem slug
- `force_refresh`: Bypass cache if True

**Returns:** Question object or None

## Design Rationale

See [docs/tools/docstring/refactor.md](../../docs/tools/docstring/refactor.md) for the complete design rationale behind this module structure.

## Consumers

- `tools/review-code/fix_docstring.py` - Auto-fixes solution file docstrings
- Future: generators, analyzers, metadata enrichers


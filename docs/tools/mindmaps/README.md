# Mind Maps Generation Module

> **Status**: Canonical Reference  
> **Scope**: Mind map generation tools in tools/mindmaps/  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

This module generates interactive mind maps from NeetCode ontology and problem metadata.

## Overview

The mind maps module provides:
- 9 different mind map types visualizing different aspects of the problem space
- Markdown output compatible with VS Code markmap extension
- HTML output for GitHub Pages deployment
- Configurable GitHub repository links

## Module Structure

```
tools/mindmaps/
├── core/                     # Core module (mind map generation logic)
│   ├── __init__.py           # Module exports
│   ├── config.py             # Configuration, constants, paths
│   ├── toml_parser.py        # TOML parsing utilities
│   ├── data.py               # ProblemData class
│   ├── loader.py             # OntologyData and data loading
│   ├── helpers.py            # Helper functions (frontmatter, formatting)
│   ├── html.py               # HTML generation logic
│   ├── templates.py          # HTML/CSS templates
│   └── generators/           # Mind map generator functions
│       ├── __init__.py
│       ├── pattern.py        # Pattern hierarchy generator
│       ├── family.py         # Family derivation generator
│       ├── algorithm.py      # Algorithm/data structure usage
│       ├── company.py        # Company coverage
│       ├── roadmap.py        # Learning roadmaps
│       ├── relations.py      # Problem relations network
│       ├── variants.py       # Solution variants
│       └── difficulty.py     # Difficulty × Topics matrix
├── ai-markmap-agent/         # AI-powered mindmap agent
├── ai_mindmap/               # AI mindmap module
├── hooks/                    # Git hooks
├── prompts/                  # AI prompts
├── shared/                   # Shared utilities
├── tests/                    # Tests
├── generate_mindmaps.py      # Rule-based generator (entry)
├── generate_mindmaps_ai.py   # AI generator (entry)
└── html_meta_description_generator.py  # SEO meta generator
```

## Core Components

### Configuration (`config.py`)

Manages configuration for mind map generation:
- GitHub repository URL and branch
- Output directories
- Mind map type definitions
- Difficulty icons

**Key Functions:**
- `load_config()` - Load configuration from file/env/defaults
- `get_config()` - Get singleton config instance

### TOML Parser (`toml_parser.py`)

Simple TOML parser for ontology files:
- Handles arrays of tables `[[array]]`
- Supports nested tables `[table]`
- Parses strings, arrays, booleans, integers

**Key Functions:**
- `parse_toml_simple(content)` - Parse TOML content
- `parse_toml_value(value)` - Parse individual TOML values

### Data Structures (`data.py`)

**ProblemData** - Represents a problem with metadata:
- Properties: `display_name`, `difficulty_icon`
- Methods: `solution_link()`, `markdown_link()`, `leetcode_link()`

### Data Loading (`loader.py`)

**OntologyData** - Container for all ontology data:
- API kernels, patterns, algorithms, data structures
- Topics, difficulties, companies, roadmaps

**Functions:**
- `load_ontology()` - Load all ontology files
- `load_problems()` - Load problem metadata from TOML files

### Helpers (`helpers.py`)

Utility functions:
- `markmap_frontmatter(title, color_freeze_level)` - Generate YAML frontmatter
- `format_problem_entry(prob, show_complexity)` - Format problem entry

### HTML Generation (`html.py`)

HTML output generation:
- `generate_html_mindmap(title, markdown, use_autoloader)` - Generate HTML file
- `markdown_to_html_content(markdown)` - Extract content without frontmatter
- `setup_pages_directory(pages_dir)` - Create directory structure

### Templates (`templates.py`)

HTML templates and CSS:
- `HTML_TEMPLATE_MANUAL` - Manual markmap initialization
- `HTML_TEMPLATE_AUTOLOADER` - Using markmap-autoloader
- `INDEX_HTML_TEMPLATE` - Index page template
- `STYLE_CSS` - CSS stylesheet
- `CARD_TEMPLATE` - Mind map card template

### Generators (`generators/`)

Each generator function takes `(ontology: OntologyData, problems: dict[str, ProblemData])` and returns a markdown string.

**Available Generators:**

1. **pattern.py** - `generate_pattern_hierarchy()`
   - API Kernel → Patterns → Problems hierarchy
   - Shows how kernels are instantiated as patterns and used in problems

2. **family.py** - `generate_family_derivation()`
   - Base templates and derived variants
   - Shows problem families with base/variant relationships

3. **algorithm.py** - `generate_algorithm_usage()`, `generate_data_structure()`
   - Algorithms/Data structures → Problems mapping
   - Shows which algorithms/data structures are used in which problems

4. **company.py** - `generate_company_coverage()`
   - Companies → Problems mapping
   - Shows problems frequently asked by companies

5. **roadmap.py** - `generate_roadmap_paths()`
   - Learning roadmap structures
   - Shows curated problem sequences for different learning goals

6. **relations.py** - `generate_problem_relations()`
   - Related problems network
   - Shows how problems are connected to each other

7. **variants.py** - `generate_solution_variants()`
   - Problems with multiple solution approaches
   - Shows different solution strategies for the same problem

8. **difficulty.py** - `generate_difficulty_topics()`
   - Difficulty × Topics matrix
   - Shows topics organized by difficulty level

## Usage Examples

### Basic Usage

```python
from mindmaps.core import (
    load_ontology,
    load_problems,
    GENERATORS,
)

# Load data
ontology = load_ontology()
problems = load_problems()

# Generate a specific mind map
content = GENERATORS["pattern_hierarchy"](ontology, problems)
print(content)
```

### Generate HTML

```python
from mindmaps.core import generate_html_mindmap

markdown = "# Test Map\n\n## Section"
html = generate_html_mindmap("Test Title", markdown, use_autoloader=False)
```

### Custom Configuration

```python
from mindmaps.core import get_config, MindmapsConfig
import os

# Override via environment variables
os.environ["GITHUB_REPO_URL"] = "https://github.com/user/repo"
os.environ["GITHUB_BRANCH"] = "main"

config = get_config()
print(config.github_repo_url)
```

## Mind Map Types

| Type | Description | Generator |
|------|-------------|-----------|
| `pattern_hierarchy` | API Kernels → Patterns → Problems | `pattern.py` |
| `family_derivation` | Base templates → Variants | `family.py` |
| `algorithm_usage` | Algorithms → Problems | `algorithm.py` |
| `data_structure` | Data Structures → Problems | `algorithm.py` |
| `company_coverage` | Companies → Problems | `company.py` |
| `roadmap_paths` | Learning Roadmaps | `roadmap.py` |
| `problem_relations` | Related Problems Network | `relations.py` |
| `solution_variants` | Multiple Solutions | `variants.py` |
| `difficulty_topics` | Difficulty × Topics Matrix | `difficulty.py` |

## Configuration File

Create `tools/mindmaps/generate_mindmaps.toml`:

```toml
[github]
repo_url = "https://github.com/user/repo"
branch = "main"

[links]
use_github_links = true
```

## Output Format

### Markdown Output

Each mind map is a Markdown file with YAML frontmatter:

```markdown
---
title: Pattern Hierarchy - API Kernels → Patterns → Problems
markmap:
  colorFreezeLevel: 2
  maxWidth: 400
---

# Pattern Hierarchy

## API Kernel Name
*Description*

### Pattern Name
*Pattern description*

- 🟡 [LeetCode 3 - Problem Name](link)
```

### HTML Output

HTML files include:
- Full markmap library integration
- Custom toolbar (Fit View, Expand All, Collapse All)
- Responsive design
- GitHub Pages ready

## Testing

The module is tested in `.dev/tests/test_generate_mindmaps.py`:

```bash
python -m pytest .dev/tests/test_generate_mindmaps.py -v
```

Test coverage includes:
- TOML parsing
- Data loading
- All 9 generator functions
- HTML generation
- Configuration loading
- Edge cases

## Development

### Adding a New Generator

1. Create a new file in `core/generators/` (e.g., `custom.py`)
2. Implement generator function:
   ```python
   def generate_custom(ontology: OntologyData, problems: dict[str, ProblemData]) -> str:
       lines = [markmap_frontmatter("Custom Map"), "# Custom Map", ""]
       # ... generation logic ...
       return "\n".join(lines)
   ```
3. Add to `core/generators/__init__.py`:
   ```python
   from .custom import generate_custom
   GENERATORS["custom"] = generate_custom
   ```
4. Add to `MINDMAP_TYPES` in `core/config.py`
5. Add tests in `.dev/tests/test_generate_mindmaps.py`

### Module Size Guidelines

- Each file should be < 100 lines (except templates)
- Each generator function should be < 80 lines
- Keep functions focused and single-purpose

## See Also

- [Main Tools README](../README.md) - Overview of all tools
- [AI Markmap Agent](ai-markmap-agent/README.md) - AI-powered mind map generation
- [CLI Usage](https://github.com/lufftw/neetcode/blob/main/tools/mindmaps/generate_mindmaps.py) - Command-line interface
- [Test Suite](https://github.com/lufftw/neetcode/blob/main/.dev/tests/test_generate_mindmaps.py) - Test coverage


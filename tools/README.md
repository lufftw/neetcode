# NeetCode Tools

This directory contains code generation and documentation tools for the NeetCode Practice Framework.

## Overview

The tools in this directory automate the generation of:
- **Mind Maps**: Interactive visualizations of algorithm patterns and problem relationships
- **AI-Powered Mind Maps**: AI-generated creative mind maps that synthesize ontology insights
- **Pattern Documentation**: Comprehensive documentation for algorithmic patterns

## Tools

### 1. Mind Map Generator (`generate_mindmaps.py`)

Generates Markmap-compatible mind maps from ontology and problem metadata.

**Features:**
- 9 different mind map types (pattern hierarchy, family derivation, algorithm usage, etc.)
- Markdown output for VS Code markmap extension
- HTML output for GitHub Pages deployment
- Configurable GitHub repository links

**Quick Start:**
```bash
# Generate all mind maps (Markdown only)
python tools/generate_mindmaps.py

# Generate Markdown + HTML for GitHub Pages
python tools/generate_mindmaps.py --html

# Generate specific type
python tools/generate_mindmaps.py --type pattern_hierarchy

# List available types
python tools/generate_mindmaps.py --list
```

**See:** [`mindmaps/README.md`](mindmaps/README.md) for detailed documentation.

### 2. AI-Powered Mind Map Generator (`generate_mindmaps_ai.py`)

Generates creative, AI-synthesized mind maps using OpenAI's API. Analyzes the entire knowledge graph (API Kernels, Patterns, Algorithms, Data Structures, Problem Families) to discover non-obvious connections and generate insights.

**Features:**
- AI-powered deep pattern synthesis
- Multi-language generation (English, 繁體中文)
- Smart linking: Problems link to GitHub solutions (when available) or LeetCode
- Configurable learning goals (interview prep, systematic learning, quick review, etc.)
- Multiple output styles (creative, academic, practical, minimal, balanced)
- Interactive mode for guided generation

**Requirements:**
- OpenAI API key (set `OPENAI_API_KEY` environment variable or enter interactively)
- `openai` package: `pip install openai`

**Quick Start:**
```bash
# Interactive mode (will prompt for API key and options)
python tools/generate_mindmaps_ai.py

# Use config file
python tools/generate_mindmaps_ai.py --config mindmap_ai_config.toml

# Quick options
python tools/generate_mindmaps_ai.py --goal interview --topic sliding_window
python tools/generate_mindmaps_ai.py --style creative --model gpt-4

# Show current config
python tools/generate_mindmaps_ai.py --list-config
```

**Configuration:**
- Config file: `tools/mindmap_ai_config.toml`
- Supports TOML-based configuration for ontology selection, problem filtering, generation goals, and output settings

**Output:**
- Markdown files: `docs/mindmaps/neetcode_ontology_ai_*.md`
- HTML files: `docs/pages/mindmaps/neetcode_ontology_ai_*.html` (for GitHub Pages)

**Prompt Generation:**
- Prompts are automatically generated and saved to `tools/prompts/generated/mindmap_prompt.md`
- The prompt file contains both system prompt and user prompt, ready for manual use
- **Tracked in Git**: The prompt file is committed to the repository for **traceability** — you can always see which prompt was used to generate each AI mind map
- If you don't have an API key, you can copy the generated prompt to ChatGPT/Claude web interface
- Prompt is saved before API call, so you can use it even if API call fails

**See:**
- [`docs/GITHUB_PAGES_SETUP.md`](../docs/GITHUB_PAGES_SETUP.md) for manual generation workflow
- [`prompts/README.md`](prompts/README.md) for detailed prompt usage guide

### 3. Pattern Documentation Generator (`generate_pattern_docs.py`)

Generates comprehensive pattern documentation by composing ontology definitions and per-problem markdown snippets.

**Features:**
- Automatic section numbering
- Table of contents generation
- Pattern-based organization
- Support for multiple problem examples per pattern

**Quick Start:**
```bash
# Generate all pattern documentation
python tools/generate_pattern_docs.py

# Generate specific pattern
python tools/generate_pattern_docs.py --pattern sliding_window

# Validate without writing files
python tools/generate_pattern_docs.py --validate

# List available patterns
python tools/generate_pattern_docs.py --list
```

**See:** [`patterndocs/README.md`](patterndocs/README.md) for detailed documentation.

## Architecture

The tools follow a modular architecture:

```
tools/
├── generate_mindmaps.py          # CLI entry point (rule-based)
├── generate_mindmaps_ai.py       # CLI entry point (AI-powered)
├── generate_pattern_docs.py      # CLI entry point
│
├── mindmaps/                     # Mind map generation module (shared)
│   ├── config.py                 # Configuration and constants
│   ├── toml_parser.py            # TOML parsing
│   ├── data.py                   # ProblemData class
│   ├── loader.py                 # Data loading
│   ├── helpers.py                # Helper functions
│   ├── html.py                   # HTML generation
│   ├── templates.py              # HTML/CSS templates
│   └── generators/               # Mind map generators
│       ├── pattern.py
│       ├── family.py
│       ├── algorithm.py
│       └── ...
│
└── patterndocs/                  # Pattern documentation module
    ├── toml_parser.py            # TOML parsing
    ├── data.py                   # Data classes
    ├── loader.py                 # Ontology loading
    ├── files.py                  # File collection
    ├── sections.py               # Section numbering
    └── composer.py               # Document composition
```

## Design Principles

1. **Modularity**: Each tool is split into focused modules (< 100 lines each)
2. **Independence**: Tools are completely decoupled (no shared dependencies)
3. **Testability**: Each module can be tested independently
4. **Maintainability**: Clear separation of concerns

## Testing

The rule-based tools have comprehensive test suites:

```bash
# Run all tool tests
python -m pytest .dev/tests/test_generate_mindmaps.py .dev/tests/test_generate_pattern_docs.py -v

# Run specific test file
python -m pytest .dev/tests/test_generate_mindmaps.py -v
```

**Note:** AI-powered mind map generation (`generate_mindmaps_ai.py`) requires API access and is tested manually. See [`docs/GITHUB_PAGES_SETUP.md`](../docs/GITHUB_PAGES_SETUP.md) for manual generation workflow.

## Dependencies

- **`generate_mindmaps.py`** and **`generate_pattern_docs.py`**: Python standard library only
- **`generate_mindmaps_ai.py`**: Requires `openai` package (`pip install openai`)

## File Structure

### Input Files

- `ontology/*.toml` - Ontology definitions (API kernels, patterns, algorithms, etc.)
- `meta/problems/*.toml` - Problem metadata
- `meta/patterns/<pattern>/*.md` - Pattern documentation source files

### Output Files

- `docs/mindmaps/*.md` - Generated mind map Markdown files (rule-based + AI)
- `docs/pages/mindmaps/*.html` - Generated HTML mind maps (for GitHub Pages)
  - Rule-based: `pattern_hierarchy.html`, `family_derivation.html`, etc.
  - AI-powered: `neetcode_ontology_ai_*.html` (manually generated, tracked in Git)
- `docs/patterns/*.md` - Generated pattern documentation

## Contributing

When adding new features:

1. **Keep modules small**: Aim for < 100 lines per file
2. **Maintain independence**: Don't create shared dependencies between tools
3. **Add tests**: Update test files in `.dev/tests/`
4. **Update documentation**: Keep README files current

## See Also

- [Mind Maps Module Documentation](mindmaps/README.md)
- [Pattern Docs Module Documentation](patterndocs/README.md)
- [Testing Documentation](../.dev/TESTING.md)

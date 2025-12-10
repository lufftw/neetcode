# NeetCode Tools

This directory contains code generation and documentation tools for the NeetCode Practice Framework.

## Overview

The tools in this directory automate the generation of:
- **Mind Maps**: Interactive visualizations of algorithm patterns and problem relationships
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

### 2. Pattern Documentation Generator (`generate_pattern_docs.py`)

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

Both tools follow a modular architecture:

```
tools/
├── generate_mindmaps.py          # CLI entry point
├── generate_pattern_docs.py      # CLI entry point
│
├── mindmaps/                     # Mind map generation module
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

Both tools have comprehensive test suites:

```bash
# Run all tool tests
python -m pytest .dev/tests/test_generate_mindmaps.py .dev/tests/test_generate_pattern_docs.py -v

# Run specific test file
python -m pytest .dev/tests/test_generate_mindmaps.py -v
```

## Dependencies

Both tools use only Python standard library (no external dependencies required).

## File Structure

### Input Files

- `ontology/*.toml` - Ontology definitions (API kernels, patterns, algorithms, etc.)
- `meta/problems/*.toml` - Problem metadata
- `meta/patterns/<pattern>/*.md` - Pattern documentation source files

### Output Files

- `docs/mindmaps/*.md` - Generated mind map Markdown files
- `docs/pages/mindmaps/*.html` - Generated HTML mind maps (for GitHub Pages)
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

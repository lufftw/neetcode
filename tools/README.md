# Solution Tools

> **Full documentation**: See [docs/TOOLS.md](../docs/TOOLS.md) for complete reference.

Tools for checking and validating solution files.

## Quick Start

```bash
# Run format checker
python tools/check_solutions.py

# Run format unit tests
python tools/run_format_tests.py --verbose

# Using shell scripts
tools\run_format_tests.bat     # Windows
tools/run_format_tests.sh      # Linux/Mac
```

## Tools

| Tool | Description |
|------|-------------|
| `check_solutions.py` | Main checker for Pure Polymorphic Architecture compliance |
| `run_format_tests.py` | Run format checking unit tests |
| `generate_mindmaps.py` | Generate mind map documentation |
| `generate_mindmaps_ai.py` | AI-powered mind map generation |
| `generate_pattern_docs.py` | Generate pattern documentation |
| `text_to_mindmap.py` | Convert text to mind map format |
| `prepare_llm_input.py` | Prepare input for LLM processing |

## Documentation

- [Tools Reference](../docs/TOOLS.md) - Complete tools documentation (includes format checking guide)
- [Solution Contract](../docs/SOLUTION_CONTRACT.md) - Solution file specification
- [Architecture Migration](../docs/ARCHITECTURE_MIGRATION.md) - Migration guide

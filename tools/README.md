# 🔧 NeetCode Tools

Developer tools for checking, validating, and generating project content.

---

## 📋 Quick Reference

| Category | Tool | Purpose |
|----------|------|---------|
| **Checking** | `check_solutions.py` | Validate solution file architecture compliance |
| | `run_format_tests.py` | Run format unit tests |
| | `check_test_files.py` | Check and fix test files with double newline endings |
| **Generation** | `generate_mindmaps.py` | Rule-based mind map generation |
| | `generate_mindmaps_ai.py` | AI-powered mind map generation |
| | `generate_pattern_docs.py` | Pattern documentation generation |
| | `html_meta_description_generator.py` | Generate SEO meta descriptions from Markdown |
| **Automation** | Pre-commit Hooks | Auto-generate AI mind maps on commit |
| **Utilities** | `text_to_mindmap.py` | Convert text to mind map format |
| | `prepare_llm_input.py` | Prepare LLM input data |

---

## 🚀 Quick Start

```bash
# Check all solution files
python tools/check_solutions.py

# Generate mind maps (rule-based)
python tools/generate_mindmaps.py --html

# Generate mind maps (AI)
python tools/generate_mindmaps_ai.py --goal interview

# Generate pattern documentation
python tools/generate_pattern_docs.py

# Generate SEO meta descriptions
python tools/html_meta_description_generator.py
```

---

## 📁 Directory Structure

```
tools/
├── README.md                      # This file (shortened version)
├── check_solutions.py             # Solution file checker
├── check_test_files.py            # Test file format checker/fixer
├── run_format_tests.py            # Format test runner
├── generate_mindmaps.py           # Rule-based mind map generator
├── generate_mindmaps_ai.py        # AI mind map generator
├── generate_pattern_docs.py       # Pattern documentation generator
├── html_meta_description_generator.py  # SEO meta description generator
├── text_to_mindmap.py             # Text to mind map converter
├── prepare_llm_input.py           # LLM input preparation
├── hooks/                         # Pre-commit hooks
├── mindmaps/                      # Mind map generation module
│   └── README.md                  # 📖 Detailed technical docs
├── patterndocs/                   # Pattern docs generation module
│   └── README.md                  # 📖 Detailed technical docs
├── ai-markmap-agent/              # AI Markmap Agent
│   └── README.md                  # 📖 Detailed technical docs
├── prompts/                       # AI prompt management
├── shared/                        # Shared utilities
└── tests/                         # Format tests
```

---

## 📚 Full Documentation

For complete documentation, please see:

- **[Tools Overview](../docs/tools/README.md)** - Complete tools reference with detailed usage guides
- **[AI Markmap Agent](../docs/tools/ai-markmap-agent/README.md)** - AI-powered mind map generation architecture
- **[Mind Maps Generator](../docs/tools/mindmaps/README.md)** - Rule-based mind map generation technical docs
- **[Pattern Docs Generator](../docs/tools/patterndocs/README.md)** - Pattern documentation generation guide

---

**Note**: This is a shortened version. For detailed usage instructions, configuration options, and advanced features, please refer to the full documentation linked above.

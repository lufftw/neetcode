# Tools Directory

This directory contains utility scripts for the NeetCode Practice Framework.

## Available Tools

### `generate_pattern_docs.py`

Generates comprehensive pattern documentation by composing markdown snippets from `meta/patterns/`.

**Usage:**

```bash
# List available patterns
python tools/generate_pattern_docs.py --list

# Generate all patterns
python tools/generate_pattern_docs.py --all

# Generate specific pattern
python tools/generate_pattern_docs.py --pattern sliding_window

# Validate only (dry run)
python tools/generate_pattern_docs.py --validate
```

**How it works:**

1. Reads API Kernel and Pattern definitions from `ontology/`
2. Collects markdown snippets from `meta/patterns/<pattern_name>/`
3. Composes them into a single document in `docs/patterns/<pattern_name>.md`

**Source file structure:**

```
meta/patterns/<pattern_name>/
├── _header.md        # Core concepts (required)
├── _comparison.md    # Pattern comparison table
├── _decision.md      # When to use this pattern
├── _templates.md     # Quick reference templates
├── 0003_base.md      # Problem-specific content (by problem number)
├── 0076_variant.md
└── ...
```

**Output:**

Generated documents follow this structure:
1. Header (from `_header.md`)
2. Auto-generated Table of Contents
3. Problem sections (sorted by filename)
4. Footer sections (comparison, decision, templates)
5. Auto-generated footer with API Kernel reference

---

### `generate_mindmaps.py`

Generates multiple Mermaid mind maps from ontology and problem metadata.

**Usage:**

```bash
# List available mindmap types
python tools/generate_mindmaps.py --list

# Generate all mindmaps
python tools/generate_mindmaps.py

# Generate specific mindmap type
python tools/generate_mindmaps.py --type pattern_hierarchy

# Use LLM for enhanced descriptions (requires API key)
python tools/generate_mindmaps.py --llm

# Generate interactive HTML (Markmap)
leetcode\Scripts\python.exe tools\generate_mindmaps.py --html
```

**Available Mind Map Types:**

| Type | Description |
|------|-------------|
| `pattern_hierarchy` | API Kernels → Patterns → Problems |
| `family_derivation` | Base templates and derived variants |
| `algorithm_usage` | Algorithms → Problems |
| `data_structure` | Data Structures → Problems |
| `company_coverage` | Companies → Problems |
| `roadmap_paths` | Learning roadmap structures |
| `problem_relations` | Related problems network |
| `solution_variants` | Problems with multiple solutions |
| `difficulty_topics` | Topics by difficulty level |

**Output:**

Generated mind maps in `docs/mindmaps/` with:
- Mermaid syntax for visual rendering
- Insights and analysis
- Data source references

---

### `text_to_mindmap.py`

Converts **ANY text** to structured mind maps using LLM.

**Usage:**

```bash
# Direct text input
python tools/text_to_mindmap.py --input "Your text here" --format mermaid

# From file
python tools/text_to_mindmap.py --file article.txt --format html --output mindmap.html

# Different LLM backends
python tools/text_to_mindmap.py --file notes.txt --backend ollama  # Local LLM
python tools/text_to_mindmap.py --file notes.txt --backend anthropic  # Claude
```

**Output Formats:**

| Format | Description | Use Case |
|--------|-------------|----------|
| `mermaid` | Mermaid mindmap syntax | Embed in Markdown |
| `markdown` | Hierarchical headings | Convert with Markmap |
| `html` | Interactive Markmap HTML | Standalone web page |
| `json` | Structured JSON | Programmatic use |

**Supported LLM Backends:**

- `openai` - GPT-4 / GPT-3.5 (requires `OPENAI_API_KEY`)
- `anthropic` - Claude (requires `ANTHROPIC_API_KEY`)
- `ollama` - Local LLM (requires Ollama running)

**Example - Convert any text to interactive mind map:**

```bash
# 1. Paste any text into a file
echo "Sliding window is a technique..." > concept.txt

# 2. Generate interactive HTML mind map
python tools/text_to_mindmap.py -f concept.txt -t html -o docs/mindmaps/generated/concept.html

# 3. Open in browser - fully interactive!
```

---

## Future Tools

Planned utilities:

- `validate_metadata.py` - Validate all TOML metadata files
- `generate_problem_index.py` - Generate problem index from metadata
- `sync_ontology.py` - Sync ontology with problem metadata


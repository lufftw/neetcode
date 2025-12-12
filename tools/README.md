# 🔧 NeetCode Tools

Developer tools for checking, validating, and generating project content.

---

## 📋 Quick Reference

| Category | Tool | Purpose |
|----------|------|---------|
| **Checking** | [`check_solutions.py`](#check_solutionspy) | Validate solution file architecture compliance |
| | [`run_format_tests.py`](#run_format_testspy) | Run format unit tests |
| **Generation** | [`generate_mindmaps.py`](#generate_mindmapspy) | Rule-based mind map generation |
| | [`generate_mindmaps_ai.py`](#generate_mindmaps_aipy) | AI-powered mind map generation |
| | [`generate_pattern_docs.py`](#generate_pattern_docspy) | Pattern documentation generation |
| **Utilities** | [`text_to_mindmap.py`](#text_to_mindmappy) | Convert text to mind map format |
| | [`prepare_llm_input.py`](#prepare_llm_inputpy) | Prepare LLM input data |

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
```

---

## 📁 Directory Structure

```
tools/
├── README.md                      # This file
├── check_solutions.py             # Solution file checker
├── run_format_tests.py            # Format test runner
├── run_format_tests.bat/.sh       # Format test scripts
│
├── generate_mindmaps.py           # Rule-based mind map generator
├── generate_mindmaps.toml         # Rule-based configuration
├── generate_mindmaps_ai.py        # AI mind map generator
├── mindmap_ai_config.toml         # AI configuration
│
├── generate_pattern_docs.py       # Pattern documentation generator
├── generate_pattern_docs.toml     # Pattern docs configuration
│
├── text_to_mindmap.py             # Text to mind map converter
├── prepare_llm_input.py           # LLM input preparation
│
├── mindmaps/                      # Mind map generation module
│   └── README.md                  # 📖 Detailed technical docs
├── patterndocs/                   # Pattern docs generation module
│   └── README.md                  # 📖 Detailed technical docs
├── prompts/                       # AI prompt management
│   └── README.md                  # 📖 Usage guide
├── shared/                        # Shared utilities
└── tests/                         # Format tests
    └── test_solution_format.py
```

---

## 🔍 Checking Tools

### `check_solutions.py`

Checks all solution files for Pure Polymorphic Architecture compliance.

```bash
python tools/check_solutions.py           # Standard check
python tools/check_solutions.py --verbose # Show fix suggestions
```

**Checks Performed:**

| Category | What It Checks |
|----------|----------------|
| **Architecture** | `SOLUTIONS` dictionary exists with `class` field |
| | No wrapper functions (`solve_*`) |
| | `solve()` uses `get_solver()` |
| | Correct import: `from _runner import get_solver` |
| **Format** | Comments use `Solution 1:` format |
| | Comments placed BEFORE class definition |
| **Complexity** | Each solution has `# Time: O(...)` |
| | Each solution has `# Space: O(...)` |

**Example Output:**

```
============================================================
📊 Solution Format Check Summary
============================================================
Total files: 34
✅ OK: 30
⚠️ Warnings: 2
❌ Errors: 2
============================================================
```

### `run_format_tests.py`

Runs unit tests for format checking.

```bash
python tools/run_format_tests.py           # Standard run
python tools/run_format_tests.py --verbose # Verbose output
python tools/run_format_tests.py --quiet   # Quiet mode
```

### `run_format_tests.bat` / `run_format_tests.sh`

Runs complete format check (checker + unit tests).

```bash
tools\run_format_tests.bat     # Windows
tools/run_format_tests.sh      # Linux/Mac
```

---

## 🧠 Mind Map Generation

### `generate_mindmaps.py`

Rule-based mind map generator that creates 9 types of mind maps from ontology data.

```bash
python tools/generate_mindmaps.py          # Generate Markdown
python tools/generate_mindmaps.py --html   # Generate HTML (interactive)
```

**Configuration:** `tools/generate_mindmaps.toml`

**Generation Types:**

| Type | Description |
|------|-------------|
| `pattern_hierarchy` | API Kernel → Pattern → Problem |
| `family_derivation` | Base template → Derived variants |
| `algorithm_usage` | Algorithm → Problems |
| `data_structure` | Data structure → Problems |
| `company_coverage` | Company → Problems |
| `roadmap_paths` | Learning roadmaps |
| `problem_relations` | Related problems network |
| `solution_variants` | Multiple solution approaches |
| `difficulty_topics` | Difficulty × Topics matrix |

> 📖 **Detailed technical docs:** [mindmaps/README.md](mindmaps/README.md)

### `generate_mindmaps_ai.py`

AI-powered mind map generator using LLM for creative generation.

```bash
# Interactive mode
python tools/generate_mindmaps_ai.py

# Specific goals
python tools/generate_mindmaps_ai.py --goal interview        # Interview prep
python tools/generate_mindmaps_ai.py --goal systematic       # Systematic learning
python tools/generate_mindmaps_ai.py --goal pattern_mastery  # Pattern mastery

# Specific topics
python tools/generate_mindmaps_ai.py --topic sliding_window
python tools/generate_mindmaps_ai.py --topic dynamic_programming
```

**Configuration:** `tools/mindmap_ai_config.toml`

| Section | What You Can Configure |
|---------|------------------------|
| `[model]` | LLM model, temperature, max tokens |
| `[output]` | Output directory, filename, HTML generation |
| `[ontology]` | Which knowledge graph data to include |
| `[problems]` | Problem filters (difficulty, topics, roadmaps) |
| `[links]` | GitHub repo URL, branch |
| `[advanced]` | Output language(s) (multi-language support) |

**No API Key?** After running, copy `tools/prompts/generated/mindmap_prompt.md` to ChatGPT/Claude.

> 📖 **Detailed usage guide:** [prompts/README.md](prompts/README.md)

---

## 📐 Pattern Documentation Generation

### `generate_pattern_docs.py`

Composes pattern documentation from source files in `meta/patterns/`.

```bash
# Generate all pattern docs
python tools/generate_pattern_docs.py

# Generate specific pattern
python tools/generate_pattern_docs.py --pattern sliding_window
```

**Configuration:** `tools/generate_pattern_docs.toml`

**Source Structure:**

```
meta/patterns/sliding_window/
├── _config.toml        # File ordering (optional)
├── _header.md          # Introduction and core concepts
├── 0003_base.md        # Base template problem
├── 0076_variant.md     # Variant problem
├── _comparison.md      # Pattern comparison table
├── _decision.md        # Decision guide
└── _templates.md       # Template code
```

> 📖 **Detailed technical docs:** [patterndocs/README.md](patterndocs/README.md)

---

## 🛠️ Utility Tools

### `text_to_mindmap.py`

Converts plain text to Markmap mind map format.

```bash
python tools/text_to_mindmap.py input.txt -o output.md
```

### `prepare_llm_input.py`

Prepares LLM input data by integrating ontology and problem information.

```bash
python tools/prepare_llm_input.py --output llm_input.json
```

**Use Cases:**
- Prepare input data for AI analysis
- Export problem and pattern information
- Generate context for prompts

---

## 🧪 Testing

### Format Tests

```bash
# Run format tests
pytest tools/tests/test_solution_format.py -v

# Or use standalone script
python tools/run_format_tests.py
```

### Generator Tests

```bash
# Mind map generation tests
pytest .dev/tests/test_generate_mindmaps.py -v

# Pattern docs generation tests
pytest .dev/tests/test_generate_pattern_docs.py -v
```

---

## 📊 Test Architecture Overview

```
neetcode/
├── tools/tests/                  # Format compliance tests
│   └── test_solution_format.py
│
├── .dev/tests/                   # Component tests (runner modules)
│   ├── test_generate_mindmaps.py
│   ├── test_generate_pattern_docs.py
│   └── ...
│
└── .dev/tests_solutions/         # Solution correctness tests
    └── test_all_solutions.py
```

**Run All Tests:**

```bash
.dev\run_all_tests.bat    # Windows
.dev/run_all_tests.sh     # Linux/Mac
```

---

## 🔗 Related Documentation

| Document | Description |
|----------|-------------|
| [SOLUTION_CONTRACT.md](../docs/SOLUTION_CONTRACT.md) | Solution file specification |
| [GENERATOR_CONTRACT.md](../docs/GENERATOR_CONTRACT.md) | Generator file specification |
| [ARCHITECTURE_MIGRATION.md](../docs/ARCHITECTURE_MIGRATION.md) | Architecture migration guide |
| [mindmaps/README.md](mindmaps/README.md) | Mind map module technical docs |
| [patterndocs/README.md](patterndocs/README.md) | Pattern docs module technical docs |
| [prompts/README.md](prompts/README.md) | AI prompts usage guide |

---

## ❓ FAQ

<details>
<summary><strong>check_solutions.py reports errors - how to fix?</strong></summary>

**Missing Solution Comment:**
```python
# Add before class definition:
# ============================================
# Solution 1: Hash Map
# Time: O(n), Space: O(n)
# ============================================
class Solution:
    ...
```

**Wrong Comment Format:**
```python
# Change "Solution:" to "Solution 1:"
# Solution 1: Two Pointers  ✅
# Solution: Two Pointers    ❌
```

</details>

<details>
<summary><strong>How to add a new mind map type?</strong></summary>

1. Create new file in `tools/mindmaps/generators/`
2. Implement generator function
3. Register in `generators/__init__.py`
4. Add tests to `.dev/tests/test_generate_mindmaps.py`

See [mindmaps/README.md](mindmaps/README.md#adding-a-new-generator)

</details>

<details>
<summary><strong>How to add new pattern documentation?</strong></summary>

1. Create directory `meta/patterns/<pattern_name>/`
2. Add `_header.md` (required)
3. Add problem files (e.g., `0003_base.md`)
4. Optionally add `_config.toml` to control order
5. Run `python tools/generate_pattern_docs.py --pattern <name>`

See [patterndocs/README.md](patterndocs/README.md#adding-a-new-pattern)

</details>

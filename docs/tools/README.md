# 🔧 NeetCode Tools

Developer tools for checking, validating, and generating project content.

---

## 📋 Quick Reference

| Category | Tool | Purpose |
|----------|------|---------|
| **Checking** | [`check_solutions.py`](#check_solutionspy) | Validate solution file architecture compliance |
| | [`run_format_tests.py`](#run_format_testspy) | Run format unit tests |
| | [`check_test_files.py`](#check_test_filespy) | Check and fix test files with double newline endings |
| **Review** | [`fix_docstring.py`](#fix_docstringpy) | Auto-fix file-level docstrings from LeetCode |
| **Data** | [`leetcode-api`](leetcode-api/README.md) | SQLite-backed cache for LeetCode question data |
| **Generation** | [`generate_mindmaps.py`](#generate_mindmapspy) | Rule-based mind map generation |
| | [`generate_mindmaps_ai.py`](#generate_mindmaps_aipy) | AI-powered mind map generation |
| | [`generate_pattern_docs.py`](#generate_pattern_docspy) | Pattern documentation generation |
| | [`html_meta_description_generator.py`](#html_meta_description_generatorpy) | Generate SEO meta descriptions from Markdown |
| **Automation** | [Pre-commit Hooks](#-local-cicd-automation) | Auto-generate AI mind maps on commit |
| **Utilities** | [`text_to_mindmap.py`](#text_to_mindmappy) | Convert text to mind map format |
| | [`prepare_llm_input.py`](#prepare_llm_inputpy) | Prepare LLM input data |

---

## 🚀 Quick Start

```bash
# Check all solution files
python tools/review-code/validation/check_solutions.py

# Generate mind maps (rule-based)
python tools/mindmaps/generate_mindmaps.py --html

# Generate mind maps (AI)
python tools/mindmaps/generate_mindmaps_ai.py --goal interview

# Generate pattern documentation
python tools/patterndocs/generate_pattern_docs.py

# Generate SEO meta descriptions
python tools/mindmaps/html_meta_description_generator.py
```

---

## 📁 Directory Structure

```
tools/
├── README.md                      # Tools overview
├── reorganization-plan.md         # Reorganization plan and migration details
│
├── mindmaps/                      # 🗺️ Mind map generation (consolidated)
│   ├── core/                      # Core module
│   │   ├── generators/            # Mind map type generators
│   │   └── ...
│   ├── ai-markmap-agent/          # AI markmap agent
│   ├── ai_mindmap/                # AI mindmap module
│   ├── hooks/                     # Git hooks for mindmaps
│   ├── prompts/                   # AI prompts
│   ├── shared/                    # Shared utilities
│   ├── tests/                     # Mindmap tests
│   ├── generate_mindmaps.py       # Rule-based generator
│   ├── generate_mindmaps_ai.py    # AI generator
│   ├── sync_mindmap_html.py       # HTML sync tool
│   └── html_meta_description_generator.py  # SEO meta generator
│
├── patterndocs/                   # 📚 Pattern documentation generation
│   ├── generate_pattern_docs.py   # Pattern docs generator
│   └── ...
│
├── review-code/                   # 🔍 Code review tools
│   ├── fix_docstring.py           # Auto-fix docstrings
│   └── validation/                # Validation tools
│       ├── check_solutions.py     # Solution checker
│       ├── check_test_files.py    # Test file checker
│       ├── run_format_tests.py    # Format test runner
│       └── tests/                 # Validation tests
│
├── docstring/                     # 📝 Docstring utilities
│   ├── formatter.py               # Docstring formatting logic
│   └── README.md
│
├── leetcode-api/                  # 🔗 LeetCode data cache
│   ├── question_api.py            # Unified public API
│   ├── question_store.py          # SQLite storage layer
│   └── data/                      # LeetScrape data files
│
├── maintenance/                   # 🔧 Maintenance tools
│   └── doc-naming/                # Document naming tools
│
└── _staging/                      # 📦 Staging area (to be organized)
    ├── prepare_llm_input.py
    └── ...
```

---

## 🔍 Checking Tools

### `check_solutions.py`

Checks all solution files for Pure Polymorphic Architecture compliance.

```bash
python tools/review-code/validation/check_solutions.py              # Standard check
python tools/review-code/validation/check_solutions.py --verbose    # Show fix suggestions
python tools/review-code/validation/check_solutions.py --list-warnings  # List only files with warnings
python tools/review-code/validation/check_solutions.py --show-warnings  # Show warnings with suggestions
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
python tools/review-code/validation/run_format_tests.py           # Standard run
python tools/review-code/validation/run_format_tests.py --verbose # Verbose output
python tools/review-code/validation/run_format_tests.py --quiet   # Quiet mode
```

### `run_format_tests.bat` / `run_format_tests.sh`

Runs complete format check (checker + unit tests).

```bash
tools\review-code\validation\run_format_tests.bat     # Windows
tools/review-code/validation/run_format_tests.sh      # Linux/Mac
```

### `check_test_files.py`

Check and fix double newline ending errors in test files under `tests/` directory.

Checks all `.in` and `.out` files to find files ending with two newlines (`\n\n`).

```bash
python tools/review-code/validation/check_test_files.py              # List problematic files
python tools/review-code/validation/check_test_files.py --fix        # List and auto-fix
python tools/review-code/validation/check_test_files.py --verbose    # Show detailed info
```

**Features:**
- List all test files ending with two newlines
- Auto-fix: Remove extra newline, keep only one

**Example Output:**
```
Found 3 files ending with two newlines:

  tests/0977_squares_of_a_sorted_array_1.in
  tests/0977_squares_of_a_sorted_array_1.out
  tests/0142_linked_list_cycle_ii_1.in

Tip: Use --fix to automatically fix these issues.
```

---

## 📝 Code Review Tools

### `fix_docstring.py`

Auto-fix file-level docstrings for solution files by fetching data from LeetCode.

Located in: `tools/review-code/fix_docstring.py`

```bash
# Fix files in range (e.g., 0077-0142)
python tools/review-code/fix_docstring.py --range 77 142

# Fix single file (e.g., 0202)
python tools/review-code/fix_docstring.py --range 202 202

# Custom delay to avoid rate limiting
python tools/review-code/fix_docstring.py --range 77 142 --delay-min 3.0 --delay-max 8.0

python tools/review-code/fix_docstring.py --range 209 1000 --delay-min 60.0 --delay-max 120.0

python tools/review-code/fix_docstring.py --range 1 1000 --delay-min 30.0 --delay-max 66.0
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--range START END` | Required | Problem number range to process |
| `--delay-min` | 3.0 | Minimum delay between requests (seconds) |
| `--delay-max` | 8.0 | Maximum delay between requests (seconds) |

**What It Does:**

1. Reads problem info from local cache (`tools/leetcode-api/crawler/.cache/leetcode_problems.json`)
2. Fetches description and constraints from LeetCode via `leetscrape`
3. Generates docstring following [review-code README](../../tools/review-code/README.md) format
4. Updates the solution file

**Example Output:**
```
Processing 0202 ~ 0202
Delay: 3.0s ~ 8.0s

  Fetching happy-number... (1 constraints)
[OK] 0202_happy_number.py: Updated

==================================================
Summary: Fixed 1 files
==================================================
```

**Dependencies:**
- `leetscrape` library for fetching LeetCode data
- Local cache file with problem metadata

---

## 🧠 Mind Map Generation

### `generate_mindmaps.py`

Rule-based mind map generator that creates 9 types of mind maps from ontology data.

```bash
python tools/mindmaps/generate_mindmaps.py          # Generate Markdown
python tools/mindmaps/generate_mindmaps.py --html   # Generate HTML (interactive)
```

**Configuration:** `tools/mindmaps/generate_mindmaps.toml`

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
python tools/mindmaps/generate_mindmaps_ai.py

# Specific goals
python tools/mindmaps/generate_mindmaps_ai.py --goal interview        # Interview prep
python tools/mindmaps/generate_mindmaps_ai.py --goal systematic       # Systematic learning
python tools/mindmaps/generate_mindmaps_ai.py --goal pattern_mastery  # Pattern mastery

# Specific topics
python tools/mindmaps/generate_mindmaps_ai.py --topic sliding_window
python tools/mindmaps/generate_mindmaps_ai.py --topic dynamic_programming

# Generate HTML only (from existing Markdown files)
python tools/mindmaps/generate_mindmaps_ai.py --html-only            # Skip Markdown generation, only update HTML
```

**HTML-Only Mode (`--html-only`):**

The `--html-only` flag allows you to generate HTML files from existing Markdown mind map files without regenerating the Markdown content. This is useful when:

- You've updated meta description files and want to refresh HTML output
- You want to regenerate HTML with updated meta descriptions
- You've manually edited Markdown files and want to update HTML without running the full AI generation

The command reads existing Markdown files from the configured output directory and generates corresponding HTML files with proper meta descriptions. It automatically:

- Detects language-specific Markdown files (e.g., `neetcode_ontology_ai_en.md`, `neetcode_ontology_ai_zh-TW.md`)
- Loads corresponding meta description files (auto-detects from `tools/mindmaps/core/meta/`)
- Generates HTML with proper `<meta name="description">` tags
- Preserves all Markdown content in the HTML output

**Configuration:** `tools/mindmaps/generate_mindmaps_ai.toml`

| Section | What You Can Configure |
|---------|------------------------|
| `[model]` | LLM model, temperature, max tokens |
| `[output]` | Output directory, filename, HTML generation |
| `[ontology]` | Which knowledge graph data to include |
| `[problems]` | Problem filters (difficulty, topics, roadmaps) |
| `[links]` | GitHub repo URL, branch |
| `[advanced]` | Output language(s) (multi-language support) |

**No API Key?** After running, copy `tools/mindmaps/prompts/generated/mindmap-prompt.md` to ChatGPT/Claude.

> 📖 **Detailed usage guide:** [prompts/README.md](https://github.com/lufftw/neetcode/blob/main/tools/mindmaps/prompts/README.md)

---

## 📐 Pattern Documentation Generation

### `generate_pattern_docs.py`

Composes pattern documentation from source files in `meta/patterns/`.

```bash
# Generate all pattern docs
python tools/patterndocs/generate_pattern_docs.py

# Generate specific pattern
python tools/patterndocs/generate_pattern_docs.py --pattern sliding_window
```

**Configuration:** `tools/patterndocs/generate_pattern_docs.toml`

**Source Structure:**

```
meta/patterns/sliding_window/
├── _config.toml        # File ordering (optional)
├── _header.md          # Introduction and core concepts
├──@03-base.md        # Base template problem
├── 0076_variant.md     # Variant problem
├── _comparison.md      # Pattern comparison table
├── _decision.md        # Decision guide
└── _templates.md       # Template code
```

> 📖 **Detailed technical docs:** [patterndocs/README.md](patterndocs/README.md)

### `html_meta_description_generator.py`

Generates SEO-friendly HTML meta descriptions from Markdown files using OpenAI GPT-4o. Follows the Meta Description Generation Spec for optimal search engine result page (SERP) display.

```bash
# Generate descriptions for all configured files
python tools/mindmaps/html_meta_description_generator.py

# Generate description for a specific file
python tools/mindmaps/html_meta_description_generator.py --file docs/mindmaps/pattern-hierarchy.md

# List configured files
python tools/mindmaps/html_meta_description_generator.py --list

# Specify output directory
python tools/mindmaps/html_meta_description_generator.py --output custom/output/dir

# Force overwrite existing files
python tools/mindmaps/html_meta_description_generator.py --force
```

**Configuration:** `tools/mindmaps/html_meta_description_generator.toml`

**Features:**
- Automatic markdown cleaning (removes code blocks, images, links, etc.)
- Language detection (English/Chinese Traditional)
- Length validation (80-160 characters, truncates at sentence boundaries)
- Content validation (removes boilerplate, keyword stuffing, etc.)
- HTML attribute escaping
- OpenAI GPT-4o integration for high-quality descriptions

**Configuration Options:**

| Setting | Description | Default |
|---------|-------------|---------|
| `minLen` | Minimum description length | 80 |
| `maxLen` | Maximum description length | 160 |
| `preferFrontmatterDescription` | Use frontmatter description if available | true |
| `keepInlineCodeContent` | Keep inline code text (remove backticks) | true |
| `keepImageAlt` | Keep image alt text | true |
| `languageMode` | Language mode: "auto", "en", "zh-TW" | "auto" |
| `outputDir` | Output directory for generated files | "tools/mindmaps/core/meta" |

**Prompt Templates:**

The tool uses configurable prompt templates in the `[prompts]` section:
- `system` - System prompt for OpenAI
- `user` - User prompt template with placeholders: `{title}`, `{content_preview}`, `{candidate_info}`, `{language}`

**API Key:**

The OpenAI API key is prompted interactively when running the program (input is hidden for security). No need to set environment variables.

**Example Configuration:**

```toml
[files]
"docs/mindmaps/pattern-hierarchy.md" = { }
"docs/mindmaps/family-derivation.md" = { minLen = 100, maxLen = 155 }
```

---

## 🛠️ Utility Tools

### `text_to_mindmap.py`

Converts plain text to Markmap mind map format.

```bash
python tools/mindmaps/text_to_mindmap.py input.txt -o output.md
```

### `prepare_llm_input.py`

Prepares LLM input data by integrating ontology and problem information.

```bash
python tools/_staging/prepare_llm_input.py --output llm_input.json
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
pytest tools/review-code/validation/tests/test_solution_format.py -v

# Or use standalone script
python tools/review-code/validation/run_format_tests.py
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
├── tools/review-code/validation/tests/  # Format compliance tests
│   └── test_solution_format.py
│
├── tools/mindmaps/tests/                # Mind map tests
│   └── test_post_processing.py
│
├── .dev/tests/                          # Component tests (runner modules)
│   ├── test_generate_mindmaps.py
│   ├── test_generate_pattern_docs.py
│   └── ...
│
└── .dev/tests_solutions/                # Solution correctness tests
    └── test_all_solutions.py
```

**Run All Tests:**

```bash
.dev\run_all_tests.bat    # Windows
.dev/run_all_tests.sh     # Linux/Mac
```

---

## 🔄 Local CI/CD Automation

### Pre-commit Hooks

The project uses [pre-commit](https://pre-commit.com/) framework to automatically generate AI mind maps when relevant files are modified.

#### Setup

```bash
# Install pre-commit (if not already installed)
pip install pre-commit

# Install Git hooks
pre-commit install
```

#### How It Works

When you commit changes to:
- `ontology/` directory
- `meta/problems/` directory  
- `tools/mindmaps/generate_mindmaps.py`

The hook automatically runs `tools/mindmaps/generate_mindmaps_ai.py` to generate AI-powered mind maps.

#### Usage

**Normal workflow (automatic):**

```bash
# Modify relevant files and commit
git add ontology/some_file.json
git commit -m "Update ontology"
# Hook automatically runs, prompts for API key, generates mind maps
```

**Skip AI generation:**

```bash
# Method 1: Use commit message tag
git commit -m "Update ontology [skip-ai]"

# Method 2: Use environment variable
# PowerShell
$env:SKIP_AI_MINDMAPS = "true"
git commit -m "Update ontology"

# CMD
set SKIP_AI_MINDMAPS=true
git commit -m "Update ontology"

# Method 3: Skip all hooks
git commit --no-verify -m "Update ontology"
```

**Manual testing:**

```bash
# Test all hooks
pre-commit run --all-files

# Test specific hook
pre-commit run generate-ai-mindmaps --all-files
```

#### Configuration

- **Config file**: `.pre-commit-config.yaml`
- **Hook script**: `tools/mindmaps/hooks/generate_ai_mindmaps_hook.py`
- **API Key**: Interactive input (not stored in any file)
- **Branch support**: Works on all branches

#### Features

| Feature | Description |
|---------|-------------|
| **Auto-detection** | Detects changes in `ontology/`, `meta/problems/`, `tools/mindmaps/generate_mindmaps.py` |
| **API Key** | Interactive input, never stored |
| **Skip options** | Multiple ways to skip when needed |
| **Branch support** | Works on all branches |
| **Docker Act compatible** | Doesn't interfere with local GitHub Actions testing |

---

## 🔗 Related Documentation

| Document | Description |
|----------|-------------|
| [solution-contract.md](../solution-contract.md) | Solution file specification |
| [generator-contract.md](../generator-contract.md) | Generator file specification |
| [architecture-migration.md](../architecture-migration.md) | Architecture migration guide |
| [mindmaps/README.md](mindmaps/README.md) | Mind map module technical docs |
| [patterndocs/README.md](patterndocs/README.md) | Pattern docs module technical docs |
| [mindmaps/ai-markmap-agent/README.md](mindmaps/ai-markmap-agent/README.md) | AI Markmap Agent docs |
| [prompts/README.md](https://github.com/lufftw/neetcode/blob/main/tools/mindmaps/prompts/README.md) | AI prompts usage guide |

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

1. Create new file in `tools/mindmaps/core/generators/`
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
5. Run `python tools/patterndocs/generate_pattern_docs.py --pattern <name>`

See [patterndocs/README.md](patterndocs/README.md#adding-a-new-pattern)

</details>

# Pattern Documentation Generation Module

This module generates comprehensive pattern documentation by composing ontology definitions and per-problem markdown snippets.

## Overview

The pattern documentation module:
- Composes documentation from multiple source files
- Automatically numbers sections and generates table of contents
- Organizes content by pattern (API kernel)
- Supports multiple problem examples per pattern

## Module Structure

```
patterndocs/
├── __init__.py           # Module exports
├── toml_parser.py        # TOML parsing utilities
├── data.py               # Data classes (APIKernel, Pattern, PatternDocConfig)
├── loader.py             # Ontology loading and kernel ID mapping
├── files.py              # Source file collection and categorization
├── sections.py           # Section numbering and TOC generation
└── composer.py           # Document composition logic
```

## Core Components

### TOML Parser (`toml_parser.py`)

Simple TOML parser for ontology files:
- Handles arrays of tables `[[array]]`
- Parses key-value pairs
- Supports quoted strings

**Key Functions:**
- `parse_toml_simple(content)` - Parse TOML content into dictionary

### Data Classes (`data.py`)

**APIKernel** - Represents an API Kernel:
- `id` - Kernel identifier
- `summary` - Kernel description

**Pattern** - Represents a Pattern:
- `id` - Pattern identifier
- `api_kernel` - Associated kernel ID
- `summary` - Pattern description

**PatternDocConfig** - Configuration for document generation:
- `kernel_id` - Target kernel ID
- `kernel_summary` - Kernel summary
- `source_dir` - Source directory path
- `output_file` - Output file path
- `patterns` - List of patterns for this kernel

### Configuration (`config.py`)

**Functions:**
- `load_generator_config()` - Load global configuration from `config.toml`
- `get_kernel_mapping()` - Get kernel mapping from config or defaults
- `get_paths()` - Get path configuration from config or defaults

**Configuration File:**
Global configuration is stored in `tools/generate_pattern_docs.toml`:
- `[kernel_mapping]` - Maps directory names to API Kernel IDs (only needed for non-auto-inferrable mappings)
- `[default_file_order]` - Default header/footer file ordering
- `[paths]` - Directory paths (optional, defaults to standard locations)

**Auto-inference:**
The `config.py` module automatically infers kernel mappings from `ontology/patterns.toml` by matching pattern IDs with directory names. Only mappings that cannot be automatically determined need to be specified in `generate_pattern_docs.toml`.

**Note:** The Python module `config.py` loads configuration from `generate_pattern_docs.toml` and supplements it with auto-inferred mappings.

### Data Loading (`loader.py`)

**Functions:**
- `load_api_kernels()` - Load API kernels from ontology
- `load_patterns()` - Load patterns grouped by kernel
- `get_available_patterns()` - Get list of pattern directories with source files
- `get_kernel_id_from_dir_name(dir_name)` - Map directory name to kernel ID

**Kernel ID Mapping:**
The module maps directory names to API Kernel IDs (configurable in `generate_pattern_docs.toml`):
- `sliding_window` → `SubstringSlidingWindow`
- `bfs_grid` → `GridBFSMultiSource`
- `backtracking` → `BacktrackingExploration`
- `two_pointers` → `TwoPointersTraversal`
- ... (see `tools/generate_pattern_docs.toml` for full list)

**Paths:**
- `PROJECT_ROOT` - Project root directory (auto-detected)
- `ONTOLOGY_DIR` - Ontology files directory (from config or default: `ontology/`)
- `META_PATTERNS_DIR` - Pattern source files directory (from config or default: `meta/patterns/`)
- `OUTPUT_DIR` - Output documentation directory (from config or default: `docs/patterns/`)

### File Collection (`files.py`)

Categorizes source files into three types and applies ordering from `_config.toml`:

**File Categories:**
1. **Header files** (`_header.md`) - Introduction and core concepts
2. **Problem files** (`0003_base.md`, `0076_variant.md`) - Problem examples
3. **Footer files** (`_comparison.md`, `_decision.md`, `_mapping.md`, `_templates.md`) - Additional sections

**Key Functions:**
- `load_config(source_dir)` - Load file ordering from `_config.toml`
  - Returns: Dictionary with `header_files`, `problem_files`, `footer_files` lists
  - Returns empty dict if config file doesn't exist
- `collect_source_files(source_dir)` - Collect and categorize files
  - Reads `_config.toml` if present to determine file order
  - Falls back to default ordering if config missing
  - Returns: `(header_files, problem_files, footer_files)`

**Constants:**
- `STRUCTURAL_FILES_ORDER` - Default order for header files
- `STRUCTURAL_FILES_FOOTER` - Default order for footer files

**Configuration File Format:**
```toml
# meta/patterns/<pattern_name>/_config.toml
header_files = [
    "_header.md"
]

problem_files = [
    "0003_base.md",
    "0076_variant.md",
    "0209_another.md"
]

footer_files = [
    "_comparison.md",
    "_decision.md",
    "_mapping.md",
    "_templates.md"
]
```

### Section Numbering (`sections.py`)

Handles section numbering and table of contents generation:

**Key Functions:**
- `generate_toc(sections_info)` - Generate table of contents
  - Input: List of `(section_num, title, anchor)` tuples
  - Output: Markdown TOC
- `create_anchor(section_num, title)` - Create markdown anchor
  - Converts title to URL-friendly anchor
- `add_section_numbers(content, section_num)` - Add numbers to sections
  - Returns: `(numbered_content, sections_info)`
  - Handles main sections (`##`) and subsections (`###`)

**Numbering Format:**
- Main sections: `## 1. Section Title`
- Subsections: `### 1.1 Subsection Title`

### Document Composition (`composer.py`)

Composes the final document from source files:

**Key Functions:**
- `compose_document(config, header_files, problem_files, footer_files)` - Compose final document
  - Two-pass process:
    1. Collect all section info for TOC
    2. Generate numbered content
  - Inserts TOC after introduction
  - Adds separators (`---`) between sections
  - Appends footer attribution

**Document Structure:**
```
Introduction (from _header.md)
---
## Table of Contents
---
Core Concepts (from _header.md)
---
Problem 1 (from 0003_base.md)
---
Problem 2 (from 0076_variant.md)
---
Comparison (from _comparison.md)
---
Footer Attribution
```

## Usage Examples

### Basic Usage

```python
from patterndocs import (
    PatternDocConfig,
    load_api_kernels,
    load_patterns,
    get_kernel_id_from_dir_name,
    collect_source_files,
    compose_document,
    META_PATTERNS_DIR,
    OUTPUT_DIR,
)

# Load ontology
kernels = load_api_kernels()
patterns_by_kernel = load_patterns()

# Setup for sliding_window pattern
pattern_name = "sliding_window"
source_dir = META_PATTERNS_DIR / pattern_name
kernel_id = get_kernel_id_from_dir_name(pattern_name)
kernel = kernels[kernel_id]

# Create config
config = PatternDocConfig(
    kernel_id=kernel_id,
    kernel_summary=kernel.summary,
    source_dir=source_dir,
    output_file=OUTPUT_DIR / f"{pattern_name}.md",
    patterns=patterns_by_kernel.get(kernel_id, []),
)

# Collect and compose
header_files, problem_files, footer_files = collect_source_files(source_dir)
document = compose_document(config, header_files, problem_files, footer_files)
```

### Section Numbering

```python
from patterndocs import add_section_numbers, generate_toc

content = """## Core Concepts
Content here.

## Base Template
More content.
"""

numbered, sections_info = add_section_numbers(content, start_num=1)
# Result: "## 1. Core Concepts\n...\n## 2. Base Template\n..."

toc = generate_toc(sections_info)
# Result: "## Table of Contents\n\n1. [Core Concepts](#1-core-concepts)\n..."
```

## Source File Organization

Pattern documentation is organized in `meta/patterns/<pattern_name>/`:

```
meta/patterns/sliding_window/
├── _config.toml            # File ordering configuration (optional)
├── _header.md              # Introduction and core concepts
├── 0003_base.md            # Base template problem (LeetCode 3)
├── 0076_variant.md         # Variant problem (LeetCode 76)
├── _comparison.md          # Pattern comparison table
├── _decision.md            # Decision guide (when to use)
├── _mapping.md             # LeetCode problem mapping (optional)
└── _templates.md           # Template code examples
```

### File Naming Conventions

- **Header files**: Start with `_` (e.g., `_header.md`)
- **Problem files**: Problem number prefix (e.g., `0003_base.md`)
- **Footer files**: Start with `_` (e.g., `_comparison.md`, `_mapping.md`)
- **Config file**: `_config.toml` (excluded from final document)

### File Ordering Configuration

Each pattern directory can include `_config.toml` to control the order of files in the final document. This is especially useful for:
- Ordering problems by LeetCode number (instead of alphabetical)
- Controlling footer section order
- Ensuring consistent document structure

**Example:**
```toml
# Order problems by LeetCode number: 3, 340, 76, 567, 438, 209
problem_files = [
    "0003_base.md",
    "0340_k_distinct.md",
    "0076_min_window.md",
    "0567_permutation.md",
    "0438_anagrams.md",
    "0209_min_subarray.md"
]
```

### File Ordering

Files are processed in this order:
1. Header files (by `_config.toml` → `STRUCTURAL_FILES_ORDER` default)
2. Problem files (by `_config.toml` → alphabetical default)
3. Footer files (by `_config.toml` → `STRUCTURAL_FILES_FOOTER` default)

**Configuration Priority:**
- If `_config.toml` exists: Files are ordered exactly as specified
- If `_config.toml` missing: Uses default ordering (alphabetical for problems)
- Files listed in config but not found: Silently skipped
- Files found but not in config: Appended at end (for problems) or after configured files (for header/footer)

## Output Format

Generated documentation includes:

1. **Introduction** - From `_header.md` (before first `##` section)
2. **Table of Contents** - Auto-generated from all sections
3. **Core Concepts** - From `_header.md` (after TOC)
4. **Problem Sections** - Each problem file becomes a numbered section
5. **Footer Sections** - Comparison, decision trees, templates
6. **Attribution** - API Kernel attribution

**Example Output Structure:**
```markdown
# Sliding Window Patterns

Introduction text here.

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: LeetCode 3](#2-base-template-leetcode-3)
...

---

## 1. Core Concepts

Content from _header.md

---

## 2. Base Template: LeetCode 3

Content from 0003_base.md

---

*Document generated for NeetCode Practice Framework — API Kernel: SubstringSlidingWindow*
```

## Testing

The module is tested in `.dev/tests/test_generate_pattern_docs.py`:

```bash
python -m pytest .dev/tests/test_generate_pattern_docs.py -v
```

Test coverage includes:
- TOML parsing
- Data classes
- Ontology loading
- Kernel ID mapping
- File collection
- Section numbering
- TOC generation
- Document composition
- Edge cases

## Development

### Adding a New Pattern

1. Create directory: `meta/patterns/<pattern_name>/`
2. Add `_header.md` with introduction (required)
3. Add problem files (e.g., `0003_base.md`)
4. Optionally add footer files (`_comparison.md`, `_decision.md`, `_mapping.md`, `_templates.md`)
5. Optionally create `_config.toml` to control file order:
   ```toml
   header_files = ["_header.md"]
   problem_files = ["0003_base.md", "0076_variant.md"]
   footer_files = ["_comparison.md", "_decision.md", "_templates.md"]
   ```
6. Run generator:
   ```bash
   python tools/generate_pattern_docs.py --pattern <pattern_name>
   ```

### Adding Kernel ID Mapping

If a new pattern directory name doesn't match the kernel ID:

1. Add mapping to `tools/patterndocs/config.toml`:
   ```toml
   [kernel_mapping]
   new_pattern = "NewKernelID"
   ```

### Customizing Section Numbering

Modify `add_section_numbers()` in `sections.py` to change:
- Numbering format
- Subsection handling
- Anchor generation

### Module Size Guidelines

- Each file should be < 100 lines
- Keep functions focused and single-purpose
- Document complex logic with comments

## Common Patterns

### Pattern with Multiple Variants

```
meta/patterns/sliding_window/
├── _header.md
├── 0003_base.md          # Base template
├── 0076_variant.md       # Variant 1
├── 0209_variant.md       # Variant 2
└── _comparison.md
```

### Pattern with Decision Tree

```
meta/patterns/binary_search/
├── _header.md
├── 0704_base.md
├── _decision.md          # When to use binary search
└── _templates.md
```

## See Also

- [Main Tools README](../README.md)
- [CLI Usage](https://github.com/lufftw/neetcode/blob/main/tools/generate_pattern_docs.py)
- [Test Suite](https://github.com/lufftw/neetcode/blob/main/.dev/tests/test_generate_pattern_docs.py)
- [Pattern Documentation Output](../../patterns/)



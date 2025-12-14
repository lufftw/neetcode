# Pattern Documentation Index

> **Auto-generated from**: `ontology/` + `meta/patterns/`  
> **Generator**: `tools/generate_pattern_docs.py`

This directory contains comprehensive documentation for each **API Kernel** and its associated problem-solving **Patterns**. Each document serves as a complete reference for understanding, implementing, and applying these patterns.

---

## Available Pattern Guides

| API Kernel | Document | Description | Problems |
|------------|----------|-------------|----------|
| `SubstringSlidingWindow` | [sliding_window.md](sliding_window.md) | Dynamic window over sequences | LeetCode 3, 76, 159, 209, 340, 438, 567 |
| `TwoPointersTraversal` | [two_pointers.md](two_pointers.md) | Two pointer traversal patterns | LeetCode 1, 11, 15, 16, 21, 26, 27, 75, 88, 125, 141, 142, 167, 202, 283, 680, 876 |
| `GridBFSMultiSource` | *coming soon* | Multi-source BFS on grids | LeetCode 994, 286, 542 |
| `BacktrackingExploration` | [backtracking_exploration.md](backtracking_exploration.md) | Exhaustive search with pruning | LeetCode 39, 40, 46, 47, 51, 77, 78, 79, 90, 93, 131, 216 |
| `KWayMerge` | *coming soon* | Merge K sorted sequences | LeetCode 23, 21, 88 |
| `BinarySearchBoundary` | *coming soon* | Binary search boundaries | LeetCode 4, 33, 34, 35 |
| `LinkedListInPlaceReversal` | *coming soon* | In-place linked list reversal | LeetCode 25, 206, 92 |
| `MonotonicStack` | *coming soon* | Monotonic stack patterns | LeetCode 84, 85, 496 |

---

## Document Structure

Each pattern document follows a consistent structure:

```
1. Header
   - API Kernel name and core mechanism
   - Overview of the pattern family

2. Core Concepts
   - Fundamental principles
   - Universal template structure
   - Strategy variants (maximize/minimize/fixed)

3. Base Template Problem
   - The "ancestor" problem that defines the pattern
   - Complete implementation with detailed comments
   - Algorithm explanation and trace examples

4. Variation Problems
   - Each variation shows:
     - Problem statement and invariant
     - Delta from base template (what changes)
     - Complete implementation
     - Key insights

5. Comparison Table
   - Side-by-side comparison of all variations

6. Decision Guide
   - When to use this pattern
   - Decision flowchart

7. Quick Reference Templates
   - Copy-paste ready templates
```

---

## Source Files

Pattern documentation is composed from:

```
meta/
└── patterns/
    └── <api_kernel_id>/
        ├── _header.md        # Core concepts
        ├── _comparison.md    # Comparison table
        ├── _decision.md      # When to use
        ├── _templates.md     # Quick reference
        └── XXXX_<name>.md    # Per-problem snippets
```

### Example: Sliding Window

```
meta/patterns/sliding_window/
├── _config.toml             # File ordering configuration (optional)
├── _header.md               # Invariant, template structure, strategies
├── _comparison.md           # Pattern comparison table
├── _decision.md             # When to use sliding window
├── _templates.md            # Maximize/minimize/fixed templates
├── 0003_base.md             # LeetCode 3 - Base template
├── 0076_min_window.md       # LeetCode 76 - Minimum Window Substring
├── 0209_min_subarray.md     # LeetCode 209 - Minimum Size Subarray Sum
├── 0340_k_distinct.md       # LeetCode 340 - At Most K Distinct
├── 0438_anagrams.md         # LeetCode 438 - Find All Anagrams
└── 0567_permutation.md      # LeetCode 567 - Permutation in String
```

### File Ordering Configuration

Each pattern directory can include a `_config.toml` file to control the order of files in the final document:

```toml
# meta/patterns/<pattern_name>/_config.toml
header_files = ["_header.md"]
problem_files = ["0003_base.md", "0076_min_window.md", ...]
footer_files = ["_comparison.md", "_decision.md", "_templates.md"]
```

- **If `_config.toml` exists**: Files are ordered exactly as specified
- **If `_config.toml` doesn't exist**: Falls back to default ordering (alphabetical for problems)

See [`meta/patterns/README.md`](../../meta/patterns/README.md) for detailed documentation.

---

## Generating Documentation

To regenerate pattern documentation:

```bash
python tools/generate_pattern_docs.py
```

Options:
```bash
# Generate specific pattern
python tools/generate_pattern_docs.py --pattern sliding_window

# Generate all patterns
python tools/generate_pattern_docs.py --all

# Validate only (no write)
python tools/generate_pattern_docs.py --validate
```

---

## Adding New Patterns

### 1. Define in Ontology

Add the API Kernel in `ontology/api_kernels.toml`:
```toml
[[api_kernels]]
id = "NewKernel"
summary = "Description of the kernel mechanism."
```

Add patterns in `ontology/patterns.toml`:
```toml
[[patterns]]
id = "new_pattern_variant"
api_kernel = "NewKernel"
summary = "Description of this specific pattern."
```

### 2. Create Source Files

Create directory and files in `meta/patterns/`:
```
meta/patterns/new_kernel/
├── _header.md
├── _comparison.md
├── _decision.md
├── _templates.md
└── XXXX_problem.md
```

### 3. Generate Documentation

```bash
python tools/generate_pattern_docs.py --pattern new_kernel
```

---

## Relationship to Problem Metadata

Each problem in `meta/problems/*.toml` references patterns:

```toml
# meta/problems/0003_longest_substring_without_repeating_characters.toml
api_kernels = ["SubstringSlidingWindow"]
patterns    = ["sliding_window_unique"]

[pattern_role]
is_base_template = true
base_for_kernel  = "SubstringSlidingWindow"
derived_problems = ["0076", "0159", "0209", "0340", "0438", "0567"]
```

The generator uses this metadata to:
- Order problems correctly (base first, then variations)
- Generate cross-references
- Build the comparison table automatically

---

*Last updated: Auto-generated by `tools/generate_pattern_docs.py`*



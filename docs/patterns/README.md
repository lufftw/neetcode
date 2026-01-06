# Pattern Documentation Index

> **Auto-generated from**: `ontology/` + `meta/patterns/`  
> **Generator**: `tools/patterndocs/generate_pattern_docs.py`

This directory contains comprehensive documentation for each **API Kernel** and its associated problem-solving **Patterns**. Each document serves as a complete reference for understanding, implementing, and applying these patterns.

---

## How to Use This Documentation

Each pattern provides **two learning paths** to help you master the concepts:

| Path | Purpose | Best For |
|------|---------|----------|
| 💡 **Intuition** | Understand the "why" through stories and visual explanations | First-time learners, building mental models |
| 🛠️ **Templates** | Production-ready implementations with problem-specific variations | Interview prep, quick reference |

**Recommended approach**: Start with Intuition to build understanding, then use Templates for implementation.

---

## Available Pattern Guides

| API Kernel | Learning Resources | Description | Problems |
|------------|-------------------|-------------|----------|
| `SubstringSlidingWindow` | 💡 [Intuition](sliding_window/intuition.md) · 🛠️ [Templates](sliding_window/templates.md) | Dynamic window over sequences | LeetCode 3, 76, 159, 209, 340, 438, 567 |
| `TwoPointersTraversal` | 💡 [Intuition](two_pointers/intuition.md) · 🛠️ [Templates](two_pointers/templates.md) | Two pointer traversal patterns | LeetCode 1, 11, 15, 16, 21, 26, 27, 75, 88, 125, 141, 142, 167, 202, 283, 680, 876 |
| `BinarySearchBoundary` | 💡 [Intuition](binary_search/intuition.md) · 🛠️ [Templates](binary_search/templates.md) | Binary search boundaries | LeetCode 33, 34, 35, 81, 162, 875, 1011 |
| `BacktrackingExploration` | 💡 [Intuition](backtracking_exploration/intuition.md) · 🛠️ [Templates](backtracking_exploration/templates.md) | Exhaustive search with pruning | LeetCode 39, 40, 46, 47, 51, 77, 78, 79, 90, 93, 131, 216 |
| `MonotonicStack` | 💡 [Intuition](monotonic_stack/intuition.md) · 🛠️ [Templates](monotonic_stack/templates.md) | Boundary resolution via monotonicity | LeetCode 42, 84, 85, 316, 321, 402, 496, 503, 739, 901, 907, 2104 |
| `PrefixSum` | 💡 [Intuition](prefix_sum/intuition.md) · 🛠️ [Templates](prefix_sum/templates.md) | Range queries and subarray sums | LeetCode 238, 303, 304, 523, 525, 560, 1094, 1109 |
| `Heap` | 💡 [Intuition](heap/intuition.md) · 🛠️ [Templates](heap/templates.md) | Top-K, median, scheduling | LeetCode 23, 215, 253, 295, 347, 621, 1046 |
| `GraphDFS` / `GraphBFS` | 💡 [Intuition](graph/intuition.md) · 🛠️ [Templates](graph/templates.md) | Graph traversal patterns | LeetCode 133, 200, 417, 785, 841, 994, 1971 |
| `IntervalMerge` / `IntervalScheduling` | 💡 [Intuition](interval/intuition.md) · 🛠️ [Templates](interval/templates.md) | Interval merge and scheduling | LeetCode 56, 57, 435, 452, 986 |
| `UnionFindConnectivity` | 💡 [Intuition](union_find/intuition.md) · 🛠️ [Templates](union_find/templates.md) | Disjoint set connectivity | LeetCode 547, 684, 721, 990, 1319 |
| `TreeTraversalDFS` / `TreeTraversalBFS` | 💡 [Intuition](tree/intuition.md) · 🛠️ [Templates](tree/templates.md) | Tree DFS/BFS and path problems | LeetCode 94, 102, 104, 110, 124, 543 |
| `TopologicalSort` | 💡 [Intuition](topological_sort/intuition.md) · 🛠️ [Templates](topological_sort/templates.md) | Dependency ordering and cycle detection | LeetCode 207, 210, 802, 1203 |
| `ShortestPath` | 💡 [Intuition](shortest_path/intuition.md) · 🛠️ [Templates](shortest_path/templates.md) | Dijkstra, 0-1 BFS, Bellman-Ford | LeetCode 743, 787, 1368, 1631, 2290 |
| `Trie` | 💡 [Intuition](trie/intuition.md) · 🛠️ [Templates](trie/templates.md) | Prefix tree operations, autocomplete | LeetCode 208, 211, 212, 648, 1268 |
| `GridBFSMultiSource` | *coming soon* | Multi-source BFS on grids | LeetCode 994, 286, 542 |
| `KWayMerge` | *coming soon* | Merge K sorted sequences | LeetCode 23, 21, 88 |
| `LinkedListInPlaceReversal` | *coming soon* | In-place linked list reversal | LeetCode 25, 206, 92 |

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
        └── XXXX-<name>.md    # Per-problem snippets
```

### Example: Sliding Window

```
meta/patterns/sliding_window/
├── _config.toml             # File ordering configuration (optional)
├── _header.md               # Invariant, template structure, strategies
├── _comparison.md           # Pattern comparison table
├── _decision.md             # When to use sliding window
├── _templates.md            # Maximize/minimize/fixed templates
├── 0003-base.md             # LeetCode 3 - Base template
├── 0076-min-window.md       # LeetCode 76 - Minimum Window Substring
├── 0209-min-subarray.md     # LeetCode 209 - Minimum Size Subarray Sum
├── 0340-k-distinct.md       # LeetCode 340 - At Most K Distinct
├── 0438-anagrams.md         # LeetCode 438 - Find All Anagrams
└── 0567-permutation.md      # LeetCode 567 - Permutation in String
```

### File Ordering Configuration

Each pattern directory can include a `_config.toml` file to control the order of files in the final document:

```toml
# meta/patterns/<pattern_name>/_config.toml
header_files = ["_header.md"]
problem_files = ["0003-base.md", "0076-min-window.md", "0209-min-subarray.md", ...]
footer_files = ["_comparison.md", "_decision.md", "_templates.md"]
```

- **If `_config.toml` exists**: Files are ordered exactly as specified
- **If `_config.toml` doesn't exist**: Falls back to default ordering (alphabetical for problems)

See [`meta/patterns/README.md`](https://github.com/lufftw/neetcode/blob/main/meta/patterns/README.md) for detailed documentation.

---

## Generating Documentation

To regenerate pattern documentation:

```bash
python tools/patterndocs/generate_pattern_docs.py
```

Options:
```bash
# Generate specific pattern
python tools/patterndocs/generate_pattern_docs.py --pattern sliding_window

# Generate all patterns
python tools/patterndocs/generate_pattern_docs.py --all

# Validate only (no write)
python tools/patterndocs/generate_pattern_docs.py --validate
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
└── XXXX-problem.md
```

### 3. Generate Documentation

```bash
python tools/patterndocs/generate_pattern_docs.py --pattern new_kernel
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

*Last updated: Auto-generated by `tools/patterndocs/generate_pattern_docs.py`*



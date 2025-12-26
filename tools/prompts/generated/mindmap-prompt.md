# System Prompt

for AI Mind Map Generation

You are a world-class expert who integrates multiple professional perspectives into a single, cohesive mental model and presentation:

- **Top Software Architect**: You design elegant, scalable architectures and map algorithms/patterns to real system contexts.
- **Distinguished Senior Algorithm Professor**: You explain theory clearly, connect fundamentals to practice, and structure knowledge for learning.
- **Senior Principal Engineer**: You prioritize real-world performance, constraints, and trade-offs; you know what works at scale.
- **LeetCode Learner & Interview Preparer**: You build step-by-step learning paths, highlight high-frequency patterns, and support progression.
- **Competitive Programming Champion**: You recognize patterns quickly, surface optimizations, and provide strong problem-to-technique mapping.

## Mission
Creatively generate **Markmap-format mind maps** from the provided **LeetCode knowledge graph data**. The mind maps must be useful for learners, interview candidates, competitive programmers, and contributors.

**Language requirement (CRITICAL):** Output must be entirely in **English** (titles, labels, descriptions, annotations).

## Your Capabilities
1. **Knowledge Graph Reasoning**: Infer and organize relationships among API Kernels, Patterns, Algorithms, and Data Structures.
2. **Educational Visualization**: Produce intuitive, aesthetically clean mind map hierarchies.
3. **Goal-Aware Emphasis**: Adapt focus and recommendations based on user goals (if provided).
4. **Importance Ranking**: Automatically surface what matters most (core concepts first; details later).

## Markmap Features (Use Actively)
- **Styling**: **bold**, *italic*, ==highlight==, ~~strikethrough~~, `code`
- **Checkboxes**: [ ] To-do, [x] Completed
- **Math**: $O(n \log n)$, $O(n^2)$
- **Code Blocks**:
  ```python
  # example
  ```
- **Tables**: Use for comparisons and quick references
- **Fold**: `<!-- markmap: fold -->` to collapse dense sections
- **Emoji**: Use sparingly for emphasis 🎯📚⚡🔥

## Table Format Guidelines
**Use tables for comparison information** (e.g., Sliding Window variants, DS trade-offs).

✅ GOOD (Table format):
```
| Problem | Invariant | State | Window Size | Goal |
|

---

# User Prompt

------|-----------|-------|-------------|------|
| LeetCode 3 | All unique | freq map | Variable | Max length |
| LeetCode 76 | Covers all | maps | Variable | Min length |
```

## CRITICAL: Problem Reference Format
When referencing LeetCode problems, you **must** use exactly:

```
LeetCode {number}
```

Examples:
- `LeetCode 3`
- `LeetCode 76`
- `LeetCode 121`

**Do NOT include:**
- URLs/links
- Problem titles
- Solution links

(These will be added automatically downstream.)

## Output Format (CRITICAL)
Output must be **valid Markmap Markdown** and must start with this frontmatter:

```
---
title: [Mind Map Title]
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---
```

## Design Principles
1. **Clear hierarchy**: Target **3–5 levels** depth for readability.
2. **Emphasis**: Use **bold** and ==highlight== for key concepts, pitfalls, and must-know items.
3. **Practice linkage**: Tie concepts to specific `LeetCode {number}` references.
4. **Readable beauty**: Use folding for dense areas; keep nodes concise; use emoji lightly.
5. **Learning-friendly**: Include progress cues (checkboxes), difficulty markers, and “next steps”.

## Naming Conventions (CRITICAL)
- Always write **“LeetCode”** in full (never “LC”).
- Always reference problems as **“LeetCode {number}”** (never “LC 1”).
- Maintain consistent naming and formatting throughout.

**Output the Markmap Markdown only. No explanations, preambles, or extra commentary.**

---

You will generate a **single Markmap mind map** from the provided LeetCode knowledge graph data.

## What You Will Receive
After these instructions, you will see a section titled **“## 📊 Data Summary”** containing large JSON blocks.  
**Do not modify, rewrite, reformat, or paraphrase any JSON.** Treat it as read-only input.

## Your Task
Create a learning-optimized mind map that:
1. **Synthesizes** the data into a coherent structure (not a raw dump).
2. **Prioritizes** the most important concepts and relationships for practical problem solving.
3. **Connects** Patterns ⇄ Algorithms ⇄ Data Structures ⇄ API Kernels ⇄ LeetCode problems.
4. **Guides progression** from fundamentals → common patterns → advanced/edge cases.

## Required Output
- Output **only** valid **Markmap Markdown**.
- Begin with the required frontmatter exactly as specified in the System Prompt.
- Use **English only**.

## Content & Structure Requirements
- Use a **clear hierarchy** (aim for **3–5 levels** deep).
- The root should be a concise, descriptive title (e.g., “LeetCode Patterns & Techniques” tailored to the provided data).
- Include the following sections when supported by the data (merge/rename only if it improves clarity):
  - **Core Patterns / Techniques**
  - **Key Data Structures**
  - **Common Algorithms**
  - **API Kernels / Useful Primitives**
  - **Problem Mapping** (organized by pattern or technique)
  - **Pitfalls & Edge Cases**
  - **Complexity & Trade-offs**
  - **Study Plan / Progress Tracker** (checkboxes)

## Problem-Linking Rules (CRITICAL)
- Whenever you mention a problem, use **only** `LeetCode {number}`.
- **No titles, no URLs, no extra annotations** next to the problem reference.

## Emphasis & Pedagogy
- Mark the most important nodes with **bold** and ==highlight==.
- Add brief “why it matters” notes for key patterns (1 short line per node max).
- Include common invariants, templates, and “when to use” cues where relevant.
- Use **tables** for comparisons (e.g., variants of a pattern, DS trade-offs, complexity comparisons).
- Use `<!-- markmap: fold -->` to collapse dense reference sections (e.g., long problem lists or detailed subcases).

## Practicality Requirements
- Include at least:
  - One **comparison table** (if the data supports comparisons).
  - One **template/code block** (language: `python`) for a high-value pattern (if applicable).
  - A **progress tracker** using checkboxes (e.g., by pattern or difficulty).
- Complexity: annotate major techniques with time/space complexity using math notation (e.g., $O(n)$, $O(n \log n)$).

## Quality Bar
- Prefer **actionable, interview-relevant** organization over encyclopedic completeness.
- Avoid redundant nodes; consolidate near-duplicates.
- Keep node text concise; use deeper nesting instead of long sentences.

## Final Check (Before You Output)
- Frontmatter present and correct.
- English-only.
- LeetCode references follow `LeetCode {number}` exactly.
- No JSON echoed back.
- No explanations—**Markmap Markdown only**.

(Next comes: **## 📊 Data Summary** with JSON. Do not edit it.)

## 📊 Data Summary

- **api_kernels**: 20 items
- **patterns**: 65 items
- **algorithms**: 36 items
- **data_structures**: 31 items
- **families**: 34 items
- **topics**: 41 items
- **difficulties**: 3 items
- **companies**: 47 items
- **roadmaps**: 13 items
- **Pattern Docs**: 6 files
- **Pattern Snippets**: 3 directories, 34 snippets
- **Problems**: 45 problems
## 📚 Ontology Knowledge Graph

```json
{
  "api_kernels": [
    {
      "id": "SubstringSlidingWindow",
      "summary": "1D window state machine over sequences with dynamic invariants."
    },
    {
      "id": "GridBFSMultiSource",
      "summary": "Multi-source BFS wavefront propagation on a grid graph."
    },
    {
      "id": "KWayMerge",
      "summary": "Merge K sorted sequences using heap or divide-and-conquer."
    },
    {
      "id": "MonotonicStack",
      "summary": "Stack maintaining monotonic order for next-greater/smaller queries."
    },
    {
      "id": "BinarySearchBoundary",
      "summary": "Binary search for boundary conditions (first >=, last <=, etc.)."
    },
    {
      "id": "UnionFindConnectivity",
      "summary": "Disjoint set union for connectivity queries."
    },
    {
      "id": "BacktrackingExploration",
      "summary": "Exhaustive search with pruning for combinatorial problems."
    },
    {
      "id": "LinkedListInPlaceReversal",
      "summary": "Reverse linked list nodes in-place with pointer manipulation."
    },
    {
      "id": "TwoPointerPartition",
      "summary": "Partition array using two pointers (Dutch flag, quick select)."
    },
    {
      "id": "TwoPointersTraversal",
      "summary": "Traverse sequence with two coordinated pointers under invariant-preserving rules."
    },
    {
      "id": "FastSlowPointers",
      "summary": "Two pointers at different speeds for cycle detection and midpoint finding."
    },
    {
      "id": "MergeSortedSequences",
      "summary": "Merge two sorted sequences using two pointers."
    },
    {
      "id": "PrefixSumRangeQuery",
      "summary": "Precomputed cumulative sums for O(1) range sum queries."
    },
    {
      "id": "TreeTraversalDFS",
      "summary": "Depth-first tree traversal (preorder, inorder, postorder)."
    },
    {
      "id": "TreeTraversalBFS",
      "summary": "Level-order tree traversal using queue."
    },
    {
      "id": "DPSequence",
      "summary": "Dynamic programming on linear sequences (LIS, LCS, etc.)."
    },
    {
      "id": "DPInterval",
      "summary": "Dynamic programming on intervals/ranges."
    },
    {
      "id": "TopologicalSort",
      "summary": "Ordering nodes in DAG respecting edge directions."
    },
    {
      "id": "TriePrefixSearch",
      "summary": "Trie-based prefix matching and autocomplete."
    },
    {
      "id": "HeapTopK",
      "summary": "Maintain top K elements using heap."
    }
  ],
  "patterns": [
    {
      "id": "sliding_window_unique",
      "api_kernel": "SubstringSlidingWindow",
      "summary": "Window where all elements are unique."
    },
    {
      "id": "sliding_window_at_most_k_distinct",
      "api_kernel": "SubstringSlidingWindow",
      "summary": "Window with at most K distinct elements."
    },
    {
      "id": "sliding_window_freq_cover",
      "api_kernel": "SubstringSlidingWindow",
      "summary": "Window must cover all required character frequencies."
    },
    {
      "id": "sliding_window_cost_bounded",
      "api_kernel": "SubstringSlidingWindow",
      "summary": "Window with sum/cost constraint."
    },
    {
      "id": "sliding_window_fixed_size",
      "api_kernel": "SubstringSlidingWindow",
      "summary": "Fixed-size sliding window."
    },
    {
      "id": "grid_bfs_propagation",
      "api_kernel": "GridBFSMultiSource",
      "summary": "Layered BFS expansion from multiple sources on a grid."
    },
    {
      "id": "bfs_shortest_path",
      "api_kernel": "GridBFSMultiSource",
      "summary": "Find shortest path in unweighted graph using BFS."
    },
    {
      "id": "bfs_level_order",
      "api_kernel": "TreeTraversalBFS",
      "summary": "Process tree/graph level by level."
    },
    {
      "id": "merge_k_sorted_heap",
      "api_kernel": "KWayMerge",
      "summary": "K-way merge using min-heap."
    },
    {
      "id": "merge_k_sorted_divide",
      "api_kernel": "KWayMerge",
      "summary": "K-way merge using divide-and-conquer."
    },
    {
      "id": "merge_two_sorted",
      "api_kernel": "KWayMerge",
      "summary": "Merge two sorted sequences."
    },
    {
      "id": "next_greater_element",
      "api_kernel": "MonotonicStack",
      "summary": "Find next greater element for each position."
    },
    {
      "id": "next_smaller_element",
      "api_kernel": "MonotonicStack",
      "summary": "Find next smaller element for each position."
    },
    {
      "id": "histogram_max_rectangle",
      "api_kernel": "MonotonicStack",
      "summary": "Find largest rectangle in histogram."
    },
    {
      "id": "binary_search_first_true",
      "api_kernel": "BinarySearchBoundary",
      "summary": "Find first index where predicate becomes true."
    },
    {
      "id": "binary_search_last_true",
      "api_kernel": "BinarySearchBoundary",
      "summary": "Find last index where predicate is true."
    },
    {
      "id": "binary_search_on_answer",
      "api_kernel": "BinarySearchBoundary",
      "summary": "Binary search on answer space (minimize/maximize)."
    },
    {
      "id": "binary_search_rotated",
      "api_kernel": "BinarySearchBoundary",
      "summary": "Binary search in rotated sorted array."
    },
    {
      "id": "backtracking_permutation",
      "api_kernel": "BacktrackingExploration",
      "summary": "Generate all permutations with backtracking."
    },
    {
      "id": "backtracking_combination",
      "api_kernel": "BacktrackingExploration",
      "summary": "Generate all combinations with backtracking."
    },
    {
      "id": "backtracking_subset",
      "api_kernel": "BacktrackingExploration",
      "summary": "Generate all subsets with backtracking."
    },
    {
      "id": "backtracking_n_queens",
      "api_kernel": "BacktrackingExploration",
      "summary": "Place N queens on board with constraint checking."
    },
    {
      "id": "backtracking_sudoku",
      "api_kernel": "BacktrackingExploration",
      "summary": "Fill sudoku grid with constraint propagation."
    },
    {
      "id": "backtracking_combination_sum",
      "api_kernel": "BacktrackingExploration",
      "summary": "Find combinations that sum to target, with or without reuse."
    },
    {
      "id": "backtracking_combination_dedup",
      "api_kernel": "BacktrackingExploration",
      "summary": "Combinations with duplicate handling via same-level skip."
    },
    {
      "id": "backtracking_permutation_dedup",
      "api_kernel": "BacktrackingExploration",
      "summary": "Unique permutations with sorting and same-level deduplication."
    },
    {
      "id": "backtracking_subset_dedup",
      "api_kernel": "BacktrackingExploration",
      "summary": "Unique subsets with sorting and same-level deduplication."
    },
    {
      "id": "backtracking_string_segmentation",
      "api_kernel": "BacktrackingExploration",
      "summary": "Partition string into valid segments (IP, palindromes)."
    },
    {
      "id": "backtracking_grid_path",
      "api_kernel": "BacktrackingExploration",
      "summary": "DFS path search in grid with visited marking."
    },
    {
      "id": "linked_list_k_group_reversal",
      "api_kernel": "LinkedListInPlaceReversal",
      "summary": "Reverse linked list in groups of K nodes."
    },
    {
      "id": "linked_list_full_reversal",
      "api_kernel": "LinkedListInPlaceReversal",
      "summary": "Reverse entire linked list."
    },
    {
      "id": "linked_list_partial_reversal",
      "api_kernel": "LinkedListInPlaceReversal",
      "summary": "Reverse portion of linked list between positions."
    },
    {
      "id": "two_pointer_opposite",
      "api_kernel": "TwoPointersTraversal",
      "summary": "Two pointers moving towards each other from opposite ends."
    },
    {
      "id": "two_pointer_opposite_search",
      "api_kernel": "TwoPointersTraversal",
      "summary": "Opposite pointers for searching pairs in sorted array."
    },
    {
      "id": "two_pointer_opposite_palindrome",
      "api_kernel": "TwoPointersTraversal",
      "summary": "Opposite pointers for symmetric/palindrome checks."
    },
    {
      "id": "two_pointer_opposite_maximize",
      "api_kernel": "TwoPointersTraversal",
      "summary": "Opposite pointers to maximize a function (e.g., container area)."
    },
    {
      "id": "two_pointer_same_direction",
      "api_kernel": "TwoPointersTraversal",
      "summary": "Two pointers moving in same direction (reader/writer)."
    },
    {
      "id": "two_pointer_writer_dedup",
      "api_kernel": "TwoPointersTraversal",
      "summary": "Reader/writer pattern for in-place deduplication."
    },
    {
      "id": "two_pointer_writer_remove",
      "api_kernel": "TwoPointersTraversal",
      "summary": "Reader/writer pattern for in-place element removal."
    },
    {
      "id": "two_pointer_writer_compact",
      "api_kernel": "TwoPointersTraversal",
      "summary": "Reader/writer pattern for array compaction (move zeroes)."
    },
    {
      "id": "fast_slow_cycle_detect",
      "api_kernel": "FastSlowPointers",
      "summary": "Floyd's algorithm Phase 1: detect cycle existence."
    },
    {
      "id": "fast_slow_cycle_start",
      "api_kernel": "FastSlowPointers",
      "summary": "Floyd's algorithm Phase 2: find cycle start node."
    },
    {
      "id": "fast_slow_midpoint",
      "api_kernel": "FastSlowPointers",
      "summary": "Fast-slow pointers to find midpoint of linked list."
    },
    {
      "id": "fast_slow_implicit_cycle",
      "api_kernel": "FastSlowPointers",
      "summary": "Cycle detection on implicit sequence (e.g., Happy Number)."
    },
    {
      "id": "dutch_flag_partition",
      "api_kernel": "TwoPointerPartition",
      "summary": "Three-way partition (Dutch national flag)."
    },
    {
      "id": "two_way_partition",
      "api_kernel": "TwoPointerPartition",
      "summary": "Two-way partition (even/odd, positive/negative)."
    },
    {
      "id": "quickselect_partition",
      "api_kernel": "TwoPointerPartition",
      "summary": "Partition-based selection for Kth element."
    },
    {
      "id": "two_pointer_three_sum",
      "api_kernel": "TwoPointersTraversal",
      "summary": "Sorted array 3Sum with deduplication."
    },
    {
      "id": "two_pointer_k_sum",
      "api_kernel": "TwoPointersTraversal",
      "summary": "Generalized k-Sum using nested two-pointer search."
    },
    {
      "id": "merge_two_sorted_lists",
      "api_kernel": "MergeSortedSequences",
      "summary": "Merge two sorted linked lists."
    },
    {
      "id": "merge_two_sorted_arrays",
      "api_kernel": "MergeSortedSequences",
      "summary": "Merge two sorted arrays (in-place or new array)."
    },
    {
      "id": "merge_sorted_from_ends",
      "api_kernel": "MergeSortedSequences",
      "summary": "Merge by comparing from ends (e.g., squares of sorted array)."
    },
    {
      "id": "dp_fibonacci_style",
      "api_kernel": "DPSequence",
      "summary": "DP with simple recurrence like Fibonacci."
    },
    {
      "id": "dp_longest_increasing",
      "api_kernel": "DPSequence",
      "summary": "Longest increasing subsequence pattern."
    },
    {
      "id": "dp_knapsack",
      "api_kernel": "DPSequence",
      "summary": "0/1 knapsack and variants."
    },
    {
      "id": "dp_palindrome",
      "api_kernel": "DPInterval",
      "summary": "Palindrome-related DP (longest, count, etc.)."
    },
    {
      "id": "tree_dfs_recursive",
      "api_kernel": "TreeTraversalDFS",
      "summary": "Recursive DFS on tree."
    },
    {
      "id": "tree_dfs_iterative",
      "api_kernel": "TreeTraversalDFS",
      "summary": "Iterative DFS using explicit stack."
    },
    {
      "id": "heap_top_k",
      "api_kernel": "HeapTopK",
      "summary": "Find/maintain top K elements."
    },
    {
      "id": "heap_kth_element",
      "api_kernel": "HeapTopK",
      "summary": "Find Kth largest/smallest element."
    },
    {
      "id": "heap_median_stream",
      "api_kernel": "HeapTopK",
      "summary": "Maintain median of data stream using two heaps."
    },
    {
      "id": "union_find_connected_components",
      "api_kernel": "UnionFindConnectivity",
      "summary": "Count/identify connected components."
    },
    {
      "id": "union_find_cycle_detection",
      "api_kernel": "UnionFindConnectivity",
      "summary": "Detect cycle in undirected graph."
    },
    {
      "id": "prefix_sum_range_query",
      "api_kernel": "PrefixSumRangeQuery",
      "summary": "Answer range sum queries in O(1)."
    },
    {
      "id": "prefix_sum_subarray_sum",
      "api_kernel": "PrefixSumRangeQuery",
      "summary": "Find subarrays with target sum using prefix sum + hash map."
    }
  ],
  "algorithms": [
    {
      "id": "graph_traversal",
      "kind": "category",
      "parent": "",
      "summary": "Algorithms for traversing graph structures."
    },
    {
      "id": "sorting",
      "kind": "category",
      "parent": "",
      "summary": "Algorithms for ordering elements."
    },
    {
      "id": "searching",
      "kind": "category",
      "parent": "",
      "summary": "Algorithms for finding elements."
    },
    {
      "id": "bfs",
      "kind": "core",
      "parent": "graph_traversal",
      "summary": "Breadth-first search using a queue."
    },
    {
      "id": "dfs",
      "kind": "core",
      "parent": "graph_traversal",
      "summary": "Depth-first search using recursion or stack."
    },
    {
      "id": "dijkstra",
      "kind": "core",
      "parent": "graph_traversal",
      "summary": "Shortest path in weighted graph using priority queue."
    },
    {
      "id": "bellman_ford",
      "kind": "core",
      "parent": "graph_traversal",
      "summary": "Shortest path with negative edges."
    },
    {
      "id": "floyd_warshall",
      "kind": "core",
      "parent": "graph_traversal",
      "summary": "All-pairs shortest path."
    },
    {
      "id": "topological_sort",
      "kind": "core",
      "parent": "graph_traversal",
      "summary": "Order DAG nodes respecting edge directions."
    },
    {
      "id": "binary_search",
      "kind": "core",
      "parent": "searching",
      "summary": "Divide search space by half each step."
    },
    {
      "id": "merge_sort",
      "kind": "core",
      "parent": "sorting",
      "summary": "Divide-and-conquer sorting algorithm."
    },
    {
      "id": "quick_sort",
      "kind": "core",
      "parent": "sorting",
      "summary": "Partition-based sorting algorithm."
    },
    {
      "id": "heap_sort",
      "kind": "core",
      "parent": "sorting",
      "summary": "Sorting using heap data structure."
    },
    {
      "id": "counting_sort",
      "kind": "core",
      "parent": "sorting",
      "summary": "Linear time sorting for bounded integers."
    },
    {
      "id": "kmp",
      "kind": "core",
      "parent": "searching",
      "summary": "Knuth-Morris-Pratt string matching."
    },
    {
      "id": "rabin_karp",
      "kind": "core",
      "parent": "searching",
      "summary": "Rolling hash string matching."
    },
    {
      "id": "two_pointers",
      "kind": "technique",
      "parent": "",
      "summary": "Move two indices over a sequence under some rule."
    },
    {
      "id": "sliding_window",
      "kind": "technique",
      "parent": "two_pointers",
      "summary": "Maintain a dynamic window [L,R] with an invariant."
    },
    {
      "id": "fast_slow_pointers",
      "kind": "technique",
      "parent": "two_pointers",
      "summary": "Two pointers moving at different speeds (cycle detection)."
    },
    {
      "id": "opposite_pointers",
      "kind": "technique",
      "parent": "two_pointers",
      "summary": "Two pointers starting from opposite ends moving toward center."
    },
    {
      "id": "reader_writer_pointers",
      "kind": "technique",
      "parent": "two_pointers",
      "summary": "Same-direction pointers for in-place array modification."
    },
    {
      "id": "dutch_national_flag",
      "kind": "technique",
      "parent": "two_pointers",
      "summary": "Three-way partitioning using multiple pointers."
    },
    {
      "id": "floyd_cycle_detection",
      "kind": "core",
      "parent": "two_pointers",
      "summary": "Tortoise and hare algorithm for cycle detection."
    },
    {
      "id": "quickselect",
      "kind": "core",
      "parent": "sorting",
      "summary": "Selection algorithm using partition to find kth element."
    },
    {
      "id": "prefix_sum",
      "kind": "technique",
      "parent": "",
      "summary": "Precompute cumulative sums for range queries."
    },
    {
      "id": "monotonic_stack",
      "kind": "technique",
      "parent": "",
      "summary": "Stack maintaining monotonic order for efficient queries."
    },
    {
      "id": "monotonic_queue",
      "kind": "technique",
      "parent": "",
      "summary": "Queue maintaining monotonic order for sliding window max/min."
    },
    {
      "id": "union_find",
      "kind": "technique",
      "parent": "",
      "summary": "Disjoint set with union and find operations."
    },
    {
      "id": "recursion",
      "kind": "technique",
      "parent": "",
      "summary": "Function calling itself to solve subproblems."
    },
    {
      "id": "memoization",
      "kind": "technique",
      "parent": "",
      "summary": "Cache recursive results to avoid recomputation."
    },
    {
      "id": "bit_manipulation",
      "kind": "technique",
      "parent": "",
      "summary": "Use bitwise operations for efficient computation."
    },
    {
      "id": "greedy",
      "kind": "paradigm",
      "parent": "",
      "summary": "Make locally optimal choices at each step."
    },
    {
      "id": "dynamic_programming",
      "kind": "paradigm",
      "parent": "",
      "summary": "Optimal substructure + overlapping subproblems."
    },
    {
      "id": "divide_and_conquer",
      "kind": "paradigm",
      "parent": "",
      "summary": "Split problem into subproblems, solve, and combine."
    },
    {
      "id": "backtracking",
      "kind": "paradigm",
      "parent": "",
      "summary": "Explore all possibilities with pruning."
    },
    {
      "id": "branch_and_bound",
      "kind": "paradigm",
      "parent": "",
      "summary": "Systematic enumeration with bounds-based pruning."
    }
  ],
  "data_structures": [
    {
      "id": "associative_container",
      "parent": "",
      "summary": "Containers with key-based access."
    },
    {
      "id": "priority_queue",
      "parent": "",
      "summary": "Queue with priority ordering."
    },
    {
      "id": "tree",
      "parent": "",
      "summary": "Hierarchical node structure."
    },
    {
      "id": "array",
      "parent": "",
      "summary": "Contiguous indexed collection."
    },
    {
      "id": "string",
      "parent": "array",
      "summary": "Character array."
    },
    {
      "id": "matrix",
      "parent": "array",
      "summary": "2D array."
    },
    {
      "id": "stack",
      "parent": "",
      "summary": "LIFO collection."
    },
    {
      "id": "queue",
      "parent": "",
      "summary": "FIFO collection."
    },
    {
      "id": "deque",
      "parent": "",
      "summary": "Double-ended queue."
    },
    {
      "id": "hash_map",
      "parent": "associative_container",
      "summary": "Key-value store with O(1) average access."
    },
    {
      "id": "hash_set",
      "parent": "associative_container",
      "summary": "Unique element collection with O(1) average lookup."
    },
    {
      "id": "counter",
      "parent": "hash_map",
      "summary": "Hash map for counting occurrences."
    },
    {
      "id": "min_heap",
      "parent": "priority_queue",
      "summary": "Binary heap for min-priority queue."
    },
    {
      "id": "max_heap",
      "parent": "priority_queue",
      "summary": "Binary heap for max-priority queue."
    },
    {
      "id": "linked_list",
      "parent": "",
      "summary": "Linear collection with O(1) insert/delete at known position."
    },
    {
      "id": "doubly_linked_list",
      "parent": "linked_list",
      "summary": "Linked list with prev and next pointers."
    },
    {
      "id": "binary_tree",
      "parent": "tree",
      "summary": "Tree where each node has at most two children."
    },
    {
      "id": "binary_search_tree",
      "parent": "binary_tree",
      "summary": "Binary tree with ordered property."
    },
    {
      "id": "balanced_bst",
      "parent": "binary_search_tree",
      "summary": "Self-balancing BST (AVL, Red-Black)."
    },
    {
      "id": "n_ary_tree",
      "parent": "tree",
      "summary": "Tree where each node can have N children."
    },
    {
      "id": "trie",
      "parent": "tree",
      "summary": "Prefix tree for string operations."
    },
    {
      "id": "segment_tree",
      "parent": "tree",
      "summary": "Tree for range queries and updates."
    },
    {
      "id": "binary_indexed_tree",
      "parent": "tree",
      "summary": "Fenwick tree for prefix operations."
    },
    {
      "id": "graph",
      "parent": "",
      "summary": "Nodes and edges structure."
    },
    {
      "id": "adjacency_list",
      "parent": "graph",
      "summary": "Graph represented as list of neighbors."
    },
    {
      "id": "adjacency_matrix",
      "parent": "graph",
      "summary": "Graph represented as 2D matrix."
    },
    {
      "id": "grid",
      "parent": "graph",
      "summary": "2D matrix as implicit graph."
    },
    {
      "id": "disjoint_set",
      "parent": "",
      "summary": "Union-Find data structure."
    },
    {
      "id": "monotonic_stack",
      "parent": "stack",
      "summary": "Stack maintaining monotonic order."
    },
    {
      "id": "monotonic_deque",
      "parent": "deque",
      "summary": "Deque maintaining monotonic order."
    },
    {
      "id": "lru_cache",
      "parent": "",
      "summary": "Least Recently Used cache (hash map + doubly linked list)."
    }
  ],
  "families": [
    {
      "id": "substring_window",
      "summary": "Problems about finding optimal substrings using sliding window."
    },
    {
      "id": "graph_wavefront",
      "summary": "Problems involving BFS propagation / shortest path on graphs."
    },
    {
      "id": "merge_sorted",
      "summary": "Problems merging multiple sorted sequences."
    },
    {
      "id": "stack_monotonic",
      "summary": "Problems using monotonic stack for range queries."
    },
    {
      "id": "binary_search_answer",
      "summary": "Problems where answer is found by binary searching a value space."
    },
    {
      "id": "backtracking_combinatorial",
      "summary": "Problems generating permutations, combinations, or placements."
    },
    {
      "id": "combination_sum",
      "summary": "Problems finding combinations that sum to a target value."
    },
    {
      "id": "string_segmentation",
      "summary": "Problems partitioning strings into valid segments (IP, palindromes)."
    },
    {
      "id": "grid_path_search",
      "summary": "Problems finding paths in 2D grids using DFS/backtracking."
    },
    {
      "id": "constraint_satisfaction",
      "summary": "Problems like N-Queens requiring constraint checking during search."
    },
    {
      "id": "linked_list_manipulation",
      "summary": "Problems involving in-place linked list operations."
    },
    {
      "id": "tree_traversal",
      "summary": "Problems involving tree traversal patterns."
    },
    {
      "id": "tree_construction",
      "summary": "Problems building trees from traversal orders."
    },
    {
      "id": "tree_path",
      "summary": "Problems finding paths in trees."
    },
    {
      "id": "dynamic_programming_sequence",
      "summary": "DP problems on sequences (LIS, LCS, etc.)."
    },
    {
      "id": "dynamic_programming_grid",
      "summary": "DP problems on 2D grids."
    },
    {
      "id": "dynamic_programming_string",
      "summary": "DP problems on strings (edit distance, regex, etc.)."
    },
    {
      "id": "two_sum_variants",
      "summary": "Problems finding pairs/tuples with target sum."
    },
    {
      "id": "interval_scheduling",
      "summary": "Problems involving interval merging, scheduling, or overlap."
    },
    {
      "id": "graph_connectivity",
      "summary": "Problems about connected components, reachability."
    },
    {
      "id": "graph_shortest_path",
      "summary": "Problems finding shortest paths in graphs."
    },
    {
      "id": "graph_cycle",
      "summary": "Problems detecting or using cycles in graphs."
    },
    {
      "id": "heap_priority",
      "summary": "Problems using heap for priority-based selection."
    },
    {
      "id": "string_matching",
      "summary": "Problems involving pattern matching in strings."
    },
    {
      "id": "array_partition",
      "summary": "Problems partitioning arrays based on conditions."
    },
    {
      "id": "two_pointers_optimization",
      "summary": "Problems using opposite pointers to optimize over sorted/symmetric data."
    },
    {
      "id": "in_place_array_modification",
      "summary": "Problems requiring in-place array modification using reader/writer pointers."
    },
    {
      "id": "linked_list_cycle",
      "summary": "Problems involving cycle detection or finding cycle start in linked structures."
    },
    {
      "id": "multi_sum_enumeration",
      "summary": "Problems finding all unique tuples with target sum (3Sum, 4Sum, etc.)."
    },
    {
      "id": "sequence_merge",
      "summary": "Problems merging sorted sequences using two-pointer technique."
    },
    {
      "id": "palindrome_validation",
      "summary": "Problems validating or constructing palindromes."
    },
    {
      "id": "matrix_traversal",
      "summary": "Problems traversing 2D matrices in various patterns."
    },
    {
      "id": "bit_manipulation",
      "summary": "Problems using bitwise operations."
    },
    {
      "id": "math_number_theory",
      "summary": "Problems involving number theory concepts."
    }
  ],
  "topics": [
    {
      "id": "array",
      "summary": "Problems involving array manipulation."
    },
    {
      "id": "string",
      "summary": "Problems involving string processing."
    },
    {
      "id": "hash_table",
      "summary": "Problems using hash-based structures."
    },
    {
      "id": "linked_list",
      "summary": "Problems on linked list structures."
    },
    {
      "id": "stack",
      "summary": "Problems using stack data structure."
    },
    {
      "id": "queue",
      "summary": "Problems using queue data structure."
    },
    {
      "id": "tree",
      "summary": "Problems on tree structures."
    },
    {
      "id": "binary_tree",
      "summary": "Problems on binary trees."
    },
    {
      "id": "binary_search_tree",
      "summary": "Problems on BST."
    },
    {
      "id": "graph",
      "summary": "Problems on graph structures."
    },
    {
      "id": "breadth_first_search",
      "summary": "Problems using BFS."
    },
    {
      "id": "depth_first_search",
      "summary": "Problems using DFS."
    },
    {
      "id": "dynamic_programming",
      "summary": "Problems using DP approach."
    },
    {
      "id": "greedy",
      "summary": "Problems using greedy strategy."
    },
    {
      "id": "backtracking",
      "summary": "Problems using backtracking."
    },
    {
      "id": "binary_search",
      "summary": "Problems using binary search."
    },
    {
      "id": "sliding_window",
      "summary": "Problems using sliding window technique."
    },
    {
      "id": "two_pointers",
      "summary": "Problems using two pointers technique."
    },
    {
      "id": "heap",
      "summary": "Problems using heap/priority queue."
    },
    {
      "id": "sorting",
      "summary": "Problems involving sorting."
    },
    {
      "id": "math",
      "summary": "Problems requiring mathematical reasoning."
    },
    {
      "id": "bit_manipulation",
      "summary": "Problems using bit operations."
    },
    {
      "id": "recursion",
      "summary": "Problems solved recursively."
    },
    {
      "id": "divide_and_conquer",
      "summary": "Problems using divide and conquer."
    },
    {
      "id": "union_find",
      "summary": "Problems using disjoint set union."
    },
    {
      "id": "trie",
      "summary": "Problems using trie data structure."
    },
    {
      "id": "matrix",
      "summary": "Problems on 2D matrices."
    },
    {
      "id": "simulation",
      "summary": "Problems requiring step-by-step simulation."
    },
    {
      "id": "design",
      "summary": "Problems about designing data structures."
    },
    {
      "id": "counting",
      "summary": "Problems involving counting occurrences."
    },
    {
      "id": "prefix_sum",
      "summary": "Problems using prefix sum technique."
    },
    {
      "id": "monotonic_stack",
      "summary": "Problems using monotonic stack."
    },
    {
      "id": "ordered_set",
      "summary": "Problems using ordered set/map."
    },
    {
      "id": "geometry",
      "summary": "Problems involving geometric concepts."
    },
    {
      "id": "number_theory",
      "summary": "Problems involving number theory."
    },
    {
      "id": "combinatorics",
      "summary": "Problems involving combinations/permutations."
    },
    {
      "id": "game_theory",
      "summary": "Problems involving game theory concepts."
    },
    {
      "id": "topological_sort",
      "summary": "Problems using topological ordering."
    },
    {
      "id": "shortest_path",
      "summary": "Problems finding shortest paths."
    },
    {
      "id": "memoization",
      "summary": "Problems using memoization."
    },
    {
      "id": "interactive",
      "summary": "Interactive problems with queries."
    }
  ],
  "difficulties": [
    {
      "id": "easy",
      "level": 1,
      "color": "green",
      "summary": "Beginner-friendly problems."
    },
    {
      "id": "medium",
      "level": 2,
      "color": "orange",
      "summary": "Intermediate problems."
    },
    {
      "id": "hard",
      "level": 3,
      "color": "red",
      "summary": "Advanced problems."
    }
  ],
  "companies": [
    {
      "id": "google",
      "name": "Google"
    },
    {
      "id": "meta",
      "name": "Meta (Facebook)"
    },
    {
      "id": "amazon",
      "name": "Amazon"
    },
    {
      "id": "microsoft",
      "name": "Microsoft"
    },
    {
      "id": "apple",
      "name": "Apple"
    },
    {
      "id": "netflix",
      "name": "Netflix"
    },
    {
      "id": "uber",
      "name": "Uber"
    },
    {
      "id": "lyft",
      "name": "Lyft"
    },
    {
      "id": "airbnb",
      "name": "Airbnb"
    },
    {
      "id": "linkedin",
      "name": "LinkedIn"
    },
    {
      "id": "twitter",
      "name": "Twitter (X)"
    },
    {
      "id": "bloomberg",
      "name": "Bloomberg"
    },
    {
      "id": "adobe",
      "name": "Adobe"
    },
    {
      "id": "oracle",
      "name": "Oracle"
    },
    {
      "id": "salesforce",
      "name": "Salesforce"
    },
    {
      "id": "bytedance",
      "name": "ByteDance"
    },
    {
      "id": "tiktok",
      "name": "TikTok"
    },
    {
      "id": "nvidia",
      "name": "NVIDIA"
    },
    {
      "id": "intel",
      "name": "Intel"
    },
    {
      "id": "paypal",
      "name": "PayPal"
    },
    {
      "id": "stripe",
      "name": "Stripe"
    },
    {
      "id": "snap",
      "name": "Snap"
    },
    {
      "id": "pinterest",
      "name": "Pinterest"
    },
    {
      "id": "walmart",
      "name": "Walmart"
    },
    {
      "id": "jpmorgan",
      "name": "JPMorgan"
    },
    {
      "id": "goldman_sachs",
      "name": "Goldman Sachs"
    },
    {
      "id": "citadel",
      "name": "Citadel"
    },
    {
      "id": "two_sigma",
      "name": "Two Sigma"
    },
    {
      "id": "jane_street",
      "name": "Jane Street"
    },
    {
      "id": "dropbox",
      "name": "Dropbox"
    },
    {
      "id": "spotify",
      "name": "Spotify"
    },
    {
      "id": "shopify",
      "name": "Shopify"
    },
    {
      "id": "doordash",
      "name": "DoorDash"
    },
    {
      "id": "instacart",
      "name": "Instacart"
    },
    {
      "id": "robinhood",
      "name": "Robinhood"
    },
    {
      "id": "coinbase",
      "name": "Coinbase"
    },
    {
      "id": "databricks",
      "name": "Databricks"
    },
    {
      "id": "snowflake",
      "name": "Snowflake"
    },
    {
      "id": "splunk",
      "name": "Splunk"
    },
    {
      "id": "vmware",
      "name": "VMware"
    },
    {
      "id": "cisco",
      "name": "Cisco"
    },
    {
      "id": "ibm",
      "name": "IBM"
    },
    {
      "id": "samsung",
      "name": "Samsung"
    },
    {
      "id": "huawei",
      "name": "Huawei"
    },
    {
      "id": "alibaba",
      "name": "Alibaba"
    },
    {
      "id": "tencent",
      "name": "Tencent"
    },
    {
      "id": "baidu",
      "name": "Baidu"
    }
  ],
  "roadmaps": [
    {
      "id": "neetcode_150",
      "name": "NeetCode 150",
      "url": "https://neetcode.io/roadmap",
      "summary": "Curated 150 problems for coding interview prep."
    },
    {
      "id": "neetcode_all",
      "name": "NeetCode All",
      "url": "https://neetcode.io/practice",
      "summary": "Complete NeetCode problem set."
    },
    {
      "id": "blind_75",
      "name": "Blind 75",
      "url": "https://leetcode.com/discuss/general-discussion/460599/blind-75",
      "summary": "Classic 75 interview questions from Blind."
    },
    {
      "id": "grind_75",
      "name": "Grind 75",
      "url": "https://www.techinterviewhandbook.org/grind75",
      "summary": "Updated interview prep list with time-based scheduling."
    },
    {
      "id": "leetcode_top_100",
      "name": "LeetCode Top 100 Liked",
      "url": "https://leetcode.com/problemset/top-100-liked-questions/",
      "summary": "Most liked problems on LeetCode."
    },
    {
      "id": "leetcode_top_interview",
      "name": "LeetCode Top Interview Questions",
      "url": "https://leetcode.com/problemset/top-interview-questions/",
      "summary": "Frequently asked interview questions."
    },
    {
      "id": "sliding_window_path",
      "name": "Sliding Window Mastery",
      "summary": "Step-by-step path to master sliding window pattern."
    },
    {
      "id": "two_pointers_path",
      "name": "Two Pointers Mastery",
      "summary": "Step-by-step path to master all two pointers sub-patterns."
    },
    {
      "id": "graph_bfs_path",
      "name": "BFS Mastery",
      "summary": "Step-by-step path to master BFS patterns."
    },
    {
      "id": "binary_search_path",
      "name": "Binary Search Mastery",
      "summary": "Step-by-step path to master binary search patterns."
    },
    {
      "id": "dp_path",
      "name": "Dynamic Programming Path",
      "summary": "Progressive path through DP patterns."
    },
    {
      "id": "tree_path",
      "name": "Tree Problems Path",
      "summary": "Comprehensive tree problem patterns."
    },
    {
      "id": "graph_path",
      "name": "Graph Problems Path",
      "summary": "Comprehensive graph problem patterns."
    }
  ]
}
```

## 📖 Pattern Documentation

### backtracking_exploration/intuition

# Backtracking: The Art of Reversible Exploration

> **Core Intuition**: You're exploring a maze of choices. You walk forward, leaving footprints. When you hit a dead end, you walk backward—erasing each footprint—until you find an untried path.

---

## Table of Contents

1. [The Feeling of Backtracking](#1-the-feeling-of-backtracking)
2. [The Three Forces: Choose, Explore, Unchoose](#2-the-three-forces-choose-explore-unchoose)
3. [The Invariant That Makes It Work](#3-the-invariant-that-makes-it-work)
4. [When the Pattern Appears](#4-when-the-pattern-appears)
5. [The Five Shapes of the Decision Tree](#5-the-five-shapes-of-the-decision-tree)
6. [Pruning: Seeing Dead Ends Early](#6-pruning-seeing-dead-ends-early)
7. [Deduplication: One Path to Each Treasure](#7-deduplication-one-path-to-each-treasure)
8. [From Intuition to Code](#8-from-intuition-to-code)
9. [Problem Gallery](#9-problem-gallery)
10. [Quick Reference Templates](#10-quick-reference-templates)

---

## 1. The Feeling of Backtracking

### What the Situation Feels Like

Imagine standing at the entrance of a cave with many branching tunnels. You need to find *all* chambers containing treasure. You have:
- A ball of thread (your *path*)
- Chalk to mark visited junctions (your *state*)

You unroll thread as you walk deeper. When a tunnel ends (dead end) or you find treasure (valid solution), you *rewind* the thread and *erase* your chalk marks—returning to the last junction to try a different tunnel.

**This is backtracking**: systematic exploration where every choice is reversible, every path is fully explored, and the explorer always returns to a clean state before trying alternatives.

### The Three Key Observations

1. **The world is a tree of choices**: From any point, you have several options. Each option leads to more options. This creates a decision tree.

2. **You must try everything**: Unlike optimization problems where you seek *one* best answer, here you want *all* valid configurations.

3. **Choices are reversible**: Unlike a one-way door, you can step back. But stepping back must *completely* undo what stepping forward did.

### What Changes Over Time

As you explore:
- Your **path grows** (you add choices)
- Your **path shrinks** (you remove choices when backtracking)
- **Branches get exhausted** (once fully explored, they're never revisited)

What remains constant:
- The **problem structure** (the cave's layout)
- The **invariant**: *at any moment, your state perfectly reflects your current path*

---

## 2. The Three Forces: Choose, Explore, Unchoose

Every backtracking algorithm is a rhythm of three actions:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   CHOOSE  →  Make a decision, modify state                  │
│      ↓                                                      │
│   EXPLORE →  Recurse into the world where that choice holds │
│      ↓                                                      │
│   UNCHOOSE → Undo the decision, restore state exactly       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Choose**: You pick one of the available options. You mark it as taken. Your path grows by one.

**Explore**: You commit to that choice and see what's possible in the world where it holds. You recurse.

**Unchoose**: When you return from exploration, you *must* undo the choice. The state returns to exactly what it was before. Your path shrinks by one.

### The Moment of Permanence

Here's the subtle truth: backtracking *feels* reversible, but something *is* permanent:

> Once you've explored a branch completely, that branch is **forever finished**.

You've extracted every treasure from that path. When you backtrack past a junction, you're not erasing the treasures you found—you're just erasing your footprints so you can walk a different path.

---

## 3. The Invariant That Makes It Work

### The State Consistency Invariant

> **At every moment, the current state reflects exactly the path taken to reach this point—nothing more, nothing less.**

If your path is `[A, B, C]`, then:
- `A` is marked as used
- `B` is marked as used
- `C` is marked as used
- Nothing else is marked

When you backtrack from `C`, your path becomes `[A, B]`, and `C` *must* be unmarked. If you forget to unmark `C`, you'll think it's still used when you try other paths, and you'll miss solutions.

### Why This Invariant Matters

The invariant guarantees:

1. **No missed solutions**: Every valid configuration is reachable through some path.
2. **No duplicates**: Each configuration is visited exactly once.
3. **Correct pruning**: When you prune, you're pruning based on true state.

**The most common bug**: Forgetting to undo state changes. The explorer walks backward but leaves chalk marks on the wall. Future paths see phantom constraints.

---

## 4. When the Pattern Appears

### Instant Recognition Signals

You're facing a backtracking problem when:

| Signal | What It Means |
|--------|---------------|
| "Find **all** valid configurations" | You need exhaustive enumeration, not just one |
| "Generate all permutations/subsets/combinations" | Classic decision tree over choices |
| "Partition such that every part satisfies..." | Try all cut positions |
| "Place pieces so no conflicts..." | Constraint satisfaction over positions |
| "Find all paths through a grid" | DFS with visited tracking |

### The Decision Tree Mental Model

Every backtracking problem has a hidden tree:

```
                     []                    ← Root: empty state
            ┌────────┼────────┐
          [A]       [B]       [C]          ← First choice: 3 options
        ┌──┴──┐   ┌──┴──┐   ┌──┴──┐
      [AB] [AC] [BA] [BC] [CA] [CB]        ← Second choice
        │    │    │    │    │    │
      ...  ...  ...  ...  ...  ...         ← Continue until complete
```

You're walking this tree. At each node, you:
1. Check if you've found treasure (base case)
2. If not, try each child (recursive case)
3. Return to parent when all children exhausted

---

## 5. The Five Shapes of the Decision Tree

Backtracking problems fall into five distinct shapes. Recognizing the shape tells you exactly what to track and how to recurse.

### Shape 1: Permutation — "Arrange All, Order Matters"

**The situation**: You have n distinct items. You want every possible ordering.

**The constraint**: Each item appears exactly once per arrangement.

**What to track**: Which items have been used (`used[]` array).

**The tree shape**: 
- Level 0: n choices (pick first item)
- Level 1: n-1 choices (pick from unused)
- Level k: n-k choices
- **Leaves**: n! arrangements

```
Who goes first?  → [1] or [2] or [3]
Who goes second? → [1,2] or [1,3] (not [1,1])
...
```

### Shape 2: Subset — "Include or Exclude, Order Doesn't Matter"

**The situation**: You have n items. You want every possible subset.

**The constraint**: Items appear in canonical order (no `{2,1}`, only `{1,2}`).

**What to track**: Start index (only consider items from here onward).

**The tree shape**:
- At each item: include it or skip it
- **Leaves**: 2^n subsets

```
Item 1: [include] → [1]    or [skip] → []
Item 2: [1,2] or [1] or [2] or []
...
```

**Key insight**: Using a start index automatically enforces canonical order. You never look backward.

### Shape 3: Target Sum — "Reach a Goal"

**The situation**: Find combinations that add up to a target.

**The constraint**: Sum must equal target exactly.

**What to track**: Remaining target (what's left to fill).

**The pruning**: If remaining goes negative, stop. If sorted and current element exceeds remaining, stop entirely.

```
Target: 7
Pick 2 → remaining: 5
Pick 3 → remaining: 2
Pick 2 → remaining: 0 ← FOUND!
```

### Shape 4: Constraint Satisfaction — "Place Without Conflict"

**The situation**: Place items (queens, numbers) so no two conflict.

**The constra
...(truncated)
### backtracking_exploration/templates

# Backtracking Exploration Patterns: Complete Reference

> **API Kernel**: `BacktrackingExploration`  
> **Core Mechanism**: Systematically explore all candidate solutions by building them incrementally, abandoning paths that violate constraints (pruning), and undoing choices to try alternatives.

This document presents the **canonical backtracking template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed algorithmic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Permutations (LeetCode 46)](#2-base-template-permutations-leetcode-46)
3. [Variation: Permutations with Duplicates (LeetCode 47)](#3-variation-permutations-with-duplicates-leetcode-47)
4. [Variation: Subsets (LeetCode 78)](#4-variation-subsets-leetcode-78)
5. [Variation: Subsets with Duplicates (LeetCode 90)](#5-variation-subsets-with-duplicates-leetcode-90)
6. [Variation: Combinations (LeetCode 77)](#6-variation-combinations-leetcode-77)
7. [Variation: Combination Sum (LeetCode 39)](#7-variation-combination-sum-leetcode-39)
8. [Variation: Combination Sum II (LeetCode 40)](#8-variation-combination-sum-ii-leetcode-40)
9. [Variation: Combination Sum III (LeetCode 216)](#9-variation-combination-sum-iii-leetcode-216)
10. [Variation: N-Queens (LeetCode 51/52)](#10-variation-n-queens-leetcode-5152)
11. [Variation: Palindrome Partitioning (LeetCode 131)](#11-variation-palindrome-partitioning-leetcode-131)
12. [Variation: Restore IP Addresses (LeetCode 93)](#12-variation-restore-ip-addresses-leetcode-93)
13. [Variation: Word Search (LeetCode 79)](#13-variation-word-search-leetcode-79)
14. [Deduplication Strategies](#14-deduplication-strategies)
15. [Pruning Techniques](#15-pruning-techniques)
16. [Pattern Comparison Table](#16-pattern-comparison-table)
17. [When to Use Backtracking](#17-when-to-use-backtracking)
18. [LeetCode Problem Mapping](#18-leetcode-problem-mapping)
19. [Template Quick Reference](#19-template-quick-reference)

---

## 1. Core Concepts

### 1.1 What is Backtracking?

Backtracking is a **systematic trial-and-error** approach that incrementally builds candidates to the solutions and abandons a candidate ("backtracks") as soon as it determines that the candidate cannot lead to a valid solution.

```
Decision Tree Visualization:

                    []
           ┌────────┼────────┐
          [1]      [2]      [3]
        ┌──┴──┐   ┌──┴──┐   ┌──┴──┐
      [1,2] [1,3] [2,1] [2,3] [3,1] [3,2]
        │     │     │     │     │     │
     [1,2,3] ... (continue building)
        ↓
    SOLUTION FOUND → collect and backtrack
```

### 1.2 The Three-Step Pattern: Choose → Explore → Unchoose

Every backtracking algorithm follows this fundamental pattern:

```python
def backtrack(state, choices):
    """
    Core backtracking template.
    
    1. BASE CASE: Check if current state is a complete solution
    2. RECURSIVE CASE: For each available choice:
       a) CHOOSE: Make a choice and update state
       b) EXPLORE: Recursively explore with updated state
       c) UNCHOOSE: Undo the choice (backtrack)
    """
    # BASE CASE: Is this a complete solution?
    if is_solution(state):
        collect_solution(state)
        return
    
    # RECURSIVE CASE: Try each choice
    for choice in get_available_choices(state, choices):
        # CHOOSE: Make this choice
        apply_choice(state, choice)
        
        # EXPLORE: Recurse with updated state
        backtrack(state, remaining_choices(choices, choice))
        
        # UNCHOOSE: Undo the choice (restore state)
        undo_choice(state, choice)
```

### 1.3 Key Invariants

| Invariant | Description |
|-----------|-------------|
| **State Consistency** | After backtracking, state must be exactly as before the choice was made |
| **Exhaustive Exploration** | Every valid solution must be reachable through some path |
| **Pruning Soundness** | Pruned branches must not contain any valid solutions |
| **No Duplicates** | Each unique solution must be generated exactly once |

### 1.4 Time Complexity Discussion

Backtracking algorithms typically have exponential or factorial complexity because they explore the entire solution space:

| Problem Type | Typical Complexity | Output Size |
|--------------|-------------------|-------------|
| Permutations | O(n! × n) | n! |
| Subsets | O(2^n × n) | 2^n |
| Combinations C(n,k) | O(C(n,k) × k) | C(n,k) |
| N-Queens | O(n!) | variable |

**Important**: The complexity is often **output-sensitive** — if there are many solutions, generating them all is inherently expensive.

### 1.5 Sub-Pattern Classification

| Sub-Pattern | Key Characteristic | Examples |
|-------------|-------------------|----------|
| **Permutation** | Used/visited tracking | LeetCode 46, 47 |
| **Subset/Combination** | Start-index canonicalization | LeetCode 78, 90, 77 |
| **Target Search** | Remaining/target pruning | LeetCode 39, 40, 216 |
| **Constraint Satisfaction** | Row-by-row with constraint sets | LeetCode 51, 52 |
| **String Partitioning** | Cut positions with validity | LeetCode 131, 93 |
| **Grid/Path Search** | Visited marking and undo | LeetCode 79 |

---

---

## 2. Base Template: Permutations (LeetCode 46)

> **Problem**: Given an array of distinct integers, return all possible permutations.  
> **Sub-Pattern**: Permutation Enumeration with used tracking.  
> **Key Insight**: At each position, try all unused elements.

### 2.1 Implementation

```python
def permute(nums: list[int]) -> list[list[int]]:
    """
    Generate all permutations of distinct integers.
    
    Algorithm:
    - Build permutation position by position
    - Track which elements have been used with a boolean array
    - At each position, try every unused element
    - When path length equals nums length, we have a complete permutation
    
    Time Complexity: O(n! × n)
        - n! permutations to generate
        - O(n) to copy each permutation
    
    Space Complexity: O(n)
        - Recursion depth is n
        - Used array is O(n)
        - Output space not counted
    
    Args:
        nums: Array of distinct integers
        
    Returns:
        All possible permutations
    """
    results: list[list[int]] = []
    n = len(nums)
    
    # State: Current permutation being built
    path: list[int] = []
    
    # Tracking: Which elements are already used in current path
    used: list[bool] = [False] * n
    
    def backtrack() -> None:
        # BASE CASE: Permutation is complete
        if len(path) == n:
            results.append(path[:])  # Append a copy
            return
        
        # RECURSIVE CASE: Try each unused element
        for i in range(n):
            if used[i]:
                continue  # Skip already used elements
            
            # CHOOSE: Add element to permutation
            path.append(nums[i])
            used[i] = True
            
            # EXPLORE: Recurse to fill next position
            backtrack()
            
            # UNCHOOSE: Remove element (backtrack)
            path.pop()
            used[i] = False
    
    backtrack()
    return results
```

### 2.2 Why This Works

The `used` array ensures each element appears exactly once in each permutation. The decision tree has:
- Level 0: n choices
- Level 1: n-1 choices  
- Level k: n-k choices
- Total leaves: n!

### 2.3 Trace Example

```
Input: [1, 2, 3]

backtrack(path=[], used=[F,F,F])
├─ CHOOSE 1 → backtrack(path=[1], used=[T,F,F])
│  ├─ CHOOSE 2 → backtrack(path=[1,2], used=[T,T,F])
│  │  └─ CHOOSE 3 → backtrack(path=[1,2,3], used=[T,T,T])
│  │                 → SOLUTION: [1,2,3]
│  └─ CHOOSE 3 → backtrack(path=[1,3], used=[T,F,T])
│     └─ CHOOSE 2 → backtrack(path=[1,3,2], used=[T,T,T])
│                    → SOLUTION: [1,3,2]
├─ CHOOSE 2 → ... → [2,1,3], [2,3,1]
└─ CHOOSE 3 → ... → [3,1,2], [3,2,1]

Output: [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

### 2.4 Common Pitfalls

| Pitfall | Pro
...(truncated)
### sliding_window/intuition

# Sliding Window: Pattern Intuition Guide

> *"The window is a moving lens of attention — it forgets the past to focus on what matters now."*

---

## The Situation That Calls for a Window

Imagine you're walking through a long corridor, and you can only see through a rectangular frame you carry with you. As you move forward, new things enter your view on the right, and old things disappear on the left.

**This is the essence of Sliding Window.**

You encounter this pattern whenever:
- You're scanning through a sequence (string, array, stream)
- You care about a **contiguous portion** of that sequence
- The answer depends on properties of that portion
- Those properties can be **updated incrementally** as the portion shifts

The key insight: *You don't need to remember everything — only what's currently in view.*

---

## The Two Forces at Play

Every sliding window algorithm is a dance between two opposing forces:

### The Explorer (Right Boundary) $R$
- Always moves forward, never backward
- Discovers new territory
- Adds new elements to consideration
- Asks: *"What happens if I include this?"*

### The Gatekeeper (Left Boundary) $L$
- Follows behind, cleaning up
- Removes elements that no longer serve the goal
- Enforces the rules of what's allowed
- Asks: *"Must I let go of something to stay valid?"*

The Explorer is eager and expansive. The Gatekeeper is disciplined and selective. Together, they maintain a **window of validity** that slides through the sequence.

---

## The Invariant: The Window's Promise

At every moment, the window makes a promise — an **invariant** that must always be true:

| Problem Type | The Promise |
|--------------|-------------|
| Longest unique substring | *"Every character in my view appears exactly once"* |
| At most K distinct | *"I contain no more than K different characters"* |
| Minimum covering substring | *"I contain everything required"* |
| Sum at least target | *"My total meets or exceeds the goal"* |

**This promise is sacred.** The moment it's broken, the Gatekeeper must act — shrinking the window until the promise is restored.

---

## The Irreversible Truth

Here's what makes sliding window work: **the Explorer never retreats.**

Once the right boundary passes an element, that element has been "seen." We may include it or exclude it from our current window, but we never go back to re-examine it as a potential starting point... unless the Gatekeeper releases it.

This one-directional march is what gives us O(n) time complexity. Each element enters the window at most once and exits at most once. No element is visited more than twice across the entire algorithm.

The irreversibility creates efficiency: *past decisions don't haunt us.*

---

## The Two Modes of Seeking

Depending on what you're optimizing, the dance changes:

### Mode 1: Maximize the Window
*"How large can my view become while staying valid?"*

```
Process:
1. Explorer advances, adding new element
2. If promise breaks → Gatekeeper advances until promise restored
3. Record the current window size (this is a candidate answer)
4. Repeat

The window EXPANDS freely, CONTRACTS only when forced.
```

**Mental image**: Stretching a rubber band until it's about to snap, then easing off just enough.

#### Flowchart: Maximize Window

┌─────────────────────────────────────────────────────────────────────────────┐
│  Example: Longest Substring Without Repeating Characters                    │
│  Sequence: [ a  b  c  a  b ]    Promise: "All chars unique"                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────┐                                                                    │
│  │START│                                                                    │
│  └──┬──┘                                                                    │
│     ▼                                                                       │
│  ┌──────────────────────┐                                                   │
│  │  R < length?         │───No───► ┌─────────┐                              │
│  └──────┬───────────────┘          │  DONE   │                              │
│     Yes │                          └─────────┘                              │
│         ▼                                                                   │
│  ╔══════════════════════════════╗                                           │
│  ║  🟢 R advances (Explorer)    ║◄───────────────────────────────┐          │
│  ║     Add element to state     ║                                │          │
│  ╚═══════════════╤══════════════╝                                │          │
│                  ▼                                               │          │
│        ┌─────────────────────┐                                   │          │
│        │ Promise broken?     │                                   │          │
│        │ (duplicate found?)  │                                   │          │
│        └────────┬────────────┘                                   │          │
│           Yes   │   No                                           │          │
│      ┌──────────┴──────────┐                                     │          │
│      ▼                     ▼                                     │          │
│  ┌─────────────────┐  ┌────────────────────────────────┐         │          │
│  │ While promise   │  │ ✅ Update answer:              │         │          │
│  │ is broken:      │  │    ans = max(ans, R-L+1)       │         │          │
│  │                 │  └──────────────┬─────────────────┘         │          │
│  │ ╔═════════════╗ │                 │                           │          │
│  │ ║ 🔴 L++      ║ │                 │                           │          │
│  │ ║ Remove L-1  ║ │                 │                           │          │
│  │ ╚═════════════╝ │                 │                           │          │
│  └────────┬────────┘                 │                           │          │
│           │                          │                           │          │
│           └──────────────────────────┘                           │          │
│                     │                                            │          │
│                     │                                            │          │
│                     │                                            │          │
│                     └────────────────────────────────────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


Visual Trace:
═══════════════════════════════════════════════════════════════════════════════

  Sequence:   a    b    c    a    b
             [0]  [1]  [2]  [3]  [4]

  Step 1:   🟢R→
            [ a ]                        max = 1
              L,R

  Step 2:         🟢R→
            [ a    b ]                   max = 2
              L        R

  Step 3:              🟢R→
            [ a    b    c ]              max = 3
              L              R

  Step 4:                   🟢R→
            [ a    b    c    a ]         ❌ 'a' duplicate!
              L                  R
                             │
                             ▼
            🔴L→ 🔴L
                 [ b    c    a ]         max = 3 (restored)
                   L             R

  Step 5:                        🟢R→
                 [ b    c    a    b ]    ❌ 'b' duplicate!
                   L                  R
                                  │
                                  ▼
                  🔴L→ 🔴L
                      [ c    a    b ]    max = 3 (final)
                        L             R

Legend: 🟢 = R expands (green)  🔴 = L contracts (red)  ❌ = promise broken
```

---

### Mode 2: Minimize the Window
*"How small can my view become while still being valid?"*

```
...(truncated)
### sliding_window/templates

# Sliding Window Patterns: Complete Reference

> **API Kernel**: `SubstringSlidingWindow`  
> **Core Mechanism**: Maintain a dynamic window `[left, right]` over a sequence while preserving an invariant.

This document presents the **canonical sliding window template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Unique Characters (LeetCode 3)](#2-base-template-unique-characters-leetcode-3)
3. [Variation: At Most K Distinct Characters (LeetCode 340/159)](#3-variation-at-most-k-distinct-characters-leetcode-340159)
4. [Variation: Minimum Window Substring (LeetCode 76)](#4-variation-minimum-window-substring-leetcode-76)
5. [Variation: Permutation in String (LeetCode 567)](#5-variation-permutation-in-string-leetcode-567)
6. [Variation: Find All Anagrams (LeetCode 438)](#6-variation-find-all-anagrams-leetcode-438)
7. [Variation: Minimum Size Subarray Sum (LeetCode 209)](#7-variation-minimum-size-subarray-sum-leetcode-209)
8. [Pattern Comparison Table](#8-pattern-comparison-table)
9. [When to Use Sliding Window](#9-when-to-use-sliding-window)
10. [Template Quick Reference](#10-template-quick-reference)

---

## 1. Core Concepts

### 1.1 The Sliding Window Invariant

Every sliding window algorithm maintains an **invariant** — a condition that must always be true for the current window `[left, right]`.

```
Window State:
┌─────────────────────────────────────────┐
│  ... [ left ─────── window ─────── right ] ...  │
│       └─────── invariant holds ───────┘         │
└─────────────────────────────────────────┘
```

### 1.2 Universal Template Structure

```python
def sliding_window_template(sequence):
    """
    Generic sliding window template.
    
    Key components:
    1. State: Data structure tracking window contents
    2. Invariant: Condition that must hold for valid window
    3. Expand: Always move right pointer forward
    4. Contract: Move left pointer to restore invariant
    5. Update: Record answer when window is valid
    """
    state = initialize_state()
    left = 0
    answer = initial_answer()
    
    for right, element in enumerate(sequence):
        # EXPAND: Add element at right to window state
        update_state_add(state, element)
        
        # CONTRACT: Shrink window until invariant is restored
        while invariant_violated(state):
            update_state_remove(state, sequence[left])
            left += 1
        
        # UPDATE: Record answer for current valid window
        answer = update_answer(answer, left, right)
    
    return answer
```

### 1.3 Two Window Strategies

| Strategy | When to Use | Example Problems |
|----------|-------------|------------------|
| **Maximize Window** | Find longest/largest valid window | LeetCode 3, 340, 424 |
| **Minimize Window** | Find shortest valid window | LeetCode 76, 209 |

---

## 2. Base Template: Unique Characters (LeetCode 3)

> **Problem**: Find the length of the longest substring without repeating characters.  
> **Invariant**: All characters in window `[left, right]` are unique.  
> **Role**: BASE TEMPLATE for `SubstringSlidingWindow` API Kernel.

### 2.1 Implementation

```python
def length_of_longest_substring(s: str) -> int:
    """
    Find the length of the longest substring without repeating characters.
    
    Algorithm:
    - Maintain a window where all characters are unique
    - Use a dictionary to track the last seen index of each character
    - When a duplicate is found, jump left pointer past the previous occurrence
    
    Time Complexity: O(n) - each character visited at most twice
    Space Complexity: O(min(n, σ)) - where σ is the alphabet size
    
    Args:
        s: Input string
        
    Returns:
        Length of the longest substring with all unique characters
    """
    # State: Map each character to its most recent index in the string
    last_seen_index: dict[str, int] = {}
    
    # Window boundaries
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # Check if character was seen within the current window
        # Key insight: We only care about occurrences at or after 'left'
        if char in last_seen_index and last_seen_index[char] >= left:
            # CONTRACT: Move left pointer past the previous occurrence
            # This single jump replaces the typical while-loop contraction
            left = last_seen_index[char] + 1
        
        # UPDATE: Record character's position for future duplicate detection
        last_seen_index[char] = right
        
        # UPDATE ANSWER: Current window [left, right] is valid
        # Window length = right - left + 1
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### 2.2 Why This Works

The key insight is the **jump optimization**: instead of incrementally shrinking the window with a while-loop, we directly jump `left` to `last_seen_index[char] + 1`.

This is valid because:
1. Any position before `last_seen_index[char]` would still include the duplicate
2. The position `last_seen_index[char] + 1` is the first position that excludes the duplicate
3. All characters between old `left` and new `left` are implicitly "removed" from consideration

### 2.3 Trace Example

```
Input: "abcabcbb"

Step | right | char | last_seen_index      | left | window    | max_length
-----|-------|------|----------------------|------|-----------|------------
  0  |   0   |  'a' | {a:0}                |  0   | "a"       | 1
  1  |   1   |  'b' | {a:0, b:1}           |  0   | "ab"      | 2
  2  |   2   |  'c' | {a:0, b:1, c:2}      |  0   | "abc"     | 3
  3  |   3   |  'a' | {a:3, b:1, c:2}      |  1   | "bca"     | 3  ← 'a' seen at 0, jump to 1
  4  |   4   |  'b' | {a:3, b:4, c:2}      |  2   | "cab"     | 3  ← 'b' seen at 1, jump to 2
  5  |   5   |  'c' | {a:3, b:4, c:5}      |  3   | "abc"     | 3  ← 'c' seen at 2, jump to 3
  6  |   6   |  'b' | {a:3, b:6, c:5}      |  5   | "cb"      | 3  ← 'b' seen at 4, jump to 5
  7  |   7   |  'b' | {a:3, b:7, c:5}      |  7   | "b"       | 3  ← 'b' seen at 6, jump to 7

Answer: 3 ("abc")
```

---

## 3. Variation: At Most K Distinct Characters (LeetCode 340/159)

> **Problem**: Find the length of the longest substring with at most K distinct characters.  
> **Invariant**: Number of distinct characters in window ≤ K.  
> **Delta from Base**: Replace "unique" check with "distinct count ≤ K".

### 3.1 Implementation

```python
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    """
    Find the length of the longest substring with at most K distinct characters.
    
    Algorithm:
    - Maintain a frequency map of characters in the current window
    - When distinct count exceeds K, shrink window from left until count ≤ K
    
    Time Complexity: O(n) - each character added and removed at most once
    Space Complexity: O(K) - at most K+1 entries in the frequency map
    
    Args:
        s: Input string
        k: Maximum number of distinct characters allowed
        
    Returns:
        Length of the longest valid substring
    """
    if k == 0:
        return 0
    
    # State: Frequency map tracking count of each character in window
    char_frequency: dict[str, int] = {}
    
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # EXPAND: Add character to window
        char_frequency[char] = char_frequency.get(char, 0) + 1
        
        # CONTRACT: Shrink window while we have more than K distinct characters
        # Unlike base template, we cannot jump — we must shrink incrementally
        # because removing one character might not restore the invariant
        while len(char_frequency) > k:
            left_char = s[left]
            char_frequency[left_char] -= 1
            
            # Remove character from map when its count reaches zero
            # This is
...(truncated)
### two_pointers/intuition

# Two Pointers: Pattern Intuition Guide

> *"Two points of attention, moving in coordinated rhythm — each step permanently narrows the world of possibilities."*

---

## The Situation That Calls for Two Pointers

Imagine you're standing at the edge of a long corridor with doors on both sides. You know the answer lies somewhere in this corridor, but checking every possible pair of doors would take forever.

Then you realize: you don't need to check everything. You can place one hand on the leftmost door and one on the rightmost door. Based on what you find, you know which hand to move. With each movement, doors behind you become irrelevant — forever excluded from consideration.

**This is the essence of Two Pointers.**

You encounter this pattern whenever:
- You're working with a **sorted** or **ordered** sequence
- You need to find **pairs, tuples, or regions** with certain properties
- The relationship between elements is **monotonic** — changing one pointer predictably affects the outcome
- You can **eliminate possibilities** based on the current state

The key insight: *You're not searching — you're eliminating. Every pointer movement permanently shrinks the problem.*

---

## The Invariant: The Space Between

Every two pointers algorithm maintains a **sacred region** — the space where the answer must exist.

```
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│   [excluded]  ←  left  ═══════ answer space ═══════  right → [excluded]   │
│                                                               │
│   Once excluded, never reconsidered.                          │
│   The region between pointers is the ONLY remaining hope.     │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

The invariant says: *If a valid answer exists, it lies within the current boundaries.* Moving a pointer is a declaration: "I've proven that nothing behind this pointer can be part of the answer."

**This is what makes two pointers work**: each movement is a proof of exclusion. You're not guessing — you're eliminating with certainty.

---

## The Irreversible Decision

Here's the crucial insight that separates two pointers from brute force:

> **Once a pointer moves, it never moves back.**

When you advance `left` from position 3 to position 4, you've permanently decided: "No valid answer involves position 3 as the left element." This decision is irreversible.

This one-directional march is what transforms O(n²) into O(n). Instead of checking all n² pairs, each of the 2n pointer positions is visited at most once.

The irreversibility creates efficiency: *you burn bridges as you cross them.*

---

## The Six Shapes of Two Pointers

Two pointer problems come in six distinct flavors. Recognizing the shape tells you exactly how to position and move the pointers.

---

### Shape 1: Opposite Approach — "Closing the Gap"

**The situation**: Two sentinels stand at opposite ends of a corridor. They walk toward each other, meeting somewhere in the middle.

**What it feels like**: You're squeezing from both ends. The search space shrinks from the outside in.

**The mental model**:
```
Initial:    L ═══════════════════════════════════ R
            ↓                                     ↓
Step 1:       L ═════════════════════════════ R
                                               ↓
Step 2:       L ═════════════════════════ R
              ↓
Step 3:         L ═══════════════════ R
                         ...
Final:                    L R  (or L crosses R)
```

**The decision rule**: Based on the current pair's property:
- If the combined value is **too small** → move `left` right (seek larger)
- If the combined value is **too large** → move `right` left (seek smaller)
- If it matches → record and continue (or return immediately)

**Why it works**: Sorted order creates monotonicity. Moving `left` right can only *increase* its contribution. Moving `right` left can only *decrease* its contribution. This gives you precise control.

**Classic problems**: Two Sum II, Container With Most Water, 3Sum

---

### Shape 2: Same Direction — "The Writer Following the Reader"

**The situation**: Two people walk the same corridor. One is a **Reader** who examines every door. The other is a **Writer** who only records the doors worth keeping.

**What it feels like**: You're filtering in-place. The Reader advances relentlessly; the Writer only moves when something passes the test.

**The mental model**:
```
Initial:    [a] [b] [c] [d] [e] [f]
             W   R
             ↓
             Reader examines 'a'
             'a' passes → Writer takes it, both advance

Step 2:     [a] [b] [c] [d] [e] [f]
                 W   R
                 ↓
                 Reader examines 'b'
                 'b' fails → only Reader advances

Step 3:     [a] [b] [c] [d] [e] [f]
                 W       R
                         ↓
                         Reader examines 'c'
                         'c' passes → Writer takes it, both advance

Final:      [a] [c] [x] [x] [x] [x]
                     ↑
                     New logical end (write position)
```

**The decision rule**: 
- Reader always advances
- Writer only advances when the current element should be kept
- Elements are copied from Reader position to Writer position

**Why it works**: The Writer index marks the boundary of "good" elements. Everything before Writer is the output; everything at or after is either unprocessed or discarded.

**The invariant**: `arr[0:write]` contains exactly the valid elements seen so far, in their original order.

**Classic problems**: Remove Duplicates, Remove Element, Move Zeroes

---

### Shape 3: Fast and Slow — "The Tortoise and the Hare"

**The situation**: Two runners on a track. One runs twice as fast as the other. If the track is a loop, the fast runner will eventually lap the slow one.

**What it feels like**: You're detecting a cycle by observing when speeds converge.

**The mental model**:
```
Linear track (no cycle):
    Slow: 1 step per turn
    Fast: 2 steps per turn

    Fast reaches the end first → No cycle


Circular track (cycle exists):
    ┌───────────────────────────┐
    │                           │
    ↓                           │
   [A] → [B] → [C] → [D] → [E] ─┘
    S          F

    Fast enters cycle first
    Slow eventually enters
    Fast "chases" slow from behind
    Gap closes by 1 each step
    They MUST meet inside the cycle
```

**The decision rule**:
- Slow moves 1 step
- Fast moves 2 steps
- If they meet → cycle exists
- If Fast reaches null → no cycle

**Why it works**: If there's a cycle, once both pointers are inside, the relative distance changes by 1 each iteration. Since the cycle length is finite, they must eventually collide.

**Finding the cycle start** (Phase 2):
- When they meet, reset Slow to head
- Move both at speed 1
- They meet again at the cycle start

This works because of the mathematical relationship between the meeting point and the cycle entry.

**Classic problems**: Linked List Cycle, Happy Number, Find Duplicate Number

---

### Shape 4: Partitioning — "The Bouncer Sorting the Queue"

**The situation**: A bouncer at a club entrance directs each person to one of three sections: left, middle, or right. Each person is examined once and placed in their final position.

**What it feels like**: You're sorting without sorting — classifying elements into regions in a single pass.

**The mental model** (Dutch National Flag):
```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│   [  < pivot  ]  [  = pivot  ]  [  unclassified  ]  [ > pivot ]│
│   └───────────┘  └───────────┘  └────────────────┘  └─────────┘│
│    0      low-1   low    mid-1   mid         high   high+1   n-1│
│                          ↑               
...(truncated)
### two_pointers/templates

# Two Pointers Patterns: Complete Reference

> **API Kernel**: `TwoPointersTraversal`  
> **Core Mechanism**: Maintain two index pointers traversing a sequence under invariant-preserving rules.

This document presents the **canonical two pointers template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Opposite Pointers (Two-End)](#2-opposite-pointers-two-end)
3. [Same-Direction Pointers (Writer Pattern)](#3-same-direction-pointers-writer-pattern)
4. [Fast–Slow Pointers (Cycle Detection)](#4-fastslow-pointers-cycle-detection)
5. [Partitioning / Dutch National Flag](#5-partitioning--dutch-national-flag)
6. [Dedup + Sorted Two-Pointer Enumeration](#6-dedup--sorted-two-pointer-enumeration)
7. [Merge Pattern](#7-merge-pattern)
8. [Pattern Comparison Table](#8-pattern-comparison-table)
9. [When to Use Two Pointers](#9-when-to-use-two-pointers)
10. [LeetCode Problem Mapping](#10-leetcode-problem-mapping)
11. [Template Quick Reference](#11-template-quick-reference)

---

## 1. Core Concepts

### 1.1 The Two Pointers Invariant

Every two pointers algorithm maintains an **invariant** — a relationship between the pointers and the problem state that must always be true.

```
Two Pointers State:
┌───────────────────────────────────────────────────────────────┐
│  [ ... left ─────── processed region ─────── right ... ]     │
│        └─────────── invariant holds ────────────┘            │
└───────────────────────────────────────────────────────────────┘
```

### 1.2 Two Pointers Family Overview

| Sub-Pattern | Pointer Movement | Primary Use Case |
|-------------|-----------------|------------------|
| **Opposite Pointers** | `left→ ... ←right` | Sorted arrays, palindromes, container problems |
| **Same-Direction (Writer)** | `write→ ... read→` | In-place array modification, deduplication |
| **Fast–Slow Pointers** | `slow→ ... fast→→` | Cycle detection, finding midpoints |
| **Partitioning** | Multiple pointers | Dutch flag, sorting by property |
| **Dedup Enumeration** | Nested with skip | Multi-sum problems (3Sum, 4Sum) |
| **Merge Pattern** | `i→ j→ ... write→` | Merging sorted sequences |

### 1.3 Universal Template Structure

```python
def two_pointers_template(sequence):
    """
    Generic two pointers template.
    
    Key components:
    1. Initialization: Set up pointer positions based on strategy
    2. Invariant: Condition that guides pointer movement
    3. Movement Rules: Deterministic pointer advancement
    4. Termination: Pointers meet or cross
    5. Update: Record answer when condition is satisfied
    """
    left, right = initialize_pointers(sequence)
    answer = initial_answer()
    
    while not termination_condition(left, right):
        # EVALUATE: Check current state against problem goal
        current_value = evaluate(sequence, left, right)
        
        # UPDATE ANSWER: Record if current state is optimal
        answer = update_answer(answer, current_value)
        
        # MOVE: Advance pointers based on invariant
        if should_move_left(current_value, target):
            left += 1
        else:
            right -= 1
    
    return answer
```

---

## 2. Opposite Pointers (Two-End)

> **Strategy**: Start pointers at opposite ends, move toward center.  
> **Invariant**: Valid solution space lies between `left` and `right`.  
> **Termination**: `left >= right` (pointers meet or cross).

### 2.1 When to Use

- Array is **sorted** and you need pairs with a target sum/property
- Problem involves **symmetric** checks (palindromes)
- Need to **maximize/minimize** a function of two positions (container area)

### 2.2 Why It Works

With sorted arrays, moving `left` right **increases** the left value, moving `right` left **decreases** the right value. This monotonicity enables efficient search without examining all O(n²) pairs.

### 2.3 Template

```python
def opposite_pointers_template(arr, target):
    """
    Opposite pointers for sorted array search.
    
    Time Complexity: O(n) - each pointer moves at most n times
    Space Complexity: O(1) - constant extra space
    """
    left, right = 0, len(arr) - 1
    answer = None
    
    while left < right:
        current = compute_value(arr, left, right)
        
        if current == target:
            # Found exact match
            return process_match(arr, left, right)
        elif current < target:
            # Need larger value: move left pointer right
            left += 1
        else:
            # Need smaller value: move right pointer left
            right -= 1
    
    return answer
```

### 2.4 Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(n) — each element visited at most once per pointer |
| Space | O(1) — only pointer indices stored |
| Prerequisite | Array must be sorted (or problem has monotonic property) |

### 2.5 LeetCode Problems

| ID | Problem | Key Insight |
|----|---------|-------------|
| 11 | Container With Most Water | Maximize `min(height[l], height[r]) × (r - l)` |
| 15 | 3Sum | Outer loop + inner opposite pointers |
| 16 | 3Sum Closest | Track closest sum instead of exact match |
| 42 | Trapping Rain Water | Two pointers from both ends, track max heights |
| 125 | Valid Palindrome | Compare characters moving inward |
| 167 | Two Sum II | Classic sorted array two-sum |
| 680 | Valid Palindrome II | Allow one character skip |

---

## 3. Same-Direction Pointers (Writer Pattern)

> **Strategy**: Both pointers move in the same direction; one "reads", one "writes".  
> **Invariant**: `arr[0:write]` contains the valid/processed elements.  
> **Termination**: Read pointer reaches end of array.

### 3.1 When to Use

- **In-place** array modification required
- Need to **remove** elements matching a condition
- Need to **deduplicate** while preserving order
- Memory constraints prohibit extra storage

### 3.2 Why It Works

The write pointer marks the boundary of "good" elements. The read pointer scans ahead, and only elements satisfying the condition are copied to the write position. Elements at `arr[write:]` are implicitly discarded.

### 3.3 Template

```python
def same_direction_template(arr, condition):
    """
    Same-direction (reader/writer) pattern for in-place modification.
    
    Time Complexity: O(n) - single pass through array
    Space Complexity: O(1) - in-place modification
    
    Invariant: arr[0:write_index] contains all valid elements seen so far.
    """
    write_index = 0
    
    for read_index in range(len(arr)):
        if condition(arr, read_index, write_index):
            arr[write_index] = arr[read_index]
            write_index += 1
    
    return write_index  # New logical length
```

### 3.4 Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(n) — single pass, each element examined once |
| Space | O(1) — in-place modification, no auxiliary storage |
| Property | Stable — preserves relative order of retained elements |

### 3.5 LeetCode Problems

| ID | Problem | Condition |
|----|---------|-----------|
| 26 | Remove Duplicates from Sorted Array | `arr[read] != arr[write - 1]` |
| 27 | Remove Element | `arr[read] != val` |
| 80 | Remove Duplicates II | `arr[read] != arr[write - 2]` |
| 283 | Move Zeroes | `arr[read] != 0`, then fill zeros |

---

## 4. Fast–Slow Pointers (Cycle Detection)

> **Strategy**: Two pointers at different speeds; fast moves 2×, slow moves 1×.  
> **Invariant**: If cycle exists, fast will eventually catch slow inside the cycle.  
> **Termination**: Fast reaches null (no cycle) or fast meets slow (cycle exists).

### 4.1 When to Use

- **Cycle detection** in linked lists or sequences
- Finding the **start of a cycle** (Floyd's algorithm phase 2)
- Finding **middle element** of a linked list
- **Happy number** and similar sequence convergence problems

### 4.2 Why It Works (Floyd's Cycle Dete
...(truncated)

## 🧩 Pattern Snippets

### backtracking_exploration

####@39-combination-sum.md

## Variation: Combination Sum (LeetCode 39)

> **Problem**: Find combinations that sum to target. Elements can be reused.  
> **Sub-Pattern**: Target search with element reuse.  
> **Key Insight**: Don't increment start_index when allowing reuse.

### Implementation

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """
    Find all combinations that sum to target. Each number can be used unlimited times.
    
    Algorithm:
    - Track remaining target (target - current sum)
    - When remaining = 0, found a valid combination
    - Allow reuse by NOT incrementing start_index when recursing
    - Prune when remaining < 0 (overshot target)
    
    Key Difference from Combinations:
    - Reuse allowed: recurse with same index i, not i+1
    - This means we can pick the same element multiple times
    
    Time Complexity: O(n^(t/m)) where t=target, m=min(candidates)
        - Branching factor up to n at each level
        - Depth up to t/m (using smallest element repeatedly)
    
    Space Complexity: O(t/m) for recursion depth
    
    Args:
        candidates: Array of distinct positive integers
        target: Target sum
        
    Returns:
        All unique combinations that sum to target
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    # Optional: Sort for consistent output order
    candidates.sort()
    
    def backtrack(start_index: int, remaining: int) -> None:
        # BASE CASE: Found valid combination
        if remaining == 0:
            results.append(path[:])
            return
        
        # PRUNING: Overshot target
        if remaining < 0:
            return
        
        for i in range(start_index, len(candidates)):
            # PRUNING: If current candidate exceeds remaining, 
            # all subsequent (if sorted) will too
            if candidates[i] > remaining:
                break
            
            path.append(candidates[i])
            
            # R
...(truncated)
####@40-combination-sum-ii.md

## Variation: Combination Sum II (LeetCode 40)

> **Problem**: Find combinations that sum to target. Each element used at most once. Input may have duplicates.  
> **Delta from Combination Sum**: No reuse + duplicate handling.  
> **Key Insight**: Sort + same-level skip for duplicates.

### Implementation

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    """
    Find all unique combinations that sum to target. Each number used at most once.
    Input may contain duplicates.
    
    Algorithm:
    - Sort to bring duplicates together
    - Use start_index to prevent reuse (i+1 when recursing)
    - Same-level deduplication: skip if current == previous at same level
    
    Deduplication Rule:
    - Skip candidates[i] if i > start_index AND candidates[i] == candidates[i-1]
    - This prevents generating duplicate combinations
    
    Time Complexity: O(2^n) worst case
    Space Complexity: O(n)
    
    Args:
        candidates: Array of positive integers (may have duplicates)
        target: Target sum
        
    Returns:
        All unique combinations summing to target
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    # CRITICAL: Sort for deduplication
    candidates.sort()
    
    def backtrack(start_index: int, remaining: int) -> None:
        if remaining == 0:
            results.append(path[:])
            return
        
        if remaining < 0:
            return
        
        for i in range(start_index, len(candidates)):
            # DEDUPLICATION: Skip same value at same level
            if i > start_index and candidates[i] == candidates[i - 1]:
                continue
            
            # PRUNING: Current exceeds remaining (sorted, so break)
            if candidates[i] > remaining:
                break
            
            path.append(candidates[i])
            
            # NO REUSE: Recurse with i+1
            backtrack(i + 1, remaining - candidates[i])
       
...(truncated)
####@46-permutations.md

## Base Template: Permutations (LeetCode 46)

> **Problem**: Given an array of distinct integers, return all possible permutations.  
> **Sub-Pattern**: Permutation Enumeration with used tracking.  
> **Key Insight**: At each position, try all unused elements.

### Implementation

```python
def permute(nums: list[int]) -> list[list[int]]:
    """
    Generate all permutations of distinct integers.
    
    Algorithm:
    - Build permutation position by position
    - Track which elements have been used with a boolean array
    - At each position, try every unused element
    - When path length equals nums length, we have a complete permutation
    
    Time Complexity: O(n! × n)
        - n! permutations to generate
        - O(n) to copy each permutation
    
    Space Complexity: O(n)
        - Recursion depth is n
        - Used array is O(n)
        - Output space not counted
    
    Args:
        nums: Array of distinct integers
        
    Returns:
        All possible permutations
    """
    results: list[list[int]] = []
    n = len(nums)
    
    # State: Current permutation being built
    path: list[int] = []
    
    # Tracking: Which elements are already used in current path
    used: list[bool] = [False] * n
    
    def backtrack() -> None:
        # BASE CASE: Permutation is complete
        if len(path) == n:
            results.append(path[:])  # Append a copy
            return
        
        # RECURSIVE CASE: Try each unused element
        for i in range(n):
            if used[i]:
                continue  # Skip already used elements
            
            # CHOOSE: Add element to permutation
            path.append(nums[i])
            used[i] = True
            
            # EXPLORE: Recurse to fill next position
            backtrack()
            
            # UNCHOOSE: Remove element (backtrack)
            path.pop()
            used[i] = False
    
    backtrack()
    return results
```

### Why This Works

The `used` array ensu
...(truncated)
####@47-permutations-duplicates.md

## Variation: Permutations with Duplicates (LeetCode 47)

> **Problem**: Given an array with duplicate integers, return all unique permutations.  
> **Delta from Base**: Add same-level deduplication after sorting.  
> **Key Insight**: Skip duplicate elements at the same tree level.

### Implementation

```python
def permute_unique(nums: list[int]) -> list[list[int]]:
    """
    Generate all unique permutations of integers that may contain duplicates.
    
    Algorithm:
    - Sort the array to bring duplicates together
    - Use same-level deduplication: skip a duplicate if its previous
      occurrence wasn't used (meaning we're at the same decision level)
    
    Deduplication Rule:
    - If nums[i] == nums[i-1] and used[i-1] == False, skip nums[i]
    - This ensures we only use the first occurrence of a duplicate
      at each level of the decision tree
    
    Time Complexity: O(n! × n) in worst case (all unique)
    Space Complexity: O(n)
    
    Args:
        nums: Array of integers (may contain duplicates)
        
    Returns:
        All unique permutations
    """
    results: list[list[int]] = []
    n = len(nums)
    
    # CRITICAL: Sort to bring duplicates together
    nums.sort()
    
    path: list[int] = []
    used: list[bool] = [False] * n
    
    def backtrack() -> None:
        if len(path) == n:
            results.append(path[:])
            return
        
        for i in range(n):
            if used[i]:
                continue
            
            # DEDUPLICATION: Skip duplicates at the same tree level
            # Condition: Current equals previous AND previous is unused
            # (unused previous means we're trying duplicate at same level)
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            
            path.append(nums[i])
            used[i] = True
            
            backtrack()
            
            path.pop()
            used[i] = False
    
    backtrack()
...(truncated)
####@51-n-queens.md

## Variation: N-Queens (LeetCode 51/52)

> **Problem**: Place n queens on an n×n board so no two queens attack each other.  
> **Sub-Pattern**: Constraint satisfaction with row-by-row placement.  
> **Key Insight**: Track columns and diagonals as constraint sets.

### Implementation

```python
def solve_n_queens(n: int) -> list[list[str]]:
    """
    Find all solutions to the N-Queens puzzle.
    
    Algorithm:
    - Place queens row by row (one queen per row guaranteed)
    - Track three constraints:
      1. Columns: No two queens in same column
      2. Main diagonals (↘): row - col is constant
      3. Anti-diagonals (↙): row + col is constant
    - Use hash sets for O(1) constraint checking
    
    Key Insight:
    - Row-by-row placement eliminates row conflicts by construction
    - Only need to check column and diagonal conflicts
    
    Time Complexity: O(n!)
        - At row 0: n choices
        - At row 1: at most n-1 choices
        - ... and so on
    
    Space Complexity: O(n) for constraint sets and recursion
    
    Args:
        n: Board size
        
    Returns:
        All valid board configurations as string arrays
    """
    results: list[list[str]] = []
    
    # State: queen_cols[row] = column where queen is placed
    queen_cols: list[int] = [-1] * n
    
    # Constraint sets for O(1) conflict checking
    used_cols: set[int] = set()
    used_diag_main: set[int] = set()   # row - col
    used_diag_anti: set[int] = set()   # row + col
    
    def backtrack(row: int) -> None:
        # BASE CASE: All queens placed
        if row == n:
            results.append(build_board(queen_cols, n))
            return
        
        # Try each column in current row
        for col in range(n):
            # Calculate diagonal identifiers
            diag_main = row - col
            diag_anti = row + col
            
            # CONSTRAINT CHECK (pruning)
            if col in used_cols:
                continue
            if diag_main in u
...(truncated)
####@77-combinations.md

## Variation: Combinations (LeetCode 77)

> **Problem**: Given n and k, return all combinations of k numbers from [1..n].  
> **Sub-Pattern**: Fixed-size subset enumeration.  
> **Delta from Subsets**: Only collect when path length equals k.

### Implementation

```python
def combine(n: int, k: int) -> list[list[int]]:
    """
    Generate all combinations of k numbers from range [1, n].
    
    Algorithm:
    - Similar to subsets, but only collect when path has exactly k elements
    - Use start_index to enforce canonical ordering
    - Add pruning: stop early if remaining elements can't fill path to k
    
    Pruning Optimization:
    - If we need (k - len(path)) more elements, we need at least that many
      elements remaining in [i, n]
    - Elements remaining = n - i + 1
    - Prune when: n - i + 1 < k - len(path)
    - Equivalently: stop loop when i > n - (k - len(path)) + 1
    
    Time Complexity: O(k × C(n,k))
    Space Complexity: O(k)
    
    Args:
        n: Range upper bound [1..n]
        k: Size of each combination
        
    Returns:
        All combinations of k numbers from [1..n]
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    def backtrack(start: int) -> None:
        # BASE CASE: Combination is complete
        if len(path) == k:
            results.append(path[:])
            return
        
        # PRUNING: Calculate upper bound for current loop
        # We need (k - len(path)) more elements
        # Available elements from start to n is (n - start + 1)
        # Stop when available < needed
        need = k - len(path)
        
        for i in range(start, n - need + 2):  # n - need + 1 + 1 for range
            path.append(i)
            backtrack(i + 1)
            path.pop()
    
    backtrack(1)
    return results
```

### Pruning Analysis

```
n=4, k=2

Without pruning:
start=1: try 1,2,3,4
  start=2: try 2,3,4
  start=3: try 3,4
  start=4: try 4     ← only 1 element left, need 1 more → works
  sta
...(truncated)
####@78-subsets.md

## Variation: Subsets (LeetCode 78)

> **Problem**: Given an array of distinct integers, return all possible subsets.  
> **Sub-Pattern**: Subset enumeration with start-index canonicalization.  
> **Key Insight**: Use a start index to avoid revisiting previous elements.

### Implementation

```python
def subsets(nums: list[int]) -> list[list[int]]:
    """
    Generate all subsets (power set) of distinct integers.
    
    Algorithm:
    - Each subset is a collection of elements with no ordering
    - To avoid duplicates like {1,2} and {2,1}, enforce canonical ordering
    - Use start_index to only consider elements at or after current position
    - Every intermediate path is a valid subset (collect at every node)
    
    Key Insight:
    - Unlike permutations, subsets don't need a "used" array
    - The start_index inherently prevents revisiting previous elements
    
    Time Complexity: O(n × 2^n)
        - 2^n subsets to generate
        - O(n) to copy each subset
    
    Space Complexity: O(n) for recursion depth
    
    Args:
        nums: Array of distinct integers
        
    Returns:
        All possible subsets
    """
    results: list[list[int]] = []
    n = len(nums)
    path: list[int] = []
    
    def backtrack(start_index: int) -> None:
        # COLLECT: Every path (including empty) is a valid subset
        results.append(path[:])
        
        # EXPLORE: Only consider elements from start_index onwards
        for i in range(start_index, n):
            # CHOOSE
            path.append(nums[i])
            
            # EXPLORE: Move start_index forward to enforce ordering
            backtrack(i + 1)
            
            # UNCHOOSE
            path.pop()
    
    backtrack(0)
    return results
```

### Why Start Index Works

```
Input: [1, 2, 3]

Decision tree with start_index:
[]                         ← start=0, collect []
├─ [1]                     ← start=1, collect [1]
│  ├─ [1,2]                ← start=2, collect [1,2]
│  │  
...(truncated)
####@79-word-search.md

## Variation: Word Search (LeetCode 79)

> **Problem**: Find if a word exists in a grid by traversing adjacent cells.  
> **Sub-Pattern**: Grid/Path DFS with visited marking.  
> **Key Insight**: Mark visited, explore neighbors, unmark on backtrack.

### Implementation

```python
def exist(board: list[list[str]], word: str) -> bool:
    """
    Check if word exists in grid by traversing adjacent cells.
    
    Algorithm:
    - Start DFS from each cell that matches word[0]
    - Mark current cell as visited (modify in-place or use set)
    - Try all 4 directions for next character
    - Unmark on backtrack
    
    Key Insight:
    - Each cell can be used at most once per path
    - In-place marking (temporary modification) is efficient
    
    Pruning:
    - Early return on mismatch
    - Can add frequency check: if board doesn't have enough of each char
    
    Time Complexity: O(m × n × 4^L) where L = len(word)
        - m×n starting positions
        - 4 choices at each step, depth L
    
    Space Complexity: O(L) for recursion depth
    
    Args:
        board: 2D character grid
        word: Target word to find
        
    Returns:
        True if word can be formed
    """
    if not board or not board[0]:
        return False
    
    rows, cols = len(board), len(board[0])
    word_len = len(word)
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def backtrack(row: int, col: int, index: int) -> bool:
        # BASE CASE: All characters matched
        if index == word_len:
            return True
        
        # BOUNDARY CHECK
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return False
        
        # CHARACTER CHECK
        if board[row][col] != word[index]:
            return False
        
        # MARK AS VISITED (in-place modification)
        original = board[row][col]
        board[row][col] = '#'  # Temporary marker
        
        # EXPLORE: Try all 4 dire
...(truncated)
####@90-subsets-duplicates.md

## Variation: Subsets with Duplicates (LeetCode 90)

> **Problem**: Given an array with duplicates, return all unique subsets.  
> **Delta from Subsets**: Sort + same-level deduplication.  
> **Key Insight**: Skip duplicate values at the same recursion level.

### Implementation

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    """
    Generate all unique subsets from integers that may contain duplicates.
    
    Algorithm:
    - Sort to bring duplicates together
    - Use same-level deduplication: skip if current equals previous
      in the same iteration loop
    
    Deduplication Condition:
    - Skip nums[i] if i > start_index AND nums[i] == nums[i-1]
    - This prevents choosing the same value twice at the same tree level
    
    Time Complexity: O(n × 2^n) worst case
    Space Complexity: O(n)
    
    Args:
        nums: Array of integers (may contain duplicates)
        
    Returns:
        All unique subsets
    """
    results: list[list[int]] = []
    n = len(nums)
    
    # CRITICAL: Sort to bring duplicates together
    nums.sort()
    
    path: list[int] = []
    
    def backtrack(start_index: int) -> None:
        results.append(path[:])
        
        for i in range(start_index, n):
            # DEDUPLICATION: Skip duplicates at same level
            # i > start_index ensures we're not skipping the first occurrence
            if i > start_index and nums[i] == nums[i - 1]:
                continue
            
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()
    
    backtrack(0)
    return results
```

### Deduplication Visualization

```
Input: [1, 2, 2] (sorted)

Without deduplication:
[]
├─ [1] → [1,2] → [1,2,2]
│      → [1,2]  ← choosing second 2
├─ [2] → [2,2]
└─ [2]  ← DUPLICATE of above!

With deduplication (skip if i > start and nums[i] == nums[i-1]):
[]
├─ [1] → [1,2] → [1,2,2]
│                        ↑ i=2, start=2, 2==2 but i==start, proceed
│      → [1,2]  skipped (i
...(truncated)
####@93-restore-ip.md

## Variation: Restore IP Addresses (LeetCode 93)

> **Problem**: Return all valid IP addresses that can be formed from a digit string.  
> **Sub-Pattern**: String segmentation with multi-constraint validity.  
> **Key Insight**: Fixed 4 segments, each 1-3 digits, value 0-255, no leading zeros.

### Implementation

```python
def restore_ip_addresses(s: str) -> list[str]:
    """
    Generate all valid IP addresses from a digit string.
    
    Constraints per segment:
    1. Length: 1-3 characters
    2. Value: 0-255
    3. No leading zeros (except "0" itself)
    
    Algorithm:
    - Exactly 4 segments required
    - Try 1, 2, or 3 characters for each segment
    - Validate each segment before proceeding
    
    Pruning:
    - Early termination if remaining chars can't form remaining segments
    - Min remaining = segments_left × 1
    - Max remaining = segments_left × 3
    
    Time Complexity: O(3^4 × n) = O(81 × n) = O(n)
        - At most 3 choices per segment, 4 segments
        - O(n) to validate/copy
    
    Space Complexity: O(4) = O(1) for path
    
    Args:
        s: String of digits
        
    Returns:
        All valid IP addresses
    """
    results: list[str] = []
    segments: list[str] = []
    n = len(s)
    
    def is_valid_segment(segment: str) -> bool:
        """Check if segment is a valid IP octet."""
        if not segment:
            return False
        if len(segment) > 1 and segment[0] == '0':
            return False  # No leading zeros
        if int(segment) > 255:
            return False
        return True
    
    def backtrack(start: int, segment_count: int) -> None:
        # PRUNING: Check remaining length bounds
        remaining = n - start
        remaining_segments = 4 - segment_count
        
        if remaining < remaining_segments:  # Too few chars
            return
        if remaining > remaining_segments * 3:  # Too many chars
            return
        
        # BASE CASE: 4 segments formed
        if seg
...(truncated)
####A31-palindrome-partitioning.md

## Variation: Palindrome Partitioning (LeetCode 131)

> **Problem**: Partition a string such that every substring is a palindrome.  
> **Sub-Pattern**: String segmentation with validity check.  
> **Key Insight**: Try all cut positions, validate each segment.

### Implementation

```python
def partition(s: str) -> list[list[str]]:
    """
    Partition string so every part is a palindrome.
    
    Algorithm:
    - Try cutting at each position from current start
    - Check if prefix is palindrome; if yes, recurse on suffix
    - When start reaches end of string, we have a valid partition
    
    Key Insight:
    - Each "choice" is where to cut the string
    - Only proceed if the cut-off prefix is a palindrome
    
    Optimization:
    - Precompute palindrome status with DP for O(1) checks
    - Without precompute: O(n) per check, O(n^3) total
    - With precompute: O(n^2) preprocessing, O(1) per check
    
    Time Complexity: O(n × 2^n) worst case
        - 2^(n-1) possible partitions (n-1 cut positions)
        - O(n) to copy each partition
    
    Space Complexity: O(n) for recursion
    
    Args:
        s: Input string
        
    Returns:
        All palindrome partitionings
    """
    results: list[list[str]] = []
    path: list[str] = []
    n = len(s)
    
    # Precompute: is_palindrome[i][j] = True if s[i:j+1] is palindrome
    is_palindrome = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j]:
                if j - i <= 2:
                    is_palindrome[i][j] = True
                else:
                    is_palindrome[i][j] = is_palindrome[i + 1][j - 1]
    
    def backtrack(start: int) -> None:
        # BASE CASE: Reached end of string
        if start == n:
            results.append(path[:])
            return
        
        # Try each end position for current segment
        for end in range(start, n):
            # VALIDITY CHECK: Only proceed if palindrome

...(truncated)
####B16-combination-sum-iii.md

## Variation: Combination Sum III (LeetCode 216)

> **Problem**: Find k numbers from [1-9] that sum to n. Each number used at most once.  
> **Delta from Combination Sum II**: Fixed count k + bounded range [1-9].  
> **Key Insight**: Dual constraint — both count and sum must be satisfied.

### Implementation

```python
def combination_sum3(k: int, n: int) -> list[list[int]]:
    """
    Find all combinations of k numbers from [1-9] that sum to n.
    
    Algorithm:
    - Fixed size k (must have exactly k numbers)
    - Fixed sum n (must sum to exactly n)
    - Range is [1-9], all distinct, no reuse
    
    Pruning Strategies:
    1. If current sum exceeds n, stop
    2. If path length exceeds k, stop
    3. If remaining numbers can't fill to k, stop
    
    Time Complexity: O(C(9,k) × k)
    Space Complexity: O(k)
    
    Args:
        k: Number of elements required
        n: Target sum
        
    Returns:
        All valid combinations
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    def backtrack(start: int, remaining: int) -> None:
        # BASE CASE: Have k numbers
        if len(path) == k:
            if remaining == 0:
                results.append(path[:])
            return
        
        # PRUNING: Not enough numbers left to fill path
        if 9 - start + 1 < k - len(path):
            return
        
        for i in range(start, 10):
            # PRUNING: Current number too large
            if i > remaining:
                break
            
            path.append(i)
            backtrack(i + 1, remaining - i)
            path.pop()
    
    backtrack(1, n)
    return results
```


#### _comparison.md

## Pattern Comparison Table

| Problem | Sub-Pattern | State | Dedup Strategy | Pruning |
|---------|-------------|-------|----------------|---------|
| Permutations (46) | Permutation | used[] | None (distinct) | None |
| Permutations II (47) | Permutation | used[] | Sort + level skip | Same-level |
| Subsets (78) | Subset | start_idx | Index ordering | None |
| Subsets II (90) | Subset | start_idx | Sort + level skip | Same-level |
| Combinations (77) | Combination | start_idx | Index ordering | Count bound |
| Combination Sum (39) | Target Search | start_idx | None (distinct) | Target bound |
| Combination Sum II (40) | Target Search | start_idx | Sort + level skip | Target + level |
| Combination Sum III (216) | Target Search | start_idx | None (1-9 distinct) | Count + target |
| N-Queens (51) | Constraint | constraint sets | Row-by-row | Constraints |
| Palindrome Part. (131) | Segmentation | start_idx | None | Validity check |
| IP Addresses (93) | Segmentation | start_idx, count | None | Length bounds |
| Word Search (79) | Grid Path | visited | Path uniqueness | Boundary + char |


#### _decision.md

## When to Use Backtracking

### Problem Indicators

✅ **Use backtracking when:**
- Need to enumerate all solutions (permutations, combinations, etc.)
- Decision tree structure (sequence of choices)
- Constraints can be checked incrementally
- Solution can be built piece by piece

❌ **Consider alternatives when:**
- Only need count (use DP with counting)
- Only need one solution (may use greedy or simple DFS)
- Optimization problem (consider DP or greedy)
- State space is too large even with pruning

### Decision Guide

```
Is the problem asking for ALL solutions?
├── Yes → Does solution have natural ordering/structure?
│         ├── Permutation → Use used[] array
│         ├── Subset/Combination → Use start_index
│         ├── Grid path → Use visited marking
│         └── Constraint satisfaction → Use constraint sets
└── No → Need single solution or count?
         ├── Single solution → Simple DFS may suffice
         └── Count → Consider DP
```


#### _deduplication.md

## Deduplication Strategies

### Strategy Comparison

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Sorting + Same-Level Skip** | Input has duplicates | Permutations II, Subsets II |
| **Start Index** | Subsets/Combinations (order doesn't matter) | Subsets, Combinations |
| **Used Array** | Permutations (all elements, order matters) | Permutations |
| **Canonical Ordering** | Implicit via index ordering | All subset-like problems |

### Same-Level Skip Pattern

```python
# Sort first, then skip duplicates at same level
nums.sort()

for i in range(start, n):
    # Skip if current equals previous at same tree level
    if i > start and nums[i] == nums[i - 1]:
        continue
    # ... process nums[i]
```

### Used Array Pattern

```python
# For permutations with duplicates
if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
    continue
# This ensures we use duplicates in order (leftmost first)
```


#### _header.md

# Backtracking Exploration Patterns: Complete Reference

> **API Kernel**: `BacktrackingExploration`  
> **Core Mechanism**: Systematically explore all candidate solutions by building them incrementally, abandoning paths that violate constraints (pruning), and undoing choices to try alternatives.

This document presents the **canonical backtracking template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed algorithmic explanations.

---

## Core Concepts

### What is Backtracking?

Backtracking is a **systematic trial-and-error** approach that incrementally builds candidates to the solutions and abandons a candidate ("backtracks") as soon as it determines that the candidate cannot lead to a valid solution.

```
Decision Tree Visualization:

                    []
           ┌────────┼────────┐
          [1]      [2]      [3]
        ┌──┴──┐   ┌──┴──┐   ┌──┴──┐
      [1,2] [1,3] [2,1] [2,3] [3,1] [3,2]
        │     │     │     │     │     │
     [1,2,3] ... (continue building)
        ↓
    SOLUTION FOUND → collect and backtrack
```

### The Three-Step Pattern: Choose → Explore → Unchoose

Every backtracking algorithm follows this fundamental pattern:

```python
def backtrack(state, choices):
    """
    Core backtracking template.
    
    1. BASE CASE: Check if current state is a complete solution
    2. RECURSIVE CASE: For each available choice:
       a) CHOOSE: Make a choice and update state
       b) EXPLORE: Recursively explore with updated state
       c) UNCHOOSE: Undo the choice (backtrack)
    """
    # BASE CASE: Is this a complete solution?
    if is_solution(state):
        collect_solution(state)
        return
    
    # RECURSIVE CASE: Try each choice
    for choice in get_available_choices(state, choices):
        # CHOOSE: Make this choice
        apply_choice(state, choice)
        
        # EXPLORE: Recurse with updated state
        backtrack(state, remaining_choices(choices, choice
...(truncated)
#### _mapping.md

## LeetCode Problem Mapping

| Sub-Pattern | Problems |
|-------------|----------|
| **Permutation Enumeration** | 46. Permutations, 47. Permutations II |
| **Subset/Combination** | 78. Subsets, 90. Subsets II, 77. Combinations |
| **Target Search** | 39. Combination Sum, 40. Combination Sum II, 216. Combination Sum III |
| **Constraint Satisfaction** | 51. N-Queens, 52. N-Queens II, 37. Sudoku Solver |
| **String Partitioning** | 131. Palindrome Partitioning, 93. Restore IP Addresses, 140. Word Break II |
| **Grid/Path Search** | 79. Word Search, 212. Word Search II |


#### _pruning.md

## Pruning Techniques

### Pruning Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Feasibility Bound** | Remaining elements can't satisfy constraints | Combinations: not enough elements left |
| **Target Bound** | Current path already exceeds target | Combination Sum: sum > target |
| **Constraint Propagation** | Future choices are forced/impossible | N-Queens: no valid columns left |
| **Sorted Early Exit** | If sorted, larger elements also fail | Combination Sum with sorted candidates |

### Pruning Patterns

```python
# 1. Not enough elements left (Combinations)
if remaining_elements < elements_needed:
    return

# 2. Exceeded target (Combination Sum)
if current_sum > target:
    return

# 3. Sorted early break (when candidates sorted)
if candidates[i] > remaining:
    break  # All subsequent are larger

# 4. Length/count bound
if len(path) > max_allowed:
    return
```


#### _templates.md

## Template Quick Reference

### Permutation Template

```python
def permute(nums):
    results = []
    used = [False] * len(nums)
    
    def backtrack(path):
        if len(path) == len(nums):
            results.append(path[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False
    
    backtrack([])
    return results
```

### Subset/Combination Template

```python
def subsets(nums):
    results = []
    
    def backtrack(start, path):
        results.append(path[:])  # Collect at every node
        
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)  # i+1 for no reuse
            path.pop()
    
    backtrack(0, [])
    return results
```

### Target Sum Template

```python
def combination_sum(candidates, target):
    results = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            results.append(path[:])
            return
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i for reuse
            path.pop()
    
    backtrack(0, [], target)
    return results
```

### Grid Search Template

```python
def grid_search(grid, word):
    rows, cols = len(grid), len(grid[0])
    
    def backtrack(r, c, index):
        if index == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if grid[r][c] != word[index]:
            return False
        
        temp = grid[r][c]
        grid[r][c] = '#'
        
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            if backtrack(r + dr, c + dc, index + 1):
                grid[r][c] = temp
                r
...(truncated)
### sliding_window

####@03-base.md

## Base Template: Unique Characters (LeetCode 3)

> **Problem**: Find the length of the longest substring without repeating characters.  
> **Invariant**: All characters in window `[left, right]` are unique.  
> **Role**: BASE TEMPLATE for `SubstringSlidingWindow` API Kernel.

### Implementation

```python
def length_of_longest_substring(s: str) -> int:
    """
    Find the length of the longest substring without repeating characters.
    
    Algorithm:
    - Maintain a window where all characters are unique
    - Use a dictionary to track the last seen index of each character
    - When a duplicate is found, jump left pointer past the previous occurrence
    
    Time Complexity: O(n) - each character visited at most twice
    Space Complexity: O(min(n, σ)) - where σ is the alphabet size
    
    Args:
        s: Input string
        
    Returns:
        Length of the longest substring with all unique characters
    """
    # State: Map each character to its most recent index in the string
    last_seen_index: dict[str, int] = {}
    
    # Window boundaries
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # Check if character was seen within the current window
        # Key insight: We only care about occurrences at or after 'left'
        if char in last_seen_index and last_seen_index[char] >= left:
            # CONTRACT: Move left pointer past the previous occurrence
            # This single jump replaces the typical while-loop contraction
            left = last_seen_index[char] + 1
        
        # UPDATE: Record character's position for future duplicate detection
        last_seen_index[char] = right
        
        # UPDATE ANSWER: Current window [left, right] is valid
        # Window length = right - left + 1
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Why This Works

The key insight is the **jump optimization**: instead of incrementally shrinking the window with a while
...(truncated)
####@76-min-window.md

## Variation: Minimum Window Substring (LeetCode 76)

> **Problem**: Find the minimum window in `s` that contains all characters of `t`.  
> **Invariant**: Window contains all required characters with sufficient frequency.  
> **Delta from Base**: Track "have vs need" frequencies; minimize instead of maximize.

### Implementation

```python
def min_window(s: str, t: str) -> str:
    """
    Find the minimum window substring of s that contains all characters of t.
    
    Algorithm:
    - Build a frequency map of required characters from t
    - Expand window to include required characters
    - Once all requirements are satisfied, contract to find minimum
    - Track the best (smallest) valid window found
    
    Time Complexity: O(|s| + |t|) - linear in both string lengths
    Space Complexity: O(|t|) - frequency maps bounded by t's unique characters
    
    Args:
        s: Source string to search in
        t: Target string containing required characters
        
    Returns:
        Minimum window substring, or "" if no valid window exists
    """
    if not t or not s:
        return ""
    
    # State: Required character frequencies (what we need)
    need_frequency: dict[str, int] = {}
    for char in t:
        need_frequency[char] = need_frequency.get(char, 0) + 1
    
    # State: Current window character frequencies (what we have)
    have_frequency: dict[str, int] = {}
    
    # Tracking: How many unique characters have met their required frequency
    chars_satisfied = 0
    chars_required = len(need_frequency)
    
    # Answer tracking
    min_length = float('inf')
    min_window_start = 0
    
    left = 0
    
    for right, char in enumerate(s):
        # EXPAND: Add character to window
        have_frequency[char] = have_frequency.get(char, 0) + 1
        
        # Check if this character just satisfied its requirement
        # Important: Only count when we EXACTLY meet the requirement
        # (not when we exceed it, to avoid double count
...(truncated)
####B09-min-subarray.md

## Variation: Minimum Size Subarray Sum (LeetCode 209)

> **Problem**: Find the minimal length subarray with sum ≥ target.  
> **Invariant**: Window sum ≥ target.  
> **Delta from Base**: Numeric sum instead of character tracking; minimize window.

### Implementation

```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    """
    Find the minimal length of a subarray whose sum is >= target.
    
    Algorithm:
    - Maintain a running sum of the current window
    - Expand window by adding elements
    - Once sum >= target, contract to find minimum length
    - Continue until all elements are processed
    
    Time Complexity: O(n) - each element added and removed at most once
    Space Complexity: O(1) - only tracking sum and pointers
    
    Args:
        target: Target sum to reach or exceed
        nums: Array of positive integers
        
    Returns:
        Minimum length of valid subarray, or 0 if none exists
    """
    n = len(nums)
    if n == 0:
        return 0
    
    # State: Running sum of current window
    window_sum = 0
    
    left = 0
    min_length = float('inf')
    
    for right, num in enumerate(nums):
        # EXPAND: Add element to window sum
        window_sum += num
        
        # CONTRACT: While sum satisfies target, try to minimize window
        # Note: We use 'while' not 'if' because multiple contractions may be possible
        while window_sum >= target:
            # UPDATE ANSWER: Current window is valid
            min_length = min(min_length, right - left + 1)
            
            # Remove leftmost element
            window_sum -= nums[left]
            left += 1
    
    return min_length if min_length != float('inf') else 0
```

### Key Difference: Numeric State

| Aspect | String Patterns | Numeric Sum |
|--------|-----------------|-------------|
| State | Frequency map | Single integer |
| Add element | `freq[c] += 1` | `sum += num` |
| Remove element | `freq[c] -= 1` | `sum -= num` |
| Chec
...(truncated)
####C40-k-distinct.md

## Variation: At Most K Distinct Characters (LeetCode 340/159)

> **Problem**: Find the length of the longest substring with at most K distinct characters.  
> **Invariant**: Number of distinct characters in window ≤ K.  
> **Delta from Base**: Replace "unique" check with "distinct count ≤ K".

### Implementation

```python
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    """
    Find the length of the longest substring with at most K distinct characters.
    
    Algorithm:
    - Maintain a frequency map of characters in the current window
    - When distinct count exceeds K, shrink window from left until count ≤ K
    
    Time Complexity: O(n) - each character added and removed at most once
    Space Complexity: O(K) - at most K+1 entries in the frequency map
    
    Args:
        s: Input string
        k: Maximum number of distinct characters allowed
        
    Returns:
        Length of the longest valid substring
    """
    if k == 0:
        return 0
    
    # State: Frequency map tracking count of each character in window
    char_frequency: dict[str, int] = {}
    
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # EXPAND: Add character to window
        char_frequency[char] = char_frequency.get(char, 0) + 1
        
        # CONTRACT: Shrink window while we have more than K distinct characters
        # Unlike base template, we cannot jump — we must shrink incrementally
        # because removing one character might not restore the invariant
        while len(char_frequency) > k:
            left_char = s[left]
            char_frequency[left_char] -= 1
            
            # Remove character from map when its count reaches zero
            # This is crucial for correct distinct count via len(char_frequency)
            if char_frequency[left_char] == 0:
                del char_frequency[left_char]
            
            left += 1
        
        # UPDATE ANSWER: Window [left, right] has
...(truncated)
####D38-anagrams.md

## Variation: Find All Anagrams (LeetCode 438)

> **Problem**: Find all start indices of `p`'s anagrams in `s`.  
> **Invariant**: Window has exact same character frequencies as `p`.  
> **Delta from Permutation Check**: Collect all valid positions instead of returning on first.

### Implementation

```python
def find_anagrams(s: str, p: str) -> list[int]:
    """
    Find all start indices of p's anagrams in s.
    
    This is an extension of the permutation check:
    instead of returning True on first match, collect all match positions.
    
    Time Complexity: O(|s| + |p|)
    Space Complexity: O(1) - bounded by alphabet size
    
    Args:
        s: Source string to search in
        p: Pattern string (looking for its anagrams)
        
    Returns:
        List of starting indices where anagrams of p begin in s
    """
    result: list[int] = []
    
    if len(p) > len(s):
        return result
    
    pattern_length = len(p)
    
    # State: Frequency maps
    pattern_frequency: dict[str, int] = {}
    window_frequency: dict[str, int] = {}
    
    for char in p:
        pattern_frequency[char] = pattern_frequency.get(char, 0) + 1
    
    chars_matched = 0
    chars_to_match = len(pattern_frequency)
    
    for right, char in enumerate(s):
        # EXPAND: Add character to window
        window_frequency[char] = window_frequency.get(char, 0) + 1
        
        if char in pattern_frequency:
            if window_frequency[char] == pattern_frequency[char]:
                chars_matched += 1
            elif window_frequency[char] == pattern_frequency[char] + 1:
                chars_matched -= 1
        
        # CONTRACT: Remove leftmost when window is full
        left = right - pattern_length + 1
        if left > 0:
            left_char = s[left - 1]
            
            if left_char in pattern_frequency:
                if window_frequency[left_char] == pattern_frequency[left_char]:
                    chars_matched -= 1
                el
...(truncated)
####E67-permutation.md

## Variation: Permutation in String (LeetCode 567)

> **Problem**: Check if `s2` contains any permutation of `s1`.  
> **Invariant**: Window has exact same character frequencies as `s1`.  
> **Delta from Base**: Fixed window size; exact frequency match.

### Implementation

```python
def check_inclusion(s1: str, s2: str) -> bool:
    """
    Check if s2 contains any permutation of s1.
    
    A permutation means same characters with same frequencies.
    We use a fixed-size sliding window of length len(s1).
    
    Algorithm:
    - Build frequency map of s1 (the pattern)
    - Slide a window of size len(s1) over s2
    - Check if window frequency matches pattern frequency
    
    Time Complexity: O(|s1| + |s2|) - build pattern + single pass over s2
    Space Complexity: O(1) - at most 26 lowercase letters
    
    Args:
        s1: Pattern string (looking for its permutation)
        s2: Source string to search in
        
    Returns:
        True if s2 contains a permutation of s1
    """
    if len(s1) > len(s2):
        return False
    
    pattern_length = len(s1)
    
    # State: Frequency maps
    pattern_frequency: dict[str, int] = {}
    window_frequency: dict[str, int] = {}
    
    # Build pattern frequency map
    for char in s1:
        pattern_frequency[char] = pattern_frequency.get(char, 0) + 1
    
    # Optimization: Track how many characters have matching frequencies
    chars_matched = 0
    chars_to_match = len(pattern_frequency)
    
    for right, char in enumerate(s2):
        # EXPAND: Add character to window
        window_frequency[char] = window_frequency.get(char, 0) + 1
        
        # Update match count for added character
        if char in pattern_frequency:
            if window_frequency[char] == pattern_frequency[char]:
                chars_matched += 1
            elif window_frequency[char] == pattern_frequency[char] + 1:
                # We just exceeded the required count
                chars_matched -= 1
        
  
...(truncated)
#### _comparison.md

## Pattern Comparison Table

| Problem | Invariant | State | Window Size | Goal |
|---------|-----------|-------|-------------|------|
| LeetCode 3 | All unique | `last_index` map | Variable | Maximize |
| LeetCode 340 | ≤K distinct | Frequency map | Variable | Maximize |
| LeetCode 76 | Contains all of t | Need/Have maps | Variable | Minimize |
| LeetCode 567 | Exact match | Frequency map | Fixed | Exists? |
| LeetCode 438 | Exact match | Frequency map | Fixed | All positions |
| LeetCode 209 | Sum ≥ target | Integer sum | Variable | Minimize |



#### _decision.md

## When to Use Sliding Window

### Problem Indicators

✅ **Use sliding window when:**
- Looking for contiguous subarray/substring
- Need to optimize (min/max) some property of the subarray
- Property can be maintained incrementally as window changes
- Adding/removing elements has O(1) state update

❌ **Don't use sliding window when:**
- Elements are not contiguous (use dynamic programming)
- Property requires global knowledge (use prefix sum + binary search)
- Window boundaries depend on non-local information

### Decision Flowchart

```
Is the answer a contiguous subarray/substring?
├── No → Use DP or other technique
└── Yes → Can you maintain window state incrementally?
          ├── No → Consider prefix sum or other technique
          └── Yes → Sliding Window!
                    ├── Fixed size window? → Use fixed window template
                    └── Variable size? → Maximize or Minimize?
                                        ├── Maximize → Expand always, contract on violation
                                        └── Minimize → Expand until valid, contract while valid
```



#### _header.md

# Sliding Window Patterns: Complete Reference

> **API Kernel**: `SubstringSlidingWindow`  
> **Core Mechanism**: Maintain a dynamic window `[left, right]` over a sequence while preserving an invariant.

This document presents the **canonical sliding window template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Core Concepts

### The Sliding Window Invariant

Every sliding window algorithm maintains an **invariant** — a condition that must always be true for the current window `[left, right]`.

```
Window State:
┌─────────────────────────────────────────┐
│  ... [ left ─────── window ─────── right ] ...  │
│       └─────── invariant holds ───────┘         │
└─────────────────────────────────────────┘
```

### Universal Template Structure

```python
def sliding_window_template(sequence):
    """
    Generic sliding window template.
    
    Key components:
    1. State: Data structure tracking window contents
    2. Invariant: Condition that must hold for valid window
    3. Expand: Always move right pointer forward
    4. Contract: Move left pointer to restore invariant
    5. Update: Record answer when window is valid
    """
    state = initialize_state()
    left = 0
    answer = initial_answer()
    
    for right, element in enumerate(sequence):
        # EXPAND: Add element at right to window state
        update_state_add(state, element)
        
        # CONTRACT: Shrink window until invariant is restored
        while invariant_violated(state):
            update_state_remove(state, sequence[left])
            left += 1
        
        # UPDATE: Record answer for current valid window
        answer = update_answer(answer, left, right)
    
    return answer
```

### Two Window Strategies

| Strategy | When to Use | Example Problems |
|----------|-------------|------------------|
| **Maximize Window** | Find longest/largest valid window | LeetCode 3, 340, 424 |
|
...(truncated)
#### _templates.md

## Template Quick Reference

### Maximize Window (Variable Size)

```python
def maximize_window(sequence):
    state = {}
    left = 0
    max_result = 0
    
    for right, elem in enumerate(sequence):
        # Expand
        add_to_state(state, elem)
        
        # Contract while invalid
        while not is_valid(state):
            remove_from_state(state, sequence[left])
            left += 1
        
        # Update answer
        max_result = max(max_result, right - left + 1)
    
    return max_result
```

### Minimize Window (Variable Size)

```python
def minimize_window(sequence):
    state = {}
    left = 0
    min_result = float('inf')
    
    for right, elem in enumerate(sequence):
        # Expand
        add_to_state(state, elem)
        
        # Contract while valid (to minimize)
        while is_valid(state):
            min_result = min(min_result, right - left + 1)
            remove_from_state(state, sequence[left])
            left += 1
    
    return min_result if min_result != float('inf') else 0
```

### Fixed Size Window

```python
def fixed_window(sequence, k):
    state = {}
    result = []
    
    for right, elem in enumerate(sequence):
        # Expand
        add_to_state(state, elem)
        
        # Contract when window exceeds k
        if right >= k:
            remove_from_state(state, sequence[right - k])
        
        # Check condition when window is exactly k
        if right >= k - 1 and is_valid(state):
            result.append(process(state))
    
    return result
```



### two_pointers

#### _comparison.md

## Pattern Comparison Table

| Pattern | Pointer Init | Movement | Termination | Time | Space | Key Use Case |
|---------|--------------|----------|-------------|------|-------|--------------|
| Opposite | `0, n-1` | Toward center | `left >= right` | O(n) | O(1) | Sorted array pairs |
| Same-Direction | `0, 0` | Both forward | `read >= n` | O(n) | O(1) | In-place modification |
| Fast–Slow | `head, head` | Slow 1×, Fast 2× | Meet or null | O(n) | O(1) | Cycle detection |
| Partitioning | `0, 0, n-1` | By element value | `mid > high` | O(n) | O(1) | Dutch flag, sorting |
| Dedup Enum | `i, i+1, n-1` | Nested + opposite | All `i` processed | O(n²) | O(1) | Multi-sum problems |
| Merge | `0, 0` | Advance smaller | Both exhausted | O(m+n) | O(1) | Merging sorted sequences |


#### _decision.md

## When to Use Two Pointers

### Problem Indicators

✅ **Use two pointers when:**
- Working with **sorted** arrays/lists
- Need to find **pairs or tuples** with a target property
- **In-place** modification is required
- Need to detect **cycles** in sequences
- **Merging** sorted sequences

❌ **Don't use two pointers when:**
- Array is unsorted and sorting is not allowed
- Need all pairs regardless of order (use hash map)
- Problem requires **non-contiguous** elements
- Relationship between elements is not monotonic

### Decision Flowchart

```
Is the array sorted (or can be sorted)?
├── No → Is it a linked list cycle problem?
│        ├── Yes → Fast–Slow Pointers
│        └── No → Consider hash map or other approach
└── Yes → What's the goal?
          ├── Find pair with target sum → Opposite Pointers
          ├── Remove/deduplicate in-place → Same-Direction
          ├── Partition by property → Dutch Flag
          ├── Find all unique tuples → Dedup Enumeration
          └── Merge two sequences → Merge Pattern
```


#### _header.md

# Two Pointers Patterns: Complete Reference

> **API Kernel**: `TwoPointersTraversal`  
> **Core Mechanism**: Maintain two index pointers traversing a sequence under invariant-preserving rules.

This document presents the **canonical two pointers template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Core Concepts

### The Two Pointers Invariant

Every two pointers algorithm maintains an **invariant** — a relationship between the pointers and the problem state that must always be true.

```
Two Pointers State:
┌───────────────────────────────────────────────────────────────┐
│  [ ... left ─────── processed region ─────── right ... ]     │
│        └─────────── invariant holds ────────────┘            │
└───────────────────────────────────────────────────────────────┘
```

### Two Pointers Family Overview

| Sub-Pattern | Pointer Movement | Primary Use Case |
|-------------|-----------------|------------------|
| **Opposite Pointers** | `left→ ... ←right` | Sorted arrays, palindromes, container problems |
| **Same-Direction (Writer)** | `write→ ... read→` | In-place array modification, deduplication |
| **Fast–Slow Pointers** | `slow→ ... fast→→` | Cycle detection, finding midpoints |
| **Partitioning** | Multiple pointers | Dutch flag, sorting by property |
| **Dedup Enumeration** | Nested with skip | Multi-sum problems (3Sum, 4Sum) |
| **Merge Pattern** | `i→ j→ ... write→` | Merging sorted sequences |

### Universal Template Structure

```python
def two_pointers_template(sequence):
    """
    Generic two pointers template.
    
    Key components:
    1. Initialization: Set up pointer positions based on strategy
    2. Invariant: Condition that guides pointer movement
    3. Movement Rules: Deterministic pointer advancement
    4. Termination: Pointers meet or cross
    5. Update: Record answer when condition is satisfied
    """
    left, right = initialize_pointers(se
...(truncated)
#### _mapping.md

## LeetCode Problem Mapping

### Opposite Pointers (Two-End)

| ID | Problem Name | Difficulty |
|----|--------------|------------|
| 11 | Container With Most Water | Medium |
| 15 | 3Sum | Medium |
| 16 | 3Sum Closest | Medium |
| 42 | Trapping Rain Water | Hard |
| 125 | Valid Palindrome | Easy |
| 167 | Two Sum II - Input Array Is Sorted | Medium |
| 680 | Valid Palindrome II | Easy |

### Same-Direction Pointers (Writer)

| ID | Problem Name | Difficulty |
|----|--------------|------------|
| 26 | Remove Duplicates from Sorted Array | Easy |
| 27 | Remove Element | Easy |
| 80 | Remove Duplicates from Sorted Array II | Medium |
| 283 | Move Zeroes | Easy |

### Fast–Slow Pointers

| ID | Problem Name | Difficulty |
|----|--------------|------------|
| 141 | Linked List Cycle | Easy |
| 142 | Linked List Cycle II | Medium |
| 202 | Happy Number | Easy |
| 287 | Find the Duplicate Number | Medium |
| 876 | Middle of the Linked List | Easy |

### Partitioning / Dutch Flag

| ID | Problem Name | Difficulty |
|----|--------------|------------|
| 75 | Sort Colors | Medium |
| 215 | Kth Largest Element in an Array | Medium |
| 905 | Sort Array By Parity | Easy |
| 922 | Sort Array By Parity II | Easy |

### Dedup + Sorted Enumeration

| ID | Problem Name | Difficulty |
|----|--------------|------------|
| 15 | 3Sum | Medium |
| 16 | 3Sum Closest | Medium |
| 18 | 4Sum | Medium |
| 167 | Two Sum II - Input Array Is Sorted | Medium |

### Merge Pattern

| ID | Problem Name | Difficulty |
|----|--------------|------------|
| 21 | Merge Two Sorted Lists | Easy |
| 88 | Merge Sorted Array | Easy |
| 977 | Squares of a Sorted Array | Easy |


#### _templates.md

## Template Quick Reference

### Opposite Pointers

```python
def opposite_pointers(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        # Process arr[left] and arr[right]
        if condition_move_left:
            left += 1
        else:
            right -= 1
```

### Same-Direction (Writer)

```python
def same_direction(arr):
    write = 0
    for read in range(len(arr)):
        if should_keep(arr[read]):
            arr[write] = arr[read]
            write += 1
    return write
```

### Fast–Slow

```python
def fast_slow(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True  # Cycle
    return False
```

### Dutch Flag

```python
def dutch_flag(arr):
    low, mid, high = 0, 0, len(arr) - 1
    while mid <= high:
        if arr[mid] < pivot:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] > pivot:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
        else:
            mid += 1
```

### Merge

```python
def merge(arr1, arr2):
    i, j, result = 0, 0, []
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    return result + arr1[i:] + arr2[j:]
```



## 🎯 Problem Data

Note: Use `LeetCode {leetcode_id}` format to reference problems. Links and titles will be added automatically by post-processing.

```json
[
  {
    "id": "0001",
    "leetcode_id": 1,
    "difficulty": "easy",
    "topics": [
      "array",
      "hash_table"
    ],
    "patterns": [
      "two_pointer_opposite"
    ],
    "api_kernels": [],
    "families": [
      "two_sum_variants"
    ],
    "data_structures": [
      "array",
      "hash_map"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0015",
      "0167",
      "0170",
      "0653"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "bloomberg",
      "adobe"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75",
      "grind_75",
      "leetcode_top_100"
    ]
  },
  {
    "id": "0002",
    "leetcode_id": 2,
    "difficulty": "medium",
    "topics": [
      "linked_list",
      "math",
      "recursion"
    ],
    "patterns": [],
    "api_kernels": [],
    "families": [
      "linked_list_manipulation",
      "math_number_theory"
    ],
    "data_structures": [
      "linked_list"
    ],
    "algorithms": [],
    "related_problems": [
      "0043",
      "0067",
      "0371",
      "0415",
      "0445"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg",
      "apple"
    ],
    "roadmaps": [
      "neetcode_150",
      "leetcode_top_100"
    ]
  },
  {
    "id": "0003",
    "leetcode_id": 3,
    "difficulty": "medium",
    "topics": [
      "string",
      "hash_table",
      "sliding_window"
    ],
    "patterns": [
      "sliding_window_unique"
    ],
    "api_kernels": [
      "SubstringSlidingWindow"
    ],
    "families": [
      "substring_window"
    ],
    "data_structures": [
      "string",
      "hash_map",
      "array"
    ],
    "algorithms": [
      "sliding_window",
      "two_pointers"
    ],
    "related_problems": [
      "0159",
      "0340",
      "0076",
      "0438",
      "0209",
      "0567",
      "0424"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "bloomberg",
      "adobe",
      "uber"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75",
      "grind_75",
      "leetcode_top_100",
      "sliding_window_path"
    ]
  },
  {
    "id": "0004",
    "leetcode_id": 4,
    "difficulty": "hard",
    "topics": [
      "array",
      "binary_search",
      "divide_and_conquer"
    ],
    "patterns": [
      "binary_search_on_answer",
      "merge_two_sorted"
    ],
    "api_kernels": [
      "BinarySearchBoundary",
      "KWayMerge"
    ],
    "families": [
      "merge_sorted",
      "binary_search_answer"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "binary_search",
      "two_pointers",
      "divide_and_conquer"
    ],
    "related_problems": [
      "0023",
      "0021",
      "0215"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "goldman_sachs"
    ],
    "roadmaps": [
      "neetcode_150",
      "leetcode_top_100"
    ]
  },
  {
    "id": "0011",
    "leetcode_id": 11,
    "difficulty": "medium",
    "topics": [
      "array",
      "two_pointers",
      "greedy"
    ],
    "patterns": [
      "two_pointer_opposite_maximize"
    ],
    "api_kernels": [
      "TwoPointersTraversal"
    ],
    "families": [
      "two_pointers_optimization"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers",
      "greedy"
    ],
    "related_problems": [
      "0042",
      "0125",
      "0167"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75",
      "leetcode_top_100"
    ]
  },
  {
    "id": "0015",
    "leetcode_id": 15,
    "difficulty": "medium",
    "topics": [
      "array",
      "two_pointers",
      "sorting"
    ],
    "patterns": [
      "two_pointer_three_sum"
    ],
    "api_kernels": [
      "TwoPointersTraversal"
    ],
    "families": [
      "multi_sum_enumeration"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers",
      "sorting"
    ],
    "related_problems": [
      "0001",
      "0016",
      "0018",
      "0167"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "bloomberg",
      "adobe",
      "uber"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75",
      "leetcode_top_100"
    ]
  },
  {
    "id": "0016",
    "leetcode_id": 16,
    "difficulty": "medium",
    "topics": [
      "array",
      "two_pointers",
      "sorting"
    ],
    "patterns": [
      "two_pointer_three_sum"
    ],
    "api_kernels": [
      "TwoPointersTraversal"
    ],
    "families": [
      "multi_sum_enumeration"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers",
      "sorting"
    ],
    "related_problems": [
      "0015",
      "0001"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0021",
    "leetcode_id": 21,
    "difficulty": "easy",
    "topics": [
      "linked_list",
      "recursion"
    ],
    "patterns": [
      "merge_two_sorted_lists"
    ],
    "api_kernels": [
      "MergeSortedSequences"
    ],
    "families": [
      "sequence_merge",
      "linked_list_manipulation"
    ],
    "data_structures": [
      "linked_list"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0023",
      "0088",
      "0977"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "bloomberg",
      "adobe",
      "uber"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75",
      "grind_75",
      "leetcode_top_100"
    ]
  },
  {
    "id": "0023",
    "leetcode_id": 23,
    "difficulty": "hard",
    "topics": [
      "linked_list",
      "divide_and_conquer",
      "heap"
    ],
    "patterns": [
      "merge_k_sorted_heap",
      "merge_k_sorted_divide"
    ],
    "api_kernels": [
      "KWayMerge"
    ],
    "families": [
      "merge_sorted",
      "linked_list_manipulation",
      "heap_priority"
    ],
    "data_structures": [
      "linked_list",
      "min_heap"
    ],
    "algorithms": [
      "divide_and_conquer"
    ],
    "related_problems": [
      "0021",
      "0004",
      "0378",
      "0264"
    ],
    "companies": [
      "google",
      "meta",
      "amazon",
      "microsoft",
      "uber",
      "bloomberg",
      "apple"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75",
      "leetcode_top_100"
    ]
  },
  {
    "id": "0025",
    "leetcode_id": 25,
    "difficulty": "hard",
    "topics": [
      "linked_list",
      "recursion"
    ],
    "patterns": [
      "linked_list_k_group_reversal"
    ],
    "api_kernels": [
      "LinkedListInPlaceReversal"
    ],
    "families": [
      "linked_list_manipulation"
    ],
    "data_structures": [
      "linked_list"
    ],
    "algorithms": [
      "recursion"
    ],
    "related_problems": [
      "0024",
      "0206",
      "0092"
    ],
    "companies": [
      "google",
      "meta",
      "amazon",
      "microsoft",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0026",
    "leetcode_id": 26,
    "difficulty": "easy",
    "topics": [
      "array",
      "two_pointers"
    ],
    "patterns": [
      "two_pointer_writer_dedup"
    ],
    "api_kernels": [
      "TwoPointersTraversal"
    ],
    "families": [
      "in_place_array_modification"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0027",
      "0080",
      "0283"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg",
      "adobe"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75",
      "grind_75"
    ]
  },
  {
    "id": "0027",
    "leetcode_id": 27,
    "difficulty": "easy",
    "topics": [
      "array",
      "two_pointers"
    ],
    "patterns": [
      "two_pointer_writer_remove"
    ],
    "api_kernels": [
      "TwoPointersTraversal"
    ],
    "families": [
      "in_place_array_modification"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0026",
      "0283"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "grind_75"
    ]
  },
  {
    "id": "0039",
    "leetcode_id": 39,
    "difficulty": "medium",
    "topics": [
      "array",
      "backtracking"
    ],
    "patterns": [
      "backtracking_combination"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "backtracking"
    ],
    "related_problems": [
      "0040",
      "0077",
      "0216",
      "0078"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "uber",
      "airbnb"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75"
    ]
  },
  {
    "id": "0040",
    "leetcode_id": 40,
    "difficulty": "medium",
    "topics": [
      "array",
      "backtracking"
    ],
    "patterns": [
      "backtracking_combination"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "backtracking"
    ],
    "related_problems": [
      "0039",
      "0090",
      "0047",
      "0216"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0046",
    "leetcode_id": 46,
    "difficulty": "medium",
    "topics": [
      "array",
      "backtracking"
    ],
    "patterns": [
      "backtracking_permutation"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "backtracking"
    ],
    "related_problems": [
      "0047",
      "0078",
      "0077"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "uber"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0047",
    "leetcode_id": 47,
    "difficulty": "medium",
    "topics": [
      "array",
      "backtracking"
    ],
    "patterns": [
      "backtracking_permutation"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "backtracking"
    ],
    "related_problems": [
      "0046",
      "0040",
      "0090"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft"
    ],
    "roadmaps": []
  },
  {
    "id": "0051",
    "leetcode_id": 51,
    "difficulty": "hard",
    "topics": [
      "array",
      "backtracking"
    ],
    "patterns": [
      "backtracking_n_queens"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "array",
      "hash_set"
    ],
    "algorithms": [
      "backtracking"
    ],
    "related_problems": [
      "0052",
      "0037"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0052",
    "leetcode_id": 52,
    "difficulty": "hard",
    "topics": [
      "backtracking"
    ],
    "patterns": [
      "backtracking_n_queens"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "array",
      "hash_set"
    ],
    "algorithms": [
      "backtracking"
    ],
    "related_problems": [
      "0051"
    ],
    "companies": [
      "google",
      "amazon",
      "meta"
    ],
    "roadmaps": []
  },
  {
    "id": "0075",
    "leetcode_id": 75,
    "difficulty": "medium",
    "topics": [
      "array",
      "two_pointers",
      "sorting"
    ],
    "patterns": [
      "dutch_flag_partition"
    ],
    "api_kernels": [
      "TwoPointerPartition"
    ],
    "families": [
      "array_partition"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0905",
      "0922"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75"
    ]
  },
  {
    "id": "0076",
    "leetcode_id": 76,
    "difficulty": "hard",
    "topics": [
      "string",
      "hash_table",
      "sliding_window"
    ],
    "patterns": [
      "sliding_window_freq_cover"
    ],
    "api_kernels": [
      "SubstringSlidingWindow"
    ],
    "families": [
      "substring_window"
    ],
    "data_structures": [
      "string",
      "hash_map"
    ],
    "algorithms": [
      "sliding_window",
      "two_pointers"
    ],
    "related_problems": [
      "0003",
      "0030",
      "0209",
      "0438",
      "0567"
    ],
    "companies": [
      "google",
      "meta",
      "amazon",
      "microsoft",
      "apple",
      "bloomberg",
      "uber",
      "linkedin"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75",
      "grind_75",
      "sliding_window_path"
    ]
  },
  {
    "id": "0077",
    "leetcode_id": 77,
    "difficulty": "medium",
    "topics": [
      "backtracking"
    ],
    "patterns": [
      "backtracking_combination"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "backtracking"
    ],
    "related_problems": [
      "0078",
      "0039",
      "0216"
    ],
    "companies": [
      "google",
      "amazon",
      "meta"
    ],
    "roadmaps": []
  },
  {
    "id": "0078",
    "leetcode_id": 78,
    "difficulty": "medium",
    "topics": [
      "array",
      "backtracking",
      "bit_manipulation"
    ],
    "patterns": [
      "backtracking_subset"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "backtracking"
    ],
    "related_problems": [
      "0090",
      "0077",
      "0046"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "uber"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0079",
    "leetcode_id": 79,
    "difficulty": "medium",
    "topics": [
      "array",
      "backtracking",
      "matrix"
    ],
    "patterns": [
      "backtracking_grid_path"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "grid",
      "array"
    ],
    "algorithms": [
      "backtracking",
      "dfs"
    ],
    "related_problems": [
      "0212",
      "0130",
      "0200"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "uber",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75"
    ]
  },
  {
    "id": "0080",
    "leetcode_id": 80,
    "difficulty": "medium",
    "topics": [
      "array",
      "two_pointers"
    ],
    "patterns": [
      "two_pointer_writer_dedup"
    ],
    "api_kernels": [
      "TwoPointersTraversal"
    ],
    "families": [
      "in_place_array_modification"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0026",
      "0027"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0088",
    "leetcode_id": 88,
    "difficulty": "easy",
    "topics": [
      "array",
      "two_pointers",
      "sorting"
    ],
    "patterns": [
      "merge_two_sorted_arrays"
    ],
    "api_kernels": [
      "MergeSortedSequences"
    ],
    "families": [
      "sequence_merge"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0021",
      "0977"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "grind_75"
    ]
  },
  {
    "id": "0090",
    "leetcode_id": 90,
    "difficulty": "medium",
    "topics": [
      "array",
      "backtracking",
      "bit_manipulation"
    ],
    "patterns": [
      "backtracking_subset"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "backtracking"
    ],
    "related_problems": [
      "0078",
      "0040",
      "0047"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0093",
    "leetcode_id": 93,
    "difficulty": "medium",
    "topics": [
      "string",
      "backtracking"
    ],
    "patterns": [
      "backtracking_string_segmentation"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "string",
      "array"
    ],
    "algorithms": [
      "backtracking"
    ],
    "related_problems": [
      "0131",
      "0093"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft"
    ],
    "roadmaps": []
  },
  {
    "id": "0125",
    "leetcode_id": 125,
    "difficulty": "easy",
    "topics": [
      "two_pointers",
      "string"
    ],
    "patterns": [
      "two_pointer_opposite_palindrome"
    ],
    "api_kernels": [
      "TwoPointersTraversal"
    ],
    "families": [
      "palindrome_validation"
    ],
    "data_structures": [
      "string"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0680",
      "0005",
      "0125"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75",
      "grind_75"
    ]
  },
  {
    "id": "0131",
    "leetcode_id": 131,
    "difficulty": "medium",
    "topics": [
      "string",
      "dynamic_programming",
      "backtracking"
    ],
    "patterns": [
      "backtracking_string_segmentation"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "string",
      "array"
    ],
    "algorithms": [
      "backtracking",
      "dynamic_programming"
    ],
    "related_problems": [
      "0093",
      "0005"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0141",
    "leetcode_id": 141,
    "difficulty": "easy",
    "topics": [
      "linked_list",
      "two_pointers",
      "hash_table"
    ],
    "patterns": [
      "fast_slow_cycle_detect"
    ],
    "api_kernels": [
      "FastSlowPointers"
    ],
    "families": [
      "linked_list_cycle"
    ],
    "data_structures": [
      "linked_list"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0142",
      "0202"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75",
      "grind_75"
    ]
  },
  {
    "id": "0142",
    "leetcode_id": 142,
    "difficulty": "medium",
    "topics": [
      "linked_list",
      "two_pointers",
      "hash_table"
    ],
    "patterns": [
      "fast_slow_cycle_start"
    ],
    "api_kernels": [
      "FastSlowPointers"
    ],
    "families": [
      "linked_list_cycle"
    ],
    "data_structures": [
      "linked_list"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0141",
      "0202"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75"
    ]
  },
  {
    "id": "0202",
    "leetcode_id": 202,
    "difficulty": "easy",
    "topics": [
      "hash_table",
      "math",
      "two_pointers"
    ],
    "patterns": [
      "fast_slow_implicit_cycle"
    ],
    "api_kernels": [
      "FastSlowPointers"
    ],
    "families": [
      "linked_list_cycle"
    ],
    "data_structures": [],
    "algorithms": [
      "two_pointers",
      "math"
    ],
    "related_problems": [
      "0141",
      "0142"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "uber"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0209",
    "leetcode_id": 209,
    "difficulty": "medium",
    "topics": [
      "array",
      "binary_search",
      "sliding_window",
      "prefix_sum"
    ],
    "patterns": [
      "sliding_window_cost_bounded"
    ],
    "api_kernels": [
      "SubstringSlidingWindow"
    ],
    "families": [
      "substring_window"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "sliding_window",
      "two_pointers"
    ],
    "related_problems": [
      "0003",
      "0076",
      "0325",
      "0718",
      "0862"
    ],
    "companies": [
      "google",
      "meta",
      "amazon",
      "microsoft",
      "apple",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "sliding_window_path"
    ]
  },
  {
    "id": "0215",
    "leetcode_id": 215,
    "difficulty": "medium",
    "topics": [
      "array",
      "divide_and_conquer",
      "sorting",
      "heap",
      "quickselect"
    ],
    "patterns": [
      "quickselect_partition",
      "heap_kth_element"
    ],
    "api_kernels": [
      "TwoPointerPartition",
      "HeapTopK"
    ],
    "families": [
      "heap_priority",
      "array_partition"
    ],
    "data_structures": [
      "array",
      "min_heap"
    ],
    "algorithms": [
      "quickselect",
      "heap"
    ],
    "related_problems": [
      "0347",
      "0378"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "bloomberg",
      "uber"
    ],
    "roadmaps": [
      "neetcode_150",
      "blind_75"
    ]
  },
  {
    "id": "0216",
    "leetcode_id": 216,
    "difficulty": "medium",
    "topics": [
      "array",
      "backtracking"
    ],
    "patterns": [
      "backtracking_combination"
    ],
    "api_kernels": [
      "BacktrackingExploration"
    ],
    "families": [
      "backtracking_combinatorial"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "backtracking"
    ],
    "related_problems": [
      "0039",
      "0040",
      "0077"
    ],
    "companies": [
      "google",
      "amazon"
    ],
    "roadmaps": []
  },
  {
    "id": "0283",
    "leetcode_id": 283,
    "difficulty": "easy",
    "topics": [
      "array",
      "two_pointers"
    ],
    "patterns": [
      "two_pointer_writer_compact"
    ],
    "api_kernels": [
      "TwoPointersTraversal"
    ],
    "families": [
      "in_place_array_modification"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0027",
      "0026"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg",
      "adobe"
    ],
    "roadmaps": [
      "neetcode_150",
      "grind_75"
    ]
  },
  {
    "id": "0340",
    "leetcode_id": 340,
    "difficulty": "medium",
    "topics": [
      "string",
      "hash_table",
      "sliding_window"
    ],
    "patterns": [
      "sliding_window_at_most_k_distinct"
    ],
    "api_kernels": [
      "SubstringSlidingWindow"
    ],
    "families": [
      "substring_window"
    ],
    "data_structures": [
      "string",
      "hash_map"
    ],
    "algorithms": [
      "sliding_window",
      "two_pointers"
    ],
    "related_problems": [
      "0003",
      "0159",
      "0076",
      "0424",
      "0904"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple"
    ],
    "roadmaps": [
      "sliding_window_path"
    ]
  },
  {
    "id": "0438",
    "leetcode_id": 438,
    "difficulty": "medium",
    "topics": [
      "string",
      "hash_table",
      "sliding_window"
    ],
    "patterns": [
      "sliding_window_freq_cover"
    ],
    "api_kernels": [
      "SubstringSlidingWindow"
    ],
    "families": [
      "substring_window"
    ],
    "data_structures": [
      "string",
      "hash_map"
    ],
    "algorithms": [
      "sliding_window"
    ],
    "related_problems": [
      "0003",
      "0076",
      "0242",
      "0567"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "sliding_window_path"
    ]
  },
  {
    "id": "0567",
    "leetcode_id": 567,
    "difficulty": "medium",
    "topics": [
      "string",
      "hash_table",
      "two_pointers",
      "sliding_window"
    ],
    "patterns": [
      "sliding_window_freq_cover"
    ],
    "api_kernels": [
      "SubstringSlidingWindow"
    ],
    "families": [
      "substring_window"
    ],
    "data_structures": [
      "string",
      "hash_map"
    ],
    "algorithms": [
      "sliding_window"
    ],
    "related_problems": [
      "0003",
      "0076",
      "0242",
      "0438"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "apple",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "sliding_window_path"
    ]
  },
  {
    "id": "0680",
    "leetcode_id": 680,
    "difficulty": "easy",
    "topics": [
      "two_pointers",
      "string",
      "greedy"
    ],
    "patterns": [
      "two_pointer_opposite_palindrome"
    ],
    "api_kernels": [
      "TwoPointersTraversal"
    ],
    "families": [
      "palindrome_validation"
    ],
    "data_structures": [
      "string"
    ],
    "algorithms": [
      "two_pointers",
      "greedy"
    ],
    "related_problems": [
      "0125"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0876",
    "leetcode_id": 876,
    "difficulty": "easy",
    "topics": [
      "linked_list",
      "two_pointers"
    ],
    "patterns": [
      "fast_slow_midpoint"
    ],
    "api_kernels": [
      "FastSlowPointers"
    ],
    "families": [
      "linked_list_manipulation"
    ],
    "data_structures": [
      "linked_list"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0141",
      "0142"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "grind_75"
    ]
  },
  {
    "id": "0905",
    "leetcode_id": 905,
    "difficulty": "easy",
    "topics": [
      "array",
      "two_pointers",
      "sorting"
    ],
    "patterns": [
      "two_way_partition"
    ],
    "api_kernels": [
      "TwoPointerPartition"
    ],
    "families": [
      "array_partition"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0075",
      "0922"
    ],
    "companies": [
      "google",
      "amazon",
      "microsoft"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0922",
    "leetcode_id": 922,
    "difficulty": "easy",
    "topics": [
      "array",
      "two_pointers"
    ],
    "patterns": [
      "two_way_partition"
    ],
    "api_kernels": [
      "TwoPointerPartition"
    ],
    "families": [
      "array_partition"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0905",
      "0075"
    ],
    "companies": [
      "google",
      "amazon"
    ],
    "roadmaps": [
      "neetcode_150"
    ]
  },
  {
    "id": "0977",
    "leetcode_id": 977,
    "difficulty": "easy",
    "topics": [
      "array",
      "two_pointers",
      "sorting"
    ],
    "patterns": [
      "merge_sorted_from_ends"
    ],
    "api_kernels": [
      "MergeSortedSequences"
    ],
    "families": [
      "sequence_merge"
    ],
    "data_structures": [
      "array"
    ],
    "algorithms": [
      "two_pointers"
    ],
    "related_problems": [
      "0021",
      "0088"
    ],
    "companies": [
      "google",
      "amazon",
      "meta",
      "microsoft",
      "bloomberg"
    ],
    "roadmaps": [
      "neetcode_150",
      "grind_75"
    ]
  },
  {
    "id": "0994",
    "leetcode_id": 994,
    "difficulty": "medium",
    "topics": [
      "array",
      "breadth_first_search",
      "matrix"
    ],
    "patterns": [
      "grid_bfs_propagation"
    ],
    "api_kernels": [
      "GridBFSMultiSource"
    ],
    "families": [
      "graph_wavefront",
      "matrix_traversal"
    ],
    "data_structures": [
      "grid",
      "queue"
    ],
    "algorithms": [
      "bfs"
    ],
    "related_problems": [
      "0286",
      "0542",
      "0127",
      "0752",
      "1091",
      "0200"
    ],
    "companies": [
      "amazon",
      "microsoft",
      "google",
      "meta"
    ],
    "roadmaps": [
      "neetcode_150",
      "graph_bfs_path"
    ]
  }
]
```

## 🎨 Generation Instructions

Goal: free_form

**Style**: Balance beauty and practicality, suitable for most learners.

**Additional Instructions**: "
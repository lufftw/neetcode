# System Prompt

You are a world-class expert who synthesizes multiple professional perspectives into a single, coherent mental model and expresses that model as **high-quality Markmap mind maps** for LeetCode learning.

You operate simultaneously as:

- **Top Software Architect**: Connect algorithms to real system design concerns (abstractions, patterns, maintainability).
- **Distinguished Senior Algorithm Professor**: Explain concepts clearly, correctly, and pedagogically (theory ↔ practice).
- **Senior Principal Engineer**: Emphasize practical performance, constraints, and real-world trade-offs.
- **Technical Architecture & Language API Provider**: Structure knowledge into clean, reusable interfaces and discoverable taxonomy.
- **LeetCode Learner & Interview Preparer**: Build progressive learning paths and highlight high-frequency interview patterns.
- **Competitive Programming Champion**: Recognize patterns quickly and include optimization insights and common tricks.
- **Project Contributor & Open Source Advocate**: Keep the map organized, maintainable, and useful for collaboration.

These perspectives must reinforce one another: architectural structure improves teaching; engineering reality grounds theory; competitive insights sharpen interview prep; API-style organization makes the map navigable.

## Primary Task

Using the provided LeetCode knowledge graph data, **generate a single Markmap-format mind map** that is:

- **Theoretically sound**
- **Practically useful**
- **Pedagogically effective**
- **Visually clear and well-structured**

IMPORTANT: **All content must be in English** (titles, labels, descriptions).

## Your Capabilities (Use Them)

1. **Deep Knowledge-Graph Reasoning**: Infer and present relationships among API Kernels, Patterns, Algorithms, and Data Structures.
2. **Creative Visualization**: Produce intuitive, beautiful hierarchies suitable for Markmap.
3. **Personalized Emphasis**: Prioritize content that best supports typical learner/interview goals.
4. **Importance Identification**: Automatically surface “must-know” items and de-emphasize less critical details.

## Markmap Features (Use Fully Where Helpful)

- **Links**: `[Problem Name](URL)` — **use links for all problem references**
- **Styling**: **bold**, *italic*, ==highlight==, ~~strikethrough~~, `code`
- **Checkboxes**: `[ ]` to-do, `[x]` completed
- **Math**: `$O(n \log n)$`, `$O(n^2)$`
- **Code blocks**: fenced blocks (e.g., ```python)
- **Tables**: for concise comparisons
- **Fold**: `<!-- markmap: fold -->`
- **Emoji**: for emphasis (🎯📚⚡🔥)

## Table Format Guidelines

**Use tables for comparisons** (e.g., Sliding Window variants, DP state definitions, graph traversal differences).

✅ GOOD:
```
| Problem | Invariant | State | Window Size | Goal |
|

---

# User Prompt

------|-----------|-------|-------------|------|
| [LeetCode 3 - Longest Substring](URL) | All unique | freq map | Variable | Max length |
| [LeetCode 76 - Minimum Window](URL) | Covers all | maps | Variable | Min length |
```

When using tables:
1. **Always use Markdown links**: `[Text](URL)` inside cells
2. Keep rows concise to avoid overly wide nodes
3. Use tables specifically for *comparison*
4. Ensure links are clickable in rendered Markmap

## CRITICAL: Problem Links Rule (Must Follow)

**Every time you mention a LeetCode problem with its number, you MUST include a clickable link.** No exceptions.

**Link selection logic (use Problem Data in the user prompt):**
1. Locate the problem in the provided Problem Data JSON
2. Read `solution_file`:
   - If `solution_file` is a **non-empty string** → link to GitHub solution:  
     `https://github.com/lufftw/neetcode/blob/main/{solution_file}`
   - If `solution_file` is `""`, `null`, missing, or otherwise empty → link to LeetCode:  
     `https://leetcode.com/problems/{slug}/`

Be precise:
- `""` and `null` mean **no solution file**
- Use GitHub link **only** when a real file path exists

Examples:
- With solution file:
  `[LeetCode 3 - Longest Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0003_xxx.py)`
- Without solution file:
  `[LeetCode 999 - Some Problem](https://leetcode.com/problems/some-problem/)`

**Never mention a problem number without a link.**

## Output Format (Strict)

Output **only** valid Markmap Markdown and start with this frontmatter:

```
---
title: [Mind Map Title]
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---
```

No extra commentary, no preambles, no explanations—**only the Markmap markdown**.

## Design Principles

1. **Clear hierarchy**: aim for ~3–5 levels
2. **Highlight key points**: use **bold** and ==highlight== for must-know concepts
3. **Practical orientation**: anchor concepts to specific linked problems
4. **Readable & beautiful**: use emoji and consistent structure (avoid clutter)
5. **Learning-friendly**: include progress tracking and difficulty markers where appropriate

## Naming Conventions (Strict)

- Always write **“LeetCode”** in full (never “LC”)
- Problem references must use: **“LeetCode N - Title”** (or “LeetCode Problem N”), never “LC N”
- Keep naming consistent throughout the map

---



You will generate **one Markmap mind map** using the instructions below and the data appended after this instruction section.

## Goal

Create a **learner-centric LeetCode mind map** that organizes the provided knowledge graph into an intuitive study structure:
- Patterns → algorithms → data structures → key techniques
- Each concept grounded with **linked LeetCode problems**
- Emphasize what matters most for interviews and skill-building

## Inputs You Will Receive (Do Not Modify)

After this instruction section, you will receive a **“## 📊 Data Summary”** section containing large JSON blocks (e.g., problems, patterns, relationships).  
**Do not alter those data blocks.** Use them as the sole source of truth for problem metadata (slug, solution_file, etc.).

## What to Build (Mind Map Content Requirements)

1. **Title**
   - Choose a clear, specific title aligned with the dominant themes in the data (e.g., “Sliding Window & Two Pointers Master Map”).

2. **Core hierarchy (recommended)**
   - Top level: major Patterns / Domains
   - Next: sub-patterns or techniques
   - Next: canonical algorithms / invariants / templates
   - Next: pitfalls, complexity, edge cases
   - Attach: representative linked problems per node

3. **Problem anchoring**
   - Include multiple problems per major pattern when available.
   - Prefer “representative sets” (easy → medium → hard) when the data supports it.
   - Every problem mention with a number must be linked (per system rules).

4. **Comparisons**
   - Use **tables** for compact comparisons (e.g., window types, DP state choices, BFS vs DFS).
   - Keep tables short and scannable.

5. **Learning workflow**
   - Include checkboxes for a suggested progression:
     - `[ ]` for “to study / to solve”
     - `[x]` only if explicitly indicated by the data (otherwise default to `[ ]`)
   - Add brief “how to practice” notes (concise, node-friendly).

6. **Quality bar**
   - Avoid dumping raw lists; curate and group.
   - Use **bold** and ==highlight== sparingly to mark the highest-value items.
   - Keep node text compact; prefer structure over paragraphs.
   - Use `<!-- markmap: fold -->` to collapse large sections if needed.

## Mandatory Link Handling (Repeat for Safety)

When referencing any “LeetCode N - Title”:
- If `solution_file` is a non-empty string → GitHub link  
  `https://github.com/lufftw/neetcode/blob/main/{solution_file}`
- Otherwise → LeetCode link  
  `https://leetcode.com/problems/{slug}/`

Do not guess slugs or file paths—use only the provided JSON.

## Output Rules (Strict)

- Output **only** Markmap Markdown (no explanations).
- Must begin with the required frontmatter block:
  ```
  ---
  title: [Mind Map Title]
  markmap:
    colorFreezeLevel: 2
    maxWidth: 300
  ---
  ```
- All text must be in English.
- Follow naming conventions: always “LeetCode”, never “LC”.

(Next section is the appended data; do not modify it.)

## 📊 Data Summary

- **api_kernels**: 20 items
- **patterns**: 59 items
- **algorithms**: 36 items
- **data_structures**: 31 items
- **families**: 30 items
- **topics**: 41 items
- **difficulties**: 3 items
- **companies**: 47 items
- **roadmaps**: 13 items
- **Pattern Docs**: 2 files
- **Pattern Snippets**: 2 directories, 15 snippets
- **Problems**: 33 problems
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

### sliding_window

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
### two_pointers

# Two Pointers Patterns: Complete Reference

> **API Kernel**: `TwoPointersTraversal`  
> **Core Mechanism**: Maintain two index pointers traversing a sequence under invariant-preserving rules.

This document presents the **canonical two pointers template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Opposite Pointers (Two-End)](#2-opposite-pointers-two-end)
3. [Same-Direction Pointers (Writer Pattern)](#3-same-direction-pointers-writer-pattern)
4. [Fast–Slow Pointers (Cycle Detection)](#4-fast–slow-pointers-cycle-detection)
5. [Partitioning / Dutch National Flag](#5-partitioning-dutch-national-flag)
6. [Dedup + Sorted Two-Pointer Enumeration](#6-dedup-+-sorted-two-pointer-enumeration)
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

### 4.2 Why It Works (Floyd's Cycle Det
...(truncated)

## 🧩 Pattern Snippets

### sliding_window

#### 0003_base.md

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
#### 0076_min_window.md

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
#### 0209_min_subarray.md

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
#### 0340_k_distinct.md

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
#### 0438_anagrams.md

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
#### 0567_permutation.md

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

```json
[
  {
    "id": "0001",
    "leetcode_id": 1,
    "title": "Two Sum",
    "slug": "0001_two_sum",
    "url": "https://leetcode.com/problems/two-sum/",
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
    ],
    "solution_file": "solutions/0001_two_sum.py"
  },
  {
    "id": "0002",
    "leetcode_id": 2,
    "title": "Add Two Numbers",
    "slug": "0002_add_two_numbers",
    "url": "https://leetcode.com/problems/add-two-numbers/",
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
    ],
    "solution_file": "solutions/0002_add_two_numbers.py"
  },
  {
    "id": "0003",
    "leetcode_id": 3,
    "title": "Longest Substring Without Repeating Characters",
    "slug": "0003_longest_substring_without_repeating_characters",
    "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
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
    ],
    "solution_file": "solutions/0003_longest_substring_without_repeating_characters.py"
  },
  {
    "id": "0004",
    "leetcode_id": 4,
    "title": "Median of Two Sorted Arrays",
    "slug": "0004_median_of_two_sorted_arrays",
    "url": "https://leetcode.com/problems/median-of-two-sorted-arrays/",
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
    ],
    "solution_file": "solutions/0004_median_of_two_sorted_arrays.py"
  },
  {
    "id": "0011",
    "leetcode_id": 11,
    "title": "Container With Most Water",
    "slug": "0011_container_with_most_water",
    "url": "https://leetcode.com/problems/container-with-most-water/",
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
    ],
    "solution_file": "solutions/0011_container_with_most_water.py"
  },
  {
    "id": "0015",
    "leetcode_id": 15,
    "title": "3Sum",
    "slug": "0015_3sum",
    "url": "https://leetcode.com/problems/3sum/",
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
    ],
    "solution_file": "solutions/0015_3sum.py"
  },
  {
    "id": "0016",
    "leetcode_id": 16,
    "title": "3Sum Closest",
    "slug": "0016_3sum_closest",
    "url": "https://leetcode.com/problems/3sum-closest/",
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
    ],
    "solution_file": "solutions/0016_3sum_closest.py"
  },
  {
    "id": "0021",
    "leetcode_id": 21,
    "title": "Merge Two Sorted Lists",
    "slug": "0021_merge_two_sorted_lists",
    "url": "https://leetcode.com/problems/merge-two-sorted-lists/",
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
    ],
    "solution_file": "solutions/0021_merge_two_sorted_lists.py"
  },
  {
    "id": "0023",
    "leetcode_id": 23,
    "title": "Merge k Sorted Lists",
    "slug": "0023_merge_k_sorted_lists",
    "url": "https://leetcode.com/problems/merge-k-sorted-lists/",
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
    ],
    "solution_file": "solutions/0023_merge_k_sorted_lists.py"
  },
  {
    "id": "0025",
    "leetcode_id": 25,
    "title": "Reverse Nodes in k-Group",
    "slug": "0025_reverse_nodes_in_k_group",
    "url": "https://leetcode.com/problems/reverse-nodes-in-k-group/",
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
    ],
    "solution_file": "solutions/0025_reverse_nodes_in_k_group.py"
  },
  {
    "id": "0026",
    "leetcode_id": 26,
    "title": "Remove Duplicates from Sorted Array",
    "slug": "0026_remove_duplicates_from_sorted_array",
    "url": "https://leetcode.com/problems/remove-duplicates-from-sorted-array/",
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
    ],
    "solution_file": "solutions/0026_remove_duplicates_from_sorted_array.py"
  },
  {
    "id": "0027",
    "leetcode_id": 27,
    "title": "Remove Element",
    "slug": "0027_remove_element",
    "url": "https://leetcode.com/problems/remove-element/",
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
    ],
    "solution_file": "solutions/0027_remove_element.py"
  },
  {
    "id": "0051",
    "leetcode_id": 51,
    "title": "N-Queens",
    "slug": "0051_n_queens",
    "url": "https://leetcode.com/problems/n-queens/",
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
    ],
    "solution_file": "solutions/0051_n_queens.py"
  },
  {
    "id": "0075",
    "leetcode_id": 75,
    "title": "Sort Colors",
    "slug": "0075_sort_colors",
    "url": "https://leetcode.com/problems/sort-colors/",
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
    ],
    "solution_file": "solutions/0075_sort_colors.py"
  },
  {
    "id": "0076",
    "leetcode_id": 76,
    "title": "Minimum Window Substring",
    "slug": "0076_minimum_window_substring",
    "url": "https://leetcode.com/problems/minimum-window-substring/",
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
    ],
    "solution_file": "solutions/0076_minimum_window_substring.py"
  },
  {
    "id": "0080",
    "leetcode_id": 80,
    "title": "Remove Duplicates from Sorted Array II",
    "slug": "0080_remove_duplicates_from_sorted_array_ii",
    "url": "https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/",
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
    ],
    "solution_file": "solutions/0080_remove_duplicates_from_sorted_array_ii.py"
  },
  {
    "id": "0088",
    "leetcode_id": 88,
    "title": "Merge Sorted Array",
    "slug": "0088_merge_sorted_array",
    "url": "https://leetcode.com/problems/merge-sorted-array/",
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
    ],
    "solution_file": "solutions/0088_merge_sorted_array.py"
  },
  {
    "id": "0125",
    "leetcode_id": 125,
    "title": "Valid Palindrome",
    "slug": "0125_valid_palindrome",
    "url": "https://leetcode.com/problems/valid-palindrome/",
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
    ],
    "solution_file": "solutions/0125_valid_palindrome.py"
  },
  {
    "id": "0141",
    "leetcode_id": 141,
    "title": "Linked List Cycle",
    "slug": "0141_linked_list_cycle",
    "url": "https://leetcode.com/problems/linked-list-cycle/",
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
    ],
    "solution_file": "solutions/0141_linked_list_cycle.py"
  },
  {
    "id": "0142",
    "leetcode_id": 142,
    "title": "Linked List Cycle II",
    "slug": "0142_linked_list_cycle_ii",
    "url": "https://leetcode.com/problems/linked-list-cycle-ii/",
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
    ],
    "solution_file": "solutions/0142_linked_list_cycle_ii.py"
  },
  {
    "id": "0202",
    "leetcode_id": 202,
    "title": "Happy Number",
    "slug": "0202_happy_number",
    "url": "https://leetcode.com/problems/happy-number/",
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
    ],
    "solution_file": "solutions/0202_happy_number.py"
  },
  {
    "id": "0209",
    "leetcode_id": 209,
    "title": "Minimum Size Subarray Sum",
    "slug": "0209_minimum_size_subarray_sum",
    "url": "https://leetcode.com/problems/minimum-size-subarray-sum/",
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
    ],
    "solution_file": "solutions/0209_minimum_size_subarray_sum.py"
  },
  {
    "id": "0215",
    "leetcode_id": 215,
    "title": "Kth Largest Element in an Array",
    "slug": "0215_kth_largest_element_in_an_array",
    "url": "https://leetcode.com/problems/kth-largest-element-in-an-array/",
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
    ],
    "solution_file": "solutions/0215_kth_largest_element_in_an_array.py"
  },
  {
    "id": "0283",
    "leetcode_id": 283,
    "title": "Move Zeroes",
    "slug": "0283_move_zeroes",
    "url": "https://leetcode.com/problems/move-zeroes/",
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
    ],
    "solution_file": "solutions/0283_move_zeroes.py"
  },
  {
    "id": "0340",
    "leetcode_id": 340,
    "title": "Longest Substring with At Most K Distinct Characters",
    "slug": "0340_longest_substring_with_at_most_k_distinct",
    "url": "https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/",
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
    ],
    "solution_file": "solutions/0340_longest_substring_with_at_most_k_distinct.py"
  },
  {
    "id": "0438",
    "leetcode_id": 438,
    "title": "Find All Anagrams in a String",
    "slug": "0438_find_all_anagrams_in_a_string",
    "url": "https://leetcode.com/problems/find-all-anagrams-in-a-string/",
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
    ],
    "solution_file": "solutions/0438_find_all_anagrams_in_a_string.py"
  },
  {
    "id": "0567",
    "leetcode_id": 567,
    "title": "Permutation in String",
    "slug": "0567_permutation_in_string",
    "url": "https://leetcode.com/problems/permutation-in-string/",
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
    ],
    "solution_file": "solutions/0567_permutation_in_string.py"
  },
  {
    "id": "0680",
    "leetcode_id": 680,
    "title": "Valid Palindrome II",
    "slug": "0680_valid_palindrome_ii",
    "url": "https://leetcode.com/problems/valid-palindrome-ii/",
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
    ],
    "solution_file": "solutions/0680_valid_palindrome_ii.py"
  },
  {
    "id": "0876",
    "leetcode_id": 876,
    "title": "Middle of the Linked List",
    "slug": "0876_middle_of_the_linked_list",
    "url": "https://leetcode.com/problems/middle-of-the-linked-list/",
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
    ],
    "solution_file": "solutions/0876_middle_of_the_linked_list.py"
  },
  {
    "id": "0905",
    "leetcode_id": 905,
    "title": "Sort Array By Parity",
    "slug": "0905_sort_array_by_parity",
    "url": "https://leetcode.com/problems/sort-array-by-parity/",
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
    ],
    "solution_file": "solutions/0905_sort_array_by_parity.py"
  },
  {
    "id": "0922",
    "leetcode_id": 922,
    "title": "Sort Array By Parity II",
    "slug": "0922_sort_array_by_parity_ii",
    "url": "https://leetcode.com/problems/sort-array-by-parity-ii/",
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
    ],
    "solution_file": "solutions/0922_sort_array_by_parity_ii.py"
  },
  {
    "id": "0977",
    "leetcode_id": 977,
    "title": "Squares of a Sorted Array",
    "slug": "0977_squares_of_a_sorted_array",
    "url": "https://leetcode.com/problems/squares-of-a-sorted-array/",
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
    ],
    "solution_file": "solutions/0977_squares_of_a_sorted_array.py"
  },
  {
    "id": "0994",
    "leetcode_id": 994,
    "title": "Rotting Oranges",
    "slug": "0994_rotting_oranges",
    "url": "https://leetcode.com/problems/rotting-oranges/",
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
    ],
    "solution_file": "solutions/0994_rotting_oranges.py"
  }
]
```

## 🔗 Link Format Instructions

## Link Generation Rules

**EVERY problem mention with a number MUST have a clickable link.**

### Decision Logic
1. Look up the problem in the Problem Data above
2. Check `solution_file` field:
   - **NOT empty** → GitHub: `https://github.com/lufftw/neetcode/blob/main/{solution_file}`
   - **Empty or not found** → LeetCode: `https://leetcode.com/problems/{slug}/`

### Link Format in Markdown
```markdown
[LeetCode {{id}} - {{title}}](URL)
```

### Examples from Problem Data

**Problem 3 (HAS solution):**
- `solution_file`: `solutions/0003_longest_substring_without_repeating_characters.py`
- Link: `[LeetCode 3 - Longest Substring...](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)`

**Problem not in data (NO solution):**
- Link: `[LeetCode 121 - Best Time to Buy...](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)`

### Slug Format
- LeetCode slug: lowercase with hyphens (e.g., `two-sum`, `best-time-to-buy-and-sell-stock`)
- Can extract from `url` field in problem data

## 🎨 Generation Instructions

Goal: free_form

**Style**: Balance beauty and practicality, suitable for most learners.

**Additional Instructions**: "
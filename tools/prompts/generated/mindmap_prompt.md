# System Prompt

You are a world-class expert who seamlessly integrates multiple professional perspectives 
into a unified, comprehensive understanding:

**As a Top Software Architect**, you design elegant, scalable system architectures and 
understand how algorithms fit into larger software systems. You think in abstractions, 
patterns, and maintainable code structures.

**As a Distinguished Senior Algorithm Professor**, you have decades of experience teaching 
algorithms at the highest level. You understand theoretical foundations, explain complex 
concepts clearly, and know how students learn best. You bridge theory and practice seamlessly.

**As a Senior Principal Engineer**, you've built production systems at scale. You know 
which algorithms work in practice, which fail under load, and how to optimize real-world 
performance. You understand trade-offs and engineering constraints.

**As a Technical Architecture & Language API Provider**, you design APIs and language 
features used by millions. You know how to expose algorithmic concepts through clean 
interfaces and structure knowledge for maximum usability.

**As a LeetCode Learner & Interview Preparer**, you understand the journey from beginner 
to expert. You know which problems build foundational skills, which patterns appear 
frequently in interviews, and how to structure learning paths that lead to success.

**As a Competitive Programming Champion**, you've solved thousands of problems under 
time pressure. You recognize patterns instantly, know optimization tricks, and understand 
the mental models that separate good solutions from great ones.

**As a Project Contributor & Open Source Advocate**, you understand what makes a project 
valuable to the community. You know how to structure knowledge so it's discoverable, 
maintainable, and helps others contribute effectively.

These perspectives are not separate—they inform each other. Your architectural thinking 
enhances your teaching. Your engineering experience grounds your theoretical knowledge. 
Your competitive programming skills inform your interview preparation. Your API design 
sense helps you structure knowledge for learners. You synthesize all these insights 
into mind maps that are simultaneously theoretically sound, practically applicable, 
pedagogically effective, and architecturally elegant.

Your task is to creatively generate Markmap-format mind maps based on the provided LeetCode 
knowledge graph data, drawing from this unified expertise to create mind maps that serve 
learners, interview candidates, competitive programmers, and contributors alike.

IMPORTANT: Generate the mind map content in English. All titles, labels, and descriptions should be in English.

## Your Capabilities

1. **Deep Understanding of Knowledge Graph**: Analyze relationships between API Kernels, Patterns, 
   Algorithms, and Data Structures
2. **Creative Visualization**: Design intuitive, beautiful, and educational mind map structures
3. **Personalized Recommendations**: Adjust content based on user goals
4. **Importance Identification**: Automatically determine which content is most important for learners

## Markmap Features (Please Utilize Fully)

- **Links**: [Problem Name](URL) - Use links for all problem references!
- **Styling**: **bold**, *italic*, ==highlight==, ~~strikethrough~~, `code`
- **Checkboxes**: [ ] To-do, [x] Completed
- **Math Formulas**: $O(n \log n)$, $O(n^2)$
- **Code Blocks**: ```python ... ```
- **Tables**: | A | B | ... |
- **Fold**: <!-- markmap: fold -->
- **Emoji**: For visual emphasis 🎯📚⚡🔥

## CRITICAL: Problem Links Rule

**Every time you mention a LeetCode problem with its number, you MUST add a clickable link.**

Link Selection Logic (check Problem Data in user prompt):
1. Find the problem in the provided Problem Data JSON
2. Check the `solution_file` field:
   - **If `solution_file` is NOT empty** → Link to GitHub solution
   - **If `solution_file` is empty or problem not in data** → Link to LeetCode problem page

Examples:
- Problem WITH solution: `[LeetCode 3 - Longest Substring](https://github.com/.../solutions/0003_xxx.py)`
- Problem WITHOUT solution: `[LeetCode 999 - Some Problem](https://leetcode.com/problems/some-problem/)`

**Never mention a problem number without a link!**

## Output Format

Must be valid Markmap Markdown, starting with this frontmatter:

```
---
title: [Mind Map Title]
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---
```

## Design Principles

1. **Clear Hierarchy**: 3-5 levels optimal
2. **Highlight Key Points**: Use bold and highlight to mark key concepts
3. **Practical Orientation**: Associate each concept with specific problems
4. **Beautiful and Readable**: Use emoji and color layers effectively
5. **Learning-Friendly**: Include progress tracking and difficulty markers

## Important Naming Conventions

- **Always use full name**: Always write "LeetCode" in full, never use abbreviations like "LC" or "LC problem"
- **Problem references**: Use format "LeetCode 1 - Two Sum" or "LeetCode Problem 1", never "LC 1"
- **Consistency**: Maintain consistent naming throughout the mind map

Output Markmap Markdown directly, without any explanations or preambles.

---

# User Prompt

## 📊 Data Summary

- **api_kernels**: 17 items
- **patterns**: 42 items
- **algorithms**: 31 items
- **data_structures**: 31 items
- **families**: 24 items
- **topics**: 41 items
- **difficulties**: 3 items
- **companies**: 47 items
- **roadmaps**: 12 items
- **Pattern Docs**: 1 files
- **Pattern Snippets**: 1 directories, 10 snippets
- **Problems**: 13 problems
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
      "api_kernel": "TwoPointerPartition",
      "summary": "Two pointers moving towards each other."
    },
    {
      "id": "two_pointer_same_direction",
      "api_kernel": "TwoPointerPartition",
      "summary": "Two pointers moving in same direction (fast/slow)."
    },
    {
      "id": "dutch_flag_partition",
      "api_kernel": "TwoPointerPartition",
      "summary": "Three-way partition (Dutch national flag)."
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
| **Minimize Window** | Find shortest valid window | LeetCode 76, 209 |

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Base Template: Unique Characters (LeetCode 3)](#base-template-unique-characters-leetcode-3)
3. [Variation: Minimum Window Substring (LeetCode 76)](#variation-minimum-window-substring-leetcode-76)
4. [Variation: Minimum Size Subarray Sum (LeetCode 209)](#variation-minimum-size-subarray-sum-leetcode-209)
5. [Variation: At Most K Distinct Characters (LeetCode 340/159)](#variation-at-most-k-distinct-characters-leetcode-340159)
6. [Variation: Find All Anagrams (LeetCode 438)](#variation-find-all-anagrams-leetcode-438)
7. [Variation: Permutation in String (LeetCode 567)](#variation-permutation-in-string-leetcode-567)
8. [Pattern Comparison Table](#pattern-comparison-table)
9. [When to Use Sliding Window](#when-to-use-sliding-window)
10. [Template Quick Reference](#template-quick-reference)

---

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

The key insight is the **jump optimization**: instead of incrementally shrinking the window with a while-loop, we directly jump `left` to `last_seen_index[char] + 1`.

This is valid because:
1. Any position before `last_seen_index[char]` would still include the duplicate
2. The position `last_seen_index[char] + 1` is the first position that excludes the duplicate
3. All characters between old `left` and new `left` are implicitly "removed" from consideration

### Trace Example

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
[LeetCode {id} - {title}](URL)
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

Goal: 自由發揮

**Style**: Balance beauty and practicality, suitable for most learners.

**Additional Instructions**: "
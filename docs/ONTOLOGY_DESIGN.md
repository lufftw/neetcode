# NeetCode Ontology & Metadata System Design

> **Status**: Canonical Reference  
> **Scope**: Ontology and metadata system  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

---

## 1. Overview

This document describes the **Ontology + Metadata** system for the NeetCode project.

### 1.1 Goals

- **API Kernels**: Define reusable algorithmic core patterns as "standard library-level" abstractions.
- **Patterns & Problem Families**: Organize problems by shared solving patterns and variations.
- **Structured Metadata**: Enable automatic generation of indexes, roadmaps, and learning paths.
- **Human Readable + Machine Parseable**: Use TOML format for clarity and tooling support.

### 1.2 Core Concepts

| Concept | Description |
|---------|-------------|
| **API Kernel** | Minimal, reusable, highly-optimized algorithmic core that solves a family of problems. |
| **Pattern** | A specific application of an API Kernel to a problem type (e.g., `sliding_window_unique`). |
| **Problem Family** | A group of problems sharing the same Pattern or API Kernel. |
| **Ontology** | Centralized definitions of all concepts (rarely changed). |
| **Meta** | Per-problem/per-solution annotations linking to ontology concepts (frequently changed). |

---

## 2. Directory Structure

```text
neetcode/
  ontology/                          # Concept definitions (rarely changed)
    api_kernels.toml
    patterns.toml
    families.toml
    algorithms.toml
    data_structures.toml
    topics.toml
    difficulties.toml
    companies.toml
    roadmaps.toml

  roadmaps/                          # Detailed roadmap content (order, groups)
    neetcode_150.toml
    blind_75.toml
    grind_75.toml
    sliding_window_path.toml
    ...

  meta/                              # Problem & solution metadata (frequently changed)
    problems/
      0001_two_sum.toml
      0002_add_two_numbers.toml
      0003_longest_substring_without_repeating_characters.toml
      ...

  docs/
    ONTOLOGY_DESIGN.md               # This file
```

---

## 3. Ontology Files Specification

### 3.1 `ontology/api_kernels.toml`

Defines the **mechanism-level** algorithmic cores.

```toml
[[api_kernels]]
id = "SubstringSlidingWindow"
summary = "1D window state machine over sequences with dynamic invariants."

[[api_kernels]]
id = "GridBFSMultiSource"
summary = "Multi-source BFS wavefront propagation on a grid graph."

[[api_kernels]]
id = "KWayMerge"
summary = "Merge K sorted sequences using heap or divide-and-conquer."

[[api_kernels]]
id = "MonotonicStack"
summary = "Stack maintaining monotonic order for next-greater/smaller queries."

[[api_kernels]]
id = "BinarySearchBoundary"
summary = "Binary search for boundary conditions (first >=, last <=, etc.)."

[[api_kernels]]
id = "UnionFindConnectivity"
summary = "Disjoint set union for connectivity queries."

[[api_kernels]]
id = "BacktrackingExploration"
summary = "Exhaustive search with pruning for combinatorial problems."

[[api_kernels]]
id = "LinkedListInPlaceReversal"
summary = "Reverse linked list nodes in-place with pointer manipulation."
```

---

### 3.2 `ontology/patterns.toml`

Defines **problem-solving patterns** that instantiate API Kernels.

```toml
[[patterns]]
id = "sliding_window_unique"
api_kernel = "SubstringSlidingWindow"
summary = "Window where all elements are unique."

[[patterns]]
id = "sliding_window_at_most_k_distinct"
api_kernel = "SubstringSlidingWindow"
summary = "Window with at most K distinct elements."

[[patterns]]
id = "sliding_window_freq_cover"
api_kernel = "SubstringSlidingWindow"
summary = "Window must cover all required character frequencies."

[[patterns]]
id = "sliding_window_cost_bounded"
api_kernel = "SubstringSlidingWindow"
summary = "Window with sum/cost constraint."

[[patterns]]
id = "grid_bfs_propagation"
api_kernel = "GridBFSMultiSource"
summary = "Layered BFS expansion from multiple sources on a grid."

[[patterns]]
id = "merge_k_sorted_heap"
api_kernel = "KWayMerge"
summary = "K-way merge using min-heap."

[[patterns]]
id = "merge_k_sorted_divide"
api_kernel = "KWayMerge"
summary = "K-way merge using divide-and-conquer."

[[patterns]]
id = "next_greater_element"
api_kernel = "MonotonicStack"
summary = "Find next greater element for each position."

[[patterns]]
id = "binary_search_first_true"
api_kernel = "BinarySearchBoundary"
summary = "Find first index where predicate becomes true."

[[patterns]]
id = "backtracking_permutation"
api_kernel = "BacktrackingExploration"
summary = "Generate all permutations with backtracking."

[[patterns]]
id = "backtracking_n_queens"
api_kernel = "BacktrackingExploration"
summary = "Place N queens on board with constraint checking."

[[patterns]]
id = "linked_list_k_group_reversal"
api_kernel = "LinkedListInPlaceReversal"
summary = "Reverse linked list in groups of K nodes."
```

---

### 3.3 `ontology/families.toml`

Defines **problem families** (groups of related problems).

```toml
[[families]]
id = "substring_window"
summary = "Problems about finding optimal substrings using sliding window."

[[families]]
id = "graph_wavefront"
summary = "Problems involving BFS propagation / shortest path on graphs."

[[families]]
id = "merge_sorted"
summary = "Problems merging multiple sorted sequences."

[[families]]
id = "stack_monotonic"
summary = "Problems using monotonic stack for range queries."

[[families]]
id = "binary_search_answer"
summary = "Problems where answer is found by binary searching a value space."

[[families]]
id = "backtracking_combinatorial"
summary = "Problems generating permutations, combinations, or placements."

[[families]]
id = "linked_list_manipulation"
summary = "Problems involving in-place linked list operations."

[[families]]
id = "tree_traversal"
summary = "Problems involving tree traversal patterns."

[[families]]
id = "dynamic_programming_sequence"
summary = "DP problems on sequences (LIS, LCS, etc.)."
```

---

### 3.4 `ontology/algorithms.toml`

Defines **algorithms and techniques**.

```toml
# === Core Algorithms ===
[[algorithms]]
id = "bfs"
kind = "core"
parent = "graph_traversal"
summary = "Breadth-first search using a queue."

[[algorithms]]
id = "dfs"
kind = "core"
parent = "graph_traversal"
summary = "Depth-first search using recursion or stack."

[[algorithms]]
id = "dijkstra"
kind = "core"
parent = "graph_traversal"
summary = "Shortest path in weighted graph using priority queue."

[[algorithms]]
id = "binary_search"
kind = "core"
parent = ""
summary = "Divide search space by half each step."

[[algorithms]]
id = "merge_sort"
kind = "core"
parent = "sorting"
summary = "Divide-and-conquer sorting algorithm."

[[algorithms]]
id = "quick_sort"
kind = "core"
parent = "sorting"
summary = "Partition-based sorting algorithm."

# === Techniques ===
[[algorithms]]
id = "two_pointers"
kind = "technique"
parent = ""
summary = "Move two indices over a sequence under some rule."

[[algorithms]]
id = "sliding_window"
kind = "technique"
parent = "two_pointers"
summary = "Maintain a dynamic window [L,R] with an invariant."

[[algorithms]]
id = "prefix_sum"
kind = "technique"
parent = ""
summary = "Precompute cumulative sums for range queries."

[[algorithms]]
id = "monotonic_stack"
kind = "technique"
parent = ""
summary = "Stack maintaining monotonic order for efficient queries."

[[algorithms]]
id = "union_find"
kind = "technique"
parent = ""
summary = "Disjoint set with union and find operations."

# === Paradigms ===
[[algorithms]]
id = "greedy"
kind = "paradigm"
parent = ""
summary = "Make locally optimal choices at each step."

[[algorithms]]
id = "dynamic_programming"
kind = "paradigm"
parent = ""
summary = "Optimal substructure + overlapping subproblems."

[[algorithms]]
id = "divide_and_conquer"
kind = "paradigm"
parent = ""
summary = "Split problem into subproblems, solve, and combine."

[[algorithms]]
id = "backtracking"
kind = "paradigm"
parent = ""
summary = "Explore all possibilities with pruning."

# === Abstract Parents ===
[[algorithms]]
id = "graph_traversal"
kind = "category"
parent = ""
summary = "Algorithms for traversing graph structures."

[[algorithms]]
id = "sorting"
kind = "category"
parent = ""
summary = "Algorithms for ordering elements."
```

**Note on `kind`**:
- `core`: Classic named algorithms (BFS, DFS, Dijkstra, etc.)
- `technique`: Coding patterns/tricks (sliding window, two pointers, etc.)
- `paradigm`: High-level strategies (greedy, DP, backtracking, etc.)
- `category`: Abstract groupings (not directly used in solutions)

---

### 3.5 `ontology/data_structures.toml`

Defines **data structures**.

```toml
[[data_structures]]
id = "array"
parent = ""
summary = "Contiguous indexed collection."

[[data_structures]]
id = "string"
parent = "array"
summary = "Character array."

[[data_structures]]
id = "hash_map"
parent = "associative_container"
summary = "Key-value store with O(1) average access."

[[data_structures]]
id = "hash_set"
parent = "associative_container"
summary = "Unique element collection with O(1) average lookup."

[[data_structures]]
id = "min_heap"
parent = "priority_queue"
summary = "Binary heap for min-priority queue."

[[data_structures]]
id = "max_heap"
parent = "priority_queue"
summary = "Binary heap for max-priority queue."

[[data_structures]]
id = "stack"
parent = ""
summary = "LIFO collection."

[[data_structures]]
id = "queue"
parent = ""
summary = "FIFO collection."

[[data_structures]]
id = "deque"
parent = ""
summary = "Double-ended queue."

[[data_structures]]
id = "linked_list"
parent = ""
summary = "Linear collection with O(1) insert/delete at known position."

[[data_structures]]
id = "binary_tree"
parent = "tree"
summary = "Tree where each node has at most two children."

[[data_structures]]
id = "binary_search_tree"
parent = "binary_tree"
summary = "Binary tree with ordered property."

[[data_structures]]
id = "graph"
parent = ""
summary = "Nodes and edges structure."

[[data_structures]]
id = "grid"
parent = "graph"
summary = "2D matrix as implicit graph."

[[data_structures]]
id = "disjoint_set"
parent = ""
summary = "Union-Find data structure."

# === Abstract Parents ===
[[data_structures]]
id = "associative_container"
parent = ""
summary = "Containers with key-based access."

[[data_structures]]
id = "priority_queue"
parent = ""
summary = "Queue with priority ordering."

[[data_structures]]
id = "tree"
parent = ""
summary = "Hierarchical node structure."
```

---

### 3.6 `ontology/topics.toml`

Defines **LeetCode-style topics/tags**.

```toml
[[topics]]
id = "array"
summary = "Problems involving array manipulation."

[[topics]]
id = "string"
summary = "Problems involving string processing."

[[topics]]
id = "hash_table"
summary = "Problems using hash-based structures."

[[topics]]
id = "linked_list"
summary = "Problems on linked list structures."

[[topics]]
id = "stack"
summary = "Problems using stack data structure."

[[topics]]
id = "queue"
summary = "Problems using queue data structure."

[[topics]]
id = "tree"
summary = "Problems on tree structures."

[[topics]]
id = "binary_tree"
summary = "Problems on binary trees."

[[topics]]
id = "binary_search_tree"
summary = "Problems on BST."

[[topics]]
id = "graph"
summary = "Problems on graph structures."

[[topics]]
id = "breadth_first_search"
summary = "Problems using BFS."

[[topics]]
id = "depth_first_search"
summary = "Problems using DFS."

[[topics]]
id = "dynamic_programming"
summary = "Problems using DP approach."

[[topics]]
id = "greedy"
summary = "Problems using greedy strategy."

[[topics]]
id = "backtracking"
summary = "Problems using backtracking."

[[topics]]
id = "binary_search"
summary = "Problems using binary search."

[[topics]]
id = "sliding_window"
summary = "Problems using sliding window technique."

[[topics]]
id = "two_pointers"
summary = "Problems using two pointers technique."

[[topics]]
id = "heap"
summary = "Problems using heap/priority queue."

[[topics]]
id = "sorting"
summary = "Problems involving sorting."

[[topics]]
id = "math"
summary = "Problems requiring mathematical reasoning."

[[topics]]
id = "bit_manipulation"
summary = "Problems using bit operations."

[[topics]]
id = "recursion"
summary = "Problems solved recursively."

[[topics]]
id = "divide_and_conquer"
summary = "Problems using divide and conquer."

[[topics]]
id = "union_find"
summary = "Problems using disjoint set union."

[[topics]]
id = "trie"
summary = "Problems using trie data structure."

[[topics]]
id = "matrix"
summary = "Problems on 2D matrices."
```

---

### 3.7 `ontology/difficulties.toml`

Defines **difficulty levels**.

```toml
[[difficulties]]
id = "easy"
level = 1
color = "green"
summary = "Beginner-friendly problems."

[[difficulties]]
id = "medium"
level = 2
color = "orange"
summary = "Intermediate problems."

[[difficulties]]
id = "hard"
level = 3
color = "red"
summary = "Advanced problems."
```

---

### 3.8 `ontology/companies.toml`

Defines **companies** that ask these problems.

```toml
[[companies]]
id = "google"
name = "Google"

[[companies]]
id = "meta"
name = "Meta (Facebook)"

[[companies]]
id = "amazon"
name = "Amazon"

[[companies]]
id = "microsoft"
name = "Microsoft"

[[companies]]
id = "apple"
name = "Apple"

[[companies]]
id = "netflix"
name = "Netflix"

[[companies]]
id = "uber"
name = "Uber"

[[companies]]
id = "airbnb"
name = "Airbnb"

[[companies]]
id = "linkedin"
name = "LinkedIn"

[[companies]]
id = "twitter"
name = "Twitter (X)"

[[companies]]
id = "bloomberg"
name = "Bloomberg"

[[companies]]
id = "adobe"
name = "Adobe"

[[companies]]
id = "oracle"
name = "Oracle"

[[companies]]
id = "salesforce"
name = "Salesforce"

[[companies]]
id = "bytedance"
name = "ByteDance"
```

---

### 3.9 `ontology/roadmaps.toml`

Defines **available roadmaps** (metadata only, content in `roadmaps/`).

```toml
[[roadmaps]]
id = "neetcode_150"
name = "NeetCode 150"
url = "https://neetcode.io/roadmap"
summary = "Curated 150 problems for coding interview prep."

[[roadmaps]]
id = "neetcode_all"
name = "NeetCode All"
url = "https://neetcode.io/practice"
summary = "Complete NeetCode problem set."

[[roadmaps]]
id = "blind_75"
name = "Blind 75"
url = "https://leetcode.com/discuss/general-discussion/460599/blind-75"
summary = "Classic 75 interview questions."

[[roadmaps]]
id = "grind_75"
name = "Grind 75"
url = "https://www.techinterviewhandbook.org/grind75"
summary = "Updated interview prep list with time-based scheduling."

[[roadmaps]]
id = "leetcode_top_100"
name = "LeetCode Top 100 Liked"
url = "https://leetcode.com/problemset/top-100-liked-questions/"
summary = "Most liked problems on LeetCode."

[[roadmaps]]
id = "sliding_window_path"
name = "Sliding Window Mastery"
summary = "Step-by-step path to master sliding window pattern."

[[roadmaps]]
id = "graph_bfs_path"
name = "BFS Mastery"
summary = "Step-by-step path to master BFS patterns."
```

---

## 4. Roadmap Files Specification

Detailed roadmap content lives in `roadmaps/*.toml`.

### 4.1 Topic-based Roadmap (e.g., NeetCode 150)

```toml
# roadmaps/neetcode_150.toml
id = "neetcode_150"
name = "NeetCode 150"

[[groups]]
name = "Arrays & Hashing"
order = 1
problems = [
  "0217_contains_duplicate",
  "0242_valid_anagram",
  "0001_two_sum",
  "0049_group_anagrams",
  "0347_top_k_frequent_elements",
  "0238_product_of_array_except_self",
  "0036_valid_sudoku",
  "0128_longest_consecutive_sequence",
]

[[groups]]
name = "Two Pointers"
order = 2
problems = [
  "0125_valid_palindrome",
  "0167_two_sum_ii",
  "0015_three_sum",
  "0011_container_with_most_water",
  "0042_trapping_rain_water",
]

[[groups]]
name = "Sliding Window"
order = 3
problems = [
  "0121_best_time_to_buy_and_sell_stock",
  "0003_longest_substring_without_repeating_characters",
  "0424_longest_repeating_character_replacement",
  "0567_permutation_in_string",
  "0076_minimum_window_substring",
  "0239_sliding_window_maximum",
]

[[groups]]
name = "Stack"
order = 4
problems = [
  "0020_valid_parentheses",
  "0155_min_stack",
  "0150_evaluate_reverse_polish_notation",
  "0022_generate_parentheses",
  "0739_daily_temperatures",
  "0853_car_fleet",
  "0084_largest_rectangle_in_histogram",
]

# ... more groups ...
```

### 4.2 Pattern-based Roadmap (Learning Path)

```toml
# roadmaps/sliding_window_path.toml
id = "sliding_window_path"
name = "Sliding Window Mastery Path"
api_kernel = "SubstringSlidingWindow"

[[steps]]
order = 1
problem = "0003_longest_substring_without_repeating_characters"
role = "base"
pattern = "sliding_window_unique"
note = "Learn the canonical sliding window template."

[[steps]]
order = 2
problem = "0340_longest_substring_with_at_most_k_distinct_characters"
role = "variant"
pattern = "sliding_window_at_most_k_distinct"
prerequisite = ["0003"]
delta = "Change uniqueness to distinct_count <= K."
note = "Add a counter constraint."

[[steps]]
order = 3
problem = "0159_longest_substring_with_at_most_two_distinct_characters"
role = "variant"
pattern = "sliding_window_at_most_k_distinct"
prerequisite = ["0340"]
delta = "Special case: K = 2."
note = "Practice the same pattern with fixed K."

[[steps]]
order = 4
problem = "0076_minimum_window_substring"
role = "variant"
pattern = "sliding_window_freq_cover"
prerequisite = ["0003"]
delta = "Track need/have frequencies; find minimum window."
note = "Reverse condition: window must cover all required chars."

[[steps]]
order = 5
problem = "0567_permutation_in_string"
role = "variant"
pattern = "sliding_window_freq_cover"
prerequisite = ["0076"]
delta = "Fixed window size = pattern length."
note = "Simplified version of minimum window."

[[steps]]
order = 6
problem = "0438_find_all_anagrams_in_a_string"
role = "variant"
pattern = "sliding_window_freq_cover"
prerequisite = ["0567"]
delta = "Collect all starting indices instead of just checking existence."
note = "Extension of permutation check."

[[steps]]
order = 7
problem = "0209_minimum_size_subarray_sum"
role = "variant"
pattern = "sliding_window_cost_bounded"
prerequisite = ["0003"]
delta = "Numeric array; condition is sum >= target."
note = "Numeric version of sliding window."

[[steps]]
order = 8
problem = "1004_max_consecutive_ones_iii"
role = "variant"
pattern = "sliding_window_cost_bounded"
prerequisite = ["0209"]
delta = "Cost = number of flips; maximize window with flip_count <= K."
note = "Binary array variant."
```

---

## 5. Problem Metadata Specification

Each problem has a `.toml` file in `meta/problems/`.

### 5.1 Full Example: `0003_longest_substring_without_repeating_characters.toml`

```toml
# ===== Problem Info =====
id = "0003"
slug = "0003_longest_substring_without_repeating_characters"
title = "Longest Substring Without Repeating Characters"
leetcode_id = 3
url = "https://leetcode.com/problems/longest-substring-without-repeating-characters/"

# ===== LeetCode Official Metadata =====
difficulty = "medium"
topics = ["string", "hash_table", "sliding_window"]
companies = ["google", "amazon", "meta", "microsoft", "apple", "bloomberg"]

# ===== Roadmaps =====
roadmaps = ["neetcode_150", "blind_75", "grind_75", "sliding_window_path"]

# ===== Ontology Tags (Problem Level) =====
api_kernels      = ["SubstringSlidingWindow"]
patterns         = ["sliding_window_unique"]
families         = ["substring_window"]
data_structures  = ["string", "hash_map"]
algorithms       = ["sliding_window", "two_pointers"]
related_problems = ["0340", "0076", "0438", "0209", "0159"]

# ===== Solutions =====
[[solutions]]
key    = "default"
class  = "Solution"
method = "lengthOfLongestSubstring"

api_kernels      = ["SubstringSlidingWindow"]
patterns         = ["sliding_window_unique"]
families         = ["substring_window"]
data_structures  = ["string", "hash_map"]
algorithms       = ["sliding_window", "two_pointers"]
related_problems = ["0340", "0076"]

role       = "base"
variant    = ""
based_on   = []
delta      = ""
complexity = "O(n) time, O(min(n, Σ)) space"
notes      = "Canonical sliding window with last-seen index map."
```

### 5.2 Example: `0994_rotting_oranges.toml`

```toml
id = "0994"
slug = "0994_rotting_oranges"
title = "Rotting Oranges"
leetcode_id = 994
url = "https://leetcode.com/problems/rotting-oranges/"

difficulty = "medium"
topics = ["array", "breadth_first_search", "matrix"]
companies = ["amazon", "microsoft", "google"]

roadmaps = ["neetcode_150", "graph_bfs_path"]

api_kernels      = ["GridBFSMultiSource"]
patterns         = ["grid_bfs_propagation"]
families         = ["graph_wavefront"]
data_structures  = ["grid", "queue"]
algorithms       = ["bfs"]
related_problems = ["0286", "0542", "0127", "0752", "1091"]

[[solutions]]
key    = "bfs"
class  = "Solution"
method = "orangesRotting"

api_kernels      = ["GridBFSMultiSource"]
patterns         = ["grid_bfs_propagation"]
families         = ["graph_wavefront"]
data_structures  = ["grid", "queue"]
algorithms       = ["bfs"]
related_problems = ["0286", "0542"]

role       = "base"
variant    = "multi_source_bfs"
based_on   = []
delta      = ""
complexity = "O(m*n)"
notes      = "Classic multi-source BFS on 2D grid."
```

### 5.3 Example: `0023_merge_k_sorted_lists.toml`

```toml
id = "0023"
slug = "0023_merge_k_sorted_lists"
title = "Merge k Sorted Lists"
leetcode_id = 23
url = "https://leetcode.com/problems/merge-k-sorted-lists/"

difficulty = "hard"
topics = ["linked_list", "divide_and_conquer", "heap"]
companies = ["google", "meta", "amazon", "microsoft", "uber"]

roadmaps = ["neetcode_150", "blind_75"]

api_kernels      = ["KWayMerge"]
patterns         = ["merge_k_sorted_heap", "merge_k_sorted_divide"]
families         = ["merge_sorted", "linked_list_manipulation"]
data_structures  = ["linked_list", "min_heap"]
algorithms       = ["divide_and_conquer"]
related_problems = ["0021", "0004", "0378"]

[[solutions]]
key    = "heap"
class  = "SolutionHeap"
method = "mergeKListsPriorityQueue"

api_kernels      = ["KWayMerge"]
patterns         = ["merge_k_sorted_heap"]
families         = ["merge_sorted"]
data_structures  = ["linked_list", "min_heap"]
algorithms       = []
related_problems = ["0021", "0378"]

role       = "base"
variant    = "heap"
based_on   = []
delta      = ""
complexity = "O(N log k)"
notes      = "Heap-based K-way merge."

[[solutions]]
key    = "divide"
class  = "SolutionDivide"
method = "mergeKListsDivideConquer"

api_kernels      = ["KWayMerge"]
patterns         = ["merge_k_sorted_divide"]
families         = ["merge_sorted"]
data_structures  = ["linked_list"]
algorithms       = ["divide_and_conquer"]
related_problems = ["0021"]

role       = "variant"
variant    = "divide_and_conquer"
based_on   = ["0023#heap"]
delta      = "Use merge-sort-like tree instead of heap."
complexity = "O(N log k)"
notes      = "Divide-and-conquer K-way merge."

[[solutions]]
key    = "greedy"
class  = "SolutionGreedy"
method = "mergeKListsGreedy"

api_kernels      = ["KWayMerge"]
patterns         = []
families         = ["merge_sorted"]
data_structures  = ["linked_list"]
algorithms       = ["greedy"]
related_problems = []

role       = "variant"
variant    = "greedy_comparison"
based_on   = ["0023#heap"]
delta      = "Compare all K heads each time (less efficient)."
complexity = "O(kN)"
notes      = "Naive greedy approach for comparison."
```

### 5.4 Example: `0051_n_queens.toml`

```toml
id = "0051"
slug = "0051_n_queens"
title = "N-Queens"
leetcode_id = 51
url = "https://leetcode.com/problems/n-queens/"

difficulty = "hard"
topics = ["array", "backtracking"]
companies = ["google", "amazon", "meta"]

roadmaps = ["neetcode_150"]

api_kernels      = ["BacktrackingExploration"]
patterns         = ["backtracking_n_queens"]
families         = ["backtracking_combinatorial"]
data_structures  = ["array", "hash_set"]
algorithms       = ["backtracking"]
related_problems = ["0052", "0037"]

[[solutions]]
key    = "default"
class  = "Solution"
method = "solveNQueens"

api_kernels      = ["BacktrackingExploration"]
patterns         = ["backtracking_n_queens"]
families         = ["backtracking_combinatorial"]
data_structures  = ["array", "hash_set"]
algorithms       = ["backtracking"]
related_problems = ["0052"]

role       = "base"
variant    = ""
based_on   = []
delta      = ""
complexity = "O(n!) time"
notes      = "Classic backtracking with column/diagonal tracking."
```

---

## 6. Solution-Level Metadata Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | ✅ | Unique identifier for this solution (e.g., `"default"`, `"heap"`, `"divide"`) |
| `class` | string | ✅ | Python class name in the solution file |
| `method` | string | ✅ | Method name to call |
| `api_kernels` | array | ❌ | API Kernels used by this specific solution |
| `patterns` | array | ❌ | Patterns used by this specific solution |
| `families` | array | ❌ | Problem families this solution belongs to |
| `data_structures` | array | ❌ | Data structures used |
| `algorithms` | array | ❌ | Algorithms/techniques used |
| `related_problems` | array | ❌ | Closely related problems for this approach |
| `role` | string | ✅ | `"base"` or `"variant"` |
| `variant` | string | ❌ | Variant name (if role is variant) |
| `based_on` | array | ❌ | Reference to base solution (e.g., `["0003#default"]`) |
| `delta` | string | ❌ | One-line description of difference from base |
| `complexity` | string | ❌ | Time/space complexity |
| `notes` | string | ❌ | Additional notes |

---

## 7. Summary: What Goes Where?

| Content | Location | Change Frequency |
|---------|----------|------------------|
| API Kernel definitions | `ontology/api_kernels.toml` | Rarely |
| Pattern definitions | `ontology/patterns.toml` | Rarely |
| Family definitions | `ontology/families.toml` | Rarely |
| Algorithm definitions | `ontology/algorithms.toml` | Rarely |
| Data structure definitions | `ontology/data_structures.toml` | Rarely |
| Topic definitions | `ontology/topics.toml` | Rarely |
| Difficulty definitions | `ontology/difficulties.toml` | Almost never |
| Company definitions | `ontology/companies.toml` | Occasionally |
| Roadmap definitions | `ontology/roadmaps.toml` | Occasionally |
| Roadmap content (order, groups) | `roadmaps/*.toml` | Occasionally |
| **Problem ↔ concept mappings** | `meta/problems/*.toml` | **Frequently** |

---

## 8. Future Tooling Ideas

Once this structure is in place, we can build tools to:

1. **Generate README indexes**
   - List all problems by API Kernel
   - List all problems by Pattern
   - List all problems by Topic/Difficulty

2. **Generate roadmap views**
   - Render roadmap as Markdown with links to solutions
   - Show progress tracking

3. **Validate metadata**
   - Check all referenced IDs exist in ontology
   - Check for missing required fields

4. **Search & filter**
   - Find all problems using a specific pattern
   - Find all problems from a specific company

5. **Learning path recommendations**
   - Based on current progress, suggest next problem
   - Show prerequisite relationships

---

## 9. Implementation Plan

### Phase 1: Create Ontology Files
- [ ] Create `ontology/` directory
- [ ] Create all ontology `.toml` files with initial entries
- [ ] Validate TOML syntax

### Phase 2: Create Roadmap Files
- [ ] Create `roadmaps/` directory
- [ ] Create `neetcode_150.toml` with groups
- [ ] Create `sliding_window_path.toml` as pattern-based example

### Phase 3: Create Problem Metadata
- [ ] Create `meta/problems/` directory
- [ ] Create `.toml` files for existing solutions:
  - [ ] 0001_two_sum.toml
  - [ ] 0002_add_two_numbers.toml
  - [ ] 0003_longest_substring_without_repeating_characters.toml
  - [ ] 0004_median_of_two_sorted_arrays.toml
  - [ ] 0023_merge_k_sorted_lists.toml
  - [ ] 0025_reverse_nodes_in_k_group.toml
  - [ ] 0051_n_queens.toml
  - [ ] 0994_rotting_oranges.toml

### Phase 4: Validation & Tooling
- [ ] Write Python script to validate all metadata
- [ ] Write script to generate problem index README

---

## 10. Open Questions

1. Should `topics` in problem meta mirror LeetCode exactly, or can we add custom topics?
2. How to handle problems that don't fit any existing API Kernel?
3. Should we version the ontology schema?

---

## Appendix A: TOML Syntax Reference

```toml
# Single values
id = "string_value"
level = 123
enabled = true

# Arrays
topics = ["array", "string", "hash_table"]

# Inline tables
meta = { author = "user", version = 1 }

# Array of tables (for multiple entries)
[[items]]
id = "item1"
name = "First Item"

[[items]]
id = "item2"
name = "Second Item"
```

---

## Appendix B: Relationship Diagram

```
                    ┌─────────────────┐
                    │   API Kernel    │
                    │ (mechanism)     │
                    └────────┬────────┘
                             │ instantiates
                             ▼
                    ┌─────────────────┐
                    │    Pattern      │
                    │ (problem type)  │
                    └────────┬────────┘
                             │ belongs to
                             ▼
                    ┌─────────────────┐
                    │ Problem Family  │
                    │ (group)         │
                    └────────┬────────┘
                             │ contains
                             ▼
┌──────────────────────────────────────────────────────┐
│                      Problem                         │
│  ┌─────────────────────────────────────────────┐    │
│  │ Solution 1 (base)                           │    │
│  │   - uses: data_structures, algorithms       │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │ Solution 2 (variant)                        │    │
│  │   - based_on: Solution 1                    │    │
│  │   - delta: "different approach"             │    │
│  └─────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
```

---

*End of Design Document*

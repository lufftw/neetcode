---
title: Solution Variants - Multiple Approaches per Problem
markmap:
  colorFreezeLevel: 2
  maxWidth: 400
---

# Solution Variants

Problems with multiple solution approaches. Understanding different approaches
deepens your algorithmic thinking.

## LeetCode 23 - Merge k Sorted Lists

**🔴 Hard** — 4 approaches

📁 <a href="https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py" target="_blank" rel="noopener noreferrer">View All Solutions</a>

### 🎯 Default (Base)

*Variant: heap*

- **Complexity:** `O(N log k) time, O(k) space`
- **Notes:** Min-heap based K-way merge. Classic API Kernel for merging K sorted sequences.

### 🎯 Heap (Base)

*Variant: heap*

- **Complexity:** `O(N log k) time, O(k) space`
- **Notes:** Same as default. Min-heap keeps track of smallest among K heads.

### 🔄 Divide

*Variant: divide_and_conquer*

- **Complexity:** `O(N log k) time, O(log k) space (recursion)`
- **Delta from base:** Use merge-sort-like tree instead of heap. Pair-wise merge in log(k) rounds.
- **Notes:** Divide and conquer: recursively merge pairs until one list remains.

### 🔄 Greedy

*Variant: greedy_comparison*

- **Complexity:** `O(kN) time, O(1) space`
- **Delta from base:** Compare all K heads each time to find minimum. Less efficient but simpler.
- **Notes:** Naive greedy approach for comparison. Demonstrates why heap optimization matters.

## LeetCode 3 - Longest Substring Without Repeating Characters

**🟡 Medium** — 3 approaches

📁 <a href="https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py" target="_blank" rel="noopener noreferrer">View All Solutions</a>

### 🎯 Default (Base)

- **Complexity:** `O(n) time, O(min(n, Σ)) space`
- **Notes:** Canonical sliding window template with last-seen index array. Uses jump optimization instead of while-loop contraction. This is the BASE TEMPLATE for all SubstringSlidingWindow problems.

### 🔄 Dict

*Variant: dictionary*

- **Complexity:** `O(n) time, O(min(n, Σ)) space`
- **Delta from base:** Uses dictionary instead of array for last-seen index. More flexible for Unicode.

### 🔄 Set

*Variant: set_while_loop*

- **Complexity:** `O(n) time, O(min(n, Σ)) space`
- **Delta from base:** Uses set + while-loop contraction. More intuitive but no jump optimization.
- **Notes:** Demonstrates standard while-loop contraction pattern used in other variants.

## LeetCode 25 - Reverse Nodes in k-Group

**🔴 Hard** — 3 approaches

📁 <a href="https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py" target="_blank" rel="noopener noreferrer">View All Solutions</a>

### 🎯 Default (Base)

*Variant: iterative*

- **Complexity:** `O(N) time, O(1) space`
- **Notes:** Iterative in-place k-group reversal using pointer manipulation. Constant space.

### 🎯 Iterative (Base)

*Variant: iterative*

- **Complexity:** `O(N) time, O(1) space`
- **Notes:** Same as default. Process k nodes at a time, reverse in-place.

### 🔄 Recursive

*Variant: recursive*

- **Complexity:** `O(N) time, O(N/k) space (recursion stack)`
- **Delta from base:** Use recursion to handle groups. Stack space for recursion.
- **Notes:** Recursive approach: reverse k nodes, then recurse on remaining list.

## LeetCode 340 - Longest Substring with At Most K Distinct Characters

**🟡 Medium** — 2 approaches

📁 <a href="https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py" target="_blank" rel="noopener noreferrer">View All Solutions</a>

### 🔄 Default

*Variant: at_most_k_distinct*

- **Complexity:** `O(n) time, O(K) space`
- **Delta from base:** Replace 'unique' with 'distinct count <= K'. Use frequency map instead of last-seen-index.
- **Notes:** Cannot use jump optimization - must shrink incrementally. Uses len(freq_map) as distinct count.

### 🔄 Two Distinct

*Variant: k_equals_2*

- **Complexity:** `O(n) time, O(1) space`
- **Delta from base:** Special case: K=2 (LeetCode 159)
- **Notes:** Direct specialization for LeetCode 159. Hardcodes K=2.

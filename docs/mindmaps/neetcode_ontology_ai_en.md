---
title: LeetCode Knowledge Graph Mind Map (Core Patterns → Kernels → Problems)
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 How to use this map (free-form, interview-oriented)
- **Rule of thumb**: pick a *pattern* → learn its *invariant* → practice 2–5 *problems* → generalize to *kernel template*
- [ ] Do 1 easy + 2 medium per kernel before moving on
- [ ] After each problem, write: `state`, `invariant`, `when to shrink/expand`, `time/space`

## 🧠 API Kernels (the reusable “engines”)
<!-- markmap: fold -->
- **SubstringSlidingWindow** — *1D window state machine with dynamic invariants*
  - Core complexity: $O(n)$ (each element enters/exits window ≤ 1)
  - State: `hash_map/counter`, sometimes `sum`
- **TwoPointersTraversal** — *two indices under invariant-preserving rules*
  - Opposite pointers / Same-direction writer / Dedup enumeration
- **FastSlowPointers** — *Floyd cycle + midpoint*
- **BacktrackingExploration** — *Choose → Explore → Unchoose* decision tree
- **GridBFSMultiSource** — *wavefront BFS from multiple sources*
- **KWayMerge** — *merge K sorted sequences (heap or divide-and-conquer)*
- **MergeSortedSequences** — *merge two sorted sequences*
- **TwoPointerPartition** — *partitioning (Dutch flag, quickselect partition)*
- **BinarySearchBoundary** — *first/last true, binary search on answer*
- **HeapTopK** — *top-k / kth / stream median*
- **PrefixSumRangeQuery** — *prefix sums + hash map for subarray queries*
- **MonotonicStack** — *next greater/smaller, histogram*
- **TreeTraversalDFS / TreeTraversalBFS** — *tree traversals*
- **UnionFindConnectivity** — *components / cycle detection*
- **DPSequence / DPInterval** — *sequence DP / interval DP*
- **TopologicalSort** — *DAG ordering*
- **TriePrefixSearch** — *prefix matching*

---

## 🪟 Sliding Window Family: `substring_window` (Kernel: SubstringSlidingWindow) 🎯
### ==Invariant-first thinking==
- Window `[L..R]` is valid iff **invariant holds**
- Two modes:
  - **Maximize**: expand `R`, shrink while invalid
  - **Minimize**: expand until valid, shrink while still valid

### Pattern comparison (cheat table)
| Pattern | Invariant | State | Window | Typical goal | Practice |
|---|---|---|---|---|---|
| sliding_window_unique | all unique | last index / freq | variable | maximize |[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) |
| sliding_window_at_most_k_distinct | ≤ K distinct | freq map | variable | maximize |[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) |
| sliding_window_freq_cover | covers required freq | need/have maps | variable/fixed | minimize / exists / all |[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py),[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py),[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) |
| sliding_window_cost_bounded | sum/cost constraint | integer sum | variable | minimize |[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) |

### Core problems
- **Unique window**
  - [ ][LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [ ][LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - [ ][LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)[ ][LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)[ ][LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - [ ][LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)

## 👉 Two Pointers Family (Kernel: TwoPointersTraversal) ⚡
### Pattern comparison
| Sub-pattern | Pointer init | Invariant | Time | Practice |
|---|---|---|---|---|
| Opposite pointers | `l=0, r=n-1` | answer lies within `[l,r]` | $O(n)$ |[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py),[LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py),[LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py), LeetCode 167 |
| Same-direction writer | `write=0`, `read` scans | `arr[:write]` is “kept/clean” | $O(n)$ |[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py),[LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py),[LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py),[LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) |
| Dedup enumeration (k-sum core) | sort + fixed `i` + `(l,r)` | skip duplicates deterministically | $O(n^2)$ |[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py),[LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py), LeetCode 18 |
| Merge (2 sorted) | `i,j` forward | output is sorted prefix | $O(m+n)$ |[LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py),[LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py),[LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py) |

### Opposite pointers (search / maximize / palindrome)
- **two_pointer_opposite_maximize**
  - [ ][LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ][LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)[ ][LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)(sorted pair search)
  - [ ] LeetCode 167 *(related via graph; good to add if available in your set)*

### Same-direction writer (in-place array modification)
- **two_pointer_writer_dedup**
  - [ ][LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)[ ][LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
  - [ ][LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - [ ][LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)

### Multi-sum enumeration (sort + two pointers)
- **two_pointer_three_sum**
  - [ ][LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)[ ][LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - [ ] LeetCode 18 *(related; if in your full 45 set)*

---

## 🐢🐇 Fast–Slow Pointers (Kernel: FastSlowPointers) 🔥
### Two-phase Floyd mental model
- Phase 1: detect cycle
- Phase 2: find cycle start (reset one pointer to head)

### Practice ladder
- [ ][LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py) *(cycle detect)*
- [ ][LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py) *(cycle start)*
- [ ][LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py) *(implicit cycle)*
- [ ][LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py) *(midpoint)*

---

## 🧩 Backtracking (Kernel: BacktrackingExploration) 📚
### ==The invariant==
- **State consistency**: after returning from recursion, state must be exactly restored

### 5 decision-tree shapes (use the right “state handle”)
- **Permutation** → `used[]`
  - [ ][LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)[ ][LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py) *(dedup: sort + same-level skip via `used[i-1]==False`)*
- **Subset** → `start_index`
  - [ ][LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)[ ][LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py) *(dedup: sort + same-level skip `i>start && nums[i]==nums[i-1]`)*
- **Combination / fixed size** → `start_index` + `len(path)==k`
  - [ ][LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)(sorted early break)
  - [ ][LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) *(reuse allowed: recurse with `i`)*
  - [ ][LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py) *(no reuse: recurse with `i+1` + dedup)*
  - [ ][LeetCode 216 - Combination Sum III](https://leetcode.com/problems/combination-sum-iii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py) *(fixed count + bounded range)*
- **Constraint satisfaction / placement**
  - [ ][LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)[ ][LeetCode 52 - N-Queens II](https://leetcode.com/problems/n-queens-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
  - [ ][LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)[ ][LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
  - [ ][LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

### Backtracking “toolbelt”
- **Pruning**
  - feasibility bound (not enough remaining choices)
  - target bound (`remaining < 0`)
  - sorted early exit (`candidates[i] > remaining → break`)
- **Dedup strategies**
  - sort + same-level skip (subset/combination)
  - sort + `used`-based skip (permutation)

---

## 🌊 Graph Wavefront BFS (Kernel: GridBFSMultiSource) 🎯
### grid_bfs_propagation
- Multi-source BFS = enqueue all sources first, expand level by level
- Complexity: $O(R \cdot C)$ for grid

### Practice
- [ ][LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

## 🔗 Merge Sorted Family
### Merge 2 sorted (Kernel: MergeSortedSequences)
- [ ][LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)[ ][LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)[ ][LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

### Merge K sorted (Kernel: KWayMerge)
- **merge_k_sorted_heap**: $O(N \log K)$
- **merge_k_sorted_divide**: $O(N \log K)$
- [ ][LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)(binary search + merge idea space)
  - [ ][LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

## 🎛️ Partitioning & Selection (Kernel: TwoPointerPartition / HeapTopK)
### Partitioning
- **dutch_flag_partition**
  - [ ][LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
  - [ ][LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)[ ][LeetCode 922 - Sort Array By Parity II](https://leetcode.com/problems/sort-array-by-parity-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
  - [ ][LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

### Heap alternative for kth/top-k (Kernel: HeapTopK)
- **heap_kth_element**
  - [ ][LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) *(compare: quickselect avg $O(n)$ vs heap $O(n\log k)$)*

---

## 🧭 Roadmap Anchors (from your graph)
- **NeetCode 150**:[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 2, 3, 4, 11, 15, 21, 23, 25, 26, 27, 39, 40, 46, 51, 75, 76, 78, 79, 80, 88, 90, 125, 131, 141, 142, 202, 209, 215, 283, 438, 567, 680, 876, 905, 922, 977, 994
- **Blind 75** (subset present):[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 3, 11, 15, 21, 23, 26, 39, 75, 76, 79, 125, 141, 142, 215, 994
- **Specialty paths**
  - Sliding Window Mastery:[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py), 76, 209, 340, 438, 567
  - BFS Mastery:[LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

---

## ✅ Quick “next 10 problems” playlist (balanced)
- [ ][LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)[ ][LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)[ ][LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)[ ][LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)[ ][LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)[ ][LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)[ ][LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)[ ][LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)[ ][LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)[ ][LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
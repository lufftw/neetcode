---
title: LeetCode Knowledge Graph 🎯 — Kernels → Patterns → Problems (Creative Atlas)
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

# LeetCode Knowledge Graph 🎯 — Kernels → Patterns → Problems
- ==How to read this map==
  - **API Kernel** = reusable “engine” (mental + code machine)
  - *Pattern* = a specific invariant/state style on top of the kernel
  - `LeetCode {number}` = practice anchor (titles auto-added later)
  - [ ] = to-do, [x] = mastered
- ==Primary learning loop==
  - [ ] Learn kernel invariant → memorize 1 template → solve 3 problems → refactor template → repeat
  - Rule of thumb: each element enters/exits state at most once ⇒ aim for $O(n)$ when possible

---

## ⚡ The 4 “Superhighways” (most ROI for interviews)
- **Two Pointers Universe** → elimination by monotonic movement
- **Sliding Window Universe** → window state machine with invariant
- **Backtracking Universe** → reversible exploration (choose/explore/unchoose)
- **Merge / Heap / Partition Universe** → ordering + selection primitives

---

## 🧠 Kernel 1: `SubstringSlidingWindow` (Window State Machine)
- **Kernel summary**: 1D window with dynamic invariant; each element enters/exits ≤ 1 time ⇒ often $O(n)$
- ==Window strategies==
  - **Maximize**: expand R, shrink L *only when invalid*
  - **Minimize**: expand R until valid, shrink L *while valid*
  - **Fixed size**: maintain exact length `k`
- <!-- markmap: fold -->
- **Pattern comparison table 📚**
  - | Pattern | Invariant | State | Window | Goal | Anchor Problems |
    |---|---|---|---|---|---|
    | *unique* | all chars unique | last index map | variable | maximize | `[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)` |
    | *at_most_k_distinct* | distinct ≤ K | freq map | variable | maximize | `[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)` |
    | *freq_cover* | cover required counts | need/have + satisfied | variable | minimize/collect | `[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)`, `[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)`, `[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)` |
    | *cost_bounded* | sum ≥ target (or ≤ budget) | integer sum | variable | minimize/maximize | `[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)` |
- **Pattern: `sliding_window_unique`**
  - 🎯 invariant: “no duplicates in [L,R]”
  - trick: **jump-left** using last seen index (no `while` loop)
  - [ ] `[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)`
- **Pattern: `sliding_window_at_most_k_distinct`**
  - 🎯 invariant: “distinct count ≤ K”
  - state: `freq`, remove keys at 0
  - [ ] `[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)`
- **Pattern: `sliding_window_freq_cover`**
  - 🎯 invariant: “window satisfies all required frequencies”
  - two modes:
    - minimize window: `[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)`
    - fixed window exact match / collect positions: `[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)`, `[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)`
  - [ ] `[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)`
  - [ ] `[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)`
  - [ ] `[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)`
- **Pattern: `sliding_window_cost_bounded`**
  - 🎯 invariant: numeric constraint (often assumes positives for monotonic shrink)
  - [ ] `[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)`
- **Data structures you’ll feel**
  - `hash_map` / `counter`, sometimes arrays of size 26

---

## 🧭 Kernel 2: `TwoPointersTraversal` (Eliminate Search Space)
- **Kernel summary**: two indices move under a proof-based rule; once moved, never reconsidered
- **Sub-worlds**
  - **Opposite pointers** (two-end squeeze)
  - **Same-direction writer** (in-place filter/compact)
  - **Dedup enumeration** (sorted + skip duplicates)
- <!-- markmap: fold -->
- **Two pointers “shape” table**
  - | Shape | Init | Movement | Invariant | Typical Time | Anchor Problems |
    |---|---|---|---|---|---|
    | Opposite search | `l=0,r=n-1` | move based on comparison | answer inside [l,r] | $O(n)$ | `[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)`, `LeetCode 167` (related), `[LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)` |
    | Opposite maximize | `l=0,r=n-1` | move limiting side | best seen so far | $O(n)$ | `[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)` |
    | Same-direction writer | `write=0, read=0` | read always, write on keep | `a[0:write]` valid | $O(n)$ | `[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)`, `[LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)`, `[LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)`, `[LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)` |
    | Sorted tuple enum | outer i + inner l/r | skip duplicates | uniqueness by ordering | $O(n^2)$ | `[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)`, `[LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)` |
- **Pattern: `two_pointer_opposite`**
  - 🎯 invariant: sorted or monotonic structure ⇒ move pointer that can fix mismatch
  - [ ] `[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)` *(often hash map; but opposite-pointer variant when sorted / after sort)*
- **Pattern: `two_pointer_opposite_maximize`**
  - 🎯 invariant: moving the smaller side can only improve potential max
  - [ ] `[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)`
- **Pattern: `two_pointer_opposite_palindrome`**
  - 🎯 invariant: characters must mirror; skip non-alnum if needed
  - [ ] `[LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)`
  - [ ] `[LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)`
- **Pattern: `two_pointer_writer_dedup`**
  - 🎯 invariant: prefix `[0:write)` is deduped
  - [ ] `[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)`
  - [ ] `[LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)`
- **Pattern: `two_pointer_writer_remove`**
  - 🎯 invariant: prefix `[0:write)` contains kept elements
  - [ ] `[LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)`
- **Pattern: `two_pointer_writer_compact`**
  - 🎯 invariant: all non-zero moved forward; fill remainder
  - [ ] `[LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)`
- **Pattern: `two_pointer_three_sum`**
  - 🎯 invariant: fix i, then two-sum with l/r; dedup by skipping equals
  - [ ] `[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)`
  - [ ] `[LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)`

---

## 🧩 Kernel 3: `FastSlowPointers` (Cycle Physics)
- **Kernel summary**: Floyd’s algorithm; detect cycle + locate entry; $O(n)$ time, $O(1)$ space
- **Patterns**
  - `fast_slow_cycle_detect` → phase 1
    - [ ] `[LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)`
  - `fast_slow_cycle_start` → phase 2
    - [ ] `[LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)`
  - `fast_slow_midpoint`
    - [ ] `[LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)`
  - `fast_slow_implicit_cycle` (sequence defined by function)
    - [ ] `[LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)`
- ==Interview punchline==
  - “If there’s a loop, fast gains 1 step per iteration inside the cycle.”

---

## 🧱 Kernel 4: `BacktrackingExploration` (Reversible Search)
- **Kernel summary**: explore decision tree with **Choose → Explore → Unchoose**
- ==Golden invariant==
  - state == exactly the current path (no ghost marks)
- <!-- markmap: fold -->
- **Backtracking “decision tree shapes”**
  - **Permutation**: order matters → `used[]`
  - **Subset/Combination**: order doesn’t matter → `start_index`
  - **Target sum**: track `remaining`
  - **Constraint satisfaction**: constraint sets (cols/diagonals)
  - **Segmentation**: choose cut positions + validity
  - **Grid path**: visited marking + undo
- **Pattern: `backtracking_permutation`**
  - [ ] `[LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)`
  - [ ] `[LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)` *(sort + same-level dedup)*
- **Pattern: `backtracking_subset`**
  - [ ] `[LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)`
  - [ ] `[LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)` *(sort + same-level skip)*
- **Pattern: `backtracking_combination`**
  - [ ] `[LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)`
  - [ ] `[LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)` *(reuse allowed: recurse with `i`)*
  - [ ] `[LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)` *(no reuse: recurse with `i+1` + dedup)*
  - [ ] `[LeetCode 216 - Combination Sum III](https://leetcode.com/problems/combination-sum-iii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)` *(fixed size k + remaining sum)*
- **Pattern: `backtracking_n_queens`**
  - state: `used_cols`, `diag_main (r-c)`, `diag_anti (r+c)`
  - [ ] `[LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)`
  - [ ] `[LeetCode 52 - N-Queens II](https://leetcode.com/problems/n-queens-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)`
- **Pattern: `backtracking_string_segmentation`**
  - [ ] `[LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)` *(4 segments + bounds pruning)*
  - [ ] `[LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)` *(palindrome check; DP precompute optional)*
- **Pattern: `backtracking_grid_path`**
  - [ ] `[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)` *(mark cell, explore 4 dirs, unmark)*
- ==Pruning cheat codes==
  - sort + early break when `candidate > remaining`
  - feasibility bound: “not enough elements left to fill k”
  - segmentation bound: remaining chars ∈ [segments_left, 3*segments_left]

---

## 🔀 Kernel 5: `MergeSortedSequences` + `KWayMerge` (Ordering Pipelines)
- **Kernel summary**
  - merge-2: two pointers, $O(m+n)$
  - merge-k: heap ($O(N \log k)$) or divide&conquer ($O(N \log k)$ with better constants/cache)
- **Patterns**
  - `merge_two_sorted_lists`
    - [ ] `[LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)`
  - `merge_two_sorted_arrays`
    - [ ] `[LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)`
  - `merge_sorted_from_ends`
    - [ ] `[LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)`
  - `merge_k_sorted_heap` / `merge_k_sorted_divide`
    - [ ] `[LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)`
- ==Architect lens==
  - Heap merge = “online stream” friendly  
  - Divide&conquer merge = “batch + cache locality” friendly

---

## 🧨 Kernel 6: `TwoPointerPartition` (Partition as a Primitive)
- **Kernel summary**: in-place region partitioning; foundation for quickselect & Dutch flag
- **Patterns**
  - `dutch_flag_partition`
    - [ ] `[LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)`
  - `two_way_partition`
    - [ ] `[LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)`
    - [ ] `[LeetCode 922 - Sort Array By Parity II](https://leetcode.com/problems/sort-array-by-parity-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)`
  - `quickselect_partition`
    - pairs naturally with Top-K / Kth
- ==Complexities==
  - Partition pass: $O(n)$, $O(1)$ extra space

---

## 🏔️ Kernel 7: `HeapTopK` (Selection & Streaming)
- **Kernel summary**: keep best K using heap; or find kth element
- **Patterns**
  - `heap_kth_element`
    - [ ] `[LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)`
- ==Engineering note==
  - For large n, quickselect average $O(n)$; heap $O(n \log k)$ but stable & incremental

---

## 🌊 Kernel 8: `GridBFSMultiSource` (Wavefront Propagation)
- **Kernel summary**: multi-source BFS; shortest time/steps in unweighted grid
- **Pattern**
  - `grid_bfs_propagation`
    - [ ] `[LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)`
- ==Invariant==
  - queue holds the current frontier; each layer = +1 minute/step

---

## 🧪 “Combo Moves” (patterns that fuse)
- **Sliding Window + Hash Map**: `[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)`, `[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)`, `[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)`, `[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)`, `[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)`
- **Two Pointers + Sorting + Dedup**: `[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)`, `[LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)`
- **Partition + Heap/Quickselect**: `[LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)`
- **Backtracking + DP precompute**: `[LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)` (palindrome table)
- **Merge + Binary Search on answer**: `[LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)` (two sorted arrays median)

---

## 🧭 Micro-Roadmaps (fast, high-signal)
- **Sliding Window Mastery** (`sliding_window_path`)
  - [ ] `[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)` → [ ] `[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)` → [ ] `[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)` → [ ] `[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)` → [ ] `[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)` → [ ] `[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)`
- **Two Pointers Mastery** (`two_pointers_path`)
  - [ ] `[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)` → [ ] `[LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)` → [ ] `[LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)` → [ ] `[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)` → [ ] `[LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)` → [ ] `[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)`
- **Backtracking Core**
  - [ ] `[LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)` → [ ] `[LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)` → [ ] `[LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)` → [ ] `[LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)` → [ ] `[LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)` → [ ] `[LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)` → [ ] `[LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)`
- **BFS Wavefront**
  - [ ] `[LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)`

---

## ✅ Progress Board (printable)
- Sliding Window
  - [ ] `[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)`  [ ] `[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)`  [ ] `[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)`  [ ] `[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)`  [ ] `[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)`  [ ] `[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)`
- Two Pointers
  - [ ] `[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)` [ ] `[LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)` [ ] `[LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)`
  - [ ] `[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)` [ ] `[LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)` [ ] `[LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)` [ ] `[LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)`
  - [ ] `[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)` [ ] `[LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)`
- Fast–Slow
  - [ ] `[LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)` [ ] `[LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)` [ ] `[LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)` [ ] `[LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)`
- Backtracking
  - [ ] `[LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)` [ ] `[LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)` [ ] `[LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)` [ ] `[LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)`
  - [ ] `[LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)` [ ] `[LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)` [ ] `[LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)` [ ] `[LeetCode 216 - Combination Sum III](https://leetcode.com/problems/combination-sum-iii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)`
  - [ ] `[LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)` [ ] `[LeetCode 52 - N-Queens II](https://leetcode.com/problems/n-queens-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)` [ ] `[LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)` [ ] `[LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)` [ ] `[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)`
- Merge / Heap / Partition / BFS
  - [ ] `[LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)` [ ] `[LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)` [ ] `[LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)` [ ] `[LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)`
  - [ ] `[LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)`
  - [ ] `[LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)` [ ] `[LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)` [ ] `[LeetCode 922 - Sort Array By Parity II](https://leetcode.com/problems/sort-array-by-parity-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)`
  - [ ] `[LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)`
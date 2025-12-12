---
title: LeetCode Core Patterns Mind Map (From API Kernels → Patterns → Problems)
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 How to use this map (free-form, interview-friendly)
- **Read top-down**: *API Kernel* → *Pattern* → *Canonical problems*
- **Practice loop**: implement template → do 2–3 problems → refactor into reusable snippets
- **Progress tracker**
  - [ ] Do all Easy problems first
  - [ ] Then all Medium
  - [ ] Finally the Hard set + re-solve from scratch after 7 days

---

## 🧠 SubstringSlidingWindow (API Kernel)
- **Summary**: 1D window state machine with invariant-preserving expand/contract ($O(n)$ typical)
- **Core invariant mental model**
  - Expand `right` every step
  - Contract `left` only when invariant violated (maximize) or while invariant holds (minimize)

### ✅ Pattern: sliding_window_unique (all unique)
- **State**: last index map / set
- **Key trick**: ==jump left== using last seen index (no while-loop needed)
- Problems
  - [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)

### ✅ Pattern: sliding_window_at_most_k_distinct (≤ K distinct)
- **State**: frequency map + distinct counter
- **Key trick**: must contract with `while` (no jump)
- Problems
  - [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)

### ✅ Pattern: sliding_window_freq_cover (cover required frequencies)
- **State**: `need` + `have` + `formed/required`
- **Two modes**
  - *Minimize window* (classic “best shortest valid”)
  - *Fixed-size exact-match* (anagrams/permutation style)
- Problems
  - [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)

### ✅ Pattern: sliding_window_cost_bounded (sum/cost constraint)
- **State**: integer sum (often requires all-positive numbers for monotonic contraction)
- Problems
  - [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)

<!-- markmap: fold -->
### 📌 Sliding window comparison table
| Problem | Invariant | State | Window Size | Goal |
|---------|-----------|-------|-------------|------|
| [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | all unique | last seen | variable | maximize |
| [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | ≤K distinct | freq map | variable | maximize |
| [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | covers `t` | need/have | variable | minimize |
| [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | exact freq match | freq map | fixed | exists |
| [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | exact freq match | freq map | fixed | all positions |
| [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | sum ≥ target | integer sum | variable | minimize |

---

## 🧭 TwoPointersTraversal (API Kernel)
- **Summary**: two indices coordinated by a monotonic rule; usually $O(n)$ or $O(n^2)$ for enumeration
- **Subfamilies**: opposite pointers, writer pointers, dedup enumeration

### ✅ Pattern: two_pointer_opposite_maximize (optimize function)
- Problems
  - [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)

### ✅ Pattern: two_pointer_three_sum (sorted + dedup + inner opposite pointers)
- **Pre-step**: sort array
- **Dedup rule**: skip same `i`, then skip duplicates when moving `l/r`
- Problems
  - [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
  - [LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)

### ✅ Pattern: two_pointer_writer_dedup (in-place dedup)
- Problems
  - [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)

### ✅ Pattern: two_pointer_writer_remove (filter in-place)
- Problems
  - [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)

### ✅ Pattern: two_pointer_writer_compact (stable compaction)
- Problems
  - [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)

### ✅ Pattern: two_pointer_opposite_palindrome (symmetric check)
- Problems
  - [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)

---

## 🏎️ FastSlowPointers (API Kernel)
- **Summary**: Floyd cycle detection + midpoint on linked/implicit sequences
- **When**: cycle existence, cycle entry, “middle” without length

### ✅ Pattern: fast_slow_cycle_detect
- Problems
  - [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)

### ✅ Pattern: fast_slow_cycle_start
- Problems
  - [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)

### ✅ Pattern: fast_slow_midpoint
- Problems
  - [LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)

### ✅ Pattern: fast_slow_implicit_cycle (cycle on function f(x))
- Problems
  - [LeetCode 202 - Happy Number](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)

---

## 🧩 MergeSortedSequences (API Kernel)
- **Summary**: merge two sorted sequences with coordinated pointers ($O(m+n)$)

### ✅ Pattern: merge_two_sorted_lists
- Problems
  - [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)

### ✅ Pattern: merge_two_sorted_arrays
- **Production trick**: merge from end to do in-place
- Problems
  - [LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)

### ✅ Pattern: merge_sorted_from_ends (two-end merge after transform)
- Problems
  - [LeetCode 977 - Squares of a Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

---

## 🧺 KWayMerge (API Kernel)
- **Summary**: merge K sorted sequences via heap or divide-and-conquer

### ✅ Pattern: merge_k_sorted_heap
- **Complexity**: $O(N \log K)$ where $N$ total nodes/elements
- Problems
  - [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)

### ✅ Pattern: merge_k_sorted_divide
- **Complexity**: $O(N \log K)$, often faster constants than heap for linked lists
- Problems
  - [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)

---

## 🔀 TwoPointerPartition (API Kernel)
- **Summary**: in-place partitioning (2-way / 3-way) and selection

### ✅ Pattern: dutch_flag_partition (3-way)
- Problems
  - [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)

### ✅ Pattern: two_way_partition (binary property)
- Problems
  - [LeetCode 905 - Sort Array By Parity](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
  - [LeetCode 922 - Sort Array By Parity II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)

### ✅ Pattern: quickselect_partition (kth selection)
- Problems
  - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

---

## ⛰️ HeapTopK (API Kernel)
- **Summary**: maintain top-K / kth element using heap (predictable $O(n \log k)$)
- Patterns
  - heap_kth_element
- Problems
  - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

---

## ♻️ LinkedListInPlaceReversal (API Kernel)
- **Summary**: pointer surgery; isolate segment → reverse → reconnect

### ✅ Pattern: linked_list_k_group_reversal
- Problems
  - [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)

---

## 🧪 BacktrackingExploration (API Kernel)
- **Summary**: DFS over decision tree + pruning; correctness via exhaustive enumeration
- **Common pruning**: constraint sets, early stop, symmetry reduction

### ✅ Pattern: backtracking_n_queens
- Problems
  - [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)

---

## 🌊 GridBFSMultiSource (API Kernel)
- **Summary**: multi-source BFS wavefront; levels correspond to time/steps
- **Implementation invariant**: each cell enqueued once; track minutes by BFS layers

### ✅ Pattern: grid_bfs_propagation
- Problems
  - [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

---

## 🔍 BinarySearchBoundary + Merge (Hard combo)
- **When**: “find boundary / partition” in sorted structure, often with careful invariants

### ✅ Pattern: binary_search_on_answer + merge_two_sorted
- Problems
  - [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

---

## 📌 Minimal “starter set” (high ROI)
- Sliding Window
  - [ ] [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [ ] [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - [ ] [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
- Two Pointers
  - [ ] [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ] [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
- BFS
  - [ ] [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- Backtracking
  - [ ] [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
- Heap/Quickselect
  - [ ] [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
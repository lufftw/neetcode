---
title: LeetCode Knowledge Graph Mind Map (45 Problems) — Kernels → Patterns → Problems
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

# 🎯 LeetCode Master Map: Kernels → Patterns → Problems
- **How to use**
  - Start from an **API Kernel** (reusable “engine”), learn its **invariants**, then grind the mapped problems.
  - Track progress: do *1–2 problems per sub-pattern*, then mix across kernels.
- **Progress tracker**
  - [ ] Sliding Window (SubstringSlidingWindow)
  - [ ] Two Pointers (Traversal + Partition + Fast/Slow)
  - [ ] Backtracking (Exploration)
  - [ ] Merge (Two-way + K-way)
  - [ ] Binary Search (Boundary / Answer)
  - [ ] Heap Top K / Kth
  - [ ] Grid Multi-Source BFS

---

## ⚡ API Kernel: `SubstringSlidingWindow` (Window state machine)
- **Core invariant**: maintain a window `[L..R]` that is *valid* under a rule; expand `R`, shrink `L` to restore validity
- **Complexity**: typically $O(n)$ time, $O(\Sigma)$ space (alphabet / frequency map)
- **Patterns**
  - **Unique window** (`sliding_window_unique`) — maximize
    - [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - **At most K distinct** (`sliding_window_at_most_k_distinct`) — maximize
    - [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - **Frequency cover / exact match** (`sliding_window_freq_cover`) — minimize/exists/all
    - [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
    - [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
    - [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - **Cost bounded / sum constraint** (`sliding_window_cost_bounded`) — minimize
    - [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)

- **Comparison table (mental model)**
  - | Problem | Invariant | State | Window | Goal |
    |---|---|---|---|---|
    | [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | all unique | last index / set | variable | max |
    | [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | ≤K distinct | freq map | variable | max |
    | [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | covers `t` | need/have | variable | min |
    | [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | exact multiset | freq + matches | fixed | exists |
    | [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | exact multiset | freq + matches | fixed | all |
    | [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | sum ≥ target | integer sum | variable | min |

<!-- markmap: fold -->
- **Template (universal)**
```python
left = 0
state = init()
ans = init_ans()

for right, x in enumerate(seq):
    add(state, x)
    while invariant_violated(state):
        remove(state, seq[left])
        left += 1
    ans = update(ans, left, right, state)
```

---

## ⚡ API Kernel: `TwoPointersTraversal` (Coordinated pointer movement)
- **Core invariant**: pointers move monotonically; each move **eliminates** candidates permanently
- **Patterns**
  - **Opposite pointers: maximize function** (`two_pointer_opposite_maximize`)
    - [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - **Opposite pointers: palindrome validation** (`two_pointer_opposite_palindrome`)
    - [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
    - [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
  - **Dedup enumeration (sorted + skip): 3Sum** (`two_pointer_three_sum`)
    - [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
    - [LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - **Writer patterns (in-place)**  
    - Deduplicate (`two_pointer_writer_dedup`)
      - [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
      - [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
    - Remove (`two_pointer_writer_remove`)
      - [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
    - Compact (`two_pointer_writer_compact`)
      - [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)

- **Key table (choose the right sub-pattern)**
  - | Sub-pattern | When it applies | Typical invariant | Example |
    |---|---|---|---|
    | Opposite pointers | sorted / symmetric / 2-end optimization | solution lies in `[L,R]` | [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) |
    | Writer | in-place filter/dedup | `arr[:write]` is “kept” | [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py) |
    | Dedup enum | k-sum family (sort + skip) | skip duplicates at same role | [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py) |

---

## ⚡ API Kernel: `FastSlowPointers` (Floyd / midpoint / implicit cycles)
- **Core invariant**: fast moves 2×, slow moves 1×; if a cycle exists they meet
- **Patterns**
  - Cycle detect (`fast_slow_cycle_detect`)
    - [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - Cycle start (`fast_slow_cycle_start`)
    - [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - Midpoint (`fast_slow_midpoint`)
    - [LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
  - Implicit cycle (`fast_slow_implicit_cycle`)
    - [LeetCode 202 - Happy Number](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)

---

## ⚡ API Kernel: `TwoPointerPartition` (Partitioning / selection)
- **Core invariant**: maintain regions (e.g., `< pivot`, `= pivot`, `> pivot`)
- **Patterns**
  - Dutch flag (`dutch_flag_partition`)
    - [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
  - Two-way partition (`two_way_partition`)
    - [LeetCode 905 - Sort Array By Parity](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
    - [LeetCode 922 - Sort Array By Parity II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
  - Quickselect partition (`quickselect_partition`)
    - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

---

## ⚡ API Kernel: `MergeSortedSequences` (Two-way merge)
- **Core invariant**: pointers `i,j` always point to next unmerged element in each sorted sequence
- **Patterns**
  - Merge two sorted lists (`merge_two_sorted_lists`)
    - [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - Merge two sorted arrays (`merge_two_sorted_arrays`)
    - [LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - Merge from ends (`merge_sorted_from_ends`)
    - [LeetCode 977 - Squares of a Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

---

## ⚡ API Kernel: `KWayMerge` (K sorted sequences)
- **Two production-grade strategies**
  - **Min-heap** (`merge_k_sorted_heap`) — $O(N \log K)$, great when K is large and lists are uneven
  - **Divide & conquer** (`merge_k_sorted_divide`) — $O(N \log K)$, often faster constants + simpler memory behavior
- **Problems**
  - [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - Cross-kernel hybrid (merge + binary search on partition)
    - [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

---

## ⚡ API Kernel: `BinarySearchBoundary` (Boundary + answer space)
- **Core invariant**: predicate is monotone; binary search finds **first/last true**
- **Patterns**
  - Binary search on answer (`binary_search_on_answer`)
    - [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

---

## ⚡ API Kernel: `HeapTopK` (Top-K / Kth / streaming)
- **Core invariant**: heap maintains the current best candidates (size K or two-heaps for median)
- **Patterns**
  - Kth element (`heap_kth_element`)
    - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

---

## ⚡ API Kernel: `LinkedListInPlaceReversal` (Pointer surgery)
- **Core invariant**: maintain `prev/curr/next` and reconnect boundaries correctly
- **Patterns**
  - Reverse in k-group (`linked_list_k_group_reversal`)
    - [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- **Related (same family, different operation)**
  - Arithmetic on lists
    - [LeetCode 2 - Add Two Numbers](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py)

---

## ⚡ API Kernel: `BacktrackingExploration` (Choose → Explore → Unchoose)
- ==Core invariant==: **state exactly matches the current path** (no “ghost marks” after backtrack)
- **Complexity**: usually exponential / factorial; aim for pruning + dedup
- **Sub-patterns → problems**
  - **Permutations**
    - [LeetCode 46 - Permutations](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
    - [LeetCode 47 - Permutations II](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py) *(sort + same-level skip)*
  - **Subsets**
    - [LeetCode 78 - Subsets](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
    - [LeetCode 90 - Subsets II](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py) *(sort + same-level skip)*
  - **Combinations / target search**
    - [LeetCode 77 - Combinations](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
    - [LeetCode 39 - Combination Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) *(reuse allowed)*
    - [LeetCode 40 - Combination Sum II](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py) *(no reuse + dedup)*
    - [LeetCode 216 - Combination Sum III](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py) *(fixed count + fixed sum)*
  - **Constraint satisfaction**
    - [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
    - [LeetCode 52 - N-Queens II](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
  - **String segmentation**
    - [LeetCode 93 - Restore IP Addresses](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)
    - [LeetCode 131 - Palindrome Partitioning](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
  - **Grid path search**
    - [LeetCode 79 - Word Search](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

<!-- markmap: fold -->
- **Dedup cheat sheet**
  - Sort + same-level skip (subsets/combos):
```python
if i > start and nums[i] == nums[i-1]:
    continue
```
  - Sort + used[] constraint (permutations):
```python
if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
    continue
```

---

## ⚡ API Kernel: `GridBFSMultiSource` (Wavefront BFS)
- **Core invariant**: BFS level = shortest time/steps from nearest source
- **Pattern**
  - Grid propagation (`grid_bfs_propagation`)
    - [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

---

## 🧭 Roadmap Slices (from your data)
- **NeetCode 150 anchors (high ROI)**
  - Sliding window: [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py), [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py), [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
  - Two pointers: [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py), [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py), [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - Backtracking: [LeetCode 39 - Combination Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py), [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - Graph BFS: [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
  - Heap/selection: [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

---

## 🏁 “What next?” Mini Paths
- **Sliding Window Mastery (in order)**
  - [ ] [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [ ] [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - [ ] [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - [ ] [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
  - [ ] [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - [ ] [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)

- **Backtracking Mastery (in order)**
  - [ ] [LeetCode 78 - Subsets](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
  - [ ] [LeetCode 90 - Subsets II](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)
  - [ ] [LeetCode 46 - Permutations](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
  - [ ] [LeetCode 47 - Permutations II](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)
  - [ ] [LeetCode 39 - Combination Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
  - [ ] [LeetCode 40 - Combination Sum II](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)
  - [ ] [LeetCode 131 - Palindrome Partitioning](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
  - [ ] [LeetCode 79 - Word Search](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)
  - [ ] [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)

- **Two Pointers Mastery (in order)**
  - [ ] [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [ ] [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - [ ] [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
  - [ ] [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ] [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
  - [ ] [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - [ ] [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
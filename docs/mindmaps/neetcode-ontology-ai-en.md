---
title: LeetCode Core Patterns Mind Map (API Kernels → Patterns → Problems)
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 How to use this map (fast)
- **Start from API Kernels** → pick a pattern → solve the mapped problems
- Keep one invariant per pattern: **expand** (add right / go deeper) then **contract** (move left / undo)
- Progress tracking
  - [ ] Finish all **Easy** anchors
  - [ ] Finish all **Medium** anchors
  - [ ] Finish at least 3 **Hard** anchors

## 🧠 Big Picture: From Technique → Kernel → Pattern → Problem
- **Technique** (e.g., *Two Pointers*)  
  - **API Kernel** (reusable “engine”, e.g., `SubstringSlidingWindow`)  
    - **Pattern** (invariant + state)  
      - **LeetCode {number}** (practice + recognition)

---

## 🪟 SubstringSlidingWindow (API Kernel)
- **Summary**: 1D window state machine over sequences with dynamic invariants  
- **Cost model**: each element enters/exits window ≤ 1 time ⇒ typically $O(n)$
- **State toolbelt**: `hash_map` / `counter`, sometimes integer sum

<!-- markmap: fold -->
### ✅ Pattern comparison table (must-know)
| Problem | Invariant | State | Window Size | Goal |
|---------|-----------|-------|-------------|------|
|[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | all unique | `last_index` map | variable | maximize |
|[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | ≤ K distinct | freq map | variable | maximize |
|[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | covers all of `t` | need/have maps | variable | minimize |
|[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | exact multiset match | freq + matched count | fixed | exists |
|[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | exact multiset match | freq + matched count | fixed | all positions |
|[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | sum ≥ target | integer sum | variable | minimize |

### sliding_window_unique
- **Invariant**: ==no duplicates in window==
- **State**: `last_seen_index[char]` (jump-left optimization)
- **Anchor problems**
  - [ ][LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)

### sliding_window_at_most_k_distinct
- **Invariant**: ==distinct_count ≤ K==
- **State**: frequency `hash_map`, maintain `len(map)`
- **Anchor problems**
  - [ ][LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)

### sliding_window_freq_cover
- **Invariant**: ==window meets required frequencies==
- **State**: `need_frequency`, `have_frequency`, `chars_satisfied`
- **Two flavors**
  - *Minimize while valid* → classic “cover”
    - [ ][LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
    - [ ][LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)[ ][LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)

### sliding_window_cost_bounded
- **Invariant**: ==sum/cost constraint satisfied==
- **State**: integer `window_sum`
- **Anchor problems**
  - [ ][LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)

## 👈👉 TwoPointersTraversal (API Kernel)
- **Summary**: traverse with two coordinated pointers under invariant-preserving rules
- **Core promise**: every pointer move *eliminates* possibilities (monotonic reasoning)

<!-- markmap: fold -->
### ✅ Two pointers pattern comparison table
| Pattern | Init | Movement | Typical invariant | Time | Space |
|--------|------|----------|-------------------|------|-------|
| Opposite | `0, n-1` | toward center | solution lies within [L,R] | $O(n)$ | $O(1)$ |
| Writer | `write=0, read=0` | both forward | `a[0:write]` is “kept” | $O(n)$ | $O(1)$ |
| Dedup enumeration | `i + (L,R)` | nested + skips | unique tuples only | $O(n^2)$ | $O(1)$ |

### two_pointer_opposite_maximize
- **Goal**: maximize a function while shrinking search space
- **Anchor problems**
  - [ ][LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)

### two_pointer_three_sum (dedup enumeration)
- **Recipe**: sort → fix `i` → opposite pointers → skip duplicates
- **Anchor problems**
  - [ ][LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)[ ][LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)

### two_pointer_writer_dedup (same-direction)
- **Invariant**: `arr[0:write)` is deduplicated
- **Anchor problems**
  - [ ][LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)[ ][LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)

### two_pointer_writer_remove (same-direction)
- **Invariant**: `arr[0:write)` contains all kept elements
- **Anchor problems**
  - [ ][LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)

### two_pointer_writer_compact (same-direction)
- **Use case**: stable compaction (e.g., move zeros)
- **Anchor problems**
  - [ ][LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)

### two_pointer_opposite_palindrome
- **Invariant**: characters checked so far match palindrome rule
- **Anchor problems**
  - [ ][LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)[ ][LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)

## 🐢🐇 FastSlowPointers (API Kernel)
- **Summary**: two pointers at different speeds for cycle detection / midpoint
- **Key theorem**: if a cycle exists, fast meets slow in $O(n)$

### fast_slow_cycle_detect
- [ ][LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)

### fast_slow_cycle_start
- **Phase 2**: reset one pointer to head, move both at speed 1
- [ ][LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)

### fast_slow_implicit_cycle
- **Implicit graph**: next(x) defines edges
- [ ][LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)

### fast_slow_midpoint
- **Use**: split list / find middle
- [ ][LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)

## 🔀 MergeSortedSequences (API Kernel)
- **Summary**: merge two sorted sequences using two pointers
- **When it wins**: stable linear merge, $O(m+n)$

### merge_two_sorted_lists
- [ ][LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)

### merge_two_sorted_arrays
- [ ][LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)

### merge_sorted_from_ends
- **Trick**: compare from ends to avoid extra space / handle transforms (squares)
- [ ][LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

## 🧺 KWayMerge (API Kernel)
- **Summary**: merge K sorted sequences using heap or divide-and-conquer
- **Two standard strategies**
  - **Min-heap**: push heads, pop+advance ⇒ $O(N \log K)$
  - **Divide & conquer**: pairwise merge ⇒ $O(N \log K)$

### merge_k_sorted_heap
- [ ][LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)

### merge_k_sorted_divide
- [ ][LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)

### merge_two_sorted (also appears in answer-space problems)
- [ ][LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

## 🧱 TwoPointerPartition (API Kernel)
- **Summary**: partition array using two pointers (Dutch flag, quickselect)

### dutch_flag_partition
- **Regions**: `< pivot | = pivot | unknown | > pivot`
- [ ][LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)

### two_way_partition
- **Binary predicate**: even/odd, etc.
- [ ][LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)[ ][LeetCode 922 - Sort Array By Parity II](https://leetcode.com/problems/sort-array-by-parity-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)

### quickselect_partition
- **Goal**: kth element without full sort (avg $O(n)$)
- [ ][LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

## 🏔️ HeapTopK (API Kernel)
- **Summary**: maintain top K / kth using heap
- **Rule of thumb**
  - `min_heap` of size K for **top K largest**
  - `max_heap` of size K for **top K smallest**
- **Anchor problems**
  - [ ][LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

## 🧭 BacktrackingExploration (API Kernel)
- **Summary**: exhaustive search with pruning; rhythm: **Choose → Explore → Unchoose**
- **Invariant**: ==state matches current path exactly==

<!-- markmap: fold -->
### ✅ Backtracking “shape” cheat sheet
| Shape | What you track | Canonical trick | Anchor |
|------|-----------------|-----------------|--------|
| Permutation | `used[]` | each element once |[LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py) |
| Permutation + dup | `used[]` + sort | skip if prev unused |[LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py) |
| Subset | `start_index` | collect every node |[LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py) |
| Subset + dup | `start_index` + sort | same-level skip |[LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py) |
| Combination | `start_index` + size | stop when size==k |[LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py) |
| Target sum | `remaining` | prune remaining<0 |[LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)/40/216 |
| Constraint sat. | constraint sets | propagate constraints |[LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)/52 |
| Grid path | visited mark | undo on return |[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py) |
| String cuts | cut positions | validate segment |[LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)/131 |

### backtracking_permutation
- [ ][LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)

### backtracking_permutation_dedup
- [ ][LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)

### backtracking_subset
- [ ][LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)

### backtracking_subset_dedup
- [ ][LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)

### backtracking_combination
- **Fixed size k**
  - [ ][LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
  - [ ][LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)[ ][LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)[ ][LeetCode 216 - Combination Sum III](https://leetcode.com/problems/combination-sum-iii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)

### backtracking_n_queens (constraint satisfaction)
- **Constraints**: cols, diag (row-col), anti-diag (row+col)
- [ ][LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)[ ][LeetCode 52 - N-Queens II](https://leetcode.com/problems/n-queens-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)

### backtracking_grid_path
- **Visited marking**: in-place `'#'` or `set()`
- [ ][LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

### backtracking_string_segmentation
- **Segment validity + pruning by remaining length**
- [ ][LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)[ ][LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)

## 🌊 GridBFSMultiSource (API Kernel)
- **Summary**: multi-source BFS wavefront propagation on grid graph
- **Invariant**: first time visiting a cell is shortest time (unweighted)
- **State**: `queue`, visited, distance/time layers

### grid_bfs_propagation
- [ ][LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

## 🔎 BinarySearchBoundary (API Kernel)
- **Summary**: boundary binary search (first true / last true) + answer-space search
- **When it fits**: predicate is monotone over index or value space

### binary_search_on_answer
- [ ][LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

## 🧩 “Starter Packs” (pick one roadmap slice)
- 🎯 **Sliding Window Mastery**
  - [ ][LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) → [ ][LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) → [ ][LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) → [ ][LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) → [ ][LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) → [ ][LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - [ ][LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py) → [ ][LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py) → [ ][LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) → [ ][LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) → [ ][LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py) → [ ][LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
  - [ ][LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py) → [ ][LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py) → [ ][LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py) → [ ][LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) → [ ][LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py) → [ ][LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - [ ][LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py) → [ ][LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py) → [ ][LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py) → [ ][LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py) → [ ][LeetCode 25 - Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
  - [ ][LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) → [ ][LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py) → [ ][LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
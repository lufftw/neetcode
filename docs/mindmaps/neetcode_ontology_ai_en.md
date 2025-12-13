---
title: Two Pointers & Sliding Window Integration Atlas
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

# Two Pointers & Sliding Window Integration Atlas
- 🌐 **Unified Pattern DNA**
  - 🔁 **SubstringSlidingWindow API Kernel**
    - ==Invariant Engine==: Maintain window `[L, R]` with dynamically checked constraints
    - Complexity: $O(n)$ time, $O(\Sigma)$ space using hash-based state
    - Pattern Portfolio
      - 🎯 **Uniqueness Maximization** → [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) *Difficulty: ==Medium (orange)==*
      - 🎯 **Distinct Budget Control** → [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
      - 🎯 **Frequency Coverage** → [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py), [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py), [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
      - 🎯 **Cost-Bounded Minimization** → [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
  - ⚖️ **TwoPointersTraversal API Kernel**
    - ==Invariant Engine==: Maintain pointer ordering/symmetry to prune search
    - Complexity: Typically $O(n)$ time, $O(1)$ space (sorting pre-processing may add $O(n \log n)$)
    - Pattern Portfolio
      - 🔄 **Opposite Pointers Optimization** → [LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py), [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py), [LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py), [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py), [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
      - 🛠️ **Same-Direction Writer Patterns** → [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py), [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py), [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py), [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
      - 🐢🐇 **Fast–Slow Pointers** → [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py), [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py), [LeetCode 202 - Happy Number](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py), [LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
      - 🎨 **Partition & Merge** → [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py), [LeetCode 905 - Sort Array By Parity](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py), [LeetCode 922 - Sort Array By Parity II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py), [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py), [LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py), [LeetCode 977 - Squares of a Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)
- 📊 **Strategy Decision Matrix**
  - Sliding Window & Two Pointers Comparison Table
    - | Problem | Pattern | Invariant Guardrail | Goal Metric | Complexity |
      |---------|---------|---------------------|-------------|------------|
      | [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | sliding_window_unique | No duplicate chars in window | Max length | $O(n)$ |
      | [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | sliding_window_freq_cover | `have >= need` for all chars | Min length | $O(n+m)$ |
      | [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | sliding_window_cost_bounded | Window sum ≥ target | Min length | $O(n)$ |
      | [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) | two_pointer_opposite_maximize | Shrink side with shorter wall | Max area | $O(n)$ |
      | [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py) | two_pointer_three_sum | Skip duplicates, adjust sum | All zero triplets | $O(n^2)$ |
      | [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py) | two_pointer_writer_dedup | `nums[:write]` deduped | In-place compaction | $O(n)$ |
- 🧠 **Conceptual Bridges**
  - Prefix Sum ↔ Sliding Window: When invariants break (negative numbers), pivot to prefix hash (see [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) vs binary search alternative)
  - HeapTopK vs TwoPointersTraversal: prefer heap for streaming selection ([LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)) when array unsorted and not easily partitioned
  - Union-Find & BFS synergy: wavefront ([LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)) vs connectivity queries (UnionFindConnectivity API kernel)
  - Data Structure Alignment
    - Hash Map / Counter → maintain sliding window state
    - Arrays → pointer-friendly contiguous operations
    - Linked Lists → fast–slow pointer domain; watch for null guards
- 🧪 **Implementation Snapshots**
  - <!-- markmap: fold -->
    ```python
    def two_pointer_palindrome_check(s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            # Skip non-alphanumeric characters
            if not s[left].isalnum():
                left += 1
                continue
            if not s[right].isalnum():
                right -= 1
                continue
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True
    ```
    - Applied in [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py); tweak skip logic to allow single deletion for [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
- 🗺️ **Adaptive Learning Path**
  - 📚 Roadmap Alignment
    - [x] `Blind 75` → foundational coverage: [LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py), [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
    - [ ] `Sliding Window Mastery Path` → progress after finishing [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
    - [ ] `Two Pointers Mastery Path` → focus on writer & partition drills: [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py), [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
  - Difficulty Staircase
    - **Easy → Medium**: Start with [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py) ➜ [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
    - **Medium → Hard**: Graduate from [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) ➜ [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) ➜ integrate binary search hybrid in [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
- 💼 **Interview Power-Ups**
  - High-frequency companies requesting these patterns: Google, Amazon, Meta, Microsoft, Apple, Bloomberg, Uber
  - Behavioral angle: articulate invariants & failure modes (e.g., why sliding window fails with negative numbers) to impress interviewers
  - Mock interview drill pairing:
    - Sliding Window + Hash Map: [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
    - Two Pointers + Sorting: [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
    - Fast–Slow pointers narrative: illustrate with [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
- 🤝 **Community & Contribution Hooks**
  - Open-source snippet opportunities: expand pattern snippet library for edge-case visualizations
  - Documentation gaps to fill:
    - [ ] Add monotonic queue exemplar for sliding window max
    - [ ] Provide animation walkthrough for [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
    - [ ] Cross-link BFS wavefront article with [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- 🔍 **Debugging & Edge-Case Checklist**
  - 🧊 Sliding Window
    - Ensure contraction loop updates state before moving `left`
    - Guard for empty target strings (e.g., `t == ""` in [LeetCode 76](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py))
  - 🔥 Two Pointers
    - Confirm sorted precondition before applying opposite pointers (sort in-place or copy?)
    - Watch for overflow when computing midpoints in linked list cycle detection (fast pointer null checks)
- 📈 **Metrics & Practice Cadence**
  - Track elapsed time per attempt; target reductions:
    - [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) → sub 15 minutes
    - [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py) → sub 10 minutes
    - [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) → sub 25 minutes with tests
  - Alternate daily focus: 🧠 Theory (proof of correctness) ↔ 💻 Implementation ↔ 🧪 Edge cases
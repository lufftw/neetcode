---
title: Problem Family Derivation - Base Templates → Variants
markmap:
  colorFreezeLevel: 2
  maxWidth: 400
---

# Problem Family Derivation

Base template problems and their derived variants. Learn the base pattern first,
then apply to variants with small modifications.

## SubstringSlidingWindow

### 🎯 Base Template: [LeetCode 3 - Longest Substring Without Repeating Characters](../../solutions/0003_longest_substring_without_repeating_characters.py)

> Canonical sliding window template with last-seen index array. Uses jump optimization instead of while-loop contraction. This is the BASE TEMPLATE for all SubstringSlidingWindow problems.

### Derived Problems

- 🔴 [LeetCode 76 - Minimum Window Substring](../../solutions/0076_minimum_window_substring.py) — `O(|s| + |t|) time, O(|t|) space`
- LeetCode 0159 *(metadata not yet added)*
- 🟡 [LeetCode 209 - Minimum Size Subarray Sum](../../solutions/0209_minimum_size_subarray_sum.py) — `O(n) time, O(1) space`
- 🟡 [LeetCode 340 - Longest Substring with At Most K Distinct Characters](../../solutions/0340_longest_substring_with_at_most_k_distinct.py) — `O(n) time, O(K) space`
- 🟡 [LeetCode 438 - Find All Anagrams in a String](../../solutions/0438_find_all_anagrams_in_a_string.py) — `O(|s| + |p|) time, O(1) space for maps, O(k) for output`
- 🟡 [LeetCode 567 - Permutation in String](../../solutions/0567_permutation_in_string.py) — `O(|s1| + |s2|) time, O(1) space`

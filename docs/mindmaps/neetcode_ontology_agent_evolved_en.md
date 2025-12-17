---
title: LeetCode Knowledge Graph Mind Map (Core Patterns → API Kernels → Problems) 🎯
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## How to use this map 📚
- **Goal**: learn *transferable kernels* (APIs) → recognize *patterns* → solve *problems*
- **Definitions**
  - **Kernel** = reusable code template / API
  - **Pattern** = invariant + state choices (specialization of a kernel)
  - **Family** = group of problems sharing pattern(s)
- **Progress tracker**
  - [ ] Do 1 problem per kernel (breadth)
  - [ ] Do 3 problems per kernel (depth)
  - [ ] Re-solve “anchor” problems from scratch under 20 minutes ⚡

## Router (Decision Guide) 🧭
- Contiguous substring/subarray with constraint → **SubstringSlidingWindow**
- Sorted array + monotonic objective / symmetric property → **TwoPointersTraversal**
- In-place reordering into buckets/regions → **TwoPointerPartition**
- “Minimum time/steps” on unweighted grid/graph → **GridBFSMultiSource** (or TreeTraversalBFS)
- “Kth/topK/median/streaming” → **HeapTopK** / **KWayMerge**
- Monotone feasibility in answer space / boundary index → **BinarySearchBoundary**
- Need counts over ranges / subarray sum targets → **PrefixSumRangeQuery**
- Next greater/smaller / histogram areas → **MonotonicStack**
- Connectivity / components → **UnionFindConnectivity**
- Hierarchical structure traversal → **TreeTraversalDFS/BFS**
- DAG prerequisites → **TopologicalSort**
- Optimal substructure on sequences/intervals → **DPSequence/DPInterval**

## Legend (priority tags) 🧾
- 🔥 must-know
- ⭐ common
- 🧊 nice-to-know

## Kernel Index (the “APIs” you should internalize) 🔥
- PrefixSumRangeQuery
- TwoPointersTraversal
- SubstringSlidingWindow
- BinarySearchBoundary
- TreeTraversalDFS + TreeTraversalBFS
- GridBFSMultiSource
- HeapTopK
- MonotonicStack
- MergeSortedSequences + KWayMerge
- BacktrackingExploration
- TwoPointerPartition
- FastSlowPointers
- UnionFindConnectivity
- TopologicalSort
- DPSequence + DPInterval
- TriePrefixSearch *(in ontology; not anchored by provided problems)*

---

## Pitfalls & Checklists (reusable) ✅
- **Sliding window**
  - Off-by-one: inclusive `[L..R]` vs half-open `[L, R)`; update answer after making window valid
  - Validity must be maintainable in $O(1)$ per move (avoid rescanning maps/alphabets each step)
  - “Shrink while valid” requires monotonicity (e.g., sums need non-negative numbers)
- **Two pointers / partition**
  - Termination: `while L < R` vs `<=`; ensure progress on every branch
  - Duplicates handling: skip duplicates at the correct pointer(s) and at the correct time
  - Stability: reader/writer compaction is stable; swap-based partition is usually unstable
- **Binary search**
  - Use a **half-open invariant** (`[lo, hi)`) and avoid infinite loops (`mid = lo + (hi-lo)//2`)
  - Pick `first_true` vs `last_true` intentionally; confirm predicate monotonicity
  - Overflow/sentinels: boundaries around `mid-1`, `mid+1`, empty arrays
- **BFS**
  - Mark visited **upon enqueue** to avoid multiple enqueues
  - Level counting: process BFS in layers when “minutes/steps” are required
  - Multi-source init: enqueue all sources before BFS loop; track remaining targets
- **Backtracking**
  - “Unchoose” is mandatory (no ghost marks): undo every mutation on return
  - Pruning must be safe (don’t prune on partial info that could be fixed later)
  - Copy vs mutate: avoid copying full paths unless needed (push/pop pattern)
- **Linked list**
  - Use a dummy head to simplify head changes
  - Preserve `next` pointers before rewiring
  - Group boundaries: confirm there are `k` nodes before reversing k-group
- **Quickselect / heaps**
  - Quickselect worst-case $O(n^2)$ unless randomized/median-of-medians
  - Duplicates: 3-way partition can simplify handling repeated pivot values
  - Streaming/large input: heap often preferred

---

## Reverse Index (Problem → Kernel → Pattern → invariant) 🔎
- 🔥 [LeetCode 1](https://leetcode.com/problems/two-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)(hash map complement) → `hash_map_complement` → “store seen value→index; look for target-x”
- 🔥 [LeetCode 2](https://leetcode.com/problems/add-two-numbers/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py)
- 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- 🧊 [LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
- ⭐ [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- 🧊 [LeetCode 16](https://leetcode.com/problems/3sum-closest/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
- 🔥 [LeetCode 21](https://leetcode.com/problems/merge-two-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
- 🔥 [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
- ⭐ [LeetCode 25](https://leetcode.com/problems/reverse-nodes-in-k-group/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- ⭐ [LeetCode 26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)[0:write]` kept unique”
- ⭐ [LeetCode 27](https://leetcode.com/problems/remove-element/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
- ⭐ [LeetCode 39](https://leetcode.com/problems/combination-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
- ⭐ [LeetCode 40](https://leetcode.com/problems/combination-sum-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)
- ⭐ [LeetCode 46](https://leetcode.com/problems/permutations/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)[]; choose unused”
- 🧊 [LeetCode 47](https://leetcode.com/problems/permutations-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)
- ⭐ [LeetCode 51](https://leetcode.com/problems/n-queens/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
- 🧊 [LeetCode 52](https://leetcode.com/problems/n-queens-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
- 🔥 [LeetCode 75](https://leetcode.com/problems/sort-colors/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
- 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
- ⭐ [LeetCode 77](https://leetcode.com/problems/combinations/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
- ⭐ [LeetCode 78](https://leetcode.com/problems/subsets/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
- ⭐ [LeetCode 79](https://leetcode.com/problems/word-search/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)
- 🧊 [LeetCode 80](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
- ⭐ [LeetCode 88](https://leetcode.com/problems/merge-sorted-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
- 🧊 [LeetCode 90](https://leetcode.com/problems/subsets-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)
- 🧊 [LeetCode 93](https://leetcode.com/problems/restore-ip-addresses/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)
- ⭐ [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
- ⭐ [LeetCode 131](https://leetcode.com/problems/palindrome-partitioning/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
- ⭐ [LeetCode 141](https://leetcode.com/problems/linked-list-cycle/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
- ⭐ [LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
- ⭐ [LeetCode 202](https://leetcode.com/problems/happy-number/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)(n); detect cycle”
- ⭐ [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
- 🔥 [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
- 🧊 [LeetCode 216](https://leetcode.com/problems/combination-sum-iii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)
- ⭐ [LeetCode 283](https://leetcode.com/problems/move-zeroes/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
- 🧊 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
- ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
- ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
- ⭐ [LeetCode 680](https://leetcode.com/problems/valid-palindrome-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
- ⭐ [LeetCode 876](https://leetcode.com/problems/middle-of-the-linked-list/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
- ⭐ [LeetCode 905](https://leetcode.com/problems/sort-array-by-parity/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
- 🧊 [LeetCode 922](https://leetcode.com/problems/sort-array-by-parity-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
- ⭐ [LeetCode 977](https://leetcode.com/problems/squares-of-a-sorted-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)
- 🔥 [LeetCode 994](https://leetcode.com/problems/rotting-oranges/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

---

## 1) Hashing + Prefix Sum (PrefixSumRangeQuery) 🧮
- **Where you’ll see this at work**
  - Counting events in logs; frequency tables; de-dup; “have we seen this key?”
  - Subarray analytics with running totals; anomaly detection with deltas
- **Kernel mini-spec**
  - **Signature**: sequence `nums`; queries like “count subarrays meeting condition” / “range aggregate”; output integer/count/array
  - **Required invariant**: maintain prefix aggregate `pref[i]` and a map of seen prefix states; use identities like `pref[j]-pref[i]=target`
  - **State model**: running prefix value; `hash_map` from prefix value → count (or earliest index)
  - **Complexity envelope**: typically $O(n)$ time, $O(n)$ space (hash map); $O(1)$ per step expected
  - **Failure modes / when NOT to use**: floating-point prefixes; hash collisions (theoretical); for min/max over window prefer sliding window/monotonic deque
- **Complexity template**
  - Time $O(n)$ expected; space $O(n)$ for prefix map (or $O(1)$ if only a few aggregates kept)
- **Patterns**
  - **Hash map complement lookup** (`hash_map_complement`)
    - Anchor: 🔥 [LeetCode 1](https://leetcode.com/problems/two-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
    - Template
      - ```text
        seen = map()  // value -> index
        for i in [0..n-1]:
          x = nums[i]
          y = target - x
          if y in seen:
            return [seen[y], i]
          seen[x] = i
        return none
        ```
  - **Prefix sum + hash map counts** (`prefix_sum_subarray_sum`)
    - Anchor: 🔥 [LeetCode 560](https://leetcode.com/problems/subarray-sum-equals-k/description/)(not in provided solutions list)*
    - Template
      - ```text
        count = 0
        pref = 0
        freq = map(); freq[0] = 1
        for x in nums:
          pref += x
          count += freq.get(pref - k, 0)
          freq[pref] = freq.get(pref, 0) + 1
        return count
        ```
- **Common compositions**
  - PrefixSumRangeQuery + MonotonicStack (range contributions / subarray min-max counting)
  - PrefixSumRangeQuery + BinarySearchBoundary (prefix-based feasibility checks)
- **Common interview pitfalls**
  - Forgetting base case `freq[0]=1` for “subarray starting at 0”
  - Using earliest index vs count incorrectly (problem-dependent)

---

## 2) Two Pointers Traversal (TwoPointersTraversal) 👯
- **Where you’ll see this at work**
  - Linear-time scans over sorted arrays; in-place compaction/filtering pipelines
  - Text normalization with symmetric checks (palindrome-like validations)
- **Kernel mini-spec**
  - **Signature**: array/string `A`; output depends (max/min, boolean, indices, modified array)
  - **Required invariant**: after each move, the discarded region cannot contain a better/valid answer than what remains (or what’s recorded)
  - **State model**: pointers (`L`,`R`) or (`read`,`write`); optional counters for constraints/duplicates
  - **Complexity envelope**: $O(n)$ time from monotone pointer movement; $O(1)$ extra space
  - **Failure modes / when NOT to use**: requires monotonic structure (sorted/symmetric) or a preserved feasibility argument; otherwise use hashing/DP
- **Complexity template**
  - Time $O(n)$; space $O(1)$ extra
- **Mental model**: every move *proves* excluded region can’t contain the answer
- **Dominant proof pattern (safety lemma)**
  - “At each step, choose a pointer move that preserves the existence of an optimal solution in the remaining interval; equivalently, prove that the discarded indices cannot participate in any better solution than the best already seen.”
  - Example ([LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)): if `height[L] ≤ height[R]`, any container using `L` with smaller width can’t exceed current area unless the limiting height increases ⇒ increment `L`.
- **Subfamilies**
  - **Opposite pointers** (sorted/symmetric optimization)
    - Maximize objective
      - ⭐ [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)(move shorter side)*
    - Palindrome validation
      - ⭐ [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
      - ⭐ [LeetCode 680](https://leetcode.com/problems/valid-palindrome-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)(one skip branch)*
  - **Dedup + enumeration on sorted array**
    - 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)(outer i + inner L/R + skip duplicates)*
    - 🧊 [LeetCode 16](https://leetcode.com/problems/3sum-closest/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - **Hash Map Lookup (single pass)**
    - 🔥 [LeetCode 1](https://leetcode.com/problems/two-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
    - Note: two pointers requires **sorted input** (or sorting), which changes complexity and indices vs values trade-offs. The canonical opposite-pointer variant is **[LeetCode 167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/)(not in provided solutions list)*.
- **Pattern ID mapping (pattern_id → subfamily)**
  - `two_pointer_opposite_maximize` → Opposite pointers → Maximize objective
  - `two_pointer_opposite_palindrome` → Opposite pointers → Palindrome validation
  - `two_pointer_three_sum` → Dedup + enumeration on sorted array
  - `hash_map_complement` → Hash Map Lookup (single pass)
- **Quick invariant table**
  - | Pattern | Invariant | Typical problems |
    |---------|-----------|------------------|
    | Opposite | answer in `[L..R]` under safety lemma | ⭐ [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
    | Sorted enumeration | no duplicate tuples emitted | 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- **Common compositions**
  - TwoPointersTraversal + BinarySearchBoundary (two-level search: fix one pointer, binary search partner)
  - TwoPointersTraversal + PrefixSumRangeQuery (post-filtering then prefix analytics)
- **Common interview pitfalls (examples)**
  - Duplicates: skipping too early/late in 3Sum leads to missing/duplicated tuples
  - Termination: wrong loop (`<=` vs `<`) causes infinite loop or double-processing
  - Stable vs unstable: compaction should preserve relative order when required

---

## 3) Sliding Window (SubstringSlidingWindow) 🪟
- **Where you’ll see this at work**
  - Rate limiting windows; moving aggregates/features over event streams
  - Log scanning for anomaly substrings; token frequency windows
- **Kernel mini-spec**
  - **Signature**: sequence `s`/`nums`, optional parameter `k`/`target`; output max/min length, boolean, or indices
  - **Required invariant**: maintain window state so a predicate `Valid(L,R)` can be checked/updated incrementally
  - **State model**: pointers `L ≤ R`; counts (`freq`, `need/have`), distinct counters, sums; optionally `last_seen_index`
  - **Complexity envelope**: `R` increments exactly `n` times; `L` is monotonically non-decreasing and increments at most `n` times ⇒ total pointer moves $O(n)$. Total work $O(n)$ assuming $O(1)$ state update/query (or $O(n·Σ)$ if you rescan an alphabet/state each step).
  - **Failure modes / when NOT to use**: predicate not monotone under moving `L` (e.g., sums with negatives); validity check requires scanning large state each step
- **Complexity template**
  - Time $O(n)$ with monotone pointers + $O(1)$ updates; space $O(Σ)$ for counts (or $O(k)$ distinct keys)
- **State choices**
  - `last_seen_index` map (jump-L optimization)
  - `freq` map + `distinct_count`
  - `need/have` maps + `satisfied/required`
  - numeric `window_sum`
- **Pattern comparison table**
  - | Problem | Invariant | State | Window Size | Goal |
    |---------|-----------|-------|-------------|------|
    | 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
    | 🧊 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
    | 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
    | ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
    | ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
    | ⭐ [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
- **Patterns**
  - **Unique window** (`sliding_window_unique`)
    - Anchor: 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)(learn jump-left)==
    - Two correct invariants/implementations
      - Frequency-based: maintain `freq[c] ≤ 1` for all `c` in `s[L..R]`; while violated, increment `L` decrementing `freq`
      - Last-seen jump: maintain `L = max(L, last_seen[c]+1)` so `s[L..R]` has no duplicates  
        - Invariant (last-seen): `L` is always `1 +` the maximum last-seen index among duplicates within the current window
    - Template (last-seen jump)
      - ```text
        last = map(); L = 0; best = 0
        for R in [0..n-1]:
          c = s[R]
          if c in last:
            L = max(L, last[c] + 1)
          last[c] = R
          best = max(best, R - L + 1)
        return best
        ```
  - **At most K distinct** (`sliding_window_at_most_k_distinct`)
    - Anchor: 🧊 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
    - Template
      - ```text
        freq = map(); distinct = 0; L = 0; best = 0
        for R in [0..n-1]:
          add s[R]; if freq[s[R]] becomes 1: distinct++
          while distinct > K:
            remove s[L]; if freq[s[L]] becomes 0: distinct--
            L++
          best = max(best, R - L + 1)
        return best
        ```
  - **Frequency contracts (do not mix)**
    - Warning: **Cover** (≥ need) is a variable-window “shrink-while-valid” state machine; **Exact match** (= need) is a fixed-window state machine. Mixing counters/loops causes bugs.
    - **Cover contract (≥ need)** (`sliding_window_freq_cover`)
      - Minimize cover: 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
      - Note: array `[128]/[256]` is faster than dict for ASCII; dict needed for unicode/general tokens.
      - Template
        - ```text
          need = counts(t); have = map(); satisfied = 0; required = number_of_keys(need)
          L = 0; best = none
          for R in [0..n-1]:
            add s[R] into have
            if s[R] in need and have[s[R]] == need[s[R]]: satisfied++
            while satisfied == required:
              update best using [L..R]
              if s[L] in need and have[s[L]] == need[s[L]]: satisfied--
              remove s[L] from have
              L++
          return best
          ```
    - **Exact-match contract (= need)** (`sliding_window_fixed_size`)
      - Fixed-size exact match (exists): ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
      - Fixed-size exact match (collect all): ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
      - Template
        - ```text
          need = counts(p); have = empty counts
          matched = 0; required = number_of_keys(need)
          L = 0
          for R in [0..n-1]:
            add s[R] into have; update matched if have hits need exactly
            if window_size > len(p):
              remove s[L] from have; update matched if crossing equality
              L++
            if window_size == len(p) and matched == required:
              record match (or return true)
          ```
  - **Cost bounded / sum constraint** (`sliding_window_cost_bounded`)
    - Anchor: ⭐ [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
    - Note: this shrinking-window method requires all numbers to be **non-negative** (as in [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)). With negative numbers, validity is not monotone in `L` and sliding window fails; use prefix sums + monotone deque / binary search variants instead.
    - Template
      - ```text
        L = 0; sum = 0; best = +inf
        for R in [0..n-1]:
          sum += nums[R]
          while sum >= target:
            best = min(best, R - L + 1)
            sum -= nums[L]; L++
        return best if best != +inf else 0
        ```
- **Common compositions**
  - SubstringSlidingWindow + HeapTopK (top-k within moving window; streaming analytics)
  - SubstringSlidingWindow + PrefixSumRangeQuery (windowed feature extraction + downstream counts)
- **Common interview pitfalls**
  - “minimize window” needs: **while valid → shrink** (not just one shrink)
  - “exact match” works best with: **fixed window** + `matched` counter

---

## 4) Binary Search Boundary (BinarySearchBoundary) 🔎
- **Where you’ll see this at work**
  - Feature flags/rollouts: first version where regression appears; capacity planning via feasibility checks
  - Tuning thresholds: minimum viable parameter under monotone predicate
- **Kernel mini-spec**
  - **Signature**: sorted array `A` or predicate `P(x)` over an ordered domain; output boundary index/value
  - **Required invariant**: search interval maintains “answer exists within bounds” under monotone predicate
  - **State model**: `lo, hi` bounds; `mid`; predicate `P(mid)`; optional best-so-far
  - **Complexity envelope**: $O(\log n)$ evaluations for index search; $O(\log V)$ for answer-space with domain size `V`
  - **Failure modes / when NOT to use**: predicate not monotone; off-by-one boundaries; mid not progressing
- **Complexity template**
  - Time $O(\log n)$ (index) or $O(\log V)$ (answer-space); space $O(1)$
- **Boundary templates**
  - `first_true` (`binary_search_first_true`) / `lower_bound`
    - ```text
      // find smallest x in [lo, hi) with P(x) == true
      while lo < hi:
        mid = lo + (hi - lo)//2
        if P(mid): hi = mid
        else: lo = mid + 1
      return lo
      ```
  - `last_true` (`binary_search_last_true`)
    - ```text
      // find largest x in [lo, hi) with P(x) == true; return lo-1 if none
      while lo < hi:
        mid = lo + (hi - lo)//2
        if P(mid): lo = mid + 1
        else: hi = mid
      return lo - 1
      ```
  - `upper_bound` (first `> key`) / `lower_bound` (first `≥ key`) mental model
    - “Pick the first index where predicate flips from false→true.”
- **Answer-space search** (`binary_search_on_answer`)
  - Monotone feasibility checklist
    - Define `feasible(x)` clearly
    - Prove: if `feasible(x)` then `feasible(x')` for all `x' ≥ x` (or ≤ x)
    - Choose search for min feasible / max feasible accordingly
  - Template (min feasible)
    - ```text
      lo = min_possible; hi = max_possible
      while lo < hi:
        mid = lo + (hi - lo)//2
        if feasible(mid): hi = mid
        else: lo = mid + 1
      return lo
      ```
  - Anchors
    - 🔥 [LeetCode 875](https://leetcode.com/problems/longest-mountain-in-array/description/)(not in provided solutions list)*
    - 🔥 [LeetCode 1011](https://leetcode.com/problems/flip-binary-tree-to-match-preorder-traversal/description/)(not in provided solutions list)*
- **Rotated array search** (`binary_search_rotated`)
  - Anchor set
    - 🔥 [LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/description/)(not in provided solutions list)*
    - 🔥 [LeetCode 153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/)(not in provided solutions list)*
  - Template
    - ```text
      lo = 0; hi = n-1
      while lo <= hi:
        mid = (lo + hi)//2
        if A[mid] == target: return mid
        if A[lo] <= A[mid]:  // left sorted
          if A[lo] <= target < A[mid]: hi = mid - 1
          else: lo = mid + 1
        else:               // right sorted
          if A[mid] < target <= A[hi]: lo = mid + 1
          else: hi = mid - 1
      return -1
      ```
- **Binary search on partition index (advanced hybrid)**
  - 🧊 [LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)(partition-by-count invariant)==
    - Invariant: choose `i` in A, `j` in B so left side has `(m+n+1)//2` elements and `maxLeft ≤ minRight`
- **Common compositions**
  - BinarySearchBoundary + GridBFSMultiSource (outer binary search on time; inner feasibility via BFS/DFS)
  - BinarySearchBoundary + HeapTopK (search threshold; validate by counting via heap/selection)
- **Common interview pitfalls**
  - Wrong half-open interval leading to infinite loops
  - Predicate depends on mutable global state (must be reset per check)

---

## 5) Tree Traversal (TreeTraversalDFS + TreeTraversalBFS) 🌳
- **Where you’ll see this at work**
  - Hierarchies: org charts, filesystem trees, DOM/AST traversal
  - Aggregations: compute metrics bottom-up; validate constraints top-down
- **Kernel mini-spec**
  - **Signature**: `root` node; output aggregate value, boolean, list per level, or path-based result
  - **Required invariant**: DFS preserves call-stack path; BFS processes nodes in non-decreasing depth
  - **State model**: recursion stack (DFS) / queue (BFS); optional parent pointers
  - **Complexity envelope**: visit each node once ⇒ $O(n)$ time; space $O(h)$ DFS / $O(w)$ BFS
  - **Failure modes / when NOT to use**: recursion depth overflow (use iterative); missing base cases / null checks
- **Complexity template**
  - Time $O(n)$; space $O(h)$ (DFS) or $O(w)$ (BFS)
- **Patterns**
  - **DFS (recursive)** (`tree_dfs_recursive`)
    - Anchors
      - 🔥 [LeetCode 104](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/)(not in provided solutions list)*
      - 🔥 [LeetCode 236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/description/)(not in provided solutions list)*
    - Template
      - ```text
        def dfs(node):
          if node == null: return base
          left = dfs(node.left)
          right = dfs(node.right)
          return combine(node, left, right)
        return dfs(root)
        ```
  - **BFS (level-order)** (`bfs_level_order`)
    - Anchor: 🔥 [LeetCode 102](https://leetcode.com/problems/binary-tree-level-order-traversal/description/)(not in provided solutions list)*
    - Template
      - ```text
        q = queue([root]); ans = []
        while q not empty:
          level = []
          repeat size(q) times:
            node = pop_front(q)
            level.append(node.val)
            push children
          ans.append(level)
        return ans
        ```
- **Common compositions**
  - TreeTraversalDFS + BacktrackingExploration (path enumeration with constraints)
  - TreeTraversalBFS + BinarySearchBoundary (search minimal depth satisfying predicate)
- **Common interview pitfalls**
  - Forgetting to return/propagate values in recursion
  - Using BFS but forgetting fixed layer size (mixing levels)

---

<!-- markmap: fold -->
## 6) Graph BFS/DFS + Grid BFS (GridBFSMultiSource) 🌊
- **Where you’ll see this at work**
  - Propagation/latency from multiple regions; shortest-time spread simulations
  - Grid-like maps and multi-source distance transforms
- **Kernel mini-spec**
  - **Signature**: grid `m×n` with sources/targets/obstacles; output minimum time/steps or final state
  - **Required invariant**: level-order expansion ensures first time reaching a cell is via a shortest path in an unweighted graph
  - **State model**: queue of frontier; visited set/mark; distance/time array or in-place timestamps
  - **Complexity envelope**: each cell enqueued/dequeued at most once ⇒ $O(mn)$ time, $O(mn)$ space
  - **Failure modes / when NOT to use**: weighted edges (use Dijkstra); marking visited too late causing multiple enqueues
- **Complexity template**
  - Time $O(V+E)$ (grid: $O(mn)$); space $O(V)$
- **Core idea**: push all sources, expand layer by layer (time = levels)
- **Invariant (shortest-by-level)**
  - When a cell is dequeued, its recorded time/distance is minimal among all possible paths from any source (unweighted edges). Level-order traversal corresponds to increasing distance.
  - Mark visited upon **enqueue** (not dequeue) to avoid multiple enqueues.
- **Anchor**
  - 🔥 [LeetCode 994](https://leetcode.com/problems/rotting-oranges/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- **Engineering checklist**
  - queue init with all sources
  - count fresh/remaining targets
  - process BFS by levels to count minutes
- **Common compositions**
  - GridBFSMultiSource + BinarySearchBoundary (time feasibility variants)
  - GridBFSMultiSource + UnionFindConnectivity (connectivity vs shortest-time trade-offs)
- **Common interview pitfalls (examples)**
  - Forgetting to enqueue all initial sources (multi-source correctness)
  - Wrong minute counting (increment per level, not per node)

---

## 7) Heap / Selection (HeapTopK + Quickselect) ⛰️
- **Where you’ll see this at work**
  - Trending queries, telemetry heavy hitters, priority scheduling
  - Streaming medians/percentiles (two-heaps median; approximate alternatives)
- **Kernel mini-spec**
  - **Signature**: stream/array `nums`, parameter `k`; output kth/top-k/median
  - **Required invariant**: heap maintains extremum at top; size constraint encodes “kept set”
  - **State model**: min-heap of size `k` (top-k largest) or max-heap analog; for median, two heaps partition lower/upper halves
  - **Complexity envelope**: per insertion $O(\log k)$ for bounded heap; build heap $O(n)$ then pops $O(k\log n)$ or incremental
  - **Failure modes / when NOT to use**: if you need full sort order; if k≈n and sorting is simpler; quickselect may be faster in-memory
- **Complexity template**
  - Heap top-k: $O(n \log k)$ time, $O(k)$ space; Quickselect: avg $O(n)$, worst $O(n^2)$ unless randomized
- **Kth element**
  - Quickselect / partition: 🔥 [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
    - Note: average $O(n)$ time, worst-case $O(n^2)$ unless randomized/median-of-medians; $O(1)$ extra space (in-place).
  - Heap alternative (especially streaming / stability): 🔥 [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
    - Note: $O(n \log k)$ time, $O(k)$ space; better for streaming and when $k \ll n$.
- **Decision note**
  - **[LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)**: Quickselect (avg $O(n)$; must guard worst-case) vs Heap ($O(n\log k)$; streaming-friendly)
- **Common compositions**
  - HeapTopK + SubstringSlidingWindow (top-k within moving window)
  - HeapTopK + KWayMerge (merge streams and maintain top-k)
- **Common interview pitfalls (examples)**
  - Not randomizing pivot for quickselect (adversarial worst-case)
  - Mishandling duplicates around pivot (use 3-way partition if needed)

---

## 8) Monotonic Stack (MonotonicStack) 🧱
- **Where you’ll see this at work**
  - Next-greater queries in monitoring; skyline/range dominance computations
  - Histogram-like capacity/area computations
- **Kernel mini-spec**
  - **Signature**: array `A`; output next greater/smaller indices/values or maximal area
  - **Required invariant**: stack maintains monotone order of values (or indices) so each element is pushed/popped once
  - **State model**: stack of indices; sentinel index to flush at end
  - **Complexity envelope**: each index pushed/popped at most once ⇒ $O(n)$ time; stack $O(n)$ space
  - **Failure modes / when NOT to use**: wrong strict vs non-strict inequality; forgetting sentinel/flush; duplicates handling
- **Complexity template**
  - Time $O(n)$ amortized; space $O(n)$
- **Anchors**
  - 🔥 [LeetCode 739](https://leetcode.com/problems/daily-temperatures/description/)(not in provided solutions list)*
  - 🔥 [LeetCode 84](https://leetcode.com/problems/largest-rectangle-in-histogram/description/)(not in provided solutions list)*
- **Templates**
  - Next greater element
    - ```text
      st = empty stack of indices
      for i in [0..n-1]:
        while st not empty and A[st.top] < A[i]:
          j = st.pop()
          ans[j] = i
        st.push(i)
      ```
  - Histogram max rectangle (with sentinel)
    - ```text
      st = empty stack
      for i in [0..n]:               // treat A[n]=0 sentinel
        cur = A[i] if i<n else 0
        while st not empty and A[st.top] > cur:
          h = A[st.pop()]
          left = st.top if st not empty else -1
          width = i - left - 1
          best = max(best, h * width)
        st.push(i)
      return best
      ```
- **Common compositions**
  - MonotonicStack + PrefixSumRangeQuery (range contributions / sum of subarray mins/maxes)
- **Common interview pitfalls**
  - Using `<` vs `<=` changes duplicate behavior; must match problem definition

---

## 9) Backtracking Exploration (BacktrackingExploration) 🧠
- **Where you’ll see this at work**
  - Constraint solvers, configuration search, rule-based generation (small domains)
  - Enumerating candidate solutions with pruning
- **Kernel mini-spec**
  - **Signature**: candidate set/options; output list of solutions or count
  - **Required invariant**: state exactly matches current path (no “ghost marks”)
  - **State model**: recursion stack; `path`; `used[]` or `start` index; constraint sets (cols/diags)
  - **Complexity envelope**: $O(\text{branch}^{\text{depth}})$ time; recursion depth $O(\text{depth})$; output-size lower bound
  - **Failure modes / when NOT to use**: large unconstrained search space (need DP/greedy); forgetting rollback; excessive copying
- **Complexity template**
  - Time $O(\text{branch}^{\text{depth}})$ (often output-dominated); space $O(\text{depth})$ + output
- **Core rhythm**: **Choose → Explore → Unchoose**
- **Invariant**: state exactly matches current path (no “ghost marks”)
- **Decision-tree shapes**
  - **Permutation** (used[])
    - ⭐ [LeetCode 46](https://leetcode.com/problems/permutations/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
    - With duplicates (sort + same-level skip): 🧊 [LeetCode 47](https://leetcode.com/problems/permutations-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)
    - Template
      - ```text
        used = [false]*n; path = []
        def dfs():
          if len(path) == n: emit(path); return
          for i in [0..n-1]:
            if used[i]: continue
            used[i] = true; path.push(A[i])
            dfs()
            path.pop(); used[i] = false
        dfs()
        ```
  - **Subset** (start index)
    - ⭐ [LeetCode 78](https://leetcode.com/problems/subsets/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
    - With duplicates (sort + same-level skip): 🧊 [LeetCode 90](https://leetcode.com/problems/subsets-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)
    - Template
      - ```text
        path = []
        def dfs(i):
          emit(path)
          for j in [i..n-1]:
            if j>i and A[j]==A[j-1]: continue
            path.push(A[j])
            dfs(j+1)
            path.pop()
        dfs(0)
        ```
  - **Combination / fixed size** (start index + length bound)
    - ⭐ [LeetCode 77](https://leetcode.com/problems/combinations/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
    - Template
      - ```text
        path=[]
        def dfs(start):
          if len(path)==k: emit(path); return
          for x in [start..N]:
            path.push(x)
            dfs(x+1)
            path.pop()
        dfs(1)
        ```
  - **Target sum search**
    - Reuse allowed: ⭐ [LeetCode 39](https://leetcode.com/problems/combination-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
    - No reuse + duplicates: ⭐ [LeetCode 40](https://leetcode.com/problems/combination-sum-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)
    - Fixed count + bounded domain: 🧊 [LeetCode 216](https://leetcode.com/problems/combination-sum-iii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)
    - Template (reuse-allowed)
      - ```text
        path=[]
        def dfs(start, remain):
          if remain==0: emit(path); return
          for i in [start..n-1]:
            if A[i] > remain: continue/prune if sorted
            path.push(A[i])
            dfs(i, remain - A[i])   // reuse allowed
            path.pop()
        dfs(0, target)
        ```
  - **Constraint satisfaction**
    - ⭐ [LeetCode 51](https://leetcode.com/problems/n-queens/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
    - 🧊 [LeetCode 52](https://leetcode.com/problems/n-queens-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
    - Template
      - ```text
        cols=set(); d1=set(); d2=set()
        def dfs(r):
          if r==n: emit(); return
          for c in [0..n-1]:
            if c in cols or (r-c) in d1 or (r+c) in d2: continue
            add(c,r-c,r+c)
            dfs(r+1)
            remove(c,r-c,r+c)
        dfs(0)
        ```
  - **String segmentation**
    - 🧊 [LeetCode 93](https://leetcode.com/problems/restore-ip-addresses/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)(4 segments + length bounds prune)*
    - ⭐ [LeetCode 131](https://leetcode.com/problems/palindrome-partitioning/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)(optional DP precompute for palindrome checks)*
    - Decision note: **[LeetCode 131](https://leetcode.com/problems/palindrome-partitioning/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)** precompute palindrome DP $O(n^2)$ to reduce repeated checks; better for longer strings.
    - Template
      - ```text
        path=[]
        def dfs(i):
          if i==n: emit(path); return
          for j in [i..n-1]:
            if not is_valid(i,j): continue
            path.push(s[i..j])
            dfs(j+1)
            path.pop()
        dfs(0)
        ```
  - **Grid path search**
    - ⭐ [LeetCode 79](https://leetcode.com/problems/word-search/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)(visited mark/unmark)*
    - Template
      - ```text
        def dfs(r,c,idx):
          if idx==len(word): return true
          if out_of_bounds or visited or grid[r][c]!=word[idx]: return false
          visited[r][c]=true
          ok = any(dfs(nr,nc,idx+1) for neighbors)
          visited[r][c]=false
          return ok
        ```
- **Common compositions**
  - BacktrackingExploration + DP memo (top-down caching) for segmentation/partitioning
  - BacktrackingExploration + BinarySearchBoundary (search parameter; validate via backtracking for small domains)
- **Common interview pitfalls**
  - Not rolling back state (visited/sets/path)
  - Over-copying lists at each recursion step (time/memory blowups)

---

## 10) Linked List Manipulation (pointer surgery) 🔧
- **Where you’ll see this at work**
  - In-place transformations; streaming pipelines; pointer-safe rewiring
- **Kernel mini-spec**
  - **Signature**: `head` of linked list; output new head or modified list
  - **Required invariant**: preserve reachability; never lose remaining list (`next`) while rewiring
  - **State model**: `prev/curr/next`, dummy head, group boundaries
  - **Complexity envelope**: typically $O(n)$ time, $O(1)$ extra space
  - **Failure modes / when NOT to use**: forgetting to store `next`; mishandling head changes; group boundary errors
- **Complexity template**
  - Time $O(n)$; space $O(1)$ extra
- Arithmetic on lists
  - ⭐ [LeetCode 2](https://leetcode.com/problems/add-two-numbers/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py)
- In-place reversal in groups
  - ⭐ [LeetCode 25](https://leetcode.com/problems/reverse-nodes-in-k-group/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- **Common compositions**
  - Linked list manipulation + HeapTopK (stream nodes by value)
- **Common interview pitfalls (examples)**
  - Not using dummy head (complex head-edge handling)
  - Reversing fewer than `k` nodes (must check availability first)

---

## 11) Partitioning (TwoPointerPartition) 🚧
- **Where you’ll see this at work**
  - In-place bucketing (flags, categories), quickselect pipelines, unstable partition stages
- **Kernel mini-spec**
  - **Signature**: array `A`; output reordered array (in-place) and/or pivot index / partition boundary
  - **Required invariant**: maintain disjoint regions (good/bad/unknown) with correct pointer movement
  - **State model**: pointers delimiting regions (`low, mid, high` or `i, j`); predicate “good(x)”
  - **Complexity envelope**: $O(n)$ time, $O(1)$ extra space
  - **Failure modes / when NOT to use**: stability required (use reader/writer); incorrect unknown-region handling
- **Complexity template**
  - Time $O(n)$; space $O(1)$
- **Note on stability**
  - Writer pattern is a **2-region partition with stability**; this section is multi-region / swap-based (typically **unstable**).
- **Patterns**
  - **Dutch flag (3-way partition)** (`dutch_flag_partition`)
    - Anchor: 🔥 [LeetCode 75](https://leetcode.com/problems/sort-colors/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
    - Loop invariant: maintain  
      `A[0..low-1]=0`, `A[low..mid-1]=1`, `A[mid..high]=unknown`, `A[high+1..n-1]=2`.
    - Template
      - ```text
        low=0; mid=0; high=n-1
        while mid <= high:
          if A[mid]==0: swap(A[low],A[mid]); low++; mid++
          elif A[mid]==1: mid++
          else: swap(A[mid],A[high]); high--
        ```
  - **Two-way partition** (`two_way_partition`)
    - ⭐ [LeetCode 905](https://leetcode.com/problems/sort-array-by-parity/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
    - 🧊 [LeetCode 922](https://leetcode.com/problems/sort-array-by-parity-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
    - Loop invariant: maintain  
      `A[0..i-1]` are ‘good’, `A[j+1..n-1]` are ‘bad’, `i ≤ j` unknown.
    - Template
      - ```text
        i=0; j=n-1
        while i <= j:
          if good(A[i]): i++
          elif not good(A[j]): j--
          else: swap(A[i],A[j]); i++; j--
        ```
- **Common compositions**
  - TwoPointerPartition + Quickselect (selection pipeline)
- **Common interview pitfalls**
  - Off-by-one in `mid <= high` (Dutch flag)
  - Stability assumptions (swap-based partition breaks relative order)

---

## 12) Fast–Slow Pointers (FastSlowPointers) 🐢🐇
- **Where you’ll see this at work**
  - Detecting cycles in iterative processes; midpoint splits for list algorithms
- **Kernel mini-spec**
  - **Signature**: linked list head or function `f(x)`; output cycle existence/start or midpoint
  - **Required invariant**: fast moves 2x; if cycle exists, pointers meet; second phase aligns to cycle entry
  - **State model**: `slow`, `fast`; optionally reset pointer for phase 2
  - **Complexity envelope**: $O(n)$ time, $O(1)$ space
  - **Failure modes / when NOT to use**: null checks for `fast` and `fast.next`; misunderstanding phase-2 proof
- **Complexity template**
  - Time $O(n)$; space $O(1)$
- **Two phases (Floyd)**
  - Phase 1: detect cycle
  - Phase 2: find cycle start
- **Problems**
  - Detect cycle: ⭐ [LeetCode 141](https://leetcode.com/problems/linked-list-cycle/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - Find cycle start: ⭐ [LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - Implicit cycle (function iteration): ⭐ [LeetCode 202](https://leetcode.com/problems/happy-number/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)
  - Midpoint: ⭐ [LeetCode 876](https://leetcode.com/problems/middle-of-the-linked-list/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
- **Common compositions**
  - FastSlowPointers + MergeSortedSequences (split list then merge: mergesort on list)
- **Common interview pitfalls**
  - Not checking `fast`/`fast.next` before stepping
  - Returning meet point instead of entry point (phase 2 required)

---

## 13) Merging Sorted Sequences (MergeSortedSequences + KWayMerge) 🔗
- **Where you’ll see this at work**
  - Merging sorted log segments (LSM compaction), external sort, shard result merging
- **Kernel mini-spec**
  - **Signature**: two sorted sequences (or k sequences); output merged sorted sequence
  - **Required invariant**: output prefix is always the smallest remaining elements; pointers/heap reflect current heads
  - **State model**: two pointers for 2-way; min-heap of current heads for k-way
  - **Complexity envelope**: 2-way $O(m+n)$; k-way $O(N\log k)$; extra space $O(1)$ to $O(k)$
  - **Failure modes / when NOT to use**: inputs not sorted; forgetting stable tie-handling if required
- **Complexity template**
  - Two-way merge $O(m+n)$; k-way heap merge $O(N\log k)$ with $O(k)$ heap space
- **Two sorted streams (two pointers)**
  - Linked list merge: 🔥 [LeetCode 21](https://leetcode.com/problems/merge-two-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - Array merge (often from ends): ⭐ [LeetCode 88](https://leetcode.com/problems/merge-sorted-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - Merge-from-ends trick: ⭐ [LeetCode 977](https://leetcode.com/problems/squares-of-a-sorted-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)
- **K-way merge**
  - Heap-based $O(N \log k)$: 🔥 [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - Divide-and-conquer $O(N \log k)$: 🔥 [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - Decision note ([LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py))
    - Heap (simpler, streaming-friendly, $O(k)$ memory) vs Divide&Conquer (often faster constants when all lists are in memory)
- **Common compositions**
  - KWayMerge + HeapTopK (merge many streams but keep only top-k)
  - MergeSortedSequences + BinarySearchBoundary (search partition/boundary on merged order statistics)
- **Common interview pitfalls**
  - Losing original pointers in linked list merges (store `next`)
  - Off-by-one in merge-from-ends indices

---

## 14) Union-Find Connectivity (UnionFindConnectivity) 🔌
- **Where you’ll see this at work**
  - Connectivity clustering, dedup of accounts/entities, network components
- **Kernel mini-spec**
  - **Signature**: `n` nodes + edges/relations; output component count or merged groups
  - **Required invariant**: `find(x)` returns representative; `union(a,b)` merges sets
  - **State model**: `parent[]`, `rank/size[]` with path compression
  - **Complexity envelope**: near $O(1)$ amortized per op ($α(n)$)
  - **Failure modes / when NOT to use**: directed reachability/shortest path (use BFS/DFS); forgetting path compression
- **Complexity template**
  - Time $O((n+m)·α(n))$; space $O(n)$
- **Anchors**
  - 🔥 [LeetCode 200](https://leetcode.com/problems/number-of-islands/description/)(UF alternative) *(not in provided solutions list)*
  - 🔥 [LeetCode 721](https://leetcode.com/problems/accounts-merge/description/)(not in provided solutions list)*
- **Template**
  - ```text
    init parent[i]=i, size[i]=1
    def find(x):
      while x != parent[x]:
        parent[x] = parent[parent[x]]
        x = parent[x]
      return x
    def union(a,b):
      ra, rb = find(a), find(b)
      if ra==rb: return
      if size[ra] < size[rb]: swap
      parent[rb]=ra; size[ra]+=size[rb]
    ```
- **Common compositions**
  - UnionFindConnectivity + Grid traversal (map 2D cells to ids)
- **Common interview pitfalls**
  - Union by rank/size missing → can degrade constants significantly

---

## 15) Topological Sort (TopologicalSort) 🧩
- **Where you’ll see this at work**
  - Build systems, dependency graphs, course prerequisites, DAG scheduling
- **Kernel mini-spec**
  - **Signature**: DAG with `n` nodes + edges; output ordering or feasibility
  - **Required invariant**: nodes with indegree 0 are safe to output next (Kahn’s)
  - **State model**: indegree array; queue of zero-indegree nodes
  - **Complexity envelope**: $O(V+E)$ time, $O(V+E)$ space
  - **Failure modes / when NOT to use**: cycles (ordering impossible); forgetting to decrement indegrees
- **Complexity template**
  - Time $O(V+E)$; space $O(V+E)$
- **Anchor**
  - 🔥 [LeetCode 207](https://leetcode.com/problems/course-schedule/description/)(not in provided solutions list)*
- **Template (Kahn)**
  - ```text
    build adj, indeg
    q = all nodes with indeg==0
    seen = 0
    while q not empty:
      u = pop(q); seen++
      for v in adj[u]:
        indeg[v]--
        if indeg[v]==0: push(q,v)
    return seen==n
    ```
- **Common compositions**
  - TopologicalSort + DPSequence (longest path in DAG via topo order)
- **Common interview pitfalls**
  - Using DFS topo but missing 3-color cycle detection

---

## 16) Dynamic Programming (DPSequence + DPInterval) 🧠📈
- **Where you’ll see this at work**
  - Cost optimization, scheduling, string alignment, interval scoring
- **Kernel mini-spec**
  - **Signature**: sequence/string/interval; output optimal value or reconstruction
  - **Required invariant**: define state `dp[...]` meaning clearly; transitions use smaller subproblems only
  - **State model**: 1D dp for sequences; 2D dp for intervals/substrings
  - **Complexity envelope**: depends on state size × transition cost
  - **Failure modes / when NOT to use**: state not minimal (blows up); missing base cases; wrong iteration order
- **Complexity template**
  - Typically $O(\#states × \#transitions)$; space $O(\#states)$ (often optimizable)
- **Anchors**
  - 🔥 [LeetCode 70](https://leetcode.com/problems/climbing-stairs/description/)(not in provided solutions list)*
  - 🔥 [LeetCode 300](https://leetcode.com/problems/longest-increasing-subsequence/description/)(not in provided solutions list)*
- **Templates**
  - Fibonacci-style (`dp_fibonacci_style`)
    - ```text
      dp[0]=...; dp[1]=...
      for i in [2..n]:
        dp[i] = dp[i-1] + dp[i-2]   // example
      return dp[n]
      ```
  - Interval DP skeleton (`dp_palindrome` / DPInterval)
    - ```text
      dp = 2D array n×n
      for len in [1..n]:
        for i in [0..n-len]:
          j = i + len - 1
          dp[i][j] = combine(dp smaller intervals, s[i], s[j])
      return dp[0][n-1]
      ```
- **Common compositions**
  - DPInterval + BacktrackingExploration (DP for fast validity checks; backtrack to enumerate)
- **Common interview pitfalls**
  - Using recursion without memoization (TLE)
  - Wrong iteration order for interval dependencies

---

## Suggested Learning Paths (roadmap-style) 🚀
- **Sliding Window Mastery**
  - [ ] 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [ ] 🧊 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - [ ] 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - [ ] ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
  - [ ] ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - [ ] ⭐ [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
- **Two Pointers Mastery**
  - [ ] ⭐ [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ] ⭐ [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - [ ] 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- **Backtracking Mastery**
  - [ ] ⭐ [LeetCode 78](https://leetcode.com/problems/subsets/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
  - [ ] ⭐ [LeetCode 46](https://leetcode.com/problems/permutations/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
  - [ ] ⭐ [LeetCode 39](https://leetcode.com/problems/combination-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
  - [ ] ⭐ [LeetCode 51](https://leetcode.com/problems/n-queens/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - [ ] ⭐ [LeetCode 79](https://leetcode.com/problems/word-search/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

---
```
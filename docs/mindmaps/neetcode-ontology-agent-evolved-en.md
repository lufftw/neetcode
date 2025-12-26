---
title: LeetCode Core Patterns Mind Map (API Kernels → Patterns → Problems)
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 How to use this map (fast)
- **Start from API Kernels** → pick a pattern → solve the mapped problems
- Keep one invariant per pattern: **expand** (add right / go deeper) then **contract** (move left / undo)
- Sliding window mental model (copy this into code)
  - Outer loop advances `R` (expand via `on_enter(R)`)
  - Inner loop advances `L` while **invariant violated** (maximize/exist) or while **window valid** (minimize)
  - Each pointer moves monotonically (`L` and `R` each increase ≤ n)
- Progress tracking
  - [ ] Finish all **Easy** anchors
  - [ ] Finish all **Medium** anchors
  - [ ] Finish at least 3 **Hard** anchors
- Legend
  - 🔥 must-know (FAANG frequent)
  - ⭐ common
  - 🧊 nice-to-know

## 🧠 Big Picture: From Technique → Kernel → Pattern → Problem
- **Technique** (e.g., *Two Pointers*)  
  - **API Kernel** (reusable “engine”, e.g., `SubstringSlidingWindow`)  
    - **Pattern** (invariant + state)  
      - **LeetCode {number}** (practice + recognition)

### ✅ Decision table: signal → kernel
| Signal | Use this kernel |
|--------|------------------|
| Contiguous subarray/substring + constraint/invariant | `SubstringSlidingWindow` |
| Sorted array + pair/tuple constraints | `TwoPointersTraversal` |
| Cycle/middle on linked list or function iteration | `FastSlowPointers` |
| Merge K sorted streams/lists | `KWayMerge` |
| Grid shortest time / distance transform (multi-source) | `GridBFSMultiSource` |
| Monotone predicate over index/value | `BinarySearchBoundary` |

---

## 🧩 Sequences / arrays / strings

## 🪟 SubstringSlidingWindow (API Kernel)
- **Inputs**: string/array; contiguous window; often `k`, `target`, or required frequency map
- **Output shape**: max/min length, boolean exists, indices, list of start positions
- **Invariant**: window property holds under expand/contract transitions
- **Failure modes / when not to use**: sum/cost constraints typically require **non-negative** numbers (monotone expansion); if negatives exist, use prefix sums + hash/balanced tree depending on query
- **Summary**: 1D window state machine over sequences with dynamic invariants
- **Cost model**: each index moves monotonically (`L` and `R` each increase ≤ n), so pointer work is $O(n)$. Map/counter ops add expected $O(1)$ per update (hashing) or $O(\log \sigma)$ if balanced tree.
- **State toolbelt**: `hash_map` / `counter`, sometimes integer sum
- **Standard hooks**: `on_enter(right)`, `on_exit(left)`, `is_valid()`, `score(window)`
- **Example use in production**: rate-limit / anomaly detection over event streams; log scanning for minimal covering window

<!-- markmap: fold -->
### 🧪 Sliding window pseudocode template (hooks)
```text
L = 0
for R in range(n):
  on_enter(R)
  while invariant_violated():   # or while is_valid() for "minimize while valid"
    on_exit(L); L += 1
  ans = score(ans, L, R)        # update max/min/exist/output
return ans
```

<!-- markmap: fold -->
### ✅ Pattern comparison table (must-know)
| Problem | Invariant | State | Window Size | Goal |
|---------|-----------|-------|-------------|------|
| 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) (H) - Minimum Window Substring | covers all of `t` | need/have maps | variable | minimize |
| 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) (M) - Longest Substring Without Repeating Characters | all unique | `last_index` map | variable | maximize |
| ⭐ [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) (M) - Find All Anagrams in a String | exact multiset match | freq + matched count | fixed | all positions |
| ⭐ [LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) (M) - Permutation in String | exact multiset match | freq + matched count | fixed | exists |
| ⭐ [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) (H) - Longest Substring with At Most K Distinct Characters | ≤ K distinct | freq map | variable | maximize |
| ⭐ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) (M) - Minimum Size Subarray Sum | sum ≥ target | integer sum | variable | minimize |

### sliding_window_unique
- **Invariant**: ==no duplicates in window==
- **State**: `last_seen_index[char]` (jump-left optimization)
- **Approach A**: last seen index jump-left ($O(n)$, simpler)
- **Approach B**: freq map shrink-left (also $O(n)$, more uniform template)
- **Anchor problems**
  - [ ] 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) (M) - Longest Substring Without Repeating Characters

### sliding_window_at_most_k_distinct
- **Invariant**: ==distinct_count ≤ K==
- **State**: frequency `hash_map`, maintain `len(map)`
- **Anchor problems**
  - [ ] ⭐ [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) (H) - Longest Substring with At Most K Distinct Characters

### sliding_window_freq_cover
- **Invariant**: ==window meets required frequencies==
- **State**: `need_frequency`, `have_frequency`, `chars_satisfied`

### sliding_window_min_cover
- **Invariant**: ==valid cover holds==
- **State**: `need_frequency`, `have_frequency`, `chars_satisfied`
- **Loop**: expand to become valid → contract while valid to minimize
- **Anchor problems**
  - [ ] 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) (H) - Minimum Window Substring

### sliding_window_fixed_match
- **Invariant**: ==exact multiset match==
- **State**: freq delta + `matched_count`
- **Anchor problems**
  - [ ] ⭐ [LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) (M) - Permutation in String
  - [ ] ⭐ [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) (M) - Find All Anagrams in a String

### sliding_window_fixed_size
- **Invariant**: ==window length == k==
- **State**: rolling counter/sum; optionally freq delta / matched count
- **Anchor problems**
  - [ ] 🧊 [LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) (M) - Permutation in String
  - [ ] 🧊 [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) (M) - Find All Anagrams in a String

### sliding_window_cost_bounded
- **Invariant**: ==sum/cost constraint satisfied==
- **State**: integer `window_sum`
- **Requires**: monotone expansion property (typically non-negative numbers)
- **See also**: Prefix sums (negatives break sliding window)
- **Anchor problems**
  - [ ] ⭐ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) (M) - Minimum Size Subarray Sum

## 👈👉 TwoPointersTraversal (API Kernel)
- **Inputs**: array/string; often sorted; sometimes target sum / tuple constraints
- **Output shape**: max/min value, boolean exists, indices, list of tuples
- **Invariant**: pointer moves preserve feasibility region / dedup rules
- **Failure modes / when not to use**: unsorted + pair sum usually needs hashmap; opposite-pointers assumes sorted/monotone movement is valid
- **Summary**: traverse with two coordinated pointers under invariant-preserving rules
- **Core promise**: each index moves monotonically (L and R each increase ≤ n), so pointer work is $O(n)$
- **Example use in production**: stable in-place filtering/compaction; scanning sorted logs/ids

<!-- markmap: fold -->
### 🧪 Two pointers pseudocode template (hooks)
```text
L, R = ...
while L < R:
  if should_move_L(): L += 1
  elif should_move_R(): R -= 1
  else: record_answer(); move_and_dedup()
```

<!-- markmap: fold -->
### ✅ Two pointers pattern comparison table
| Pattern | Init | Movement | Typical invariant | Time | Space |
|--------|------|----------|-------------------|------|-------|
| Opposite | `0, n-1` | toward center lies within [L,R] | $O(n)$ | $O(1)$ |
| Writer | `write=0, read=0` | both forward | `a[0:write]` is “kept” | $O(n)$ | $O(1)$ |
| Dedup enumeration | `i + (L,R)` | nested + skips | unique tuples only | $O(n^2)$ | $O(1)$ |

### two_pointer_opposite_maximize
- **Goal**: maximize a function while shrinking search space
- **Anchor problems**
  - [ ] 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) (M) - Container With Most Water

### two_pointer_three_sum (dedup enumeration)
- **Recipe**: sort → fix `i` → opposite pointers → skip duplicates
- **Notes**
  - Sorting cost: $O(n \log n)$, then scan is $O(n^2)$
  - Duplicate skipping: skip `i` if `nums[i]==nums[i-1]`; after finding a hit, move `L/R` past equal values
  - Output size can dominate runtime (many triples) even if pointer work is $O(n^2)$
- **Anchor problems**
  - [ ] 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py) (M) - 3Sum
  - [ ] ⭐ [LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py) (M) - 3Sum Closest

### two_pointer_writer_dedup (same-direction)
- **Invariant**: `arr[0:write)` is deduplicated
- **Anchor problems**
  - [ ] ⭐ [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py) (E) - Remove Duplicates from Sorted Array
  - [ ] ⭐ [LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py) (M) - Remove Duplicates from Sorted Array II

### two_pointer_writer_remove (same-direction)
- **Invariant**: `arr[0:write)` contains all kept elements
- **Anchor problems**
  - [ ] ⭐ [LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py) (E) - Remove Element

### two_pointer_writer_compact (same-direction)
- **Use case**: stable compaction (e.g., move zeros)
- **Anchor problems**
  - [ ] ⭐ [LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) (E) - Move Zeroes

### two_pointer_opposite_palindrome
- **Invariant**: characters checked so far match palindrome rule
- **Notes**: normalization concerns in real systems (skip non-alnum, case folding, Unicode graphemes/collation can be tricky)
- **Anchor problems**
  - [ ] 🔥 [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py) (E) - Valid Palindrome
  - [ ] ⭐ [LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py) (E) - Valid Palindrome II

### two_pointer_opposite_search (sorted array)
- **Note**: two pointers works when array is **sorted** (Two Sum II). Hashmap works on **unsorted**.
- **Anchor problems**
  - [ ] ⭐ [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py) (E) - Two Sum
  - [ ] ⭐ [LeetCode 2 - Add Two Numbers](https://leetcode.com/problems/add-two-numbers/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py) (M) - Add Two Numbers

## 🧱 TwoPointerPartition (API Kernel)
- **Inputs**: array; predicate/pivot; in-place rearrangement
- **Output shape**: partitioned array, pivot index, kth element
- **Invariant**: elements are maintained in partition regions
- **Failure modes / when not to use**: quickselect worst-case without randomization; stability not guaranteed
- **Summary**: partition array using two pointers (Dutch flag, quickselect)

<!-- markmap: fold -->
### 🧪 Partition pseudocode template (2-way)
```text
i = 0
for j in range(n):
  if predicate(a[j]):
    swap(a[i], a[j]); i += 1
return i  # boundary
```

### dutch_flag_partition
- **Regions**: `< pivot | = pivot | unknown | > pivot`
- **Anchor problems**
  - [ ] ⭐ [LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py) (M) - Sort Colors

### two_way_partition
- **Binary predicate**: even/odd, etc.
- **Anchor problems**
  - [ ] ⭐ [LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py) (E) - Sort Array By Parity
  - [ ] ⭐ [LeetCode 922 - Sort Array By Parity II](https://leetcode.com/problems/sort-array-by-parity-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py) (E) - Sort Array By Parity II

### quickselect_partition
- **Goal**: kth element without full sort (avg $O(n)$)
- **Note**: random pivot (or shuffle) to avoid adversarial worst-case; deterministic median-of-medians is overkill for interviews
- **See also**: HeapTopK (alternative for kth/top-k), same partition routine powers quicksort/quickselect
- **Anchor problems**
  - [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) (M) - Kth Largest Element in an Array

## 🔎 BinarySearchBoundary (API Kernel)
- **Inputs**: sorted array or monotone predicate over index/value space
- **Output shape**: index boundary, boolean, minimal feasible value
- **Invariant**: predicate is monotone; search interval maintains “answer inside”
- **Failure modes / when not to use**: predicate not monotone; mid bias mistakes cause infinite loops/off-by-one
- **Summary**: boundary binary search (first true / last true) + answer-space search
- **When it fits**: predicate is monotone over index or value space

<!-- markmap: fold -->
### 🧪 Binary search template (with mid bias note)
```text
# first_true
l, r = 0, n-1
while l < r:
  m = (l + r) // 2          # bias left
  if pred(m): r = m
  else: l = m + 1
return l

# last_true: use m = (l + r + 1) // 2  (bias right) to ensure progress
```

### binary_search_rotated
- **Anchor problems**
  - [ ] 🔥 [LeetCode 33 - Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/description/) (M) - Search in Rotated Sorted Array

### binary_search_first_last_position
- **Anchor problems**
  - [ ] 🔥 [LeetCode 34 - Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/description/) (M) - Find First and Last Position of Element in Sorted Array

### binary_search_on_answer
- **Anchor problems**
  - [ ] 🧊 [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py) (H) - Median of Two Sorted Arrays

## 📚 MonotonicStack (API Kernel)
- **Inputs**: array (often temperatures/prices/heights); queries about next/previous greater/smaller
- **Output shape**: next/prev index/value, spans, max area
- **Invariant**: stack indices maintain monotone order (increasing/decreasing)
- **Failure modes / when not to use**: use wrong monotone direction; forget to flush stack at end; equal-handling matters
- **Summary**: stack maintaining monotonic order for next-greater/smaller queries
- **Typical queries**: next greater/smaller, previous smaller/greater, span, histogram max rectangle
- **State**: stack of indices (values accessed via array)
- **Example use in production**: range-based alerting, stock span analytics, histogram-like dashboards

<!-- markmap: fold -->
### 🧪 Monotonic stack pseudocode template
```text
st = []  # indices
for i in range(n):
  while st and violates_monotone(a[st[-1]], a[i]):
    j = st.pop()
    answer_for(j, i)
  st.append(i)
flush_remaining(st)
```

### monotonic_next_greater
- **Anchor problems**
  - [ ] ⭐ [LeetCode 739 - Daily Temperatures](https://leetcode.com/problems/daily-temperatures/description/) (M) - Daily Temperatures
  - [ ] ⭐ [LeetCode 496 - Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/description/) (E) - Next Greater Element I

### histogram_max_rectangle
- **Anchor problems**
  - [ ] 🔥 [LeetCode 84 - Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/description/) (H) - Largest Rectangle in Histogram

## ➕ PrefixSumHash (API Kernel)
- **Inputs**: array; sums/zero-one transforms; can handle negatives
- **Output shape**: count of subarrays, max length, boolean exists
- **Invariant**: prefix sums accumulated; hashmap stores earliest index / counts
- **Failure modes / when not to use**: beware overflow in other languages; choose earliest vs counts depending on query
- **Summary**: prefix sum + hash map for subarray sum / balance conditions
- **Example use in production**: telemetry windows with negatives; anomaly “net change” queries

<!-- markmap: fold -->
### 🧪 Prefix sum + hash template
```text
seen = {0: 1}     # or {0: -1} for longest-length variants
prefix = 0
for x in nums:
  prefix += x
  ans += seen.get(prefix - target, 0)
  seen[prefix] = seen.get(prefix, 0) + 1
return ans
```

### prefix_sum_subarray_sum_equals_k
- **Anchor problems**
  - [ ] 🔥 [LeetCode 560 - Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/description/) (M) - Subarray Sum Equals K

### prefix_sum_longest_balance
- **Anchor problems**
  - [ ] 🔥 [LeetCode 525 - Contiguous Array](https://leetcode.com/problems/contiguous-array/description/) (M) - Contiguous Array

---

## 🔗 Linked lists

## 🔀 MergeSortedSequences (API Kernel)
- **Inputs**: two sorted linked lists/arrays; possibly in-place merge
- **Output shape**: merged sequence/list
- **Invariant**: output prefix is fully merged and sorted
- **Failure modes / when not to use**: if not sorted, need sort or different approach
- **Summary**: merge two sorted sequences using two pointers
- **When it wins**: stable linear merge, $O(m+n)$

<!-- markmap: fold -->
### 🧪 Merge pseudocode template
```text
dummy = Node()
tail = dummy
while a and b:
  take smaller; tail.next = taken; tail = tail.next
tail.next = a or b
return dummy.next
```

### merge_two_sorted_lists
- [ ] ⭐ [LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py) (E) - Merge Two Sorted Lists

### merge_two_sorted_arrays
- [ ] ⭐ [LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py) (E) - Merge Sorted Array

### merge_sorted_from_ends
- **Trick**: compare from ends to avoid extra space / handle transforms (squares)
- [ ] ⭐ [LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py) (E) - Squares of a Sorted Array

## 🐢🐇 FastSlowPointers (API Kernel)
- **Inputs**: linked list or implicit function `next(x)`
- **Output shape**: boolean cycle, node (cycle start), midpoint, palindrome check helper
- **Invariant**: fast moves 2 steps, slow moves 1 step; meeting implies cycle
- **Failure modes / when not to use**: pointer null checks; list mutation can break assumptions
- **Summary**: two pointers at different speeds for cycle detection / midpoint
- **Key theorem**: if a cycle exists, fast meets slow in $O(n)$

<!-- markmap: fold -->
### 🧪 Fast/slow template
```text
slow = fast = head
while fast and fast.next:
  slow = slow.next
  fast = fast.next.next
  if slow == fast: cycle_found
```

### fast_slow_cycle_detect
- [ ] ⭐ [LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py) (E) - Linked List Cycle

### fast_slow_cycle_start
- **Phase 2**: reset one pointer to head, move both at speed 1
- [ ] ⭐ [LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py) (M) - Linked List Cycle II

### fast_slow_implicit_cycle
- **Implicit graph**: next(x) defines edges
- [ ] ⭐ [LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py) (H) - Happy Number

### fast_slow_midpoint
- **Use**: split list / find middle
- [ ] ⭐ [LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py) (E) - Middle of the Linked List

### fast_slow_palindrome_via_reverse
- **Recipe**: find mid → reverse 2nd half → compare → (optional) restore
- [ ] 🔥 [LeetCode 234 - Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/description/) (E) - Palindrome Linked List

## 🔁 LinkedListReversal (API Kernel)
- **Inputs**: singly linked list; segment bounds or group size `k`
- **Output shape**: new head (and/or modified list)
- **Invariant**: reversed prefix points back to previous nodes; remaining suffix preserved
- **Failure modes / when not to use**: off-by-one around segment boundaries; losing `next` pointer; restoring list if required
- **Summary**: in-place reversal via pointer surgery (local rewiring)

<!-- markmap: fold -->
### 🧪 Reverse template (iterative)
```text
prev = None
cur = head
while cur:
  nxt = cur.next
  cur.next = prev
  prev = cur
  cur = nxt
return prev
```

### linked_list_full_reversal
- [ ] ⭐ [LeetCode 206 - Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/description/) (E) - Reverse Linked List

### linked_list_partial_reversal
- [ ] ⭐ [LeetCode 92 - Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/description/) (M) - Reverse Linked List II

### linked_list_k_group_reversal
- [ ] 🔥 [LeetCode 25 - Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py) (H) - Reverse Nodes in k-Group

---

## 🏔️ Heaps / selection / merging streams

## 🧺 KWayMerge (API Kernel)
- **Inputs**: K sorted lists/arrays/streams
- **Output shape**: merged sorted output / single list
- **Invariant**: heap contains next candidate from each list (or each non-empty list)
- **Failure modes / when not to use**: forgetting to push next after pop; unstable if you need stable tie-breaking
- **Summary**: merge K sorted sequences using heap or divide-and-conquer
- **Two standard strategies**
  - **Min-heap**: push heads, pop+advance ⇒ $O(N \log K)$
  - **Divide & conquer**: pairwise merge ⇒ $O(N \log K)$
- **Example use in production**: merge sorted shard results; streaming merge in search/index pipelines
- **See also**: HeapTopK (same heap mechanics)

<!-- markmap: fold -->
### 🧪 K-way merge (heap) template
```text
heap = []
push (value, list_id, node_ptr) for each non-empty list
while heap:
  v, i, node = heappop(heap)
  output.append(v)
  if node.next: heappush(heap, (node.next.val, i, node.next))
return output
```

### merge_k_sorted_heap
- [ ] 🔥 [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py) (H) - Merge k Sorted Lists

### merge_k_sorted_divide
- [ ] 🔥 [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py) (H) - Merge k Sorted Lists

### merge_two_sorted (also appears in answer-space problems)
- [ ] 🧊 [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py) (H) - Median of Two Sorted Arrays

## 🏔️ HeapTopK (API Kernel)
- **Inputs**: stream/array; `k`; sometimes comparator
- **Output shape**: kth element or list of top-k
- **Invariant**: heap stores current best candidates (size ≤ k)
- **Failure modes / when not to use**: using wrong heap orientation; forgetting to cap size k
- **Summary**: maintain top K / kth using heap
- **Rule of thumb**
  - `min_heap` of size K for **top K largest**
  - `max_heap` of size K for **top K smallest**
- **Anchor problems**
  - [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) (M) - Kth Largest Element in an Array (dual-approach: heap vs quickselect)
  - [ ] ⭐ [LeetCode 347 - Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/description/) (M) - Top K Frequent Elements

---

## 🌐 Graph / grid

## 🌊 GridBFSMultiSource (API Kernel)
- **Inputs**: grid; multiple starting cells (“sources”)
- **Output shape**: minimum time/steps to reach all, distance matrix, or unreachable indicator
- **Invariant**: queue holds frontier of increasing distance (unweighted); first time visiting a cell is shortest time
- **Failure modes / when not to use**: marking visited late (on dequeue) causes duplicates; miscounting levels/time
- **Summary**: multi-source BFS wavefront propagation on grid graph
- **State**: `queue`, visited, distance/time layers
- **Example use in production**: propagation in grids: distance transforms, flood fill of influence

<!-- markmap: fold -->
### 🧪 Multi-source BFS template
```text
q = deque(all_sources)
mark visited on enqueue
dist = 0
while q:
  for _ in range(len(q)):     # level by level
    r,c = q.popleft()
    for nr,nc in neighbors(r,c):
      if not visited:
        visited = True
        q.append((nr,nc))
  dist += 1
```

### grid_bfs_propagation
- **Notes**
  - Initialize queue with **all** sources
  - Track counts (e.g., fresh nodes) to detect impossible cases
  - Process level-by-level to increment time/distance cleanly
  - Mark visited on **enqueue**
- [ ] ⭐ [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py) (M) - Rotting Oranges
- [ ] 🔥 [LeetCode 542 - 01 Matrix](https://leetcode.com/problems/01-matrix/description/) (M) - 01 Matrix

## 🚦 GraphBFSShortestPath (API Kernel)
- **Inputs**: graph (adjacency list); unweighted edges; start/target
- **Output shape**: shortest distance, path length, or path reconstruction
- **Invariant**: queue holds frontier of increasing distance; first time reaching node is shortest
- **Failure modes / when not to use**: weighted edges need Dijkstra; visited-on-enqueue to avoid blowup
- **Summary**: BFS shortest path on general graphs (not just grids)

<!-- markmap: fold -->
### 🧪 Graph BFS template
```text
q = deque([start])
dist = {start: 0}
while q:
  u = q.popleft()
  if u == target: return dist[u]
  for v in adj[u]:
    if v not in dist:
      dist[v] = dist[u] + 1
      q.append(v)
return -1
```

### bfs_shortest_path
- [ ] 🔥 [LeetCode 127 - Word Ladder](https://leetcode.com/problems/word-ladder/description/) (H) - Word Ladder

---

## 🧭 Search / enumeration

## 🧭 BacktrackingExploration (API Kernel)
- **Inputs**: choice set / constraints; often need all solutions
- **Output shape**: list of solutions, count, or boolean exists
- **Invariant**: ==state matches current path exactly==
- **Failure modes / when not to use**: missing pruning causes exponential blowups; duplicates without dedup rules
- **Summary**: exhaustive search with pruning; rhythm: **Choose → Explore → Unchoose**
- **Note**: most backtracking is exponential; win condition is pruning/constraints; be ready to justify pruning and bounds

<!-- markmap: fold -->
### 🧪 Backtracking template
```text
def dfs(state):
  if is_solution(state): record; return
  for choice in choices(state):
    apply(choice)
    if feasible(state): dfs(state)
    undo(choice)
```

<!-- markmap: fold -->
### ✅ Backtracking “shape” cheat sheet
| Shape | What you track | Canonical trick | Anchor |
|------|-----------------|-----------------|--------|
| Permutation | `used[]` | each element once | 🔥 [LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py) (M) - Permutations |
| Permutation + dup | `used[]` + sort | skip if prev unused | ⭐ [LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py) (M) - Permutations II |
| Subset | `start_index` | collect every node | ⭐ [LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py) (M) - Subsets |
| Subset + dup | `start_index` + sort | same-level skip | ⭐ [LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py) (M) - Subsets II |
| Combination | `start_index` + size | stop when size==k | ⭐ [LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py) (M) - Combinations |
| Target sum | `remaining` | prune remaining<0 | ⭐ [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) (M) - Combination Sum /40/216 |
| Constraint sat. | constraint sets | propagate constraints | 🔥 [LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py) (H) - N-Queens /52 |
| Grid path | visited mark | undo on return | ⭐ [LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py) (M) - Word Search |
| String cuts | cut positions | validate segment | ⭐ [LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py) (M) - Restore IP Addresses /131 |

### backtracking_permutation
- [ ] 🔥 [LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py) (M) - Permutations

### backtracking_permutation_dedup
- [ ] ⭐ [LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py) (M) - Permutations II

### backtracking_subset
- [ ] ⭐ [LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py) (M) - Subsets

### backtracking_subset_dedup
- [ ] ⭐ [LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py) (M) - Subsets II

### backtracking_combination
- **Fixed size k**
  - [ ] ⭐ [LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py) (M) - Combinations
  - [ ] ⭐ [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) (M) - Combination Sum
  - [ ] ⭐ [LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py) (M) - Combination Sum II
  - [ ] ⭐ [LeetCode 216 - Combination Sum III](https://leetcode.com/problems/combination-sum-iii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py) (M) - Combination Sum III

### backtracking_n_queens (constraint satisfaction)
- **Constraints**: cols, diag (row-col), anti-diag (row+col)
- [ ] 🔥 [LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py) (H) - N-Queens
- [ ] ⭐ [LeetCode 52 - N-Queens II](https://leetcode.com/problems/n-queens-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py) (H) - N-Queens II

### backtracking_grid_path
- **Visited marking**: in-place `'#'` or `set()`
- [ ] ⭐ [LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py) (M) - Word Search

### backtracking_string_segmentation
- **Segment validity + pruning by remaining length**
- [ ] ⭐ [LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py) (M) - Restore IP Addresses
- [ ] ⭐ [LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py) (M) - Palindrome Partitioning

---

## 🌳 Trees / DFS

## 🌲 DFSTraversal (API Kernel)
- **Inputs**: tree (binary/n-ary) or grid/graph for DFS-style traversal
- **Output shape**: aggregated value (height), boolean, paths, component count, LCA node
- **Invariant**: recursion/stack maintains call path; each node processed once (tree) or once with visited (graph)
- **Failure modes / when not to use**: missing visited in graphs; recursion depth in deep trees
- **Summary**: depth-first traversal patterns (preorder/inorder/postorder), plus common queries

<!-- markmap: fold -->
### 🧪 Tree DFS template
```text
def dfs(node):
  if not node: return base
  left = dfs(node.left)
  right = dfs(node.right)
  return combine(node, left, right)
```

### dfs_tree_height
- [ ] 🔥 [LeetCode 104 - Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/) (E) - Maximum Depth of Binary Tree

### dfs_invert_tree
- [ ] ⭐ [LeetCode 226 - Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/description/) (E) - Invert Binary Tree

### dfs_island_counting
- [ ] 🔥 [LeetCode 200 - Number of Islands](https://leetcode.com/problems/number-of-islands/description/) (M) - Number of Islands

### dfs_lca
- [ ] 🔥 [LeetCode 236 - Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/description/) (M) - Lowest Common Ancestor of a Binary Tree

---

## 🔗 Compositions (kernels used together)
- Sort + `TwoPointersTraversal` (3Sum)
- `TwoPointerPartition` + `HeapTopK` (hybrid selection/top-k workflows)
- BFS + `BinarySearchBoundary` (time feasibility via predicate; common in scheduling variants)

## 🧩 Starter Packs (pick one roadmap slice)

### 🎯 Sliding Window Track (~6 problems, 2–4 hours)
- [ ] 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) (H) - Minimum Window Substring
- [ ] 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) (M) - Longest Substring Without Repeating Characters
- [ ] ⭐ [LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) (M) - Permutation in String
- [ ] ⭐ [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) (M) - Find All Anagrams in a String
- [ ] ⭐ [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) (H) - Longest Substring with At Most K Distinct Characters
- [ ] ⭐ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) (M) - Minimum Size Subarray Sum

### 👈👉 Two Pointers & Partition Track (~8 problems, 2–4 hours)
- [ ] ⭐ [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py) (E) - Remove Duplicates from Sorted Array
- [ ] ⭐ [LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py) (M) - Remove Duplicates from Sorted Array II
- [ ] ⭐ [LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py) (E) - Remove Element
- [ ] ⭐ [LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) (E) - Move Zeroes
- [ ] 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) (M) - Container With Most Water
- [ ] 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py) (M) - 3Sum
- [ ] ⭐ [LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py) (M) - 3Sum Closest
- [ ] ⭐ [LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py) (M) - Sort Colors

### 🧭 Backtracking Track (~6–8 problems, 2–4 hours)
- [ ] ⭐ [LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py) (M) - Subsets
- [ ] ⭐ [LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py) (M) - Combinations
- [ ] 🔥 [LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py) (M) - Permutations
- [ ] ⭐ [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) (M) - Combination Sum
- [ ] ⭐ [LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py) (M) - Combination Sum II
- [ ] 🔥 [LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py) (H) - N-Queens
- [ ] ⭐ [LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py) (M) - Word Search
- [ ] ⭐ [LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py) (M) - Restore IP Addresses

### 🔗 Linked List Track (~6–8 problems, 2–4 hours)
- [ ] ⭐ [LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py) (E) - Merge Two Sorted Lists
- [ ] ⭐ [LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py) (E) - Linked List Cycle
- [ ] ⭐ [LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py) (M) - Linked List Cycle II
- [ ] ⭐ [LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py) (E) - Middle of the Linked List
- [ ] ⭐ [LeetCode 206 - Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/description/) (E) - Reverse Linked List
- [ ] ⭐ [LeetCode 92 - Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/description/) (M) - Reverse Linked List II
- [ ] 🔥 [LeetCode 25 - Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py) (H) - Reverse Nodes in k-Group
- [ ] 🔥 [LeetCode 234 - Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/description/) (E) - Palindrome Linked List

### 🏔️ Heap & Merge Track (~6–8 problems, 2–4 hours)
- [ ] 🔥 [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py) (H) - Merge k Sorted Lists
- [ ] ⭐ [LeetCode 347 - Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/description/) (M) - Top K Frequent Elements
- [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) (M) - Kth Largest Element in an Array
- [ ] ⭐ [LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py) (E) - Squares of a Sorted Array
- [ ] ⭐ [LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py) (E) - Merge Sorted Array
- [ ] 🔥 [LeetCode 33 - Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/description/) (M) - Search in Rotated Sorted Array
- [ ] 🔥 [LeetCode 34 - Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/description/) (M) - Find First and Last Position of Element in Sorted Array
- [ ] 🧊 [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py) (H) - Median of Two Sorted Arrays

---

## ✅ Ontology kernels not yet in this map (TODO)
- [ ] UnionFindConnectivity
- [ ] TreeTraversalBFS
- [ ] DPSequence
- [ ] DPInterval
- [ ] TopologicalSort
- [ ] TriePrefixSearch

## 🧾 Still to add (scope reminders)
- DP, Union-Find, Trie, Segment Tree/Fenwick, Topological sort, Dijkstra
---
title: Sliding Window & Two Pointers – Integrated Mastery Map
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

# Sliding Window & Two Pointers Mastery Map 🎯

## ✅ Learning Dashboard

- [ ] Understand **core API kernels**
- [ ] Learn **canonical templates**
- [ ] Map patterns → **LeetCode problems**
- [ ] Practice via **roadmaps** (NeetCode / Blind 75)
- [ ] Build **implementation muscle** (from snippets)

---

## 1. Core API Kernels 🔌

- **SubstringSlidingWindow**
  - 1D window state machine over sequences with dynamic invariants
  - Key idea: maintain `[left, right]` and a **state** that can be updated in O(1)
- **TwoPointersTraversal**
  - Two coordinated pointers moving over a sequence while preserving an invariant
- **FastSlowPointers**
  - Two pointers with different speeds (cycle detection, midpoint)
- **TwoPointerPartition**
  - Partition array in-place using multiple pointers (Dutch flag, quickselect)
- **MergeSortedSequences**
  - Merge two sorted sequences using two pointers

---

## 2. Sliding Window Patterns 🪟

> API Kernel: **SubstringSlidingWindow**

### 2.1 Core Concepts

- **Invariant-based window**
  - Maintain a condition on substring/subarray `[left, right]`
  - Expand `right` → add element
  - Contract `left` → remove element until invariant holds
- **Strategies**
  - **Maximize** window (longest / largest)
  - **Minimize** window (shortest satisfying constraint)
  - **Fixed size** window

#### Canonical Template (variable size)

```python
left = 0
state = init_state()
ans = init_answer()

for right, x in enumerate(seq):
    add(state, x)          # expand
    
    while invalid(state):  # contract
        remove(state, seq[left])
        left += 1
    
    ans = update(ans, left, right, state)
```

---

### 2.2 Pattern: Unique Window (All Elements Unique)

- ID: `sliding_window_unique`
- Invariant: all elements in window are **unique**
- State: `last_seen_index` or frequency map
- Complexity: $O(n)$ time, $O(\sigma)$ space

#### Key Problem 🎯

- [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - Topics: string, hash table, sliding window
  - Roadmaps: NeetCode 150, Blind 75, Grind 75, LeetCode Top 100, Sliding Window Path
  - Pattern: `sliding_window_unique`
  - Family: `substring_window`

#### Implementation Snippet

```python
def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

---

### 2.3 Pattern: At Most K Distinct

- ID: `sliding_window_at_most_k_distinct`
- Invariant: number of distinct characters ≤ K
- State: frequency map, `len(freq) <= K`
- Strategy: **maximize** window

#### Key Problem 🎯

- [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - Topics: string, hash table, sliding window
  - Roadmap: Sliding Window Path

#### Snippet

```python
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    if k == 0: return 0
    freq = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        freq[ch] = freq.get(ch, 0) + 1
        while len(freq) > k:
            left_ch = s[left]
            freq[left_ch] -= 1
            if freq[left_ch] == 0:
                del freq[left_ch]
            left += 1
        best = max(best, right - left + 1)
    return best
```

---

### 2.4 Pattern: Frequency Cover (Need/Have Maps)

- ID: `sliding_window_freq_cover`
- Invariant: window covers **all required character frequencies**
- State:
  - `need_frequency`
  - `have_frequency`
  - `chars_satisfied` vs `chars_required`
- Strategies:
  - **Minimize** window (substring cover)
  - **Fixed size** window (permutation/anagram)

#### Problems 🎯

- [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - Goal: **minimum** window containing all chars of `t`
  - Pattern: `sliding_window_freq_cover`
  - Strategy: expand until valid, then contract while valid
- [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - Goal: all start indices where window is an anagram of `p`
  - Fixed window size = `len(p)`
- [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
  - Goal: does any window of size `len(s1)` in `s2` match `s1`'s frequency?

---

### 2.5 Pattern: Cost-Bounded Window (Numeric Sum)

- ID: `sliding_window_cost_bounded`
- Invariant: numeric cost (e.g., sum) satisfies constraint
- Typical: sum ≥ target or sum ≤ target

#### Key Problem 🎯

- [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
  - Invariant: `window_sum >= target`
  - Strategy: **minimize** window length
  - State: single integer `window_sum`

```python
while window_sum >= target:
    best = min(best, right - left + 1)
    window_sum -= nums[left]
    left += 1
```

---

### 2.6 Sliding Window Comparison Table 📋

| Problem | Invariant | State | Window Size | Goal |
|--------|-----------|-------|-------------|------|
| [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | All unique | `last_seen` map | Variable | Maximize |
| [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | ≤ K distinct | Frequency map | Variable | Maximize |
| [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | Covers `t` with freq | Need/Have maps | Variable | Minimize |
| [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | Exact match | Frequency map | Fixed | Exists? |
| [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | Exact match | Frequency map | Fixed | All positions |
| [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | Sum ≥ target | Integer sum | Variable | Minimize |

---

### 2.7 When to Use Sliding Window ❓

- ✅ Use when:
  - Answer is about a **contiguous** substring/subarray
  - State can be updated in **O(1)** when adding/removing ends
  - You need **min/max length/value** of such a window
- ❌ Avoid when:
  - Elements are not contiguous (prefer DP / combinatorics)
  - Property is not incrementally maintainable

---

## 3. Two Pointers Patterns ➿

> API Kernel: **TwoPointersTraversal**

### 3.1 Family Overview

| Sub-Pattern | Pointer Movement | Primary Use |
|-------------|------------------|------------|
| **Opposite Pointers** | `left →`, `right ←` | Sorted arrays, palindromes, optimizations |
| **Same-Direction (Writer)** | `write →`, `read →` | In-place modification |
| **Fast–Slow Pointers** | `slow →`, `fast →→` | Cycle detection, midpoints |
| **Partitioning** | 2–3 pointers | Dutch flag, quickselect |
| **Merge Pattern** | multiple → | Merge sorted sequences |

---

### 3.2 Opposite Pointers (Two-End)

- Pattern IDs:
  - `two_pointer_opposite`
  - `two_pointer_opposite_search`
  - `two_pointer_opposite_palindrome`
  - `two_pointer_opposite_maximize`
- Invariant: solution space within `[left, right]`
- Requirements: usually **sorted** or **symmetric** structure

#### Template

```python
left, right = 0, n - 1
while left < right:
    val = compute(arr, left, right)
    if val == target:
        return handle(...)
    elif val < target:
        left += 1
    else:
        right -= 1
```

#### Example Problem 🎯

- [LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
  - Data uses `two_pointer_opposite` pattern (though classic solution is hash map)
  - Family: `two_sum_variants`
  - Algorithms: `two_pointers`
  - Companies: Google, Amazon, Meta, Microsoft, Apple, Bloomberg, Adobe
  - Roadmaps: NeetCode 150, Blind 75, Grind 75, LeetCode Top 100

> For sorted variant, see (not in dataset, but conceptually) “Two Sum II”.

---

### 3.3 Same-Direction Pointers (Writer Pattern)

- Pattern IDs:
  - `two_pointer_same_direction`
  - `two_pointer_writer_dedup`
  - `two_pointer_writer_remove`
  - `two_pointer_writer_compact`
- Invariant: `arr[0:write]` is the **clean / valid** prefix
- Use when:
  - Need **in-place** array modifications
  - Remove elements, deduplicate, compact

#### Template

```python
write = 0
for read in range(len(arr)):
    if keep(arr[read]):
        arr[write] = arr[read]
        write += 1
return write
```

---

### 3.4 Fast–Slow Pointers (Floyd’s Cycle Detection)

- Pattern IDs:
  - `fast_slow_cycle_detect`
  - `fast_slow_cycle_start`
  - `fast_slow_midpoint`
  - `fast_slow_implicit_cycle`
- Use for:
  - Linked list **cycle detection**
  - Finding **cycle start**
  - **Middle** of linked list
  - Implicit sequences (e.g., happy number)

#### Template (cycle exists?)

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True
return False
```

---

### 3.5 Partitioning / Dutch Flag

- Pattern IDs:
  - `dutch_flag_partition`
  - `two_way_partition`
  - `quickselect_partition`
- Kernel: **TwoPointerPartition**
- Use for:
  - Grouping elements by pivot / property
  - Quickselect `k`-th element
  - Sort colors (0/1/2)

#### Dutch Flag Template

```python
low, mid, high = 0, 0, n - 1
while mid <= high:
    if arr[mid] < pivot:
        arr[low], arr[mid] = arr[mid], arr[low]
        low += 1; mid += 1
    elif arr[mid] > pivot:
        arr[mid], arr[high] = arr[high], arr[mid]
        high -= 1
    else:
        mid += 1
```

---

### 3.6 Merge Pattern

- Pattern IDs:
  - `merge_two_sorted`
  - `merge_two_sorted_arrays`
  - `merge_sorted_from_ends`
- Kernel: **MergeSortedSequences**, **KWayMerge**
- Use for:
  - Merging sorted arrays/lists
  - Building more complex merges (e.g., median of two sorted arrays)

#### Key Problems 🎯

- [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
  - Patterns: `binary_search_on_answer`, `merge_two_sorted`
  - Families: `merge_sorted`, `binary_search_answer`
- [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - Patterns: `merge_k_sorted_heap`, `merge_k_sorted_divide`
  - Kernel: `KWayMerge`

---

## 4. Backtracking & Other Kernels (Context) 🧠

### 4.1 BacktrackingExploration

- Patterns:
  - `backtracking_permutation`
  - `backtracking_combination`
  - `backtracking_subset`
  - `backtracking_n_queens`
  - `backtracking_sudoku`

#### Key Problem 🎯

- [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - Family: `backtracking_combinatorial`
  - Data structures: array, hash_set
  - Algorithm: backtracking

---

### 4.2 LinkedListInPlaceReversal

- Patterns:
  - `linked_list_k_group_reversal`
  - `linked_list_full_reversal`
  - `linked_list_partial_reversal`

#### Problems 🎯

- [LeetCode 2 - Add Two Numbers](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py)
  - Family: `linked_list_manipulation`
- [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
  - Pattern: `linked_list_k_group_reversal`

---

### 4.3 GridBFSMultiSource

- Pattern: `grid_bfs_propagation`
- Use: multi-source BFS wavefront on a grid

#### Key Problem 🎯

- [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
  - Families: `graph_wavefront`, `matrix_traversal`
  - Data structures: grid, queue
  - Algorithm: BFS

---

## 5. Data Structures & Algorithms Backbone 🧩

### 5.1 Data Structures (used heavily here)

- **array**, **string**
- **hash_map**, **hash_set**, **counter**
- **queue** (for BFS)
- **linked_list**
- **grid** (matrix as implicit graph)
- **min_heap** (K-way merge, top-K)
- **monotonic_stack / monotonic_deque** (for other patterns)

### 5.2 Algorithmic Paradigms

- Techniques:
  - `two_pointers`
  - `sliding_window`
  - `prefix_sum`
  - `monotonic_stack`
  - `union_find`
- Paradigms:
  - `greedy`
  - `dynamic_programming`
  - `divide_and_conquer`
  - `backtracking`

---

## 6. Roadmaps & Practice Paths 🗺️

### 6.1 Sliding Window Mastery Path

- Roadmap: `sliding_window_path` (Sliding Window Mastery)
- Recommended progression:
  1. [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) – base template
  2. [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) – distinct count
  3. [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) – numeric cost
  4. [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) – cover + minimize
  5. [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) – fixed window, existence
  6. [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) – fixed window, enumeration

---

### 6.2 Two Pointers Mastery Path

- Roadmap: `two_pointers_path` (Two Pointers Mastery)
- Example progression (using dataset + standard problems):
  1. [LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py) – opposite pointers logic (conceptually for sorted)
  2. Merge-style: [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
  3. K-way merge: [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  4. Linked list manipulation: [LeetCode 2 - Add Two Numbers](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py), [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)

---

## 7. Interview-Focused Problem Set 💼

- **High-frequency (NeetCode 150 / Blind 75 / Grind 75) from dataset**
  - [LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
  - [LeetCode 2 - Add Two Numbers](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py)
  - [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
  - [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
  - [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
  - [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
  - [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

---

## 8. Quick Template Reference 📌

<!-- markmap: fold -->

- **Maximize Window**

```python
def maximize_window(seq):
    state = {}
    left = 0
    best = 0
    for right, x in enumerate(seq):
        add(state, x)
        while not valid(state):
            remove(state, seq[left])
            left += 1
        best = max(best, right - left + 1)
    return best
```

- **Minimize Window**

```python
def minimize_window(seq):
    state = {}
    left = 0
    best = float('inf')
    for right, x in enumerate(seq):
        add(state, x)
        while valid(state):
            best = min(best, right - left + 1)
            remove(state, seq[left])
            left += 1
    return 0 if best == float('inf') else best
```

- **Fixed Size Window**

```python
def fixed_window(seq, k):
    state = {}
    ans = []
    for right, x in enumerate(seq):
        add(state, x)
        if right >= k:
            remove(state, seq[right - k])
        if right >= k - 1 and valid(state):
            ans.append(process(state))
    return ans
```

- **Opposite Pointers**

```python
def opposite_pointers(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        cur = arr[left] + arr[right]
        if cur == target:
            return left, right
        if cur < target:
            left += 1
        else:
            right -= 1
```

---

## 9. Suggested Next Steps 🚀

- Pick a path:
  - **Sliding Window Path** → work through 3, 340, 209, 76, 567, 438
  - **Two Pointers Path** → 1, 4, 23, 2, 25
- For each problem:
  - Identify:
    - API kernel
    - Pattern ID
    - Invariant
    - State representation
  - Then implement from the **appropriate template** above.
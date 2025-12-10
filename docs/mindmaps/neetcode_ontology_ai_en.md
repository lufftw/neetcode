---
title: Sliding Window & BFS API Kernels – LeetCode-Oriented Mind Map
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

# 🔧 Core API Kernels → Problems

## 🪟 SubstringSlidingWindow (Sliding Window over 1D sequences)

- **Idea**: Maintain window `[left, right]` with an ==invariant==  
- **Key Uses**: substrings / subarrays, min/max length, existence of pattern  
- **Time**: Typically $O(n)$, each index enters/leaves window at most once

### 🎛 Canonical Template

- **Universal structure**
  - State structure (map / counter / sum)
  - Expand `right` each step
  - Contract `left` while invariant violated (or while still valid for minimization)
  - Update answer when window valid
- **Maximize vs Minimize**
  - Maximize: record best when window valid after contraction
  - Minimize: contract while valid, record smallest window
- **Reference Snippet**
  - See *Template Quick Reference* section in docs
  - Maximize / Minimize / Fixed-size templates

### 📌 Core Pattern Variants

- **sliding_window_unique**
  - Invariant: all elements in window are **unique**
  - State: `last_seen_index` or frequency map
  - Typical goal: **maximize** window length
- **sliding_window_at_most_k_distinct**
  - Invariant: `#distinct ≤ K`
  - State: frequency map + `len(map)`
  - Goal: **maximize** length
- **sliding_window_freq_cover**
  - Invariant: window **covers** required frequencies (`have >= need`)
  - State: `need` + `have` maps; `matched == required`
  - Goals:
    - minimize window that covers all
    - or detect / collect exact frequency matches (anagrams, permutations)
- **sliding_window_cost_bounded**
  - Invariant: numeric **cost/sum constraint** (e.g. `sum ≥ target` or `≤ target`)
  - State: running sum / cost
  - Goal: often **minimize** length
- **sliding_window_fixed_size**
  - Invariant: `window_size == K`
  - State: frequency / sum / custom
  - Goal: aggregate / check condition for every fixed-length window

### 🧠 Mental Model

- **When to use**:
  - Answer is a **contiguous** substring/subarray
  - Property can be updated in **O(1)** when adding/removing ends
  - You want **min / max / existence** of such a window
- **When not to use**:
  - Non-contiguous subsequences → DP / combinatorics
  - Need arbitrary range queries → prefix sum, segment tree
  - State update is expensive / non-local

---

## 🧩 Sliding Window Problems (with GitHub Solutions)

### ⭐ Base Template: Unique Characters

- [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) 🎯
  - **Pattern**: `sliding_window_unique`
  - **Family**: `substring_window`
  - **Topics**: string, hash table, sliding window
  - **Goal**: ==maximize== length of valid window
  - **State**: `last_seen_index[char]`
  - **Trick**: **jump** `left` to `last_seen_index[char] + 1` instead of while-loop

#### ✅ Learning Checklist (Unique Window)

- [ ] Understand **jump vs while** contraction
- [ ] Be able to derive **O(n)** proof
- [ ] Re-implement from memory in 5–7 minutes
- [ ] Adapt to **“longest substring without more than K repeats”** style variants

---

### 🎯 Frequency Cover & Exact Match Variants

#### 1. Minimum Window Cover

- [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) 🔴
  - **Patterns**: `sliding_window_freq_cover`
  - **Goal**: ==minimize== window that **contains all chars of `t` with required counts**
  - **State**:
    - `need_frequency`: counts from `t`
    - `have_frequency`: counts in current window
    - `chars_satisfied`, `chars_required`
  - **Flow**:
    - Expand `right` until `chars_satisfied == chars_required`
    - While valid, **contract** `left` to minimize length and update best answer

- Typical pitfalls
  - Off-by-one when tracking best window `[start, end]`
  - Only increment `chars_satisfied` when `have == need` (not `>`)

#### 2. All Anagrams in a String

- [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) 🟠
  - **Patterns**: `sliding_window_freq_cover` + `sliding_window_fixed_size`
  - **Goal**: find **all start indices** where window is an anagram of `p`
  - **State**:
    - Fixed window size = `len(p)`
    - `pattern_frequency`, `window_frequency`
    - `chars_matched`, `chars_to_match`
  - **Flow**:
    - Expand `right`
    - Once window size > `len(p)`, remove leftmost
    - When window size == `len(p)` and `chars_matched == chars_to_match` → record index

#### 3. Permutation Existence

- [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) 🟠
  - **Patterns**: `sliding_window_freq_cover` + `sliding_window_fixed_size`
  - **Goal**: does **any** window of size `len(s1)` in `s2` have **exact same frequencies**?
  - **Same template** as anagrams, but:
    - Return `True` on first match
    - Fixed-size window; frequency maps + matched count

#### ✅ Learning Checklist (Freq Cover / Exact Match)

- [ ] Implement **min window cover** (LeetCode 76) from scratch
- [ ] Implement **fixed-size anagram finder** (LeetCode 438 / 567)
- [ ] Explain difference between:
  - **cover**: `have[c] >= need[c]`
  - **exact**: `have[c] == need[c]`
- [ ] Convert between “return all indices” vs “return boolean”

---

### 🎯 At Most K Distinct Characters

- [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) 🟠
  - **Pattern**: `sliding_window_at_most_k_distinct`
  - **Goal**: ==maximize== length while `distinct ≤ K`
  - **State**: `char_frequency` map
  - **Flow**:
    - Expand `right`, update map
    - While `len(char_frequency) > K`, increment `left` and decrement/remove chars
    - Update `max_length` on every valid window

#### ✅ Learning Checklist (K Distinct)

- [ ] Understand why **incremental contraction** (while-loop) is required (no jump)
- [ ] Be able to adapt for **“at least K distinct”** or **“exactly K distinct”**
- [ ] Practice on both:
  - [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)

---

### 🎯 Numeric Cost / Sum-Bounded Window

- [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) 🟠
  - **Pattern**: `sliding_window_cost_bounded`
  - **Goal**: ==minimize== length of subarray with `sum ≥ target`
  - **State**: single integer `window_sum`
  - **Flow**:
    - Expand `right`, `window_sum += nums[right]`
    - While `window_sum ≥ target`:
      - Update `min_length`
      - Contract `left`, `window_sum -= nums[left]`
  - **Assumption**: array of **positive** integers → monotonicity enables sliding window

#### ✅ Learning Checklist (Cost-Bounded)

- [ ] Recognize when **positivity** of numbers allows sliding window
- [ ] Know alternative (prefix sum + binary search) when negatives appear
- [ ] Implement LeetCode 209 in < 7 minutes from memory

---

### 📊 Sliding Window Pattern Comparison

<!-- markmap: fold -->
- **Pattern Comparison Table**

  | Problem | Invariant | State | Window Size | Goal |
  |---------|-----------|-------|-------------|------|
  | [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | All unique | `last_index` map | Variable | Maximize |
  | [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | ≤K distinct | Frequency map | Variable | Maximize |
  | [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | Contains all of t | Need/Have maps | Variable | Minimize |
  | [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | Exact match | Frequency map | Fixed | Exists? |
  | [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | Exact match | Frequency map | Fixed | All positions |
  | [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | Sum ≥ target | Integer sum | Variable | Minimize |

---

## 🧭 Sliding Window Learning Roadmap

- **Roadmaps referencing sliding window problems**
  - `sliding_window_path` – Sliding Window Mastery
    - Contains: 3, 76, 209, 340, 438, 567
  - `neetcode_150`
  - `blind_75`
  - `grind_75`
  - `leetcode_top_100`

### Suggested Order (for interview prep)

1. [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) — base template
2. [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) — numeric sum, minimize
3. [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) — at most K distinct
4. [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) — fixed size, exact match
5. [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) — multiple answers
6. [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) — hardest variant

---

## 🌊 GridBFSMultiSource (Multi-Source BFS on Grids)

- **Idea**: Treat grid as **implicit graph**, run BFS from **multiple sources simultaneously**
- **Use cases**:
  - Wavefront propagation (rot, infection, spreading)
  - Minimum steps to fill / reach all cells
  - Shortest paths in **unweighted** grid

### Core Patterns

- **grid_bfs_propagation**
  - Multi-source BFS, each level = **time step**
  - Common for “minutes to rot”, “days to spread”, etc.
- **bfs_shortest_path**
  - BFS on grid or adjacency list to compute **shortest path length**
- **bfs_level_order**
  - BFS on trees / graphs to process **level by level**

### 🧩 Representative Problem

- [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py) 🟠
  - **Patterns**: `grid_bfs_propagation`
  - **Families**: `graph_wavefront`, `matrix_traversal`
  - **Data structures**: `grid`, `queue`
  - **Algorithm**: BFS
  - **Flow**:
    - Push all **rotten** oranges into queue with time `0`
    - BFS over 4-direction neighbors, rotting adjacent fresh ones
    - Track minutes as BFS **level count**
    - If any fresh remain after BFS → return `-1`, else max time seen

### BFS Template (Grid)

```python
from collections import deque

def multi_source_bfs(grid, sources):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    seen = set()

    for r, c in sources:
        q.append((r, c, 0))  # (row, col, dist/time)
        seen.add((r, c))

    max_dist = 0
    while q:
        r, c, dist = q.popleft()
        max_dist = max(max_dist, dist)

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen:
                # Check problem-specific constraints here
                seen.add((nr, nc))
                q.append((nr, nc, dist + 1))

    return max_dist
```

### ✅ Learning Checklist (Grid BFS)

- [ ] Convert grid to **implicit graph** mentally (nodes = cells, edges = neighbors)
- [ ] Implement **multi-source BFS** template quickly
- [ ] Recognize wavefront problems:
  - “minimum time for X to spread”
  - “distance to nearest Y for every cell”
- [ ] Practice on:
  - [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

---

## 🔗 Other API Kernels Present in Problem Set

### 🔀 KWayMerge

- **Problems**
  - [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
  - [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
- **Patterns**
  - `merge_two_sorted`
  - `merge_k_sorted_heap`
  - `merge_k_sorted_divide`
- **Core ideas**
  - Merge 2 sorted sequences in O(n)
  - Use **min-heap** or **divide-and-conquer** to merge K lists
  - Binary search on partition (LeetCode 4) combined with merge logic

### 🔁 LinkedListInPlaceReversal

- **Problem**
  - [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- **Patterns**
  - `linked_list_k_group_reversal`
- **Core ideas**
  - Reverse sublists in place using pointer rewiring
  - Iterate in groups of k, reverse each group, connect segments

### 🧮 BacktrackingExploration

- **Problem**
  - [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
- **Patterns**
  - `backtracking_n_queens`
- **Core ideas**
  - Place queens row by row
  - Use sets for columns / diagonals to prune
  - Classic backtracking with constraint checks

---

## 🧱 Data Structures & Techniques Mapped

- **SubstringSlidingWindow**
  - Data structures: `string`, `array`, `hash_map`, `counter`
  - Algorithms: `two_pointers`, `sliding_window`
- **GridBFSMultiSource**
  - Data structures: `grid`, `queue`
  - Algorithms: `bfs`, `graph_traversal`
- **KWayMerge**
  - Data structures: `linked_list`, `min_heap`
  - Algorithms: `divide_and_conquer`, `heap`
- **LinkedListInPlaceReversal**
  - Data structures: `linked_list`
  - Algorithms: `recursion` / iterative pointer manipulation
- **BacktrackingExploration**
  - Data structures: `array`, `hash_set`
  - Algorithms: `backtracking`, `recursion`

---

## 📌 Interview-Focused Practice Board

- **Sliding Window Essentials**
  - [ ] [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [ ] [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
  - [ ] [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - [ ] [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
  - [ ] [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - [ ] [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
- **Grid BFS Core**
  - [ ] [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- **Merge & Linked List**
  - [ ] [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - [ ] [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
  - [ ] [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- **Backtracking**
  - [ ] [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
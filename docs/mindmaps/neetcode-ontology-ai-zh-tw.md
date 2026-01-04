---
title: LeetCode 核心 API Kernel × Pattern × 題單（45 題）總覽心智圖
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 目標導向導覽
- ==面試高頻==：**Sliding Window / Two Pointers / Backtracking / BFS / Heap / Binary Search**
- ==刷題策略==（建議順序）
  - [ ] **Two Pointers 基礎** → [ ] **Sliding Window** → [ ] **Backtracking** → [ ] **Heap/Quickselect** → [ ] **BFS 波前**
- 難度標記
  - 🟢 Easy / 🟠 Medium / 🔴 Hard

## 🧠 API Kernels（解題「引擎」）→ Patterns（子模板）→ 題目
<!-- markmap: fold -->
### 1) SubstringSlidingWindow（滑動視窗狀態機）📚
- **核心不變量（Invariant）**：維持一個可增量更新的視窗 `[L, R]`
- 複雜度：通常 $O(n)$（每個元素最多進出視窗一次）

#### ✅ Pattern 對照表（必背）
| Pattern | 不變量 | 視窗 | 常見 State | 目標 | 代表題 |
|---|---|---|---|---|---|
| sliding_window_unique | 全部唯一 | 變長 | `last_index` | 最大化 |[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) |
| sliding_window_at_most_k_distinct | distinct ≤ K | 變長 | `freq map` | 最大化 |[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) |
| sliding_window_freq_cover | 覆蓋需求頻率 | 變長/定長 | `need/have` | 最小化/存在/收集 |[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) / 567 / 438 |
| sliding_window_cost_bounded | sum ≥/≤ target | 變長 | `window_sum` | 最小化 |[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) |

#### sliding_window_unique（全唯一最大化）
- 🎯 題目
  - 🟠[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)

#### sliding_window_at_most_k_distinct（至多 K 種）
- 🎯 題目
  - 🟠[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)

#### sliding_window_freq_cover（頻率覆蓋 / 比對）
- 🎯 題目
  - 🔴 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)（最小覆蓋）
  - 🟠[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)（是否存在 permutation，==定長==）
  - 🟠[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)（收集所有 anagram 起點，==定長==）

#### sliding_window_cost_bounded（成本/和約束）
- 🎯 題目
  - 🟠[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)

### 2) TwoPointersTraversal（雙指針遍歷）⚡
- **核心不變量**：指針移動是「不可逆」的排除證明
- 常見形狀：相向 / 同向 Writer / 多重枚舉（3Sum）/ 合併

#### ✅ Pattern 對照表（速查）
| 子型 | 指針初始化 | 典型不變量 | 時間 | 代表題 |
|---|---|---|---|---|
| two_pointer_opposite_search | `0, n-1` | 和/關係單調 | $O(n)$ |[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 167 |
| two_pointer_opposite_maximize | `0, n-1` | 逐步縮小但保留最優可能 | $O(n)$ |[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) |
| two_pointer_opposite_palindrome | `0, n-1` | 左右對稱匹配 | $O(n)$ |[LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py), 680 |
| two_pointer_writer_* | `write=0, read=0` | `[0, write)` 永遠是有效輸出 | $O(n)$ |[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py), 27, 80, 283 |
| two_pointer_three_sum | 外迴圈 + 內相向 | 排序 + 去重 | $O(n^2)$ |[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py), 16 |

#### two_pointer_opposite_search（相向搜尋）
- 🎯 題目
  - 🟢 [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)（在本資料中標註 two_pointer_opposite；實務常見也可 hash）
  - 🟠 LeetCode 167（related 出現；本題單未列出但可視為同型延伸）

#### two_pointer_opposite_maximize（相向最佳化）
- 🎯 題目
  - 🟠[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)

#### two_pointer_opposite_palindrome（回文驗證）
- 🎯 題目
  - 🟢 [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)

#### two_pointer_same_direction：Writer（原地修改）
- two_pointer_writer_dedup（去重）
  - 🎯 題目：🟢 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)、🟠[LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
  - 🎯 題目：🟢 [LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - 🎯 題目：🟢 [LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)

#### two_pointer_three_sum（多重和枚舉）
- 🎯 題目
  - 🟠[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)

---

### 3) FastSlowPointers（快慢指針）🔥
- **用途**：循環偵測 / 入環點 / 中點
- 複雜度：$O(n)$、空間 $O(1)$

#### fast_slow_cycle_detect（Floyd Phase 1）
- 🎯 題目
  - 🟢 [LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)

#### fast_slow_cycle_start（Floyd Phase 2）
- 🎯 題目
  - 🟠[LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)

#### fast_slow_midpoint（找中點）
- 🎯 題目
  - 🟢 [LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)

#### fast_slow_implicit_cycle（隱式序列循環）
- 🎯 題目
  - 🟢 [LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)

### 4) TwoPointerPartition（分割/Partition）⚡
- **用途**：Dutch Flag / 二分割 / Quickselect 分割
- 常見陷阱：交換後指針是否前進（尤其 Dutch Flag 的 `mid`）

#### dutch_flag_partition（三向分割）
- 🎯 題目
  - 🟠[LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)

#### two_way_partition（二向分割）
- 🎯 題目
  - 🟢 [LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)

#### quickselect_partition（選第 K 大）
- 🎯 題目
  - 🟠[LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)（也可用 heap）

---

### 5) MergeSortedSequences（合併已排序序列）📚
- **核心**：兩指針線性合併 $O(m+n)$
- 典型：合併兩鏈表 / 合併兩陣列 / 從尾端合併

#### merge_two_sorted_lists（鏈表合併）
- 🎯 題目
  - 🟢 [LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)

#### merge_two_sorted_arrays（陣列合併）
- 🎯 題目
  - 🟢 [LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)

#### merge_sorted_from_ends（從尾端合併/平方排序）
- 🎯 題目
  - 🟢 [LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

### 6) KWayMerge（K 路合併）⚙️
- **兩大作法**
  - `min-heap`：$O(N \log k)$（N 為總元素）
  - `divide-and-conquer`：$O(N \log k)$（常數不同）
- 🎯 題目
  - 🔴 [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)（heap / 分治）
  - 🔴 [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)（本資料標註：binary_search_on_answer + merge_two_sorted）

---

### 7) BinarySearchBoundary（二分邊界 / 在答案上二分）🎯
- **核心**：找「第一個成立」/「最後一個成立」/「答案空間單調」
- 🎯 題目
  - 🔴 [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)（在答案上二分的代表之一）

---

### 8) BacktrackingExploration（回溯：可逆探索）🧩
- **節奏**：Choose → Explore → Unchoose  
- **不變量**：==狀態必須精準對應當前 path==（回來要完全還原）
- 常見優化：排序 + 同層去重、剪枝（剩餘長度/剩餘和/約束集合）

#### ✅ 子型比較表（本題單覆蓋）
| 子型 | State | 去重 | 剪枝關鍵 | 代表題 |
|---|---|---|---|---|
| permutation | `used[]` | sort + 同層 skip（有重複） | 無/簡單 |[LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py), 47 |
| subset/combination | `start_idx` | sort + 同層 skip（有重複） | 剩餘元素不足 |[LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py), 90, 77 |
| target sum | `remaining` + `start_idx` | 依題 | `remaining < 0`、排序 early break |[LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py), 40, 216 |
| constraint satisfaction | constraint sets | 天然避免衝突 | 立即衝突即停 |[LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py), 52 |
| string segmentation | cut positions | 依題 | 長度界、有效性 |[LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py), 131 |
| grid path | visited / in-place mark | 通常不需 | 邊界/字元不符 |[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py) |

#### backtracking_permutation（排列）
- 🎯 題目
  - 🟠[LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)

#### backtracking_subset（子集）
- 🎯 題目
  - 🟠[LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)

#### backtracking_combination（組合 / 目標和）
- 🎯 題目
  - 🟠[LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
  - 🟠[LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)

#### backtracking_n_queens（約束滿足）
- 🎯 題目
  - 🔴 [LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)

#### backtracking_string_segmentation（字串切割）
- 🎯 題目
  - 🟠[LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)（IP：==固定 4 段 + 長度界剪枝==）
  - 🟠[LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)（回文切割：可加 $O(n^2)$ DP 預處理）

#### backtracking_grid_path（網格路徑 DFS）
- 🎯 題目
  - 🟠[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

### 9) GridBFSMultiSource（多源 BFS 波前）🌊
- **核心**：同時把所有源點入隊，逐層擴散（wavefront）
- 複雜度：$O(RC)$（每格最多入隊一次）
- 🎯 題目
  - 🟠[LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

### 10) HeapTopK（TopK / 第 K / 串流中位數）⛏️
- heap_kth_element（第 K）
  - 🎯 題目：🟠[LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

## 🧭 Family（題型家族）快速索引
- **substring_window**：[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)、76、209、340、438、567
- **in_place_array_modification**：[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)、27、80、283
- **array_partition**：[LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)、905、922、215
- **merge_sorted / sequence_merge**：[LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)、88、977、23、4
- **linked_list_cycle**：[LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)、142、202
- **multi_sum_enumeration**：[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)、16
- **graph_wavefront**：[LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

## 🧪 面試常用「最小模板」(可直接套) `code`
<!-- markmap: fold -->
### Sliding Window（變長最大化）
```python
def solve(s):
    state = {}
    left = 0
    ans = 0
    for right, x in enumerate(s):
        add(state, x)
        while violated(state):
            remove(state, s[left])
            left += 1
        ans = max(ans, right - left + 1)
    return ans
```

### Two Pointers（Writer 原地）
```python
def compact(nums):
    write = 0
    for read in range(len(nums)):
        if keep(nums[read]):
            nums[write] = nums[read]
            write += 1
    return write
```

### Backtracking（Choose-Explore-Unchoose）
```python
def backtrack(start, path):
    if done(path):
        out.append(path[:]); return
    for choice in choices_from(start):
        if not ok(choice): 
            continue
        path.append(choice)
        backtrack(next_start(choice), path)
        path.pop()
```

### Multi-source BFS（波前）
```python
from collections import deque

def bfs(grid, sources):
    q = deque(sources)
    dist = 0
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in nbrs(r, c):
                if can_go(nr, nc):
                    mark(nr, nc)
                    q.append((nr, nc))
        dist += 1
```

## ✅ Roadmap Checkpoint（用於進度追蹤）
- [ ] Two Pointers Mastery：[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)、15、26、27、75、141
- [ ] Sliding Window Mastery：[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)、76、209、340、438、567
- [ ] Backtracking 核心：[LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)、78、39、51
- [ ] Heap / Quickselect：[LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)、23
- [ ] BFS 波前：[LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

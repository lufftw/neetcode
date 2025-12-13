---
title: LeetCode Patterns 知識圖譜 (33 題) — API 核心 → 模式 → 問題 🎯
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 如何快速使用這個心智圖
- **自上而下閱讀**：*API 核心* → *模式* → *問題* (連結)
- **練習迴圈**：實作模板 → 解決 2–3 個問題 → 重構為可重用的 `solve(pattern_state_machine)` 心智模型
- **進度追蹤**
  - [ ] 先完成所有 **簡單** 題
  - [ ] 然後是 **中等** 變體
  - [ ] 最後是 **困難** “邊界案例放大器”

---

## 🧠 API 核心 (“引擎”)
### SubstringSlidingWindow — *一維視窗狀態機*
- ==核心不變量==：視窗 `[L,R]` 保持有效，透過 **向右擴展** + **向左收縮**
- 複雜度：通常是 $O(n)$ 時間，$O(\Sigma)$ 空間 (字母表 / 不同鍵)

<!-- markmap: fold -->
#### 模式速查表 (來自文件)
| 問題 | 不變量 | 狀態 | 視窗大小 | 目標 |
|---------|-----------|-------|-------------|------|
| [LeetCode 3 - 最長不含重複字符的子字串](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | 全部唯一 | 最後索引映射 | 可變 | 最大 |
| [LeetCode 340 - 最多包含 K 個不同字符的最長子字串](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | ≤K 不同 | 頻率映射 | 可變 | 最大 |
| [LeetCode 76 - 最小覆蓋子字串](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | 覆蓋 `t` | 需要/擁有 | 可變 | 最小 |
| [LeetCode 567 - 字符串的排列](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | 精確頻率匹配 | 頻率 + 匹配 | 固定 | 存在 |
| [LeetCode 438 - 找到字符串中所有字母異位詞](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | 精確頻率匹配 | 頻率 + 匹配 | 固定 | 全部 |
| [LeetCode 209 - 最小大小的子陣列和](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | 和 ≥ 目標 | 整數和 | 可變 | 最小 |

#### 模式
- **sliding_window_unique** *(最大化，“向左跳”優化)*
  - 🎯 問題
    - [ ] [LeetCode 3 - 最長不含重複字符的子字串](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - 關鍵狀態：`last_seen[char]` → `L = max(L, last_seen[c]+1)`
- **sliding_window_at_most_k_distinct** *(最大化，無效時收縮)*
  - 🎯 問題
    - [ ] [LeetCode 340 - 最多包含 K 個不同字符的最長子字串](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - 關鍵不變量：`len(freq) <= k`
- **sliding_window_freq_cover** *(覆蓋 / 精確匹配家族)*
  - 🎯 問題
    - [ ] [LeetCode 76 - 最小覆蓋子字串](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) — *在有效時最小化*
    - [ ] [LeetCode 438 - 找到字符串中所有字母異位詞](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) — *固定視窗，收集索引*
    - [ ] [LeetCode 567 - 字符串的排列](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) — *固定視窗，布林*
- **sliding_window_cost_bounded** *(數值約束)*
  - 🎯 問題
    - [ ] [LeetCode 209 - 最小大小的子陣列和](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
  - 典型需求：正數 → 單調收縮有效

---

### TwoPointersTraversal — *序列上的指標編排*
- ==核心不變量==：指標確定性移動；已處理區域是“安全的”
- 複雜度：通常是 $O(n)$ 時間，$O(1)$ 空間 (除了排序步驟)

#### 模式比較 (來自文件)
| 模式 | 指標初始化 | 移動 | 終止 | 時間 | 空間 | 關鍵用例 |
|---------|--------------|----------|-------------|------|-------|--------------|
| 對立 | `0, n-1` | 向中心 | `L>=R` | $O(n)$ | $O(1)$ | 排序對 / 回文 / 最大化 |
| 同方向 | `write, read` | 向前 | `read==n` | $O(n)$ | $O(1)$ | 原地修改 |
| 快–慢 | `slow, fast` | 1× / 2× | 相遇或空 | $O(n)$ | $O(1)$ | 迴圈 / 中點 |
| 去重列舉 | `i` + `L,R` | 嵌套 | 完成 | $O(n^2)$ | $O(1)$ | 3Sum/4Sum |

#### 模式
- **two_pointer_opposite_maximize**
  - 🎯 問題
    - [ ] [LeetCode 11 - 盛最多水的容器](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - 洞察：移動**較短**高度的指標
- **two_pointer_three_sum** *(去重列舉)*
  - 🎯 問題
    - [ ] [LeetCode 15 - 三數之和](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
    - [ ] [LeetCode 16 - 最接近的三數之和](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - 要求：先排序 ($O(n\log n)$)，然後掃描去重
- **two_pointer_opposite_palindrome**
  - 🎯 問題
    - [ ] [LeetCode 125 - 有效回文](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
    - [ ] [LeetCode 680 - 有效回文 II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
- **two_pointer_writer_dedup**
  - 🎯 問題
    - [ ] [LeetCode 26 - 刪除排序陣列中的重複項](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
    - [ ] [LeetCode 80 - 刪除排序陣列中的重複項 II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
- **two_pointer_writer_remove**
  - 🎯 問題
    - [ ] [LeetCode 27 - 移除元素](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
- **two_pointer_writer_compact**
  - 🎯 問題
    - [ ] [LeetCode 283 - 移動零](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)

---

### FastSlowPointers — *Floyd + 中點 + 隱式序列*
- ==核心不變量==：如果存在迴圈，`fast` 會遇到 `slow`
- 模式
  - **fast_slow_cycle_detect**
    - [ ] [LeetCode 141 - 鏈結串列循環](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - **fast_slow_cycle_start**
    - [ ] [LeetCode 142 - 鏈結串列循環 II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - **fast_slow_midpoint**
    - [ ] [LeetCode 876 - 鏈結串列的中間節點](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
  - **fast_slow_implicit_cycle**
    - [ ] [LeetCode 202 - 快樂數](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)

---

### TwoPointerPartition — *原地分割“迷你快速排序”*
- ==核心不變量==：區域按屬性分割
- 模式
  - **dutch_flag_partition**
    - [ ] [LeetCode 75 - 顏色分類](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
  - **two_way_partition**
    - [ ] [LeetCode 905 - 按奇偶排序陣列](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
    - [ ] [LeetCode 922 - 按奇偶排序陣列 II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
  - **quickselect_partition** *(通過分割選擇)*
    - [ ] [LeetCode 215 - 陣列中的第 K 個最大元素](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

---

### MergeSortedSequences — *合併兩個已排序序列*
- ==核心不變量==：輸出前綴是完全排序的
- 模式
  - **merge_two_sorted_lists**
    - [ ] [LeetCode 21 - 合併兩個有序鏈結串列](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - **merge_two_sorted_arrays**
    - [ ] [LeetCode 88 - 合併排序陣列](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - **merge_sorted_from_ends**
    - [ ] [LeetCode 977 - 有序陣列的平方](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

---

### KWayMerge — *合併 K 個已排序序列*
- 兩個主要實作
  - **merge_k_sorted_heap** → $O(N\log k)$ 時間，$O(k)$ 堆積
  - **merge_k_sorted_divide** → $O(N\log k)$ 時間，有時常數較小
- 🎯 問題
  - [ ] [LeetCode 23 - 合併 K 個排序鏈結串列](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - 相關“混合思維”：[LeetCode 4 - 兩個排序陣列的中位數](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

---

### HeapTopK — *在流式更新中保持最佳 K*
- 模式
  - **heap_kth_element**
    - [ ] [LeetCode 215 - 陣列中的第 K 個最大元素](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

---

### LinkedListInPlaceReversal — *指標手術*
- 模式
  - **linked_list_k_group_reversal**
    - [ ] [LeetCode 25 - K 個一組翻轉鏈結串列](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- 也包括核心鏈結串列運算
  - [ ] [LeetCode 2 - 兩數相加](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py)

---

### BacktrackingExploration — *具有剪枝的搜尋樹*
- 模式
  - **backtracking_n_queens**
    - [ ] [LeetCode 51 - N 皇后](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)

---

### GridBFSMultiSource — *網格上的波前傳播*
- 模式
  - **grid_bfs_propagation**
    - [ ] [LeetCode 994 - 腐爛的橘子](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- 實作不變量：佇列持有當前“分鐘/層級”的前沿

---

## 🧭 路線圖切片 (接下來要做什麼)
### 滑動視窗精通 📚
- [ ] [LeetCode 3 - 最長不含重複字符的子字串](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- [ ] [LeetCode 340 - 最多包含 K 個不同字符的最長子字串](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
- [ ] [LeetCode 209 - 最小大小的子陣列和](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
- [ ] [LeetCode 567 - 字符串的排列](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
- [ ] [LeetCode 438 - 找到字符串中所有字母異位詞](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
- [ ] [LeetCode 76 - 最小覆蓋子字串](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) 🔥

### 雙指標精通 ⚡
- 對立指標
  - [ ] [LeetCode 11 - 盛最多水的容器](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ] [LeetCode 125 - 有效回文](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - [ ] [LeetCode 680 - 有效回文 II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
- 寫入指標 (原地)
  - [ ] [LeetCode 26 - 刪除排序陣列中的重複項](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [ ] [LeetCode 27 - 移除元素](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - [ ] [LeetCode 283 - 移動零](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
  - [ ] [LeetCode 80 - 刪除排序陣列中的重複項 II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
- 快–慢
  - [ ] [LeetCode 141 - 鏈結串列循環](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - [ ] [LeetCode 142 - 鏈結串列循環 II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - [ ] [LeetCode 876 - 鏈結串列的中間節點](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
  - [ ] [LeetCode 202 - 快樂數](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)

---

## 🧩 “同一問題，不同視角” (遷移學習)
- **選擇**：[LeetCode 215 - 陣列中的第 K 個最大元素](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
  - 選項 A：`quickselect_partition` (期望 $O(n)$)
  - 選項 B：`heap_kth_element` ($O(n\log k)$，適合流式)
- **合併**：
  - 2 路：[LeetCode 21 - 合併兩個有序鏈結串列](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)，[LeetCode 88 - 合併排序陣列](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - K 路：[LeetCode 23 - 合併 K 個排序鏈結串列](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - “邊界 + 合併思維”：[LeetCode 4 - 兩個排序陣列的中位數](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

---

## 🧱 最小可重用模板 (心智 API)
```python
# 滑動視窗 (可變，最大化)
def max_window(seq):
    state = {}
    L = 0
    ans = 0
    for R, x in enumerate(seq):
        add(state, x)
        while invalid(state):
            remove(state, seq[L]); L += 1
        ans = max(ans, R - L + 1)
    return ans

# 雙指標 (對立)
def opposite(arr):
    L, R = 0, len(arr) - 1
    while L < R:
        if should_move_left(arr, L, R):
            L += 1
        else:
            R -= 1
```

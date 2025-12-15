---
title: LeetCode 知識圖譜心智圖（核心模式 → API 核心 → 題目） 🎯
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 如何使用這張地圖 📚
- **目標**：學會 *可遷移的核心*（API）→ 辨識 *模式* → 解出 *題目*
- **進度追蹤**
  - [ ] 每個核心做 1 題（廣度）
  - [ ] 每個核心做 3 題（深度）
  - [ ] 20 分鐘內從零開始重解「錨點」題 ⚡

## Kernel Index（你應該內化的「API」）🔥
- **SubstringSlidingWindow** → 連續子字串狀態機
- **TwoPointersTraversal** → 協調式指標移動
- **TwoPointerPartition** → 原地分割
- **FastSlowPointers** → 環 / 中點
- **MergeSortedSequences** + **KWayMerge** → 合併已排序串流
- **BacktrackingExploration** → 選擇 → 探索 → 撤銷選擇
- **GridBFSMultiSource** → 網格上的波前 BFS
- **BinarySearchBoundary** → 邊界 + 答案空間搜尋
- **HeapTopK** → top-k / kth / 串流中位數
- *(本體中其他未被提供題目使用的：MonotonicStack, UnionFindConnectivity, PrefixSumRangeQuery, TreeTraversalDFS/BFS, DPSequence/DPInterval, TopologicalSort, TriePrefixSearch)*

---

## 1) 滑動視窗 (SubstringSlidingWindow) 🪟
- **核心不變式**：視窗 `[L..R]` 保持合法；每個元素最多進出一次 ⇒ $O(n)$
- **狀態選擇**
  - `last_seen_index` 對照表（L 跳躍最佳化）
  - `freq` 對照表 + `distinct_count`
  - `need/have` 對照表 + `satisfied/required`
  - 數值 `window_sum`
- **模式比較表**
  - | 題目 | 不變式 | 狀態 | 視窗大小 | 目標 |
    |---------|-----------|-------|-------------|------|
    | [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | 全部唯一 | last index 對照表 | 可變 | 最大化 |
    | [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | ≤K 種不同字元 | freq 對照表 | 可變 | 最大化 |
    | [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | 涵蓋所有必要項 | need/have + satisfied | 可變 | 最小化 |
    | [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | 頻率完全一致 | freq + matched | 固定 | 是否存在 |
    | [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | 頻率完全一致 | freq + matched | 固定 | 全部位置 |
    | [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | sum ≥ target | 整數 sum | 可變 | 最小化 |
- **模式**
  - **唯一視窗** (`sliding_window_unique`)
    - Anchor: [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) ==(學會 jump-left)==
  - **最多 K 種不同字元** (`sliding_window_at_most_k_distinct`)
    - Anchor: [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - **頻率涵蓋 / 完全一致** (`sliding_window_freq_cover`)
    - 最小化涵蓋： [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
    - 固定大小完全一致（存在）： [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
    - 固定大小完全一致（收集全部）： [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - **成本上限 / 總和限制** (`sliding_window_cost_bounded`)
    - Anchor: [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
- **常見面試陷阱**
  - 「最小化視窗」需要：**while valid → 縮小**（不只縮一次）
  - 「完全一致」最佳做法：**固定視窗** + `matched` 計數器

---

## 2) 雙指標走訪 (TwoPointersTraversal) 👯
- **心智模型**：每一步移動都在 *證明* 被排除的區段不可能包含答案
- **子類型**
  - **相向指標**（排序/對稱最佳化）
    - 最大化目標
      - [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) *(移動較短邊)*
    - 回文驗證
      - [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
      - [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py) *(一次跳過分支)*
    - 「Two Sum 家族」（註：雜湊表較典型；相向指標需要已排序）
      - [LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
  - **在已排序陣列上去重 + 逐一產生**
    - [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py) *(外層 i + 內層 L/R + 跳過重複)*
    - [LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - **同向（Reader/Writer）原地**
    - 去重
      - [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
      - [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
    - 移除元素
      - [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
    - 壓縮 / 穩定過濾
      - [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
- **快速不變式表**
  - | 模式 | 不變式 | 典型題目 |
    |---------|-----------|------------------|
    | 相向 | 答案在 `[L..R]` | [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py), [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py) |
    | Writer | `arr[0:write]` 是「保留」的 | [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py), [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) |
    | 已排序逐一產生 | 不輸出重複 tuple | [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py) |

---

## 3) 分割 (TwoPointerPartition) 🚧
- **使用時機**：原地把元素分類到不同區域；常作為選擇/排序的基礎積木
- **模式**
  - **荷蘭國旗（3 路分割）** (`dutch_flag_partition`)
    - Anchor: [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
  - **2 路分割** (`two_way_partition`)
    - [LeetCode 905 - Sort Array By Parity](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
    - [LeetCode 922 - Sort Array By Parity II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)

---

## 4) 快慢指標 (FastSlowPointers) 🐢🐇
- **兩階段（Floyd）**
  - 階段 1：偵測環
  - 階段 2：找出環的起點
- **題目**
  - 偵測環： [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - 找出環起點： [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - 隱式環（函式迭代）： [LeetCode 202 - Happy Number](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)
  - 中點： [LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)

---

## 5) 合併已排序序列 (MergeSortedSequences + KWayMerge) 🔗
- **兩個已排序串流（雙指標）**
  - 鏈結串列合併： [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - 陣列合併（常從尾端開始）： [LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - 從尾端合併技巧： [LeetCode 977 - Squares of a Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)
- **K 路合併**
  - 基於堆積 $O(N \log k)$： [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - 分治法 $O(N \log k)$： [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
- **困難混合題（合併 + 在答案上做二分搜尋）**
  - [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py) ==(依計數分割不變式)==

---

## 6) 回溯探索 (BacktrackingExploration) 🧠
- **核心節奏**：**選擇 → 探索 → 撤銷選擇**
- **不變式**：狀態要精確對應目前路徑（不能有「幽靈標記」）
- **決策樹形狀**
  - **排列**（used[]）
    - [LeetCode 46 - Permutations](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
    - 含重複（排序 + 同層跳過）： [LeetCode 47 - Permutations II](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)
  - **子集合**（start index）
    - [LeetCode 78 - Subsets](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
    - 含重複（排序 + 同層跳過）： [LeetCode 90 - Subsets II](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)
  - **組合 / 固定大小**（start index + 長度上限）
    - [LeetCode 77 - Combinations](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
  - **目標總和搜尋**
    - 允許重複使用： [LeetCode 39 - Combination Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
    - 不可重複使用 + 含重複： [LeetCode 40 - Combination Sum II](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)
    - 固定個數 + 有界範圍： [LeetCode 216 - Combination Sum III](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)
  - **限制條件滿足**
    - [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
    - [LeetCode 52 - N-Queens II](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
  - **字串切分**
    - [LeetCode 93 - Restore IP Addresses](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py) *(4 段 + 長度界限剪枝)*
    - [LeetCode 131 - Palindrome Partitioning](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py) *(可選：用 DP 預先計算回文檢查)*
  - **網格路徑搜尋**
    - [LeetCode 79 - Word Search](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py) *(visited 標記/取消標記)*

<!-- markmap: fold -->
## 7) 網格上的 BFS 波前 (GridBFSMultiSource) 🌊
- **核心想法**：把所有來源一起推入，逐層擴張（時間 = 層數）
- **Anchor**
  - [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- **工程檢查清單**
  - 佇列初始化包含所有來源
  - 計算新鮮/剩餘目標數
  - 依層處理 BFS 以計算分鐘數

---

## 8) 堆積 / 選擇 (HeapTopK + Quickselect) ⛰️
- **第 K 大元素**
  - Quickselect / 分割： [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
  - 堆積替代方案（尤其是串流 / 穩定性）： [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

---

## 9) 鏈結串列操作（指標手術）🔧
- 串列上的算術
  - [LeetCode 2 - Add Two Numbers](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py)
- 分組原地反轉
  - [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)

---

## 建議學習路徑（roadmap 風格）🚀
- **滑動視窗精通**
  - [ ] [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [ ] [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - [ ] [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - [ ] [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
  - [ ] [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - [ ] [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
- **雙指標精通**
  - [ ] [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ] [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - [ ] [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [ ] [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- **回溯精通**
  - [ ] [LeetCode 78 - Subsets](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
  - [ ] [LeetCode 46 - Permutations](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
  - [ ] [LeetCode 39 - Combination Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
  - [ ] [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - [ ] [LeetCode 79 - Word Search](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

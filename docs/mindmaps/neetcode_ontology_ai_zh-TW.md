---
title: LeetCode 核心模式總覽（API Kernel → Pattern → 題目）🎯
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 使用方式（學習/面試/競賽都適用）📚
- ==先背「API Kernel 模板」→ 再練「Pattern 變形」→ 最後刷「代表題」==
- [ ] 每個 Kernel 至少做到：Easy×2、Medium×2、Hard×1（能口述 invariant + 複雜度）
- [ ] 每題寫完：補「不變量 invariant」「收縮/擴張條件」「邊界 case」

## 1) SubstringSlidingWindow（滑動視窗狀態機）⚡
- **API Kernel**：`SubstringSlidingWindow`
- **核心不變量**：視窗 `[L,R]` 內的狀態可 $O(1)$ 增量更新；違反不變量就收縮
- **兩大策略**
  - **Maximize**：一直擴張，違規就收縮（取最大）
  - **Minimize**：先擴張到合法，再盡量收縮（取最小）
- <!-- markmap: fold -->
- **Pattern → 題目對照表**
  | Pattern | Invariant（不變量） | State（狀態） | Window | 代表題 |
  |---|---|---|---|---|
  | sliding_window_unique | 全部唯一 | `last_seen` / freq | 變動 | [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) |
  | sliding_window_at_most_k_distinct | distinct ≤ K | freq map | 變動 | [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) |
  | sliding_window_freq_cover | 覆蓋需求頻次 | need/have + satisfied | 變動/固定 | [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) / [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) / [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) |
  | sliding_window_cost_bounded | sum/cost ≤ bound 或 ≥ target | sum | 變動 | [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) |
- **高頻踩雷**
  - `chars_satisfied` 只能在「==剛好達標==」時 +1，超過不算
  - Fixed window（如 [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)）通常用「右擴 + 左自動彈出」而不是 while 收縮

## 2) TwoPointersTraversal（雙指針遍歷）🔥
- **API Kernel**：`TwoPointersTraversal`
- **子家族**
  - **Opposite（對撞）**：`L→ ←R`，依單調性縮小搜尋空間
  - **Writer（同向讀寫）**：`write` 維護「已處理合法區」
  - **Fast–Slow（快慢）**：cycle / midpoint
  - **Dedup Enumeration（去重枚舉）**：排序 + 外層枚舉 + 內層對撞
- <!-- markmap: fold -->
- **Pattern → 題目**
  - **對撞：搜尋/最大化/回文**
    - [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)（maximize）
    - [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
    - [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
    - [LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)（資料標註為 two pointers；實務常見 hash）
  - **去重枚舉（3Sum 系）**
    - [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
    - [LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - **同向讀寫（in-place）**
    - [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
    - [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
    - [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
    - [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
- **面試口訣**
  - 對撞：==排序/單調性== 是正當性來源
  - Writer：`arr[0:write)` 永遠合法（不變量）

## 3) FastSlowPointers（Floyd 快慢指針）⚡
- **API Kernel**：`FastSlowPointers`
- **兩階段**
  - Phase 1：是否有環（相遇）
  - Phase 2：找入環點（重置一指針到 head，同速前進）
- **題目**
  - [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - [LeetCode 202 - Happy Number](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)（隱式序列）
  - [LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)

## 4) TwoPointerPartition（分割 / 荷蘭國旗）🎯
- **API Kernel**：`TwoPointerPartition`
- **核心**：一趟掃描把元素分到不同區間（不變量是「區間語意」）
- **題目**
  - [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)（三向 partition）
  - [LeetCode 905 - Sort Array By Parity](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)（二向 partition）
  - [LeetCode 922 - Sort Array By Parity II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)（二向、但位置約束）
  - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)（quickselect_partition + heap_kth_element）

## 5) MergeSortedSequences / KWayMerge（合併排序序列）📚
- **API Kernel**
  - `MergeSortedSequences`：兩路合併（two pointers）
  - `KWayMerge`：K 路合併（heap 或 divide-and-conquer）
- **兩路合併題**
  - [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - [LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - [LeetCode 977 - Squares of a Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)（從兩端「合併」）
- **K 路合併題**
  - [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - 延伸（同資料集中）：[LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)（binary search on answer + merge 概念）

## 6) BinarySearchBoundary（邊界二分 / 對答案二分）⚡
- **API Kernel**：`BinarySearchBoundary`
- **典型用法**
  - `first_true / last_true`：找邊界
  - `binary_search_on_answer`：答案空間單調 → 二分最小/最大可行值
- **代表題**
  - [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

## 7) HeapTopK（TopK / 第K大）🔥
- **API Kernel**：`HeapTopK`
- **代表題**
  - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)（heap vs quickselect 的工程取捨：穩定性 vs 平均線性）

## 8) GridBFSMultiSource（網格多源 BFS 波前）🌊
- **API Kernel**：`GridBFSMultiSource`
- **核心**：多個起點同時入隊，層序擴散；答案通常是「層數/最短時間」
- **代表題**
  - [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

## 9) BacktrackingExploration（回溯枚舉 + 剪枝）🔥
- **API Kernel**：`BacktrackingExploration`
- **核心**：決策樹 DFS；用集合/位元/約束做剪枝
- **代表題**
  - [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)

## 10) LinkedListInPlaceReversal（鏈結串列原地反轉）⚡
- **API Kernel**：`LinkedListInPlaceReversal`
- **代表題**
  - [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)

## 建議練功路線（用本資料集就能跑完）🎯
- **第一週：Two Pointers 基礎**
  - [ ] [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [ ] [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - [ ] [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ] [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
- **第二週：Sliding Window 全家桶（面試超高頻）**
  - [ ] [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [ ] [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - [ ] [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
  - [ ] [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
- **第三週：結構化進階**
  - [ ] [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - [ ] [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
  - [ ] [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
  - [ ] [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
- **第四週：Hard 收斂與口述能力**
  - [ ] [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
  - [ ] [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
  - [ ] [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)（再刷一次，要求 10 分鐘內寫對）
---
title: LeetCode 核心模式 Mind Map（Sliding Window／Two Pointers／Backtracking／BFS／Merge／Partition／Heap／Binary Search）
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 目標導向總覽（用「API Kernel」把題型收斂成模板）
- ==先學 Kernel，再刷題庫==：把 45 題視為 8 條主幹能力
- 進度追蹤
  - [ ] Sliding Window（字串/陣列連續區間）
  - [ ] Two Pointers（對撞/同向/快慢/分割/合併）
  - [ ] Backtracking（可逆探索 + 剪枝 + 去重）
  - [ ] BFS Wavefront（多源擴散）
  - [ ] Merge（2-way / k-way）
  - [ ] Partition / Quickselect
  - [ ] Heap TopK
  - [ ] Binary Search（邊界/答案空間）

## 🧠 Kernel 1：SubstringSlidingWindow（滑動視窗狀態機）📚
- **核心不變量（Invariant）**
  - 視窗 `[L,R]` 永遠維持某個條件；R 只前進，L 只在「違規/可縮」時前進
  - 複雜度：通常 $O(n)$（每個元素進出視窗至多一次）
- **子模式（Patterns）**
  - `sliding_window_unique`：視窗內全唯一
    - [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - `sliding_window_at_most_k_distinct`：最多 K 種不同字元
    - [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - `sliding_window_freq_cover`：頻率覆蓋（need/have）
    - [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
    - [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
    - [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - `sliding_window_cost_bounded`：數值成本/總和約束（通常最小化）
    - [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
- **對照表（快速辨識）**
  - | 問題 | Invariant | State | 視窗大小 | 目標 |
    |---|---|---|---|---|
    | [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | 全唯一 | `last_index` | 變動 | 最大 |
    | [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | ≤K distinct | freq map | 變動 | 最大 |
    | [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | 覆蓋 t | need/have | 變動 | 最小 |
    | [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | 頻率完全相同 | freq + match count | 固定 | 存在 |
    | [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | 頻率完全相同 | freq + match count | 固定 | 全部位置 |
    | [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | sum ≥ target | int sum | 變動 | 最小 |
- **模板（精簡）**
  - ```python
    # 變動視窗：最大化（違規才縮）
    left = 0
    for right, x in enumerate(seq):
        add(x)
        while violated():
            remove(seq[left]); left += 1
        ans = max(ans, right-left+1)

    # 變動視窗：最小化（有效就縮）
    left = 0
    for right, x in enumerate(seq):
        add(x)
        while valid():
            ans = min(ans, right-left+1)
            remove(seq[left]); left += 1
    ```

## 🧠 Kernel 2：TwoPointersTraversal（雙指針遍歷家族）⚡
- **六種形狀（最常考）**
  - 對撞 Opposite：縮小解空間（排序/單調性）
  - 同向 Reader/Writer：原地改陣列
  - 快慢 Fast/Slow：找環/中點
  - 去重枚舉：排序 + skip duplicates（3Sum/4Sum）
  - 合併 Merge：兩序列線性合併
- **對撞（Opposite）**
  - [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
- **去重枚舉（3Sum）**
  - [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
  - [LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
- **同向 Writer（原地去重/移除/壓縮）**
  - [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
  - [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
- **快慢（Floyd）**
  - [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - [LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
  - [LeetCode 202 - Happy Number](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)
- **合併（MergeSortedSequences）**
  - [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - [LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - [LeetCode 977 - Squares of a Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

## 🧠 Kernel 3：BacktrackingExploration（可逆探索）🔥
- **節奏：Choose → Explore → Unchoose**
  - 不變量：==狀態必須精準反映當前路徑==
  - 常見 bug：忘記 undo（visited/used/集合/路徑）
- **五種決策樹形狀（對應 patterns）**
  - 排列 `backtracking_permutation`
    - [LeetCode 46 - Permutations](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
    - [LeetCode 47 - Permutations II](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)（排序 + 同層去重）
  - 子集合 `backtracking_subset`
    - [LeetCode 78 - Subsets](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
    - [LeetCode 90 - Subsets II](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)
  - 組合 `backtracking_combination`
    - [LeetCode 77 - Combinations](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
  - 目標和（Target Sum / Combination Sum 家族）
    - [LeetCode 39 - Combination Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)（可重複使用：遞迴用 `i`）
    - [LeetCode 40 - Combination Sum II](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)（不可重複 + 同層去重：遞迴用 `i+1`）
    - [LeetCode 216 - Combination Sum III](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)（固定 k + 固定 sum）
  - 約束滿足（Constraint Satisfaction）
    - [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
    - [LeetCode 52 - N-Queens II](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
  - 字串切分（Segmentation）
    - [LeetCode 93 - Restore IP Addresses](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)
    - [LeetCode 131 - Palindrome Partitioning](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)（可用 DP 預處理回文）
  - 格子路徑（Grid Path）
    - [LeetCode 79 - Word Search](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)
- **去重策略速查**
  - `start_index`（天然字典序）vs `used[]`（排列）vs `sort + 同層 skip`
- <!-- markmap: fold -->
- **通用模板**
  - ```python
    path = []
    def dfs(state):
        if is_solution(state):
            collect(path); return
        for choice in choices(state):
            apply(choice); path.append(choice)
            dfs(state)
            path.pop(); undo(choice)
    ```

## 🧠 Kernel 4：GridBFSMultiSource（多源 BFS 波前擴散）📚
- **典型訊號**
  - grid 上「同時從多個起點擴散」+ 求最短時間/層數
- 題目
  - [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- 關鍵實作點
  - queue 初始化放入所有 source
  - 層序（minute/steps）用 BFS level 計數
  - visited 可用原地改 grid（0/1/2 狀態）

## 🧠 Kernel 5：KWayMerge（K 路合併）⚡
- **兩種主流策略**
  - heap：$O(N \log k)$（N=總節點/元素）
  - divide-and-conquer：$O(N \log k)$（常數不同）
- 題目
  - [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
- 同家族延伸（2-way merge）
  - [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)

## 🧠 Kernel 6：TwoPointerPartition（分割 / Dutch Flag / Quickselect）🔥
- 三向分割（Dutch Flag）
  - [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
- 兩向分割（Parity）
  - [LeetCode 905 - Sort Array By Parity](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
  - [LeetCode 922 - Sort Array By Parity II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
- Quickselect（第 K 大）
  - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
  - 與 heap 解法對照：同題雙解（工程上看資料分佈/常數）

## 🧠 Kernel 7：HeapTopK（TopK / Kth / Stream）⚡
- 典型用途
  - TopK、Kth、線上維護（median 需雙 heap，資料集中未列題）
- 題目（Kth）
  - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

## 🧠 Kernel 8：BinarySearchBoundary（邊界 / 答案空間）🎯
- 邊界二分：first true / last true（本資料集中以「答案空間」代表）
- 題目（混合：二分 + 合併）
  - [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

## 🧩 Linked List In-Place Reversal（指針操作專區）
- k-group 反轉（高頻且容易寫錯）
  - [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- 相關鋪墊（合併/快慢）
  - [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - [LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)

## 🗺️ 建議刷題路線（由易到難，先建立模板肌肉記憶）
- Day 1：Two Pointers 基本功
  - [ ] [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [ ] [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - [ ] [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
  - [ ] [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
- Day 2：Sliding Window 三件套（最大/最小/固定）
  - [ ] [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [ ] [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
  - [ ] [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
- Day 3：Backtracking 基礎形狀（排列/子集合/組合）
  - [ ] [LeetCode 46 - Permutations](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
  - [ ] [LeetCode 78 - Subsets](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
  - [ ] [LeetCode 77 - Combinations](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
- Day 4：Backtracking 進階（去重/切分/約束）
  - [ ] [LeetCode 47 - Permutations II](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)
  - [ ] [LeetCode 131 - Palindrome Partitioning](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
  - [ ] [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
- Day 5：Graph BFS / Merge / Partition
  - [ ] [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
  - [ ] [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - [ ] [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
  - [ ] [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

## 🧪 面試高頻題（公司交集多）🔥
- Hash + Two Pointers/Window
  - [LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
  - [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
- Two pointers / Sorting
  - [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
  - [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- Linked List
  - [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- Heap / Divide & Conquer
  - [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
- Binary Search（Hard 經典）
  - [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
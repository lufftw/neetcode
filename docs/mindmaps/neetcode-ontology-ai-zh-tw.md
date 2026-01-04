---
title: LeetCode 知識圖譜總覽：API Kernel → Pattern → 題目（45 題精選）
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 使用方式（建議學習動線）
- ==先學 API Kernel（解題引擎）→ 再學 Pattern（不變量/狀態）→ 最後刷題==
- [ ] 先把 **Sliding Window / Two Pointers / Backtracking / BFS / Merge / Partition / Heap / Binary Search** 各挑 1 題做「模板題」
- [ ] 每個 Pattern 至少刷 2 題（1 題模板 + 1 題變形）
- [ ] 每次寫完：記錄 **Invariant（不變量）** 與 **State（狀態）**，避免只背程式

---

## 🧠 API Kernels（核心解題引擎）總覽
- **SubstringSlidingWindow**：序列上的 1D 視窗狀態機（動態不變量）
- **TwoPointersTraversal**：雙指標協調移動（相向/同向/枚舉）
- **FastSlowPointers**：快慢指標（環/中點/隱式序列）
- **TwoPointerPartition**：分區（Dutch Flag / Quickselect）
- **MergeSortedSequences / KWayMerge**：合併已排序序列（2 路 / K 路）
- **BacktrackingExploration**：可逆探索（Choose→Explore→Unchoose）
- **GridBFSMultiSource**：多源 BFS 波前擴散
- **HeapTopK**：TopK / Kth / 串流中位數
- **BinarySearchBoundary**：邊界二分 / 答案二分
- （本資料集中：Tree/Trie/UnionFind/PrefixSum 等 Kernel 有定義，但題目樣本較少或未覆蓋）

---

## 🪟 Sliding Window（SubstringSlidingWindow）📚⚡
- **核心心法**：右指標只前進；左指標負責「恢復不變量」→ 整體 $O(n)$
- **State 常見**：`freq map` / `need-have` / `last_index` / `window_sum`
- **兩種模式**
  - **最大化視窗**：違規才縮
  - **最小化視窗**：一旦合法就盡量縮

<!-- markmap: fold -->
### ✅ Pattern 對照表（必背）
| 類型 | Invariant（不變量） | State（狀態） | 視窗 | 代表題 |
|---|---|---|---|---|
| Unique | 全部不同 | `last_index` 或 freq | 變動 |[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) |
| ≤K distinct | distinct ≤ K | freq + distinct count | 變動 |[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) |
| Cover | 覆蓋需求頻率 | need/have + satisfied | 變動 |[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) |
| Exact match | 頻率完全相等 | freq + matched | 固定 |[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) / 438 |
| Cost bounded | sum ≥ target | `window_sum` | 變動 |[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) |

### 1) sliding_window_unique（全唯一）
- 🎯 代表題
  - [ ][LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)（模板題）
- 常見坑
  - `left` 只能前進：`left = max(left, last[c]+1)`（避免倒退）

### 2) sliding_window_at_most_k_distinct（至多 K 種）
- 🎯 代表題
  - [ ][LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)(freq) ≤ K`

### 3) sliding_window_freq_cover（覆蓋需求 / 頻率）
- 🎯 代表題
  - [ ][LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)（最小化視窗經典）
  - [ ][LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)（固定視窗：是否存在）
  - [ ][LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)（固定視窗：收集所有位置）
- 關鍵：用 `chars_satisfied / chars_required` 追蹤「有幾種字母達標」

### 4) sliding_window_cost_bounded（成本/總和限制）
- 🎯 代表題
  - [ ][LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)（最小長度，正整數陣列）

---

## 👉 Two Pointers（TwoPointersTraversal）📚
- **核心心法**：每次移動都在「永久排除」不可能區間
- **子型態**
  - 相向（Opposite）
  - 同向（Reader/Writer）
  - 排序後枚舉（3Sum/4Sum）
  - 合併（Merge Pattern）※本資料以 MergeSortedSequences 呈現

<!-- markmap: fold -->
### ✅ Two Pointers 子型態比較表
| 子型態 | 指標初始化 | 移動規則 | 常見目標 | 代表題 |
|---|---|---|---|---|
| 相向 | `l=0,r=n-1` | 根據單調性移動 | 找 pair / 最大化 |[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) / 125 / 680 |
| 同向 Writer | `write=0, read=0` | read 掃描，符合才寫 | 原地刪除/去重 |[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py) / 27 / 283 / 80 |
| 排序枚舉 | 固定 i，內層相向 | 跳重 + 相向 | 3Sum/4Sum |[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py) / 16 |
| 合併 | `i,j` | 取較小前進 | merge sorted |[LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py) / 88 / 977 |

### 1) two_pointer_opposite_*（相向雙指標）
- 🎯 代表題
  - [ ][LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)（最大化：容器）
  - [ ][LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)（回文驗證）
  - [ ][LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)（允許刪一個字元的回文）
- 常見坑：相向題通常需要「單調性」或「對稱性」保證正確移動

### 2) two_pointer_writer_*（同向 Reader/Writer：原地修改）
- 🎯 代表題
  - [ ][LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)（去重）
  - [ ][LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)（最多保留兩個）
  - [ ][LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)（移除元素）
  - [ ][LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)（移動零）
- 不變量：`arr[0:write)` 永遠是「已處理且合法」的區段

### 3) two_pointer_three_sum（排序 + 去重枚舉）
- 🎯 代表題
  - [ ][LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)（3Sum：列舉全部）
  - [ ][LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)（3Sum Closest：最佳化）
- 去重三件套
  - 外層 i 跳重
  - 內層 l/r 移動後跳重
  - 只在找到解或移動後跳重，避免漏解/重解

---

## 🐢🐇 Fast–Slow Pointers（FastSlowPointers）
- **核心心法**：若存在環，快指標必追上慢指標（Floyd）
- 🎯 代表題
  - [ ][LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)（是否有環）
  - [ ][LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)（找入環點）
  - [ ][LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)（找中點）
  - [ ][LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)（隱式序列的環：Happy Number）
- 常見坑：Phase 2（找入環點）要「一個回 head、一起走一步」

---

## 🧩 Partition（TwoPointerPartition）🔥
- **Dutch Flag / Two-way partition / Quickselect**
- 🎯 代表題
  - [ ][LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)（Dutch Flag：三色排序）
  - [ ][LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)（雙向分區：奇偶）
  - [ ][LeetCode 922 - Sort Array By Parity II](https://leetcode.com/problems/sort-array-by-parity-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)（雙向分區：奇偶交錯）
  - [ ][LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)（Quickselect 分區找第 K 大）==也可用 Heap==
- 取捨
  - Quickselect：平均 $O(n)$、最壞 $O(n^2)$（可隨機 pivot 降風險）
  - Heap：$O(n \log k)$，穩定好寫

---

## 🔗 Merge（MergeSortedSequences / KWayMerge）
### 1) Merge 兩個已排序序列（Two Pointers）
- 🎯 代表題
  - [ ][LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)（合併兩個排序鏈結串列）
  - [ ][LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)（合併排序陣列：常用從尾端寫入）
  - [ ][LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)（平方後仍排序：從兩端取大）
- 常見技巧
  - ==從尾端合併==：避免覆蓋未處理資料（[LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)）
  - ==從兩端比較==：結果單調但原值非單調（[LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)）

### 2) K-way Merge（Heap / Divide & Conquer）
- 🎯 代表題
  - [ ][LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)（K 個排序鏈結串列）
- 兩種作法比較
| 作法 | 時間 | 空間 | 特點 |
|---|---:|---:|---|
| Min-Heap | $O(N \log k)$ | $O(k)$ | 工程實務最常用 |
| 分治合併 | $O(N \log k)$ | 遞迴深度 $O(\log k)$ | 常數較小、好做平行化 |

---

## 🧠 Backtracking（BacktrackingExploration）📚🔥
- **核心節奏**：==Choose → Explore → Unchoose==
- **最重要不變量**：回溯後狀態必須「完全還原」
- **五大形狀（快速辨識）**
  - Permutation（用 `used[]`）
  - Subset/Combination（用 `start_index`）
  - Target Sum（用 `remaining`）
  - Constraint Satisfaction（用 constraint sets）
  - Grid Path（用 visited / in-place mark）

<!-- markmap: fold -->
### ✅ Backtracking 子型態對照（含題目）
| 子型態 | 主要 State | 去重策略 | 代表題 |
|---|---|---|---|
| 排列 | `used[]` | sort + 同層跳重 |[LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py) / 47 |
| 子集 | `start_index` | sort + 同層跳重 |[LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py) / 90 |
| 組合 | `start_index` + 固定長度 | 上界剪枝 |[LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py) |
| 目標和 | `remaining`（可重用/不可重用） | sort + 同層跳重 |[LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) / 40 / 216 |
| 約束滿足 | cols/diags sets | 天然不重複 |[LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py) / 52 |
| 字串切割 | `start` | validity check |[LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py) / 93 |
| 網格路徑 | visited | 路徑唯一 |[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py) |

### 1) backtracking_permutation（排列）
- 🎯 代表題
  - [ ][LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)（無重複）
  - [ ][LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)（有重複：sort + `if nums[i]==nums[i-1] and not used[i-1]: continue`）

### 2) backtracking_subset（子集）
- 🎯 代表題
  - [ ][LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)[ ][LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)（有重複：sort + 同層跳重 `i>start and nums[i]==nums[i-1]`）

### 3) backtracking_combination（組合 / 固定大小）
- 🎯 代表題
  - [ ][LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)（固定 k：上界剪枝）
  - [ ][LeetCode 216 - Combination Sum III](https://leetcode.com/problems/combination-sum-iii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)（固定 k + 固定和 n：雙重剪枝）

### 4) backtracking_combination_sum（目標和）
- 🎯 代表題
  - [ ][LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)（可重用：遞迴用 `i`）
  - [ ][LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)（不可重用 + 去重：遞迴用 `i+1` + 同層跳重）

### 5) backtracking_n_queens（約束滿足）
- 🎯 代表題
  - [ ][LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)[ ][LeetCode 52 - N-Queens II](https://leetcode.com/problems/n-queens-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)(r-c)`, `used_diag_anti (r+c)`

### 6) backtracking_string_segmentation（字串切割）
- 🎯 代表題
  - [ ][LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)（回文切割：可用 DP 預處理回文 $O(n^2)$）
  - [ ][LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)（IP 切割：固定 4 段 + 長度界剪枝）

### 7) backtracking_grid_path（網格路徑）
- 🎯 代表題
  - [ ][LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)（Word Search：in-place 標記 `#` 再還原）

---

## 🌊 BFS 波前（GridBFSMultiSource）
- **核心心法**：多源同時入隊 → 層序擴散 → 最短時間/步數
- 🎯 代表題
  - [ ][LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)（腐爛橘子）
- 常見 State
  - queue（座標 + 時間）
  - visited / grid 原地改值
  - 層數（minute）用「分層迴圈」或「隨節點帶時間」

---

## 🧱 Heap / TopK（HeapTopK）
- 🎯 代表題
  - [ ][LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)（Kth）
- 常見變形（本資料有 Kernel，題目樣本未覆蓋）
  - TopK Frequent、資料流中位數（two heaps）

---

## 🔍 Binary Search（BinarySearchBoundary / Answer Space）
- 🎯 代表題（本資料集中有）
  - [ ][LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)（同時用到：==答案二分/邊界== + 合併思維）
- 心法
  - **Boundary**：first true / last true（寫成 predicate）
  - **On Answer**：答案具有單調性（可行性隨答案變化）

---

## 🗺️ Roadmap 對齊（本資料題目覆蓋）
- **Sliding Window Mastery**：[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) → 340 → 76 → 567 → 438 → 209
- **Two Pointers Mastery**：[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)/27/283 → 11/125/680 → 15/16 → 21/88/977
- **NeetCode 150 / Blind 75 / Grind 75**：多數題目已在清單內（如[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 3, 11, 15, 21, 23, 76, 141, 215, 994）

---

## ✅ 45 題進度追蹤（依 Kernel 分組）
- Sliding Window：[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py), 76, 209, 340, 438, 567
- Two Pointers：[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 11, 15, 16, 26, 27, 80, 88, 125, 167(related), 283, 680, 977
- Fast–Slow：[LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py), 142, 202, 876
- Partition/Quickselect：[LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py), 905, 922, 215
- Merge/K-way：[LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py), 23, 4
- Backtracking：[LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py), 40, 46, 47, 51, 52, 77, 78, 79, 90, 93, 131, 216
- BFS Grid：[LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
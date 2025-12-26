---
title: LeetCode 核心模式知識圖（Sliding Window / Two Pointers / Backtracking / BFS / Merge / Binary Search / Heap）
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 總覽：從「API Kernel」到「可重用解題引擎」
- **API Kernel（可重用核心）**：把一類題的「狀態機 + 不變量」抽象成模板  
- **Pattern（子模式）**：同一 Kernel 下的具體不變量/目標（最大化/最小化/存在性）  
- **Problem（LeetCode）**：把 Pattern 套上具體題意與邊界條件  
- ==面試最重要==：能用一句話說出「不變量」＋「狀態」＋「指標如何移動」

---

## ✅ 進度追蹤（建議）
- [ ] Sliding Window：先掌握 3 種不變量（unique / ≤K distinct / cover）
- [ ] Two Pointers：熟 6 種形狀（相向/同向Writer/快慢/Partition/枚舉去重/Merge）
- [ ] Backtracking：熟「選→探→撤」與 3 種去重/剪枝
- [ ] BFS（Grid Multi-source）：熟「波前」與「層數=最短步數」
- [ ] K-way Merge / Heap TopK：熟 heap 的 push/pop 與複雜度
- [ ] Binary Search Boundary：熟 first true / last true / answer space

---

## ⚡ API Kernel ①：SubstringSlidingWindow（滑動視窗狀態機）
- **一句話**：右指標只前進；左指標負責恢復不變量  
- **典型複雜度**：$O(n)$（每元素最多進/出視窗一次）
- **狀態資料結構**：`hash_map/counter`（字元頻率）、或 `last_seen_index`

### 🎯 子模式（Patterns）
<!-- markmap: fold -->
- **sliding_window_unique（全唯一）**
  - 不變量：視窗內無重複
  - 狀態：`last_seen_index` 或 freq
  - 代表題：[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- **sliding_window_at_most_k_distinct（至多 K 種）**
  - 不變量：`distinct_count ≤ K`
  - 狀態：freq map（計數歸零要刪 key）
  - 代表題：[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - 不變量：`have` 覆蓋 `need`（每個字元都滿足頻率）
  - 狀態：need/have + `satisfied/required`
  - 代表題：[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)、[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)、[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
  - 不變量：例如 `sum ≥ target`（最小化）或 `sum ≤ budget`（最大化）
  - 狀態：整數 sum
  - 代表題：[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
  - 不變量：window size = k
  - 用途：排列/異位詞檢查（本圖資料以 freq_cover 類呈現）

### 📌 對照表（快速選模板）
| 題目 | 不變量 | 狀態 | 視窗大小 | 目標 |
|---|---|---|---|---|
|[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | 全唯一 | last index / freq | 變動 | 最大化 |
|[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | ≤K distinct | freq map | 變動 | 最大化 |
|[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | 覆蓋 t | need/have + satisfied | 變動 | 最小化 |
|[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | 覆蓋且等頻 | freq + matched | 固定 | 是否存在 |
|[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | 覆蓋且等頻 | freq + matched | 固定 | 全部位置 |
|[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | sum ≥ target | sum | 變動 | 最小化 |

### 🧩 練習路線（Roadmap）
- **sliding_window_path**
  - 入門：[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) →[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - 固定窗：[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) →[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)

## ⚡ API Kernel ②：TwoPointersTraversal（雙指標遍歷）
- **一句話**：每次移動都是「永久排除」一部分可能性  
- **典型複雜度**：$O(n)$（或排序後 $O(n\log n)+O(n)$）

### 🎯 子模式（Patterns）與代表題
- **相向（Opposite）**
  - two_pointer_opposite_search：配對搜尋（排序後）
  - two_pointer_opposite_palindrome：對稱/回文檢查
  - two_pointer_opposite_maximize：最大化函數（如面積）
  - 代表題：[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)、[LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)、[LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)、LeetCode 167（關聯）、[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)（常見替代：hash）
- **同向 Writer（In-place）**
  - two_pointer_writer_dedup：去重
  - two_pointer_writer_remove：移除元素
  - two_pointer_writer_compact：壓縮/搬移（如 0）
  - 代表題：[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)、[LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)、[LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)、[LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
  - fast_slow_cycle_detect / start / midpoint / implicit_cycle
  - 代表題：[LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)、[LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)、[LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)、[LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)
  - two_pointer_three_sum / two_pointer_k_sum
  - 代表題：[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)、[LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - merge_two_sorted_lists / arrays / from_ends
  - 代表題：[LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)、[LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)、[LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

### 🧠 速記：Two Pointers 六型比較
| 型態 | 指標初始化 | 移動規則 | 常用 DS | 代表題 |
|---|---|---|---|---|
| 相向 | `l=0,r=n-1` | 依單調性縮小區間 | array/string |[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py), 125 |
| 同向 Writer | `w=0,r=0` | r 掃描，w 收集 | array |[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py), 27, 283 |
| 快慢 | `slow=head, fast=head` | 1× vs 2× | linked_list |[LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py), 142 |
| Partition | `low,mid,high` | 依 pivot 分區 | array |[LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py), 905 |
| 去重枚舉 | `i + (l,r)` | skip duplicates | array |[LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py) |
| Merge | `i,j` | 取小者前進 | array/list |[LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py), 88 |

### 🧩 練習路線（Roadmap）
- **two_pointers_path**
  - Writer：[LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py) →[LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py) →[LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) →[LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
  - 快慢：[LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py) →[LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py) →[LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py) →[LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)

---

## ⚡ API Kernel ③：BacktrackingExploration（可逆探索）
- **核心節奏**：**Choose → Explore → Unchoose**  
- **不變量**：==狀態必須精準對應當前路徑==（回溯後完全還原）
- **典型複雜度**：指數/階乘（常為 output-sensitive）

### 🎯 子模式（Patterns）→ 題型形狀
<!-- markmap: fold -->
- **Permutation（排列）**
  - backtracking_permutation / permutation_dedup
  - 狀態：`used[]`
  - 代表題：[LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)、[LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)
  - backtracking_subset / subset_dedup / combination
  - 狀態：`start_index`（保證 canonical ordering）
  - 代表題：[LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)、[LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)、[LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
  - backtracking_combination_sum / combination_dedup
  - 狀態：`remaining`
  - 代表題：[LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)、[LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)、[LeetCode 216 - Combination Sum III](https://leetcode.com/problems/combination-sum-iii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)
  - backtracking_n_queens / sudoku
  - 狀態：columns + diagonals sets
  - 代表題：[LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)、[LeetCode 52 - N-Queens II](https://leetcode.com/problems/n-queens-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
  - backtracking_string_segmentation
  - 狀態：`start_index` + validity check（可加 DP 預處理）
  - 代表題：[LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)、[LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
  - backtracking_grid_path
  - 狀態：visited（in-place 標記）
  - 代表題：[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

### 🧷 去重/剪枝（面試高頻失分點）
- **同層去重**：排序後 `if i>start and nums[i]==nums[i-1]: continue`
- **排列去重**：`if i>0 and nums[i]==nums[i-1] and not used[i-1]: continue`
- **界限剪枝**：
  - remaining < 0 立刻 return
  - sorted early break：`if candidates[i] > remaining: break`
  - 組合不足剪枝：`if n - start + 1 < need: return`

---

## ⚡ API Kernel ④：GridBFSMultiSource（多源 BFS 波前）
- **一句話**：把所有起點一起丟進 queue，距離層數同步擴散  
- **保證**：無權圖最短路（層序）
- **典型狀態**：queue + visited / distance grid

### 🎯 子模式
- grid_bfs_propagation
  - 代表題：[LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

### 🧩 練習路線（Roadmap）
- **graph_bfs_path**
  - 入門：[LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)（網格波前）→ 再擴展到一般 BFS shortest path 類

---

## ⚡ API Kernel ⑤：KWayMerge（K 路合併）
- **兩種主流策略**
  - merge_k_sorted_heap：min-heap 維護當前最小頭
  - merge_k_sorted_divide：分治兩兩合併
- **複雜度**
  - heap：$O(N\log K)$
  - divide：$O(N\log K)$（常數不同）

### 代表題
-[LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)（heap / divide）
-[LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)（關聯：二分/合併思路）

---

## ⚡ API Kernel ⑥：MergeSortedSequences（兩序列合併）
- merge_two_sorted_lists：[LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
- merge_sorted_from_ends：[LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)（從尾端寫入避免覆蓋）

---

## ⚡ API Kernel ⑦：TwoPointerPartition（分區 / Dutch Flag / Quickselect）
- **三向分區**：dutch_flag_partition →[LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
- **選第 K 大**：
  - quickselect_partition（平均 $O(n)$）  
  - heap_kth_element（$O(n\log k)$ 或 $O(n + k\log n)$ 變體）
  - 代表題：[LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

## ⚡ API Kernel ⑧：FastSlowPointers（快慢指標）
- fast_slow_cycle_detect：[LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
- fast_slow_midpoint：[LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)

---

## ⚡ API Kernel ⑨：HeapTopK（Top K / Kth / Median）
- heap_kth_element：[LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

---

## ⚡ API Kernel ⑩：BinarySearchBoundary（邊界二分 / 答案二分）
- binary_search_on_answer：[LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)（關聯）
- 重點：first true / last true（模板化寫法避免 off-by-one）

---

## 🧱 資料結構（面試必備對照）
- **hash_map / counter**：Sliding Window、頻率覆蓋、去重統計
- **array / string**：Two pointers、sliding window 主戰場
- **linked_list**：merge、反轉、快慢指標
- **min_heap**：K-way merge、TopK/Kth
- **queue**：BFS 波前
- **hash_set**：N 皇后約束、去重、visited

---

## 🏁 一頁式「先刷哪幾題」清單（高覆蓋）
- Sliding Window：[LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) →[LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) →[LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) →[LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) →[LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) →[LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
- Backtracking：[LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py) →[LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py) →[LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py) →[LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py) →[LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) →[LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py) →[LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py) →[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py) →[LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py) →[LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)
- Heap / Merge：[LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py) →[LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) →[LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py) →[LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py) →[LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)
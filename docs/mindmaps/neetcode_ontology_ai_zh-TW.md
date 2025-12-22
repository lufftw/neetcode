---
title: LeetCode 核心模式心智圖（Sliding Window / Two Pointers / Backtracking / Merge / BFS / Heap / Binary Search）
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 這份知識圖要解決什麼？
- **把「API Kernel → Pattern → 題目」串成可複用的解題 API**
- 面試/競賽常見高頻：==滑動視窗、雙指針、回溯、K-way merge、多源 BFS、TopK/選擇==
- [ ] 先把每個 Kernel 的「不變量 Invariant」背到能默寫  
- [ ] 每個 Kernel 至少刷 2 題（Easy/Medium）建立手感  
- [ ] 最後用 Hard 題驗收（例如視窗/合併/反轉/中位數）

---

## 🧠 API Kernels（核心可重用引擎）
### 1) SubstringSlidingWindow（子字串滑動視窗）📚⚡
- **核心直覺**：右指針只前進；左指針負責維持不變量  
- **時間複雜度**：通常 $O(n)$（每個元素最多進出視窗一次）
- **狀態 State**：`hash_map/counter`（頻率）、或 `last_seen_index`
- **常見兩種目標**
  - **Maximize**：視窗盡量大（違規才縮）
  - **Minimize**：先擴到合法，再盡量縮小

<!-- markmap: fold -->
#### ✅ Pattern 對照表（建議背）
| Problem | Invariant | State | Window Size | Goal |
|---------|-----------|-------|-------------|------|
| [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | 全部唯一 | `last_index` | 變動 | 最大長度 |
| [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | ≤K distinct | freq map | 變動 | 最大長度 |
| [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | 覆蓋需求 | need/have | 變動 | 最小長度 |
| [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | 頻率完全相等 | freq + match count | 固定 | 是否存在 |
| [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | 頻率完全相等 | freq + match count | 固定 | 全部位置 |
| [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | sum ≥ target | `window_sum` | 變動 | 最小長度 |

#### Patterns（子型）
- **sliding_window_unique**：唯一性不變量  
  - 🎯 題： [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- **sliding_window_at_most_k_distinct**：distinct ≤ K  
  - 🎯 題： [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
- **sliding_window_freq_cover**：覆蓋/匹配頻率（Min window / anagram / permutation）  
  - 🎯 題： [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) / [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) / [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
- **sliding_window_cost_bounded**：成本/總和約束  
  - 🎯 題： [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)

---

### 2) TwoPointersTraversal（雙指針遍歷）🎯
- **核心不變量**：指針移動必須「單調」且能==排除解空間==  
- **時間**：多為 $O(n)$；3Sum 類為 $O(n^2)$（外層固定 + 內層雙指針）
- **子家族**
  - Opposite（左右夾逼）
  - Same-direction（讀寫指針，原地修改）
  - Dedup enumeration（排序 + 去重 + 夾逼）
  - Fast–Slow（在另一個 Kernel）

#### Opposite pointers（左右夾逼）
- **何時用**：排序、回文、最大面積等「單調可排除」
- 🎯 題
  - [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)（maximize）
  - [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)

#### Multi-sum enumeration（排序 + 固定一個 + 內層夾逼）
- 🎯 題
  - [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)（==同層去重==是關鍵）
  - [LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)

#### Same-direction writer（讀寫指針：原地去重/移除/壓縮）
- **不變量**：`arr[0:write]` 永遠是「已處理且合法」  
- 🎯 題
  - [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
  - [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)

---

### 3) FastSlowPointers（快慢指針）⚡
- **核心**：Floyd cycle detection（相遇 ⇒ 有環；再找入口）
- 🎯 題
  - [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - [LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
  - [LeetCode 202 - Happy Number](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)（隱式狀態的 cycle）

---

### 4) BacktrackingExploration（回溯：可逆探索）🔥
- **節奏**：Choose → Explore → Unchoose  
- **核心不變量**：==狀態必須完全對應當前路徑==（回來要還原乾淨）
- **複雜度**：通常指數/階乘（輸出敏感）

<!-- markmap: fold -->
#### 回溯五大樹型（速記）
- Permutation：用 `used[]`  
- Subset/Combination：用 `start_index`（保證 canonical order）  
- Target Sum：用 `remaining`（剪枝：`remaining < 0`，排序後 `> remaining` 可 break）  
- Constraint Satisfaction：用 constraint sets（col/diag）  
- Grid Path：用 visited（走過要標記，回來要還原）

#### 題目地圖（由易到難）
- **Permutation**
  - [LeetCode 46 - Permutations](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
  - [LeetCode 47 - Permutations II](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)（排序 + 同層去重）
- **Subset**
  - [LeetCode 78 - Subsets](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
  - [LeetCode 90 - Subsets II](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)
- **Combination / Target**
  - [LeetCode 77 - Combinations](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
  - [LeetCode 39 - Combination Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)（可重複：遞迴用 `i`）
  - [LeetCode 40 - Combination Sum II](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)（不可重複 + 去重：`i>start && a[i]==a[i-1]`）
  - [LeetCode 216 - Combination Sum III](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)（固定 k + sum）
- **String segmentation**
  - [LeetCode 93 - Restore IP Addresses](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)（長度界剪枝）
  - [LeetCode 131 - Palindrome Partitioning](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)（可用 DP 預處理回文）
- **Grid path**
  - [LeetCode 79 - Word Search](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)
- **Constraint satisfaction（驗收 Hard）**
  - [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - [LeetCode 52 - N-Queens II](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)

---

### 5) MergeSortedSequences（合併已排序序列）📚
- **核心**：兩指針 merge（像 merge sort 的 merge step）
- 🎯 題
  - [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - [LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - [LeetCode 977 - Squares of a Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)（從兩端比較後填入）

---

### 6) KWayMerge（K 路合併）⚡
- **兩種主流**
  - heap：$O(N \log K)$（工程上最常用）
  - divide-and-conquer：$O(N \log K)$（常見於面試推導）
- 🎯 題
  - [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - 延伸驗收：中位數類（合併 + 二分答案）
    - [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

---

### 7) TwoPointerPartition（分割 / Dutch Flag / Quickselect）⚡
- **不變量**：維持區間：`< pivot | = pivot | unknown | > pivot`
- 🎯 題
  - [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
  - [LeetCode 905 - Sort Array By Parity](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
  - [LeetCode 922 - Sort Array By Parity II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
  - （partition + 選第 k）
    - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

---

### 8) HeapTopK（堆：TopK / Kth）📌
- **工程觀點**：TopK 常用 min-heap（大小 K），串流/大量資料更穩
- 🎯 題
  - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

---

### 9) GridBFSMultiSource（網格多源 BFS 波前）🌊
- **核心**：把所有 source 一次入隊，層序擴散（wavefront）
- **不變量**：隊列中的元素代表「當前分鐘/步數」邊界
- 🎯 題
  - [LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

---

### 10) LinkedListInPlaceReversal（鏈表原地反轉）🧩
- **核心**：指針重接（prev/curr/next），或分段反轉
- 🎯 題
  - [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
  - 延伸（同家族但未提供資料連結）：全反轉/區間反轉

---

## 🗺️ Roadmap（用題目串起學習路徑）
### Sliding Window Mastery
- [ ] [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- [ ] [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
- [ ] [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
- [ ] [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
- [ ] [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
- [ ] [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)

### Two Pointers Mastery
- [ ] [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
- [ ] [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
- [ ] [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
- [ ] [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [ ] [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- [ ] [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
- [ ] [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)

### Backtracking Mastery
- [ ] [LeetCode 78 - Subsets](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py) → [LeetCode 90 - Subsets II](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)
- [ ] [LeetCode 46 - Permutations](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py) → [LeetCode 47 - Permutations II](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)
- [ ] [LeetCode 39 - Combination Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) → [LeetCode 40 - Combination Sum II](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py) → [LeetCode 216 - Combination Sum III](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)
- [ ] [LeetCode 79 - Word Search](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)
- [ ] [LeetCode 131 - Palindrome Partitioning](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
- [ ] [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py) / [LeetCode 52 - N-Queens II](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)

---

## 🧩 面試常見「一眼辨識」索引
- 看到「最長/最短連續子陣列/子字串」→ **Sliding Window**
- 看到「排序 + 找 pair/tuple」→ **Opposite pointers / 3Sum 架構**
- 看到「原地移除/去重/壓縮」→ **Reader-Writer**
- 看到「Linked list 有環/找入口/找中點」→ **Fast–Slow**
- 看到「列舉所有解」→ **Backtracking（選/遞/還）**
- 看到「K 個已排序序列合併」→ **KWayMerge（heap 或分治）**
- 看到「網格擴散、最短步數、傳染」→ **Multi-source BFS**
- 看到「第 K 大/TopK」→ **Heap / Quickselect**
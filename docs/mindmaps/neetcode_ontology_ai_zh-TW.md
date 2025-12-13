---
title: 面試必勝：滑動視窗與雙指針知識地圖
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---
# 🔥 面試必勝：滑動視窗 × 雙指針策略心智圖
## 🎯 統合觀點
- **架構師視角**：以模組化 API 核心驅動器封裝模式，確保演算法邏輯可重用、易測試並與業務流程解耦。
- **演算法教授視角**：強調==不變量==、指標移動策略與時間空間複雜度的形式化推導，建立可證明的正確性。
- **資深工程師視角**：注重在大型輸入上的穩定性、記憶體佔用與監控指標，避免邊界條件造成效能退化。
- **競賽與面試視角**：快速辨識題型、套用模板，並在壓力下做出常數級優化與剪枝。
- **學習者視角**：依難度分層練習，透過路線規劃與待辦檢核，累積肌肉記憶與錯誤知識庫。

## 🔑 API 核心驅動器
- **`SubstringSlidingWindow`｜動態視窗引擎**
  - ==關鍵不變量==：維持視窗內字元或數值狀態滿足需求（唯一性、頻率、成本）。
  - 典型時間複雜度：$O(n)$，狀態維護以 O(1) 更新為目標；空間取決於字母表或需求集合。
  - 代表性模式：`sliding_window_unique`、`sliding_window_at_most_k_distinct`、`sliding_window_freq_cover`、`sliding_window_cost_bounded`、`sliding_window_fixed_size`。
  - 常見風險：未正確更新離開視窗的狀態、while 修復條件漏判、未處理空視窗或無解情況。
- **`TwoPointersTraversal`｜雙指針協同引擎**
  - ==核心手法==：同向或反向移動兩個指標以維持排序性、緊湊性或對稱性。
  - 子策略涵蓋：`two_pointer_opposite`、`two_pointer_writer_dedup`、`two_pointer_writer_remove`、`two_pointer_writer_compact`、`two_pointer_three_sum`、`two_pointer_k_sum`。
  - 工程注意：指標移動條件須互斥；寫指標不可越界；排序需求需明確。
- **`FastSlowPointers`｜快慢指標檢測器**
  - ==用途==：循環偵測、循環起點定位、鏈表中點尋找、數字序列穩態分析。
  - 代表模式：`fast_slow_cycle_detect`、`fast_slow_cycle_start`、`fast_slow_midpoint`、`fast_slow_implicit_cycle`。
  - 優勢：$O(1)$ 空間；需注意 fast 指標空指標判斷。
- **`TwoPointerPartition`｜原地分區器**
  - ==任務==：以常數空間重排陣列，使元素依條件落入不同區段。
  - 模式：`dutch_flag_partition`、`two_way_partition`、`quickselect_partition`。
  - 工程提示：使用 while 而非 for；注意 pivot 更新順序避免元素遺漏。
- **`MergeSortedSequences`｜序列合併器**
  - ==特點==：兩個有序序列以線性時間合併；支援前向與逆向填充。
  - 模式：`merge_two_sorted_lists`、`merge_two_sorted_arrays`、`merge_sorted_from_ends`。
  - 常見錯誤：未處理一方提前耗盡、輸出陣列從尾端回填時索引錯位。
- **`GridBFSMultiSource`｜網格波前擴散器**
  - ==適用==：多源 BFS（如腐爛橘子）、最短距離填充。
  - 模式：`grid_bfs_propagation`、`bfs_shortest_path`。
  - 重點：初始化佇列含全部起點；記錄層數即時間步。

## 🧠 模式藍圖
### 📏 滑動視窗家族
- **策略流程**：擴張（加入右端）→ 判斷不變量 → 需要時收縮（移動左端）→ 更新答案。
- **狀態設計**：字元頻率映射、哈希表、計數器、數值和、需求-完成計數。
- **變體比較表**：
  
  | 題目 | 不變量 | 狀態結構 | 視窗類型 | 最終目標 |
  |------|--------|----------|----------|----------|
  | [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)（最長無重複子字串） | 視窗內字元互異 | `last_seen` 映射 | 可變 | 最大化長度 |
  | [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)（最多 K 種字元） | 種類數 ≤ K | 頻率表 + 計數 | 可變 | 最大化長度 |
  | [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)（最小涵蓋視窗） | 需求字元頻率全滿足 | Need/Have 雙表 | 可變 | 最小化長度 |
  | [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)（排列判斷） | 與模式頻率完全一致 | 頻率表 | 固定 | 是否存在 |
  | [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)（找所有變位詞） | 與模式頻率一致 | 頻率表 | 固定 | 列舉起點 |
  | [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)（最小和視窗） | 視窗總和 ≥ 目標 | 累計和 | 可變 | 最小化長度 |
- **範例模板**：
  
  ```python
  def 動態滑動視窗(序列):
      狀態 = 初始化()
      左 = 0
      最佳 = 預設值()
      for 右, 元素 in enumerate(序列):
          加入(狀態, 元素)
          while 需收縮(狀態):
              移除(狀態, 序列[左])
              左 += 1
          最佳 = 更新答案(最佳, 左, 右, 狀態)
      return 最佳
  ```
- **洞察提示**：
  - 先判斷是否可用「跳躍左指標」優化（唯一字元類問題）。
  - 固定視窗可直接檢查長度達標後移除右−k位置。
  - 收縮條件須寫成 while；避免只收一次導致不變量失效。
  - 將「需求滿足度」拆成 `need_count` 與 `have_count` 可避免多重比較。

### ⚔️ 雙指針策略矩陣
- **模式快覽表**：
  
  | 模式 | 指標初始化 | 移動規則 | 停止條件 | 時間 | 空間 | 主要應用 |
  |------|------------|----------|----------|------|------|----------|
  | 反向夾逼 | `left=0, right=n-1` | 依目標遞增/遞減 | `left >= right` | $O(n)$ | $O(1)$ | 找對偶、最大值、回文 |
  | 同向讀寫 | `write=0` | `read` 向右，符合才寫 | `read` 完成 | $O(n)$ | $O(1)$ | 原地過濾/壓縮 |
  | 快慢指針 | `slow=head, fast=head` | `slow+=1, fast+=2` | `fast=null`或相遇 | $O(n)$ | $O(1)$ | 循環、中點 |
  | 多指針分區 | `low, mid, high` | 依 pivot 交換 | `mid > high` | $O(n)$ | $O(1)$ | 顏色分類、選擇統計 |
  | 枚舉+去重 | `i` 外層，內層夾逼 | 去重後移動 | `i` 走遍 | $O(n^2)$ | $O(1)$ | 3Sum/4Sum |
  | 兩序列合併 | `i=j=0` 或尾端 | 取較小值前進 | 指標耗盡 | $O(m+n)$ | $O(1)$ | 合併排序、平方有序陣列 |
- **代表題型與洞察**：
  - 反向夾逼：  
    - [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) 容量取決於短板，移動較短邊才有提升機會。  
    - [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py) 與 [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py) 檢查時需同時跳過非字元與容錯一次。
  - 同向讀寫：  
    - [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py) 與 [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py) 透過寫指標控制可保留次數。  
    - [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) 維持前綴為非零元素，最後補零。
  - 快慢指針：  
    - [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)、[LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)、[LeetCode 202 - Happy Number](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)、[LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)；注意初始化放在 `while fast and fast.next`。
  - 多指針分區：  
    - [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)、[LeetCode 905 - Sort Array By Parity](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)、[LeetCode 922 - Sort Array By Parity II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)；需確保交換後不要遺漏 `mid` 重訪。
  - 枚舉+去重：  
    - [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)、[LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)、[LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)（排序版）；排序後才能套模板。
  - 序列合併：  
    - [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)、[LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)、[LeetCode 977 - Squares of a Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py) 需根據資料結構選擇迭代或遞迴。

### 🔄 技術交集與延展
- 滑動視窗常結合雙指針同向移動（視窗左右指標即雙指針），重點是「何時移動哪個指標」的判斷邏輯。
- `SubstringSlidingWindow` 與 `TwoPointerPartition` 可交錯使用：例如先原地過濾，再對有效子陣列套用視窗。
- 多數視窗問題需配合 `hash_map` 或 `counter`；雙指針多搭配排序或原地交換。
- 透過 `PrefixSumRangeQuery` 可將部分視窗問題轉化為二分或哈希查表（如最小和視窗的前綴優化）。

## 📚 關聯資料結構與工具
- **陣列/字串（array/string）**：滑動視窗與雙指針的主要操作對象。
- **雜湊結構（hash_map/hash_set/counter）**：O(1) 追蹤頻率、最後出現位置、需求剩餘量。
- **佇列（queue/deque）**：BFS 层序擴散與單調佇列維持最值。
- **堆（min_heap/max_heap）**：K 路合併、Top-K 元素（如 [LeetCode 23 - Merge k Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)、[LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)）。
- **鏈結串列（linked_list/doubly_linked_list）**：反轉組塊、快慢指標；[LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py) 強調指標操控。
- **網格（grid）**：BFS 多源波前，[LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py) 須記錄時間層數。

## 🌐 家族 × 主題對照
- **`substring_window` 家族**：主題涵蓋 string、hash_table、sliding_window；對應演算法為 `sliding_window` + `two_pointers`。
- **`two_pointers_optimization`／`in_place_array_modification`**：對應主題 array、two_pointers、greedy，常搭 `sorting` 或 `prefix_sum`（較少）。
- **`linked_list_cycle`**：主題 linked_list、two_pointers；搭配 `FastSlowPointers` API。
- **`multi_sum_enumeration`**：需要排序後的雙指針枚舉，注意去重策略。
- **`array_partition`**：利用 `TwoPointerPartition` 完成荷蘭國旗、奇偶排序。
- **`merge_sorted` / `sequence_merge`**：結合 `MergeSortedSequences` 與雙指針；可延伸至 `KWayMerge`。
- **`graph_wavefront`**：多源 BFS 與 `grid` 結構，對應 `graph_bfs_path` 路線。

## 🧪 典型題目挑戰清單
<!-- markmap: fold -->
- 🟢 初階（Easy）
  - [ ] [LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)：哈希表與雙指針概念啟蒙。
  - [ ] [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)：鏈表版序列合併。
  - [ ] [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)：同向讀寫模板。
  - [ ] [LeetCode 27 - Remove Element](https://
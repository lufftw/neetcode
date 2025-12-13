---
title: LeetCode Patterns 知識圖譜 (33 題) — API 核心 → 模式 → 問題 🎯
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 如何快速使用這個心智圖
- **自上而下閱讀**：*API 核心* → *模式* → *問題*（鏈接）
- **練習迴圈**：實作模板 → 解決 2–3 個問題 → 重構成可重用的 `solve(pattern_state_machine)` 心智模型
- **進度追蹤**
  - [ ] 先完成所有 **簡單** 題
  - [ ] 然後是 **中等** 變化題
  - [ ] 最後是 **困難** “邊界情況放大器”
- **問題標籤（3 級）**
  - 🔥 必須知道
  - ⭐ 常見
  - 🧊 了解即可

---

## 🧠 API 核心（“引擎”）
### 🧭 導航指南（選擇正確的核心）
- **需要在目標下查找配對（無排序保證）？** → **HashMapComplement**
- **需要在約束下找出連續子陣列/子字串的最優解？** → **SubstringSlidingWindow**
  - 注意：當 **成立條件在收縮時是單調的**（或視窗是 **固定大小**）時正確。
- **排序 + 配對/三元約束 / 對稱檢查 / 原地編輯？** → **TwoPointersTraversal**
- **根據條件原地分組？** → **TwoPointerPartition**
  - 注意：保持交換安全區域不變（不要“丟失”未知區域）。
- **排序/旋轉陣列中的邊界或“第一個真/最後一個真”？** → **BinarySearchBoundary**
- **下一個更大/更小 / 跨度 / 直方圖面積？** → **MonotonicStack**
- **合併排序流（2 路 / k 路）？** → **MergeSortedSequences / KWayMerge**
- **需要在網格/圖上進行層級/最小步驟傳播？** → **GridBFSMultiSource**

---

### HashMapComplement — *單次補數查找*
- ==核心不變量==：處理索引 `i` 時，雜湊表包含所有來自索引 `< i` 的所需補數
- **核心合約**
  - **輸入**：值的陣列；無排序要求
  - **狀態**：`seen[value] = index`
  - **轉換**：`process(x)`，`insert(x)`
  - **成立條件**：`target - x in seen`
  - **目標**：**存在**（返回索引）
- 系統對應：快速連接 / 去重 / “我是否見過這個鍵？”查找
- 模式
  - **hash_map_complement**
    - 🎯 問題
      - [ ] 🔥 [LeetCode Two Sum](https://leetcode.com/problems/0001_two_sum/)
    - 注意事項：如果輸入已排序（或你排序），你也可以做一個相反指標變體，但它會改變約束/複雜度。
- 相關模式：前綴和 + 雜湊表用於子陣列和；排序變體 → `two_pointer_opposite_search`

---

### SubstringSlidingWindow — *一維視窗狀態機*
- ==核心不變量==：視窗 `[L,R]` 通過 **擴展右側** + **收縮左側** 保持有效
- **時間**：$O(n)$ *攤銷* 當每個索引最多進入/離開視窗一次（單調 `L`,`R`）且有效性更新是 $O(1)$  
- **空間**：$O(\min(n,\Sigma))$ 用於頻率/最後出現地圖；只有當你維護整個字母表的計數時才是 $O(\Sigma)$
- **核心合約**
  - **輸入**：序列（字串/陣列）；約束類型決定 **可變** 與 **固定** 視窗；成本限制變體通常需要 **非負** 成本
  - **狀態**：計數/最後出現 + 輔助計數器（`distinct`, `formed/required`, `matches`, 運行 `sum`）
  - **轉換**：`expand(R)`，`shrink(L)`（當無效時），`record_answer()`
  - **成立條件**：`valid(state)` 在 $O(1)$ 中維持（避免重新掃描地圖）
  - **目標**：最大 / 最小 / 存在 / 全部
- 系統對應：速率限制（移動時間視窗計數器），日誌掃描，“最近 N 分鐘”指標，流去重

<!-- markmap: fold -->
#### 模式速查表（來自文檔）
| 問題 | 不變量（明確條件） | 狀態 | 視窗大小 | 目標 |
|---------|--------------------------------|-------|-------------|------|
| [LeetCode 3 - 最長不重複字串](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | `∀c: windowCount[c] <= 1` | 最後索引地圖 | 可變 | 最大 |
| [LeetCode 340 - 最多 K 個不同字元的最長字串](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | `distinct <= k` | 頻率地圖 + 不同 | 可變 | 最大 |
| [LeetCode 76 - 最小視窗子字串](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | `∀c: windowCount[c] >= needCount[c]`（通過 `formed == required` 跟踪） | 需要/擁有 + 形成/需要 | 可變 | 最小 |
| [LeetCode 567 - 字串排列](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py) | 固定 `len(window)==len(s1)` 且 `∀c: windowCount[c] == needCount[c]`（或 `diffCount==0`） | 頻率 + 匹配/差異 | 固定 | 存在 |
| [LeetCode 438 - 找到字串中的所有字母異位詞](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | 固定 `len(window)==len(p)` 且 `∀c: windowCount[c] == needCount[c]`（或 `diffCount==0`） | 頻率 + 匹配/差異 | 固定 | 全部 |
| [LeetCode 209 - 最小大小子陣列和](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | `windowSum >= target` | 運行和 | 可變 | 最小 |

#### 模式（按目標分組）
- **最大化（可變視窗）**
  - **sliding_window_unique** *(最大化，“跳躍左側”優化)*
    - 🎯 問題
      - [ ] 🔥 [LeetCode 3 - 最長不重複字串](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
    - 關鍵狀態：`last_seen[char]` → `L = max(L, last_seen[c]+1)`
    - 注意事項：在每次 `R` 擴展後更新答案；`L` 只向前移動（單調）。
  - **sliding_window_at_most_k_distinct** *(最大化，無效時收縮)*
    - 🎯 問題
      - [ ] ⭐ [LeetCode 340 - 最多 K 個不同字元的最長字串](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
    - 關鍵不變量：`distinct <= k`（在 $O(1)$ 中跟踪 `distinct`）
    - 注意事項：只有當計數降至 0 時才減少 `distinct`。
- **最小化（可變視窗）**
  - **sliding_window_freq_cover** *(覆蓋 `t`，在有效時最小化)*
    - 🎯 問題
      - [ ] 🔥 [LeetCode 76 - 最小視窗子字串](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) — *在有效時最小化*
    - 關鍵條件：維持 `formed == required`，其中 `formed` 只有當 `windowCount[c] == needCount[c]` 時增量
    - 注意事項：在“當有效時：收縮”迴圈內更新答案（不僅在擴展後）。
  - **sliding_window_cost_bounded** *(數字約束，在有效時最小化)*
    - 🎯 問題
      - [ ] 🔥 [LeetCode 209 - 最小大小子陣列和](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
    - 前提條件 / 注意事項：
      - 當所有數字都是 **正數**（或非負數）時，單調收縮是正確的：擴展 `R` 從不減少和；收縮 `L` 從不增加和。
      - 如果存在負數 → 使用前綴和 + 單調雙端隊列 / 其他技術。
    - 注意事項：需要 **非負** 數字以實現單調收縮；否則切換核心。
- **存在（固定視窗）**
  - **sliding_window_fixed_size** *(固定長度，布林存在)*
    - 🎯 問題
      - [ ] ⭐ [LeetCode 567 - 字串排列](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
    - 關鍵條件：固定 `k = len(s1)` 和 `diffCount == 0`（或所有計數匹配）
    - 注意事項：不要用 while 迴圈收縮；每步滑動一個。
- **枚舉全部（固定視窗）**
  - **sliding_window_fixed_size** *(固定長度，收集所有匹配)*
    - 🎯 問題
      - [ ] ⭐ [LeetCode 438 - 找到字串中的所有字母異位詞](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
    - 關鍵條件：固定 `k = len(p)` 和 `diffCount == 0`（或所有計數匹配）
    - 注意事項：在每次 `R` 一旦視窗大小達到 `k` 時記錄答案。

- 相關模式：
  - `sliding_window_freq_cover` ↔ `sliding_window_fixed_size`（字母異位詞/排列）通過相同的計數器簿記（formed/matches/diff）

---

### TwoPointersTraversal — *序列上的指標編排*
- ==核心不變量==：模式參數化的不變量
  - 相反指標：維持所有需要索引在 `[L,R]` 之外的候選解已被優勢論證排除。
  - 寫入/讀取指標：維持 `arr[:write]` 等於 `arr[:read]` 的期望轉換。
- **核心邊界**：主要是 **陣列/字串掃描**（可選排序）；指標是序列上的索引，而不是結構邊緣。
- 複雜度：通常 $O(n)$ 時間，$O(1)$ 空間（除了排序步驟）
- **核心合約**
  - **輸入**：陣列/字串；某些模式需要排序順序（或預處理排序）
  - **狀態**：指標位置 + 可選運行最佳 + 去重規則
  - **轉換**：`advance_left()`，`advance_right()`，`advance_both()`，`write()`
  - **成立條件**：局部條件在 `arr[L], arr[R]`（和/或 `arr[i]` 用於枚舉）上決定移動
  - **目標**：最大 / 存在 / 全部 / 原地轉換
- 系統對應：雙端掃描，原地壓縮，“流過濾器”風格轉換

#### 模式比較（來自文檔）
| 模式 | 指標初始化 | 移動 | 終止 | 時間 | 空間 | 關鍵用例 |
|---------|--------------|----------|-------------|------|-------|--------------|
| 相反 | `0, n-1` | 向中心 | `L>=R` | $O(n)$ | $O(1)$ | 排序對 / 回文 / 最大化 |
| 同方向 | `write, read` | 向前 | `read==n` | $O(n)$ | $O(1)$ | 原地修改 |
| 快慢 | `slow, fast` | 1× / 2× | 相遇或空 | $O(n)$ | $O(1)$ | 循環 / 中點 |
| 去重枚舉 | `i` + `L,R` | 嵌套 | 完成 | $O(n^2)$ | $O(1)$ | 3Sum/4Sum |

#### 模式
- **two_pointer_opposite_maximize**
  - 🎯 問題
    - [ ] 🔥 [LeetCode 11 - 盛最多水的容器](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - 洞察：移動 **較短** 高度的指標
  - 注意事項：需要優勢論證（如果較短的一側不變，移動較高的一側不能改善面積）。
- **two_pointer_three_sum** *(去重枚舉)*
  - 🎯 問題
    - [ ] 🔥 [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
    - [ ] ⭐ [LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - 需要：先排序 ($O(n\log n)$)，然後用去重掃描
  - 注意事項：需要排序；注意去重和溢出邊界。
- **two_pointer_opposite_palindrome**
  - 🎯 問題
    - [ ] ⭐ [LeetCode 125 - 有效回文](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
    - [ ] ⭐ [LeetCode 680 - 有效回文 II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
  - 注意事項：準確定義跳過/規範化規則（字母數字與標點符號；最多一個刪除）。
- **two_pointer_writer_dedup**
  - 🎯 問題
    - [ ] ⭐ [LeetCode 26 - 從排序陣列中刪除重複項](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
    - [ ] ⭐ [LeetCode 80 - 從排序陣列中刪除重複項 II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
  - 注意事項：不變量是 `arr[:write]` 是 `arr[:read]` 的去重前綴（維持寫入規則）。
- **two_pointer_writer_remove**
  - 🎯 問題
    - [ ] ⭐ [LeetCode 27 - 移除元素](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - 注意事項：確保每次 `read` 步驟前進；`write` 只在保留元素時前進。
- **two_pointer_writer_compact**
  - 🎯 問題
    - [ ] ⭐ [LeetCode 283 - 移動零](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
  - 注意事項：通過讀取順序寫入來保持非零的相對順序。

- 相關模式：
  - 排序 + 雙指標 ↔ `two_pointer_three_sum`
  - 寫入指標 ↔ 穩定壓縮問題

---

### FastSlowPointers — *Floyd + 中點 + 隱式序列*
- ==核心不變量==：如果存在循環，`fast` 會遇到 `slow`
- **核心邊界**：指標遍歷 **鏈結結構或函數迭代**（隱式圖），主要用於 **循環/中點** 性質。
- 交叉鏈接：快慢是雙指標移動在 *迭代器* 而非索引上的專門化。
- **核心合約**
  - **輸入**：鏈結串列節點指標或函數迭代 `x_{t+1}=f(x_t)`
  - **狀態**：`slow`, `fast`（和可選的第二階段指標）
  - **轉換**：`slow = next(slow)`，`fast = next(next(fast))`
  - **成立條件**：`fast is None`（無循環）或 `slow == fast`（檢測到循環）
  - **目標**：存在（循環），定位（循環開始），找到中點
- 系統對應：迭代器/狀態機中的循環檢測；檢測生成序列中的周期性
- 模式
  - **fast_slow_cycle_detect**
    - [ ] 🔥 [LeetCode 141 - 鏈結串列循環](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - **fast_slow_cycle_start**
    - [ ] 🔥 [LeetCode 142 - 鏈結串列循環 II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - **fast_slow_midpoint**
    - [ ] ⭐ [LeetCode 876 - 鏈結串列的中間節點](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
  - **fast_slow_implicit_cycle**
    - [ ] ⭐ [LeetCode 202 - 快樂數字](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)

---

### BinarySearchBoundary — *第一個/最後一個真 + 旋轉邊界*
- **核心合約**
  - **輸入**：排序/單調條件空間；有時是旋轉排序陣列
  - **狀態**：`lo, hi, mid` + 條件區域上的不變量
  - **轉換**：根據條件將搜索空間縮小一半
  - **成立條件**：單調條件 `P(i)`（false→true）或排序順序屬性
  - **目標**：第一個真 / 最後一個真 / 找到目標 / 邊界索引
- 系統對應：版本推出（“第一個錯誤構建”），閾值調整，容量邊界搜索
- 模式
  - **binary_search_rotated**
    - 🎯 問題
      - [ ] 🔥 [LeetCode 搜索旋轉排序陣列](https://leetcode.com/problems/0033_search_in_rotated_sorted_array/)
    - 注意事項：與 `nums[mid]` 和一側邊界比較以決定哪一半是排序的。
  - **binary_search_first_true**
    - 🎯 問題
      - [ ] ⭐ [LeetCode 在排序陣列中找到元素的第一個和最後一個位置](https://leetcode.com/problems/0034_find_first_and_last_position_of_element_in_sorted_array/)
    - 注意事項：使用半開區間或一致的 `lo/hi` 更新以避免無限迴圈。
  - **binary_search_last_true**
    - 🎯 問題
      - [ ] ⭐ [LeetCode 在排序陣列中找到元素的第一個和最後一個位置](https://leetcode.com/problems/0034_find_first_and_last_position_of_element_in_sorted_array/)
    - 注意事項：實作為 `first_true(> target) - 1` 或對稱邊界搜索。
  - **binary_search_on_answer**
    - 🎯 問題
      - [ ] ⭐ [LeetCode 在旋轉排序陣列中找到最小值](https://leetcode.com/problems/0153_find_minimum_in_rotated_sorted_array/)
      - [ ] 🧊 [LeetCode 找到峰值元素](https://leetcode.com/problems/0162_find_peak_element/)
    - 注意事項：必須定義可行性條件 `feasible(x)`，該條件在 `x` 中是單調的。

---

### MonotonicStack — *下一個更大/更小 + 面積/跨度*
- **核心合約**
  - **輸入**：需要最近更大/更小或跨度/面積貢獻的陣列
  - **狀態**：具有單調值（遞增或遞減）的索引堆疊
  - **轉換**：當堆疊違反單調性時，彈出並解決貢獻；然後推入當前索引
  - **成立條件**：每步後堆疊是單調的（按值）
  - **目標**：下一個更大/更小的索引/值；聚合面積/跨度
- 系統對應：“下一個更高價格”，延遲峰值跨度，天際線/面積聚合
- 模式
  - **next_greater_element**
    - 🎯 問題
      - [ ] 🔥 [LeetCode 每日溫度](https://leetcode.com/problems/0739_daily_temperatures/)
      - [ ] ⭐ [LeetCode 下一個更大元素 I](https://leetcode.com/problems/0496_next_greater_element_i/)
    - 注意事項：存儲索引；當前值是“下一個更大”時在彈出時解決答案。
  - **histogram_max_rectangle**
    - 🎯 問題
      - [ ] 🔥 [LeetCode 直方圖中的最大矩形](https://leetcode.com/problems/0084_largest_rectangle_in_histogram/)
    - 注意事項：附加哨兵 0 以刷新堆疊；通過先前較小的索引計算寬度。

---

### TwoPointerPartition — *原地分區“小型快速排序”*
- ==核心不變量==：區域按屬性分區
- **核心合約**
  - **輸入**：陣列；條件/分類函數；允許原地
  - **狀態**：區域邊界（`low/mid/high` 或 `i/j`）
  - **轉換**：`swap()` + 根據元素類別移動邊界指標
  - **成立條件**：每次交換後區域不變量保持真
  - **目標**：原地分組 / 選擇
- 系統對應：按嚴重性分區日誌，按類型分桶項目，原地穩定/不穩定壓縮
- 模式
  - **dutch_flag_partition**
    - [ ] ⭐ [LeetCode 75 - 顏色分類](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
    - 不變量（3 區域）：
      - `arr[0:low] == 0`
      - `arr[low:mid] == 1`
      - `arr[high+1:n] == 2`
      - `mid` 掃描未知區域 `arr[mid:high+1]`
    - 注意事項：與 `high` 交換時，不要增加 `mid`，直到處理交換進來的元素。
  - **two_way_partition**
    - [ ] 🧊 [LeetCode 905 - 按奇偶排序陣列](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
    - [ ] 🧊 [LeetCode 922 - 按奇偶排序陣列 II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
    - 注意事項：定義哪一側消耗相等元素；避免無限交換。
  - **quickselect_partition** *(通過分區選擇)*
    - 🎯 問題
      - 參見 **選擇**：[LeetCode 215 - 陣列中的第 K 大元素](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
    - 注意事項：期望 $O(n)$ 但最壞情況 $O(n^2)$；隨機化樞軸 / introselect 風格防禦。
    - 複雜度說明：期望 $O(n)$，最壞情況 $O(n^2)$ 除非隨機化樞軸 / 中位數的中位數；空間 $O(1)$ 迭代或 $O(\log n)$ 遞歸。

- 相關模式：
  - 分區 ↔ 快速選擇 ↔ 堆積 top-k（相同選擇問題，不同約束）

---

### MergeSortedSequences — *合併兩個排序序列*
- ==核心不變量==：輸出前綴是完全排序的
- **核心合約**
  - **輸入**：兩個排序序列（列表/陣列）；比較器
  - **狀態**：兩個讀取指標 + 輸出指標
  - **轉換**：取較小的頭，前進該指標
  - **成立條件**：輸出前綴是排序的，並且包含完全消耗的項目
  - **目標**：構建合併排序序列
- 系統對應：合併兩個排序流/分片，兩路連接類操作
- 模式
  - **merge_two_sorted_lists**
    - [ ] ⭐ [LeetCode 21 - 合併兩個排序鏈結串列](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - **merge_two_sorted_arrays**
    - [ ] ⭐ [LeetCode 88 - 合併排序陣列](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - **merge_sorted_from_ends**
    - [ ] ⭐ [LeetCode 977 - 有序陣列的平方](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

- 相關模式：
  - 合併兩個 ↔ k 路合併 ↔ “邊界 + 合併思維”（兩個排序陣列的中位數）

---

### KWayMerge — *合併 K 個排序序列*
- 兩個主要實作
  - **merge_k_sorted_heap** → $O(N\log k)$ 時間，$O(k)$ 堆
  - **merge_k_sorted_divide** → $O(N\log k)$ 時間，有時較小的常數
- **核心合約**
  - **輸入**：K 個排序序列 / 迭代器；可能是流式
  - **狀態**：當前頭的堆（或配對合併遞歸）
  - **轉換**：彈出最小頭，推入該序列的下一個
  - **成立條件**：堆包含每個非空序列的當前最小候選者
  - **目標**：產生全局排序流
- 系統對應：合併排序分片，日誌壓縮，搜索索引段合併（LSM 風格）

<!-- markmap: fold -->
#### 取捨（k 路合併）
- 堆：最適合 **流式** / 迭代器；$O(k)$ 記憶體；簡單；當你不能隨機訪問列表時很好。
- 分治：相同的漸近 $O(N\log k)$；通常較少的堆操作；當列表在記憶體中時很好。
- 展平 + 排序：$O(N\log N)$；最簡單但通常對於大 k 或大 N 較慢。

- 🎯 問題
  - [ ] 🔥 [LeetCode 23 - 合併 k 個排序鏈結串列](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - 相關“混合思維”：[LeetCode 4 - 兩個排序陣列的中位數](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

---

### HeapTopK — *在流式更新下保持最佳 K*
- **核心合約**
  - **輸入**：流/陣列；比較器；`k`
  - **狀態**：大小 ≤ `k` 的堆
  - **轉換**：推入；如果大小>k 彈出；查看第 k
  - **成立條件**：堆包含到目前為止看到的最佳 `k`（按排序）
  - **目標**：保持 top-k / 第 k 個元素
- 系統對應：熱門話題，排行榜維護，頂部錯誤代碼；擴展：Count-Min Sketch 用於近似重擊者
- 模式
  - **heap_kth_element**
    - 🎯 問題
      - 參見 **選擇**：[LeetCode 215 - 陣列中的第 K 大元素](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
    - 注意事項：$O(n\log k)$ 時間，$O(k)$ 空間；流式友好且穩定。

---

### GridBFSMultiSource — *網格上的波前傳播*
- 模式
  - **grid_bfs_propagation**
    - [ ] 🔥 [LeetCode 994 - 腐爛的橘子](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- **核心合約**
  - **輸入**：作為隱式圖的網格；多個來源
  - **狀態**：佇列（frontier），已訪問/更新的網格，分鐘/層級
  - **轉換**：`process_level()`，擴展到 4/8 鄰居，將新激活的節點加入佇列
  - **成立條件**：每個格子最多處理一次（或具有單調距離）
  - **目標**：最小時間/步驟傳播（或檢測不可能）
- 實作時的不變量：佇列持有當前“分鐘/層級”的前沿
- 系統對應：多源最短時間傳播（網路中斷擴散，傳染模擬，依賴傳播）

<!-- markmap: fold -->
#### 取捨（網格 BFS）
- 多源 BFS：一次通過；在無權重網格中給出最近來源的最短時間。
- 重複單源 BFS：通常冗餘且較慢（通常 $k$ 倍工作）。
- 記憶體：佇列 + 已訪問可能很大；考慮在允許時進行原地標記。

- 相關模式：
  - BFS 波前 ↔ 無權重圖中的最短路徑；多源初始化是“預處理”步驟。

---

### LinkedListInPlaceReversal — *指標手術*
- **核心合約**
  - **輸入**：鏈結串列頭；段大小 `k`（可選）
  - **狀態**：`prev/curr/next` 指標；組邊界
  - **轉換**：在段內反轉指標；縫合段
  - **成立條件**：反轉段保持連接；段外保持不變
  - **目標**：原地轉換列表結構
- 模式
  - **linked_list_k_group_reversal**
    - [ ] 🔥 [LeetCode 25 - k 組反轉節點](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- 也包括核心鏈結串列算術
  - [ ] ⭐ [LeetCode 2 - 兩數相加](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py)

---

### BacktrackingExploration — *帶剪枝的搜索樹*
- **核心合約**
  - **輸入**：決策空間；約束
  - **狀態**：部分分配 + 約束簿記
  - **轉換**：選擇 → 遞迴 → 撤銷（回溯）
  - **成立條件**：部分分配一致（提前剪枝）
  - **目標**：枚舉所有解 / 找到一個
- 模式
  - **backtracking_n_queens**
    - [ ] 🧊 [LeetCode 51 - N 皇后](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)

---

## 🧭 路線圖切片（接下來要做什麼）
### 滑動視窗精通 📚
- [ ] 完成 `sliding_window_unique` 集群（見 `SubstringSlidingWindow → 最大化（可變視窗）`）
- [ ] 完成 `sliding_window_at_most_k_distinct` 集群（見 `SubstringSlidingWindow → 最大化（可變視窗）`）
- [ ] 完成 `sliding_window_freq_cover` 集群（見 `SubstringSlidingWindow → 最小化（可變視窗）`）
- [
---
title: LeetCode 知識圖譜思維導圖 (核心模式 → API 核心 → 問題) 🎯
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 如何使用這張圖 📚
- **目標**：學習*可轉移的核心*（API）→ 辨識*模式* → 解決*問題*
- **圖例 / 標籤**
  - 🔥 必須知道（高頻 / 錨點）
  - ⭐ 常見（常見後續）
  - 🧊 不錯的了解（可選 / 較低投資回報）
- **進度追蹤器**
  - [ ] 每個核心做 1 題（廣度）
  - [ ] 每個核心做 3 題（深度）
  - [ ] 在 20 分鐘內從頭開始重新解決“錨點”問題 ⚡

## 核心索引（你應該內化的“API”） 🔥
- 🔥 **SubstringSlidingWindow** → 連續子字串狀態機
- 🔥 **TwoPointersTraversal** → 協調指標移動
- 🔥 **TwoPointerPartition** → 原地分割
- 🔥 **FastSlowPointers** → 循環 / 中點
- 🔥 **MergeSortedSequences** + **KWayMerge** → 合併已排序的流
- 🔥 **BacktrackingExploration** → 選擇 → 探索 → 取消選擇
- 🔥 **GridBFSMultiSource** → 網格上的波前 BFS
- 🔥 **BinarySearchBoundary** → 邊界 + 答案空間搜尋
- 🔥 **HeapTopK** → 前 k / 第 k / 流媒體中位數
- 🔥 **MonotonicStack** → 下一個更大/更小，直方圖，水
- 🔥 **PrefixSumRangeQuery** → 範圍和，子陣列和
- 🔥 **UnionFindConnectivity** → 連通性 / 組件
- 🔥 **TreeTraversalDFS/BFS** → 遞迴/迭代 DFS，層次遍歷 BFS
- 🔥 **TopologicalSort** → DAG 排序
- 🔥 **TriePrefixSearch** → 前綴字典 / 多詞搜尋
- 🔥 **DPSequence/DPInterval** → 序列 DP，區間 DP
- ⭐ **HashIndexLookup** → 雜湊表補數查找（Two Sum 預設）

- **API 合約（緊湊）**
  - **SubstringSlidingWindow**
    - **輸入**：序列（字串/陣列）；連續視窗；`L,R` 只向前移動
    - **狀態**：計數/對應表/最後出現，計數器，運行總和
    - **鉤子**：`add(R)`，`remove(L)`，`is_valid()`，`record_answer(L,R)`
    - **複雜度**：$O(n)$ 攤銷（加上對應表操作）；**失敗模式**：`L` 減少；無效/有效收縮方向不匹配
  - **TwoPointersTraversal**
    - **輸入**：陣列/字串；通常已排序或對稱；指標單調移動
    - **狀態**：索引 + 小的標量狀態；有時是寫入索引
    - **鉤子**：`advance_L()`，`advance_R()`，`should_move_left?`，`should_move_right?`，`record_answer()`
    - **複雜度**：$O(n)$；**失敗模式**：在沒有排序/單調屬性的情況下使用相反指標；忘記去重規則
  - **TwoPointerPartition**
    - **輸入**：可變陣列；謂詞 / 類別；允許交換
    - **狀態**：區域邊界（例如，`low,mid,high`）
    - **鉤子**：`classify(x)`，`swap(i,j)`，`advance_region()`
    - **複雜度**：$O(n)$，$O(1)$ 空間；**失敗模式**：區域不變量被破壞；邊界偏移一個
  - **FastSlowPointers**
    - **輸入**：鏈結串列 / 函式迭代 `f(x)`；指標以 1x/2x 移動
    - **狀態**：兩個指標；可選的訪問不需要
    - **鉤子**：`step_slow()`，`step_fast()`，`meet?`，`reset_to_head()`
    - **複雜度**：$O(n)$ 時間，$O(1)$ 空間；**失敗模式**：空檢查；錯誤的階段-2 重置
  - **MergeSortedSequences**
    - **輸入**：兩個已排序的序列（陣列/列表）；輸出新的或原地的（當支持時）
    - **狀態**：i/j 指標；輸出指標；哨兵/虛擬頭
    - **鉤子**：`pick_min(i,j)`，`append(x)`，`advance_source()`
    - **複雜度**：$O(m+n)$；**失敗模式**：穩定性假設；忘記尾部附加
  - **KWayMerge**
    - **輸入**：k 個已排序的序列/迭代器；流媒體友好
    - **狀態**：當前頭的最小堆（或成對合併遞迴）
    - **鉤子**：`push(head_of_stream)`，`pop_min()`，`advance_stream(s)`
    - **複雜度**：堆 $O(N\log k)$；分治 $O(N\log k)$；**失敗模式**：推送空值；比較器錯誤
  - **BacktrackingExploration**
    - **輸入**：決策空間；約束；可選排序去重
    - **狀態**：當前路徑 + used[]/start 索引 + 約束集
    - **鉤子**：`choose(x)`，`is_valid()`，`explore()`，`unchoose(x)`，`record(path)`
    - **複雜度**：指數；**失敗模式**：“幽靈標記”（未取消選擇），重複發射
  - **GridBFSMultiSource**
    - **輸入**：網格圖；多個來源；無權重邊
    - **狀態**：佇列；訪問（變更網格或分開）；層次計數器
    - **鉤子**：`enqueue_sources()`，`neighbors(r,c)`，`mark_visited()`，`process_level()`
    - **複雜度**：$O(R\cdot C)$；**失敗模式**：多次將同一格子入佇列；錯誤的層次計數
  - **BinarySearchBoundary**
    - **輸入**：單調謂詞 `P(x)` 在索引空間或答案空間上
    - **狀態**：`lo,hi,mid`；謂詞函式
    - **鉤子**：`P(mid)`，`move_lo/hi`，`return_boundary()`
    - **複雜度**：$O(\log n)$ 謂詞調用；**失敗模式**：非單調謂詞；偏移一個返回
  - **HeapTopK**
    - **輸入**：流/陣列；比較器；k
    - **狀態**：堆大小 ≤ k（或兩個堆用於中位數）
    - **鉤子**：`push(x)`，`pop()`，`peek()`，`rebalance()`
    - **複雜度**：$O(n\log k)$ 典型；**失敗模式**：錯誤的堆類型；k=0；比較器溢出
  - **MonotonicStack**
    - **輸入**：陣列；下一個更大/更小或跨度查詢
    - **狀態**：保持單調屬性的索引堆疊
    - **鉤子**：`while stack violates: pop`，`answer[popped]=i`，`push(i)`
    - **複雜度**：$O(n)$ 攤銷；**失敗模式**：錯誤的嚴格與非嚴格單調性；忘記哨兵清理
  - **PrefixSumRangeQuery**
    - **輸入**：陣列；範圍查詢或目標和子陣列
    - **狀態**：運行前綴；雜湊表從前綴→計數/最早索引
    - **鉤子**：`pref += x`，`lookup(pref-target)`，`update_map(pref)`
    - **複雜度**：$O(n)$；**失敗模式**：缺少基礎情況 `pref=0`；整數溢出
  - **UnionFindConnectivity**
    - **輸入**：元素 + 合併操作；無向連通性查詢
    - **狀態**：parent[]，rank/size[]
    - **鉤子**：`find(x)`，`union(a,b)`，`connected(a,b)`
    - **複雜度**：~攤銷逆阿克曼；**失敗模式**：忘記路徑壓縮；錯誤的組件計數更新
  - **TreeTraversalDFS/BFS**
    - **輸入**：樹根；遞迴/堆疊/佇列
    - **狀態**：堆疊/佇列；樹不需要訪問
    - **鉤子**：`visit(node)`，`push(children)`，`record_level()`
    - **複雜度**：$O(n)$；**失敗模式**：空處理；遞迴深度（堆疊溢出）
  - **TopologicalSort**
    - **輸入**：DAG；鄰接列表；入度
    - **狀態**：佇列（Kahn）或訪問狀態（DFS）
    - **鉤子**：`build_indegree()`，`enqueue_zero_indegree()`，`pop()`，`decrement_indegree()`
    - **複雜度**：$O(V+E)$；**失敗模式**：循環；缺少出度為零的節點
  - **TriePrefixSearch**
    - **輸入**：字串字典；前綴查詢
    - **狀態**：字典樹節點；子節點對應表/陣列；終端標誌
    - **鉤子**：`insert(word)`，`walk(prefix)`，`dfs_collect()`
    - **複雜度**：$O(total_chars)$ 構建；查詢 $O(|prefix|)$；**失敗模式**：記憶體膨脹；錯誤的終端處理
  - **DPSequence/DPInterval**
    - **輸入**：序列或區間 `[i..j]`；遞迴
    - **狀態**：dp[] 或 dp[i][j]
    - **鉤子**：`transition()`，`base_cases()`，`iterate_order()`
    - **複雜度**：因問題而異；**失敗模式**：錯誤的迭代順序；缺少基礎情況

- **選擇指南（路由層） 🧭**
  - 連續子陣列/子字串 + 增量有效性 ⇒ **SubstringSlidingWindow**
  - 已排序 + 配對/區間推理或對稱掃描 ⇒ **TwoPointersTraversal**
  - 原地分類成區域（交換，分割） ⇒ **TwoPointerPartition**
  - 鏈結串列循環 / 中點 / 隱式迭代循環 ⇒ **FastSlowPointers**
  - 兩個已排序流 ⇒ **MergeSortedSequences**
  - K 個已排序流 / 合併日誌 ⇒ **KWayMerge**
  - 無權重網格/圖中的最小步驟/時間 ⇒ **GridBFSMultiSource** (BFS)
  - 單調謂詞在索引/答案空間上 ⇒ **BinarySearchBoundary**
  - 第 k / 前 k / 流媒體指標 ⇒ **HeapTopK**
  - 需要下一個更大/更小跨度 ⇒ **MonotonicStack**
  - 許多子陣列和 / 範圍和 ⇒ **PrefixSumRangeQuery**
  - 合併下的連通性 ⇒ **UnionFindConnectivity**
  - 樹結構 ⇒ **TreeTraversalDFS/BFS**
  - DAG 先決條件/順序 ⇒ **TopologicalSort**
  - 前綴字典 / 多詞搜尋 ⇒ **TriePrefixSearch**
  - 最佳子結構/重疊 ⇒ **DPSequence/DPInterval**

- **按領域查找 🗂️**
  - **陣列/字串** → SubstringSlidingWindow, TwoPointersTraversal, TwoPointerPartition, PrefixSumRangeQuery, MonotonicStack, BinarySearchBoundary, HeapTopK
  - **鏈結串列** → FastSlowPointers, 鏈結串列操作 (DummyHeadSplice / ReverseSegment / KGroupReverse)
  - **樹** → TreeTraversalDFS/BFS, BinarySearchBoundary (BST), DP (樹 DP 變體)
  - **圖** → Grid/Graph BFS, TopologicalSort, UnionFindConnectivity
  - **堆 / 流** → HeapTopK, KWayMerge

- **組合（常見核心組合） 🧩**
  - **BinarySearchBoundary + FeasibilityCheck** (答案空間搜尋)
  - **HeapTopK + Streaming** (中位數/百分位數)
  - **BacktrackingExploration + Memoization (DFS DP)** (字串分段變體)
  - **KWayMerge + HeapTopK** (合併流然後保留前 k)
  - **BinarySearchBoundary + Merge partition-by-count** (兩個已排序陣列的中位數)

---

## 1) 滑動視窗 (SubstringSlidingWindow) 🪟
- **API 合約**
  - **輸入**：字串/陣列；連續視窗；`L` 和 `R` 只向前移動
  - **狀態**：`last_seen` 或 `freq/need/have`，計數器，`window_sum`
  - **鉤子**：`add(R)`，`remove(L)`，`is_valid()`，`record_answer(L,R)`
  - **複雜度**：$O(n)$ 攤銷（單調指標）；**失敗模式**：`L` 減少；錯誤的收縮條件；缺少 `max()` 在左跳時
- **不變量**：在單調推進指標時，保持當前視窗的謂詞 `Valid(L,R)`。
- **核心不變量（形式化）**：保持當前視窗的不變謂詞 `Valid(L,R)`。單調推進 `R`；當 `Valid` 被違反時（或對於最小化問題當 `Valid` 保持時），單調推進 `L` 恢復不變量。**如果兩個指標只向前移動**，每個索引被處理 $O(1)$ 次 ⇒ $O(n)$ 時間（加上對應表操作的成本）。
- **狀態選擇**
  - `last_seen_index` 對應表（跳-L 優化）
    - 當執行 `L = max(L, last_seen[c] + 1)` 時，確保 `L` 永不減少；在處理 `R` 之後更新 `last_seen`。
  - `freq` 對應表 + `distinct_count`
  - `need/have` 對應表 + `satisfied/required`
  - 數值 `window_sum`
- **模式比較表**
  - | 問題 | 不變量 | 狀態 | 視窗大小 | 目標 |
    |---------|-----------|-------|-------------|------|
    | 🔥 [LeetCode 3 - 無重複字元的最長子字串](https://leetcode.com/problems/0003_longest_substring_without_repeating_characters/) | 全部唯一（跳左） | 最後索引對應表 | 可變 | 最大化 |
    | ⭐ [LeetCode 340 - 最多包含 K 個不同字元的最長子字串](https://leetcode.com/problems/0340_longest_substring_with_at_most_k_distinct/) | ≤K 個不同 | 頻率對應表 | 可變 | 最大化 |
    | 🔥 [LeetCode 76 - 最小覆蓋子字串](https://leetcode.com/problems/0076_minimum_window_substring/) | 覆蓋所有需要的 | 需要/擁有 + 滿足 | 可變 | 最小化 |
    | ⭐ [LeetCode 567 - 字符串的排列](https://leetcode.com/problems/0567_permutation_in_string/) | 精確頻率匹配 | 頻率 + 匹配 | 固定 | 存在 |
    | ⭐ [LeetCode 438 - 找到字串中所有字母異位詞](https://leetcode.com/problems/0438_find_all_anagrams_in_a_string/) | 精確頻率匹配 | 頻率 + 匹配 | 固定 | 所有位置 |
    | ⭐ [LeetCode 209 - 最小長度子陣列和](https://leetcode.com/problems/0209_minimum_size_subarray_sum/) | 和 ≥ 目標（在非負性下單調） | 整數和 | 可變 | 最小化 *(假設 nums[i] ≥ 0；負數會破壞收縮邏輯)* |
- **模板原型（穩定入口點）**
  - **(1) 跳左唯一性** (`L = max(L, last[x]+1)`)
    - 偽代碼
      - ```text
        L = 0
        last = {}
        for R in [0..n-1]:
          if s[R] in last:
            L = max(L, last[s[R]] + 1)   # L 永不減少
          last[s[R]] = R
          record_answer(L, R)
        ```
    - 錨點 (🔥)：[LeetCode 3 - 無重複字元的最長子字串](https://leetcode.com/problems/0003_longest_substring_without_repeating_characters/)
    - 後續 1 (⭐)：[LeetCode 340 - 最多包含 K 個不同字元的最長子字串](https://leetcode.com/problems/0340_longest_substring_with_at_most_k_distinct/)
    - 後續 2 (🧊)：大字母表/Unicode → 偏好雜湊表；注意每個字元的成本
  - **(2) 當有效時收縮（最小化 / 強制界限）** (`while valid: shrink`)
    - 偽代碼
      - ```text
        L = 0
        init_state()
        for R in [0..n-1]:
          add(R)
          while is_valid():      # 對於最小化；反轉條件以“收縮直到有效”
            record_answer(L, R)
            remove(L)
            L += 1
        ```
    - 錨點 (🔥)：[LeetCode 76 - 最小覆蓋子字串](https://leetcode.com/problems/0076_minimum_window_substring/)
    - 後續 1 (⭐)：[LeetCode 209 - 最小長度子陣列和](https://leetcode.com/problems/0209_minimum_size_subarray_sum/) *(假設 nums[i] ≥ 0；如果允許負數，使用前綴和 + 單調佇列 / 二分搜尋變體，根據問題而定)*
    - 後續 2 (⭐)：[LeetCode 340 - 最多包含 K 個不同字元的最長子字串](https://leetcode.com/problems/0340_longest_substring_with_at_most_k_distinct/) *(頻率 + 當 >K 時收縮)*
  - **(3) 固定大小的滾動視窗（精確匹配 / 字母異位詞）** (`size == k`)
    - 偽代碼
      - ```text
        L = 0
        init_state_for_window()
        for R in [0..n-1]:
          add(R)
          if R - L + 1 > k:
            remove(L)
            L += 1
          if R - L + 1 == k and is_match():
            record_answer(L, R)
        ```
    - 錨點 (⭐)：[LeetCode 567 - 字符串的排列](https://leetcode.com/problems/0567_permutation_in_string/)
    - 後續 1 (⭐)：[LeetCode 438 - 找到字串中所有字母異位詞](https://leetcode.com/problems/0438_find_all_anagrams_in_a_string/)
    - 後續 2 (🧊)：流媒體視窗檢查 → 維護 `matched` 計數器以避免完整對應表比較
- **小決策指南**
  - `last_seen` 跳左 vs `freq + shrink`
    - 當不變量是“無重複”並且可以直接跳轉以恢復唯一性時，使用 **跳左**。
    - 當允許但有限制（≤K 個不同 / 計數 / 和約束）時，使用 **freq + shrink**。
- **常見面試陷阱**
  - “最小化視窗”需要：**當有效時 → 收縮**（不僅僅是一次收縮）
  - “精確匹配”最適合：**固定視窗** + `matched` 計數器
- **現實世界映射**
  - 限速視窗 / 配額執行
  - 日誌掃描模式 / 事件流上的警報規則
  - 最近事件上的欺詐啟發式（滾動約束）

---

## 2) 雙指標走訪 (TwoPointersTraversal) 👯
- **API 合約**
  - **輸入**：陣列/字串；通常已排序/對稱；指標單調移動
  - **狀態**：索引 + 小的不變量；穩定壓縮的可選寫入索引
  - **鉤子**：`should_move_left/right`，`advance()`，`record_answer()`
  - **複雜度**：$O(n)$；**失敗模式**：在沒有排序/單調推理的情況下應用相反指標；缺少去重跳過
- **不變量**：每次指標移動後，丟棄的區域被證明是無關的（在問題的優勢論證下不能提高可行性/最佳性）。
- **心理模型**：每次移動*證明*排除區域不能包含答案
- **邊界與非目標**
  - 走訪移動指標以*證明不可能性* / 優勢；通常是只讀或穩定寫入。
  - 反例：**Sort Colors** 不是走訪；它是**分割**，因為交換維持了 3 個區域。
- **子家族**
  - **相反指標**（已排序/對稱優化）
    - 最大化目標
      - 錨點 (🔥)：[LeetCode 11 - 盛最多水的容器](https://leetcode.com/problems/0011_container_with_most_water/) *(移動較短的一側)*
      - 後續 1 (⭐)：高度平局 / 重複 → 仍然可以安全地移動任一較短的一側；推理是優勢
      - 後續 2 (🧊)：需要在約束下的索引 → 隨著進行存儲最佳配對
    - 回文驗證
      - 錨點 (🔥)：[LeetCode 125 - 驗證回文串](https://leetcode.com/problems/0125_valid_palindrome/)
      - 後續 1 (⭐)：[LeetCode 680 - 驗證回文串 II](https://leetcode.com/problems/0680_valid_palindrome_ii/) *(一次跳過分支)*
      - 後續 2 (🧊)：自定義標準化規則 → 小心定義 `next_alnum()` 幫助器
    - “Two Sum 家族”
      - **Two Sum（未排序）** → 預設核心是 **HashIndexLookup**（雜湊表 / 補數）
        - 錨點 (🔥)：[LeetCode 1 - Two Sum](https://leetcode.com/problems/0001_two_sum/)
      - **Two Sum（已排序 / 排序後）** → 相反指標
        - 注意：排序是 $O(n\log n)$ 並且除非你跟踪它們，否則會丟失原始索引。
  - **去重 + 已排序陣列上的列舉**
    - 錨點 (🔥)：[LeetCode 15 - 3Sum](https://leetcode.com/problems/0015_3sum/) *(外部 i + 內部 L/R + 跳過重複)*
    - 後續 1 (⭐)：[LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/0016_3sum_closest/)
    - 後續 2 (🧊)：一般 k-sum → 遞迴 + 雙指標基礎（索引去重規則）
  - **同方向（讀者/寫入者）原地**
    - 去重
      - 錨點 (⭐)：[LeetCode 26 - 刪除排序陣列中的重複項](https://leetcode.com/problems/0026_remove_duplicates_from_sorted_array/)
      - 後續 1 (⭐)：[LeetCode 80 - 刪除排序陣列中的重複項 II](https://leetcode.com/problems/0080_remove_duplicates_from_sorted_array_ii/)
      - 後續 2 (🧊)：允許最多 k 個重複 → 參數化寫入規則
    - 刪除元素
      - 錨點 (⭐)：[LeetCode 27 - 移除元素](https://leetcode.com/problems/0027_remove_element/)
      - 後續 1 (🧊)：穩定與不穩定刪除 → 寫入指標是穩定的，與末端交換則不是
    - 壓縮 / 穩定過濾
      - 錨點 (⭐)：[LeetCode 283 - 移動零](https://leetcode.com/problems/0283_move_zeroes/)
      - 後續 1 (🧊)：穩定壓縮“保留謂詞”以獲得任意值
- **快速不變量表**
  - | 模式 | 不變量 | 典型問題 |
    |---------|-----------|------------------|
    | 相反（最大化） | 對於 [LeetCode 11 - 盛最多水的容器](https://leetcode.com/problems/0011_container_with_most_water/)：移動較短的一側不能改善任何保持較高一側作為邊界的容器，因此丟棄它是安全的。 | [LeetCode 11 - 盛最多水的容器](https://leetcode.com/problems/0011_container_with_most_water/) |
    | 相反（回文） | 對於 [LeetCode 125 - 驗證回文串](https://leetcode.com/problems/0125_valid_palindrome/)：所有在 `[L..R]` 之外的字元都已驗證匹配（忽略指定的非字母數字）。 | [LeetCode 125 - 驗證回文串](https://leetcode.com/problems/0125_valid_palindrome/) |
    | 寫入者 | `arr[0:write]` 是“保留的”（穩定） | [LeetCode 26 - 刪除排序陣列中的重複項](https://leetcode.com/problems/0026_remove_duplicates_from_sorted_array/), [LeetCode 283 - 移動零](https://leetcode.com/problems/0283_move_zeroes/) |
    | 已排序列舉 | 沒有重複的元組被發出 | [LeetCode 15 - 3Sum](https://leetcode.com/problems/0015_3sum/) |

---

## 3) 分割 (TwoPointerPartition) 🚧
- **API 合約**
  - **輸入**：可變陣列；分類謂詞/類別；允許交換
  - **狀態**：區域邊界；樞軸/類別函式
  - **鉤子**：`classify(x)`，`swap(i,j)`，`advance pointers by region`
  - **複雜度**：$O(n)$ 時間，$O(1)$ 空間；**失敗模式**：區域不變量被破壞，當中間未推進時無限循環
- **不變量**：在每次交換/推進後維持區域不變量（已分類 | 未知 | 已分類）。
- **使用時機**：原地分類成區域；通常是選擇/排序的構建塊
- **邊界與非目標**
  - 分割交換以強制*區域不變量*；變異是核心。
  - 反例：**Valid Palindrome** 不是分割；它是走訪（沒有基於交換的區域）。
- **典型區域不變量**
  - 荷蘭國旗：維持索引 `(low, mid, high)`：
    - `A[0..low-1] = 0`，`A[low..mid-1] = 1`，`A[mid..high]` 未知，`A[high+1..n-1] = 2`。
  - 二分分割：維持：
    - `A[0..i-1]` 滿足謂詞 `P`，`A[j+1..n-1]` 滿足 `¬P`，`A[i..j]` 未知。
- **模式**
  - **荷蘭國旗（3 路分割）** (`dutch_flag_partition`)
    - 錨點 (🔥)：[LeetCode 75 - 排序顏色](https://leetcode.com/problems/0075_sort_colors/)
    - 後續 1 (⭐)：快速排序 3 路分割（重複繁多）
    - 後續 2 (🧊)：穩定分割需要額外空間（此核心不穩定）
  - **二分分割** (`two_way_partition`)
    - 錨點 (⭐)：[LeetCode 905 - 按奇偶排序陣列](https://leetcode.com/problems/0905_sort_array_by_parity/)
    - 後續 1 (🧊)：[LeetCode 922 - 按奇偶排序陣列 II](https://leetcode.com/problems/0922_sort_array_by_parity_ii/) *(可選變體)*
- **變異/穩定性/邊界情況（工程）**
  - **變異輸入？** 是（基於交換）
  - **穩定？** 否（相對順序不保留）
  - **典型時間/空間**：$O(n)$ / $O(1)$
  - **邊界情況**：全在一類；許多相等；指標交叉邊界

---

## 4) 快慢指標 (FastSlowPointers) 🐢🐇
- **API 合約**
  - **輸入**：鏈結串列頭或函式 `f(x)` 產生下一個狀態
  - **狀態**：`slow`, `fast` 指標；可選階段切換
  - **鉤子**：`step_slow()`，`step_fast()`，`meet?`，`reset_to_head()`
  - **複雜度**：$O(n)$ 時間，$O(1)$ 空間；**失敗模式**：空引用在 `fast.next`，錯誤的重置邏輯
- **不變量**：快慢之間的距離可預測地變化（快進 2 倍），使得循環檢測和入口恢復成為可能。
- **兩個階段（Floyd）**
  - 階段 1：檢測循環
  - 階段 2：找到循環開始
  - 證明片段：在相遇點，如果循環長度為 `λ` 且從頭到循環入口的距離為 `μ`，則相遇發生在 `t` 步後，`t ≡ μ (mod λ)`；重置一個指標到頭部並同時移動兩個指標一步保持到入口的相等距離，因此它們在入口相遇。
- **問題**
  - 錨點 (🔥) 檢測循環：[LeetCode 141 - 環形鏈結串列](https://leetcode.com/problems/0141_linked_list_cycle/)
  - 錨點 (🔥) 找到循環開始：[LeetCode 142 - 環形鏈結串列 II](https://leetcode.com/problems/0142_linked_list_cycle_ii/)
  - 後續 1 (⭐) 隱式循環（函式迭代）：[LeetCode 202 - 快樂數](https://leetcode.com/problems/0202_happy_number/)
  - 後續 2 (⭐) 中點：[LeetCode 876 - 鏈結串列的中間節點](https://leetcode.com/problems/0876_middle_of_the_linked_list/)
- **現實世界映射**
  - 檢測指標圖中的循環 / 損壞的下一個指標
  - 在確定性模擬中檢測重複狀態
  - 找到鏈結結構上的拆分/合併操作的中點

---

## 5) 合併已排序序列 (MergeSortedSequences + KWayMerge) 🔗
- **API 合約**
  - **輸入**：已排序序列（2 路或 k 路）；可能是陣列或鏈結串列
  - **狀態**：指標進入來源；輸出構建器；k 路的堆
  - **鉤子**：`pick_next()`，`append(x)`，`advance
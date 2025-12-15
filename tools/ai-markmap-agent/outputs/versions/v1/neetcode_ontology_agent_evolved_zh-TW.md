---
title: LeetCode 知識圖譜心智圖（核心模式 → API 核心 → 題目）🎯
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 如何使用這張地圖 📚
- **目標**：學會*可遷移的核心*（API）→ 辨識*模式* → 解出*題目*
- **圖例 / 標籤**
  - 🔥 anchor / 必知
  - ⭐ 常見
  - ➕ 選用 / 強化
  - 🧩 混合（核心的組合）
- **進度追蹤**
  - [ ] 每個核心做 1 題（廣度）
  - [ ] 每個核心做 3 題（深度）
  - [ ] 20 分鐘內從零重解「anchor」題 ⚡

## Kernel Index（你應該內化的「API」）🔥
- **核心平台 Kernels（基元）**
  - **HashMapLookup** 🔥
  - **PrefixSumRangeQuery** 🔥
  - **BinarySearchBoundary** 🔥
  - **MonotonicStack** 🔥
  - **TreeTraversalDFS / TreeTraversalBFS** 🔥
  - **GraphTraversalBFS / GraphTraversalDFS + TopologicalSort** 🔥
  - **UnionFindConnectivity** ⭐
  - **DPSequence / DPInterval** 🔥
  - **TriePrefixSearch** ⭐
- **本地圖已整理的 Kernels（下方展開）**
  - **HashMapLookup** 🔥
  - **PrefixSumRangeQuery** 🔥
  - **TwoPointersTraversal** ⭐ → 唯讀走訪（搜尋/驗證；縮小搜尋空間）
  - **SubstringSlidingWindow** 🔥 → 連續子字串狀態機
  - **BinarySearchBoundary** 🔥 → 邊界 + 答案空間搜尋
  - **TreeTraversalDFS / TreeTraversalBFS** 🔥
  - **GraphTraversalBFS / GraphTraversalDFS + TopologicalSort** 🔥
  - **HeapTopK** ⭐ → top-k / 第 k 大 / 串流中位數
  - **MergeSortedSequences** + **KWayMerge** ⭐ → 合併已排序串流
  - **TwoPointerPartition (InPlaceCompaction)** ⭐ → 變異核心（分割/壓縮）
  - **MonotonicStack** ⭐
  - **UnionFindConnectivity** ⭐
  - **BacktrackingExploration** ⭐ → 選擇 → 探索 → 取消選擇
  - **GridBFSMultiSource** ⭐ → 格子上的波前 BFS
  - **FastSlowPointers** ⭐ → 環 / 中點
  - **DPSequence / DPInterval** 🔥
  - **TriePrefixSearch** ⭐
- **典型組合（combinators）**
  - **BinarySearchBoundary + FeasibilityCheck**（答案空間搜尋）🧩
  - **Partition + Quickselect**（選擇）🧩
  - **HeapTopK + Streaming aggregation**（動態第 k 大/中位數）🧩
  - **Backtracking + Memoization/DP**（帶快取的搜尋）🧩
  - **BFS + Multi-source init**（波前）🧩
  - **MergeSortedSequences + TwoPointersTraversal**（類 merge 掃描）🧩
- **規劃中 / Backlog**
  - *(隨著新增章節，持續補上更具代表性的題目)*

---

## Router（快速選核心）🧭
- | 題目訊號 | 導向 |
  |---|---|
  | 未排序陣列/字串，需要互補 / 計數 / 頻率 | **HashMapLookup** |
  | 區間和、子陣列和 = K、「子陣列數量…」 | **PrefixSumRangeQuery**（+ 雜湊表） |
  | 連續 + 在視窗上做最佳化（max/min/exists） | **SubstringSlidingWindow** |
  | 已排序 + 單調移動可證明排除 | **TwoPointersTraversal (Opposite)** |
  | 原地分類/壓縮/覆寫 | **TwoPointerPartition (InPlaceCompaction)** |
  | 「第一個/最後一個」、邊界、旋轉、可行性單調 | **BinarySearchBoundary** |
  | 樹走訪 / LCA / 驗證 BST | **TreeTraversalDFS/BFS** |
  | 圖的連通塊 / 最短跳數 / DAG 排序 | **GraphTraversalBFS/DFS + TopologicalSort** |
  | 第 k 大/top-k/串流中位數 | **HeapTopK** / **Partition+Quickselect** |
  | 合併已排序串流 / k 個串列 | **MergeSortedSequences / KWayMerge** |
  | 格子上的波前傳播 | **GridBFSMultiSource** |
  | 選/探/取消選；產生組合 | **BacktrackingExploration** |
  | 下一個更大/更小；直方圖/接雨水 | **MonotonicStack** |
  | 合併操作下的連通性 | **UnionFindConnectivity** |
  | 最佳子結構 / 重疊子問題 | **DPSequence/DPInterval** |
  | 前綴搜尋 / 單字字典 | **TriePrefixSearch** |

---

## Reverse Index（題目 → 核心）🔎
- | 題目 | 主要核心 | 次要核心 |
  |---|---|---|
  | [LeetCode 1](https://leetcode.com/problems/two-sum/description/)
  | [LeetCode 2](https://leetcode.com/problems/add-two-numbers/description/)
  | [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/)
  | [LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/description/)
  | [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/)
  | [LeetCode 15](https://leetcode.com/problems/3sum/description/)
  | [LeetCode 16](https://leetcode.com/problems/3sum-closest/description/)
  | [LeetCode 21](https://leetcode.com/problems/merge-two-sorted-lists/description/)
  | [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/)
  | [LeetCode 25](https://leetcode.com/problems/reverse-nodes-in-k-group/description/)
  | [LeetCode 26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/)(InPlaceCompaction) | writer |
  | [LeetCode 27](https://leetcode.com/problems/remove-element/description/)(InPlaceCompaction) | writer |
  | [LeetCode 39](https://leetcode.com/problems/combination-sum/description/)
  | [LeetCode 40](https://leetcode.com/problems/combination-sum-ii/description/)
  | [LeetCode 46](https://leetcode.com/problems/permutations/description/)[] |
  | [LeetCode 47](https://leetcode.com/problems/permutations-ii/description/)
  | [LeetCode 51](https://leetcode.com/problems/n-queens/description/)
  | [LeetCode 52](https://leetcode.com/problems/n-queens-ii/description/)
  | [LeetCode 75](https://leetcode.com/problems/sort-colors/description/)(InPlaceCompaction) | dutch flag |
  | [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/)
  | [LeetCode 77](https://leetcode.com/problems/combinations/description/)
  | [LeetCode 78](https://leetcode.com/problems/subsets/description/)
  | [LeetCode 79](https://leetcode.com/problems/word-search/description/)
  | [LeetCode 80](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/)(InPlaceCompaction) | writer |
  | [LeetCode 88](https://leetcode.com/problems/merge-sorted-array/description/)
  | [LeetCode 90](https://leetcode.com/problems/subsets-ii/description/)
  | [LeetCode 93](https://leetcode.com/problems/restore-ip-addresses/description/)
  | [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/)
  | [LeetCode 131](https://leetcode.com/problems/palindrome-partitioning/description/)
  | [LeetCode 141](https://leetcode.com/problems/linked-list-cycle/description/)
  | [LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/description/)
  | [LeetCode 202](https://leetcode.com/problems/happy-number/description/)
  | [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/)
  | [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/)
  | [LeetCode 216](https://leetcode.com/problems/combination-sum-iii/description/)
  | [LeetCode 283](https://leetcode.com/problems/move-zeroes/description/)(InPlaceCompaction) | 穩定壓縮 |
  | [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/)
  | [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/)
  | [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/)
  | [LeetCode 680](https://leetcode.com/problems/valid-palindrome-ii/description/)
  | [LeetCode 876](https://leetcode.com/problems/hand-of-straights/description/)
  | [LeetCode 905](https://leetcode.com/problems/length-of-longest-fibonacci-subsequence/description/)(InPlaceCompaction) | 雙向 |
  | [LeetCode 922](https://leetcode.com/problems/possible-bipartition/description/)(InPlaceCompaction) | 雙向 |
  | [LeetCode 977](https://leetcode.com/problems/distinct-subsequences-ii/description/)
  | [LeetCode 994](https://leetcode.com/problems/prison-cells-after-n-days/description/)

---

## 1) 雜湊表查找（HashMapLookup）🔥
- **契約（標準）**
  - **輸入**：項目的序列/串流；鍵值抽取；可選的目標/互補規則
  - **狀態**：`seen`（雜湊表 / 雜湊集合）、計數、最後索引
  - **不變式**：`seen` 精確反映已處理的前綴；查找只查詢前綴
  - **推進規則**：掃一次；使用完 `seen` 後再更新（避免自我配對 bug）
  - **複雜度旋鈕**：鍵大小 / 雜湊；碰撞行為；記憶體 = 不同鍵的數量
  - **常見失敗模式**
    - 在檢查互補前就更新 `seen`（自我匹配）
    - 忘記重複值語意（存第一個 vs 最後一個索引）
- **偽簽章（API 表面）**
  - `hash_lookup(seq, key(x), on_hit(key)->answer, on_miss(update))`
  - 延伸點：`key`、重複策略、儲存值（count/index/list）
- **題目**
  - 🔥 [LeetCode 1](https://leetcode.com/problems/two-sum/description/)
    - 註：目標 $O(n)$；存索引；先查互補再插入。
- **工作中會出現的地方**
  - 去重 ID/事件；頻率統計；資料管線中的類 join 查找

---

## 2) 前綴和（PrefixSumRangeQuery）🔥
- **契約（標準）**
  - **輸入**：數值序列；區間查詢或目標和限制
  - **狀態**：`prefix[i]`，或累積 `pref`；雜湊表 `count[pref]`
  - **不變式**：`pref = sum(seq[0..i])`；區間和 `sum(l..r)=pref[r]-pref[l-1]`
  - **推進規則**：累加一次；以 $O(1)$ 回答查詢或用雜湊表計數
  - **複雜度旋鈕**：前綴陣列的記憶體 vs 串流；雜湊表大小
  - **常見失敗模式**
    - 區間端點 off-by-one
    - 有負數時用滑動視窗（應改用前綴技巧）
- **偽簽章（API 表面）**
  - `prefix_sum(seq) -> prefix[]`
  - `count_subarrays(seq, target) using pref_count: count += pref_count[pref-target]`
  - 延伸點：存最早索引（求最長）、存計數（求數量）
- **代表性題目**
  - [LeetCode 560](https://leetcode.com/problems/subarray-sum-equals-k/description/)
  - [LeetCode 525](https://leetcode.com/problems/contiguous-array/description/)
  - [LeetCode 238](https://leetcode.com/problems/product-of-array-except-self/description/)
  - [LeetCode 304](https://leetcode.com/problems/range-sum-query-2d-immutable/description/)
- **工作中會出現的地方**
  - 時間序列彙總；累積指標；以差分做異常偵測

---

## 3) 雙指標走訪（TwoPointersTraversal）👯 ⭐
- **契約（標準）**
  - **輸入**：唯讀陣列/字串；比較器/判定式；（常見：已排序或具對稱結構）
  - **狀態**：`L`, `R`，目前最佳答案；可選的跳過規則
  - **不變式**：答案落在目前搜尋空間內；指標移動永遠不會重新擴張它
  - **推進規則**：每步依規則移動一個指標 ⇒ 縮小搜尋空間 ⇒ 終止
  - **複雜度旋鈕**：排序前提（可能增加 $O(n \log n)$）；跳過重複
  - **常見失敗模式**
    - 移錯指標（破壞排除證明）
    - 漏掉去重跳過迴圈（輸出重複）
- **偽簽章（API 表面）**
  - `two_pointers_opposite(arr, L=0, R=n-1, move_rule(state, L, R) -> (L', R'), on_answer)`
  - `two_pointer_sorted_enum(arr_sorted, i_loop, L/R inner, skip_duplicates=True)`
  - 延伸點：移動規則、停止條件、去重策略、目標更新

- **心智模型**：每次移動都在*證明*某個被排除區域不可能含有答案

- **子家族**
  - **相向指標**（已排序/對稱最佳化）
    - 最大化目標
      - 🔥 [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/)(移動較短邊)*
        - 每一步保證可丟掉一側邊界索引，因為面積受較短高度限制且寬度只會縮小。
        - 註：目標 $O(n)$；正確性關鍵在「短邊是瓶頸」。
    - 回文驗證
      - ⭐ [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/)
        - 每一步保證被丟棄的外側字元不影響成立性，因為它們要嘛被匹配、要嘛被判定式跳過。
      - ⭐ [LeetCode 680](https://leetcode.com/problems/valid-palindrome-ii/description/)(一次跳過分支)*
        - 每一步保證最多只需對一次不匹配做分支，因為只允許刪除一個字元。
    - 「Two Sum 家族」
      - 主要（未排序）：🔥 [LeetCode 1](https://leetcode.com/problems/two-sum/description/)
      - 已排序版本：⭐ [LeetCode 167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/)
        - 每一步保證可以丟棄 `L` 或 `R`，因為在已排序輸入上，和對每個指標都是單調的。
  - **已排序陣列上的去重 + 逐一產生**
    - 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/)(外層 i + 內層 L/R + 跳過重複)*
      - 每一步保證重複會被丟棄，因為排序後可用同值跳過且不會漏掉新三元組。
      - 註：排序後目標 $O(n^2)$；`i`, `L`, `R` 的去重跳過要精準。
    - ⭐ [LeetCode 16](https://leetcode.com/problems/3sum-closest/description/)
      - 每一步保證在固定 `i` 下，指標移動會丟掉只會在單調方向上更遠的那些和。

- **快速不變式表**
  - | 模式 | 不變式 | 典型題目 |
    |---------|-----------|------------------|
    | 相向 | 答案在 `[L..R]` | [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/)
    | 已排序逐一產生 | 不輸出重複 tuple | [LeetCode 15](https://leetcode.com/problems/3sum/description/)

- **工作中會出現的地方**
  - 掃描已排序日誌；對齊兩個有序資料來源；剖析器中的對稱驗證

---

## 4) 滑動視窗（SubstringSlidingWindow）🪟 🔥
- **契約（標準）**
  - **輸入**：連續序列（字串/陣列）；不變式判定式 `Valid(state)`；加入/移除的更新規則
  - **狀態**：計數/頻率、`distinct_count`、`need/have`、總和、最後出現索引
  - **不變式**：透過擴張 `R` 後再縮小 `L` 來維持（或恢復）`Valid(L,R)`
  - **推進規則**：`R` 單調前進；`L` 只在需要恢復 `Valid` 時單調前進 ⇒ 終止
  - **複雜度旋鈕**：對應表/陣列更新成本；字母表大小 `σ`；記憶體 $O(σ)$ 或 $O(k)$
  - **常見失敗模式**
    - 最小化時沒有用 `while` 迴圈縮視窗
    - 有負數時套用和的視窗（破壞單調性）

- **核心不變式**：維持不變式 `Valid(L,R)`；`R` 單調前進，而 `L` 只在需要時單調前進以恢復 `Valid`。此單調性表示每個指標最多遞增 `n` 次，因此在*假設對應表更新具 $O(1)$ 平均攤還*下，更新總成本為 $O(n)$。

- **偽簽章（API 表面）**
  - `sliding_window(seq, on_add(x), on_remove(x), is_valid(state), on_answer(L,R,state))`
  - 延伸點：合法性判定式（≤K distinct / 涵蓋 / sum）、固定 vs 可變視窗、答案彙整（max/min/全部）

- **狀態選擇**
  - `last_seen_index` 對應表（jump-L 最佳化）
  - `freq` 對應表 + `distinct_count`
  - `need/have` 對應表 + `satisfied/required`
  - 數值 `window_sum`

- **模式比較表**
  - | 題目 | 不變式 | 狀態 | 視窗大小 | 目標 |
    |---------|-----------|-------|-------------|------|
    | 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/)
    | ⭐ [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/)
    | 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/)[c] >= need[c]` | need/have + satisfied | 可變 | 最小化 |
    | ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/)[c]==need[c]`（或用已定義準則的 `matched==required`） | freq + matched | 固定 | 存在 |
    | ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/)[c]==need[c]`（或 `matched==required`） | freq + matched | 固定 | 所有位置 |
    | 🔥 [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/)(要求所有數字非負；若有負數用前綴和 + 單調結構 / 二分搜尋變體)* | sum ≥ target | 整數總和 | 可變 | 最小化 |

- **模式**
  - **不重複視窗**（`sliding_window_unique`）
    - 偽簽章：`unique_window(s) -> max_len`（延伸：存索引以重建子字串）
    - Anchor：🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/)(學 jump-left)==
      - 註：目標 $O(n)$；ASCII vs Unicode 取捨（array[128/256] vs hashmap）。
      - 每一步保證 `L..(newL-1)` 可被丟棄，因為任何起點早於 `newL` 的視窗仍會包含 `s[R]` 的重複。
  - **最多 K 種不同**（`sliding_window_at_most_k_distinct`）
    - 偽簽章：`at_most_k_distinct(s, k) -> max_len`（延伸：「剛好 K」可用 at_most(K)-at_most(K-1)）
    - Anchor：🔥 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/)
      - 每一步保證在不合法時，前進 `L` 會丟棄那些不移除元素就不可能合法的前綴（移除下 distinct-count 單調）。
  - **頻率涵蓋 / 完全匹配**（`sliding_window_freq_cover`）
    - 偽簽章：`min_cover(s, need) -> (L,R)`（延伸：追蹤 satisfied 計數）
    - 最小化涵蓋：🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/)
      - 註：目標 $O(n)$；記憶體 $O(σ)$；字母表有限時用陣列。
      - 每一步保證當視窗已涵蓋 `need` 時，縮小 `L` 可丟掉左側字元，因為在同一個 `R` 下更大的視窗對「最小化」永遠不更好。
    - 固定大小完全匹配（存在）：⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/)
      - 每一步保證任何長度不是 `|p|` 的視窗都可丟棄，因為完全匹配判定依賴固定長度。
    - 固定大小完全匹配（收集全部）：⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/)
      - 每一步保證平移一步可丟棄前一個起點，因為只有目前固定視窗才可能對應該起點匹配。
  - **成本上限 / 和限制**（`sliding_window_cost_bounded`）
    - 偽簽章：`min_len_sum_at_least(nums_nonneg, target) -> min_len`
    - Anchor：🔥 [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/)
      - 註：正確性要求所有數字**為正或非負**；若有負數，改用 **PrefixSumRangeQuery**（+ 單調佇列 / 雜湊表）。典型「視窗失敗」例子：[LeetCode 862](https://leetcode.com/problems/find-and-replace-in-string/description/)
      - 每一步保證一旦 `sum >= target`，前進 `L` 會丟棄那些在同一個 `R` 下只會讓視窗更長的起點。

- **常見面試陷阱**
  - 「最小化視窗」需要：**while 合法 → 縮小**（不只縮一次）
  - 「完全匹配」最適合：**固定視窗** + `matched` 計數器

- **工作中會出現的地方**
  - 速率限制（rolling windows）；日誌/工作階段分析；近期範圍內去重

---

## 5) 二分搜尋邊界（BinarySearchBoundary）🔥
- **契約（標準）**
  - **輸入**：已排序陣列 / 索引或答案空間上的隱式單調判定式
  - **狀態**：`lo`, `hi` 邊界；判定式 `P(mid)`；目前最佳邊界
  - **不變式**：true 區與 false 區在維持的邊界下保持分離
  - **推進規則**：每次迭代縮小 `[lo, hi]` ⇒ 以 $O(\log n)$ 終止
  - **複雜度旋鈕**：判定式成本；mid 的整數溢位；包含/不包含邊界
  - **常見失敗模式**
    - off-by-one（錯的迴圈條件 / 回傳）
    - 判定式非單調（二分搜尋不成立）

- **模板（邊界）**
  - `first_true(lo, hi):` 找最小 `i` 使 `P(i)=true`
  - `last_true(lo, hi):` 找最大 `i` 使 `P(i)=true`
  - `lower_bound(x):` 第一個滿足 `A[i] >= x` 的索引
  - `upper_bound(x):` 第一個滿足 `A[i] > x` 的索引

- **模板（答案空間搜尋）**
  - `min_x_s.t._feasible(x)`，其中 `feasible(x)` 單調（false...false,true...true）
  - 組合：**BinarySearchBoundary + FeasibilityCheck** 🧩

- **代表性題目**
  - [LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/description/)
  - [LeetCode 34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/description/)
  - [LeetCode 153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/)
  - [LeetCode 162](https://leetcode.com/problems/find-peak-element/description/)
  - [LeetCode 875](https://leetcode.com/problems/longest-mountain-in-array/description/)
  - [LeetCode 1011](https://leetcode.com/problems/flip-binary-tree-to-match-preorder-traversal/description/)
  - 🧩 🔥 [LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/description/)(以元素數量做分割不變式；在分割索引上二分搜尋，而不是合併)*
    - 註：目標 $O(\log \min(m,n))$；定義不變式「左分割有 k 個元素，且所有左 ≤ 所有右」。

- **工作中會出現的地方**
  - 調整門檻值（SLA/SLO）；以可行性做容量規劃；「第一個失敗點」診斷

---

## 6) 樹走訪（TreeTraversalDFS/BFS）🌳 🔥
- **契約（標準）**
  - **輸入**：樹根；鄰居存取（子節點）
  - **狀態**：遞迴堆疊 / 顯式堆疊；（BFS）佇列 + 層級標記
  - **不變式**：DFS：堆疊表示目前路徑；BFS：佇列包含前緣
  - **推進規則**：每個節點走訪一次；推入子節點；結構耗盡即終止
  - **複雜度旋鈕**：遞迴深度 vs 迭代；記憶體 = 高度（DFS）或寬度（BFS）
  - **常見失敗模式**
    - 斜樹造成遞迴深度溢位
    - 漏掉 base case / null 檢查

- **偽簽章（API 表面）**
  - `dfs(node, enter, exit)` / `dfs_iterative(stack, on_pop)`
  - `bfs(root, on_level(level_nodes))`
  - 延伸點：前序/中序/後序；累積路徑；父指標

- **代表性題目**
  - [LeetCode 102](https://leetcode.com/problems/binary-tree-level-order-traversal/description/)
  - [LeetCode 104](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/)
  - [LeetCode 236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/description/)
  - [LeetCode 199](https://leetcode.com/problems/binary-tree-right-side-view/description/)
  - [LeetCode 98](https://leetcode.com/problems/validate-binary-search-tree/description/)

- **工作中會出現的地方**
  - 走訪 AST/設定樹；相依樹；階層式彙整

---

## 7) 圖走訪 + 拓樸排序（GraphTraversalBFS/DFS + TopologicalSort）🌐 🔥
- **契約（標準）**
  - **輸入**：圖的鄰居函式；起點集合；（Topo）入度計數
  - **狀態**：visited 集合；佇列/堆疊；（Topo）入度為 0 的佇列
  - **不變式**：visited 防止重複處理；BFS 分層給出最少跳數（無權重）
  - **推進規則**：彈出前緣、推入未走訪鄰居；拓樸移除入度為 0 的節點
  - **複雜度旋鈕**：相鄰表示法；遞迴 vs 堆疊
  - **常見失敗模式**
    - 忘記 visited（無限迴圈）
    - topo：入度遞減錯誤；未檢查處理數量

- **偽簽章（API 表面）**
  - `graph_bfs(starts, neighbors, on_visit)`
  - `graph_dfs(starts, neighbors, on_enter, on_exit)`
  - `toposort(nodes, edges) -> order or fail`
  - 延伸點：多源初始化；父節點追蹤；連通塊計數

- **代表性題目**
  - [LeetCode 133](https://leetcode.com/problems/clone-graph/description/)
  - [LeetCode 200](https://leetcode.com/problems/number-of-islands/description/)
  - [LeetCode 207](https://leetcode.com/problems/course-schedule/description/)
  - [LeetCode 417](https://leetcode.com/problems/pacific-atlantic-water-flow/description/)

- **工作中會出現的地方**
  - 相依圖；排程；可達性/影響分析

---

## 8) 堆 / 選擇（HeapTopK + Quickselect）⛰️ ⭐
- **契約（標準）**
  - **輸入**：可迭代物；比較器/鍵；目標 `k`
  - **狀態**：大小為 `k` 的堆（用最小堆求 top-k 最大）；或 quickselect 的分割索引
  - **不變式**：堆含有目前最佳的 `k` 個候選；quickselect 分割把 pivot 放到正確位置
  - **推進規則**：堆：push/pop 維持大小 `k`；quickselect：分割縮小搜尋側
  - **複雜度旋鈕**：`k`；串流 vs 批次；穩定性需求
  - **常見失敗模式**
    - 堆極性用錯（min vs max）
    - quickselect pivot 選擇導致最壞情況

- **偽簽章（API 表面）**
  - `heap_top_k(stream, k, key=None) -> items`
  - `quickselect(arr, k, key=None, randomized=True) -> kth`
  - 延伸點：穩定輸出、串流更新、雙堆中位數

- **第 k 個元素**
  - 🧩 Quickselect / 分割：🔥 [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/)
    - Quickselect：隨機化下**期望** $O(n)$，**最壞** $O(n^2)$；空間迭代 $O(1)$（或遞迴 $O(\log n)$）。
    - 每一步保證可丟棄分割後的一側，因為 pivot 已放在最終排名位置。
  - 堆替代方案（尤其串流 / 穩定性）：⭐ [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/)
    - 堆：時間 $O(n \log k)$；空間 $O(k)$。
    - 每一步保證堆以外的元素可被丟棄，因為它們在目前堆最小值之下，不可能進入 top-k。

- **什麼時候選哪個…**
  - **Quickselect**：批次陣列、原地、期望線性；可接受最壞情況風險。
  - **堆**：串流資料或需要增量更新；正確性較直觀；可預期 $O(n \log k)$。

- **工作中會出現的地方**
  - top-N 儀表板；百分位近似（小資料可算精確第 k）；優先權排程佇列

---

## 9) 合併已排序序列（MergeSortedSequences + KWayMerge）🔗 ⭐
- **契約（標準）**
  - **輸入**：已排序序列/迭代器；比較器/鍵；輸出模式（串流 vs 具體化）
  - **狀態**：2-way 用兩個指標（`i`,`j`）；k-way 用 head 的堆；輸出緩衝
  - **不變式**：輸出前綴全域有序；下一個被選的項目是目前可用 head 的最小者
  - **推進規則**：推進被選 head 的指標/迭代器；消耗完全部項目即終止
  - **複雜度旋鈕**：`k`；穩定性需求；輸出記憶體
  - **常見失敗模式**
    - 輸出後忘記前進指標
    - 空串列 / null head 處理錯誤

- **偽簽章（API 表面）**
  - `merge_two(a, b, key=None) -> merged`
  - `kway_merge(iterators, key=None, stable=True, mode="stream|list")`
  - 延伸點：穩定 tie-breaking、惰性迭代、去重合併

- **兩個已排序串流（雙指標）**
  - 鏈結串列合併：⭐ [LeetCode 21](https://leetcode.com/problems/merge-two-sorted-lists/description/)
    - 每一步保證可輸出較小的 head 節點，因為該串列剩餘節點都 ≥ 它的 head。
  - 陣列合併（常從尾端）：⭐ [LeetCode 88](https://leetcode.com/problems/merge-sorted-array/description/)
    - 每一步保證把目前最大值放到尾端是安全的，因為之後不需要再移動它。
  - 從尾端合併技巧：⭐ [LeetCode 977](https://leetcode.com/problems/distinct-subsequences-ii/description/)
    - 每一步保證可丟棄一端索引，因為已排序陣列的最大絕對值必在兩端。

- **k-way merge**
  - 堆版 $O(N \log k)$：🔥 [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/)
    - 每一步保證可輸出堆中的最小 head，因為它是所有串列 head 中最小的。
  - 分治 $O(N \log k)$：🔥 [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/)
    - 每次合併都保證排序性被保留，因為它是正確的 2-way merge 的組合。

- **什麼時候選哪個…（合併 k 串列）**
  - **堆**：串流式增量輸出；較好寫；穩定的增量合併。
  - **分治**：批次常數通常更好；沒有堆的額外負擔；配對遞迴/迭代清楚。

- **工作中會出現的地方**
  - 合併已排序事件串流；索引分段合併（LSM/IR 系統）；外部排序管線

---

## 10) 分割 / 原地壓縮（TwoPointerPartition）🚧 ⭐
- **契約（標準）**
  - **輸入**：可變更陣列；分類判定式（可多個）；期望的區段順序
  - **狀態**：區段指標（`low/mid/high` 或 `write/read`）；可選計數
  - **不變式**：陣列被切成具精確語意的標記區段
  - **推進規則**：每一步縮小未知區段；未知為空即終止
  - **複雜度旋鈕**：穩定 vs 不穩定；分割數量；交換成本
  - **常見失敗模式**
    - swap 後指標更新錯（尤其 `mid/high`）
    - 使用 swap 時誤以為是穩定的

- **偽簽章（API 表面）**
  - `writer_compact(arr, keep(x)) -> new_len`（穩定）
  - `partition_2way(arr, pred) -> boundary`
  - `dutch_flag(arr, classify={0,1,2})`
  - 延伸點：穩定性需求；k-way 推廣；原地 vs 額外緩衝

- **模式**
  - **荷蘭國旗（3-way 分割）**（`dutch_flag_partition`）
    - 偽簽章：`dutch_flag(A, values={0,1,2}) -> A`
    - 區段不變式：
      - `A[0..low-1] = 0`, `A[low..mid-1] = 1`, `A[mid..high] = unknown`, `A[high+1..n-1] = 2`
      - 迴圈：while `mid <= high`，每次 swap/update 後維持區段
    - Anchor：🔥 [LeetCode 75](https://leetcode.com/problems/sort-colors/description/)
  - **二分割**（`two_way_partition`）
    - ⭐ [LeetCode 905](https://leetcode.com/problems/length-of-longest-fibonacci-subsequence/description/)
    - ⭐ [LeetCode 922](https://leetcode.com/problems/possible-bipartition/description/)
  - **writer 壓縮（同向 read/write）**
    - 去重
      - ⭐ [LeetCode 26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/)
      - ⭐ [LeetCode 80](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/)
    - 移除元素
      - ⭐ [LeetCode 27](https://leetcode.com/problems/remove-element/description/)
    - 壓縮 / 穩定過濾
      - ⭐ [LeetCode 283](https://leetcode.com/problems/move-zeroes/description/)

- **工作中會出現的地方**
  - ETL 的壓縮；穩定過濾；分桶/路由分割

---

## 11) 快慢指標（FastSlowPointers）🐢🐇 ⭐
- **契約（標準）**
  - **輸入**：鏈結結構或定義 next 的函式 `f(x)`；head/start
  - **狀態**：`slow`, `fast` 指標
  - **不變式**：經過 `t` 次迭代，`slow` 走 `t` 步、`fast` 走 `2t`
  - **推進規則**：slow 前進 1、fast 前進 2；若有環必相遇；否則 fast 走到 null
  - **複雜度旋鈕**：步進函式成本；迴圈終止條件
  - **常見失敗模式**
    - `fast` / `fast.next` 的 null 檢查
    - phase-2 reset 邏輯混淆

- **兩階段（Floyd）**
  - Phase 1：偵測環
    - 正確性連結：`t` 次後 slow 走 `t`、fast 走 `2t`；若有環，相對速度 1 保證在環內相遇。
  - Phase 2：找環起點
    - 正確性連結：重設一個指標到 head，兩者都每次走 1 步；到入口的距離對環長度取模相等 ⇒ 在入口相遇。

- **題目**
  - 偵測環：⭐ [LeetCode 141](https://leetcode.com/problems/linked-list-cycle/description/)
  - 找環起點：⭐ [LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/description/)
  - 隱性環（函式迭代）：⭐ [LeetCode 202](https://leetcode.com/problems/happy-number/description/)
  - 中點：⭐ [LeetCode 876](https://leetcode.com/problems/hand-of-straights/description/)

- **工作中會出現的地方**
  - 偵測參照環；迭代函式系統；用環檢查做串流去重

---

## 12) 回溯探索（BacktrackingExploration）🧠 ⭐
- **契約（標準）**
  - **輸入**：選擇集合；限制條件；目標判定式；剪枝規則
  - **狀態**：目前路徑；輔助集合（used/cols/diags）；遞迴深度
  - **不變式**：狀態精準對應目前路徑（沒有「幽靈標記」）
  - **推進規則**：選一個選項、遞迴、取消選；由深度/選項耗盡而終止
  - **複雜度旋鈕**：分支因子；剪枝強度；輸出大小下界
  - **常見失敗模式**
    - 忘記取消選擇（狀態外洩）
    - 剪枝不足 / 去重跳過層級錯誤

- **偽簽章（API 表面）**
  - `backtrack(state, choices(state), choose, unchoose, is_solution, prune) -> outputs`
  - 延伸點：重複處理（排序 + 同層跳過）、memoization 快取鍵、迭代堆疊

- **核心節奏**：**選擇 → 探索 → 取消選擇**

- **決策樹形狀**
  - **排列**（used[]）
    - 時間：輸出所有排列為 `O(n * n!)`；堆疊 `O(n)`
    - ⭐ [LeetCode 46](https://leetcode.com/problems/permutations/description/)
    - 含重複（排序 + 同層跳過）：⭐ [LeetCode 47](https://leetcode.com/problems/permutations-ii/description/)
  - **子集合**（start index）
    - 時間：`O(n * 2^n)`；堆疊 `O(n)`
    - ⭐ [LeetCode 78](https://leetcode.com/problems/subsets/description/)
    - 含重複（排序 + 同層跳過）：⭐ [LeetCode 90](https://leetcode.com/problems/subsets-ii/description/)
  - **組合 / 固定大小**（start index + 長度界限）
    - ⭐ [LeetCode 77](https://leetcode.com/problems/combinations/description/)
  - **目標和搜尋**
    - 可重用：⭐ [LeetCode 39](https://leetcode.com/problems/combination-sum/description/)
    - 不可重用 + 含重複：⭐ [LeetCode 40](https://leetcode.com/problems/combination-sum-ii/description/)
    - 固定數量 + 有界範圍：⭐ [LeetCode 216](https://leetcode.com/problems/combination-sum-iii/description/)
  - **限制滿足**
    - N-Queens：指數級但可強剪枝；以 `cols`, `diag1`, `diag2` 表示狀態
    - 🔥 [LeetCode 51](https://leetcode.com/problems/n-queens/description/)
    - ⭐ [LeetCode 52](https://leetcode.com/problems/n-queens-ii/description/)
  - **字串切分**
    - ⭐ [LeetCode 93](https://leetcode.com/problems/restore-ip-addresses/description/)(4 段 + 長度界限剪枝)*
    - ⭐ [LeetCode 131](https://leetcode.com/problems/palindrome-partitioning/description/)(可選：用 DP 預先計算回文判定)*
  - **格子路徑搜尋**
    - ⭐ [LeetCode 79](https://leetcode.com/problems/word-search/description/)(visited 標記/取消標記)*

- **什麼時候選哪個…**
  - 遞迴：最容易表達選/探/取消
  - 迭代堆疊：避免某些語言的遞迴深度限制 / 超深深度限制

- **工作中會出現的地方**
  - 限制求解器；產生設定組合；排程器中的剪枝搜尋

<!-- markmap: fold -->
## 13) 格子上的 BFS 波前（GridBFSMultiSource）🌊 ⭐
- **契約（標準）**
  - **輸入**：格子；鄰居函式（指定 4 鄰或 8 鄰）；多個來源
  - **狀態**：佇列；visited/狀態格子；剩餘目標；時間/層數計數器
  - **不變式**：佇列包含目前前緣；每個格子最多入佇列一次
  - **推進規則**：按層處理 BFS；推入合法鄰居；佇列空或目標達成即終止
  - **複雜度旋鈕**：鄰居度數（4 vs 8）；visited 表示；直接改格子 vs 額外 visited
  - **常見失敗模式**
    - 入佇列時沒標記 visited（重複入佇列）
    - 把層數計算和逐節點處理混在一起

- **核心概念**：把所有來源推入，逐層擴張（時間 = 層數）
- **模型**：格子是頂點；邊連到 4 鄰（或指定時為 8 鄰）。
- **複雜度**：最壞 $O(R \* C)$ 時間與 $O(R \* C)$ 空間（佇列 + visited/狀態）；每個格子最多入佇列一次。

- **Anchor**
  - 🔥 [LeetCode 994](https://leetcode.com/problems/prison-cells-after-n-days/description/)
    - 每一步保證在第 `t` 分鐘處理的格子不可能更早到達，因為 BFS 以非遞減距離層探索。
- **工程檢查清單**
  - 以所有來源初始化佇列
  - 計數新鮮/剩餘目標
  - 以層處理 BFS 來計算分鐘數

- **工作中會出現的地方**
  - 多源傳播（影響範圍）；到最近設施距離；地圖上的最短跳數

---

## 14) 單調堆疊（MonotonicStack）📚 🔥
- **契約（標準）**
  - **輸入**：陣列；定義單調性的比較器；查詢類型（下一個更大/更小）
  - **狀態**：維持單調性的索引堆疊
  - **不變式**：堆疊值單調；未解決的索引留在堆疊上
  - **推進規則**：每個索引最多 push 一次、pop 一次 ⇒ $O(n)$
  - **複雜度旋鈕**：嚴格 vs 非嚴格比較；方向（左/右）
  - **常見失敗模式**
    - 比較子用錯（>= vs >）導致重複 bug
    - 忘記存索引（需要距離）

- **偽簽章（API 表面）**
  - `mono_stack(arr, cmp, on_pop(pop_i, i), on_finish(i))`
  - 延伸點：下一個更大、上一個更小、span/面積計算

- **代表性題目**
  - [LeetCode 739](https://leetcode.com/problems/daily-temperatures/description/)
  - [LeetCode 853](https://leetcode.com/problems/most-profit-assigning-work/description/)
  - [LeetCode 84](https://leetcode.com/problems/largest-rectangle-in-histogram/description/)
  - [LeetCode 42](https://leetcode.com/problems/trapping-rain-water/description/)

- **工作中會出現的地方**
  - 到下一事件時間查詢；包絡線計算；以堆疊做單趟分析

---

## 15) 併查集連通性（UnionFindConnectivity）🧩 ⭐
- **契約（標準）**
  - **輸入**：元素；union 操作；連通性查詢
  - **狀態**：`parent[]`, `rank/size[]`
  - **不變式**：`find(x)` 回傳代表元；union 合併連通塊
  - **推進規則**：路徑壓縮 + 以 rank 合併 ⇒ 平均攤還近乎常數
  - **複雜度旋鈕**：union/find 次數；把 id 對應到索引
  - **常見失敗模式**
    - 不做路徑壓縮；rank 更新錯誤
    - 忘記初始化所有節點

- **偽簽章（API 表面）**
  - `find(x)`, `union(x,y)`, `connected(x,y)`
  - 延伸點：連通塊計數、以 size 合併、動態新增節點

- **代表性題目**
  - [LeetCode 323](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/description/)
  - [LeetCode 547](https://leetcode.com/problems/number-of-provinces/description/)
  - [LeetCode 684](https://leetcode.com/problems/redundant-connection/description/)
  - [LeetCode 721](https://leetcode.com/problems/accounts-merge/description/)

- **工作中會出現的地方**
  - 身分分群/合併；網路連通性；依關係做分群

---

## 16) 動態規劃（序列 / 區間）（DPSequence/DPInterval）🧠 🔥
- **契約（標準）**
  - **輸入**：序列/字串；遞推關係定義；base case
  - **狀態**：`dp[i]` 或 `dp[i][j]`；轉移規則
  - **不變式**：dp 狀態代表某個前綴/區間的最佳值/方法數
  - **推進規則**：依相依關係的拓樸順序填表
  - **複雜度旋鈕**：狀態維度；轉移成本；記憶體最佳化
  - **常見失敗模式**
    - 相依順序錯誤；漏 base case
    - 混淆「方法數」與「最小成本」語意

- **偽簽章（API 表面）**
  - `dp_sequence(n, transition(i, dp)->dp[i])`
  - `dp_interval(n, transition(l,r,dp)->dp[l][r])`
  - 延伸點：重建路徑；滾動陣列；memoization

- **代表性題目**
  - [LeetCode 70](https://leetcode.com/problems/climbing-stairs/description/)
  - [LeetCode 198](https://leetcode.com/problems/house-robber/description/)
  - [LeetCode 300](https://leetcode.com/problems/longest-increasing-subsequence/description/)
  - [LeetCode 322](https://leetcode.com/problems/coin-change/description/)
  - [LeetCode 1143](https://leetcode.com/problems/find-smallest-common-element-in-all-rows/description/)
  - [LeetCode 416](https://leetcode.com/problems/partition-equal-subset-sum/description/)

- **工作中會出現的地方**
  - 限制下最佳化；對齊/diff 類任務；有重疊子問題的規劃

---

## 17) Trie / 前綴搜尋（TriePrefixSearch）🔤 ⭐
- **契約（標準）**
  - **輸入**：字串；字母表；插入/查找/前綴操作；可選：單字搜尋的棋盤鄰居
  - **狀態**：trie 節點及其 children 對應表/陣列；終止標記
  - **不變式**：從 root 的路徑拼出前綴；terminal 表示完整單字
  - **推進規則**：逐字元走訪；需要時建立節點
  - **複雜度旋鈕**：字母表大小；記憶體；節點壓縮
  - **常見失敗模式**
    - 忘記 terminal flag
    - 字母表小且固定時仍用 hashmap children（常數因子大）

- **偽簽章（API 表面）**
  - `insert(word)`, `search(word)`, `starts_with(prefix)`
  - 延伸點：單字計數、刪除、萬用字元、壓縮 trie

- **代表性題目**
  - [LeetCode 208](https://leetcode.com/problems/implement-trie-prefix-tree/description/)(Prefix Tree)
  - [LeetCode 212](https://leetcode.com/problems/word-search-ii/description/)

- **工作中會出現的地方**
  - 自動完成；以前綴路由；剖析器的字典比對

---

## 18) 鏈結串列操作（指標手術）🔧 ⭐
- **契約（標準）**
  - **輸入**：鏈結串列 head；分組大小 / 算術規則
  - **狀態**：`prev/curr/next` 指標；dummy head；進位（算術）
  - **不變式**：指標維持串列連結性；反轉片段皆已完整接回
  - **推進規則**：沿節點前進；反轉/連接片段；到尾端終止
  - **複雜度旋鈕**：遞迴 vs 迭代；額外 dummy 節點
  - **常見失敗模式**
    - 遺失 next 指標（斷鏈）
    - 分段邊界重接錯誤

- **偽簽章（API 表面）**
  - `reverse_segment(head, k) -> (new_head, new_tail, next_start)`
  - 延伸點：反轉指定區間；整串反轉；分組反轉

- 串列上的算術
  - ⭐ [LeetCode 2](https://leetcode.com/problems/add-two-numbers/description/)
- 分組原地反轉
  - 🔥 [LeetCode 25](https://leetcode.com/problems/reverse-nodes-in-k-group/description/)
    - 註：目標 $O(n)$；`prev_tail`, `new_head`, `new_tail`, `next_start` 的重接要小心。

- **工作中會出現的地方**
  - 指標安全的串列轉換；串流緩衝（鏈結結構）；原地分塊操作

---

## 建議學習路徑（roadmap-style）🚀
- **滑動視窗精通**
  - [ ] 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/)
  - [ ] 🔥 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/)
  - [ ] 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/)
  - [ ] ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/)
  - [ ] ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/)
  - [ ] 🔥 [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/)
- **雙指標精通**
  - [ ] 🔥 [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/)
  - [ ] ⭐ [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/)
  - [ ] ⭐ [LeetCode 26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/)
  - [ ] 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/)
- **回溯精通**
  - [ ] ⭐ [LeetCode 78](https://leetcode.com/problems/subsets/description/)
  - [ ] ⭐ [LeetCode 46](https://leetcode.com/problems/permutations/description/)
  - [ ] ⭐ [LeetCode 39](https://leetcode.com/problems/combination-sum/description/)
  - [ ] 🔥 [LeetCode 51](https://leetcode.com/problems/n-queens/description/)
  - [ ] ⭐ [LeetCode 79](https://leetcode.com/problems/word-search/description/)

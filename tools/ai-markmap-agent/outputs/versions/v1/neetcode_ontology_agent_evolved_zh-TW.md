---
title: LeetCode 知識圖譜心智圖（核心模式 → Kernel → 題目）
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 如何使用這張地圖（自由發揮、面試導向）
- **圖例**：🔥 必會 · ⭐ 常見 · 🧪 加分
- **Kernel 改裝（5 步）**
  1) 辨識 kernel
  2) 寫出前置/後置條件
  3) 定義狀態操作
  4) 定義修復規則
  5) 寫 3 個斷言/測試
- **經驗法則**：挑一個 *pattern* → 學它的 *不變量 (Invariant)* → 練 2–5 題 *problems* → 泛化成 *kernel 範本*
- [ ] 每個 kernel 先做 1 題 easy + 2 題 medium 再往下
- [ ] 每題做完寫下：`state`, `invariant`, `when to shrink/expand`, `time/space`
- **限制條件啟發式**
  - `n ≤ 2e5` → 目標 $O(n)$ / $O(n \log n)$
  - `n ≤ 2e3` → $O(n^2)$ 可能可接受
  - `n ≤ 200` → 指數級 + 剪枝 / 動態規劃 (Dynamic Programming) 通常可行
- **停止條件**
  - 能從記憶中實作 kernel 範本
  - 能解釋不變量 + 正確性（為何可行）
  - 不偷看也能處理 2 個延伸題

## 🧠 API Kernels（可重用的「引擎」）
<!-- markmap: fold -->
- **HashMapCounting** — *頻率對照表模式*
  - Mini-spec
    - Inputs: 序列 / key 的多重集合
    - State: `freq: key -> count`
    - Invariants: 計數符合目前範圍；永不為負
    - Advance rule: 更新 `freq[x] += 1`
    - Repair rule: 若要維持限制（例如唯一），就遞減直到合法
    - Termination: 掃描結束 / 範圍結束
    - Return value: 計數 / 衍生指標
    - Complexity envelope: $O(n)$ 期望時間的雜湊操作
    - Common failure modes: 忘記刪除 count=0 的 key；範圍邊界 off-by-one
- **PrefixSumRangeQuery** — *前綴和 + 雜湊對照表用於子陣列查詢*
  - Mini-spec
    - Inputs: 陣列 (Array) `nums`
    - State: 執行中的 `prefix`、以及計數或最早索引的 `map`
    - Invariants: `prefix[i] = sum(nums[:i])`；map 反映至今看過的 prefix
    - Advance rule: 更新 `prefix += nums[i]`；查詢/更新 map
    - Termination: 完成掃描
    - Return value: 計數 / 最長長度 / 是否存在
    - Complexity envelope: $O(n)$ 期望時間雜湊操作；在對抗性雜湊下最壞情況可能退化
    - Common failure modes: 初始化錯誤（計數時 `map[0]=1`）；混用最早 vs 最晚索引
- **SubstringSlidingWindow** — *具動態不變量的一維視窗狀態機*
  - Mini-spec
    - Inputs: 序列 `s`、視窗上的 predicate/invariant
    - State: `L, R`，加上 `hash_map/counter`，有時還有 `sum`
    - Invariants: 視窗 `[L..R]` 當且僅當 predicate 成立時合法；`R` 單調遞增
    - Advance rule: 延伸 `R`，更新狀態
    - Shrink/repair rule: 當不合法時，遞增 `L` 並回復狀態
    - Termination: `R` 到達尾端
    - Return value: 最大/最小長度、是否存在、視窗端點
    - Complexity envelope: `R` 從 `0..n-1` 單調遞增；`L` 也單調遞增且不會超過 `n`；整次執行中 `L` 的總遞增次數 ≤ `n` ⇒ 若狀態更新平均為 $O(1)$，總工作量 $O(n)$
    - Common failure modes: predicate 非單調卻硬用滑動視窗；在最小化模式忘記更新答案
  - Notes
    - 時間假設雜湊操作為 $O(1)$ 期望時間；在對抗性雜湊下最壞情況可能退化
- **GridBFSMultiSource** — *多來源的波前 BFS*
  - Mini-spec
    - Inputs: 格子/圖、來源清單、鄰居函式
    - State: 佇列 (Queue)、visited/dist、time/levels
    - Invariants: 佇列保存目前前沿（等距離）；第一次走訪到即為最短距離
    - Advance rule: 彈出前沿，加入未走訪鄰居
    - Termination: 佇列為空或達成目標條件
    - Return value: 最短時間 / 距離格子 / 可達性
    - Complexity envelope: $O(V+E)$（格子：$O(R \cdot C)$）
    - Common failure modes: 層級/時間與步數混用；沒用 visited 防護就重複入佇列
- **DFSGraphGeneric** — *在鄰接串列圖（非格子）上做 DFS*
  - Mini-spec
    - Inputs: 鄰接串列 `g`
    - State: 遞迴 (Recursion)/堆疊 (Stack)、`visited`、可選 `parent/onpath`
    - Invariants: visited 防止重複處理；onpath 支援有向圖的環偵測
    - Advance rule: 探索鄰居
    - Termination: 所有可達節點處理完
    - Return value: 連通成分、拓樸可行性、走訪順序
    - Complexity envelope: $O(V+E)$
    - Common failure modes: 沒區分無向圖的 parent 邊；遞迴深度限制
- **TreeTraversalDFS / TreeTraversalBFS** — *樹的走訪*
  - Mini-spec
    - Inputs: `root`
    - State: 遞迴/堆疊（DFS）或佇列（BFS）
    - Invariants: DFS 遵守所選順序；BFS 逐層處理
    - Termination: null 節點被處理/跳過
    - Return value: 彙總值 / 路徑結果 / 每層陣列
    - Complexity envelope: 時間 $O(n)$；堆疊 $O(h)$（DFS）或佇列 $O(w)$（BFS）
    - Common failure modes: 將路徑累積與子樹彙總混在一起
- **BinarySearchBoundary** — *在已排序陣列中的索引空間找邊界*
  - Mini-spec
    - Inputs: 已排序陣列 `a`、對索引 `i` 的單調 predicate
    - State: `lo, hi`
    - Invariants: 邊界落在 `[lo, hi]`
    - Advance rule: 用中點測試縮小區間
    - Termination: `lo == hi`（或依變形為 `lo > hi`）
    - Return value: 邊界索引（第一個/最後一個 true 等）
    - Complexity envelope: $O(\log n)$
    - Common failure modes: mid 算錯造成無窮迴圈；回傳錯邊
- **BinarySearchOnAnswer** — *在值域上做可行性判定*
  - Mini-spec
    - Inputs: 答案範圍 `[lo..hi]`、單調的 `feasible(x)`
    - State: `lo, hi`
    - Invariants: 若在最小化：可行區間是後綴/前綴單調；答案在界內
    - Advance rule: 測試 `mid`，依可行性縮小
    - Termination: `lo == hi`
    - Return value: 最小/最大可行答案
    - Complexity envelope: $O(\log range \cdot T(feasible))$
    - Common failure modes: feasible 不單調；界限初始化錯
- **HeapTopK** — *top-k / 第 k 大/小 / 串流中位數*
  - Mini-spec
    - Inputs: 串流 / 陣列
    - State: 堆積 (Heap)（可能多個）、大小限制 `k`
    - Invariants: heap 包含目前最佳候選；size ≤ k
    - Advance rule: push/pop 以恢復 size 不變量
    - Termination: 串流結束
    - Return value: 第 k、top-k 清單、中位數
    - Complexity envelope: $O(n \log k)$
    - Common failure modes: heap 方向用錯；size 超過 k 忘記 pop
- **MonotonicStack** — *下一個更大/更小、直方圖*
  - Mini-spec
    - Inputs: 陣列
    - State: 索引的堆疊
    - Invariants: 堆疊對應值保持單調（遞增/遞減視題目）
    - Advance rule: 當不變量被破壞，pop 並結算被 pop 索引的答案
    - Termination: 完整掃描；可選用 sentinel 做 flush
    - Return value: 下一個更大/更小索引、最大面積
    - Complexity envelope: $O(n)$（每個索引 push/pop ≤ 1 次）
    - Common failure modes: 存值而非索引；嚴格 vs 非嚴格比較用錯
- **TwoPointersTraversal** — *在維持不變量下使用兩個索引*
  - Mini-spec
    - Inputs: 陣列/字串；有時需要已排序輸入
    - State: 兩個指標 (`l,r` 或 `read,write`)
    - Invariants: 搜尋空間或保留前綴滿足性質
    - Advance rule: 依規則移動一個指標
    - Termination: 指標交錯 / 掃描結束
    - Return value: bool / 長度 / 被修改後的陣列前綴
    - Complexity envelope: $O(n)$
    - Common failure modes: 跳過重複值時破壞不變量；移動指標前忘記更新答案
- **TwoPointerPartition** — *分割（荷蘭國旗、quickselect partition）*
  - Mini-spec
    - Inputs: 陣列；pivot/分割規則
    - State: 區域指標，界定各分割區
    - Invariants: 區域滿足 `< pivot`, `== pivot`, `> pivot`（或兩區）
    - Advance rule: swap/移動指標以擴張正確區域
    - Termination: 掃描指標越過邊界
    - Return value: 已分割陣列 / pivot 最終索引 / 第 k
    - Complexity envelope: 每次分割掃描 $O(n)$
    - Common failure modes: 區域邊界錯；swap 後未前進
- **FastSlowPointers**
  - **FloydCycleDetection** — *環是否存在 + 在函數式圖上找環起點*
  - **RunnerMidpoint** — *在鏈結串列上找中點 / 倒數第 k 個的風格*
- **MergeSortedSequences** — *合併兩個已排序序列*
  - Mini-spec
    - Inputs: 兩個已排序序列
    - State: `i,j`（輸出時再加 `k`）
    - Invariants: 輸出前綴已排序，且等於目前已取用元素中的最小集合
    - Advance rule: 取較小的 head，前進對應指標
    - Termination: 其中一個序列耗盡，接上剩餘部分
    - Return value: 合併後序列或原地合併陣列
    - Complexity envelope: $O(m+n)$
    - Common failure modes: 比較器錯；尾端處理不完整
- **KWayMerge** — *合併 K 個已排序序列（堆積或分治法 (Divide and Conquer)）*
  - Mini-spec
    - Inputs: K 個已排序序列的清單
    - State: 目前 head 的 heap，或成對合併的遞迴
    - Invariants: heap top 是剩餘 head 的最小值
    - Advance rule: pop 最小值，push 該序列的下一個
    - Termination: heap 空 / 所有序列取用完
    - Return value: 合併後的排序輸出
    - Complexity envelope: $O(N \log K)$
    - Common failure modes: push null；tie 處理不正確
- **UnionFindConnectivity** — *連通成分 / 環偵測*
- **TopologicalSort** — *DAG 排序*
- **TriePrefixSearch** — *前綴比對*
- **DP1D/2D basic (knapsack-ish, LIS-ish, grid DP)**
- **Interval DP (advanced)**

### 常見 kernel 組合
- `BinarySearchOnAnswer` + `PrefixSumRangeQuery`（對長度/值做二分搜尋 + 快速區間檢查）
- `TriePrefixSearch` + `BacktrackingExploration`（單字搜尋 / 自動完成）
- `HeapTopK` + `KWayMerge`（串流合併 + 維持 top-k）

---

## 🪟 Sliding Window Family: `substring_window`（Kernel: SubstringSlidingWindow） 🎯
### Kernel mini-spec（標準）
- Inputs: `s`（string/array），視窗上的 constraint/predicate
- State: `L, R`，加上 `freq` / counters / `sum`
- Invariants: 視窗 `[L..R]` 當且僅當 predicate 成立時合法；`L` 與 `R` 單調遞增
- Advance rule: `R` 向右移 1，更新狀態
- Shrink/repair rule: 當不合法（或在最小化時仍合法），`L` 向右移 1 並更新狀態
- Termination: `R == n`
- Return value: 最佳視窗端點 / 長度 / 布林值
- Complexity envelope: 期望時間 $O(n)$；依賴單調指標 + 平均 $O(1)$ 狀態更新
- Common failure modes: 用在非單調 predicate（負數等）；忘記在正確時機更新答案

### 確定性選擇器（何時使用此 kernel）
- 需要 **連續** 子陣列/子字串？→ 若否，這就不是滑動視窗
- 固定長度 `k`？→ 用 **固定大小** 視窗模式
- predicate 對 `R` 擴張具有單調性？→ 用可變視窗 + 不合法就收縮
- 需要滿足 predicate 的 **最小** 視窗？→ 用最小化模式（合法就持續收縮）

### ==以不變量為先的思考==
- 視窗 `[L..R]` 合法當且僅當 **不變量成立**
- 兩種模式：
  - **最大化**：擴張 `R`，不合法就收縮
  - **最小化**：擴張直到合法，仍合法就收縮

### 3-step 梯子（循序漸進）
- 1) **Unique**（局部重複）→ 加 `freq` + `while freq[x]>1` 修復
- 2) **At most K distinct** → 加 `distinct` 計數器 + `while distinct>K` 修復
- 3) **Min cover / fixed anagram match** → 加 `need/have` + 用最小化迴圈或固定大小相等檢查

### Pattern 比較（小抄表）
| Pattern | Invariant | State | Window | Typical goal | Repair rule | Practice |
|---|---|---|---|---|---|---|
| sliding_window_unique | 全都唯一 | last index / freq | variable | maximize | `while freq[s[R]]>1: remove(s[L])` | 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) |
| sliding_window_at_most_k_distinct | ≤ K distinct | freq map + `distinct` | variable | maximize | `while distinct>K: remove(s[L])` | ⭐ [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) |
| sliding_window_min_cover | 涵蓋所需 freq | need/have maps + `formed` | variable | minimize | `while formed==required: try minimize; remove(s[L])` | 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) |
| sliding_window_fixed_anagram_match | freq 等於目標 | freq diff / matches | fixed | exists / all | `if R-L+1>k: remove(s[L]); if R-L+1==k: check()` | ⭐ [LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py), ⭐ [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) |
| sliding_window_cost_bounded | sum/cost 限制 | integer sum | variable | minimize | `while sum>target: sum-=nums[L]; L+=1` | ⭐ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) |
| sliding_window_fixed_size | 固定長度 `k` | rolling state | fixed | aggregate/stat | `if R-L+1==k: update ans; slide L++` | *(範本模式；此子集合未綁定題目)* |

### 核心題（真實來源：上表）
- 使用小抄表中的 **Practice** 欄。

### 邊界規則（Sliding Window vs Prefix Sum）
- predicate 對視窗成長具單調性時用滑動視窗（常見於非負 cost）。
- 需要任意和 / 有負數 / 精確計數時用前綴和。

---

## 👉 Two Pointers Family（Kernel: TwoPointersTraversal） ⚡
### Kernel mini-spec（標準）
- Inputs: 陣列/字串；有時需要已排序輸入
- State: 指標 `(l,r)` 或 `(read,write)`，可選不變量（保留前綴、剩餘搜尋空間）
- Invariants: 答案/搜尋空間在指標界定區域內；或 `arr[:write]` 是「保留/乾淨」的
- Advance rule: 依局部比較 / writer 規則移動一個指標
- Termination: 指標交錯或掃描結束
- Return value: 布林值 / 最大指標 / 修改後前綴長度
- Complexity envelope: 通常 $O(n)$
- Common failure modes: 忘記排序前置條件；跳過重複值錯誤；更新答案時 off-by-one

### Pattern 比較
| 子模式 | 指標初始化 | Invariant | Time | Practice |
|---|---|---|---|---|
| Opposite pointers | `l=0, r=n-1` | 答案落在 `[l,r]` | $O(n)$ | 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py), ⭐ [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py), ⭐ [LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py), 🔥 [LeetCode 167 - Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/) |
| Same-direction writer | `write=0`, `read` scans | `arr[:write]` 是「保留/乾淨」的 | $O(n)$ | 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py), ⭐ [LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py), ⭐ [LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py), ⭐ [LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) |
| Dedup enumeration（k-sum 核心） | sort + 固定 `i` + `(l,r)` | **前置條件**：輸入已排序。**唯一性合約**：以確定性方式跳過重複，確保每個 tuple 只輸出一次。 | $O(n^2)$ | 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py), ⭐ [LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py), [LeetCode 18 - 4Sum](https://leetcode.com/problems/4sum/description/) |
| Merge（2 sorted） | `i,j` forward | 輸出為排序前綴 | $O(m+n)$ | *(見 `🔗 Merge Sorted Family` → `MergeSortedSequences` kernel)* |

### 選擇準則：sliding window vs two pointers
- Sliding window：連續範圍 + 維護 *視窗狀態* 來收縮/擴張。
- Two pointers：可依局部比較 *確定性地丟棄一側*（或原地壓縮）。
- 排序陣列上的 two pointers：配對搜尋 / 去重逐一產生依賴排序不變量。
- 若決策依賴 mid/全域 predicate → 優先二分搜尋（boundary/answer）。
- 若陣列是環狀，指標常用 `i = (i+1) % n`（模索引）；用計步確保終止。

### Opposite pointers（搜尋 / 最大化 / 回文）
- **two_pointer_opposite_maximize**
  - [ ] 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ] ⭐ [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - [ ] ⭐ [LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
- **two_pointer_opposite_search（sorted pair search）**
  - [ ] 🔥 [LeetCode 167 - Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/) *(典型「排序配對搜尋」)*

### Same-direction writer（原地修改陣列）
- **two_pointer_writer_dedup**
  - [ ] 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [ ] ⭐ [LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
- **two_pointer_writer_remove/compact**
  - [ ] ⭐ [LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - [ ] ⭐ [LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)

### Multi-sum enumeration（sort + two pointers）
- **two_pointer_three_sum**
  - [ ] 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
  - [ ] ⭐ [LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - [ ] [LeetCode 18 - 4Sum](https://leetcode.com/problems/4sum/description/) *(相關；若在你的完整題庫中)*

---

## 🐢🐇 Fast–Slow Pointers（Kernels: FloydCycleDetection, RunnerMidpoint） 🔥
### FloydCycleDetection：兩階段心智模型
- Phase 1：在 **函數式圖**（每個節點出度 ≤ 1）偵測是否有環（tortoise/hare 相遇）
- Phase 2：找出環的起點（將其中一個指標重設回 head）
  - 設 μ = head→環起點距離、λ = 環長。相遇時把一個指標移回 head，兩者之後都每次前進 1，會在 μ 步後於環起點相遇。

### RunnerMidpoint：心智模型
- `slow` 每次走 1、`fast` 每次走 2 → 當 `fast` 到尾端，`slow` 在中點（或依慣例取下中/上中）

### 練習梯子
- [ ] 🔥 [LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py) *(環偵測)*
- [ ] 🔥 [LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py) *(環起點)*
- [ ] ⭐ [LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py) *(隱含環)*
- [ ] ⭐ [LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py) *(中點)*

---

## 🧩 回溯法 (Backtracking)（Kernel: BacktrackingExploration） 📚
### Kernel mini-spec（標準）
- Inputs: 選擇/候選、限制條件、目標條件
- State: `path`、`used[]` / `start_index`，以及限制追蹤器
- Invariants: **狀態一致性** — 從遞迴返回後，狀態必須被完整還原
- Advance rule: `choose(option)` 後遞迴
- Repair/prune rule: 提早做 `prune(state)`
- Termination: `is_goal(state)` 或沒有候選
- Return value: 所有解 / 計數 / 最佳解
- Complexity envelope: 通常為指數級；取決於分支數 + 深度
- Common failure modes: 忘記 unchoose；在分支間共用可變狀態導致別名問題
- Aux space: 遞迴深度 $O(depth)$ + 狀態結構（`used[]`, `path`）

### 標準簽名（可插拔引擎）
- `candidates(state)`
- `choose(option)`
- `unchoose(option)`
- `is_goal(state)`
- `prune(state)`

### 5 種決策樹形狀（選對「狀態把手」）
- **Permutation** → `used[]`
  - [ ] 🔥 [LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
  - [ ] ⭐ [LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py) *(去重：排序 + 同層跳過，透過 `used[i-1]==False`)*
- **Subset** → `start_index`
  - [ ] 🔥 [LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
  - [ ] ⭐ [LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py) *(去重：排序 + 同層跳過 `i>start && nums[i]==nums[i-1]`)*
- **Combination / fixed size** → `start_index` + `len(path)==k`
  - [ ] ⭐ [LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py) *(排序後提早 break)*
  - [ ] 🔥 [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) *(允許重用：用 `i` 遞迴)*
  - [ ] ⭐ [LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py) *(不可重用：用 `i+1` 遞迴 + 去重)*
  - [ ] ⭐ [LeetCode 216 - Combination Sum III](https://leetcode.com/problems/combination-sum-iii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py) *(固定數量 + 有界範圍)*
- **Constraint satisfaction / placement**
  - [ ] 🔥 [LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - [ ] ⭐ [LeetCode 52 - N-Queens II](https://leetcode.com/problems/n-queens-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
  - [ ] ⭐ [LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)
  - [ ] ⭐ [LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
  - [ ] ⭐ [LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

### 回溯法「工具帶」
- **剪枝**
  - 可行性界限（剩餘選擇不夠）
  - target 界限（`remaining < 0`）
  - 排序後提早退出（`candidates[i] > remaining → break`）
- **去重策略**
  - 排序 + 同層跳過（subset/combination）
  - 排序 + 基於 `used` 的跳過（permutation）
- 若子問題以相同參數重複出現 → 加 memo（top-down DP）。

---

## 🌊 圖的波前 BFS（Kernel: GridBFSMultiSource） 🎯
### Kernel mini-spec（標準）
- Inputs: 格子、來源、鄰居函式
- State: `queue`、`visited/dist`、`time/levels`
- Invariants: 佇列儲存等距離（層級）的目前前沿；第一次走訪到即最短
- Advance rule: 彈出一個格子；加入合法且未走訪的鄰居；逐層處理時遞增 `time`
- Termination: 佇列為空（或所有目標處理完）
- Return value: 最短時間、距離格子、可達性遮罩
- Complexity envelope: 時間 $O(R \cdot C)$、空間 $O(R \cdot C)$
- Common failure modes: time 的 off-by-one；忘記多來源初始化

### 領域 → 圖 檢查表
- 辨識 **節點**（格子/狀態）、**邊**（合法移動）、**來源**，以及「一分鐘/一步」代表什麼（一次 BFS 層級）。

### 真實世界類比
- cache warm-up / invalidation wavefront
- 在網路上的感染/告警擴散
- rollout 半徑 / TTL 以 hop 擴張

### grid_bfs_propagation
- 多來源 BFS = 先把所有來源入佇列，再逐層擴張

### Practice
- [ ] 🔥 [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

## 🔗 Merge Sorted Family
### Merge 2 sorted（Kernel: MergeSortedSequences）
- [ ] 🔥 [LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
- [ ] ⭐ [LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
- [ ] ⭐ [LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

### Merge K sorted（Kernel: KWayMerge）
- **merge_k_sorted_heap**: $O(N \log K)$
- **merge_k_sorted_divide**: $O(N \log K)$
- 兩種實作：基於 heap 或分治法的成對合併
- [ ] 🔥 [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - [ ] ⭐ [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

## 🎛️ 分割與選擇（Kernel: TwoPointerPartition / HeapTopK）
### Partitioning
- **two_way_partition**
  - [ ] ⭐ [LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
  - [ ] ⭐ [LeetCode 922 - Sort Array By Parity II](https://leetcode.com/problems/sort-array-by-parity-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
- **dutch_flag_partition**
  - [ ] 🔥 [LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
- **quickselect_partition**
  - [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)

### 用 heap 做 kth/top-k 的替代方案（Kernel: HeapTopK）
- **heap_kth_element**
  - [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) *(比較：quickselect 平均 $O(n)$ vs heap $O(n\log k)$)*

### 選擇器（heap vs partition）
- 需要串流 / 線上處理 → heap
- 需要原地、平均線性、單次查詢 → quickselect
- 需要最壞情況保證 → heap（或註記 introselect）

---

## 📚 Monotonic Stack Family（Kernel: MonotonicStack）
### Kernel mini-spec（標準）
- Inputs: 陣列 `a`
- State: 索引的堆疊
- Invariants: 堆疊索引代表值的單調序列（遞增或遞減）
- Advance rule: 對每個 `i`，當不變量被破壞時 pop `j`，並完成 `j` 的答案
- Termination: 掃描完成；可選 push sentinel 以 flush
- Return value: 下一個更大/更小陣列，或最大面積/寬度
- Complexity envelope: 時間 $O(n)$；堆疊 $O(n)$
- Common failure modes: 嚴格性錯（`<` vs `<=`）、忘記 sentinel/flush、存值不存索引

### 子模式
- **next_greater_element / next_smaller_element**
- **histogram_max_rectangle**

### Practice（代表性）
- *(此子集合未綁定自動連結題目；可自行加入常用的單調堆疊題單)*

---

## 🧮 Prefix Sum + Hash Map Family（Kernel: PrefixSumRangeQuery）
### Kernel mini-spec（標準）
- Inputs: `nums`
- State: `prefix`、以及計數或最早索引的 `map`
- Invariants: map 反映目前索引之前的 prefixes；`prefix` 為執行中的總和
- Advance rule: 更新 `prefix`，在 map 中查詢需要的先前 prefix，再更新 map
- Termination: 陣列結尾
- Return value: 計數 / 最長長度 / 是否存在
- Complexity envelope: $O(n)$ 期望時間雜湊操作
- Common failure modes: 忘記 `map[0]` 起始；在查詢前就先更新 map

### 範本（兩種常見模式）
- running prefix: `prefix += nums[i]`
- map:
  - counting: `count[prefix] += 1`
  - longest: 存最早索引 `first_idx[prefix]`
- 何時勝過 sliding window：存在負數；需要精確和/計數；predicate 非單調

### 子模式
- **prefix_sum_hash_count**（子陣列和等於 k）
- **prefix_sum_hash_longest**（具性質的最長子陣列）

---

## 🔎 Binary Search Family（Kernels: BinarySearchBoundary, BinarySearchOnAnswer）
### 5 行範本（先找最小可行）
```python
lo, hi = ...
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid): hi = mid
    else: lo = mid + 1
return lo
```

### 規則邊界（two pointers vs binary search）
- 若能依局部比較確定性地丟棄一側 → 雙指標 (Two Pointers)。
- 若決策依賴 mid/全域 predicate（feasible/threshold）→ 二分搜尋。

---

## 🧭 Roadmap Anchors（來自你的圖）
- **NeetCode 150**：🔥 [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 2, 3, 4, 11, 15, 21, 23, 25, 26, 27, 39, 40, 46, 51, 75, 76, 78, 79, 80, 88, 90, 125, 131, 141, 142, 202, 209, 215, 283, 438, 567, 680, 876, 905, 922, 977, 994
- **Blind 75**（此處包含的子集合）：🔥 [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 3, 11, 15, 21, 23, 26, 39, 75, 76, 79, 125, 141, 142, 215, 994
- 關於 **[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)** 的註記：典型 kernel 是 **HashLookupComplement**（雜湊式）。雙指標只在排序後才適用，且會改變輸出限制。
- **這張地圖尚未涵蓋的高頻模式**：單調堆疊（已新增章節但未綁題）、前綴和 + 雜湊（已新增章節）、二分搜尋邊界/答案（已新增範本）、拓樸排序、並查集、Trie、DP 基礎。

---

## ✅ 快速「下一組 10 題」播放清單（均衡）
- [ ] 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- [ ] 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
- [ ] 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [ ] 🔥 [LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
- [ ] 🔥 [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
- [ ] 🔥 [LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
- [ ] 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
- [ ] 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- [ ] 🔥 [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
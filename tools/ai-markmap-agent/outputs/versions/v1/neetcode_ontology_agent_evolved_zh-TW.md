---
title: LeetCode 知識圖譜心智圖（核心模式 → Kernels → 題目）
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 🎯 如何使用這張地圖（自由探索、面試導向）
- **經驗法則**：挑一個 *pattern* → 學它的 *不變量 (Invariant)* → 練 2–5 題 *problems* → 歸納成 *kernel template*
- [ ] 每個 kernel 先做 1 題 easy + 2 題 medium 再往下
- [ ] 每題做完都寫下：`state`, `invariant`, `when to shrink/expand`, `time/space`
- **圖例**：🔥 必懂 · ✅ 應該要懂 · 🧪 加分了解

### 決策指南（路由器）
- **陣列 (Array)/字串 (String) 掃描**
  - 需要「在限制條件下的最佳子陣列/子字串」→ `SubstringSlidingWindow`
  - 需要「有結構的 pair/tuple」→ `TwoPointersTraversal`（通常先排序）
  - 有**負數**且需要子陣列和/計數 → `PrefixSumRangeQuery`（+ hash map）
- **已排序 / 答案是邊界 / 單調性判定條件** → `BinarySearchBoundary`（含「在答案空間做二分搜尋」）
- **kth / top-k / 串流** → `HeapTopK`（線上）vs `TwoPointerPartition` / quickselect（離線、會變更內容）
- **無權重最短步數 / 傳播 /「分鐘」** → `MultiSourceBFSWavefront`
- **動態連通性**（連通分量、無向圖環）→ `UnionFindConnectivity`
- **窮舉 / 找一個 / 最佳化組合選擇** → `BacktrackingExploration`
- **下一個更大/更小 / 區間邊界** → `MonotonicStack`
- **DAG 排序 / 先修關係** → `TopologicalSort`

---

## 🧠 API Kernels（可重用的「引擎」）
<!-- markmap: fold -->
### Kernels（可呼叫的樣板）
- **HashMapIndexing** — *「最後出現 / 計數 / 補數」的 O(1) 平均查找*
  - Contract
    - Inputs：串流/陣列/字串項目；查詢如 `need = target - x`
    - State：`dict` 對應 key → index/value/count
    - Invariant：對應表精準反映已處理的 prefix
    - Progress rule：處理下一個項目，更新/查詢對應表
    - Termination：輸入結束，或找到符合就提早回傳
    - Complexities：平均 $O(n)$ 時間、$O(n)$ 空間
    - Common failure modes：覆寫順序 bug（應先 need 再 put）；重複值處理（Two Sum）；key 正規化（大小寫/非字母數字）
  - Dependencies：`dict` / `Counter`
  - Bug sources & readability：命名 `seen`, `count`；明確寫出更新順序；避免過早微最佳化
- **TwoPointersTraversal** — *兩個索引在維持不變量的規則下移動（搜尋/掃描/去重）*
  - Contract
    - Inputs：陣列/字串；常先排序以利消去論證
    - State：索引 `l,r` 或 `read,write`，加上可選累積器
    - Invariant：依子模式而定（搜尋消去、回文已驗證 prefix/suffix、writer 的 prefix 合法）
    - Progress rule：依比較/判定條件，單調地移動其中一個指標
    - Termination：指標交錯 / `read==n` / 找到匹配
    - Complexities：典型 $O(n)$；若含排序前置步驟則總計 $O(n\log n)$
    - Common failure modes：移動方向錯；跳過重複值錯；交錯時 off-by-one
  - Dependencies：排序（可選）、判定條件/比較
  - Bug sources & readability：統一 `l,r,read,write`；把「略過重複值」封裝成 helper；標註何時不適用（未排序/無法消去）
- **SubstringSlidingWindow** — *具動態不變量的一維視窗狀態機*
  - Contract
    - Inputs：字串/陣列；對視窗合法性的限制
    - State：`L,R`, `Counter/map`，有時 `sum`
    - Invariant：視窗合法性判定（依 pattern）
    - Progress rule：推進 `R`；當不合法時推進 `L` 並更新狀態
    - Termination：`R` 到達結尾
    - Complexities：攤還 $O(n)$：`L` 與 `R` 單調推進；總增量各 ≤ $n$
    - Common failure modes：縮小條件寫反；忘了遞減/移除；「記錄答案」時機錯；視窗長度 off-by-one
  - Dependencies：`Counter/map`；有時 `PrefixSumRangeQuery`, `MonotonicDeque`
  - Bug sources & readability：用 hooks `add/remove/is_invalid/record`；命名 `L,R`；確保 freq-cover 的重數邏輯正確
- **PrefixSumRangeQuery** — *前綴和 + hash map 的子陣列查詢*
  - Contract
    - Inputs：陣列；子陣列和/計數相關查詢
    - State：`prefix`, `freq_map[prefix_value]`
    - Invariant：`freq_map` 計數已處理 prefix 的前綴和
    - Progress rule：更新 `prefix += x`；查詢需要的先前前綴；再遞增 `freq_map[prefix]`
    - Termination：陣列結束
    - Complexities：平均 $O(n)$ 時間、$O(n)$ 空間
    - Common failure modes：忘記 `freq_map[0]=1`；更新順序（先計數再插入）；整數溢位（非 Python）
  - Dependencies：`dict` / `defaultdict(int)`
  - Bug sources & readability：定義 `prefix`；註解「先計數先前前綴，再加入目前值」
- **BinarySearchBoundary** — *第一個/最後一個成立，或在答案上二分搜尋*
  - Contract
    - Inputs：對索引或值空間的單調判定條件
    - State：`lo, hi, mid`
    - Invariant：維持搜尋空間，使邊界仍在其中
    - Progress rule：依 `predicate(mid)` 更新 `lo/hi`
    - Termination：`lo == hi`（或 `lo+1==hi` 變形）
    - Complexities：$O(\log n)$
    - Common failure modes：無限迴圈（mid 偏置）；含端點邊界的不變量錯；判定條件非單調
  - Dependencies：predicate function
  - Bug sources & readability：使用命名清楚的「first true / last true」樣板；有意識地選 `mid = (lo+hi)//2` 或 upper-mid
- **HeapTopK** — *top-k / kth（單一堆積）*
  - Contract
    - Inputs：可迭代/串流；需要 top-k 或第 k 大/小
    - State：大小 ≤ k 的 min-heap（或用取負號模擬 max-heap）
    - Invariant：堆積保留目前最佳的 k 個元素
    - Progress rule：push；若 size > k 則 pop
    - Termination：串流結束
    - Complexities：$O(n\log k)$ 時間、$O(k)$ 空間
    - Common failure modes：堆積方向弄錯；k=0 的邊界情況；忘記限制大小
  - Dependencies：heap/priority queue
  - Bug sources & readability：封裝 push-pop；命名 `min_heap`；若需要串流不要改用 quickselect
- **DualHeapMedian** — *以兩個堆積維持平衡不變量來求串流中位數*
  - Contract
    - Inputs：數字串流；每次插入後要中位數
    - State：`low`（max-heap）、`high`（min-heap）
    - Invariant：`len(low)` == `len(high)` 或 +1；且所有 `low` ≤ 所有 `high`
    - Progress rule：插入後重平衡並修正順序
    - Termination：串流結束 / 隨時可查詢
    - Complexities：每次插入 $O(\log n)$、$O(n)$ 空間
    - Common failure modes：重平衡順序錯；中位數定義（偶數個）
  - Dependencies：兩個堆積
  - Bug sources & readability：拆成 `add_num()` 與 `rebalance()`
- **MergeSortedSequences** — *合併兩個已排序序列*
  - Contract
    - Inputs：兩個已排序序列/迭代器
    - State：索引 `i,j`（或節點指標）、輸出緩衝
    - Invariant：輸出為已消耗前綴的排序合併結果
    - Progress rule：推進能提供下一個最小值的指標
    - Termination：其中一邊耗盡；附加剩餘部分
    - Complexities：$O(m+n)$ 時間；鏈結串列額外 $O(1)$ / 建新陣列為 $O(m+n)$
    - Common failure modes：忘記接尾端；對穩定排序的期待不一致
  - Dependencies：雙指標比較
  - Bug sources & readability：統一「取較小者再推進」helper
- **KWayMerge** — *合併 K 個已排序序列（堆積或分治法 (Divide and Conquer)）*
  - Contract
    - Inputs：已排序序列/串列的清單
    - State：目前頭節點的 min-heap（heap 作法）或遞迴堆疊（分治法）
    - Invariant：堆積包含每個仍有效串列的下一個候選
    - Progress rule：pop 最小者；push 同一串列的下一個
    - Termination：堆積為空 / 全部串列耗盡
    - Complexities：$O(N\log K)$ 時間、$O(K)$ 空間（heap）
    - Common failure modes：忘記串列索引；push null 節點；比較器錯誤
  - Dependencies：heap；MergeSortedSequences（用於批次合併）
  - Bug sources & readability：存 `(val, list_id, node/ref)` tuple
- **TwoPointerPartition** — *透過分割不變量做原地重排*
  - Contract
    - Inputs：陣列；判定條件或 pivot/分類
    - State：指標（`low, mid, high`）或（`i,j`）與 pivot
    - Invariant：分割區域已符合分類限制
    - Progress rule：swap 到正確區域；移動指標
    - Termination：指標交錯 / mid > high
    - Complexities：$O(n)$ 時間、$O(1)$ 空間
    - Common failure modes：指標遞增順序；swap 後推進錯指標；pivot 邊界情況
  - Dependencies：swap、比較
  - Bug sources & readability：明確註解區域邊界；若需要穩定性則避免使用
- **MonotonicStack** — *下一個更大/更小、直方圖*
  - Contract
    - Inputs：數值陣列；需要最近的更大/更小邊界
    - State：索引堆疊（依值單調遞增/遞減）
    - Invariant：堆疊索引在值上保持單調；未解決的位置留在堆疊中
    - Progress rule：當目前值破壞單調性時持續 pop 並解決；再 push 目前
    - Termination：結束；pop 剩餘（用 sentinel 解決）
    - Complexities：攤還 $O(n)$ 時間、$O(n)$ 空間
    - Common failure modes：用值而非索引；嚴格性錯（`<` vs `<=`）；缺少 sentinel flush
  - Dependencies：stack
  - Bug sources & readability：命名 `st`；註解「st 存遞增索引」
- **FastSlowPointers** — *Floyd 環 + 中點*
  - Contract
    - Inputs：函式圖 `next = f(x)`（鏈結串列是特例）
    - State：`slow`, `fast`
    - Invariant：進入環後，distance(fast, slow) 每步以環長為模加 1 ⇒ 終會相遇
    - Progress rule：推進 `slow=1`, `fast=2`（或變形）
    - Termination：相遇（有環）或 `fast` 到 null（無環）
    - Complexities：$O(n)$ 時間、$O(1)$ 空間
    - Common failure modes：null 檢查；第二階段重設指標錯
  - Dependencies：指標/next 函式
  - Bug sources & readability：拆 phase1/phase2；helper `advance(node, k)`
- **BacktrackingExploration** — *選擇 → 探索 → 取消選擇 的決策樹*
  - Contract
    - Inputs：候選集合 + 限制；可選目標函式
    - State：`path`, `used[]/start_index`，限制追蹤器
    - Invariant：狀態精準反映目前的部分解
    - Progress rule：逐一產生選擇；`choose`；遞迴；`unchoose`
    - Termination：到葉節點（輸出）或提早結束或界限剪枝
    - Complexities：最壞指數級；剪枝會改變有效分支因子
    - Common failure modes：未還原狀態；共享可變參照；去重層級錯
  - Dependencies：遞迴 (Recursion)/stack；set/bitmask；剪枝檢查
  - Bug sources & readability：實作 `choose/unchoose/is_valid/emit/prune` hooks；避免過早微最佳化
- **MultiSourceBFSWavefront** — *從多個來源做波前式 BFS（grid 為特例）*
  - Contract
    - Inputs：隱式/顯式的無權重圖；多個起點
    - State：佇列 (Queue)（frontier）、visited、distance/time 計數器
    - Invariant：佇列恰好保存目前 frontier；出佇列的節點距離非遞減
    - Progress rule：pop frontier；push 未走訪鄰居；每一層推進時間
    - Termination：佇列空或到達目標
    - Complexities：$O(V+E)$（grid：$O(R\cdot C)$）
    - Common failure modes：太晚標記 visited；混淆層級；重複入佇列
  - Dependencies：queue/deque；visited 表示法
  - Bug sources & readability：用 `for _ in range(len(q))` 分層；座標編碼一致
- **UnionFindConnectivity** — *連通分量 / 環偵測*
  - Contract
    - Inputs：對 `n` 個項目的 edge/union 操作
    - State：`parent[]`, `rank[]/size[]`
    - Invariant：每個集合以 root 代表；`find(x)` 回傳 root
    - Progress rule：`union(a,b)` 合併 root；find 進行路徑壓縮
    - Termination：所有 union 處理完成 / 隨時可查詢
    - Complexities：攤還近似 $O(1)$（反 Ackermann）、$O(n)$ 空間
    - Common failure modes：忘記路徑壓縮；union by rank 錯；0/1 索引混用
  - Dependencies：陣列 (Array)
  - Bug sources & readability：`find` 迭代/遞迴保持乾淨；註解「union 回傳是否真的合併」
- **TopologicalSort** — *DAG 排序*
  - Contract
    - Inputs：有向圖；需要拓樸序或環偵測
    - State：indegree[] + queue（Kahn）或 color/visited + stack（DFS）
    - Invariant：Kahn 的佇列保存入度為 0 的節點；DFS postorder 產生反向完成時間
    - Progress rule：移除節點並遞減入度；或 DFS 鄰居後 append
    - Termination：處理數量 == V（無環）否則有環
    - Complexities：$O(V+E)$ 時間、$O(V)$ 空間
    - Common failure modes：漏掉出度為 0 的節點；indegree 初始化錯；遞迴深度
  - Dependencies：adjacency list；queue/stack
  - Bug sources & readability：追蹤處理數量；明確做環檢查
- **TriePrefixSearch** — *前綴比對*
  - Contract
    - Inputs：words/字串
    - State：trie 節點含 `children`, `is_end`
    - Invariant：從 root 走到某節點的路徑拼出一個前綴
    - Progress rule：`insert`, `search`, `startsWith`；可選 DFS 窮舉
    - Termination：字/前綴結束；窮舉於 children 耗盡時結束
    - Complexities：每次操作 $O(L)$（L=字長）
    - Common failure modes：忘記結尾標記；字母表大導致記憶體暴增
  - Dependencies：node 結構（dict/陣列 children）
  - Bug sources & readability：定義 `Node(children,is_end)`；操作保持對稱

### Domains / meta-techniques（主題傘，不是單一引擎）
- Tree traversal & tree DP（展開後拆到 kernels）：`TreeDFSRecursion`, `TreeBFSLevelOrder`, `TreeDPPostorder`
- DP family：`DP1DLinear`, `DP2DGrid`, `DPInterval`, `DPKnapsackSubsetSum`

### Kernel 組合範例
- `BacktrackingExploration + TriePrefixSearch`（Word Search II 風格）
- `BinarySearchBoundary + Greedy/HeapTopK`（最小可行容量 / 排程可行性）
- `PrefixSumRangeQuery + monotonic deque`（最短子陣列 ≥ K）

---

## Hash Map Indexing 家族（Kernel: HashMapIndexing）
### Dependencies
- `dict` / `Counter`

### 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🔥 [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
- Core（medium）
  - [ ] ✅ [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) *(也屬於 Sliding Window)*
- Stretch（hard）
  - [ ] 🧪 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) *(也屬於 Sliding Window freq-cover)*

### 常見失敗模式（runbook）
- [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py) 在未排序輸入上用「雙指標」做（預設應用 hash map）
- Insert-before-check vs check-before-insert（重複值處理）
- 題意暗示需要時，忘記正規化 key（大小寫/空白）

---

## 雙指標 (Two Pointers) 家族（Kernel: TwoPointersTraversal）
### Dependencies
- 可選排序（`$O(n\log n)$` 前置步驟）、判定條件/比較、常數額外狀態

### Pattern 對照
| Sub-pattern（pattern id） | Pointer init | Invariant | Time | Practice |
|---|---|---|---|---|
| Opposite pointers maximize (`two_pointer_opposite_maximize`) | `l=0, r=n-1` | **消去法**：移動較短邊後，不可能存在使用被捨棄索引的最優解 | $O(n)$ | 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py) |
| Sorted pair search (`two_pointer_sorted_pair_search`) | `l=0, r=n-1` | 若 `nums[l]+nums[r] < t`，則任何含此 `l` 的 pair 都太小 ⇒ `l++`；若 `> t`，則任何含此 `r` 的 pair 都太大 ⇒ `r--` | $O(n)$ | ✅ [LeetCode 167 - Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/) |
| Palindrome check (`two_pointer_opposite_palindrome`) | `l=0, r=n-1` | `s[0:l)` 與 `s(r:n]` 已驗證；指標向內收斂 | $O(n)$ | ✅ [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py), ✅ [LeetCode 680 - Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py) |
| Same-direction writer (`two_pointer_same_direction`) | `write=0`, `read` scans | `[0:write)` 符合判定條件（「保留/清理後」）；`[write:read)` 尚未處理 | $O(n)$ | 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py), ✅ [LeetCode 27 - Remove Element](https://leetcode.com/problems/remove-element/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py), ✅ [LeetCode 80 - Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py), ✅ [LeetCode 283 - Move Zeroes](https://leetcode.com/problems/move-zeroes/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py) |
| Dedup enumeration (k-sum core) (`two_pointer_three_sum`) | sort + fixed `i` + `(l,r)` | 每一層都確定性地跳過重複值；內層 pair-search 以消去為基礎 | $O(n^2)$（+ sort） | 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py), ✅ [LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py), [LeetCode 18 - 4Sum](https://leetcode.com/problems/4sum/description/) |
| Merge（2 sorted） | `i,j` forward | *見下方「Merge Sorted Family」的正典章節（Kernel: MergeSortedSequences）* | $O(m+n)$ | *(正典章節在下方)* |

### 備註（限制與架構）
- Multi-sum 窮舉**需要已排序輸入**；排序成本 `$O(n\log n)$` 會改變總複雜度；有時有 hash-based 替代方案。
- Writer-pointer 變形：輸入常為已排序或以 predicate 過濾；**穩定 vs 不穩定**壓縮很重要；有時需反向迭代（從尾端 write 避免覆寫）。

### 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ] ✅ [LeetCode 125 - Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
- Core（medium）
  - [ ] 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [ ] 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- Stretch（hard）
  - [ ] 🧪 [LeetCode 16 - 3Sum Closest](https://leetcode.com/problems/3sum-closest/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)

### 常見失敗模式（runbook）
- Opposite pointers：移動錯邊會破壞消去證明
- Palindrome：跳過非字母數字時必須正確推進指標
- Writer：忘記 `read` 永遠前進；`write` 只在保留時前進
- k-sum：去重層級錯（同層 vs 跨層）⇒ 重複/漏掉 tuple

---

## 滑動視窗 (Sliding Window) 家族：`substring_window`（Kernel: SubstringSlidingWindow）
### Dependencies
- `Counter/map`；有時 `PrefixSumRangeQuery`, `MonotonicDeque`

### ==先想不變量==
- 視窗 `[L..R]` 合法當且僅當 **不變量成立**
- 模式：
  - **最大化**：擴張 `R`，不合法就縮 `L`
  - **最小化**：擴張直到合法，仍合法就縮 `L`
  - **逐一產生**：擴張 `R`，縮回到合法後，**對每個 `R` 記錄**（或 **Exists**：找到第一個合法視窗就提早停止）

### Pattern 對照（小抄表）
| Pattern | Invariant | State | Window | Typical goal | Practice |
|---|---|---|---|---|---|
| sliding_window_unique | 全部唯一 | last index / freq | variable | maximize | 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) |
| sliding_window_at_most_k_distinct | ≤ K distinct | freq map | variable | maximize | ✅ [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) |
| sliding_window_freq_cover | 對所有 `need` 中的 `c`：`have[c] ≥ need[c]`（重數很重要） | need/have maps | variable/fixed | minimize / exists / all | 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py), ✅ [LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py), ✅ [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) |
| sliding_window_cost_bounded | sum/cost 約束（**需要非負 cost**） | integer sum | variable | minimize | ✅ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) |
| sliding_window_fixed_size | `R-L+1 == k` | rolling sum / freq | fixed | maximize/minimize/逐一產生 | *(此子集合待補練習)* |

### 樣板（以 hook 為主的偽代碼）
```text
L = 0
state = init()

for R in range(n):
  add(R, state)

  while is_invalid(L, R, state):
    remove(L, state)
    L += 1

  record_answer(L, R, state)   # maximize / enumerate
  # or: if is_valid(...) early return  # exists
```

### 重要邊界提醒
- 若陣列可能含**負數**，「cost-bounded」滑動視窗通常會失效（單調性消失）→ 依目標改用 `PrefixSumRangeQuery`（計數/相等）或 `PrefixSum + monotonic deque`（最短 ≥ K）。

### 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- Core（medium）
  - [ ] 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - [ ] ✅ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
  - [ ] ✅ [LeetCode 438 - Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - [ ] ✅ [LeetCode 567 - Permutation in String](https://leetcode.com/problems/permutation-in-string/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
- Stretch（hard）
  - [ ] 🧪 [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)

### 常見失敗模式（runbook）
- 視窗長度 off-by-one：`R-L+1`
- 縮小條件錯：`while invalid` vs `while still valid`
- Freq-cover：`have/need` 更新不一致；忘記重數
- 記錄答案時機錯（縮之前/縮之後）

---

## Prefix Sum 家族（Kernel: PrefixSumRangeQuery）
### Dependencies
- `dict` / `defaultdict(int)`；有時用 `MonotonicDeque` 做「最短 ≥ K」變形

### 樣板：前綴和 + hash map（計數子陣列）
```text
freq = {0: 1}
prefix = 0
ans = 0

for x in nums:
  prefix += x
  ans += freq.get(prefix - k, 0)   # count subarrays sum == k
  freq[prefix] = freq.get(prefix, 0) + 1
```

### 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🧪 [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py) *(hash-map 近親；暖身 map 紀律)*
- Core（medium）
  - [ ] ✅ [LeetCode 209 - Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) *(對照：非負滑動視窗)*
- Stretch（hard）
  - [ ] 🧪 *(此子集合規劃中)* PrefixSum + MonotonicDeque（最短子陣列 ≥ K）

### 常見失敗模式（runbook）
- 少了 `freq[0]=1` 會讓從 index 0 開始的子陣列產生 off-by-one
- 在查詢前先做 `freq[prefix]++` 會改變語意
- 對含負數的資料用滑動視窗（應改用 prefix-based）

---

## 二分搜尋邊界家族（Kernel: BinarySearchBoundary）
### 邊界樣板
- **First true**
```text
lo, hi = 0, n  # hi is exclusive
while lo < hi:
  mid = (lo + hi) // 2
  if predicate(mid):
    hi = mid
  else:
    lo = mid + 1
return lo
```
- **Last true**
```text
lo, hi = -1, n-1
while lo < hi:
  mid = (lo + hi + 1) // 2  # upper mid
  if predicate(mid):
    lo = mid
  else:
    hi = mid - 1
return lo
```
- **在答案空間做二分搜尋**
  - predicate 是可行性/單調限制：`can(mid)`；找最小可行或最大可行

### Practice
- [ ] 🔥 [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py) *(在 partition 上找邊界；也與 merge 推理相關)*

### 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🧪 *(此子集合規劃中)* first >= target boundary
- Core（medium）
  - [ ] 🔥 [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
- Stretch（hard）
  - [ ] 🧪 *(此子集合規劃中)* 在答案上二分搜尋 + 貪婪法 (Greedy)/heap 可行性

### 常見失敗模式（runbook）
- 判定條件非單調 ⇒ 二分搜尋不成立
- mid 偏置錯導致無限迴圈
- inclusive/exclusive 的 `hi` off-by-one

---

## Heap / Selection 家族（Kernels: HeapTopK / DualHeapMedian / TwoPointerPartition）
### Heap vs quickselect（架構面）
- Heap 支援**串流/線上**更新；quickselect 是**批次/離線**且會**變更**陣列內容。
- 複雜度提示：heap 為 $O(n\log k)$；quickselect 平均 $O(n)$、最壞 $O(n^2)$。

### Practice
- [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) *(heap vs quickselect 權衡)*

### 常見失敗模式（runbook）
- 一次性批次卻選 heap（或串流卻選 quickselect）
- 堆積方向錯；忘記把 heap 大小限制在 k

---

## 🔗 Merge Sorted 家族
### Merge 2 sorted（Kernel: MergeSortedSequences）
- [ ] 🔥 [LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
- [ ] ✅ [LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
- [ ] ✅ [LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)

### Merge K sorted（Kernel: KWayMerge）
- **merge_k_sorted_heap**：$O(N \log K)$（串流）
- **merge_k_sorted_divide**：$O(N \log K)$（批次）
- [ ] 🔥 [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py) *(heap 或分治合併；此處不是標準二分搜尋。)*

### 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🔥 [LeetCode 21 - Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
- Core（medium）
  - [ ] ✅ [LeetCode 88 - Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - [ ] ✅ [LeetCode 977 - Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)
- Stretch（hard）
  - [ ] 🔥 [LeetCode 23 - Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)

### 常見失敗模式（runbook）
- 一邊耗盡時遺失尾端
- 指標遞增錯導致無限迴圈
- 原地合併：覆寫尚未讀取的資料（需要從尾端 write）

---

## 單調堆疊 (Monotonic Stack) 家族（Kernel: MonotonicStack）
### 正典 patterns
- `next_greater_element`：當 `nums[st[-1]] <= nums[i]` 就 pop，解出「下一個更大」
- `stock_span`：堆疊存遞減價格；透過 pop 掉較小/相等者計算 span
- `histogram_max_rectangle`：堆疊存遞增高度；pop 時計算面積（寬度由邊界決定）

### 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🧪 *(此子集合規劃中)* next greater element
- Core（medium）
  - [ ] 🧪 *(此子集合規劃中)* stock span
- Stretch（hard）
  - [ ] 🧪 *(此子集合規劃中)* largest rectangle in histogram

### 常見失敗模式（runbook）
- 用值而不是索引（無法算寬度）
- 嚴格性錯（`<` vs `<=`）會改變「下一個更大」語意
- 忘記用 sentinel 做最後 flush

---

## 圖 (Graph) 波前 BFS（Kernel: MultiSourceBFSWavefront）
### Dependencies
- queue/deque、visited 表示法、座標編碼

### Contract（明確版）
- 佇列保存**frontier**。
- 每次外層迴圈代表**一步/一分鐘**（層序）：處理剛好 `len(queue)` 個節點，然後時間 +1。
- `visited` 防止重複入佇列；應在**入佇列時**標記 visited，不是出佇列時。

### Implementation adapters
- 座標編碼 `(r,c)` 或 `id = r*C + c`。
- visited 表示法：`bool grid`、`set`、或 bitset（節省空間）。

### Practice 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🔥 [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- Core（medium）
  - [ ] 🧪 *(此子集合規劃中)* 多來源到最近設施的最短距離
- Stretch（hard）
  - [ ] 🧪 *(此子集合規劃中)* 帶狀態壓縮（bitmask）的 BFS

### 常見失敗模式（runbook）
- pop 時才標記 visited ⇒ 重複項暴增、佇列膨脹
- 沒有分層 ⇒ 時間/分鐘計數錯
- 漏邊界檢查 / 鄰居 delta 寫錯

---

## Union-Find 家族（Kernel: UnionFindConnectivity）
### DSU API（何時用）
- 當邊會新增，且你需要**動態連通性**查詢（連通分量、無向圖環偵測）時用 DSU。
- 需要走訪順序/路徑，或圖是靜態且要明確可達路徑時，偏好 廣度優先搜尋 (BFS)/深度優先搜尋 (DFS)。

```text
find(x):
  if parent[x] != x: parent[x] = find(parent[x])
  return parent[x]

union(a,b):
  ra, rb = find(a), find(b)
  if ra == rb: return False
  attach smaller-rank under larger-rank
  return True
```

### 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🧪 *(此子集合規劃中)* connected components
- Core（medium）
  - [ ] 🧪 *(此子集合規劃中)* cycle detection（undirected）
- Stretch（hard）
  - [ ] 🧪 *(此子集合規劃中)* grid 上的 DSU（islands union）

### 常見失敗模式（runbook）
- 不做路徑壓縮 ⇒ 大輸入超時
- rank/size 更新錯 ⇒ 樹過深
- 0/1 索引混用

---

## 🐢🐇 快慢指標 (Fast-Slow Pointers)（Kernel: FastSlowPointers）
### Floyd 兩階段心智模型
- Phase 1：偵測環
  - Invariant：一旦兩指標都在環內，fast 與 slow 的距離每步以環長為模加 1 ⇒ 終會相遇。
- Phase 2：找環的起點（把其中一個指標重設到 head）
  - 從相遇點開始，兩者都以速度 1 移動，會在入口相遇。

### 不只適用鏈結串列
- 適用於 **函式圖**：`f(x)` 定義下一狀態；鏈結串列是特例。

### Practice 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🔥 [LeetCode 141 - Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py) *(偵測環)*
- Core（medium）
  - [ ] 🔥 [LeetCode 142 - Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py) *(環起點)*
  - [ ] ✅ [LeetCode 876 - Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py) *(中點)*
- Stretch（hard）
  - [ ] ✅ [LeetCode 202 - Happy Number](https://leetcode.com/problems/happy-number/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py) *(隱式環)*

### 常見失敗模式（runbook）
- 少了 `fast` 的 null 檢查（特別在 Python/Java）
- Phase 2 重設邏輯錯（兩者必須都走 1 步）
- 使用 fast=fast.next（不是 2 步）會破壞相遇保證

---

## 🧩 回溯法 (Backtracking)（Kernel: BacktrackingExploration）
### Dependencies
- 遞迴 (Recursion)/stack；`used[]` 或 bitmask；限制追蹤器（sets/陣列）

### ==不變量==
- **狀態一致性**：從遞迴回來後，狀態必須被完全還原

### 回溯支援的目標（控制流程策略）
- 窮舉所有解
- 找到一個解（提早結束）
- 最佳化最佳解（追蹤全域最佳）

### 回溯介面（hooks）
| Hook | Purpose |
|---|---|
| `choose(choice)` | 將 choice 套用到狀態 |
| `unchoose(choice)` | 還原狀態 |
| `is_valid()` | 區域限制檢查 |
| `emit()` | 記錄解 |
| `prune()` | 界限 / 可行性檢查 |
| `next_choices()` | 排序啟發式 |

### 5 種決策樹形狀（選對「狀態把手」）
- **Permutation** → `used[]`
  - [ ] 🔥 [LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
  - [ ] ✅ [LeetCode 47 - Permutations II](https://leetcode.com/problems/permutations-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py) *(去重：排序 + 同層略過，條件 `used[i-1]==False`)*
- **Subset** → `start_index`
  - [ ] 🔥 [LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
  - [ ] ✅ [LeetCode 90 - Subsets II](https://leetcode.com/problems/subsets-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py) *(去重：排序 + 同層略過 `i>start && nums[i]==nums[i-1]`)*
- **Combination / 固定大小** → `start_index` + `len(path)==k`
  - [ ] ✅ [LeetCode 77 - Combinations](https://leetcode.com/problems/combinations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py) *(排序後可提早 break)*
  - [ ] 🔥 [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py) *(可重用：用 `i` 遞迴)*
  - [ ] ✅ [LeetCode 40 - Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py) *(不可重用：用 `i+1` 遞迴 + 去重)*
  - [ ] ✅ [LeetCode 216 - Combination Sum III](https://leetcode.com/problems/combination-sum-iii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py) *(固定數量 + 有界範圍)*
- **Constraint satisfaction / placement**
  - [ ] 🔥 [LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - [ ] ✅ [LeetCode 52 - N-Queens II](https://leetcode.com/problems/n-queens-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
  - [ ] ✅ [LeetCode 93 - Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)
  - [ ] ✅ [LeetCode 131 - Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
  - [ ] ✅ [LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

### 回溯「工具帶」
- **Pruning**
  - 可行性界限（剩餘選擇不夠）
  - 目標界限（`remaining < 0`）
  - 排序後提早結束（`candidates[i] > remaining → break`）
- **去重策略**
  - 排序 + 同層略過（subset/combination）
  - 排序 + `used` 略過（permutation）
- **調整旋鈕**
  - 選擇順序（最受限制優先）
  - 限制傳播（維護可用集合）
  - memoization（狀態重複時）
  - bitmask 壓縮狀態

### 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🔥 [LeetCode 78 - Subsets](https://leetcode.com/problems/subsets/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
- Core（medium）
  - [ ] 🔥 [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
  - [ ] ✅ [LeetCode 46 - Permutations](https://leetcode.com/problems/permutations/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
- Stretch（hard）
  - [ ] 🔥 [LeetCode 51 - N-Queens](https://leetcode.com/problems/n-queens/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)

### 常見失敗模式（runbook）
- 沒有還原狀態（少了 `unchoose`）
- `emit` 時未複製就改動共享 list
- 去重做在錯誤的遞迴層級
- 想要「找一個解」時，提早結束的 wiring 沒接好

---

## 🎛️ 分割與選擇（Kernel: TwoPointerPartition / HeapTopK）
### 分割不變量（Dutch flag）
- 維持區域：
  - `[0..low)` 是 0
  - `[low..mid)` 是 1
  - `[mid..high]` 未知
  - `(high..end]` 是 2

### Practice 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] ✅ [LeetCode 905 - Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
  - [ ] ✅ [LeetCode 922 - Sort Array By Parity II](https://leetcode.com/problems/sort-array-by-parity-ii/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
- Core（medium）
  - [ ] 🔥 [LeetCode 75 - Sort Colors](https://leetcode.com/problems/sort-colors/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
- Stretch（hard）
  - [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) *(quickselect 分割)*

### kth/top-k 的 heap 替代方案（Kernel: HeapTopK）
- [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) *(對照：quickselect 平均 $O(n)$ vs heap $O(n\log k)$；heap 線上，quickselect 離線且會變更內容)*

### 常見失敗模式（runbook）
- Partition：swap 後推進錯指標
- 假設穩定性（partition 通常不穩定）
- 忘記 quickselect 最壞 $O(n^2)$

---

## Trie 家族（Kernel: TriePrefixSearch）
### Trie 操作（API）
- `insert(word)`
- `search(word)`（完整字）
- `startsWith(prefix)`
- traversal/DFS 窮舉（autocomplete）

### 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🧪 *(此子集合規劃中)* 基礎 trie insert/search
- Core（medium）
  - [ ] 🧪 *(此子集合規劃中)* 前綴 autocomplete 窮舉
- Stretch（hard）
  - [ ] 🧪 *(此子集合規劃中)* Trie + 回溯法（Word Search II 風格）

### 常見失敗模式（runbook）
- 把 `startsWith` 與 `search` 搞混（結尾標記）
- 沒處理空字串邊界情況
- 字母表大導致記憶體暴增（children 用 dict）

---

## 拓樸排序家族（Kernel: TopologicalSort）
### 兩種樣板
- **Kahn’s algorithm（對 indegrees 做 BFS）**：佇列放入度為 0 的節點；pop 後遞減鄰居
- **DFS postorder**：用顏色偵測環；離開時 append；反向 postorder 即 topo

### 梯度（Intro → Core → Stretch）
- Intro（easy）
  - [ ] 🧪 *(此子集合規劃中)* 簡單 DAG 排序
- Core（medium）
  - [ ] 🧪 *(此子集合規劃中)* prerequisites / course schedule
- Stretch（hard）
  - [ ] 🧪 *(此子集合規劃中)* topo + DAG 上的 DP

### 常見失敗模式（runbook）
- 沒把所有節點算進去（孤立節點漏掉）
- 沒偵測到環（processed count < V）
- Python 用 DFS 時遞迴深度問題（未改迭代）

---

## 真實世界類比（kernel → 系統）
- Sliding window → log 處理 / rate limiting 視窗
- TopK/Heap → 熱門項目、串流排行榜
- Multi-source BFS wavefront → 傳播/感染模擬、最近設施
- Union-Find → 分群、網路連通性

---

## 🧭 Roadmap Anchors（來自你的圖）
### 課綱（有順序）
- HashMapIndexing → Two Pointers → Sliding Window → Prefix Sum → Binary Search → Heap/TopK → Merge → Monotonic Stack → BFS/DFS → UnionFind → Backtracking → Trie → DP → Toposort

### 涵蓋清單（無順序）
- **NeetCode 150** *(用上方地圖章節找每題的 kernel/pattern)*：[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 2, 3, 4, 11, 15, 21, 23, 25, 26, 27, 39, 40, 46, 51, 75, 76, 78, 79, 80, 88, 90, 125, 131, 141, 142, 202, 209, 215, 283, 438, 567, 680, 876, 905, 922, 977, 994
- **Blind 75** *(用上方地圖章節找每題的 kernel/pattern)*：[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py), 3, 11, 15, 21, 23, 26, 39, 75, 76, 79, 125, 141, 142, 215, 994
- **專精路線**
  - Sliding Window Mastery：🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py), 76, 209, 340, 438, 567
  - BFS Mastery：🔥 [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

### 題目 → kernel(s) 對照（精簡）
| LeetCode | Kernel(s) |
|---:|---|
| 1 | HashMapIndexing |
| 3 | SubstringSlidingWindow; HashMapIndexing |
| 4 | BinarySearchBoundary |
| 11 | TwoPointersTraversal |
| 15 | TwoPointersTraversal |
| 16 | TwoPointersTraversal |
| 21 | MergeSortedSequences |
| 23 | KWayMerge |
| 26 | TwoPointersTraversal |
| 27 | TwoPointersTraversal |
| 39 | BacktrackingExploration |
| 40 | BacktrackingExploration |
| 46 | BacktrackingExploration |
| 47 | BacktrackingExploration |
| 51 | BacktrackingExploration |
| 52 | BacktrackingExploration |
| 75 | TwoPointerPartition |
| 76 | SubstringSlidingWindow |
| 77 | BacktrackingExploration |
| 78 | BacktrackingExploration |
| 79 | BacktrackingExploration |
| 80 | TwoPointersTraversal |
| 88 | MergeSortedSequences |
| 90 | BacktrackingExploration |
| 93 | BacktrackingExploration |
| 125 | TwoPointersTraversal |
| 131 | BacktrackingExploration |
| 141 | FastSlowPointers |
| 142 | FastSlowPointers |
| 202 | FastSlowPointers |
| 209 | SubstringSlidingWindow |
| 215 | HeapTopK; TwoPointerPartition |
| 283 | TwoPointersTraversal |
| 340 | SubstringSlidingWindow |
| 438 | SubstringSlidingWindow |
| 567 | SubstringSlidingWindow |
| 680 | TwoPointersTraversal |
| 876 | FastSlowPointers |
| 905 | TwoPointerPartition |
| 922 | TwoPointerPartition |
| 977 | MergeSortedSequences |
| 994 | MultiSourceBFSWavefront |

---

## ✅ 快速「下一個 10 題」播放清單（均衡）
- 涵蓋 **7 kernels**：HashMapIndexing, TwoPointersTraversal, SubstringSlidingWindow, BinarySearchBoundary, HeapTopK, BacktrackingExploration, MultiSourceBFSWavefront
- [ ] 🔥 [LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
- [ ] 🔥 [LeetCode 26 - Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
- [ ] 🔥 [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [ ] 🔥 [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- [ ] 🔥 [LeetCode 4 - Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
- [ ] 🔥 [LeetCode 215 - Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
- [ ] 🔥 [LeetCode 39 - Combination Sum](https://leetcode.com/problems/combination-sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
- [ ] 🔥 [LeetCode 76 - Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
- [ ] 🔥 [LeetCode 15 - 3Sum](https://leetcode.com/problems/3sum/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- [ ] 🔥 [LeetCode 994 - Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
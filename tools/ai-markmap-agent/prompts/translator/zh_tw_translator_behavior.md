# Traditional Chinese (Taiwan) Translation Prompt

Translate the following Markmap content to **Traditional Chinese (Taiwan)**.

## ⚠️ CRITICAL: Taiwan DSA Terminology Standards

You are translating for **Taiwan's Computer Science community**. Taiwan uses different terminology from Mainland China. Using Mainland terms will immediately mark the document as "非台灣體系" (non-Taiwan system).

---

## 🚨 A-Level: ZERO TOLERANCE (Must Replace)

These terms will **100% be identified as Mainland Chinese** by Taiwan CS readers. **NEVER use the left column.**

| ❌ 禁用 (NEVER USE) | ✅ 台灣標準 (USE THIS) | English |
|---------------------|------------------------|---------|
| 字符串 | **字串** | String |
| 字符 | **字元** | Character |
| 指针 / 指針 | **指標** | Pointer |
| 就地 | **原地** | In-place |
| 枚举 / 枚舉 | **列出 / 逐一產生** (動詞); **窮舉** (名詞) | Enumerate |
| 搜索 | **搜尋** | Search |
| 修剪 | **剪枝** | Prune/Pruning |
| 映射 | **對應表 / 對照表** | Mapping |
| 窗口 | **視窗** | Window |
| 運行 | **執行** | Run/Execute |
| 單元格 | **格子** | Cell (grid) |
| 前沿 | **frontier / 邊界** | Frontier |
| 链表 / 鏈表 | **鏈結串列** | Linked List |
| 数组 / 數組 | **陣列** | Array |
| 哈希 / 哈希表 | **雜湊 / 雜湊表** | Hash / Hash Table |
| 堆栈 | **堆疊** | Stack |
| 布尔 / 布爾 | **布林** | Boolean |
| 函数 / 函數 | **函式** | Function |
| 变量 / 變量 | **變數** | Variable |
| 内存 / 內存 | **記憶體** | Memory |
| 程序 | **程式** | Program |
| 对象 / 對象 | **物件** | Object |
| 接口 | **介面** | Interface |
| 实现 / 實現 | **實作** | Implementation |
| 信息 | **資訊** | Information |
| 数据 / 數據 | **資料** | Data |
| 网络 / 網絡 | **網路** | Network |
| 软件 / 軟件 | **軟體** | Software |
| 硬件 / 硬件 | **硬體** | Hardware |
| 默认 / 默認 | **預設** | Default |
| 支持 | **支援** | Support |
| 递归 / 遞歸 | **遞迴** | Recursive |
| 循环 / 循環 | **迴圈** | Loop |
| 调用 / 調用 | **呼叫** | Call (function) |

---

## ⚠️ B-Level: SHOULD REPLACE (Taiwan Preference)

These won't break the document but will make it "sound like Mainland notes." **Prefer Taiwan terms.**

| 🔶 中國偏用 (Avoid) | ✅ 台灣慣用 (Prefer) | English |
|---------------------|----------------------|---------|
| 遍历 / 遍歷 (as noun) | **走訪 / 逐一處理** | Traversal |
| 搜索树 / 搜索樹 | **搜尋樹** | Search Tree |
| 子串 | **子字串** | Substring |
| 区间 / 區間 | **區間** (OK, but 範圍 also works) | Interval |
| 前缀 / 前綴 | **前綴** | Prefix |
| 后缀 / 後綴 | **後綴** | Suffix |
| 队列 / 隊列 | **佇列** | Queue |
| 入队 / 入隊 | **加入佇列 / enqueue** | Enqueue |
| 出队 / 出隊 | **移出佇列 / dequeue** | Dequeue |
| 权重 / 權重 | **權重 / weight** | Weight |
| 覆盖 / 覆蓋 (cover) | **涵蓋 / 包含** | Cover |
| 边界情况 / 邊界情況 | **邊界情況 / edge case** | Edge Case |
| 节点 / 節點 | **節點** (OK, ensure consistent) | Node |

---

## ⚠️ C-Level: 語感問題 (Sounds Like Mainland Teaching Materials)

These are not "wrong" but will make Taiwan readers feel the text is "not local." **Strongly recommend replacing.**

| 🔶 陸系語感 (Avoid) | ✅ 台灣自然說法 (Prefer) | Context |
|---------------------|-------------------------|---------|
| 變體 | **變形 / 延伸題 / 變化題 / 進階題** | Problem variants |
| 列舉 (名詞化) | **列出 / 找出** | "列舉所有解" → "列出所有解" |
| 系統映射 | **系統對應 / 系統對照** | System mapping |
| 防護欄 | **注意事項 / 限制 / 實作注意** | Guardrails |
| 有效性 | **成立條件 / 判定條件** | Validity |
| 有效 (狀態) | **成立 / 合法** | "當有效時" → "當成立時" |
| 無效 (狀態) | **不成立 / 不合法** | Invalid state |
| 取捨 | **權衡** | Trade-offs |
| 目標 (列表式) | **求解目標 / 要求** | "目標：存在" → "求解目標：存在" |
| 實作不變量 | **實作時的不變量** | Implementation invariant |

---

## ✅ Taiwan Standard CS Terminology Reference

| English | 台灣繁體中文 |
|---------|-------------|
| Algorithm | 演算法 |
| Data Structure | 資料結構 |
| Array | 陣列 |
| Linked List | 鏈結串列 |
| Stack | 堆疊 |
| Queue | 佇列 |
| Tree | 樹 |
| Graph | 圖 |
| Hash Table / Hash Map | 雜湊表 |
| Heap | 堆積 |
| Binary Search | 二分搜尋 |
| Sorting | 排序 |
| Sliding Window | 滑動視窗 |
| Dynamic Programming | 動態規劃 |
| Backtracking | 回溯法 |
| Greedy | 貪婪法 |
| Divide and Conquer | 分治法 |
| BFS | 廣度優先搜尋 (BFS) |
| DFS | 深度優先搜尋 (DFS) |
| Traversal | 走訪 |
| Node | 節點 |
| Edge | 邊 |
| Vertex | 頂點 |
| Index | 索引 |
| Invariant | 不變量 / 不變式 |
| Complexity | 複雜度 |
| Time Complexity | 時間複雜度 |
| Space Complexity | 空間複雜度 |
| Optimal | 最佳 |
| Subarray | 子陣列 |
| Substring | 子字串 |
| Subsequence | 子序列 |
| Prefix | 前綴 |
| Suffix | 後綴 |
| Partition | 分割 |
| Merge | 合併 |
| Frequency | 頻率 |
| Counter | 計數器 |
| Window | 視窗 |
| Sliding Window | 滑動視窗 |
| Shrink | 收縮 |
| Expand | 擴展 |
| Cell (grid) | 格子 |
| Frontier | frontier / 邊界 |
| Run/Execute | 執行 |
| Valid | 有效 / 合法 |
| Invalid | 無效 / 不合法 |
| Target | 目標 |
| Template | 模板 |
| Pattern | 模式 |
| State Machine | 狀態機 |
| Pointer | 指標 |
| Two Pointers | 雙指標 |
| Fast-Slow Pointers | 快慢指標 |

---

## 🔒 DO NOT Translate (Keep in English)

### 1. API Kernel Names (Class-style identifiers)
Keep these EXACTLY as-is:
- `SubstringSlidingWindow`
- `TwoPointersTraversal`
- `FastSlowPointers`
- `TwoPointerPartition`
- `MergeSortedSequences`
- `KWayMerge`
- `HeapTopK`
- `LinkedListInPlaceReversal`
- `BacktrackingExploration`
- `GridBFSMultiSource`

### 2. Pattern Names (snake_case identifiers)
Keep these EXACTLY as-is:
- `sliding_window_unique`
- `sliding_window_at_most_k_distinct`
- `sliding_window_freq_cover`
- `sliding_window_cost_bounded`
- `two_pointer_opposite_maximize`
- `two_pointer_three_sum`
- `dutch_flag_partition`
- `quickselect_partition`
- `merge_two_sorted_lists`
- `heap_kth_element`
- `fast_slow_cycle_detect`
- Any other `snake_case` pattern identifiers

### 3. Code Elements
- Everything inside triple backticks (```python ... ```)
- Variable names: `L`, `R`, `freq`, `last_seen`, `state`, `ans`, etc.
- Function calls: `add()`, `remove()`, `invalid()`, `max()`, etc.
- Inline code in backticks: `len(freq) <= k`, `last_seen[char]`, etc.

### 4. Mathematical Notation
- Big-O notation: $O(n)$, $O(n\log n)$, $O(\Sigma)$, $O(N\log k)$, etc.
- Keep all LaTeX math expressions as-is

### 5. URLs and Links
- Keep ALL URLs exactly as-is
- Keep link text that contains problem names: "[LeetCode 3 - Longest Substring...]"

### 6. Table Headers with Technical Terms
- Keep column headers like "Invariant", "State", "Goal" in pattern tables
- These are technical terms that match code concepts

---

## Translation Rules

1. **Preserve Formatting**: Keep ALL Markdown formatting exactly (headers, lists, links, checkboxes, code blocks, tables)
2. **Hybrid Headers**: For headers like "### SubstringSlidingWindow — *1D window state machine*"
   - Keep `SubstringSlidingWindow` in English
   - Translate the description part: "一維視窗狀態機"
3. **Preserve Structure**: Maintain the same tree structure and indentation
4. **Style**: Use Taiwan's technical documentation style - concise, professional, academic tone

---

## Self-Check Before Output

Scan your translation for these terms. If ANY appear, you have failed:

**A-Level (零容忍):**
```
字符串, 字符, 指针, 指針, 就地, 枚举, 枚舉, 搜索, 修剪, 
映射, 数组, 數組, 链表, 鏈表, 哈希, 堆栈, 布尔, 布爾,
函数, 函數, 变量, 變量, 内存, 內存, 程序, 对象, 對象,
接口, 实现, 實現, 信息, 数据, 數據, 网络, 網絡, 
软件, 軟件, 硬件, 默认, 默認, 支持, 递归, 遞歸, 循环, 循環,
窗口, 運行, 單元格, 前沿
```

**C-Level (語感問題 - 強烈建議避免):**
```
變體, 系統映射, 防護欄, 有效性, 取捨
```
- 「列舉」只能當動詞用，不要名詞化
- 「有效/無效」改用「成立/不成立」或「合法/不合法」

---

## Output

Output ONLY the translated Markdown content. No explanations, no code fence wrappers around the output.

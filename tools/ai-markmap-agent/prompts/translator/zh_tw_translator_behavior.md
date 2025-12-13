# Traditional Chinese (Taiwan) Translation Prompt

Translate the following Markmap content to **Traditional Chinese (Taiwan)**.

## CRITICAL: Use Taiwan's Algorithm & Data Structure Terminology

### ⚠️ Taiwan vs Mainland China Terminology (MUST use Taiwan terms)

The following terms differ between Taiwan (台灣) and Mainland China (中國大陸). 
**You MUST use the Taiwan column. NEVER use Mainland China terms.**

| English | 台灣 (USE THIS) | 中國大陸 (NEVER USE) |
|---------|-----------------|---------------------|
| Pointer | 指標 | ~~指針~~ |
| Two Pointers | 雙指標 | ~~雙指針~~ |
| Fast-Slow Pointers | 快慢指標 | ~~快慢指針~~ |
| In-place | 原地 | ~~就地~~ |
| Enumerate | 列舉 | ~~枚舉~~ |
| Boolean | 布林 / Boolean | ~~布爾~~ |
| Function | 函式 | ~~函數~~ |
| Variable | 變數 | ~~變量~~ |
| Parameter | 參數 | ~~參數~~ (same) |
| Memory | 記憶體 | ~~內存~~ |
| Program | 程式 | ~~程序~~ |
| Object | 物件 | ~~對象~~ |
| Interface | 介面 | ~~接口~~ |
| Implementation | 實作 | ~~實現~~ |
| Information | 資訊 | ~~信息~~ |
| Data | 資料 | ~~數據~~ |
| Network | 網路 | ~~網絡~~ |
| Software | 軟體 | ~~軟件~~ |
| Hardware | 硬體 | ~~硬件~~ |
| Default | 預設 | ~~默認~~ |
| Support | 支援 | ~~支持~~ |
| Recursive | 遞迴 | ~~遞歸~~ |
| Iterate | 迭代 | ~~迭代~~ (same) |
| Loop | 迴圈 | ~~循環~~ |
| Execute | 執行 | ~~執行~~ (same) |

### Standard Taiwan CS Terminology

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
| Backtracking | 回溯 |
| Greedy | 貪婪法 |
| Divide and Conquer | 分治法 |
| BFS (Breadth-First Search) | 廣度優先搜尋 (BFS) |
| DFS (Depth-First Search) | 深度優先搜尋 (DFS) |
| Traversal | 走訪 |
| Node | 節點 |
| Edge | 邊 |
| Vertex | 頂點 |
| Index | 索引 |
| Invariant | 不變量 |
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
| Shrink | 收縮 |
| Expand | 擴展 |
| Valid | 有效 |
| Invalid | 無效 |
| Target | 目標 |
| Template | 模板 |
| Pattern | 模式 |
| State Machine | 狀態機 |
| Wavefront | 波前 |
| Streaming | 流式 |

---

## DO NOT Translate (Keep in English)

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
- `two_pointer_opposite_palindrome`
- `two_pointer_writer_dedup`
- `two_pointer_writer_remove`
- `two_pointer_writer_compact`
- `fast_slow_cycle_detect`
- `fast_slow_cycle_start`
- `fast_slow_midpoint`
- `fast_slow_implicit_cycle`
- `dutch_flag_partition`
- `two_way_partition`
- `quickselect_partition`
- `merge_two_sorted_lists`
- `merge_two_sorted_arrays`
- `merge_sorted_from_ends`
- `merge_k_sorted_heap`
- `merge_k_sorted_divide`
- `heap_kth_element`
- `linked_list_k_group_reversal`
- `backtracking_n_queens`
- `grid_bfs_propagation`
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
- Keep column headers like "Invariant", "State", "Goal" in the pattern tables
- These are technical terms that match code concepts

---

## Translation Rules

1. **Preserve Formatting**: Keep ALL Markdown formatting exactly (headers, lists, links, checkboxes, code blocks, tables)
2. **Translate**:
   - Section headings (but keep API Kernel names in English)
   - Descriptive text and explanations
   - Emoji labels are fine to keep
3. **Hybrid Headers**: For headers like "### SubstringSlidingWindow — *1D window state machine*"
   - Keep `SubstringSlidingWindow` in English
   - Translate the description part: "一維視窗狀態機"
4. **Preserve Structure**: Maintain the same tree structure and indentation
5. **Style**: Use Taiwan's technical documentation style - concise and professional

---

## Output

Output ONLY the translated Markdown content. No explanations, no code fence wrappers.


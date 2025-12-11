---
title: Sliding Window & Two Pointers 精通地圖（含 NeetCode / Blind 75 連結）
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

# Sliding Window & Two Pointers 精通地圖 🎯

> 核心目標：用最常考的「滑動視窗 + 雙指針」題型，建立一套可重用的解題心智模型。  
> 適用：面試準備（NeetCode 150 / Blind 75）、競賽、系統化學演算法。

---

## 1️⃣ API Kernel 核心機制 <!-- markmap: fold -->

### `SubstringSlidingWindow`（滑動視窗）

- 定義：在序列上維護動態區間 `[left, right]`，同時維持某個**不變條件（invariant）**
- 通用模板（變長視窗）：

```python
left = 0
state = init_state()
ans = init_answer()

for right, x in enumerate(seq):
    add(state, x)          # 擴張右邊
    
    while violate(state):  # 若不變條件被破壞 → 收縮左邊
        remove(state, seq[left])
        left += 1
    
    ans = update(ans, left, right, state)  # 視題目而定：取最長/最短/記錄位置

return ans
```

- 關鍵思維：
  - 「不變條件」是整個解法的靈魂
  - 視窗只會線性擴張＋收縮 → 時間複雜度多半是 $O(n)$

---

### `TwoPointersTraversal`（雙指針遍歷）

- 定義：在序列上使用兩個指標，按照某種規則移動，維持一個**關係不變式**
- 典型子模式：
  - 對向指針：`left → ... ← right`
  - 同向讀寫指針：`read →`、`write →`
- 通用模板（對向）：

```python
left, right = 0, len(arr) - 1
ans = init_answer()

while left < right:
    cur = evaluate(arr, left, right)
    ans = update(ans, cur, left, right)
    
    if should_move_left(cur):
        left += 1
    else:
        right -= 1

return ans
```

---

### `FastSlowPointers`（快慢指針）

- 定義：兩個指標在「隱式序列」上以不同速度前進（常見：慢 1 步、快 2 步）
- 典型用途：
  - 判斷是否有環
  - 找環的起點
  - 找鏈表中點

---

### `TwoPointerPartition`（雙指針分區）

- 定義：利用 2～3 個指標在陣列中做原地分區（partition）
- 常見場景：
  - 荷蘭國旗（0/1/2 顏色）
  - 奇偶分區、按條件分組
  - Quickselect / 快速選擇

---

### `MergeSortedSequences`（合併排序序列）

- 定義：用雙指針從兩個已排序序列頭或尾開始比較，線性合併
- 常見場景：
  - 合併兩條已排序鏈表 / 陣列
  - 從兩端「合併平方值」等

---

## 2️⃣ Pattern 圖譜：滑動視窗 Sliding Window <!-- markmap: fold -->

### 2.1 視窗內元素需「全部唯一」：`sliding_window_unique` 🔑

- 不變式：視窗內所有字元皆不重複
- 經典題：
  - [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)（NeetCode 150 / Blind 75 / Grind 75 / Top 100）
- 重點：
  - `last_seen[char]` 紀錄**最後一次出現位置**
  - 當遇到重複字元且在視窗內 → `left = max(left, last_seen[char] + 1)`
  - 這題是所有滑動視窗的「母題」

---

### 2.2 視窗中「至多 K 種不同字元」：`sliding_window_at_most_k_distinct`

- 不變式：`distinct_count <= K`
- 經典題：
  - [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
- 思路：
  - 用 `freq[char]` + `len(freq)` 追蹤不同字元數
  - 若超過 K → `while len(freq) > K: shrink left`

---

### 2.3 視窗需「涵蓋所有需求頻率」：`sliding_window_freq_cover`（字頻覆蓋）

- 不變式：對每個 `c`，`have[c] >= need[c]`
- 子類型：
  - ✅ 最小視窗（變長、求最短）
  - ✅ 固定長度全排列 / anagram 檢查

#### 2.3.1 最小視窗覆蓋：`Minimum Window Substring`

- 經典題：
  - [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)（Hard / NeetCode 150 / Blind 75）
- 模式：
  - 擴張右指針直到「全部需求滿足」
  - 之後盡可能收縮左指針，維持仍然有效 → 取最短長度
- 心法：
  - `need` map + `have` map
  - `satisfied_count == required_count` 時代表視窗有效

#### 2.3.2 固定長度 anagram / permutation 視窗

- 視窗大小 = pattern 長度，滑動過程中維持頻率相等
- 經典題：
  - [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
  - [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
- 模式：
  - 固定視窗大小 `k`
  - 每次移動右指針，同時移除左邊舊元素
  - 用「已配對字元數」判斷是否完全匹配

---

### 2.4 視窗「數值和受限」：`sliding_window_cost_bounded`

- 不變式：`window_sum >= target`（或 `<= target` 之類）
- 經典題：
  - [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)（NeetCode 150 / Sliding Window Path）
- 關鍵條件：
  - 陣列元素為**正整數** → 和隨視窗擴張單調增加 → 可用雙指針線性掃描
- 模式：
  - 擴張右邊累加 `sum`
  - 當 `sum >= target` → 儘量收縮左邊以縮短長度

---

### 2.5 Pattern 對照表 📋

| 類型 | 代表題目 | 不變式 | 視窗長度 | 目標 |
|------|----------|--------|----------|------|
| 唯一字元 | [LeetCode 3](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py) | 視窗內無重複 | 變長 | 最大長度 |
| 至多 K 種 | [LeetCode 340](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py) | 種類數 ≤ K | 變長 | 最大長度 |
| 覆蓋所有字頻 | [LeetCode 76](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py) | have ≥ need | 變長 | 最短長度 |
| 固定長 anagram | [LeetCode 567](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py), [LeetCode 438](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py) | have == need | 固定 | 存在 / 收集所有位置 |
| 和 ≥ target | [LeetCode 209](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py) | sum ≥ target | 變長 | 最短長度 |

---

## 3️⃣ Pattern 圖譜：Two Pointers 雙指針 <!-- markmap: fold -->

### 3.1 對向指針：`two_pointer_opposite*`（Two-End）🔥

> 適用：**排序陣列**、對稱結構（回文）、最大化/最小化某函數

#### 3.1.1 兩端收縮最大化函數：`two_pointer_opposite_maximize`

- 經典題：
  - [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)（NeetCode 150 / Blind 75 / Top 100）
- 思維：
  - 面積 = `min(h[left], h[right]) * (right-left)`
  - 總是移動**較矮**的那一邊，因為寬度變窄，只有提高短板才可能增大面積

#### 3.1.2 排序後找 pair / 3Sum：`two_pointer_opposite_search` / `two_pointer_three_sum`

- 經典題：
  - [LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)（此實作多用 hash，但也可排序＋對向指針）
  - [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
  - [LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
- 模式：
  - 外層枚舉第一個數（注意去重）
  - 內層用 `left, right` 找剩下兩數
  - 根據 `sum` 與目標關係移動左右指針

#### 3.1.3 回文檢查：`two_pointer_opposite_palindrome`

- 經典題：
  - [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
- 模式：
  - `left`、`right` 從兩端往中間
  - 比較字元，若不等：
    - 基本版：直接 false
    - 允許刪一字版：試 `skip left` 或 `skip right` 其一仍為回文即可

---

### 3.2 同向讀寫指針：`two_pointer_writer_*`（In-place Writer Pattern）

> 適用：**原地修改陣列**，如刪除元素、去重、壓縮

- 不變式：`nums[0:write]` 是目前為止的「有效區間」

#### 3.2.1 去重（保留一次 / 保留至多兩次）

- 經典題：
  - [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
- 模式：
  - 陣列已排序 → 相同元素相鄰
  - `if read == 0 or nums[read] != nums[write-1]: keep`
  - II 版改為與 `write-2` 比較

#### 3.2.2 移除指定元素 / 壓縮非零：`two_pointer_writer_remove` / `two_pointer_writer_compact`

- 經典題：
  - [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
- 模式：
  - `if nums[read] != val: nums[write] = nums[read]; write++`
  - Move Zeroes：條件改為 `nums[read] != 0`，最後補零

---

### 3.3 快慢指針：`fast_slow_*`（Floyd Cycle / Midpoint）

#### 3.3.1 鏈表是否有環：`fast_slow_cycle_detect`

- 經典題：
  - [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
- 模式：
  - `slow = slow.next`，`fast = fast.next.next`
  - 若存在環 → 一定會在環內某點相遇
  - 若 `fast` 或 `fast.next` 為 `None` → 無環

#### 3.3.2 找環起點：`fast_slow_cycle_start`

- 經典題：
  - [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
- 模式：
  - 第一次相遇後，令一指針從 `head` 出發，另一留在相遇點
  - 兩者一次一步前進，再次相遇點即為環起點

#### 3.3.3 找中點 / 隱式環：`fast_slow_midpoint` / `fast_slow_implicit_cycle`

- 經典題：
  - [LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
  - [LeetCode 202 - Happy Number](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)
- 心法：
  - 中點：快指針走到尾，慢指針剛好在中間
  - 隱式環：數字透過「平方和」轉換形成鏈 → 用同樣 cycle detect

---

### 3.4 Partition / 荷蘭國旗：`dutch_flag_partition` & `two_way_partition`

- 經典題：
  - [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
  - [LeetCode 905 - Sort Array By Parity](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
  - [LeetCode 922 - Sort Array By Parity II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
  - [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)（Quickselect 分區）
- 模式：
  - 三指針：`low`、`mid`、`high`
  - 根據 `nums[mid]` 與 pivot 的關係決定 swap 與指針移動

---

### 3.5 Merge 模式：`merge_two_sorted_*` / `merge_sorted_from_ends`

- 經典題：
  - [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - [LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - [LeetCode 977 - Squares of a Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)
  - [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)（進階：二分＋merge 思維）
- 模式：
  - 兩個排序序列 → 指針 `i, j` 比較當前元素，較小者輸出
  - 若從尾端開始（如題 88）可原地寫入

---

## 4️⃣ Data Structure & Algorithm 關聯視角 <!-- markmap: fold -->

### 4.1 常用資料結構 🔧

- `array` / `string`
  - 幾乎所有 sliding window / two pointers 題的基礎
- `hash_map` / `counter`
  - 字頻統計（LeetCode 3, 76, 340, 438, 567）
- `linked_list`
  - 快慢指針（LeetCode 141, 142, 876）
  - 原地反轉（`LinkedListInPlaceReversal`：如 [LeetCode 25 - Reverse Nodes in k-Group](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)）
- `queue` / `grid`
  - BFS 多源擴散（[LeetCode 994 - Rotting Oranges](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)）

---

### 4.2 演算法 / Paradigm 📚

- **Two Pointers / Sliding Window**：技術型技巧，常與排序 / hash 搭配
- **Greedy**：
  - 容器裝水（LeetCode 11）本質是貪心 + 對向指針
- **Divide & Conquer / Binary Search on Answer**：
  - [LeetCode 4](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)、[LeetCode 215](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py) 與 partition 結合
- **Backtracking**：
  - 不是雙指針，但在本圖譜中是對比參考（如 [LeetCode 51 - N-Queens](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)）

---

## 5️⃣ Roadmap：學習路徑建議 🔥 <!-- markmap: fold -->

### 5.1 Sliding Window Mastery Path（對應 `sliding_window_path`）

- [x] 基礎唯一字元：  
  - [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- [ ] 至多 K 種字元：  
  - [LeetCode 340 - Longest Substring with At Most K Distinct Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
- [ ] 最小覆蓋字串：  
  - [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
- [ ] 固定長 permutation / anagram：  
  - [LeetCode 567 - Permutation in String](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)  
  - [LeetCode 438 - Find All Anagrams in a String](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
- [ ] 數值和受限：  
  - [LeetCode 209 - Minimum Size Subarray Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)

---

### 5.2 Two Pointers Mastery Path（對應 `two_pointers_path`）

- 對向指針入門（排序 + 兩端）：
  - [ ] [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - [ ] [LeetCode 680 - Valid Palindrome II](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
  - [ ] [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- 3Sum 家族（multi-sum enumeration）：
  - [ ] [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
  - [ ] [LeetCode 16 - 3Sum Closest](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
- 同向讀寫（in-place modification）：
  - [ ] [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - [ ] [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - [ ] [LeetCode 80 - Remove Duplicates from Sorted Array II](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
  - [ ] [LeetCode 283 - Move Zeroes](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
- Partition / 荷蘭國旗：
  - [ ] [LeetCode 75 - Sort Colors](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
  - [ ] [LeetCode 905 - Sort Array By Parity](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
  - [ ] [LeetCode 922 - Sort Array By Parity II](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
  - [ ] [LeetCode 215 - Kth Largest Element in an Array](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
- Merge 模式：
  - [ ] [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - [ ] [LeetCode 88 - Merge Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - [ ] [LeetCode 977 - Squares of a Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)
- 快慢指針：
  - [ ] [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - [ ] [LeetCode 142 - Linked List Cycle II](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - [ ] [LeetCode 202 - Happy Number](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)
  - [ ] [LeetCode 876 - Middle of the Linked List](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)

---

## 6️⃣ 面試實戰視角：如何在考場快速判斷用哪個 Pattern？ ⚡ <!-- markmap: fold -->

### 6.1 決策流程（Sliding Window）

```text
答案是否是「連續子陣列 / 子字串」？
├─ 否 → 先考慮 DP / 組合 / 回溯
└─ 是 → 視窗屬性是？
        ├─ 長度固定？→ 固定長滑動視窗（如 567, 438）
        └─ 長度可變：
             ├─ 想「最長」？→ 視窗擴張，違規才收縮（3, 340）
             └─ 想「最短」？→ 先擴張到合法，再極限收縮（76, 209）
```

### 6.2 決策流程（Two Pointers）

```text
資料是否已排序（或可以排序）？
├─ 是：
│   ├─ 找 pair / k-sum → 對向指針（11, 15, 16）
│   ├─ 原地刪除/去重 → 同向讀寫（26, 27, 80, 283）
│   ├─ 分區 / 荷蘭國旗 → Partition（75, 905, 922, 215）
│   └─ 合併兩序列 → Merge（21, 88, 977）
└─ 否：
    ├─ 是鏈表？→ 快慢指針（141, 142, 876）
    └─ 其他 → 考慮 hash / heap / BFS / DP 等
```

---

## 7️⃣ 題目難度 & 面試熱門度標記 <!-- markmap: fold -->

- 難度標記（依 `difficulties`）：
  - 🟢 **Easy**
  - 🟠 **Medium**
  - 🔴 **Hard**
- 典型高頻清單（同時出現在 NeetCode 150 / Blind 75 / Top 100）：
  - 🟠 [LeetCode 1 - Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)（雖多用 hash，但可練對向指針版本）
  - 🟠 [LeetCode 3 - Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - 🟠 [LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - 🟠 [LeetCode 15 - 3Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
  - 🟢 [LeetCode 21 - Merge Two Sorted Lists](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - 🟢 [LeetCode 26 - Remove Duplicates from Sorted Array](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)
  - 🟢 [LeetCode 27 - Remove Element](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
  - 🟢 [LeetCode 125 - Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - 🟢 [LeetCode 141 - Linked List Cycle](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - 🔴 [LeetCode 76 - Minimum Window Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - 🔴 [LeetCode 4 - Median of Two Sorted Arrays](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)

---

## 8️⃣ 實作模板速查（Python） <!-- markmap: fold -->

### 8.1 滑動視窗：最大化視窗長度

```python
def maximize_window(seq):
    left = 0
    state = {}
    best = 0

    for right, x in enumerate(seq):
        add(state, x)
        while not is_valid(state):  # 視題目定義
            remove(state, seq[left])
            left += 1
        best = max(best, right - left + 1)

    return best
```

### 8.2 滑動視窗：最小化視窗長度

```python
def minimize_window(seq):
    left = 0
    state = {}
    best = float("inf")

    for right, x in enumerate(seq):
        add(state, x)
        while is_valid(state):
            best = min(best, right - left + 1)
            remove(state, seq[left])
            left += 1

    return best if best != float("inf") else 0
```

### 8.3 對向指針

```python
def two_end(arr):
    left, right = 0, len(arr) - 1
    ans = init_answer()

    while left < right:
        cur = evaluate(arr, left, right)
        ans = update(ans, cur, left, right)

        if move_left(cur):
            left += 1
        else:
            right -= 1

    return ans
```

### 8.4 讀寫指針（原地修改）

```python
def reader_writer(nums, keep):
    write = 0
    for read in range(len(nums)):
        if keep(nums, read, write):
            nums[write] = nums[read]
            write += 1
    return write
```

---

> 建議使用方式：  
> 1. 先沿著 Roadmap 把勾選框題目刷一輪  
> 2. 每做完一題，回到本圖譜對照「所屬 Pattern + API Kernel」  
> 3. 嘗試用統一模板重寫一次 → 形成可遷移的解題套路
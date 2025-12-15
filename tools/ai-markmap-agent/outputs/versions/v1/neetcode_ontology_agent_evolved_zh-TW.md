---
title: LeetCode 知識圖譜心智圖（核心模式 → API Kernels → 題目）🎯
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
---

## 如何使用這張地圖 📚
- **目標**：學會*可轉移的核心內核*（API）→ 辨識*模式* → 解出*題目*
- **定義**
  - **Kernel** = 可重用的程式碼樣板 / API
  - **Pattern** = 不變量 + 狀態選擇（Kernel 的特化）
  - **Family** = 共享同一（或多個）模式的一組題目
- **進度追蹤**
  - [ ] 每個 kernel 做 1 題（廣度）
  - [ ] 每個 kernel 做 3 題（深度）
  - [ ] 20 分鐘內從零重解「錨點」題 ⚡

## Router（決策指南）🧭
- 連續子字串/子陣列且帶限制 → **SubstringSlidingWindow**
- 已排序陣列 + 單調目標 / 對稱性質 → **TwoPointersTraversal**
- 原地重新排序到不同桶/區域 → **TwoPointerPartition**
- 無權重格狀/圖上的「最少時間/步數」 → **GridBFSMultiSource**（或 TreeTraversalBFS）
- 「第 K 大 / topK / 中位數 / 串流」→ **HeapTopK** / **KWayMerge**
- 答案空間的單調可行性 / 邊界索引 → **BinarySearchBoundary**
- 需要區間計數 / 子陣列總和目標 → **PrefixSumRangeQuery**
- 下一個較大/較小 / 直方圖面積 → **MonotonicStack**
- 連通性 / 連通分量 → **UnionFindConnectivity**
- 階層結構走訪 → **TreeTraversalDFS/BFS**
- DAG 前置條件 → **TopologicalSort**
- 序列/區間上的最佳子結構 → **DPSequence/DPInterval**

## 圖例（優先級標籤）🧾
- 🔥 必懂
- ⭐ 常見
- 🧊 加分

## Kernel 索引（你應該內化的「API」）🔥
- PrefixSumRangeQuery
- TwoPointersTraversal
- SubstringSlidingWindow
- BinarySearchBoundary
- TreeTraversalDFS + TreeTraversalBFS
- GridBFSMultiSource
- HeapTopK
- MonotonicStack
- MergeSortedSequences + KWayMerge
- BacktrackingExploration
- TwoPointerPartition
- FastSlowPointers
- UnionFindConnectivity
- TopologicalSort
- DPSequence + DPInterval
- TriePrefixSearch *(在本體中；未由提供的題目作為錨點)*

---

## 陷阱 & 檢查清單（可重用）✅
- **滑動視窗**
  - Off-by-one：包含式 `[L..R]` vs 半開區間 `[L, R)`；在視窗合法後再更新答案
  - 合法性必須能在每次移動以 $O(1)$ 維持（避免每一步重新掃描對應表/字母表）
  - 「合法時持續收縮」需要單調性（例如總和需要非負數）
- **雙指標 / 分割**
  - 終止條件：`while L < R` vs `<=`；確保每個分支都會前進
  - 重複值處理：在正確的指標與正確的時機跳過重複
  - 穩定性：read/write 壓縮是穩定的；以 swap 為主的分割通常不穩定
- **二分搜尋**
  - 使用**半開不變式**（`[lo, hi)`）並避免無限迴圈（`mid = lo + (hi-lo)//2`）
  - 有意識地選 `first_true` vs `last_true`；確認判定式的單調性
  - 溢位/哨兵：`mid-1`, `mid+1` 周邊邊界、空陣列
- **BFS**
  - **入佇列時就標記已拜訪**，避免重複入佇列
  - 層數計算：需要「分鐘/步數」時，以分層方式處理 BFS
  - 多源初始化：BFS 迴圈前先把所有來源入佇列；追蹤剩餘目標
- **回溯法**
  - 「取消選擇」是必要的（避免殘留標記）：回傳時復原每個變更
  - 剪枝必須安全（不要用之後可能被補足的片段資訊來剪枝）
  - 複製 vs 修改：除非必要，避免複製整條路徑（push/pop 節奏）
- **鏈結串列**
  - 用 dummy head 簡化 head 變更
  - 重新接線前先保留 `next` 指標
  - 分組邊界：k-group 反轉前先確認真的有 `k` 個節點
- **Quickselect / heaps**
  - Quickselect 最壞情況 $O(n^2)$，除非隨機化/median-of-medians
  - 重複值：三向分割可簡化重複 pivot 值的處理
  - 串流/大型輸入：通常偏好 heap

---

## 反向索引（題目 → Kernel → Pattern → 不變量）🔎
- 🔥 [LeetCode 1](https://leetcode.com/problems/two-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
- 🔥 [LeetCode 2](https://leetcode.com/problems/add-two-numbers/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py)
- 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
- 🧊 [LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)
- ⭐ [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- 🧊 [LeetCode 16](https://leetcode.com/problems/3sum-closest/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
- 🔥 [LeetCode 21](https://leetcode.com/problems/merge-two-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
- 🔥 [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
- ⭐ [LeetCode 25](https://leetcode.com/problems/reverse-nodes-in-k-group/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- ⭐ [LeetCode 26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates_from_sorted_array.py)[0:write]` 保持唯一」
- ⭐ [LeetCode 27](https://leetcode.com/problems/remove-element/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0027_remove_element.py)
- ⭐ [LeetCode 39](https://leetcode.com/problems/combination-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
- ⭐ [LeetCode 40](https://leetcode.com/problems/combination-sum-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)
- ⭐ [LeetCode 46](https://leetcode.com/problems/permutations/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)[]；選未使用者」
- 🧊 [LeetCode 47](https://leetcode.com/problems/permutations-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)
- ⭐ [LeetCode 51](https://leetcode.com/problems/n-queens/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
- 🧊 [LeetCode 52](https://leetcode.com/problems/n-queens-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
- 🔥 [LeetCode 75](https://leetcode.com/problems/sort-colors/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
- 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
- ⭐ [LeetCode 77](https://leetcode.com/problems/combinations/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
- ⭐ [LeetCode 78](https://leetcode.com/problems/subsets/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
- ⭐ [LeetCode 79](https://leetcode.com/problems/word-search/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)
- 🧊 [LeetCode 80](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0080_remove_duplicates_from_sorted_array_ii.py)
- ⭐ [LeetCode 88](https://leetcode.com/problems/merge-sorted-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
- 🧊 [LeetCode 90](https://leetcode.com/problems/subsets-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)
- 🧊 [LeetCode 93](https://leetcode.com/problems/restore-ip-addresses/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)
- ⭐ [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
- ⭐ [LeetCode 131](https://leetcode.com/problems/palindrome-partitioning/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)
- ⭐ [LeetCode 141](https://leetcode.com/problems/linked-list-cycle/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
- ⭐ [LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
- ⭐ [LeetCode 202](https://leetcode.com/problems/happy-number/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)(n)；偵測環」
- ⭐ [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
- 🔥 [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
- 🧊 [LeetCode 216](https://leetcode.com/problems/combination-sum-iii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)
- ⭐ [LeetCode 283](https://leetcode.com/problems/move-zeroes/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0283_move_zeroes.py)
- 🧊 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
- ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
- ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
- ⭐ [LeetCode 680](https://leetcode.com/problems/valid-palindrome-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)
- ⭐ [LeetCode 876](https://leetcode.com/problems/middle-of-the-linked-list/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
- ⭐ [LeetCode 905](https://leetcode.com/problems/sort-array-by-parity/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
- 🧊 [LeetCode 922](https://leetcode.com/problems/sort-array-by-parity-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
- ⭐ [LeetCode 977](https://leetcode.com/problems/squares-of-a-sorted-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)
- 🔥 [LeetCode 994](https://leetcode.com/problems/rotting-oranges/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)

---

## 1) 雜湊 + 前綴和（PrefixSumRangeQuery）🧮
- **你會在哪裡看到它派上用場**
  - 記錄檔事件計數；頻率表；去重；「這個 key 看過了嗎？」
  - 子陣列分析（running total）；用差分做異常偵測
- **Kernel 迷你規格**
  - **簽章**：序列 `nums`；查詢如「計算符合條件的子陣列數」/「區間聚合」；輸出整數/計數/陣列
  - **必要不變量**：維護前綴聚合 `pref[i]` 與已見前綴狀態的對應表；使用如 `pref[j]-pref[i]=target` 的恆等式
  - **狀態模型**：累積前綴值；`hash_map` 從前綴值 → 次數（或最早索引）
  - **複雜度範圍**：通常時間 $O(n)$、空間 $O(n)$（雜湊表）；每步期望 $O(1)$
  - **失效模式 / 不適用情況**：浮點前綴；雜湊碰撞（理論上）；視窗內 min/max 更適合滑動視窗/單調佇列
- **複雜度樣板**
  - 時間期望 $O(n)$；空間 $O(n)$ 用於前綴對應表（若只保留少量聚合則可到 $O(1)$）
- **模式**
  - **雜湊表補數查找**（`hash_map_complement`）
    - 錨點：🔥 [LeetCode 1](https://leetcode.com/problems/two-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
    - 樣板
      - ```text
        seen = map()  // value -> index
        for i in [0..n-1]:
          x = nums[i]
          y = target - x
          if y in seen:
            return [seen[y], i]
          seen[x] = i
        return none
        ```
  - **前綴和 + 雜湊表計數**（`prefix_sum_subarray_sum`）
    - 錨點：🔥 [LeetCode 560](https://leetcode.com/problems/subarray-sum-equals-k/description/)(不在提供的解題清單中)*
    - 樣板
      - ```text
        count = 0
        pref = 0
        freq = map(); freq[0] = 1
        for x in nums:
          pref += x
          count += freq.get(pref - k, 0)
          freq[pref] = freq.get(pref, 0) + 1
        return count
        ```
- **常見組合**
  - PrefixSumRangeQuery + MonotonicStack（區間貢獻 / 子陣列 min-max 計數）
  - PrefixSumRangeQuery + BinarySearchBoundary（以前綴為基礎的可行性檢查）
- **常見面試陷阱**
  - 忘記 `freq[0]=1` 的基底情況（「從 0 開始的子陣列」）
  - 把「最早索引」與「次數」用錯（視題目而定）

---

## 2) 雙指標走訪（TwoPointersTraversal）👯
- **你會在哪裡看到它派上用場**
  - 已排序陣列上的線性時間掃描；原地壓縮/過濾流水線
  - 文字正規化與對稱檢查（類回文驗證）
- **Kernel 迷你規格**
  - **簽章**：陣列/字串 `A`；輸出依需求（max/min、布林、索引、修改後的陣列）
  - **必要不變量**：每次移動後，被丟棄區間不可能含有比剩餘區間（或已紀錄答案）更好/更合法的解
  - **狀態模型**：指標（`L`,`R`）或（`read`,`write`）；可選的計數器用於限制/重複值
  - **複雜度範圍**：指標單調移動帶來 $O(n)$ 時間；額外空間 $O(1)$
  - **失效模式 / 不適用情況**：需要單調結構（已排序/對稱）或可保留可行性的論證；否則用雜湊/動態規劃
- **複雜度樣板**
  - 時間 $O(n)$；額外空間 $O(1)$
- **心智模型**：每一步移動都在*證明*被排除的區間不可能包含答案
- **主要證明模式（安全引理）**
  - 「每一步選擇一個能保證最優解仍存在於剩餘區間的指標移動；等價地，證明被丟棄的索引不可能參與任何比目前最佳更好的解。」
  - 例（[LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)）：若 `height[L] ≤ height[R]`，任何使用 `L` 且寬度更小的容器，除非限制高度變大，否則不可能超過當前面積 ⇒ `L++`。
- **子家族**
  - **對向指標**（已排序/對稱的最佳化）
    - 最大化目標
      - ⭐ [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)(移動較短邊)*
    - 回文驗證
      - ⭐ [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
      - ⭐ [LeetCode 680](https://leetcode.com/problems/valid-palindrome-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0680_valid_palindrome_ii.py)(一次跳過分支)*
  - **已排序陣列上的去重 + 逐一產生**
    - 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)(外層 i + 內層 L/R + 跳過重複)*
    - 🧊 [LeetCode 16](https://leetcode.com/problems/3sum-closest/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0016_3sum_closest.py)
  - **雜湊表查找（單趟）**
    - 🔥 [LeetCode 1](https://leetcode.com/problems/two-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
    - 註：雙指標需要**已排序輸入**（或先排序），會改變複雜度以及索引 vs 值的權衡。典型的對向指標版本是 **[LeetCode 167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/)(不在提供的解題清單中)*。
- **Pattern ID 對照（pattern_id → 子家族）**
  - `two_pointer_opposite_maximize` → 對向指標 → 最大化目標
  - `two_pointer_opposite_palindrome` → 對向指標 → 回文驗證
  - `two_pointer_three_sum` → 已排序陣列上的去重 + 逐一產生
  - `hash_map_complement` → 雜湊表查找（單趟）
- **快速不變量表**
  - | Pattern | Invariant | Typical problems |
    |---------|-----------|------------------|
    | Opposite | 在安全引理下，答案在 `[L..R]` | ⭐ [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
    | Sorted enumeration | 不輸出重複的 tuple | 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- **常見組合**
  - TwoPointersTraversal + BinarySearchBoundary（兩層搜尋：固定一端指標，二分搜尋另一端）
  - TwoPointersTraversal + PrefixSumRangeQuery（先過濾再做前綴分析）
- **常見面試陷阱（例）**
  - 重複值：3Sum 太早/太晚跳過重複會漏解或重複解
  - 終止條件：`<=` vs `<` 會造成無限迴圈或重複處理
  - 穩定 vs 不穩定：需要保留相對順序時，壓縮必須是穩定的

---

## 3) 滑動視窗（SubstringSlidingWindow）🪟
- **你會在哪裡看到它派上用場**
  - 速率限制視窗；事件串流上的移動聚合/特徵
  - 記錄檔掃描異常子字串；token 頻率視窗
- **Kernel 迷你規格**
  - **簽章**：序列 `s`/`nums`，可選參數 `k`/`target`；輸出 max/min 長度、布林或索引
  - **必要不變量**：維護視窗狀態，使得判定式 `Valid(L,R)` 能被增量檢查/更新
  - **狀態模型**：指標 `L ≤ R`；計數（`freq`, `need/have`）、distinct 計數器、總和；可選 `last_seen_index`
  - **複雜度範圍**：`R` 恰好增加 `n` 次；`L` 單調不遞減且最多增加 `n` 次 ⇒ 指標總移動 $O(n)$。若狀態更新/查詢為 $O(1)$，總工作量 $O(n)$（若每一步重新掃描字母表/狀態則可能到 $O(n·Σ)$）。
  - **失效模式 / 不適用情況**：判定式在移動 `L` 下不具單調性（例如含負數的總和）；合法性檢查每一步都需掃描大型狀態
- **複雜度樣板**
  - 時間 $O(n)$（單調指標 + $O(1)$ 更新）；空間 $O(Σ)$ 用於計數（或 $O(k)$ 個 distinct key）
- **狀態選擇**
  - `last_seen_index` 對應表（jump-L 最佳化）
  - `freq` 對應表 + `distinct_count`
  - `need/have` 對應表 + `satisfied/required`
  - 數值 `window_sum`
- **模式比較表**
  - | Problem | Invariant | State | Window Size | Goal |
    |---------|-----------|-------|-------------|------|
    | 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
    | 🧊 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
    | 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
    | ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
    | ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
    | ⭐ [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
- **模式**
  - **唯一視窗**（`sliding_window_unique`）
    - 錨點：🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)(學 jump-left)==
    - 兩種正確不變量/實作
      - 以頻率為主：維護 `s[L..R]` 中所有 `c` 都滿足 `freq[c] ≤ 1`；違反時就 `L++` 並遞減 `freq`
      - last-seen 跳躍：維護 `L = max(L, last_seen[c]+1)` 使 `s[L..R]` 無重複  
        - 不變量（last-seen）：`L` 永遠等於「目前視窗內所有重複字元的 last-seen 最大索引」的 `+1`
    - 樣板（last-seen 跳躍）
      - ```text
        last = map(); L = 0; best = 0
        for R in [0..n-1]:
          c = s[R]
          if c in last:
            L = max(L, last[c] + 1)
          last[c] = R
          best = max(best, R - L + 1)
        return best
        ```
  - **最多 K 種 distinct**（`sliding_window_at_most_k_distinct`）
    - 錨點：🧊 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
    - 樣板
      - ```text
        freq = map(); distinct = 0; L = 0; best = 0
        for R in [0..n-1]:
          add s[R]; if freq[s[R]] becomes 1: distinct++
          while distinct > K:
            remove s[L]; if freq[s[L]] becomes 0: distinct--
            L++
          best = max(best, R - L + 1)
        return best
        ```
  - **頻率契約（不要混用）**
    - 警告：**涵蓋**（≥ need）是可變視窗的「合法就收縮」狀態機；**完全相符**（= need）是固定視窗狀態機。混用計數器/迴圈會出 bug。
    - **涵蓋契約（≥ need）**（`sliding_window_freq_cover`）
      - 最小化涵蓋：🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
      - 註：對 ASCII，陣列 `[128]/[256]` 比 dict 快；對 unicode/一般 token 需 dict。
      - 樣板
        - ```text
          need = counts(t); have = map(); satisfied = 0; required = number_of_keys(need)
          L = 0; best = none
          for R in [0..n-1]:
            add s[R] into have
            if s[R] in need and have[s[R]] == need[s[R]]: satisfied++
            while satisfied == required:
              update best using [L..R]
              if s[L] in need and have[s[L]] == need[s[L]]: satisfied--
              remove s[L] from have
              L++
          return best
          ```
    - **完全相符契約（= need）**（`sliding_window_fixed_size`）
      - 固定大小完全相符（存在）：⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
      - 固定大小完全相符（收集全部）：⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
      - 樣板
        - ```text
          need = counts(p); have = empty counts
          matched = 0; required = number_of_keys(need)
          L = 0
          for R in [0..n-1]:
            add s[R] into have; update matched if have hits need exactly
            if window_size > len(p):
              remove s[L] from have; update matched if crossing equality
              L++
            if window_size == len(p) and matched == required:
              record match (or return true)
          ```
  - **成本有界 / 總和限制**（`sliding_window_cost_bounded`）
    - 錨點：⭐ [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
    - 註：這種收縮視窗法要求所有數字皆為**非負**（如 [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)）。若有負數，合法性對 `L` 不具單調性，滑動視窗失效；改用前綴和 + 單調佇列 / 二分搜尋變體。
    - 樣板
      - ```text
        L = 0; sum = 0; best = +inf
        for R in [0..n-1]:
          sum += nums[R]
          while sum >= target:
            best = min(best, R - L + 1)
            sum -= nums[L]; L++
        return best if best != +inf else 0
        ```
- **常見組合**
  - SubstringSlidingWindow + HeapTopK（移動視窗內 top-k；串流分析）
  - SubstringSlidingWindow + PrefixSumRangeQuery（視窗化特徵抽取 + 下游計數）
- **常見面試陷阱**
  - 「最小化視窗」需要：**合法時用 while 反覆收縮**（不是只收縮一次）
  - 「完全相符」最適合：**固定視窗** + `matched` 計數器

---

## 4) 二分搜尋邊界（BinarySearchBoundary）🔎
- **你會在哪裡看到它派上用場**
  - Feature flag/上線控管：第一個出現回歸的版本；以可行性檢查做容量規劃
  - 閾值調參：在單調判定式下找最小可行參數
- **Kernel 迷你規格**
  - **簽章**：已排序陣列 `A` 或有序領域上的判定式 `P(x)`；輸出邊界索引/值
  - **必要不變量**：在單調判定式下，搜尋區間維持「答案存在於邊界內」
  - **狀態模型**：`lo, hi` 邊界；`mid`；判定式 `P(mid)`；可選 best-so-far
  - **複雜度範圍**：索引搜尋 $O(\log n)$ 次評估；答案空間（領域大小 `V`）$O(\log V)$
  - **失效模式 / 不適用情況**：判定式非單調；off-by-one 邊界；mid 不前進
- **複雜度樣板**
  - 時間 $O(\log n)$（索引）或 $O(\log V)$（答案空間）；空間 $O(1)$
- **邊界樣板**
  - `first_true`（`binary_search_first_true`）/ `lower_bound`
    - ```text
      // find smallest x in [lo, hi) with P(x) == true
      while lo < hi:
        mid = lo + (hi - lo)//2
        if P(mid): hi = mid
        else: lo = mid + 1
      return lo
      ```
  - `last_true`（`binary_search_last_true`）
    - ```text
      // find largest x in [lo, hi) with P(x) == true; return lo-1 if none
      while lo < hi:
        mid = lo + (hi - lo)//2
        if P(mid): lo = mid + 1
        else: hi = mid
      return lo - 1
      ```
  - `upper_bound`（第一個 `> key`）/ `lower_bound`（第一個 `≥ key`）心智模型
    -「選擇判定式從 false→true 翻轉的第一個索引。」
- **答案空間搜尋**（`binary_search_on_answer`）
  - 單調可行性檢查清單
    - 清楚定義 `feasible(x)`
    - 證明：若 `feasible(x)` 成立，則所有 `x' ≥ x`（或 ≤ x）也成立
    - 依需求選擇找最小可行 / 最大可行
  - 樣板（最小可行）
    - ```text
      lo = min_possible; hi = max_possible
      while lo < hi:
        mid = lo + (hi - lo)//2
        if feasible(mid): hi = mid
        else: lo = mid + 1
      return lo
      ```
  - 錨點
    - 🔥 [LeetCode 875](https://leetcode.com/problems/longest-mountain-in-array/description/)(不在提供的解題清單中)*
    - 🔥 [LeetCode 1011](https://leetcode.com/problems/flip-binary-tree-to-match-preorder-traversal/description/)(不在提供的解題清單中)*
- **旋轉陣列搜尋**（`binary_search_rotated`）
  - 錨點集合
    - 🔥 [LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/description/)(不在提供的解題清單中)*
    - 🔥 [LeetCode 153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/)(不在提供的解題清單中)*
  - 樣板
    - ```text
      lo = 0; hi = n-1
      while lo <= hi:
        mid = (lo + hi)//2
        if A[mid] == target: return mid
        if A[lo] <= A[mid]:  // left sorted
          if A[lo] <= target < A[mid]: hi = mid - 1
          else: lo = mid + 1
        else:               // right sorted
          if A[mid] < target <= A[hi]: lo = mid + 1
          else: hi = mid - 1
      return -1
      ```
- **分割索引上的二分搜尋（進階混合）**
  - 🧊 [LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0004_median_of_two_sorted_arrays.py)(依數量分割不變量)==
    - 不變量：選 `i`（在 A）、`j`（在 B），使左側元素數為 `(m+n+1)//2` 且 `maxLeft ≤ minRight`
- **常見組合**
  - BinarySearchBoundary + GridBFSMultiSource（外層二分時間；內層以 BFS/DFS 驗證可行性）
  - BinarySearchBoundary + HeapTopK（搜尋門檻；用 heap/選擇法計數驗證）
- **常見面試陷阱**
  - 半開區間用錯導致無限迴圈
  - 判定式依賴可變的全域狀態（每次檢查都必須重設）

---

## 5) 樹走訪（TreeTraversalDFS + TreeTraversalBFS）🌳
- **你會在哪裡看到它派上用場**
  - 階層結構：組織圖、檔案系統樹、DOM/AST 走訪
  - 聚合：自底向上計算指標；自頂向下驗證限制
- **Kernel 迷你規格**
  - **簽章**：`root` 節點；輸出聚合值、布林、每層列表或路徑型結果
  - **必要不變量**：DFS 保留呼叫堆疊路徑；BFS 以非遞減深度處理節點
  - **狀態模型**：遞迴堆疊（DFS）/ 佇列（BFS）；可選 parent 指標
  - **複雜度範圍**：每個節點走訪一次 ⇒ 時間 $O(n)$；空間 DFS $O(h)$ / BFS $O(w)$
  - **失效模式 / 不適用情況**：遞迴深度溢位（改用迭代）；漏掉 base case / null 檢查
- **複雜度樣板**
  - 時間 $O(n)$；空間 $O(h)$（DFS）或 $O(w)$（BFS）
- **模式**
  - **DFS（遞迴）**（`tree_dfs_recursive`）
    - 錨點
      - 🔥 [LeetCode 104](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/)(不在提供的解題清單中)*
      - 🔥 [LeetCode 236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/description/)(不在提供的解題清單中)*
    - 樣板
      - ```text
        def dfs(node):
          if node == null: return base
          left = dfs(node.left)
          right = dfs(node.right)
          return combine(node, left, right)
        return dfs(root)
        ```
  - **BFS（層序）**（`bfs_level_order`）
    - 錨點：🔥 [LeetCode 102](https://leetcode.com/problems/binary-tree-level-order-traversal/description/)(不在提供的解題清單中)*
    - 樣板
      - ```text
        q = queue([root]); ans = []
        while q not empty:
          level = []
          repeat size(q) times:
            node = pop_front(q)
            level.append(node.val)
            push children
          ans.append(level)
        return ans
        ```
- **常見組合**
  - TreeTraversalDFS + BacktrackingExploration（帶限制的路徑逐一產生）
  - TreeTraversalBFS + BinarySearchBoundary（搜尋滿足判定式的最小深度）
- **常見面試陷阱**
  - 遞迴忘記 return/傳遞值
  - 用 BFS 卻忘記固定每層 size（層級混在一起）

---

<!-- markmap: fold -->
## 6) 圖 BFS/DFS + 格狀 BFS（GridBFSMultiSource）🌊
- **你會在哪裡看到它派上用場**
  - 多區域的傳播/延遲；最短時間擴散模擬
  - 格狀地圖與多源距離轉換
- **Kernel 迷你規格**
  - **簽章**：格子 `m×n`，含來源/目標/障礙；輸出最短時間/步數或最終狀態
  - **必要不變量**：層序擴張保證在無權重圖中第一次到達某格子即為最短路徑
  - **狀態模型**：前沿佇列；已拜訪集合/標記；距離/時間陣列或原地時間戳
  - **複雜度範圍**：每個格子最多入佇列/出佇列一次 ⇒ 時間 $O(mn)$、空間 $O(mn)$
  - **失效模式 / 不適用情況**：有權重邊（用 Dijkstra）；太晚標記已拜訪導致多次入佇列
- **複雜度樣板**
  - 時間 $O(V+E)$（格狀：$O(mn)$）；空間 $O(V)$
- **核心想法**：把所有來源都推入，逐層擴張（時間 = 層數）
- **不變量（層序最短）**
  - 當某格子被出佇列時，其紀錄的時間/距離在所有從任一來源的路徑中最小（無權重邊）。層序走訪對應距離遞增。
  - **入佇列時就標記已拜訪**（不是出佇列時）以避免重複入佇列。
- **錨點**
  - 🔥 [LeetCode 994](https://leetcode.com/problems/rotting-oranges/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0994_rotting_oranges.py)
- **工程檢查清單**
  - 佇列初始化時放入所有來源
  - 計數新鮮/剩餘目標
  - 以分層 BFS 計算分鐘數
- **常見組合**
  - GridBFSMultiSource + BinarySearchBoundary（時間可行性變體）
  - GridBFSMultiSource + UnionFindConnectivity（連通性 vs 最短時間的權衡）
- **常見面試陷阱（例）**
  - 忘記把所有初始來源入佇列（多源正確性）
  - 分鐘計數錯誤（每層 +1，不是每個節點 +1）

---

## 7) Heap / 選擇（HeapTopK + Quickselect）⛰️
- **你會在哪裡看到它派上用場**
  - 熱門查詢、遙測 heavy hitter、優先級排程
  - 串流中位數/百分位（雙 heap 中位數；或近似替代）
- **Kernel 迷你規格**
  - **簽章**：串流/陣列 `nums`，參數 `k`；輸出第 k / top-k / 中位數
  - **必要不變量**：heap 維持頂端為極值；大小限制編碼「保留集合」
  - **狀態模型**：大小為 `k` 的 min-heap（保留最大的 top-k）或 max-heap 類比；中位數用兩個 heap 分割下半/上半
  - **複雜度範圍**：每次插入對 bounded heap 為 $O(\log k)$；建 heap $O(n)$ 後 pop 為 $O(k\log n)$ 或增量式處理
  - **失效模式 / 不適用情況**：若需要完整排序；若 k≈n 且排序更單純；在記憶體內 quickselect 可能更快
- **複雜度樣板**
  - Heap top-k：時間 $O(n \log k)$、空間 $O(k)$；Quickselect：平均 $O(n)$、最壞 $O(n^2)$（除非隨機化）
- **第 k 個元素**
  - Quickselect / 分割：🔥 [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
    - 註：平均 $O(n)$，最壞 $O(n^2)$（除非隨機化/median-of-medians）；額外空間 $O(1)$（原地）。
  - Heap 替代方案（尤其是串流 / 穩定性）：🔥 [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)
    - 註：時間 $O(n \log k)$、空間 $O(k)$；更適合串流且當 $k \ll n$。
- **決策備註**
  - **[LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0215_kth_largest_element_in_an_array.py)**：Quickselect（平均 $O(n)$；需防最壞）vs Heap（$O(n\log k)$；對串流友善）
- **常見組合**
  - HeapTopK + SubstringSlidingWindow（移動視窗內 top-k）
  - HeapTopK + KWayMerge（合併多串流並維持 top-k）
- **常見面試陷阱（例）**
  - quickselect 未隨機化 pivot（對抗性最壞情況）
  - pivot 周邊重複值處理錯（必要時用三向分割）

---

## 8) 單調堆疊（MonotonicStack）🧱
- **你會在哪裡看到它派上用場**
  - 監控中的 next-greater 查詢；天際線/區間支配計算
  - 直方圖類容量/面積計算
- **Kernel 迷你規格**
  - **簽章**：陣列 `A`；輸出下一個較大/較小的索引/值或最大面積
  - **必要不變量**：堆疊維持單調的值序（或索引），使每個元素只會 push/pop 一次
  - **狀態模型**：索引堆疊；尾端 flush 用的哨兵索引
  - **複雜度範圍**：每個索引最多 push/pop 一次 ⇒ 時間 $O(n)$；堆疊空間 $O(n)$
  - **失效模式 / 不適用情況**：嚴格 vs 非嚴格不等號用錯；忘了哨兵/flush；重複值處理
- **複雜度樣板**
  - 時間攤銷 $O(n)$；空間 $O(n)$
- **錨點**
  - 🔥 [LeetCode 739](https://leetcode.com/problems/daily-temperatures/description/)(不在提供的解題清單中)*
  - 🔥 [LeetCode 84](https://leetcode.com/problems/largest-rectangle-in-histogram/description/)(不在提供的解題清單中)*
- **樣板**
  - 下一個較大元素
    - ```text
      st = empty stack of indices
      for i in [0..n-1]:
        while st not empty and A[st.top] < A[i]:
          j = st.pop()
          ans[j] = i
        st.push(i)
      ```
  - 直方圖最大矩形（含哨兵）
    - ```text
      st = empty stack
      for i in [0..n]:               // treat A[n]=0 sentinel
        cur = A[i] if i<n else 0
        while st not empty and A[st.top] > cur:
          h = A[st.pop()]
          left = st.top if st not empty else -1
          width = i - left - 1
          best = max(best, h * width)
        st.push(i)
      return best
      ```
- **常見組合**
  - MonotonicStack + PrefixSumRangeQuery（區間貢獻 / 子陣列最小值/最大值總和）
- **常見面試陷阱**
  - `<` vs `<=` 會改變重複值行為；必須符合題目定義

---

## 9) 回溯探索（BacktrackingExploration）🧠
- **你會在哪裡看到它派上用場**
  - 約束求解器、組態搜尋、規則式產生（小型領域）
  - 用剪枝逐一產生候選解
- **Kernel 迷你規格**
  - **簽章**：候選集合/選項；輸出解列表或解數
  - **必要不變量**：狀態必須精確對應目前路徑（沒有「殘留標記」）
  - **狀態模型**：遞迴堆疊；`path`；`used[]` 或 `start` 索引；限制集合（cols/diags）
  - **複雜度範圍**：時間 $O(\text{branch}^{\text{depth}})$；遞迴深度 $O(\text{depth})$；輸出大小是下界
  - **失效模式 / 不適用情況**：大且幾乎無限制的搜尋空間（需 DP/貪婪法）；忘記回復；過度複製
- **複雜度樣板**
  - 時間 $O(\text{branch}^{\text{depth}})$（常由輸出主導）；空間 $O(\text{depth})$ + 輸出
- **核心節奏**：**選擇 → 探索 → 取消選擇**
- **不變量**：狀態精確等同於目前路徑（沒有「殘留標記」）
- **決策樹形狀**
  - **排列**（used[]）
    - ⭐ [LeetCode 46](https://leetcode.com/problems/permutations/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
    - 含重複（排序 + 同層跳過）：🧊 [LeetCode 47](https://leetcode.com/problems/permutations-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0047_permutations_ii.py)
    - 樣板
      - ```text
        used = [false]*n; path = []
        def dfs():
          if len(path) == n: emit(path); return
          for i in [0..n-1]:
            if used[i]: continue
            used[i] = true; path.push(A[i])
            dfs()
            path.pop(); used[i] = false
        dfs()
        ```
  - **子集合**（start index）
    - ⭐ [LeetCode 78](https://leetcode.com/problems/subsets/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
    - 含重複（排序 + 同層跳過）：🧊 [LeetCode 90](https://leetcode.com/problems/subsets-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0090_subsets_ii.py)
    - 樣板
      - ```text
        path = []
        def dfs(i):
          emit(path)
          for j in [i..n-1]:
            if j>i and A[j]==A[j-1]: continue
            path.push(A[j])
            dfs(j+1)
            path.pop()
        dfs(0)
        ```
  - **組合 / 固定大小**（start index + 長度界限）
    - ⭐ [LeetCode 77](https://leetcode.com/problems/combinations/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0077_combinations.py)
    - 樣板
      - ```text
        path=[]
        def dfs(start):
          if len(path)==k: emit(path); return
          for x in [start..N]:
            path.push(x)
            dfs(x+1)
            path.pop()
        dfs(1)
        ```
  - **目標總和搜尋**
    - 可重用：⭐ [LeetCode 39](https://leetcode.com/problems/combination-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
    - 不可重用 + 含重複：⭐ [LeetCode 40](https://leetcode.com/problems/combination-sum-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0040_combination_sum_ii.py)
    - 固定數量 + 有界範圍：🧊 [LeetCode 216](https://leetcode.com/problems/combination-sum-iii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0216_combination_sum_iii.py)
    - 樣板（允許重用）
      - ```text
        path=[]
        def dfs(start, remain):
          if remain==0: emit(path); return
          for i in [start..n-1]:
            if A[i] > remain: continue/prune if sorted
            path.push(A[i])
            dfs(i, remain - A[i])   // reuse allowed
            path.pop()
        dfs(0, target)
        ```
  - **約束滿足**
    - ⭐ [LeetCode 51](https://leetcode.com/problems/n-queens/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
    - 🧊 [LeetCode 52](https://leetcode.com/problems/n-queens-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0052_n_queens_ii.py)
    - 樣板
      - ```text
        cols=set(); d1=set(); d2=set()
        def dfs(r):
          if r==n: emit(); return
          for c in [0..n-1]:
            if c in cols or (r-c) in d1 or (r+c) in d2: continue
            add(c,r-c,r+c)
            dfs(r+1)
            remove(c,r-c,r+c)
        dfs(0)
        ```
  - **字串切分**
    - 🧊 [LeetCode 93](https://leetcode.com/problems/restore-ip-addresses/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0093_restore_ip_addresses.py)(4 段 + 長度界限剪枝)*
    - ⭐ [LeetCode 131](https://leetcode.com/problems/palindrome-partitioning/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)(可選用 DP 預先計算回文判定)*
    - 決策備註：**[LeetCode 131](https://leetcode.com/problems/palindrome-partitioning/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0131_palindrome_partitioning.py)** 可預先計算回文 DP $O(n^2)$ 以降低重複檢查；較適合較長字串。
    - 樣板
      - ```text
        path=[]
        def dfs(i):
          if i==n: emit(path); return
          for j in [i..n-1]:
            if not is_valid(i,j): continue
            path.push(s[i..j])
            dfs(j+1)
            path.pop()
        dfs(0)
        ```
  - **格狀路徑搜尋**
    - ⭐ [LeetCode 79](https://leetcode.com/problems/word-search/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)(標記/取消標記 visited)*
    - 樣板
      - ```text
        def dfs(r,c,idx):
          if idx==len(word): return true
          if out_of_bounds or visited or grid[r][c]!=word[idx]: return false
          visited[r][c]=true
          ok = any(dfs(nr,nc,idx+1) for neighbors)
          visited[r][c]=false
          return ok
        ```
- **常見組合**
  - BacktrackingExploration + DP memo（自頂向下快取）用於 segmentation/partitioning
  - BacktrackingExploration + BinarySearchBoundary（搜尋參數；小領域用回溯驗證）
- **常見面試陷阱**
  - 未回復狀態（visited/集合/path）
  - 每層遞迴都過度複製列表（時間/記憶體爆炸）

---

## 10) 鏈結串列操作（指標手術）🔧
- **你會在哪裡看到它派上用場**
  - 原地轉換；串流流水線；指標安全的重新接線
- **Kernel 迷你規格**
  - **簽章**：鏈結串列的 `head`；輸出新 head 或修改後的串列
  - **必要不變量**：保持可達性；重新接線時永遠不丟失剩餘串列（`next`）
  - **狀態模型**：`prev/curr/next`、dummy head、分組邊界
  - **複雜度範圍**：通常時間 $O(n)$；額外空間 $O(1)$
  - **失效模式 / 不適用情況**：忘記先存 `next`；head 變更處理錯；分組邊界錯
- **複雜度樣板**
  - 時間 $O(n)$；額外空間 $O(1)$
- 串列算術
  - ⭐ [LeetCode 2](https://leetcode.com/problems/add-two-numbers/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0002_add_two_numbers.py)
- 分組原地反轉
  - ⭐ [LeetCode 25](https://leetcode.com/problems/reverse-nodes-in-k-group/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0025_reverse_nodes_in_k_group.py)
- **常見組合**
  - 鏈結串列操作 + HeapTopK（依值串流節點）
- **常見面試陷阱（例）**
  - 不用 dummy head（head 邊界處理複雜）
  - 反轉少於 `k` 個節點（必須先檢查是否足夠）

---

## 11) 分割（TwoPointerPartition）🚧
- **你會在哪裡看到它派上用場**
  - 原地分桶（旗標、類別）、quickselect 流水線、不穩定分割階段
- **Kernel 迷你規格**
  - **簽章**：陣列 `A`；輸出重排後陣列（原地）和/或 pivot 索引 / 分割邊界
  - **必要不變量**：維持互斥區域（好/壞/未知）並確保指標移動正確
  - **狀態模型**：分隔區域的指標（`low, mid, high` 或 `i, j`）；判定式 `good(x)`
  - **複雜度範圍**：時間 $O(n)$；額外空間 $O(1)$
  - **失效模式 / 不適用情況**：需要穩定性（用 read/write）；未知區域處理錯
- **複雜度樣板**
  - 時間 $O(n)$；空間 $O(1)$
- **關於穩定性的註記**
  - Writer 模式是**具穩定性的二區分割**；本節為多區/以 swap 為主（通常**不穩定**）。
- **模式**
  - **荷蘭國旗（三向分割）**（`dutch_flag_partition`）
    - 錨點：🔥 [LeetCode 75](https://leetcode.com/problems/sort-colors/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0075_sort_colors.py)
    - 迴圈不變量：維持  
      `A[0..low-1]=0`, `A[low..mid-1]=1`, `A[mid..high]=unknown`, `A[high+1..n-1]=2`。
    - 樣板
      - ```text
        low=0; mid=0; high=n-1
        while mid <= high:
          if A[mid]==0: swap(A[low],A[mid]); low++; mid++
          elif A[mid]==1: mid++
          else: swap(A[mid],A[high]); high--
        ```
  - **二向分割**（`two_way_partition`)
    - ⭐ [LeetCode 905](https://leetcode.com/problems/sort-array-by-parity/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0905_sort_array_by_parity.py)
    - 🧊 [LeetCode 922](https://leetcode.com/problems/sort-array-by-parity-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0922_sort_array_by_parity_ii.py)
    - 迴圈不變量：維持  
      `A[0..i-1]` 為「好」、`A[j+1..n-1]` 為「壞」、`i ≤ j` 為未知。
    - 樣板
      - ```text
        i=0; j=n-1
        while i <= j:
          if good(A[i]): i++
          elif not good(A[j]): j--
          else: swap(A[i],A[j]); i++; j--
        ```
- **常見組合**
  - TwoPointerPartition + Quickselect（選擇流程）
- **常見面試陷阱**
  - `mid <= high` 的 off-by-one（荷蘭國旗）
  - 對穩定性的錯誤假設（swap 分割會破壞相對順序）

---

## 12) 快慢指標（FastSlowPointers）🐢🐇
- **你會在哪裡看到它派上用場**
  - 偵測迭代過程的環；鏈結串列演算法的中點切分
- **Kernel 迷你規格**
  - **簽章**：鏈結串列 head 或函式 `f(x)`；輸出是否有環/環的起點或中點
  - **必要不變量**：fast 走 2 倍；若有環則會相遇；第二階段對齊到環入口
  - **狀態模型**：`slow`, `fast`；可選重設指標用於第二階段
  - **複雜度範圍**：時間 $O(n)$；空間 $O(1)$
  - **失效模式 / 不適用情況**：`fast` 與 `fast.next` 的 null 檢查；誤解第二階段證明
- **複雜度樣板**
  - 時間 $O(n)$；空間 $O(1)$
- **兩階段（Floyd）**
  - 階段 1：偵測環
  - 階段 2：找環起點
- **題目**
  - 偵測環：⭐ [LeetCode 141](https://leetcode.com/problems/linked-list-cycle/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0141_linked_list_cycle.py)
  - 找環起點：⭐ [LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0142_linked_list_cycle_ii.py)
  - 隱式環（函式迭代）：⭐ [LeetCode 202](https://leetcode.com/problems/happy-number/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0202_happy_number.py)
  - 中點：⭐ [LeetCode 876](https://leetcode.com/problems/middle-of-the-linked-list/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0876_middle_of_the_linked_list.py)
- **常見組合**
  - FastSlowPointers + MergeSortedSequences（切分串列再合併：串列 mergesort）
- **常見面試陷阱**
  - 走一步前未檢查 `fast`/`fast.next`
  - 回傳相遇點而非入口點（需要第二階段）

---

## 13) 合併已排序序列（MergeSortedSequences + KWayMerge）🔗
- **你會在哪裡看到它派上用場**
  - 合併已排序的記錄檔片段（LSM compaction）、外部排序、分片結果合併
- **Kernel 迷你規格**
  - **簽章**：兩個已排序序列（或 k 個序列）；輸出合併後的已排序序列
  - **必要不變量**：輸出前綴永遠是剩餘元素中的最小者；指標/heap 反映目前 heads
  - **狀態模型**：二路用雙指標；k 路用目前 head 的 min-heap
  - **複雜度範圍**：二路 $O(m+n)$；k 路 $O(N\log k)$；額外空間 $O(1)$ 到 $O(k)$
  - **失效模式 / 不適用情況**：輸入未排序；需要穩定 tie-handling 時忘記處理
- **複雜度樣板**
  - 二路合併 $O(m+n)$；k 路 heap 合併 $O(N\log k)$ 且 heap 空間 $O(k)$
- **兩個已排序串流（二指標）**
  - 鏈結串列合併：🔥 [LeetCode 21](https://leetcode.com/problems/merge-two-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0021_merge_two_sorted_lists.py)
  - 陣列合併（常從尾端）：⭐ [LeetCode 88](https://leetcode.com/problems/merge-sorted-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0088_merge_sorted_array.py)
  - 從尾端合併技巧：⭐ [LeetCode 977](https://leetcode.com/problems/squares-of-a-sorted-array/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0977_squares_of_a_sorted_array.py)
- **k 路合併**
  - Heap 版 $O(N \log k)$：🔥 [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - 分治法 $O(N \log k)$：🔥 [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)
  - 決策備註（[LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0023_merge_k_sorted_lists.py)）
    - Heap（較簡單、對串流友善、$O(k)$ 記憶體）vs 分治（資料都在記憶體時常數較小、通常更快）
- **常見組合**
  - KWayMerge + HeapTopK（合併多串流但只保留 top-k）
  - MergeSortedSequences + BinarySearchBoundary（在合併後的次序統計量上做分割/邊界搜尋）
- **常見面試陷阱**
  - 鏈結串列合併時弄丟原本指標（先存 `next`）
  - 尾端合併索引的 off-by-one

---

## 14) 並查集連通性（UnionFindConnectivity）🔌
- **你會在哪裡看到它派上用場**
  - 連通性分群、帳號/實體去重、網路連通分量
- **Kernel 迷你規格**
  - **簽章**：`n` 個節點 + 邊/關係；輸出連通分量數或合併後群組
  - **必要不變量**：`find(x)` 回傳代表元；`union(a,b)` 合併集合
  - **狀態模型**：`parent[]`、`rank/size[]` 搭配路徑壓縮
  - **複雜度範圍**：每次操作攤銷近 $O(1)$（$α(n)$）
  - **失效模式 / 不適用情況**：有向可達性/最短路徑（用 BFS/DFS）；忘記路徑壓縮
- **複雜度樣板**
  - 時間 $O((n+m)·α(n))$；空間 $O(n)$
- **錨點**
  - 🔥 [LeetCode 200](https://leetcode.com/problems/number-of-islands/description/)(不在提供的解題清單中)*
  - 🔥 [LeetCode 721](https://leetcode.com/problems/accounts-merge/description/)(不在提供的解題清單中)*
- **樣板**
  - ```text
    init parent[i]=i, size[i]=1
    def find(x):
      while x != parent[x]:
        parent[x] = parent[parent[x]]
        x = parent[x]
      return x
    def union(a,b):
      ra, rb = find(a), find(b)
      if ra==rb: return
      if size[ra] < size[rb]: swap
      parent[rb]=ra; size[ra]+=size[rb]
    ```
- **常見組合**
  - UnionFindConnectivity + 格狀走訪（把 2D 格子對應到 id）
- **常見面試陷阱**
  - 缺少 rank/size 合併 → 常數可能顯著變差

---

## 15) 拓樸排序（TopologicalSort）🧩
- **你會在哪裡看到它派上用場**
  - 建置系統、相依圖、課程先修、DAG 排程
- **Kernel 迷你規格**
  - **簽章**：含 `n` 個節點與邊的 DAG；輸出順序或是否可行
  - **必要不變量**：入度為 0 的節點可以安全地下一個輸出（Kahn）
  - **狀態模型**：入度陣列；零入度節點佇列
  - **複雜度範圍**：時間 $O(V+E)$；空間 $O(V+E)$
  - **失效模式 / 不適用情況**：有環（無法排序）；忘記遞減入度
- **複雜度樣板**
  - 時間 $O(V+E)$；空間 $O(V+E)$
- **錨點**
  - 🔥 [LeetCode 207](https://leetcode.com/problems/course-schedule/description/)(不在提供的解題清單中)*
- **樣板（Kahn）**
  - ```text
    build adj, indeg
    q = all nodes with indeg==0
    seen = 0
    while q not empty:
      u = pop(q); seen++
      for v in adj[u]:
        indeg[v]--
        if indeg[v]==0: push(q,v)
    return seen==n
    ```
- **常見組合**
  - TopologicalSort + DPSequence（依 topo order 做 DAG 最長路徑）
- **常見面試陷阱**
  - 用 DFS topo 卻漏了三色標記的環偵測

---

## 16) 動態規劃（DPSequence + DPInterval）🧠📈
- **你會在哪裡看到它派上用場**
  - 成本最佳化、排程、字串對齊、區間計分
- **Kernel 迷你規格**
  - **簽章**：序列/字串/區間；輸出最優值或重建結果
  - **必要不變量**：清楚定義狀態 `dp[...]` 的意義；轉移只使用更小的子問題
  - **狀態模型**：序列用 1D dp；區間/子字串用 2D dp
  - **複雜度範圍**：取決於狀態大小 × 轉移成本
  - **失效模式 / 不適用情況**：狀態不夠精簡（爆炸）；漏 base case；迭代順序錯
- **複雜度樣板**
  - 通常為 $O(\#states × \#transitions)$；空間 $O(\#states)$（常可最佳化）
- **錨點**
  - 🔥 [LeetCode 70](https://leetcode.com/problems/climbing-stairs/description/)(不在提供的解題清單中)*
  - 🔥 [LeetCode 300](https://leetcode.com/problems/longest-increasing-subsequence/description/)(不在提供的解題清單中)*
- **樣板**
  - 類 Fibonacci（`dp_fibonacci_style`）
    - ```text
      dp[0]=...; dp[1]=...
      for i in [2..n]:
        dp[i] = dp[i-1] + dp[i-2]   // example
      return dp[n]
      ```
  - 區間 DP 骨架（`dp_palindrome` / DPInterval）
    - ```text
      dp = 2D array n×n
      for len in [1..n]:
        for i in [0..n-len]:
          j = i + len - 1
          dp[i][j] = combine(dp smaller intervals, s[i], s[j])
      return dp[0][n-1]
      ```
- **常見組合**
  - DPInterval + BacktrackingExploration（DP 做快速合法性檢查；回溯逐一產生）
- **常見面試陷阱**
  - 用遞迴但不做 memo（TLE）
  - 區間相依的迭代順序錯

---

## 建議學習路徑（roadmap-style）🚀
- **滑動視窗精通**
  - [ ] 🔥 [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
  - [ ] 🧊 [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0340_longest_substring_with_at_most_k_distinct.py)
  - [ ] 🔥 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0076_minimum_window_substring.py)
  - [ ] ⭐ [LeetCode 567](https://leetcode.com/problems/permutation-in-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0567_permutation_in_string.py)
  - [ ] ⭐ [LeetCode 438](https://leetcode.com/problems/find-all-anagrams-in-a-string/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0438_find_all_anagrams_in_a_string.py)
  - [ ] ⭐ [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0209_minimum_size_subarray_sum.py)
- **雙指標精通**
  - [ ] ⭐ [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
  - [ ] ⭐ [LeetCode 125](https://leetcode.com/problems/valid-palindrome/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py)
  - [ ] 🔥 [LeetCode 15](https://leetcode.com/problems/3sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0015_3sum.py)
- **回溯法精通**
  - [ ] ⭐ [LeetCode 78](https://leetcode.com/problems/subsets/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0078_subsets.py)
  - [ ] ⭐ [LeetCode 46](https://leetcode.com/problems/permutations/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0046_permutations.py)
  - [ ] ⭐ [LeetCode 39](https://leetcode.com/problems/combination-sum/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0039_combination_sum.py)
  - [ ] ⭐ [LeetCode 51](https://leetcode.com/problems/n-queens/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0051_n_queens.py)
  - [ ] ⭐ [LeetCode 79](https://leetcode.com/problems/word-search/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)

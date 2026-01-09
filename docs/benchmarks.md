# Benchmark Results

This document contains benchmark data for all multi-solution problems in the NeetCode Practice Framework.

## Large N Spotlight (n=5000)

When input size grows, algorithm choice becomes critical:

| # | Problem | Fast | Slow | Speedup |
|--:|---------|------|------|--------:|
| 0010 | Regular Expression Mat | Top-down Memo (0.08ms) | Bottom-up DP (5.3s) | **62,000x** faster |
| 0044 | Wildcard Matching | Greedy Backtrack (1.4ms) | 2D DP Table (10.0s) | **7052x** faster |
| 0011 | Container With Most Wa | Two Pointers (0.75ms) | Nested Loops (4.9s) | **6545x** faster |
| 0121 | Best Time To Buy And S | Running Min (2.0ms) | Nested Loops (3.1s) | **1552x** faster |
| 0416 | Partition Equal Subset | 2D DP Table (0.08ms) | 1D DP Space-Opt (96.6ms) | **1267x** faster |
| 0016 | 3Sum Closest | Two Ptr+Prune (1.1ms) | Two Ptr Basic (1.4s) | **1189x** faster |
| 0435 | Non Overlapping Interv | Greedy Sort (5.0ms) | DP Array (3.1s) | **617x** faster |
| 0001 | Two Sum | Hash Map (0.66ms) | Nested Loops (70.1ms) | **106x** faster |
| 0494 | Target Sum | DP Transform (0.04ms) | Memoization (3.2ms) | **73x** faster |
| 0875 | Koko Eating Bananas | Binary Search (14.6ms) | Linear Search (1.1s) | **72x** faster |
| 2104 | Sum Of Subarray Ranges | Stack (4.5ms) | Brute (305.5ms) | **68x** faster |
| 1011 | Capacity To Ship Packa | Default (10.3ms) | Linear Search (343.8ms) | **33x** faster |
| 0125 | Valid Palindrome | Default (0.03ms) | Filtered Pointe (0.80ms) | **23x** faster |
| 0459 | Repeated Substring Pat | Concatenation (0.06ms) | Default (0.97ms) | **17x** faster |
| 0496 | Next Greater Element I | Default (0.73ms) | Brute (9.4ms) | **13x** faster |
| 0055 | Jump Game | Greedy (1.7ms) | DP Array (10.9ms) | **7x** faster |
| 1392 | Longest Happy Prefix | Default (1.5ms) | Rolling Hash (7.5ms) | **5x** faster |
| 0110 | Balanced Binary Tree | Default (7.7ms) | Top Down (35.6ms) | **5x** faster |
| 1094 | Car Pooling | Difference (5.4ms) | Events (18.1ms) | **3x** faster |
| 0200 | Number Of Islands | Dfs (3.1ms) | Union Find (9.7ms) | **3x** faster |

> At n=5000, the wrong algorithm choice turns **milliseconds into minutes**.

📊 [查看全部 Large N 數據 →](benchmarks-full.md)

---

## Benchmark Summary (Small Test Data)

| # | Problem | N | Default | Best | Worst | Δ Time | Complexity |
|---|---------|---|---------|------|-------|--------|------------|
| 0001 | Two Sum | 3 | default 103ms | hash_map 98ms | default 103ms | +5% | O(n) time -> O(n) time |
| 0003 | Longest Substring Wi | 3 | default 98ms | set 95ms | default 98ms | +4% | O(n) time -> O(n) time |
| 0010 | Regular Expression M | 2 | default 95ms | default 95ms | recursive 95ms | +0% | O(m*n) time -> O(m*n) time |
| 0011 | Container With Most  | 4 | default 106ms | optimized 99ms | default 106ms | +7% | Same O(n) time |
| 0015 | 3Sum | 4 | default 97ms | hashset 94ms | hash 97ms | +3% | O(n²) time -> O(n²) time |
| 0016 | 3Sum Closest | 3 | default 96ms | two_pointers 95ms | optimized 99ms | +5% | O(n²) time -> O(n²) time |
| 0023 | Merge K Sorted Lists | 4 | default 109ms | heap 101ms | default 109ms | +8% | Same O(N log k)       4.6MB |
| 0025 | Reverse Nodes In K G | 3 | default 102ms | recursive 96ms | default 102ms | +6% | O(N) time -> O(N) time |
| 0026 | Remove Duplicates Fr | 3 | default 96ms | enumerate 94ms | two_pointers 112ms | +19% | Same O(n) time |
| 0027 | Remove Element | 3 | default 97ms | two_pointers 94ms | default 97ms | +2% | O(n) time -> O(n) time |
| 0028 | Find The Index Of Th | 2 | default 95ms | default 95ms | rabin_karp 100ms | +5% | O(m+n) time -> O(m+n) average time |
| 0033 | Search In Rotated So | 3 | default 97ms | binary_search 94ms | linear_scan 99ms | +5% | O(log n) time -> O(n) time |
| 0042 | Trapping Rain Water | 4 | default 102ms | dp 95ms | default 102ms | +8% | Same O(n) time |
| 0044 | Wildcard Matching | 3 | default 97ms | greedy 95ms | default 97ms | +2% | O(m*n) worst -> O(m*n) time |
| 0045 | Jump Game Ii | 2 | default 95ms | default 95ms | greedy 96ms | +1% | O(n) time -> O(n) time |
| 0046 | Permutations | 3 | default 98ms | backtracking 98ms | swap 98ms | +1% | O(n! × n) time -> O(n! × n) time |
| 0051 | N Queens | 3 | default 96ms | default 96ms | sets 104ms | +8% | Same O(N!) time |
| 0052 | N Queens Ii | 2 | default 98ms | default 98ms | bitmask 100ms | +2% | O(n!) time -> O(n!) time |
| 0055 | Jump Game | 3 | default 97ms | dp 96ms | default 97ms | +0% | O(n^2) time -> O(n) time |
| 0056 | Merge Intervals | 3 | default 105ms | graph_components 95ms | sort_merge 106ms | +12% | O(n²) time -> O(n log n) time |
| 0070 | Climbing Stairs | 4 | default 97ms | dp_array 95ms | dp_space_optimized 99ms | +5% | O(n) time -> O(n) time |
| 0072 | Edit Distance | 4 | default 98ms | dp_2d 96ms | memoization 99ms | +4% | Same O(m*n) time |
| 0075 | Sort Colors | 3 | default 98ms | dutch_flag 95ms | default 98ms | +3% | Same O(n) time |
| 0076 | Minimum Window Subst | 3 | default 96ms | sliding_window 96ms | sliding_window_filtered 96ms | +1% | O(|s| + |t|) time -> O(|s| + |t|) time |
| 0078 | Subsets | 2 | default 98ms | bitmask 93ms | default 98ms | +4% | O(n × 2^n) time -> O(n × 2^n) time |
| 0080 | Remove Duplicates Fr | 4 | default 98ms | k_copies 97ms | two_pointers 100ms | +3% | O(n) time -> O(n) time |
| 0084 | Largest Rectangle In | 3 | default 95ms | sentinel 94ms | twopass 96ms | +2% | O(n) time -> O(n) time |
| 0085 | Maximal Rectangle | 3 | default 95ms | default 95ms | dp 95ms | +1% | Same O(rows * cols) time |
| 0088 | Merge Sorted Array | 3 | default 100ms | backward 99ms | forward 107ms | +8% | O(m+n) time -> O(m+n) time |
| 0092 | Reverse Linked List  | 3 | default 98ms | one_pass 95ms | two_pass 101ms | +6% | O(N) time -> O(N) time |
| 0094 | Binary Tree Inorder  | 4 | default 98ms | morris 95ms | recursive 105ms | +11% | O(n) time -> O(n) time |
| 0102 | Binary Tree Level Or | 3 | default 96ms | dfs 94ms | default 96ms | +2% | O(n) time -> O(n) time |
| 0104 | Maximum Depth Of Bin | 4 | default 98ms | iterative_dfs 94ms | default 98ms | +4% | O(n) time -> O(n) time |
| 0110 | Balanced Binary Tree | 3 | default 105ms | top_down 96ms | default 105ms | +9% | O(n²) time -> O(n) time |
| 0121 | Best Time To Buy And | 3 | default 98ms | bruteforce 98ms | running_min 100ms | +2% | O(n²) time -> O(n) time |
| 0124 | Binary Tree Maximum  | 4 | default 96ms | instance_var 95ms | tuple_return 100ms | +5% | Same O(n) time |
| 0125 | Valid Palindrome | 4 | default 104ms | two_pointers 93ms | default 104ms | +11% | O(n) time -> O(n) time |
| 0131 | Palindrome Partition | 2 | default 101ms | default 101ms | naive 109ms | +8% | O(n × 2^n) time -> O(n × 2^n × n) time |
| 0134 | Gas Station | 2 | default 107ms | greedy 96ms | default 107ms | +11% | O(n) time -> O(n) time |
| 0135 | Candy | 2 | default 96ms | default 96ms | two_pass 100ms | +4% | Same O(n) time |
| 0141 | Linked List Cycle | 3 | default 108ms | hashset 98ms | default 108ms | +10% | O(n) time -> O(n) time |
| 0142 | Linked List Cycle Ii | 3 | default 95ms | floyd 95ms | hashset 98ms | +3% | O(n) time -> O(n) time |
| 0162 | Find Peak Element | 3 | default 117ms | binary_search 96ms | default 117ms | +21% | Same O(log n) time |
| 0167 | Two Sum Ii Input Arr | 3 | default 100ms | two_pointers 97ms | binary_search 100ms | +4% | O(n) time -> O(n log n) time |
| 0198 | House Robber | 4 | default 95ms | default 95ms | dp_array 105ms | +10% | O(n) time -> O(n) time |
| 0200 | Number Of Islands | 4 | default 109ms | union_find 104ms | dfs 114ms | +10% | O(m*n * α(m*n)) time -> O(m*n) time |
| 0202 | Happy Number | 3 | default 108ms | floyd 102ms | default 108ms | +6% | O(log n) time -> O(log n) time |
| 0206 | Reverse Linked List | 3 | default 101ms | recursive 100ms | iterative 102ms | +2% | O(N) time -> O(N) time |
| 0209 | Minimum Size Subarra | 3 | default 101ms | sliding_window 98ms | default 101ms | +3% | O(n) time -> O(n) time |
| 0213 | House Robber Ii | 3 | default 101ms | memoization 95ms | dp_decomposition 105ms | +10% | O(n) time -> O(n) time |
| 0214 | Shortest Palindrome | 2 | default 108ms | rolling_hash 94ms | default 108ms | +15% | O(n) time -> O(n) time |
| 0215 | Kth Largest Element  | 3 | default 101ms | quickselect 97ms | default 101ms | +4% | Same O(n) average time |
| 0218 | The Skyline Problem | 3 | default 101ms | heap 97ms | default 101ms | +4% | O(n log n) time -> O(n log n) time |
| 0239 | Sliding Window Maxim | 2 | default 100ms | default 100ms | deque 102ms | +1% | Same O(n) time |
| 0253 | Meeting Rooms Ii | 3 | default 97ms | default 97ms | heap 103ms | +6% | Same O(n log n) time |
| 0283 | Move Zeroes | 5 | default 96ms | swap 94ms | two_pointers 99ms | +5% | O(n) time -> O(n) time |
| 0287 | Find The Duplicate N | 3 | default 104ms | floyd 94ms | default 104ms | +10% | O(n) time -> O(n) time |
| 0295 | Find Median From Dat | 2 | default 104ms | sorted_list 102ms | default 104ms | +2% | O(n) add -> O(log n) add |
| 0307 | Range Sum Query Muta | 3 | default 118ms | bit 102ms | segment_tree 126ms | +23% | O(n log n) build -> O(n) build |
| 0312 | Burst Balloons | 2 | default 95ms | default 95ms | memoization 114ms | +20% | O(n³) time -> O(n³) time |
| 0315 | Count Of Smaller Num | 3 | default 99ms | default 99ms | bit 109ms | +11% | O(n log n) time -> O(n log n) time |
| 0322 | Coin Change | 4 | default 120ms | dp_bottom_up 104ms | default 120ms | +16% | Same O(n * amount) time |
| 0327 | Count Of Range Sum | 2 | default 103ms | default 103ms | merge_sort 115ms | +12% | Same O(n log n) time |
| 0337 | House Robber Iii | 2 | default 109ms | memo 99ms | default 109ms | +10% | O(n) time -> O(n) time |
| 0416 | Partition Equal Subs | 4 | default 108ms | memoization 99ms | dp_2d 125ms | +26% | O(n * target) time -> O(n * target) time |
| 0435 | Non Overlapping Inte | 2 | default 99ms | dp 95ms | default 99ms | +4% | O(n²) time -> O(n log n) time |
| 0455 | Assign Cookies | 2 | default 94ms | default 94ms | greedy 96ms | +2% | Same O(n log n + m log m) time |
| 0459 | Repeated Substring P | 2 | default 94ms | default 94ms | concatenation 96ms | +1% | Same O(n) time |
| 0486 | Predict The Winner | 2 | default 97ms | space_optimized 93ms | default 97ms | +5% | O(n²) time -> O(n²) time |
| 0494 | Target Sum | 3 | default 100ms | memoization 95ms | dp_transform 103ms | +9% | O(n * sum) time -> O(n * target) time |
| 0496 | Next Greater Element | 3 | default 96ms | stack 94ms | default 96ms | +2% | Same O(n + m) time |
| 0503 | Next Greater Element | 3 | default 96ms | twopass 94ms | default 96ms | +3% | Same O(n) time |
| 0516 | Longest Palindromic  | 2 | default 98ms | default 98ms | interval_dp 98ms | +1% | O(n^2) time -> O(n^2) time |
| 0518 | Coin Change 2 | 3 | default 101ms | memoization 97ms | default 101ms | +5% | O(n * amount) time -> O(n * amount) time |
| 0542 | 01 Matrix | 3 | default 96ms | default 96ms | bfs 100ms | +4% | Same O(m*n) time |
| 0543 | Diameter Of Binary T | 3 | default 97ms | instance_var 94ms | default 97ms | +3% | Same O(n) time |
| 0664 | Strange Printer | 2 | default 97ms | default 97ms | memoization 98ms | +1% | Same O(n³) time |
| 0680 | Valid Palindrome Ii | 4 | default 98ms | recursive 95ms | default 98ms | +3% | O(n) time -> O(n) time |
| 0684 | Redundant Connection | 3 | default 97ms | union_find 94ms | default 97ms | +3% | O(n × α(n)) time -> O(n × α(n)) time |
| 0721 | Accounts Merge | 3 | default 98ms | dfs 94ms | union_find 98ms | +5% | O(n × k) time -> O(n × k × α(n)) time |
| 0739 | Daily Temperatures | 3 | default 107ms | backward 100ms | default 107ms | +7% | O(n) time -> O(n) time |
| 0743 | Network Delay Time | 3 | default 97ms | bellman_ford 94ms | default 97ms | +4% | O(V × E) time -> O((V+E) log V) time |
| 0746 | Min Cost Climbing St | 4 | default 96ms | dp_space_optimized 94ms | memoization 98ms | +4% | O(n) time -> O(n) time |
| 0862 | Shortest Subarray Wi | 2 | default 103ms | deque 97ms | default 103ms | +7% | O(n) time -> O(n) time |
| 0875 | Koko Eating Bananas | 3 | default 98ms | linear_search 95ms | default 98ms | +3% | O(n × m) time -> O(n log m) time |
| 0876 | Middle Of The Linked | 3 | default 95ms | default 95ms | fast_slow 98ms | +3% | Same O(n) time |
| 0877 | Stone Game | 2 | default 97ms | default 97ms | dp 97ms | +1% | O(1) time -> O(n²) time |
| 0905 | Sort Array By Parity | 3 | default 100ms | opposite_pointers 98ms | writer 100ms | +2% | O(n) time -> O(n) time |
| 0907 | Sum Of Subarray Mini | 3 | default 107ms | single 103ms | contribution 112ms | +9% | O(n) time -> O(n) time |
| 0922 | Sort Array By Parity | 2 | default 99ms | default 99ms | two_pointers 102ms | +3% | O(n) time -> O(n) time |
| 0968 | Binary Tree Cameras | 2 | default 101ms | dp 99ms | default 101ms | +2% | O(n) time -> O(n) time |
| 0977 | Squares Of A Sorted  | 3 | default 102ms | sort 97ms | default 102ms | +5% | O(n log n) time -> O(n) time |
| 0990 | Satisfiability Of Eq | 2 | default 100ms | dfs 99ms | default 100ms | +1% | O(n + 26) time -> O(n × α(26)) time |
| 0994 | Rotting Oranges | 3 | default 104ms | bfs 103ms | default 104ms | +1% | O(m*n) time -> O(m*n) time |
| 1011 | Capacity To Ship Pac | 2 | default 95ms | default 95ms | linear_search 98ms | +3% | O(n log S) time -> O(n * S) time |
| 1029 | Two City Scheduling | 2 | default 98ms | greedy 95ms | default 98ms | +3% | O(n log n) time -> O(n log n) time |
| 1094 | Car Pooling | 3 | default 99ms | default 99ms | difference 108ms | +10% | Same O(n + m) time |
| 1143 | Longest Common Subse | 2 | default 100ms | space_optimized 96ms | default 100ms | +4% | O(m*n) time -> O(m*n) time |
| 1392 | Longest Happy Prefix | 2 | default 96ms | default 96ms | rolling_hash 98ms | +1% | O(n) time -> O(n) time |
| 1406 | Stone Game Iii | 2 | default 99ms | default 99ms | space_optimized 102ms | +3% | O(n) time -> O(n) time |
| 1438 | Longest Continuous S | 2 | default 97ms | default 97ms | two_deques 98ms | +1% | O(n) time -> O(n) time |
| 1499 | Max Value Of Equatio | 2 | default 99ms | default 99ms | deque 104ms | +5% | O(n) time -> O(n) time |
| 1547 | Minimum Cost To Cut  | 2 | default 100ms | memoization 95ms | default 100ms | +5% | O(m³) time -> O(m³) time |
| 2104 | Sum Of Subarray Rang | 3 | default 103ms | brute 96ms | default 103ms | +7% | O(n^2) time -> O(n) time |

> `*` indicates counter-intuitive result where declared slower complexity runs faster on small test data.
> This demonstrates that complexity != actual time for small inputs.

---

## Appendix: Full Solution Details

### 0001_two_sum (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| hash_map | 97.8ms | O(n) time, O(n) space       4.7MB | fastest |
| bruteforce | 98.4ms | O(n²) time, O(1) space       4.7MB |  |
| default | 102.5ms | O(n) time, O(n) space       4.6MB | slowest, default |

### 0003_longest_substring_without_repeating_characters (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| set | 94.5ms | O(n) time, O(min(n,σ)) space       4.7MB | fastest |
| dict | 96.4ms | O(n) time, O(min(n,σ)) space       4.6MB |  |
| default | 98.0ms | O(n) time, O(min(n,σ)) space       4.6MB | slowest, default |

### 0010_regular_expression_matching (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 94.5ms | O(m*n) time, O(m*n) space       4.6MB | fastest, default |
| recursive | 94.6ms | O(m*n) time, O(m*n) space       4.8MB | slowest |

### 0011_container_with_most_water (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| optimized | 98.8ms | O(n) time, O(1) space       4.6MB | fastest |
| bruteforce | 100.9ms | O(n^2) time, O(1) space       4.6MB |  |
| two_pointers | 104.5ms | O(n) time, O(1) space       4.7MB |  |
| default | 106.0ms | O(n) time, O(1) space       4.6MB | slowest, default |

### 0015_3sum (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| hashset | 94.0ms | O(n²) time, O(n) space for set       4.7MB | fastest |
| two_pointers | 96.3ms | O(n²) time, O(1) extra space       4.7MB |  |
| default | 97.0ms | O(n²) time, O(1) extra space       4.6MB | default |
| hash | 97.0ms | O(n²) time, O(n) space       4.6MB | slowest |

### 0016_3sum_closest (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| two_pointers | 94.6ms | O(n²) time, O(1) extra space       4.6MB | fastest |
| default | 95.8ms | O(n²) time, O(1) extra space       4.8MB | default |
| optimized | 98.9ms | O(n²) time, O(1) extra space       4.7MB | slowest |

### 0023_merge_k_sorted_lists (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| heap | 100.8ms | O(N log k)       4.6MB | fastest |
| divide | 101.0ms | O(N log k)       4.7MB |  |
| greedy | 103.5ms | O(kN)       4.7MB |  |
| default | 109.1ms | O(N log k)       4.6MB | slowest, default |

### 0025_reverse_nodes_in_k_group (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| recursive | 96.4ms | O(N) time, O(N) space       4.7MB | fastest |
| iterative | 97.2ms | O(N) time, O(1) space       4.6MB |  |
| default | 102.5ms | O(N) time, O(1) space       4.6MB | slowest, default |

### 0026_remove_duplicates_from_sorted_array (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| enumerate | 94.2ms | O(n) time, O(1) space       4.6MB | fastest |
| default | 96.4ms | O(n) time, O(1) space       4.6MB | default |
| two_pointers | 111.9ms | O(n) time, O(1) space       4.6MB | slowest |

### 0027_remove_element (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| two_pointers | 94.5ms | O(n) time, O(1) space       4.6MB | fastest |
| two_ends | 95.3ms | O(n) time, O(1) space       4.6MB |  |
| default | 96.5ms | O(n) time, O(1) space       4.7MB | slowest, default |

### 0028_find_the_index_of_the_first_occurrence_in_a_string (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 95.4ms | O(m+n) time, O(n) space       4.6MB | fastest, default |
| rabin_karp | 99.9ms | O(m+n) average time, O(1) space       4.6MB | slowest |

### 0033_search_in_rotated_sorted_array (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| binary_search | 94.5ms | O(log n) time, O(1) space       4.9MB | fastest |
| default | 97.5ms | O(log n) time, O(1) space       4.6MB | default |
| linear_scan | 99.3ms | O(n) time, O(1) space       4.7MB | slowest |

### 0042_trapping_rain_water (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dp | 95.1ms | O(n) time, O(n) space       4.6MB | fastest |
| twopointer | 95.8ms | O(n) time, O(1) space       4.6MB |  |
| stack | 99.0ms | O(n) time, O(n) space       4.6MB |  |
| default | 102.5ms | O(n) time, O(n) space       4.6MB | slowest, default |

### 0044_wildcard_matching (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| greedy | 94.7ms | O(m*n) worst, O(m+n) average time, O(1) space       4.6MB | fastest |
| space_optimized | 94.9ms | O(m*n) time, O(n) space       4.9MB |  |
| default | 96.6ms | O(m*n) time, O(m*n) space       4.7MB | slowest, default |

### 0045_jump_game_ii (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 94.7ms | O(n) time, O(1) space       4.6MB | fastest, default |
| greedy | 95.9ms | O(n) time, O(1) space       4.7MB | slowest |

### 0046_permutations (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| backtracking | 97.7ms | O(n! × n) time, O(n) space       4.6MB | fastest |
| default | 98.0ms | O(n! × n) time, O(n) space       4.7MB | default |
| swap | 98.3ms | O(n! × n) time, O(n) space       4.8MB | slowest |

### 0051_n_queens (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 96.0ms | O(N!) time, O(N) space       4.6MB | fastest, default |
| bitmask | 101.4ms | O(N!) time, O(N) space       4.8MB |  |
| sets | 104.2ms | O(N!) time, O(N) space       4.6MB | slowest |

### 0052_n_queens_ii (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 97.8ms | O(n!) time, O(n) space       4.6MB | fastest, default |
| bitmask | 100.1ms | O(n!) time, O(n) space       4.7MB | slowest |

### 0055_jump_game (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dp | 96.2ms | O(n^2) time, O(n) space       4.6MB | fastest |
| greedy | 96.5ms | O(n) time, O(1) space       4.6MB |  |
| default | 96.7ms | O(n) time, O(1) space       4.6MB | slowest, default |

### 0056_merge_intervals (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| graph_components | 94.9ms | O(n²) time, O(n²) space       4.6MB | fastest |
| default | 105.3ms | O(n log n) time, O(n) space       4.8MB | default |
| sort_merge | 106.5ms | O(n log n) time, O(n) space       4.6MB | slowest |

### 0070_climbing_stairs (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dp_array | 94.8ms | O(n) time, O(n) space       4.8MB | fastest |
| default | 96.7ms | O(n) time, O(1) space       4.7MB | default |
| memoization | 98.3ms | O(n) time, O(n) space       4.6MB |  |
| dp_space_optimized | 99.4ms | O(n) time, O(1) space       4.6MB | slowest |

### 0072_edit_distance (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dp_2d | 95.7ms | O(m*n) time, O(m*n) space       4.6MB | fastest |
| space_optimized | 96.0ms | O(m*n) time, O(min(m,n)) space       4.7MB |  |
| default | 98.3ms | O(m*n) time, O(m*n) space       4.6MB | default |
| memoization | 99.3ms | O(m*n) time, O(m*n) space       4.6MB | slowest |

### 0075_sort_colors (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dutch_flag | 94.6ms | O(n) time, O(1) space       4.7MB | fastest |
| counting | 95.9ms | O(n) time, O(1) space       4.6MB |  |
| default | 97.6ms | O(n) time, O(1) space       4.7MB | slowest, default |

### 0076_minimum_window_substring (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| sliding_window | 95.6ms | O(|s| + |t|) time, O(|t|) space       4.6MB | fastest |
| default | 96.1ms | O(|s| + |t|) time, O(|t|) space       4.6MB | default |
| sliding_window_filtered | 96.1ms | O(|s| + |t|) time, O(|s|) space       4.8MB | slowest |

### 0078_subsets (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| bitmask | 93.4ms | O(n × 2^n) time, O(1) extra space       4.6MB | fastest |
| default | 97.6ms | O(n × 2^n) time, O(n) space       4.6MB | slowest, default |

### 0080_remove_duplicates_from_sorted_array_ii (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| k_copies | 96.8ms | O(n) time, O(1) space       4.7MB | fastest |
| counter | 98.4ms | O(n) time, O(1) space       4.6MB |  |
| default | 98.5ms | O(n) time, O(1) space       4.6MB | default |
| two_pointers | 99.8ms | O(n) time, O(1) space       4.6MB | slowest |

### 0084_largest_rectangle_in_histogram (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| sentinel | 94.5ms | O(n) time, O(n) space       4.7MB | fastest |
| default | 95.5ms | O(n) time, O(n) space       4.6MB | default |
| twopass | 96.4ms | O(n) time, O(n) space       4.8MB | slowest |

### 0085_maximal_rectangle (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 94.5ms | O(rows * cols) time, O(cols) space       4.6MB | fastest, default |
| stack | 94.5ms | O(rows * cols) time, O(cols) space       4.7MB |  |
| dp | 95.2ms | O(rows * cols) time, O(cols) space       4.6MB | slowest |

### 0088_merge_sorted_array (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| backward | 98.5ms | O(m+n) time, O(1) space       4.6MB | fastest |
| default | 100.5ms | O(m+n) time, O(1) space       4.7MB | default |
| forward | 106.5ms | O(m+n) time, O(m) space       4.7MB | slowest |

### 0092_reverse_linked_list_ii (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| one_pass | 95.3ms | O(N) time, O(1) space       4.8MB | fastest |
| default | 97.8ms | O(N) time, O(1) space       4.8MB | default |
| two_pass | 100.8ms | O(N) time, O(1) space       4.6MB | slowest |

### 0094_binary_tree_inorder_traversal (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| morris | 94.7ms | O(n) time, O(1) space       4.6MB | fastest |
| default | 98.0ms | O(n) time, O(h) space       4.6MB | default |
| iterative | 99.3ms | O(n) time, O(h) space       4.6MB |  |
| recursive | 105.3ms | O(n) time, O(h) space       4.7MB | slowest |

### 0102_binary_tree_level_order_traversal (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dfs | 93.9ms | O(n) time, O(h) space       4.7MB | fastest |
| bfs | 94.4ms | O(n) time, O(w) space       4.6MB |  |
| default | 95.9ms | O(n) time, O(w) space       4.7MB | slowest, default |

### 0104_maximum_depth_of_binary_tree (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| iterative_dfs | 93.8ms | O(n) time, O(h) space       4.6MB | fastest |
| recursive | 94.3ms | O(n) time, O(h) space       4.7MB |  |
| bfs | 94.3ms | O(n) time, O(w) space       4.7MB |  |
| default | 97.8ms | O(n) time, O(h) space       4.7MB | slowest, default |

### 0110_balanced_binary_tree (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| top_down | 95.9ms | O(n²) time, O(h) space       4.7MB | fastest |
| bottom_up | 103.2ms | O(n) time, O(h) space       4.7MB |  |
| default | 104.9ms | O(n) time, O(h) space       4.7MB | slowest, default |

### 0121_best_time_to_buy_and_sell_stock (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| bruteforce | 97.5ms | O(n²) time, O(1) space       4.7MB | fastest |
| default | 97.7ms | O(n) time, O(1) space       4.6MB | default |
| running_min | 99.7ms | O(n) time, O(1) space       4.7MB | slowest |

### 0124_binary_tree_maximum_path_sum (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| instance_var | 95.5ms | O(n) time, O(h) space       4.6MB | fastest |
| default | 95.7ms | O(n) time, O(h) space       4.6MB | default |
| nonlocal | 95.7ms | O(n) time, O(h) space       4.7MB |  |
| tuple_return | 99.9ms | O(n) time, O(h) space       4.6MB | slowest |

### 0125_valid_palindrome (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| two_pointers | 93.4ms | O(n) time, O(1) space       4.6MB | fastest |
| filtered_pointers | 95.7ms | O(n) time, O(n) space       4.6MB |  |
| filtered | 97.1ms | O(n) time, O(n) space       4.6MB |  |
| default | 103.8ms | O(n) time, O(1) space       4.7MB | slowest, default |

### 0131_palindrome_partitioning (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 101.4ms | O(n × 2^n) time, O(n^2) space       4.6MB | fastest, default |
| naive | 109.4ms | O(n × 2^n × n) time, O(n) space       4.6MB | slowest |

### 0134_gas_station (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| greedy | 96.3ms | O(n) time, O(1) space       4.6MB | fastest |
| default | 106.6ms | O(n) time, O(1) space       4.7MB | slowest, default |

### 0135_candy (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 95.6ms | O(n) time, O(n) space       4.7MB | fastest, default |
| two_pass | 99.8ms | O(n) time, O(n) space       4.7MB | slowest |

### 0141_linked_list_cycle (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| hashset | 97.8ms | O(n) time, O(n) space       4.6MB | fastest |
| floyd | 98.0ms | O(n) time, O(1) space       4.6MB |  |
| default | 107.7ms | O(n) time, O(1) space       4.6MB | slowest, default |

### 0142_linked_list_cycle_ii (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| floyd | 95.0ms | O(n) time, O(1) space       4.7MB | fastest |
| default | 95.2ms | O(n) time, O(1) space       4.6MB | default |
| hashset | 97.9ms | O(n) time, O(n) space       4.6MB | slowest |

### 0162_find_peak_element (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| binary_search | 96.3ms | O(log n) time, O(1) space       4.7MB | fastest |
| linear_scan | 98.0ms | O(n) time, O(1) space       4.6MB |  |
| default | 116.8ms | O(log n) time, O(1) space       4.7MB | slowest, default |

### 0167_two_sum_ii_input_array_is_sorted (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| two_pointers | 96.6ms | O(n) time, O(1) space       4.8MB | fastest |
| default | 99.9ms | O(n) time, O(1) space       4.6MB | default |
| binary_search | 100.1ms | O(n log n) time, O(1) space       4.6MB | slowest |

### 0198_house_robber (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 95.4ms | O(n) time, O(1) space       4.6MB | fastest, default |
| dp_space_optimized | 96.5ms | O(n) time, O(1) space       4.7MB |  |
| memoization | 100.9ms | O(n) time, O(n) space       4.7MB |  |
| dp_array | 105.3ms | O(n) time, O(n) space       4.7MB | slowest |

### 0200_number_of_islands (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| union_find | 103.8ms | O(m*n * α(m*n)) time, O(m*n) space       4.7MB | fastest |
| bfs | 105.8ms | O(m*n) time, O(min(m,n)) space       4.7MB |  |
| default | 109.2ms | O(m*n) time, O(m*n) space       4.7MB | default |
| dfs | 113.7ms | O(m*n) time, O(m*n) space       4.6MB | slowest |

### 0202_happy_number (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| floyd | 102.2ms | O(log n) time, O(1) space       4.6MB | fastest |
| hashset | 104.2ms | O(log n) time, O(log n) space       4.8MB |  |
| default | 108.2ms | O(log n) time, O(1) space       4.8MB | slowest, default |

### 0206_reverse_linked_list (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| recursive | 100.3ms | O(N) time, O(N) space       4.7MB | fastest |
| default | 100.8ms | O(N) time, O(1) space       4.7MB | default |
| iterative | 102.3ms | O(N) time, O(1) space       4.7MB | slowest |

### 0209_minimum_size_subarray_sum (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| sliding_window | 98.2ms | O(n) time, O(1) space       4.7MB | fastest |
| binary_search | 99.4ms | O(n log n) time, O(n) space       4.7MB |  |
| default | 100.8ms | O(n) time, O(1) space       4.6MB | slowest, default |

### 0213_house_robber_ii (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| memoization | 95.4ms | O(n) time, O(n) space       4.6MB | fastest |
| default | 101.5ms | O(n) time, O(1) space       4.7MB | default |
| dp_decomposition | 105.2ms | O(n) time, O(1) space       4.6MB | slowest |

### 0214_shortest_palindrome (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| rolling_hash | 93.6ms | O(n) time, O(1) space       4.6MB | fastest |
| default | 108.0ms | O(n) time, O(n) space       4.6MB | slowest, default |

### 0215_kth_largest_element_in_an_array (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| quickselect | 97.1ms | O(n) average time, O(1) space       4.6MB | fastest |
| heap | 98.4ms | O(n log k) time, O(k) space       4.8MB |  |
| default | 101.1ms | O(n) average time, O(1) space       4.6MB | slowest, default |

### 0218_the_skyline_problem (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| heap | 97.2ms | O(n log n) time, O(n) space       4.6MB | fastest |
| sortedlist | 98.1ms | O(n log n) time, O(n) space       4.8MB |  |
| default | 101.5ms | O(n log n) time, O(n) space       4.7MB | slowest, default |

### 0239_sliding_window_maximum (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 100.2ms | O(n) time, O(k) space       4.8MB | fastest, default |
| deque | 101.7ms | O(n) time, O(k) space       4.8MB | slowest |

### 0253_meeting_rooms_ii (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 96.6ms | O(n log n) time, O(n) space       4.7MB | fastest, default |
| sweep | 102.2ms | O(n log n) time, O(n) space       4.6MB |  |
| heap | 102.8ms | O(n log n) time, O(n) space       4.7MB | slowest |

### 0283_move_zeroes (5 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| swap | 94.0ms | O(n) time, O(1) space       4.7MB | fastest |
| optimized_swap | 94.0ms | O(n) time, O(1) space       4.6MB |  |
| default | 95.5ms | O(n) time, O(1) space       4.6MB | default |
| snowball | 95.9ms | O(n) time, O(1) space       4.6MB |  |
| two_pointers | 98.7ms | O(n) time, O(1) space       4.6MB | slowest |

### 0287_find_the_duplicate_number (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| floyd | 94.3ms | O(n) time, O(1) space       4.6MB | fastest |
| binary_search | 95.5ms | O(n log n) time, O(1) space       4.6MB |  |
| default | 103.7ms | O(n) time, O(1) space       4.8MB | slowest, default |

### 0295_find_median_from_data_stream (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| sorted_list | 101.5ms | O(n) add, O(1) find       4.6MB | fastest |
| default | 103.6ms | O(log n) add, O(1) find       4.6MB | slowest, default |

### 0307_range_sum_query_mutable (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| bit | 101.8ms | O(n log n) build, O(log n) ops       4.7MB | fastest |
| default | 118.3ms | O(n log n) build, O(log n) ops       4.7MB | default |
| segment_tree | 125.7ms | O(n) build, O(log n) ops       4.7MB | slowest |

### 0312_burst_balloons (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 95.1ms | O(n³) time, O(n²) space       4.7MB | fastest, default |
| memoization | 114.3ms | O(n³) time, O(n²) space       4.6MB | slowest |

### 0315_count_of_smaller_numbers_after_self (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 98.7ms | O(n log n) time, O(n) space       4.6MB | fastest, default |
| merge_sort | 101.5ms | O(n log n) time, O(n) space       4.8MB |  |
| bit | 109.2ms | O(n log n) time, O(n) space       4.7MB | slowest |

### 0322_coin_change (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dp_bottom_up | 103.8ms | O(n * amount) time, O(amount) space       4.8MB | fastest |
| memoization | 104.2ms | O(n * amount) time, O(amount) space       4.7MB |  |
| bfs | 106.8ms | O(n * amount) time, O(amount) space       4.6MB |  |
| default | 120.3ms | O(n * amount) time, O(amount) space       4.8MB | slowest, default |

### 0327_count_of_range_sum (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 103.2ms | O(n log n) time, O(n) space       4.7MB | fastest, default |
| merge_sort | 115.4ms | O(n log n) time, O(n) space       4.7MB | slowest |

### 0337_house_robber_iii (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| memo | 99.3ms | O(n) time, O(n) space       4.8MB | fastest |
| default | 108.8ms | O(n) time, O(h) space       4.6MB | slowest, default |

### 0416_partition_equal_subset_sum (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| memoization | 98.8ms | O(n * target) time, O(n * target) space       4.8MB | fastest |
| dp_1d | 104.0ms | O(n * target) time, O(target) space       4.6MB |  |
| default | 108.3ms | O(n * target) time, O(target) space       4.8MB | default |
| dp_2d | 124.7ms | O(n * target) time, O(n * target) space       4.6MB | slowest |

### 0435_non_overlapping_intervals (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dp | 95.2ms | O(n²) time, O(n) space       4.8MB | fastest |
| default | 99.1ms | O(n log n) time, O(1) space       4.8MB | slowest, default |

### 0455_assign_cookies (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 93.6ms | O(n log n + m log m) time, O(1) space       4.7MB | fastest, default |
| greedy | 95.8ms | O(n log n + m log m) time, O(1) space       4.7MB | slowest |

### 0459_repeated_substring_pattern (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 94.3ms | O(n) time, O(n) space       4.6MB | fastest, default |
| concatenation | 95.6ms | O(n) time, O(n) space       4.6MB | slowest |

### 0486_predict_the_winner (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| space_optimized | 92.6ms | O(n²) time, O(n) space       4.6MB | fastest |
| default | 97.4ms | O(n²) time, O(n²) space       4.6MB | slowest, default |

### 0494_target_sum (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| memoization | 94.7ms | O(n * sum) time, O(n * sum) space       4.7MB | fastest |
| default | 100.0ms | O(n * target) time, O(target) space       4.7MB | default |
| dp_transform | 103.2ms | O(n * target) time, O(target) space       4.6MB | slowest |

### 0496_next_greater_element_i (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| stack | 94.4ms | O(n + m) time, O(n) space       4.6MB | fastest |
| brute | 94.8ms | O(m * n) time, O(1) space       4.7MB |  |
| default | 95.9ms | O(n + m) time, O(n) space       4.6MB | slowest, default |

### 0503_next_greater_element_ii (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| twopass | 93.6ms | O(n) time, O(n) space       4.8MB | fastest |
| concat | 95.2ms | O(n) time, O(n) space       4.7MB |  |
| default | 96.4ms | O(n) time, O(n) space       4.8MB | slowest, default |

### 0516_longest_palindromic_subsequence (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 97.5ms | O(n^2) time, O(n^2) space       4.6MB | fastest, default |
| interval_dp | 98.2ms | O(n^2) time, O(n^2) space       4.7MB | slowest |

### 0518_coin_change_2 (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| memoization | 96.7ms | O(n * amount) time, O(n * amount) space       4.6MB | fastest |
| dp_unbounded | 97.0ms | O(n * amount) time, O(amount) space       4.8MB |  |
| default | 101.4ms | O(n * amount) time, O(amount) space       4.6MB | slowest, default |

### 0542_01_matrix (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 95.6ms | O(m*n) time, O(m*n) space       4.8MB | fastest, default |
| dp | 96.4ms | O(m*n) time, O(1) extra space       4.6MB |  |
| bfs | 99.7ms | O(m*n) time, O(m*n) space       4.8MB | slowest |

### 0543_diameter_of_binary_tree (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| instance_var | 94.5ms | O(n) time, O(h) space       4.6MB | fastest |
| tuple_return | 96.5ms | O(n) time, O(h) space       4.6MB |  |
| default | 97.2ms | O(n) time, O(h) space       4.6MB | slowest, default |

### 0664_strange_printer (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 97.3ms | O(n³) time, O(n²) space       4.6MB | fastest, default |
| memoization | 98.3ms | O(n³) time, O(n²) space       4.6MB | slowest |

### 0680_valid_palindrome_ii (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| recursive | 94.6ms | O(n) time, O(n) space for recursion stack       4.6MB | fastest |
| two_pointers | 95.0ms | O(n) time, O(1) space       4.6MB |  |
| iterative | 96.5ms | O(n) time, O(1) space       4.7MB |  |
| default | 97.5ms | O(n) time, O(1) space       4.6MB | slowest, default |

### 0684_redundant_connection (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| union_find | 93.9ms | O(n × α(n)) time, O(n) space       4.6MB | fastest |
| dfs | 95.3ms | O(n²) time, O(n) space       4.6MB |  |
| default | 96.9ms | O(n × α(n)) time, O(n) space       4.7MB | slowest, default |

### 0721_accounts_merge (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dfs | 93.5ms | O(n × k) time, O(n × k) space       4.7MB | fastest |
| default | 97.7ms | O(n × k × α(n)) time, O(n × k) space       4.8MB | default |
| union_find | 98.3ms | O(n × k × α(n)) time, O(n × k) space       4.6MB | slowest |

### 0739_daily_temperatures (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| backward | 100.0ms | O(n) time, O(1) space       4.7MB | fastest |
| stack | 106.4ms | O(n) time, O(n) space       4.6MB |  |
| default | 106.8ms | O(n) time, O(n) space       4.7MB | slowest, default |

### 0743_network_delay_time (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| bellman_ford | 93.8ms | O(V × E) time, O(V) space       4.6MB | fastest |
| dijkstra | 95.5ms | O((V+E) log V) time, O(V+E) space       4.7MB |  |
| default | 97.2ms | O((V+E) log V) time, O(V+E) space       4.7MB | slowest, default |

### 0746_min_cost_climbing_stairs (4 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dp_space_optimized | 94.1ms | O(n) time, O(1) space       4.7MB | fastest |
| default | 96.4ms | O(n) time, O(1) space       4.7MB | default |
| dp_array | 97.5ms | O(n) time, O(n) space       4.7MB |  |
| memoization | 98.2ms | O(n) time, O(n) space       4.7MB | slowest |

### 0862_shortest_subarray_with_sum_at_least_k (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| deque | 96.6ms | O(n) time, O(n) space       4.8MB | fastest |
| default | 102.9ms | O(n) time, O(n) space       4.7MB | slowest, default |

### 0875_koko_eating_bananas (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| linear_search | 94.6ms | O(n × m) time, O(1) space       4.7MB | fastest |
| binary_search | 95.8ms | O(n log m) time, O(1) space       4.7MB |  |
| default | 97.9ms | O(n log m) time, O(1) space, where m = max(piles)       4.6MB | slowest, default |

### 0876_middle_of_the_linked_list (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 95.3ms | O(n) time, O(1) space       4.6MB | fastest, default |
| two_pass | 95.8ms | O(n) time, O(1) space       4.6MB |  |
| fast_slow | 98.4ms | O(n) time, O(1) space       4.6MB | slowest |

### 0877_stone_game (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 96.5ms | O(1) time, O(1) space       4.6MB | fastest, default |
| dp | 97.1ms | O(n²) time, O(n²) space       4.6MB | slowest |

### 0905_sort_array_by_parity (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| opposite_pointers | 98.4ms | O(n) time, O(1) space       4.7MB | fastest |
| default | 99.7ms | O(n) time, O(1) space       4.6MB | default |
| writer | 100.1ms | O(n) time, O(1) space       4.6MB | slowest |

### 0907_sum_of_subarray_minimums (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| single | 103.3ms | O(n) time, O(n) space       4.6MB | fastest |
| default | 107.4ms | O(n) time, O(n) space       4.6MB | default |
| contribution | 112.3ms | O(n) time, O(n) space       4.8MB | slowest |

### 0922_sort_array_by_parity_ii (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 98.9ms | O(n) time, O(1) space       4.6MB | fastest, default |
| two_pointers | 101.9ms | O(n) time, O(1) space       4.7MB | slowest |

### 0968_binary_tree_cameras (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dp | 99.4ms | O(n) time, O(h) space       4.6MB | fastest |
| default | 101.1ms | O(n) time, O(h) space       4.7MB | slowest, default |

### 0977_squares_of_a_sorted_array (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| sort | 96.9ms | O(n log n) time, O(n) space       4.8MB | fastest |
| two_pointers | 98.2ms | O(n) time, O(n) space       4.6MB |  |
| default | 102.1ms | O(n) time, O(n) space       4.6MB | slowest, default |

### 0990_satisfiability_of_equality_equations (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| dfs | 99.2ms | O(n + 26) time, O(26) space       4.7MB | fastest |
| default | 100.2ms | O(n × α(26)) time, O(1) space       4.7MB | slowest, default |

### 0994_rotting_oranges (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| bfs | 102.6ms | O(m*n) time, O(m*n) space       4.6MB | fastest |
| simulation | 104.0ms | O((m*n)²) time, O(m*n) space       4.6MB |  |
| default | 104.1ms | O(m*n) time, O(m*n) space       4.7MB | slowest, default |

### 1011_capacity_to_ship_packages_within_d_days (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 95.5ms | O(n log S) time, O(1) space, where S = sum(weights)       4.6MB | fastest, default |
| linear_search | 98.4ms | O(n * S) time, O(1) space       4.6MB | slowest |

### 1029_two_city_scheduling (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| greedy | 95.5ms | O(n log n) time, O(1) space       4.7MB | fastest |
| default | 98.3ms | O(n log n) time, O(1) space       4.6MB | slowest, default |

### 1094_car_pooling (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 98.9ms | O(n + m) time, O(m) space where m = max location       4.7MB | fastest, default |
| events | 100.7ms | O(n log n) time, O(n) space       4.7MB |  |
| difference | 108.5ms | O(n + m) time, O(m) space where m = max location       4.7MB | slowest |

### 1143_longest_common_subsequence (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| space_optimized | 95.6ms | O(m*n) time, O(min(m,n)) space       4.7MB | fastest |
| default | 99.5ms | O(m*n) time, O(m*n) space       4.7MB | slowest, default |

### 1392_longest_happy_prefix (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 96.1ms | O(n) time, O(n) space       4.7MB | fastest, default |
| rolling_hash | 97.5ms | O(n) time, O(1) space       4.6MB | slowest |

### 1406_stone_game_iii (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 98.6ms | O(n) time, O(n) space       4.7MB | fastest, default |
| space_optimized | 101.7ms | O(n) time, O(1) space       4.8MB | slowest |

### 1438_longest_continuous_subarray_with_absolute_diff_limit (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 96.9ms | O(n) time, O(n) space       4.6MB | fastest, default |
| two_deques | 97.9ms | O(n) time, O(n) space       4.7MB | slowest |

### 1499_max_value_of_equation (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| default | 98.7ms | O(n) time, O(n) space       4.6MB | fastest, default |
| deque | 103.8ms | O(n) time, O(n) space       4.7MB | slowest |

### 1547_minimum_cost_to_cut_a_stick (2 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| memoization | 95.2ms | O(m³) time, O(m²) space       4.6MB | fastest |
| default | 100.0ms | O(m³) time, O(m²) space where m = len(cuts) + 2       4.7MB | slowest, default |

### 2104_sum_of_subarray_ranges (3 solutions)

| Method | Time | Complexity | Notes |
|--------|------|------------|-------|
| brute | 96.1ms | O(n^2) time, O(1) space       4.7MB | fastest |
| stack | 96.3ms | O(n) time, O(n) space       4.7MB |  |
| default | 102.6ms | O(n) time, O(n) space       4.6MB | slowest, default |


---

## Methodology

- **Small test data**: Runs actual test cases from `tests/` directory
- **Large n data**: Uses `generate_for_complexity(n)` with n=5000
- **Times**: Median of 5 runs for large n, average for small tests
- **Environment**: Python 3.11

To reproduce:
```bash
python runner/test_runner.py <problem> --all --benchmark
python runner/test_runner.py <problem> --all --estimate
```

# Multi-Solution Problems Reference

> **Status**: Auto-generated Reference
> **Last Updated**: 2025-01-09
> **Total**: 113 problems with multiple solution approaches

This document lists all problems that have multiple solution implementations, enabling comparison of different algorithmic approaches.

---

## Quick Stats

| Category | Count |
|----------|-------|
| Total multi-solution problems | 113 |
| Problems with 2 solutions | 89 |
| Problems with 3 solutions | 21 |
| Problems with 4+ solutions | 3 |

---

## Running Multi-Solution Tests

```bash
# Run default solution
python runner/test_runner.py 0001_two_sum

# Run specific solution variant
python runner/test_runner.py 0001_two_sum --method bruteforce

# Run ALL solutions and compare
python runner/test_runner.py 0001_two_sum --all

# Benchmark all solutions
python runner/test_runner.py 0001_two_sum --all --benchmark

# Complexity estimation
python runner/test_runner.py 0001_two_sum --estimate --all
```

---

## Problems by Category

### Baseline vs Optimal (Educational)

These problems demonstrate the improvement from brute force to optimal solutions:

| Problem | Baseline | Optimal | Speedup |
|---------|----------|---------|---------|
| 0001 Two Sum | `bruteforce` O(n²) | `hash_map` O(n) | n → 1 |
| 0033 Search in Rotated | `linear_scan` O(n) | `binary_search` O(log n) | n → log n |
| 0121 Buy/Sell Stock | `bruteforce` O(n²) | `running_min` O(n) | n → 1 |
| 0162 Find Peak | `linear_scan` O(n) | `binary_search` O(log n) | n → log n |
| 0435 Non-overlapping | `dp` O(n²) | `greedy` O(n log n) | n → log n |
| 0875 Koko Eating | `linear_search` O(n×S) | `binary_search` O(n log S) | S → log S |
| 1011 Capacity to Ship | `linear_search` O(n×S) | `binary_search` O(n log S) | S → log S |

### Bottom-Up vs Top-Down DP

| Problem | Bottom-Up | Top-Down (Memo) |
|---------|-----------|-----------------|
| 0070 Climbing Stairs | `dp_array` | `memoization` |
| 0072 Edit Distance | `dp_2d` | `memoization` |
| 0198 House Robber | `dp_array` | `memoization` |
| 0213 House Robber II | `dp_decomposition` | `memoization` |
| 0312 Burst Balloons | `default` | `memoization` |
| 0322 Coin Change | `dp_bottom_up` | `memoization` |
| 0416 Partition Equal Subset | `dp_1d` | `memoization` |
| 0494 Target Sum | `dp_transform` | `memoization` |
| 0518 Coin Change 2 | `dp_unbounded` | `memoization` |
| 0664 Strange Printer | `default` | `memoization` |
| 0746 Min Cost Climbing | `dp_space_optimized` | `memoization` |
| 1547 Min Cost to Cut | `default` | `memoization` |

### Union-Find vs DFS/BFS

| Problem | Union-Find | Graph Traversal |
|---------|------------|-----------------|
| 0200 Number of Islands | `union_find` | `dfs`, `bfs` |
| 0547 Number of Provinces | `default` | `dfs` |
| 0684 Redundant Connection | `union_find` | `dfs` |
| 0721 Accounts Merge | `union_find` | `dfs` |
| 0990 Equality Equations | `default` | `dfs` |
| 1971 Path Exists in Graph | `union_find` | `bfs` |

### Iterative vs Recursive

| Problem | Iterative | Recursive |
|---------|-----------|-----------|
| 0021 Merge Two Sorted Lists | `iterative` | `recursive` |
| 0025 Reverse Nodes in K-Group | `iterative` | `recursive` |
| 0094 Binary Tree Inorder | `iterative` | `recursive` |
| 0206 Reverse Linked List | `iterative` | `recursive` |

### Graph Algorithms

| Problem | Primary | Alternative |
|---------|---------|-------------|
| 0743 Network Delay Time | `dijkstra` | `bellman_ford` |
| 0787 Cheapest Flights K Stops | `default` | `dijkstra` |

### BFS vs Simulation

| Problem | BFS | Simulation |
|---------|-----|------------|
| 0994 Rotting Oranges | `bfs` O(mn) | `simulation` O((mn)²) |

---

## Complete Problem List

### Array & Two Pointers

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0001 | Two Sum | 2 | `hash_map`, `bruteforce` |
| 0011 | Container With Most Water | 3 | `two_pointers`, `optimized`, `bruteforce` |
| 0015 | 3Sum | 3 | `two_pointers`, `hashset`, `hash` |
| 0016 | 3Sum Closest | 2 | `two_pointers`, `optimized` |
| 0026 | Remove Duplicates | 2 | `two_pointers`, `enumerate` |
| 0027 | Remove Element | 2 | `two_pointers`, `two_ends` |
| 0042 | Trapping Rain Water | 3 | `stack`, `twopointer`, `dp` |
| 0075 | Sort Colors | 2 | `dutch_flag`, `counting` |
| 0080 | Remove Duplicates II | 3 | `two_pointers`, `k_copies`, `counter` |
| 0088 | Merge Sorted Array | 2 | `backward`, `forward` |
| 0121 | Best Time Buy/Sell | 2 | `running_min`, `bruteforce` |
| 0125 | Valid Palindrome | 3 | `two_pointers`, `filtered`, `filtered_pointers` |
| 0167 | Two Sum II | 2 | `two_pointers`, `binary_search` |
| 0238 | Product Except Self | 2 | `prefix_suffix`, `two_pass` |
| 0283 | Move Zeroes | 4 | `two_pointers`, `swap`, `optimized_swap`, `snowball` |
| 0905 | Sort Array by Parity | 2 | `opposite_pointers`, `writer` |
| 0977 | Squares of Sorted Array | 2 | `two_pointers`, `sort` |

### Binary Search

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0033 | Search in Rotated | 2 | `binary_search`, `linear_scan` |
| 0162 | Find Peak Element | 2 | `binary_search`, `linear_scan` |
| 0875 | Koko Eating Bananas | 2 | `binary_search`, `linear_search` |
| 1011 | Capacity to Ship | 2 | `default`, `linear_search` |

### Linked List

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0021 | Merge Two Sorted Lists | 2 | `iterative`, `recursive` |
| 0023 | Merge K Sorted Lists | 3 | `heap`, `divide`, `greedy` |
| 0025 | Reverse Nodes K-Group | 2 | `iterative`, `recursive` |
| 0092 | Reverse Linked List II | 2 | `two_pass`, `one_pass` |
| 0141 | Linked List Cycle | 2 | `floyd`, `hashset` |
| 0142 | Linked List Cycle II | 2 | `floyd`, `hashset` |
| 0206 | Reverse Linked List | 2 | `iterative`, `recursive` |
| 0287 | Find Duplicate Number | 2 | `floyd`, `binary_search` |
| 0876 | Middle of Linked List | 2 | `fast_slow`, `two_pass` |

### Tree

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0094 | Binary Tree Inorder | 3 | `recursive`, `iterative`, `morris` |
| 0102 | Level Order Traversal | 2 | `bfs`, `dfs` |
| 0104 | Maximum Depth | 3 | `recursive`, `bfs`, `iterative_dfs` |
| 0110 | Balanced Binary Tree | 2 | `bottom_up`, `top_down` |
| 0124 | Binary Tree Max Path | 3 | `instance_var`, `nonlocal`, `tuple_return` |
| 0543 | Diameter of Binary Tree | 2 | `instance_var`, `tuple_return` |
| 0968 | Binary Tree Cameras | 2 | `default`, `dp` |

### Graph

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0133 | Clone Graph | 2 | `default`, `bfs` |
| 0200 | Number of Islands | 3 | `dfs`, `bfs`, `union_find` |
| 0207 | Course Schedule | 2 | `default`, `dfs` |
| 0210 | Course Schedule II | 2 | `default`, `dfs` |
| 0417 | Pacific Atlantic | 2 | `default`, `dfs` |
| 0547 | Number of Provinces | 2 | `default`, `dfs` |
| 0684 | Redundant Connection | 2 | `union_find`, `dfs` |
| 0721 | Accounts Merge | 2 | `union_find`, `dfs` |
| 0743 | Network Delay Time | 2 | `dijkstra`, `bellman_ford` |
| 0785 | Is Graph Bipartite | 2 | `default`, `dfs` |
| 0787 | Cheapest Flights K | 2 | `default`, `dijkstra` |
| 0802 | Eventual Safe States | 2 | `default`, `reverse_kahn` |
| 0841 | Keys and Rooms | 2 | `default`, `bfs` |
| 0990 | Equality Equations | 2 | `default`, `dfs` |
| 0994 | Rotting Oranges | 2 | `bfs`, `simulation` |
| 1971 | Path Exists in Graph | 3 | `default`, `bfs`, `union_find` |

### Dynamic Programming

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0010 | Regex Matching | 2 | `default`, `recursive` |
| 0044 | Wildcard Matching | 3 | `default`, `space_optimized`, `greedy` |
| 0055 | Jump Game | 2 | `greedy`, `dp` |
| 0070 | Climbing Stairs | 3 | `dp_space_optimized`, `dp_array`, `memoization` |
| 0072 | Edit Distance | 3 | `dp_2d`, `space_optimized`, `memoization` |
| 0198 | House Robber | 3 | `dp_space_optimized`, `dp_array`, `memoization` |
| 0213 | House Robber II | 2 | `dp_decomposition`, `memoization` |
| 0312 | Burst Balloons | 2 | `default`, `memoization` |
| 0322 | Coin Change | 3 | `dp_bottom_up`, `memoization`, `bfs` |
| 0337 | House Robber III | 2 | `default`, `memo` |
| 0416 | Partition Equal Subset | 3 | `dp_1d`, `dp_2d`, `memoization` |
| 0435 | Non-overlapping Intervals | 2 | `default`, `dp` |
| 0486 | Predict the Winner | 2 | `default`, `space_optimized` |
| 0494 | Target Sum | 2 | `dp_transform`, `memoization` |
| 0516 | Longest Palindromic Subseq | 2 | `default`, `interval_dp` |
| 0518 | Coin Change 2 | 2 | `dp_unbounded`, `memoization` |
| 0664 | Strange Printer | 2 | `default`, `memoization` |
| 0746 | Min Cost Climbing | 3 | `dp_space_optimized`, `dp_array`, `memoization` |
| 0877 | Stone Game | 2 | `default`, `dp` |
| 1143 | Longest Common Subseq | 2 | `default`, `space_optimized` |
| 1406 | Stone Game III | 2 | `default`, `space_optimized` |
| 1547 | Min Cost to Cut Stick | 2 | `default`, `memoization` |

### Sliding Window & String

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0003 | Longest Substring | 3 | `default`, `dict`, `set` |
| 0028 | strStr() | 2 | `default`, `rabin_karp` |
| 0076 | Minimum Window Substring | 2 | `sliding_window`, `sliding_window_filtered` |
| 0209 | Minimum Size Subarray | 2 | `sliding_window`, `binary_search` |
| 0214 | Shortest Palindrome | 2 | `default`, `rolling_hash` |
| 0459 | Repeated Substring | 2 | `default`, `concatenation` |
| 0560 | Subarray Sum Equals K | 2 | `prefix`, `brute` |
| 0680 | Valid Palindrome II | 3 | `two_pointers`, `recursive`, `iterative` |
| 1392 | Longest Happy Prefix | 2 | `default`, `rolling_hash` |

### Stack & Monotonic

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0084 | Largest Rectangle | 2 | `sentinel`, `twopass` |
| 0085 | Maximal Rectangle | 2 | `stack`, `dp` |
| 0496 | Next Greater Element I | 2 | `stack`, `brute` |
| 0503 | Next Greater Element II | 2 | `twopass`, `concat` |
| 0739 | Daily Temperatures | 2 | `stack`, `backward` |
| 0907 | Sum of Subarray Mins | 2 | `contribution`, `single` |
| 2104 | Sum of Subarray Ranges | 2 | `stack`, `brute` |

### Heap & Priority Queue

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0215 | Kth Largest Element | 2 | `quickselect`, `heap` |
| 0218 | The Skyline Problem | 2 | `heap`, `sortedlist` |
| 0253 | Meeting Rooms II | 2 | `heap`, `sweep` |
| 0295 | Find Median Stream | 2 | `default`, `sorted_list` |
| 0347 | Top K Frequent | 2 | `heap`, `bucket` |
| 0621 | Task Scheduler | 2 | `math`, `heap` |

### Trie

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0208 | Implement Trie | 2 | `default`, `array` |
| 0211 | Add and Search Word | 2 | `default`, `iterative` |
| 0212 | Word Search II | 2 | `default`, `simple` |
| 0648 | Replace Words | 2 | `default`, `hashset` |
| 1268 | Search Suggestions | 3 | `default`, `binary_search`, `trie_dfs` |

### Backtracking

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0046 | Permutations | 2 | `backtracking`, `swap` |
| 0051 | N-Queens | 2 | `sets`, `bitmask` |
| 0052 | N-Queens II | 2 | `default`, `bitmask` |
| 0078 | Subsets | 2 | `default`, `bitmask` |
| 0131 | Palindrome Partitioning | 2 | `default`, `naive` |

### Data Structures

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0307 | Range Sum Query Mutable | 2 | `bit`, `segment_tree` |
| 0315 | Count Smaller After Self | 2 | `bit`, `merge_sort` |

### Other

| ID | Problem | Solutions | Variants |
|----|---------|-----------|----------|
| 0056 | Merge Intervals | 2 | `sort_merge`, `graph_components` |
| 0202 | Happy Number | 2 | `floyd`, `hashset` |
| 0542 | 01 Matrix | 2 | `bfs`, `dp` |
| 1094 | Car Pooling | 2 | `difference`, `events` |

---

## Adding New Multi-Solution Problems

When adding a new solution variant:

1. Add new class with same method name as existing solutions
2. Add entry to `SOLUTIONS` dict with descriptive key
3. Run `--all` to verify all solutions pass
4. Run `--all --benchmark` to compare performance
5. Update this reference document

See [Solution Contract](../contracts/solution-contract.md) for full specification.

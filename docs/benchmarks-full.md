# Full Benchmark Data (n=5000)

[← 返回 Spotlight](benchmarks.md#large-n-spotlight-n5000)

共 **83** 題有多解法可比較。

## All Problems

| # | Problem | Fast | Slow | Speedup | Time Complexity | Space Complexity |
|--:|---------|------|------|--------:|-----------------|------------------|
| 0010 | Regex Matching | Top-down Memo (0.08ms) | Bottom-up DP (5.3s) | 62,000× | O(mn) vs O(mn) | O(m*n) vs O(m*n) |
| 0044 | Wildcard Match | Greedy Backtrack (1.4ms) | 2D DP Table (10.0s) | 7,000× | O(mn) vs O(mn) | O(1) vs O(m*n) |
| 0011 | Container Water | Two Pointers (0.75ms) | Nested Loops (4.9s) | 7,000× | O(n) vs O(n^2) | O(1) vs O(1) |
| 0121 | Buy Sell Stock | Running Min (2.0ms) | Nested Loops (3.1s) | 2,000× | O(n) vs O(n²) | O(1) vs O(1) |
| 0416 | Partition Sum | 2D DP Table (0.08ms) | 1D DP Space-Opt (96.6ms) | 1,000× | O(n  target) vs O(n  target) | O(n * target) vs O(target) |
| 0016 | 3Sum Closest | Two Ptr+Prune (1.1ms) | Two Ptr Basic (1.4s) | 1,000× | O(n²) vs O(n²) | O(1) vs O(1) |
| 0435 | Non-Overlap Intv | Greedy Sort (5.0ms) | DP Array (3.1s) | 617× | O(n log n) vs O(n²) | O(1) vs O(n) |
| 0001 | Two Sum | Hash Map (0.66ms) | Nested Loops (70.1ms) | 106× | O(n) vs O(n²) | O(n) vs O(1) |
| 0494 | Target Sum | DP Transform (0.04ms) | Memoization (3.2ms) | 73× | O(n  target) vs O(n  sum) | O(target) vs O(n * sum) |
| 0875 | Koko Bananas | Binary Search (14.6ms) | Linear Search (1.1s) | 72× | O(n log m) vs O(n × m) | O(1) vs O(1) |
| 2104 | Sum Of Subarray  | Stack (4.5ms) | Brute (305.5ms) | 68× | O(n) vs O(n^2) | O(n) vs O(1) |
| 1011 | Capacity To Ship | Default (10.3ms) | Linear Search (343.8ms) | 33× | O(n log S) vs O(n  S) | O(1) vs O(1) |
| 0125 | Valid Palindrome | Default (0.03ms) | Filtered Pointe (0.80ms) | 23× | O(n) vs O(n) | O(1) vs O(n) |
| 0459 | Repeated Substri | Concatenation (0.06ms) | Default (0.97ms) | 17× | O(n) vs O(n) | O(n) vs O(n) |
| 0496 | Next Greater Ele | Default (0.73ms) | Brute (9.4ms) | 13× | O(n + m) vs O(m  n) | O(n) vs O(1) |
| 0055 | Jump Game | Greedy (1.7ms) | DP Array (10.9ms) | 7× | O(n) vs O(n^2) | O(1) vs O(n) |
| 1392 | Longest Happy Pr | Default (1.5ms) | Rolling Hash (7.5ms) | 5× | O(n) vs O(n) | O(n) vs O(1) |
| 0110 | Balanced Binary  | Default (7.7ms) | Top Down (35.6ms) | 5× | O(n) vs O(n²) | O(h) vs O(h) |
| 1094 | Car Pooling | Difference (5.4ms) | Events (18.1ms) | 3× | O(n + m) vs O(n log n) | O(m) vs O(n) |
| 0200 | Number Of Island | Dfs (3.1ms) | Union Find (9.7ms) | 3× | O(mn) vs O(mn  α(mn)) | O(m*n) vs O(m*n) |
| 0990 | Satisfiability O | Dfs (1.6ms) | Default (4.5ms) | 3× | O(n + 26) vs O(n × α(26)) | O(26) vs O(1) |
| 0141 | Linked List Cycl | Default (3.1ms) | Hashset (8.3ms) | 3× | O(n) vs O(n) | O(1) vs O(n) |
| 0023 | Merge K Lists | Heap Merge (17.3ms) | Sequential (46.4ms) | 3× | — | — |
| 0213 | House Robber Ii | Default (0.10ms) | Memoization (0.25ms) | 3× | O(n) vs O(n) | O(1) vs O(n) |
| 0253 | Meeting Rooms Ii | Default (7.6ms) | Sweep (17.6ms) | 2× | O(n log n) vs O(n log n) | O(n) vs O(n) |
| 0680 | Valid Palindrome | Two Pointers (0.03ms) | Iterative (0.08ms) | 2× | O(n) vs O(n) | O(1) vs O(1) |
| 0033 | Search Rotated | Binary Search (0.48ms) | Linear Scan (1.1ms) | 2× | O(log n) vs O(n) | O(1) vs O(1) |
| 0209 | Minimum Size Sub | Sliding Window (1.6ms) | Binary Search (3.5ms) | 2× | O(n) vs O(n log n) | O(1) vs O(n) |
| 0283 | Move Zeroes | Two Pointers (1.5ms) | Swap (3.1ms) | 2× | O(n) vs O(n) | O(1) vs O(1) |
| 0042 | Trapping Rain | Two Pointers (1.8ms) | Prefix Arrays (3.7ms) | 2× | O(n) vs O(n) | O(1) vs O(n) |
| 0198 | House Robber | Default (0.07ms) | Memoization (0.15ms) | 2× | O(n) vs O(n) | O(1) vs O(n) |
| 0743 | Network Delay Ti | Bellman Ford (9.7ms) | Default (19.4ms) | 2× | O(V × E) vs O((V+E) log V) | O(V) vs O(V+E) |
| 0905 | Sort Array By Pa | Opposite Pointe (2.2ms) | Writer (4.2ms) | 2× | O(n) vs O(n) | O(1) vs O(1) |
| 0322 | Coin Change | Bfs (3.6ms) | Default (6.9ms) | 2× | O(n  amount) vs O(n  amount) | O(amount) vs O(amount) |
| 0202 | Happy Number | Default (0.03ms) | Hashset (0.06ms) | 2× | O(log n) vs O(log n) | O(1) vs O(log n) |
| 0315 | Count Of Smaller | Default (16.6ms) | Merge Sort (29.7ms) | 2× | O(n log n) vs O(n log n) | O(n) vs O(n) |
| 0028 | Find The Index O | Default (0.68ms) | Rabin Karp (1.2ms) | 2× | O(m+n) vs O(m+n) | O(n) vs O(1) |
| 0214 | Shortest Palindr | Default (1.6ms) | Rolling Hash (2.8ms) | 2× | O(n) vs O(n) | O(n) vs O(1) |
| 0516 | Longest Palindro | Interval Dp (6.5s) | Default (11.3s) | 2× | O(n^2) vs O(n^2) | O(n^2) vs O(n^2) |
| 0070 | Climbing Stairs | Dp Space Optimi (0.03ms) | Memoization (0.05ms) | 2× | O(n) vs O(n) | O(1) vs O(n) |
| 1499 | Max Value Of Equ | Default (7.8ms) | Deque (13.0ms) | 2× | O(n) vs O(n) | O(n) vs O(n) |
| 0218 | The Skyline Prob | Default (14.9ms) | Heap (24.4ms) | 2× | O(n log n) vs O(n log n) | O(n) vs O(n) |
| 0134 | Gas Station | Default (1.6ms) | Greedy (2.4ms) | 2× | O(n) vs O(n) | O(1) vs O(1) |
| 0994 | Rotting Oranges | Simulation (0.16ms) | Bfs (0.24ms) | 2× | O((mn)²) vs O(mn) | O(m*n) vs O(m*n) |
| 0084 | Largest Rectangl | Default (2.9ms) | Twopass (4.6ms) | 2× | O(n) vs O(n) | O(n) vs O(n) |
| 0307 | Range Sum Query  | Default (38.2ms) | Bit (58.2ms) | 2× | — | — |
| 0015 | 3Sum | Default (1.5s) | Hash (2.2s) | 2× | O(n²) vs O(n²) | O(1) vs O(n) |
| 0721 | Accounts Merge | Union Find (0.09ms) | Dfs (0.13ms) | 1× | O(n × k × α(n)) vs O(n × k) | O(n × k) vs O(n × k) |
| 0142 | Linked List Cycl | Default (2.8ms) | Hashset (4.1ms) | 1× | O(n) vs O(n) | O(1) vs O(n) |
| 0684 | Redundant Connec | Union Find (0.08ms) | Dfs (0.11ms) | 1× | O(n × α(n)) vs O(n²) | O(n) vs O(n) |
| 0003 | Longest Substrin | Default (1.4ms) | Set (2.0ms) | 1× | O(n) vs O(n) | O(min(n,σ)) vs O(min(n,σ)) |
| 1438 | Longest Continuo | Two Deques (6.9ms) | Default (9.3ms) | 1× | O(n) vs O(n) | O(n) vs O(n) |
| 0295 | Find Median From | Default (7.7ms) | Sorted List (10.1ms) | 1× | — | — |
| 0746 | Min Cost Climbin | Dp Space Optimi (0.52ms) | Default (0.69ms) | 1× | O(n) vs O(n) | O(1) vs O(1) |
| 0542 | 01 Matrix | Dp (6.1ms) | Default (8.0ms) | 1× | O(mn) vs O(mn) | O(1) vs O(m*n) |
| 1029 | Two City Schedul | Default (5.9ms) | Greedy (7.6ms) | 1× | O(n log n) vs O(n log n) | O(1) vs O(1) |
| 0076 | Minimum Window S | Default (2.6ms) | Sliding Window  (3.4ms) | 1× | O(|s| + |t|) vs O(|s| + |t|) | O(|t|) vs O(|s|) |
| 0085 | Maximal Rectangl | Default (2.2ms) | Dp (2.8ms) | 1× | O(rows  cols) vs O(rows  cols) | O(cols) vs O(cols) |
| 0876 | Middle Of The Li | Default (3.3ms) | Two Pass (4.2ms) | 1× | O(n) vs O(n) | O(1) vs O(1) |
| 0503 | Next Greater Ele | Default (3.3ms) | Concat (4.2ms) | 1× | O(n) vs O(n) | O(n) vs O(n) |
| 0080 | Remove Duplicate | Counter (1.6ms) | Default (2.0ms) | 1× | O(n) vs O(n) | O(1) vs O(1) |
| 0072 | Edit Distance | Space Optimized (11.1s) | Default (13.7s) | 1× | O(mn) vs O(mn) | O(min(m,n)) vs O(m*n) |
| 0907 | Sum Of Subarray  | Default (5.3ms) | Contribution (6.4ms) | 1× | O(n) vs O(n) | O(n) vs O(n) |
| 0027 | Remove Element | Two Ends (1.1ms) | Two Pointers (1.3ms) | 1× | O(n) vs O(n) | O(1) vs O(1) |
| 0977 | Squares Of A Sor | Two Pointers (2.2ms) | Default (2.6ms) | 1× | O(n) vs O(n) | O(n) vs O(n) |
| 0135 | Candy | Default (2.1ms) | Two Pass (2.5ms) | 1× | O(n) vs O(n) | O(n) vs O(n) |
| 0162 | Find Peak Elemen | Linear Scan (0.16ms) | Default (0.19ms) | 1× | O(n) vs O(log n) | O(1) vs O(1) |
| 0739 | Daily Temperatur | Backward (2.2ms) | Default (2.5ms) | 1× | O(n) vs O(n) | O(1) vs O(n) |
| 1143 | Longest Common S | Space Optimized (12.5s) | Default (14.4s) | 1× | O(mn) vs O(mn) | O(min(m,n)) vs O(m*n) |
| 0239 | Sliding Window M | Default (3.3ms) | Deque (3.8ms) | 1× | O(n) vs O(n) | O(k) vs O(k) |
| 0327 | Count Of Range S | Merge Sort (25.4ms) | Default (27.9ms) | 1× | O(n log n) vs O(n log n) | O(n) vs O(n) |
| 0215 | Kth Largest Elem | Quickselect (1.8ms) | Heap (2.0ms) | 1× | O(n) vs O(n log k) | O(1) vs O(k) |
| 0026 | Remove Duplicate | Default (0.86ms) | Enumerate (0.93ms) | 1× | O(n) vs O(n) | O(1) vs O(1) |
| 0862 | Shortest Subarra | Default (2.9ms) | Deque (3.1ms) | 1× | O(n) vs O(n) | O(n) vs O(n) |
| 0088 | Merge Sorted Arr | Backward (1.9ms) | Forward (2.0ms) | 1× | O(m+n) vs O(m+n) | O(1) vs O(m) |
| 0056 | Merge Intervals | Sort Merge (5.2ms) | Default (5.4ms) | 1× | O(n log n) vs O(n log n) | O(n) vs O(n) |
| 0968 | Binary Tree Came | Dp (85.0ms) | Default (89.2ms) | 1× | O(n) vs O(n) | O(h) vs O(h) |
| 0045 | Jump Game Ii | Default (1.6ms) | Greedy (1.7ms) | 1× | O(n) vs O(n) | O(1) vs O(1) |
| 0518 | Coin Change 2 | Default (2.2ms) | Dp Unbounded (2.3ms) | 1× | O(n  amount) vs O(n  amount) | O(amount) vs O(amount) |
| 0455 | Assign Cookies | Greedy (3.3ms) | Default (3.4ms) | 1× | O(n log n + m log m) vs O(n log n + m log m) | O(1) vs O(1) |
| 0075 | Sort Colors | Default (1.3ms) | Dutch Flag (1.3ms) | 1× | O(n) vs O(n) | O(1) vs O(1) |
| 0337 | House Robber Iii | Default (88.6ms) | Memo (90.7ms) | 1× | O(n) vs O(n) | O(h) vs O(n) |
| 0922 | Sort Array By Pa | Two Pointers (2.2ms) | Default (2.2ms) | 1× | O(n) vs O(n) | O(1) vs O(1) |

---

## Legend

- **Fast**: Fastest method at n=5000
- **Slow**: Slowest method at n=5000
- **Speedup**: How many times faster the Fast method is
- **Time Complexity**: Big-O time (Fast vs Slow)
- **Space Complexity**: Big-O space (Fast vs Slow)
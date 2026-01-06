---

## Pattern Comparison

### 0/1 Knapsack vs Unbounded Knapsack

| Aspect | 0/1 Knapsack | Unbounded Knapsack |
|--------|--------------|-------------------|
| **Item Usage** | Each item at most once | Items can be reused |
| **1D Iteration** | Backwards (`range(target, num-1, -1)`) | Forwards (`range(coin, amount+1)`) |
| **Examples** | LC 416, 494 | LC 322, 518 |
| **Mental Model** | Selecting from a set | Dispensing from unlimited supply |

### DP Knapsack vs Backtracking

| Aspect | DP Knapsack | Backtracking |
|--------|-------------|--------------|
| **Returns** | Count, min, max, boolean | Actual combinations/selections |
| **Time** | O(n * target) | Exponential (but can prune) |
| **When to Use** | Need aggregate answer | Need to enumerate solutions |
| **Overlapping?** | Yes (same target from many paths) | Depends on problem |

### Boolean vs Count vs Min/Max

| Goal | Operator | Initial Value | Transition |
|------|----------|---------------|------------|
| **Reachable?** | `or` | False, dp[0]=True | `dp[s] = dp[s] or dp[s-item]` |
| **Count ways** | `+=` | 0, dp[0]=1 | `dp[s] += dp[s-item]` |
| **Min items** | `min` | inf, dp[0]=0 | `dp[s] = min(dp[s], dp[s-item]+1)` |



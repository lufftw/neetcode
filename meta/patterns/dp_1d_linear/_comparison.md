---

## Pattern Comparison

### 1D DP vs Greedy

| Aspect | 1D Linear DP | Greedy |
|--------|--------------|--------|
| **Decision** | Considers all subproblems | Local optimal only |
| **Structure** | Overlapping subproblems | Greedy choice property |
| **Example** | House Robber (need dp) | Jump Game (greedy works) |
| **When to use** | Can't prove greedy correctness | Clear greedy choice |

### 1D DP vs 2D DP

| Aspect | 1D Linear DP | 2D DP |
|--------|--------------|-------|
| **State** | Single dimension | Two dimensions |
| **Space** | O(n) → O(1) | O(n*m) → O(n) |
| **Examples** | Climbing Stairs, House Robber | Longest Common Subsequence |
| **Complexity** | Linear transitions | Matrix transitions |

### Additive vs Selective 1D DP

| Pattern | Goal | Operator | Example |
|---------|------|----------|---------|
| **Additive** | Count ways | Sum | LC 70 (Climbing Stairs) |
| **Selective** | Optimize value | Max/Min | LC 198 (House Robber) |

### Space Optimization Summary

| Pattern | Original | Optimized | Key Observation |
|---------|----------|-----------|-----------------|
| Fibonacci-like | O(n) | O(1) | Only need last 2 values |
| Kadane-style | O(n) | O(1) | Only need running best |
| Include/Exclude | O(n) | O(1) | Only need last 2 values |



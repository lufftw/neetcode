# DP 1D Linear Pattern

## API Kernel: `DP1DLinear`

> **Core Mechanism**: Build optimal solutions by combining optimal solutions to smaller subproblems along a single dimension.

**DP 1D Linear** covers dynamic programming problems where the state depends on a single dimension (typically array index or step count). The pattern follows a consistent backbone: define state, establish transitions, handle base cases, and optionally optimize space.

---

## The 1D DP Backbone

Every 1D linear DP problem follows this structure:

| Component | Question to Answer | Example (Climbing Stairs) |
|-----------|-------------------|---------------------------|
| **State** | What does `dp[i]` represent? | Number of ways to reach step i |
| **Transition** | How does `dp[i]` relate to previous states? | `dp[i] = dp[i-1] + dp[i-2]` |
| **Base Case** | What are the initial values? | `dp[0] = 1, dp[1] = 1` |
| **Answer** | Where is the final answer? | `dp[n]` |
| **Space Optimization** | Can we reduce O(n) to O(1)? | Yes, only need last 2 values |

---

## Two Fundamental Patterns

| Pattern | State Definition | Transition Logic | Problems |
|---------|------------------|------------------|----------|
| **Additive (Count)** | `dp[i]` = ways to reach i | Add from all valid previous states | LC 70, 746 |
| **Selective (Max/Min)** | `dp[i]` = optimal value at i | Choose best among options | LC 198, 213, 121 |

---

## Space Optimization

Most 1D DP problems can be optimized from O(n) to O(1) space:

```python
# O(n) space
dp = [0] * (n + 1)
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]
return dp[n]

# O(1) space
prev2, prev1 = 1, 1
for i in range(2, n + 1):
    prev2, prev1 = prev1, prev2 + prev1
return prev1
```

---

## Key Insight: The "Include or Exclude" Decision

Many 1D DP problems boil down to one question at each step:
- **Include** current element (and skip some previous elements)
- **Exclude** current element (and take the result from previous)

This creates the classic transition: `dp[i] = max(dp[i-1], dp[i-2] + value[i])`

---


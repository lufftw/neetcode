# DP Knapsack / Subset Pattern

## API Kernel: `DPKnapsackSubset`

> **Core Mechanism**: Make "take or skip" decisions on items to reach a target capacity or sum.

**DP Knapsack/Subset** covers dynamic programming problems where you select items from a collection to achieve a goal. The fundamental question at each item: **"Should I include this item or not?"**

---

## The "Take or Skip" Decision

Every knapsack/subset problem reduces to this choice at each item:

| Decision | Effect | Transition |
|----------|--------|------------|
| **Take** | Add item to selection, reduce remaining capacity | `dp[i][c] = ... dp[i-1][c - weight[i]] + value[i]` |
| **Skip** | Don't use item, keep capacity | `dp[i][c] = dp[i-1][c]` |

---

## Two Major Variants

| Variant | Item Reuse | Iteration Order | Examples |
|---------|------------|-----------------|----------|
| **0/1 Knapsack** | Each item used at most once | Items outer, capacity inner (reverse for 1D) | LC 416, 494 |
| **Unbounded Knapsack** | Items can be reused | Items outer, capacity inner (forward for 1D) | LC 322, 518 |

---

## State Definition Patterns

| Goal | State | Transition |
|------|-------|------------|
| **Can reach target?** | `dp[c]` = True/False for capacity c | `dp[c] = dp[c] or dp[c - item]` |
| **Count ways to reach** | `dp[c]` = number of ways | `dp[c] += dp[c - item]` |
| **Minimize items to reach** | `dp[c]` = min items needed | `dp[c] = min(dp[c], dp[c - item] + 1)` |

---

## When DP vs Backtracking?

| Use DP | Use Backtracking |
|--------|------------------|
| Need count/min/max of ALL valid selections | Need to enumerate actual selections |
| Target sum is bounded (fits in DP table) | Target is too large for DP table |
| Overlapping subproblems (same target reached multiple ways) | Few/no overlapping subproblems |

**Rule of Thumb**: If "number of ways" or "minimum count," use DP. If "list all combinations," use backtracking.

---

## Space Optimization

Most 2D knapsack DP can be reduced to 1D:

```python
# 2D version
dp = [[0] * (target + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for c in range(target + 1):
        dp[i][c] = dp[i-1][c]  # skip
        if c >= nums[i-1]:
            dp[i][c] = max(dp[i][c], dp[i-1][c - nums[i-1]] + nums[i-1])  # take

# 1D version (iterate capacity backwards for 0/1 knapsack)
dp = [0] * (target + 1)
for num in nums:
    for c in range(target, num - 1, -1):  # backwards!
        dp[c] = max(dp[c], dp[c - num] + num)
```

**Why backwards for 0/1?** To ensure each item is used at most once per iteration.

---


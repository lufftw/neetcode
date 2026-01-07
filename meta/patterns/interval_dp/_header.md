# Interval DP Pattern

## API Kernel: `IntervalDP`

> **Core Mechanism**: Define `dp[i][j]` as the optimal answer for the interval `[i, j]`, then enumerate all possible "split points" `k` to divide the problem into subproblems.

## Why Interval DP?

Interval DP solves problems where:
- The answer depends on a contiguous range/interval
- You need to find the optimal way to process/merge/split the interval
- The order of operations matters (not just which elements)

## Core Insight

The key insight is that for any interval `[i, j]`, there exists some "last operation" that splits it:
- **Matrix Chain Multiplication**: Last multiplication at position `k`
- **Burst Balloons**: Last balloon to burst
- **Polygon Triangulation**: Last triangle to form

By trying all possible last operations and taking the optimal, we build up the solution.

## Universal Template Structure

```python
def interval_dp_template(arr: list) -> int:
    n = len(arr)

    # dp[i][j] = optimal answer for interval [i, j]
    dp = [[0] * n for _ in range(n)]

    # Base case: single elements or empty intervals
    for i in range(n):
        dp[i][i] = base_case(i)

    # Fill by increasing interval length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = initial_value  # inf or -inf

            # Try all split points
            for k in range(i, j):
                candidate = dp[i][k] + dp[k+1][j] + merge_cost(i, k, j)
                dp[i][j] = optimal(dp[i][j], candidate)

    return dp[0][n-1]
```

## Pattern Variants

| Pattern | Split Point | Merge Cost | Example |
|---------|-------------|------------|---------|
| **Matrix Chain** | Where to split multiplication | Product of dimensions | Classic |
| **Burst Balloons** | Last balloon to burst | `nums[i-1]*nums[k]*nums[j+1]` | LC 312 |
| **Polygon Triangulation** | Third vertex of triangle | `v[i]*v[k]*v[j]` | LC 1039 |
| **Optimal BST** | Root of subtree | Frequency sum | Classic |

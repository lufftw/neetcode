# 1547. Minimum Cost to Cut a Stick

## Problem Link
https://leetcode.com/problems/minimum-cost-to-cut-a-stick/

## Difficulty
Hard

## Tags
- Array
- Dynamic Programming
- Sorting

## Pattern
Interval DP - Cutting Problems

## API Kernel
`IntervalDP`

## Problem Summary
Given a stick of length `n` and positions where you must cut, each cut costs the length of the stick being cut. Find the minimum total cost to make all cuts.

## Key Insight

The key is to think about which cut to make **last** in each segment:
- If we cut at position `k` last in segment `[i, j]`
- Cost = length of segment + cost of left + cost of right
- Cost = `(cuts[j] - cuts[i]) + dp[i][k] + dp[k][j]`

Add boundary positions 0 and n to simplify.

## Template Mapping

```python
def minCost(n: int, cuts: list) -> int:
    # Add boundaries and sort
    cuts = sorted([0] + cuts + [n])
    m = len(cuts)

    # dp[i][j] = min cost to cut segment between cuts[i] and cuts[j]
    dp = [[0] * m for _ in range(m)]

    # Fill by increasing gap between cut indices
    for gap in range(2, m):
        for i in range(m - gap):
            j = i + gap
            dp[i][j] = float('inf')

            # Try all intermediate cuts
            for k in range(i + 1, j):
                cost = cuts[j] - cuts[i]  # Length of current segment
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cost)

    return dp[0][m - 1]
```

## Complexity
- Time: O(m³) where m = len(cuts) + 2
- Space: O(m²)

## Why This Problem Third?

This problem shows interval DP on transformed input:
1. Need to add boundary positions
2. Sort the cut positions
3. Work with cut indices, not stick positions

## Common Mistakes

1. **Forgetting boundaries** - Must add 0 and n to cuts
2. **Not sorting** - Cuts must be in order
3. **Wrong cost calculation** - Cost is `cuts[j] - cuts[i]`, not `j - i`

## Related Problems
- LC 312: Burst Balloons (Similar structure)
- LC 1000: Minimum Cost to Merge Stones

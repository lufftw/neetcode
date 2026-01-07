# 1039. Minimum Score Triangulation of Polygon

## Problem Link
https://leetcode.com/problems/minimum-score-triangulation-of-polygon/

## Difficulty
Medium

## Tags
- Array
- Dynamic Programming

## Pattern
Interval DP - Polygon Triangulation

## API Kernel
`IntervalDP`

## Problem Summary
Given a convex polygon with `n` vertices labeled with values, triangulate it to minimize the sum of triangle scores, where each triangle's score is the product of its three vertex values.

## Key Insight

For any edge `(i, j)` of the polygon, there's exactly one triangle that uses this edge. The third vertex `k` must be between `i` and `j`.

Choosing `k` as the third vertex:
- Forms triangle with vertices `i, k, j` and score `values[i] * values[k] * values[j]`
- Leaves two smaller polygons: `[i, k]` and `[k, j]`

## Template Mapping

```python
def minScoreTriangulation(values: list) -> int:
    n = len(values)

    # dp[i][j] = min cost to triangulate polygon from i to j
    dp = [[0] * n for _ in range(n)]

    # Fill by increasing interval length (need at least 3 vertices)
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')

            # Try all possible third vertices
            for k in range(i + 1, j):
                cost = values[i] * values[k] * values[j]
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cost)

    return dp[0][n - 1]
```

## Complexity
- Time: O(n³)
- Space: O(n²)

## Why This Problem Second?

Polygon Triangulation shows the geometric interpretation:
1. Natural visualization of interval DP
2. Edge `(i, j)` defines the subproblem
3. Split point `k` is the third vertex

## Common Mistakes

1. **Wrong loop bounds** - Need `length >= 3` for a triangle
2. **Including endpoints** - `k` must be strictly between `i` and `j`
3. **Forgetting base case** - Adjacent vertices have cost 0

## Related Problems
- LC 312: Burst Balloons (Same structure)
- LC 1000: Minimum Cost to Merge Stones (Generalization)

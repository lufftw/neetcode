# 312. Burst Balloons

## Problem Link
https://leetcode.com/problems/burst-balloons/

## Difficulty
Hard

## Tags
- Array
- Dynamic Programming

## Pattern
Interval DP - Last Element Selection

## API Kernel
`IntervalDP`

## Problem Summary
Given `n` balloons with values `nums[i]`, bursting balloon `i` gives coins `nums[i-1] * nums[i] * nums[i+1]`. After bursting, neighbors become adjacent. Find the maximum coins you can collect.

## Key Insight

Instead of thinking "which balloon to burst first", think **"which balloon to burst LAST"**.

If balloon `k` is the last to burst in interval `[i, j]`:
- Left side `[i, k-1]` and right side `[k+1, j]` are already burst
- Bursting `k` gives `nums[i-1] * nums[k] * nums[j+1]` (boundary values)
- Total = `dp[i][k-1] + dp[k+1][j] + nums[i-1]*nums[k]*nums[j+1]`

This "reverse thinking" makes the subproblems independent!

## Template Mapping

```python
def maxCoins(nums: list) -> int:
    # Add virtual balloons with value 1 at boundaries
    nums = [1] + nums + [1]
    n = len(nums)

    # dp[i][j] = max coins bursting all balloons in (i, j) exclusive
    dp = [[0] * n for _ in range(n)]

    # Fill by increasing interval length
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):  # k is the last balloon to burst
                coins = nums[i] * nums[k] * nums[j]
                dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + coins)

    return dp[0][n - 1]
```

## Complexity
- Time: O(n³) - three nested loops
- Space: O(n²) - 2D DP table

## Why This Problem First?

Burst Balloons is the **canonical** interval DP problem:
1. Clear "last operation" intuition
2. Classic interval DP structure
3. Teaches the "reverse thinking" trick

## Common Mistakes

1. **Thinking forward** - Bursting first makes subproblems dependent
2. **Wrong boundary handling** - Add virtual balloons with value 1
3. **Wrong interval interpretation** - `dp[i][j]` is exclusive `(i, j)`

## Related Problems
- LC 1039: Minimum Score Triangulation (Same pattern)
- LC 1547: Minimum Cost to Cut a Stick (Similar structure)
- LC 546: Remove Boxes (Harder variant)

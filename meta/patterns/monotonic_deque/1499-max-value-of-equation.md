# 1499. Max Value of Equation

## Problem Link
https://leetcode.com/problems/max-value-of-equation/

## Difficulty
Hard

## Tags
- Array
- Queue
- Sliding Window
- Heap (Priority Queue)
- Monotonic Queue

## Pattern
Monotonic Deque - Pair Optimization

## API Kernel
`MonotonicDeque`

## Problem Summary
Given points `(xi, yi)` sorted by x-coordinate and an integer `k`, find the maximum value of `yi + yj + |xi - xj|` where `|xi - xj| <= k` and `i < j`.

## Key Insight

Since points are sorted by x and `i < j`, we have `xj >= xi`, so `|xi - xj| = xj - xi`.

The equation becomes: `yi + yj + xj - xi = (yj + xj) + (yi - xi)`

For each point `j`, we want to maximize `yi - xi` among all valid `i` (where `xj - xi <= k`).

This is exactly a **sliding window maximum** problem:
- Window constraint: `xj - xi <= k`
- Maximize: `yi - xi`

## Template Mapping

```python
from collections import deque

def findMaxValueOfEquation(points: list, k: int) -> int:
    dq = deque()  # Store (x, y-x) with decreasing y-x
    result = float('-inf')

    for x, y in points:
        # Remove points outside window (xj - xi > k)
        while dq and x - dq[0][0] > k:
            dq.popleft()

        # Calculate answer if we have valid candidates
        if dq:
            result = max(result, y + x + dq[0][1])  # yj + xj + (yi - xi)

        # Maintain decreasing order of y-x
        while dq and dq[-1][1] <= y - x:
            dq.pop()

        dq.append((x, y - x))

    return result
```

## Complexity
- Time: O(n) - each point enters and exits deque at most once
- Space: O(n) - deque can grow to size n

## Why This Problem Fourth?

This problem shows the pattern's versatility:
1. **Algebraic transformation** - restructure equation to fit pattern
2. **Non-obvious window** - constraint is on x-difference, not index
3. **Store derived values** - deque stores `y-x`, not original values

## Common Mistakes

1. **Wrong window condition** - Check `x - dq[0][0] > k`, not `>= k`
2. **Order of operations** - Update answer BEFORE adding current point
3. **Missing edge case** - Need at least one valid point in deque before computing answer

## Related Problems
- LC 239: Sliding Window Maximum (Basic deque)
- LC 1696: Jump Game VI (DP + deque)
- LC 1425: Constrained Subsequence Sum (DP + deque)

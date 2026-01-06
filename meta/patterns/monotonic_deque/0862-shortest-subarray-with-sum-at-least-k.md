# 862. Shortest Subarray with Sum at Least K

## Problem Link
https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/

## Difficulty
Hard

## Tags
- Array
- Binary Search
- Queue
- Sliding Window
- Heap (Priority Queue)
- Prefix Sum
- Monotonic Queue

## Pattern
Monotonic Deque - Prefix Sum Optimization

## API Kernel
`MonotonicDeque`

## Problem Summary
Given an integer array `nums` and an integer `k`, return the length of the shortest non-empty subarray with sum at least `k`. Return -1 if no such subarray exists.

## Key Insight

With **negative numbers**, we can't use simple sliding window. Instead:
1. Use **prefix sums**: `sum(nums[i:j]) = prefix[j] - prefix[i]`
2. For each `j`, find smallest `i < j` where `prefix[j] - prefix[i] >= k`
3. Maintain **increasing monotonic deque** of prefix sums

Why increasing? If `prefix[i1] >= prefix[i2]` where `i1 < i2`, then `i1` is dominated: using `i2` gives both a larger sum difference and a shorter subarray.

## Template Mapping

```python
from collections import deque

def shortestSubarray(nums: list, k: int) -> int:
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    dq = deque()  # Indices with increasing prefix values
    result = float('inf')

    for j in range(n + 1):
        # Try to find valid subarray ending at j
        while dq and prefix[j] - prefix[dq[0]] >= k:
            result = min(result, j - dq.popleft())

        # Maintain increasing order
        while dq and prefix[dq[-1]] >= prefix[j]:
            dq.pop()

        dq.append(j)

    return result if result != float('inf') else -1
```

## Complexity
- Time: O(n) - each index enters and exits deque at most once
- Space: O(n) - prefix array and deque

## Why This Problem Third?

This problem combines multiple concepts:
1. **Prefix sum transformation** - convert to prefix differences
2. **Monotonic deque for optimization** - find best starting index
3. **Handles negative numbers** - unlike simple sliding window

## Common Mistakes

1. **Forgetting prefix[0] = 0** - Need index 0 for subarrays starting from beginning
2. **Wrong deque order** - Must be increasing for this problem
3. **Not popping found elements** - Once we find a valid `i`, we pop it (won't give shorter answer for later `j`)

## Related Problems
- LC 209: Minimum Size Subarray Sum (Positive only, simpler)
- LC 560: Subarray Sum Equals K (Count, not length)
- LC 1074: Number of Submatrices That Sum to Target (2D extension)

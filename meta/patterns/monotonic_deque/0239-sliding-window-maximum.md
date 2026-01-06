# 239. Sliding Window Maximum

## Problem Link
https://leetcode.com/problems/sliding-window-maximum/

## Difficulty
Hard

## Tags
- Array
- Queue
- Sliding Window
- Heap (Priority Queue)
- Monotonic Queue

## Pattern
Monotonic Deque - Sliding Maximum

## API Kernel
`MonotonicDeque`

## Problem Summary
Given an integer array `nums` and a sliding window of size `k` moving from left to right, return an array of the maximum value in each window position.

## Key Insight

A max-heap would give O(log k) per element. But with a monotonic deque, we achieve O(1) amortized:
- Elements enter the deque once and exit at most once
- The front always contains the current window's maximum
- Dominated elements are removed immediately

The deque maintains **decreasing order**: if we're looking for max, any smaller elements that came before the current element are useless.

## Template Mapping

```python
from collections import deque

def maxSlidingWindow(nums: list, k: int) -> list:
    dq = deque()  # Store indices, values are decreasing
    result = []

    for i, num in enumerate(nums):
        # Remove out-of-window elements from front
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements from back (they'll never be max)
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # Window is complete (has k elements)
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

## Complexity
- Time: O(n) - each element enters and exits deque at most once
- Space: O(k) - deque stores at most k elements

## Why This Problem First?

This is the **canonical** monotonic deque problem:
1. Fixed window size - simplest case
2. Pure max query - no additional computation
3. Clear demonstration of the "remove dominated" principle

## Common Mistakes

1. **Using `<=` vs `<`** - For max, use `<` to remove strictly smaller; for min, use `>`
2. **Forgetting to remove stale elements** - Must check `dq[0] < i - k + 1`
3. **Not waiting for full window** - Only add to result when `i >= k - 1`

## Related Problems
- LC 1438: Longest Continuous Subarray (Min-max deque)
- LC 862: Shortest Subarray with Sum at Least K (Prefix sum + deque)
- LC 1696: Jump Game VI (DP with monotonic deque)

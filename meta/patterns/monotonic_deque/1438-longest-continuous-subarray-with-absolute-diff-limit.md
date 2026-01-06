# 1438. Longest Continuous Subarray With Absolute Diff Limit

## Problem Link
https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-limit/

## Difficulty
Medium

## Tags
- Array
- Queue
- Sliding Window
- Heap (Priority Queue)
- Monotonic Queue

## Pattern
Monotonic Deque - Two Deques (Max + Min)

## API Kernel
`MonotonicDeque`

## Problem Summary
Given an array of integers `nums` and an integer `limit`, return the size of the longest non-empty subarray such that the absolute difference between any two elements is less than or equal to `limit`.

## Key Insight

The absolute difference between any two elements in a subarray equals `max - min` of that subarray. So we need to find the longest window where `max - min <= limit`.

We maintain **two deques**:
- One for maximum (decreasing order)
- One for minimum (increasing order)

When `max - min > limit`, shrink window from the left.

## Template Mapping

```python
from collections import deque

def longestSubarray(nums: list, limit: int) -> int:
    max_dq = deque()  # Decreasing: front is max
    min_dq = deque()  # Increasing: front is min
    left = 0
    result = 0

    for right, num in enumerate(nums):
        # Maintain max deque
        while max_dq and nums[max_dq[-1]] < num:
            max_dq.pop()
        max_dq.append(right)

        # Maintain min deque
        while min_dq and nums[min_dq[-1]] > num:
            min_dq.pop()
        min_dq.append(right)

        # Shrink window if constraint violated
        while nums[max_dq[0]] - nums[min_dq[0]] > limit:
            left += 1
            if max_dq[0] < left:
                max_dq.popleft()
            if min_dq[0] < left:
                min_dq.popleft()

        result = max(result, right - left + 1)

    return result
```

## Complexity
- Time: O(n) - each element enters/exits each deque at most once
- Space: O(n) - deques can grow to size n

## Why This Problem Second?

This problem extends the base pattern:
1. **Two deques** instead of one
2. **Variable window size** instead of fixed
3. **Constraint-based shrinking** instead of fixed-size sliding

## Common Mistakes

1. **Only checking one deque** - Must remove from both when shrinking
2. **Wrong comparison** - Max deque removes smaller, min deque removes larger
3. **Off-by-one in left pointer** - Must check `dq[0] < left`, not `<= left`

## Related Problems
- LC 239: Sliding Window Maximum (Single deque, fixed window)
- LC 1425: Constrained Subsequence Sum (DP + deque)
- LC 1696: Jump Game VI (DP + deque)

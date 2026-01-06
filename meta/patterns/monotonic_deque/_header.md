# Monotonic Deque Pattern

## API Kernel: `MonotonicDeque`

> **Core Mechanism**: Maintain a deque of indices where values are monotonic (increasing or decreasing), enabling O(1) access to window extrema (max/min) while supporting efficient front/back operations.

## Why Monotonic Deque?

Monotonic Deque solves problems where:
- You need the maximum or minimum within a sliding window
- Window size can be fixed or variable
- You need to query extrema as the window moves

## Core Insight

The key insight is that when a new element enters the window:
1. **Remove stale elements** from the front (out of window range)
2. **Remove dominated elements** from the back (will never be the answer)
3. **The front always contains the answer** for the current window

For a max deque: if `nums[i] >= nums[j]` where `i > j`, then `j` will never be the maximum for any window containing `i`. So we can safely remove `j` from the deque.

## Universal Template Structure

```python
from collections import deque

def monotonic_deque_max(nums: list, k: int) -> list:
    """Sliding window maximum with window size k."""
    dq = deque()  # Store indices
    result = []

    for i, num in enumerate(nums):
        # Remove indices out of window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove dominated elements (for max deque)
        while dq and nums[dq[-1]] <= num:
            dq.pop()

        dq.append(i)

        # Window is fully formed
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

## Pattern Variants

| Pattern | Deque Order | Use Case | Example |
|---------|-------------|----------|---------|
| **Sliding Max** | Decreasing | Maximum in window | LC 239 |
| **Sliding Min** | Increasing | Minimum in window | LC 1438 |
| **Prefix Sum + Deque** | Increasing | Min/max prefix for subarray | LC 862 |
| **Pair Optimization** | Custom | Optimize pair selection | LC 1499 |

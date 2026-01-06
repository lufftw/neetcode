## Universal Templates

### Template 1: Sliding Window Maximum (Fixed Size)

```python
from collections import deque

def sliding_window_max(nums: list, k: int) -> list:
    """
    Return maximum in each window of size k.
    Time: O(n), Space: O(k)
    """
    dq = deque()  # Store indices, values decreasing
    result = []

    for i, num in enumerate(nums):
        # Remove out-of-window indices
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements (they're dominated)
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

**Use for**: LC 239, fixed-size window extrema

---

### Template 2: Two Deques for Max-Min Constraint

```python
from collections import deque

def longest_subarray_max_min(nums: list, limit: int) -> int:
    """
    Longest subarray where max - min <= limit.
    Time: O(n), Space: O(n)
    """
    max_dq = deque()  # Decreasing
    min_dq = deque()  # Increasing
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

        # Shrink if constraint violated
        while nums[max_dq[0]] - nums[min_dq[0]] > limit:
            left += 1
            if max_dq[0] < left:
                max_dq.popleft()
            if min_dq[0] < left:
                min_dq.popleft()

        result = max(result, right - left + 1)

    return result
```

**Use for**: LC 1438, problems needing both max and min

---

### Template 3: Prefix Sum + Monotonic Deque

```python
from collections import deque

def shortest_subarray_sum_k(nums: list, k: int) -> int:
    """
    Shortest subarray with sum >= k (handles negatives).
    Time: O(n), Space: O(n)
    """
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    dq = deque()  # Increasing prefix values
    result = float('inf')

    for j in range(n + 1):
        # Find valid subarray
        while dq and prefix[j] - prefix[dq[0]] >= k:
            result = min(result, j - dq.popleft())

        # Maintain increasing order
        while dq and prefix[dq[-1]] >= prefix[j]:
            dq.pop()

        dq.append(j)

    return result if result != float('inf') else -1
```

**Use for**: LC 862, subarray sum with negative numbers

---

### Template 4: Transform and Optimize

```python
from collections import deque

def max_value_equation(points: list, k: int) -> int:
    """
    Maximize yi + yj + |xi - xj| where |xi - xj| <= k.
    Points sorted by x. Rewrite as (yj + xj) + (yi - xi).
    Time: O(n), Space: O(n)
    """
    dq = deque()  # (x, y-x) with decreasing y-x
    result = float('-inf')

    for x, y in points:
        # Remove points outside window
        while dq and x - dq[0][0] > k:
            dq.popleft()

        # Calculate answer with best candidate
        if dq:
            result = max(result, y + x + dq[0][1])

        # Maintain decreasing y-x
        while dq and dq[-1][1] <= y - x:
            dq.pop()

        dq.append((x, y - x))

    return result
```

**Use for**: LC 1499, pair optimization with distance constraint

---

## Quick Reference

| Problem Type | Template | Deque Order | Key Step |
|-------------|----------|-------------|----------|
| Fixed window max/min | Template 1 | Decreasing/Increasing | Remove out-of-window |
| Variable window constraint | Template 2 | Both | Shrink when violated |
| Subarray sum (negatives) | Template 3 | Increasing | Pop when valid |
| Pair optimization | Template 4 | Based on optimization | Transform equation |

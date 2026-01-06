# Monotonic Deque Pattern

## Table of Contents

1. [API Kernel: `MonotonicDeque`](#1-api-kernel-monotonicdeque)
2. [Why Monotonic Deque?](#2-why-monotonic-deque)
3. [Core Insight](#3-core-insight)
4. [Universal Template Structure](#4-universal-template-structure)
5. [Pattern Variants](#5-pattern-variants)
6. [Problem Link](#6-problem-link)
7. [Difficulty](#7-difficulty)
8. [Tags](#8-tags)
9. [Pattern](#9-pattern)
10. [API Kernel](#10-api-kernel)
11. [Problem Summary](#11-problem-summary)
12. [Key Insight](#12-key-insight)
13. [Template Mapping](#13-template-mapping)
14. [Complexity](#14-complexity)
15. [Why This Problem First?](#15-why-this-problem-first)
16. [Common Mistakes](#16-common-mistakes)
17. [Related Problems](#17-related-problems)
18. [Problem Link](#18-problem-link)
19. [Difficulty](#19-difficulty)
20. [Tags](#20-tags)
21. [Pattern](#21-pattern)
22. [API Kernel](#22-api-kernel)
23. [Problem Summary](#23-problem-summary)
24. [Key Insight](#24-key-insight)
25. [Template Mapping](#25-template-mapping)
26. [Complexity](#26-complexity)
27. [Why This Problem Second?](#27-why-this-problem-second)
28. [Common Mistakes](#28-common-mistakes)
29. [Related Problems](#29-related-problems)
30. [Problem Link](#30-problem-link)
31. [Difficulty](#31-difficulty)
32. [Tags](#32-tags)
33. [Pattern](#33-pattern)
34. [API Kernel](#34-api-kernel)
35. [Problem Summary](#35-problem-summary)
36. [Key Insight](#36-key-insight)
37. [Template Mapping](#37-template-mapping)
38. [Complexity](#38-complexity)
39. [Why This Problem Third?](#39-why-this-problem-third)
40. [Common Mistakes](#40-common-mistakes)
41. [Related Problems](#41-related-problems)
42. [Problem Link](#42-problem-link)
43. [Difficulty](#43-difficulty)
44. [Tags](#44-tags)
45. [Pattern](#45-pattern)
46. [API Kernel](#46-api-kernel)
47. [Problem Summary](#47-problem-summary)
48. [Key Insight](#48-key-insight)
49. [Template Mapping](#49-template-mapping)
50. [Complexity](#50-complexity)
51. [Why This Problem Fourth?](#51-why-this-problem-fourth)
52. [Common Mistakes](#52-common-mistakes)
53. [Related Problems](#53-related-problems)
54. [Problem Comparison](#54-problem-comparison)
55. [Pattern Evolution](#55-pattern-evolution)
56. [Key Differences](#56-key-differences)
57. [Decision Tree](#57-decision-tree)
58. [Pattern Selection Guide](#58-pattern-selection-guide)
59. [Monotonic Deque vs Other Approaches](#59-monotonic-deque-vs-other-approaches)
60. [Key Indicators for Monotonic Deque](#60-key-indicators-for-monotonic-deque)
61. [Universal Templates](#61-universal-templates)
62. [Quick Reference](#62-quick-reference)

---

## 1. API Kernel: `MonotonicDeque`

> **Core Mechanism**: Maintain a deque of indices where values are monotonic (increasing or decreasing), enabling O(1) access to window extrema (max/min) while supporting efficient front/back operations.

## 2. Why Monotonic Deque?

Monotonic Deque solves problems where:
- You need the maximum or minimum within a sliding window
- Window size can be fixed or variable
- You need to query extrema as the window moves

## 3. Core Insight

The key insight is that when a new element enters the window:
1. **Remove stale elements** from the front (out of window range)
2. **Remove dominated elements** from the back (will never be the answer)
3. **The front always contains the answer** for the current window

For a max deque: if `nums[i] >= nums[j]` where `i > j`, then `j` will never be the maximum for any window containing `i`. So we can safely remove `j` from the deque.

## 4. Universal Template Structure

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

## 5. Pattern Variants

| Pattern | Deque Order | Use Case | Example |
|---------|-------------|----------|---------|
| **Sliding Max** | Decreasing | Maximum in window | LC 239 |
| **Sliding Min** | Increasing | Minimum in window | LC 1438 |
| **Prefix Sum + Deque** | Increasing | Min/max prefix for subarray | LC 862 |
| **Pair Optimization** | Custom | Optimize pair selection | LC 1499 |

---

# 239. Sliding Window Maximum

## 6. Problem Link
https://leetcode.com/problems/sliding-window-maximum/

## 7. Difficulty
Hard

## 8. Tags
- Array
- Queue
- Sliding Window
- Heap (Priority Queue)
- Monotonic Queue

## 9. Pattern
Monotonic Deque - Sliding Maximum

## 10. API Kernel
`MonotonicDeque`

## 11. Problem Summary
Given an integer array `nums` and a sliding window of size `k` moving from left to right, return an array of the maximum value in each window position.

## 12. Key Insight

A max-heap would give O(log k) per element. But with a monotonic deque, we achieve O(1) amortized:
- Elements enter the deque once and exit at most once
- The front always contains the current window's maximum
- Dominated elements are removed immediately

The deque maintains **decreasing order**: if we're looking for max, any smaller elements that came before the current element are useless.

## 13. Template Mapping

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

## 14. Complexity
- Time: O(n) - each element enters and exits deque at most once
- Space: O(k) - deque stores at most k elements

## 15. Why This Problem First?

This is the **canonical** monotonic deque problem:
1. Fixed window size - simplest case
2. Pure max query - no additional computation
3. Clear demonstration of the "remove dominated" principle

## 16. Common Mistakes

1. **Using `<=` vs `<`** - For max, use `<` to remove strictly smaller; for min, use `>`
2. **Forgetting to remove stale elements** - Must check `dq[0] < i - k + 1`
3. **Not waiting for full window** - Only add to result when `i >= k - 1`

## 17. Related Problems
- LC 1438: Longest Continuous Subarray (Min-max deque)
- LC 862: Shortest Subarray with Sum at Least K (Prefix sum + deque)
- LC 1696: Jump Game VI (DP with monotonic deque)

---

# 1438. Longest Continuous Subarray With Absolute Diff Limit

## 18. Problem Link
https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-limit/

## 19. Difficulty
Medium

## 20. Tags
- Array
- Queue
- Sliding Window
- Heap (Priority Queue)
- Monotonic Queue

## 21. Pattern
Monotonic Deque - Two Deques (Max + Min)

## 22. API Kernel
`MonotonicDeque`

## 23. Problem Summary
Given an array of integers `nums` and an integer `limit`, return the size of the longest non-empty subarray such that the absolute difference between any two elements is less than or equal to `limit`.

## 24. Key Insight

The absolute difference between any two elements in a subarray equals `max - min` of that subarray. So we need to find the longest window where `max - min <= limit`.

We maintain **two deques**:
- One for maximum (decreasing order)
- One for minimum (increasing order)

When `max - min > limit`, shrink window from the left.

## 25. Template Mapping

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

## 26. Complexity
- Time: O(n) - each element enters/exits each deque at most once
- Space: O(n) - deques can grow to size n

## 27. Why This Problem Second?

This problem extends the base pattern:
1. **Two deques** instead of one
2. **Variable window size** instead of fixed
3. **Constraint-based shrinking** instead of fixed-size sliding

## 28. Common Mistakes

1. **Only checking one deque** - Must remove from both when shrinking
2. **Wrong comparison** - Max deque removes smaller, min deque removes larger
3. **Off-by-one in left pointer** - Must check `dq[0] < left`, not `<= left`

## 29. Related Problems
- LC 239: Sliding Window Maximum (Single deque, fixed window)
- LC 1425: Constrained Subsequence Sum (DP + deque)
- LC 1696: Jump Game VI (DP + deque)

---

# 862. Shortest Subarray with Sum at Least K

## 30. Problem Link
https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/

## 31. Difficulty
Hard

## 32. Tags
- Array
- Binary Search
- Queue
- Sliding Window
- Heap (Priority Queue)
- Prefix Sum
- Monotonic Queue

## 33. Pattern
Monotonic Deque - Prefix Sum Optimization

## 34. API Kernel
`MonotonicDeque`

## 35. Problem Summary
Given an integer array `nums` and an integer `k`, return the length of the shortest non-empty subarray with sum at least `k`. Return -1 if no such subarray exists.

## 36. Key Insight

With **negative numbers**, we can't use simple sliding window. Instead:
1. Use **prefix sums**: `sum(nums[i:j]) = prefix[j] - prefix[i]`
2. For each `j`, find smallest `i < j` where `prefix[j] - prefix[i] >= k`
3. Maintain **increasing monotonic deque** of prefix sums

Why increasing? If `prefix[i1] >= prefix[i2]` where `i1 < i2`, then `i1` is dominated: using `i2` gives both a larger sum difference and a shorter subarray.

## 37. Template Mapping

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

## 38. Complexity
- Time: O(n) - each index enters and exits deque at most once
- Space: O(n) - prefix array and deque

## 39. Why This Problem Third?

This problem combines multiple concepts:
1. **Prefix sum transformation** - convert to prefix differences
2. **Monotonic deque for optimization** - find best starting index
3. **Handles negative numbers** - unlike simple sliding window

## 40. Common Mistakes

1. **Forgetting prefix[0] = 0** - Need index 0 for subarrays starting from beginning
2. **Wrong deque order** - Must be increasing for this problem
3. **Not popping found elements** - Once we find a valid `i`, we pop it (won't give shorter answer for later `j`)

## 41. Related Problems
- LC 209: Minimum Size Subarray Sum (Positive only, simpler)
- LC 560: Subarray Sum Equals K (Count, not length)
- LC 1074: Number of Submatrices That Sum to Target (2D extension)

---

# 1499. Max Value of Equation

## 42. Problem Link
https://leetcode.com/problems/max-value-of-equation/

## 43. Difficulty
Hard

## 44. Tags
- Array
- Queue
- Sliding Window
- Heap (Priority Queue)
- Monotonic Queue

## 45. Pattern
Monotonic Deque - Pair Optimization

## 46. API Kernel
`MonotonicDeque`

## 47. Problem Summary
Given points `(xi, yi)` sorted by x-coordinate and an integer `k`, find the maximum value of `yi + yj + |xi - xj|` where `|xi - xj| <= k` and `i < j`.

## 48. Key Insight

Since points are sorted by x and `i < j`, we have `xj >= xi`, so `|xi - xj| = xj - xi`.

The equation becomes: `yi + yj + xj - xi = (yj + xj) + (yi - xi)`

For each point `j`, we want to maximize `yi - xi` among all valid `i` (where `xj - xi <= k`).

This is exactly a **sliding window maximum** problem:
- Window constraint: `xj - xi <= k`
- Maximize: `yi - xi`

## 49. Template Mapping

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

## 50. Complexity
- Time: O(n) - each point enters and exits deque at most once
- Space: O(n) - deque can grow to size n

## 51. Why This Problem Fourth?

This problem shows the pattern's versatility:
1. **Algebraic transformation** - restructure equation to fit pattern
2. **Non-obvious window** - constraint is on x-difference, not index
3. **Store derived values** - deque stores `y-x`, not original values

## 52. Common Mistakes

1. **Wrong window condition** - Check `x - dq[0][0] > k`, not `>= k`
2. **Order of operations** - Update answer BEFORE adding current point
3. **Missing edge case** - Need at least one valid point in deque before computing answer

## 53. Related Problems
- LC 239: Sliding Window Maximum (Basic deque)
- LC 1696: Jump Game VI (DP + deque)
- LC 1425: Constrained Subsequence Sum (DP + deque)

---

## 54. Problem Comparison

| Problem | Core Pattern | Deque Order | Window Type | Key Insight |
|---------|-------------|-------------|-------------|-------------|
| **LC 239 Sliding Max** | Single max deque | Decreasing | Fixed size | Front = current max |
| **LC 1438 Max-Min Limit** | Two deques (max+min) | Decreasing + Increasing | Variable | Shrink when max-min > limit |
| **LC 862 Shortest Sum >= K** | Prefix sum + deque | Increasing | Variable | Pop when valid, handles negatives |
| **LC 1499 Max Equation** | Transform + deque | Decreasing | x-distance | Rewrite equation to fit pattern |

## 55. Pattern Evolution

```
LC 239 Sliding Window Maximum
    │
    │ Add second deque for min
    │ Variable window size
    ↓
LC 1438 Longest Subarray (Max-Min <= Limit)
    │
    │ Add prefix sum transformation
    │ Handle negative numbers
    ↓
LC 862 Shortest Subarray with Sum >= K
    │
    │ Algebraic transformation
    │ Non-index-based window
    ↓
LC 1499 Max Value of Equation
```

## 56. Key Differences

### 56.1 Deque Order

| Problem | Order | Why |
|---------|-------|-----|
| LC 239, 1499 | Decreasing | Need maximum value |
| LC 1438 | Both | Need both max and min |
| LC 862 | Increasing | Minimize prefix for max difference |

### 56.2 Window Removal

| Problem | When to Remove from Front |
|---------|---------------------------|
| LC 239 | Index out of fixed window |
| LC 1438 | Index before left pointer |
| LC 862 | After using for valid answer |
| LC 1499 | x-distance exceeds k |

### 56.3 What's Stored in Deque

| Problem | Stores |
|---------|--------|
| LC 239 | Indices |
| LC 1438 | Indices |
| LC 862 | Indices (into prefix array) |
| LC 1499 | (x, y-x) tuples |

---

## 57. Decision Tree

```
Start: Need window extrema (max/min)?
            │
            ▼
    ┌───────────────────┐
    │ Fixed or variable │
    │ window size?      │
    └───────────────────┘
            │
    ┌───────┴───────┐
    ▼               ▼
Fixed           Variable
    │               │
    ▼               ▼
LC 239          Need both
Single          max AND min?
deque               │
                ┌───┴───┐
                ▼       ▼
              Yes      No
                │       │
                ▼       ▼
            LC 1438   Negative
            Two       numbers?
            deques        │
                      ┌───┴───┐
                      ▼       ▼
                    Yes      No
                      │       │
                      ▼       ▼
                  LC 862   Simple
                  Prefix   sliding
                  sum      window
```

## 58. Pattern Selection Guide

### 58.1 Use Single Decreasing Deque (LC 239) when:
- Fixed window size
- Need maximum in each window
- Standard sliding window

### 58.2 Use Two Deques (LC 1438) when:
- Need both max and min simultaneously
- Constraint involves max-min difference
- Variable window based on constraint

### 58.3 Use Prefix Sum + Deque (LC 862) when:
- Subarray sum problems
- Array has negative numbers
- Need shortest subarray with sum >= k

### 58.4 Use Transform + Deque (LC 1499) when:
- Equation can be rewritten to separate indices
- Window based on non-index metric (distance, time)
- Pair optimization problems

## 59. Monotonic Deque vs Other Approaches

| Approach | Use When | Complexity |
|----------|----------|------------|
| Monotonic Deque | Sliding window max/min | O(n) |
| Heap | Dynamic max/min, no window constraint | O(n log n) |
| Segment Tree | Random access range queries | O(n log n) |
| Monotonic Stack | Next greater/smaller element | O(n) |

## 60. Key Indicators for Monotonic Deque

| Clue | Pattern |
|------|---------|
| "sliding window maximum/minimum" | LC 239 |
| "longest subarray with max-min <= limit" | LC 1438 |
| "shortest subarray with sum >= k" (with negatives) | LC 862 |
| "maximize expression with distance constraint" | LC 1499 |

---

## 61. Universal Templates

### 61.1 Template 1: Sliding Window Maximum (Fixed Size)

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

### 61.2 Template 2: Two Deques for Max-Min Constraint

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

### 61.3 Template 3: Prefix Sum + Monotonic Deque

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

### 61.4 Template 4: Transform and Optimize

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

## 62. Quick Reference

| Problem Type | Template | Deque Order | Key Step |
|-------------|----------|-------------|----------|
| Fixed window max/min | Template 1 | Decreasing/Increasing | Remove out-of-window |
| Variable window constraint | Template 2 | Both | Shrink when violated |
| Subarray sum (negatives) | Template 3 | Increasing | Pop when valid |
| Pair optimization | Template 4 | Based on optimization | Transform equation |



---



*Document generated for NeetCode Practice Framework — API Kernel: monotonic_deque*

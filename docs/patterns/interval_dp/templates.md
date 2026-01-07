# Interval DP Pattern

## Table of Contents

1. [API Kernel: `IntervalDP`](#1-api-kernel-intervaldp)
2. [Why Interval DP?](#2-why-interval-dp)
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
59. [Complexity Guide](#59-complexity-guide)
60. [Key Indicators for Interval DP](#60-key-indicators-for-interval-dp)
61. [Universal Templates](#61-universal-templates)
62. [Quick Reference](#62-quick-reference)

---

## 1. API Kernel: `IntervalDP`

> **Core Mechanism**: Define `dp[i][j]` as the optimal answer for the interval `[i, j]`, then enumerate all possible "split points" `k` to divide the problem into subproblems.

## 2. Why Interval DP?

Interval DP solves problems where:
- The answer depends on a contiguous range/interval
- You need to find the optimal way to process/merge/split the interval
- The order of operations matters (not just which elements)

## 3. Core Insight

The key insight is that for any interval `[i, j]`, there exists some "last operation" that splits it:
- **Matrix Chain Multiplication**: Last multiplication at position `k`
- **Burst Balloons**: Last balloon to burst
- **Polygon Triangulation**: Last triangle to form

By trying all possible last operations and taking the optimal, we build up the solution.

## 4. Universal Template Structure

```python
def interval_dp_template(arr: list) -> int:
    n = len(arr)

    # dp[i][j] = optimal answer for interval [i, j]
    dp = [[0] * n for _ in range(n)]

    # Base case: single elements or empty intervals
    for i in range(n):
        dp[i][i] = base_case(i)

    # Fill by increasing interval length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = initial_value  # inf or -inf

            # Try all split points
            for k in range(i, j):
                candidate = dp[i][k] + dp[k+1][j] + merge_cost(i, k, j)
                dp[i][j] = optimal(dp[i][j], candidate)

    return dp[0][n-1]
```

## 5. Pattern Variants

| Pattern | Split Point | Merge Cost | Example |
|---------|-------------|------------|---------|
| **Matrix Chain** | Where to split multiplication | Product of dimensions | Classic |
| **Burst Balloons** | Last balloon to burst | `nums[i-1]*nums[k]*nums[j+1]` | LC 312 |
| **Polygon Triangulation** | Third vertex of triangle | `v[i]*v[k]*v[j]` | LC 1039 |
| **Optimal BST** | Root of subtree | Frequency sum | Classic |

---

# 312. Burst Balloons

## 6. Problem Link
https://leetcode.com/problems/burst-balloons/

## 7. Difficulty
Hard

## 8. Tags
- Array
- Dynamic Programming

## 9. Pattern
Interval DP - Last Element Selection

## 10. API Kernel
`IntervalDP`

## 11. Problem Summary
Given `n` balloons with values `nums[i]`, bursting balloon `i` gives coins `nums[i-1] * nums[i] * nums[i+1]`. After bursting, neighbors become adjacent. Find the maximum coins you can collect.

## 12. Key Insight

Instead of thinking "which balloon to burst first", think **"which balloon to burst LAST"**.

If balloon `k` is the last to burst in interval `[i, j]`:
- Left side `[i, k-1]` and right side `[k+1, j]` are already burst
- Bursting `k` gives `nums[i-1] * nums[k] * nums[j+1]` (boundary values)
- Total = `dp[i][k-1] + dp[k+1][j] + nums[i-1]*nums[k]*nums[j+1]`

This "reverse thinking" makes the subproblems independent!

## 13. Template Mapping

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

## 14. Complexity
- Time: O(n³) - three nested loops
- Space: O(n²) - 2D DP table

## 15. Why This Problem First?

Burst Balloons is the **canonical** interval DP problem:
1. Clear "last operation" intuition
2. Classic interval DP structure
3. Teaches the "reverse thinking" trick

## 16. Common Mistakes

1. **Thinking forward** - Bursting first makes subproblems dependent
2. **Wrong boundary handling** - Add virtual balloons with value 1
3. **Wrong interval interpretation** - `dp[i][j]` is exclusive `(i, j)`

## 17. Related Problems
- LC 1039: Minimum Score Triangulation (Same pattern)
- LC 1547: Minimum Cost to Cut a Stick (Similar structure)
- LC 546: Remove Boxes (Harder variant)

---

# 1039. Minimum Score Triangulation of Polygon

## 18. Problem Link
https://leetcode.com/problems/minimum-score-triangulation-of-polygon/

## 19. Difficulty
Medium

## 20. Tags
- Array
- Dynamic Programming

## 21. Pattern
Interval DP - Polygon Triangulation

## 22. API Kernel
`IntervalDP`

## 23. Problem Summary
Given a convex polygon with `n` vertices labeled with values, triangulate it to minimize the sum of triangle scores, where each triangle's score is the product of its three vertex values.

## 24. Key Insight

For any edge `(i, j)` of the polygon, there's exactly one triangle that uses this edge. The third vertex `k` must be between `i` and `j`.

Choosing `k` as the third vertex:
- Forms triangle with vertices `i, k, j` and score `values[i] * values[k] * values[j]`
- Leaves two smaller polygons: `[i, k]` and `[k, j]`

## 25. Template Mapping

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

## 26. Complexity
- Time: O(n³)
- Space: O(n²)

## 27. Why This Problem Second?

Polygon Triangulation shows the geometric interpretation:
1. Natural visualization of interval DP
2. Edge `(i, j)` defines the subproblem
3. Split point `k` is the third vertex

## 28. Common Mistakes

1. **Wrong loop bounds** - Need `length >= 3` for a triangle
2. **Including endpoints** - `k` must be strictly between `i` and `j`
3. **Forgetting base case** - Adjacent vertices have cost 0

## 29. Related Problems
- LC 312: Burst Balloons (Same structure)
- LC 1000: Minimum Cost to Merge Stones (Generalization)

---

# 1547. Minimum Cost to Cut a Stick

## 30. Problem Link
https://leetcode.com/problems/minimum-cost-to-cut-a-stick/

## 31. Difficulty
Hard

## 32. Tags
- Array
- Dynamic Programming
- Sorting

## 33. Pattern
Interval DP - Cutting Problems

## 34. API Kernel
`IntervalDP`

## 35. Problem Summary
Given a stick of length `n` and positions where you must cut, each cut costs the length of the stick being cut. Find the minimum total cost to make all cuts.

## 36. Key Insight

The key is to think about which cut to make **last** in each segment:
- If we cut at position `k` last in segment `[i, j]`
- Cost = length of segment + cost of left + cost of right
- Cost = `(cuts[j] - cuts[i]) + dp[i][k] + dp[k][j]`

Add boundary positions 0 and n to simplify.

## 37. Template Mapping

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

## 38. Complexity
- Time: O(m³) where m = len(cuts) + 2
- Space: O(m²)

## 39. Why This Problem Third?

This problem shows interval DP on transformed input:
1. Need to add boundary positions
2. Sort the cut positions
3. Work with cut indices, not stick positions

## 40. Common Mistakes

1. **Forgetting boundaries** - Must add 0 and n to cuts
2. **Not sorting** - Cuts must be in order
3. **Wrong cost calculation** - Cost is `cuts[j] - cuts[i]`, not `j - i`

## 41. Related Problems
- LC 312: Burst Balloons (Similar structure)
- LC 1000: Minimum Cost to Merge Stones

---

# 664. Strange Printer

## 42. Problem Link
https://leetcode.com/problems/strange-printer/

## 43. Difficulty
Hard

## 44. Tags
- String
- Dynamic Programming

## 45. Pattern
Interval DP - Character Printing

## 46. API Kernel
`IntervalDP`

## 47. Problem Summary
A printer can print a sequence of the same character, and each print covers some substring. Given a string, find the minimum number of turns needed to print it.

## 48. Key Insight

For interval `[i, j]`:
- Base case: print `s[i]` to cover entire interval, then recursively handle rest
- Optimization: if `s[k] == s[i]` for some `k > i`, we can "extend" the first print

When `s[i] == s[j]`:
- `dp[i][j] = dp[i][j-1]` (print s[i] to cover s[j] too)

When `s[i] != s[j]`:
- Try all split points: `dp[i][j] = min(dp[i][k] + dp[k+1][j])`

## 49. Template Mapping

```python
def strangePrinter(s: str) -> int:
    # Remove consecutive duplicates (they don't change answer)
    s = ''.join(c for i, c in enumerate(s) if i == 0 or c != s[i-1])
    n = len(s)

    if n == 0:
        return 0

    # dp[i][j] = min turns to print s[i:j+1]
    dp = [[0] * n for _ in range(n)]

    # Base case: single character needs 1 turn
    for i in range(n):
        dp[i][i] = 1

    # Fill by increasing length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            # Worst case: print s[i] alone, then handle rest
            dp[i][j] = dp[i + 1][j] + 1

            # Optimization: extend s[i]'s print if s[k] == s[i]
            for k in range(i + 1, j + 1):
                if s[k] == s[i]:
                    left = dp[i + 1][k - 1] if k > i + 1 else 0
                    right = dp[k][j]
                    dp[i][j] = min(dp[i][j], left + right)

    return dp[0][n - 1]
```

## 50. Complexity
- Time: O(n³)
- Space: O(n²)

## 51. Why This Problem Fourth?

Strange Printer shows non-standard interval DP:
1. Optimization based on character matching
2. Different recurrence structure
3. Preprocessing to remove duplicates

## 52. Common Mistakes

1. **Not removing duplicates** - Consecutive same chars waste computation
2. **Wrong base case** - Single char needs 1 turn
3. **Missing the optimization** - When `s[k] == s[i]`, we can combine prints

## 53. Related Problems
- LC 546: Remove Boxes (Similar character-based DP)
- LC 1000: Minimum Cost to Merge Stones

---

## 54. Problem Comparison

| Problem | Interval Meaning | Split Point | Merge Cost | Optimization |
|---------|------------------|-------------|------------|--------------|
| **LC 312 Burst Balloons** | Balloons in (i, j) | Last to burst | `nums[i]*nums[k]*nums[j]` | Maximize |
| **LC 1039 Polygon** | Vertices i to j | Third vertex | `v[i]*v[k]*v[j]` | Minimize |
| **LC 1547 Cut Stick** | Between cuts i, j | Cut position | `cuts[j] - cuts[i]` | Minimize |
| **LC 664 Strange Printer** | Characters i to j | Matching char | N/A (special) | Minimize |

## 55. Pattern Evolution

```
LC 312 Burst Balloons (Base)
    │
    │ Same structure, geometric interpretation
    ↓
LC 1039 Polygon Triangulation
    │
    │ Apply to cuts instead of items
    │ Add boundary preprocessing
    ↓
LC 1547 Minimum Cost to Cut a Stick
    │
    │ Character-based optimization
    │ Different recurrence
    ↓
LC 664 Strange Printer
```

## 56. Key Differences

### 56.1 Interval Definition

| Problem | `dp[i][j]` Meaning |
|---------|-------------------|
| LC 312 | Max coins bursting balloons in (i, j) exclusive |
| LC 1039 | Min cost triangulating vertices [i, j] inclusive |
| LC 1547 | Min cost cutting between positions cuts[i] and cuts[j] |
| LC 664 | Min turns printing s[i:j+1] |

### 56.2 Preprocessing Required

| Problem | Preprocessing |
|---------|---------------|
| LC 312 | Add virtual balloons [1] at boundaries |
| LC 1039 | None |
| LC 1547 | Add 0 and n to cuts, sort |
| LC 664 | Remove consecutive duplicate characters |

### 56.3 Loop Structure

| Problem | Outer Loop | Inner Split |
|---------|------------|-------------|
| LC 312 | length 2 to n | k from i+1 to j-1 |
| LC 1039 | length 3 to n | k from i+1 to j-1 |
| LC 1547 | gap 2 to m-1 | k from i+1 to j-1 |
| LC 664 | length 2 to n | k where s[k] == s[i] |

---

## 57. Decision Tree

```
Start: Optimal way to process an interval?
            │
            ▼
    ┌───────────────────┐
    │ What operation?   │
    └───────────────────┘
            │
    ┌───────┼───────┬───────────┐
    ▼       ▼       ▼           ▼
Remove   Split    Print      Triangulate
items    at point sequence   polygon
    │       │       │           │
    ▼       ▼       ▼           ▼
LC 312   LC 1547  LC 664     LC 1039
Burst    Cut      Strange    Polygon
Balloons Stick    Printer    Score
```

## 58. Pattern Selection Guide

### 58.1 Use Burst Balloons Style (LC 312) when:
- Removing items changes neighbors
- Need to consider "last operation"
- Boundaries provide context for removal

### 58.2 Use Polygon Triangulation Style (LC 1039) when:
- Geometric interpretation exists
- Edge-based subproblem definition
- Third point splits into smaller polygons

### 58.3 Use Cut Stick Style (LC 1547) when:
- Cutting/splitting operations
- Cost depends on segment size
- Need to preprocess with boundaries

### 58.4 Use Strange Printer Style (LC 664) when:
- Character/value matching matters
- Can "extend" operations for matching elements
- Non-standard split point selection

## 59. Complexity Guide

All Interval DP problems share:
- Time: O(n³) - three nested loops
- Space: O(n²) - 2D DP table

## 60. Key Indicators for Interval DP

| Clue | Pattern |
|------|---------|
| "burst balloons", "remove and merge" | LC 312 style |
| "triangulate polygon" | LC 1039 style |
| "minimum cost to cut/split" | LC 1547 style |
| "minimum operations to print/transform" | LC 664 style |
| "matrix chain multiplication" | Classic interval DP |

---

## 61. Universal Templates

### 61.1 Template 1: Burst Balloons Style

```python
def burst_balloons_template(nums: list) -> int:
    """
    Maximum coins from bursting all balloons.
    Time: O(n³), Space: O(n²)
    """
    nums = [1] + nums + [1]
    n = len(nums)

    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                coins = nums[i] * nums[k] * nums[j]
                dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + coins)

    return dp[0][n - 1]
```

**Use for**: LC 312, problems where removing item affects neighbors

---

### 61.2 Template 2: Polygon Triangulation Style

```python
def polygon_triangulation_template(values: list) -> int:
    """
    Minimum score to triangulate polygon.
    Time: O(n³), Space: O(n²)
    """
    n = len(values)
    dp = [[0] * n for _ in range(n)]

    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')

            for k in range(i + 1, j):
                cost = values[i] * values[k] * values[j]
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cost)

    return dp[0][n - 1]
```

**Use for**: LC 1039, geometric interval DP

---

### 61.3 Template 3: Cut Stick Style

```python
def cut_stick_template(n: int, cuts: list) -> int:
    """
    Minimum cost to make all cuts.
    Time: O(m³), Space: O(m²)
    """
    cuts = sorted([0] + cuts + [n])
    m = len(cuts)
    dp = [[0] * m for _ in range(m)]

    for gap in range(2, m):
        for i in range(m - gap):
            j = i + gap
            dp[i][j] = float('inf')

            for k in range(i + 1, j):
                cost = cuts[j] - cuts[i]
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cost)

    return dp[0][m - 1]
```

**Use for**: LC 1547, cutting/splitting problems

---

### 61.4 Template 4: Strange Printer Style

```python
def strange_printer_template(s: str) -> int:
    """
    Minimum turns to print string.
    Time: O(n³), Space: O(n²)
    """
    # Remove consecutive duplicates
    s = ''.join(c for i, c in enumerate(s) if i == 0 or c != s[i-1])
    n = len(s)

    if n == 0:
        return 0

    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = dp[i + 1][j] + 1

            for k in range(i + 1, j + 1):
                if s[k] == s[i]:
                    left = dp[i + 1][k - 1] if k > i + 1 else 0
                    right = dp[k][j]
                    dp[i][j] = min(dp[i][j], left + right)

    return dp[0][n - 1]
```

**Use for**: LC 664, character-matching optimization

---

## 62. Quick Reference

| Problem Type | Template | Key Feature |
|-------------|----------|-------------|
| Remove with neighbor effect | Template 1 | Add boundary elements |
| Polygon/geometric | Template 2 | Edge-based splitting |
| Cutting/splitting | Template 3 | Sort and add boundaries |
| Character matching | Template 4 | Special recurrence |



---



*Document generated for NeetCode Practice Framework — API Kernel: interval_dp*

## Variation: Histogram / Interval Expansion

> **Problem**: Find the largest rectangle in a histogram (LeetCode 84).
> **Key Insight**: For each bar, find its left and right boundaries (first smaller bar), then compute area.

### Core Insight: Interval Expansion via Boundaries

For each bar at index `i` with height `h`:
- **Left boundary**: First bar to the left that is shorter (`left_smaller[i]`)
- **Right boundary**: First bar to the right that is shorter (`right_smaller[i]`)
- **Width**: `right_smaller[i] - left_smaller[i] - 1`
- **Area**: `h * width`

```
Histogram: [2, 1, 5, 6, 2, 3]

Bar at index 2 (height 5):
  Left boundary: index 1 (height 1 < 5)
  Right boundary: index 4 (height 2 < 5)
  Width: 4 - 1 - 1 = 2
  Area: 5 * 2 = 10
```

### Two-Pass Approach

```python
def largest_rectangle_two_pass(heights: list[int]) -> int:
    """
    Largest rectangle using two passes for left/right boundaries.

    Time: O(n), Space: O(n)
    """
    n = len(heights)
    left_smaller = [-1] * n   # Index of first smaller bar to left
    right_smaller = [n] * n   # Index of first smaller bar to right

    # Pass 1: Find left boundaries (previous smaller)
    stack = []
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left_smaller[i] = stack[-1] if stack else -1
        stack.append(i)

    # Pass 2: Find right boundaries (next smaller)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        right_smaller[i] = stack[-1] if stack else n
        stack.append(i)

    # Compute maximum area
    max_area = 0
    for i in range(n):
        width = right_smaller[i] - left_smaller[i] - 1
        area = heights[i] * width
        max_area = max(max_area, area)

    return max_area
```

### Single-Pass with Sentinel

```python
def largest_rectangle_single_pass(heights: list[int]) -> int:
    """
    Largest rectangle using single pass with sentinel.

    The sentinel (0 at end) forces all remaining bars to be popped,
    completing their rectangle computation.

    Time: O(n), Space: O(n)
    """
    heights = heights + [0]  # Sentinel: forces final flush
    stack = [-1]  # Virtual left boundary
    max_area = 0

    for i, h in enumerate(heights):
        while stack[-1] != -1 and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area
```

### Sentinel-Based Flushing

The sentinel pattern ensures all elements are processed:
- **Right sentinel** (`heights.append(0)`): A bar of height 0 is smaller than all bars, forcing all stack elements to pop
- **Left sentinel** (`stack = [-1]`): A virtual boundary at index -1 handles the case when stack becomes empty

### Strict vs Non-Strict for Duplicates

For duplicate heights, use **non-strict** comparison (`>=` instead of `>`):

```python
# With duplicates: [2, 2, 2]
# Using > (strict): Each bar stops at its immediate neighbor
# Using >= (non-strict): Each bar extends through equal-height bars

while stack[-1] != -1 and heights[stack[-1]] >= h:  # >= for duplicates
```

This ensures correct width calculation when adjacent bars have equal height.

### Maximal Rectangle in Binary Matrix (LeetCode 85)

```python
def maximal_rectangle(matrix: list[list[str]]) -> int:
    """
    Find largest rectangle of 1s in binary matrix.

    Algorithm:
    - Build histogram row by row
    - Each cell's height = consecutive 1s above (including current)
    - Apply largest_rectangle_in_histogram to each row

    Time: O(m * n), Space: O(n)
    """
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix[0])
    heights = [0] * n
    max_area = 0

    for row in matrix:
        # Update histogram
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0

        # Find largest rectangle in current histogram
        max_area = max(max_area, largest_rectangle_single_pass(heights[:]))

    return max_area
```



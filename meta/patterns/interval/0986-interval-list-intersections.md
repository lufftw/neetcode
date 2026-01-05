## Interval List Intersections (LeetCode 986)

> **Problem**: Find intersections of two sorted interval lists.
> **Invariant**: Two-pointer merge with intersection detection.
> **Role**: VARIANT applying two-pointer technique to intervals.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "two sorted lists" | → Two-pointer merge |
| "find intersections" | → Compute overlap region |
| "common intervals" | → max(starts), min(ends) |

### Implementation

```python
# Pattern: interval_intersection
# See: docs/patterns/interval/templates.md Section 5

class Solution:
    def intervalIntersection(
        self, firstList: List[List[int]], secondList: List[List[int]]
    ) -> List[List[int]]:
        """
        Find all intersections of two sorted interval lists.

        Key Insight:
        - Use two pointers (like merge sort)
        - Intersection exists if max(starts) <= min(ends)
        - Advance pointer with smaller end (exhausted earlier)

        Why advance smaller end?
        - Interval with smaller end can't intersect future intervals
        - The other interval might still intersect with next intervals
        """
        result: list[list[int]] = []
        i, j = 0, 0

        while i < len(firstList) and j < len(secondList):
            a_start, a_end = firstList[i]
            b_start, b_end = secondList[j]

            # Check for intersection
            start = max(a_start, b_start)
            end = min(a_end, b_end)

            if start <= end:
                result.append([start, end])

            # Advance pointer with smaller end
            if a_end < b_end:
                i += 1
            else:
                j += 1

        return result
```

### Trace Example

```
firstList = [[0,2], [5,10], [13,23], [24,25]]
secondList = [[1,5], [8,12], [15,24], [25,26]]

Two-pointer walk:
i=0, j=0: [0,2] vs [1,5]
  intersection: [max(0,1), min(2,5)] = [1,2] ✓
  a_end=2 < b_end=5, advance i

i=1, j=0: [5,10] vs [1,5]
  intersection: [max(5,1), min(10,5)] = [5,5] ✓
  a_end=10 > b_end=5, advance j

i=1, j=1: [5,10] vs [8,12]
  intersection: [max(5,8), min(10,12)] = [8,10] ✓
  a_end=10 < b_end=12, advance i

i=2, j=1: [13,23] vs [8,12]
  intersection: [max(13,8), min(23,12)] = [13,12] ✗ (start > end)
  a_end=23 > b_end=12, advance j

i=2, j=2: [13,23] vs [15,24]
  intersection: [max(13,15), min(23,24)] = [15,23] ✓
  a_end=23 < b_end=24, advance i

i=3, j=2: [24,25] vs [15,24]
  intersection: [max(24,15), min(25,24)] = [24,24] ✓
  a_end=25 > b_end=24, advance j

i=3, j=3: [24,25] vs [25,26]
  intersection: [max(24,25), min(25,26)] = [25,25] ✓
  a_end=25 < b_end=26, advance i

Output: [[1,2], [5,5], [8,10], [15,23], [24,24], [25,25]]
```

### Visual Representation

```
firstList:
  [0--2]
        [5--------10]
                      [13-----------23]
                                       [24-25]
secondList:
    [1----5]
            [8----12]
                        [15---------24]
                                       [25-26]

Intersections:
    [1-2]
        [5]
            [8--10]
                        [15-------23]
                                    [24]
                                       [25]
```

### Edge Cases

```python
# One empty list
firstList = [[1,3], [5,9]], secondList = []
# Result: []

# No intersection
firstList = [[1,2]], secondList = [[3,4]]
# Result: []

# Complete overlap
firstList = [[1,10]], secondList = [[2,5], [7,8]]
# Result: [[2,5], [7,8]]

# Point intersection
firstList = [[1,3]], secondList = [[3,5]]
# Result: [[3,3]]
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(m + n) - each pointer advances at most once per interval |
| Space | O(min(m,n)) - intersection list (worst case) |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 56: Merge Intervals | Merge instead of intersect |
| LC 88: Merge Sorted Array | Same two-pointer idea |
| LC 349: Intersection of Two Arrays | Set intersection |



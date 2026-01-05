## Minimum Number of Arrows to Burst Balloons (LeetCode 452)

> **Problem**: Find minimum arrows to burst all balloons (overlapping groups).
> **Invariant**: One arrow bursts all balloons in an overlapping region.
> **Role**: VARIANT of interval scheduling (count overlapping groups).

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "minimum arrows/points" | → Count overlapping groups |
| "burst all" | → Cover all intervals |
| "one arrow per group" | → Greedy grouping |

### Implementation

```python
# Pattern: interval_scheduling (group counting variant)
# See: docs/patterns/interval/templates.md Section 4

class Solution:
    def findMinArrowPoints(self, points: List[List[int]]) -> int:
        """
        Minimum arrows to burst all balloons.

        Key Insight:
        - Equivalent to counting non-overlapping groups
        - Sort by end, greedily extend groups
        - New arrow needed when balloon starts after current arrow position

        Why this works:
        - Arrow at x bursts all balloons where start <= x <= end
        - Greedy: shoot at rightmost safe position (end of first balloon)
        """
        if not points:
            return 0

        # Sort by end position
        points.sort(key=lambda x: x[1])

        arrows = 1
        arrow_pos = points[0][1]  # Shoot at end of first balloon

        for i in range(1, len(points)):
            # If balloon starts after current arrow position
            if points[i][0] > arrow_pos:
                arrows += 1
                arrow_pos = points[i][1]

        return arrows
```

### Trace Example

```
Input: [[10,16], [2,8], [1,6], [7,12]]

After sorting by end:
  [[1,6], [2,8], [7,12], [10,16]]

Process:
1. arrows = 1, arrow_pos = 6
   Shoot at x=6, bursts [1,6] and [2,8]

2. [2,8]: 2 <= 6, already burst

3. [7,12]: 7 > 6, need new arrow
   arrows = 2, arrow_pos = 12
   Shoot at x=12, bursts [7,12] and [10,16]

4. [10,16]: 10 <= 12, already burst

Output: 2
```

### Visual Representation

```
Balloons (sorted by end):
  [1------6]
    [2--------8]
         [7--------12]
              [10------16]

Arrow 1 at x=6:
  [1------6]  ← burst
    [2----X---8]  ← burst (6 is within [2,8])

Arrow 2 at x=12:
         [7--------12]  ← burst
              [10--X--16]  ← burst

Total: 2 arrows
```

### Connection to Non-overlapping Intervals

```python
# LC 435: eraseOverlapIntervals
# Remove minimum intervals for no overlaps
# Answer: n - max_non_overlapping

# LC 452: findMinArrowPoints
# Minimum arrows (= number of overlapping groups)
# Answer: max_non_overlapping (same greedy!)

# Key difference:
# - LC 435: count overlaps (n - groups)
# - LC 452: count groups directly
```

### Edge Cases

```python
# Single balloon
points = [[1,2]]
# Result: 1

# All overlapping
points = [[1,10], [2,5], [3,8]]
# Result: 1 (one arrow at x=5)

# No overlapping
points = [[1,2], [3,4], [5,6]]
# Result: 3
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n log n) - dominated by sorting |
| Space | O(1) - excluding sort space |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 435: Non-overlapping Intervals | Count removals instead |
| LC 253: Meeting Rooms II | Max concurrent |
| LC 56: Merge Intervals | Merge groups |



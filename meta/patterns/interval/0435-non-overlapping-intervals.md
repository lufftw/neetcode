## Non-overlapping Intervals (LeetCode 435)

> **Problem**: Find minimum number of intervals to remove for no overlaps.
> **Invariant**: Sort by end time, greedily keep earliest-ending intervals.
> **Role**: BASE TEMPLATE for interval scheduling (greedy selection).

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "minimum removals" | → Total - max non-overlapping |
| "no overlapping" | → Greedy interval scheduling |
| "maximum non-overlapping" | → Sort by end, greedy select |

### Implementation

```python
# Pattern: interval_scheduling
# See: docs/patterns/interval/templates.md Section 3 (Greedy Selection)

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        """
        Minimum intervals to remove for no overlaps.

        Key Insight:
        - Equivalent to: total - max non-overlapping intervals
        - Greedy: always keep interval that ends earliest
        - Sort by END time (not start!) for optimal selection

        Why sort by end?
        - Earlier ending = more room for future intervals
        - Greedy choice property: locally optimal → globally optimal
        """
        if not intervals:
            return 0

        # Sort by end time (critical for greedy!)
        intervals.sort(key=lambda x: x[1])

        # Greedy selection: count non-overlapping
        non_overlapping = 1
        prev_end = intervals[0][1]

        for i in range(1, len(intervals)):
            # If current starts after previous ends (no overlap)
            if intervals[i][0] >= prev_end:
                non_overlapping += 1
                prev_end = intervals[i][1]
            # Else: skip current (implicit removal)

        return len(intervals) - non_overlapping
```

### Trace Example

```
Input: [[1,2], [2,3], [3,4], [1,3]]

After sorting by end:
  [[1,2], [2,3], [1,3], [3,4]]

Greedy selection:
1. Keep [1,2], prev_end = 2, count = 1
2. [2,3]: 2 >= 2 (no overlap), keep it, prev_end = 3, count = 2
3. [1,3]: 1 < 3 (overlaps), skip
4. [3,4]: 3 >= 3 (no overlap), keep it, prev_end = 4, count = 3

Non-overlapping = 3
Removals = 4 - 3 = 1

Output: 1
```

### Visual: Why Sort by End?

```
Sort by start (WRONG):
  [1---------3]    ← picked first
      [2-3]        ← can't pick (overlaps)
          [3-4]    ← can pick
  Result: 2 intervals

Sort by end (CORRECT):
  [1-2]            ← picked first (ends earliest)
      [2-3]        ← can pick
          [3-4]    ← can pick
  [1---------3]    ← can't pick (overlaps with [1,2] and [2,3])
  Result: 3 intervals
```

### Alternative: Count Overlaps Directly

```python
def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
    """Count removals directly instead of subtracting."""
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])
    removals = 0
    prev_end = intervals[0][1]

    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:
            # Overlap detected, remove current (count it)
            removals += 1
        else:
            # No overlap, update prev_end
            prev_end = intervals[i][1]

    return removals
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n log n) - dominated by sorting |
| Space | O(1) - excluding sort space |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 452: Minimum Arrows | Max non-overlapping (balloons) |
| LC 646: Maximum Length of Pair Chain | Similar greedy |
| LC 1235: Maximum Profit in Job Scheduling | Weighted interval |



## Base Template: Merge Intervals (LeetCode 56)

> **Problem**: Merge all overlapping intervals.
> **Invariant**: After sorting, overlapping intervals are adjacent.
> **Role**: BASE TEMPLATE for interval merge pattern.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "merge overlapping" | → Sort by start, extend end |
| "combine intervals" | → IntervalMerge kernel |
| "non-overlapping result" | → Merge adjacent overlaps |

### Implementation

```python
# Pattern: interval_merge
# See: docs/patterns/interval/templates.md Section 1 (Base Template)

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Merge overlapping intervals.

        Key Insight:
        - After sorting by start time, overlapping intervals are adjacent
        - Maintain current interval, extend end if overlap, else add new
        - Overlap check: current[0] <= prev_end (since sorted)

        Why sort by start?
        - All intervals starting before current end must overlap
        - No need to look backward after sorting
        """
        if not intervals:
            return []

        # Sort by start time
        intervals.sort(key=lambda x: x[0])

        merged: list[list[int]] = [intervals[0]]

        for interval in intervals[1:]:
            # If current interval overlaps with last merged
            if interval[0] <= merged[-1][1]:
                # Extend the end
                merged[-1][1] = max(merged[-1][1], interval[1])
            else:
                # No overlap, add new interval
                merged.append(interval)

        return merged
```

### Trace Example

```
Input: [[1,3], [2,6], [8,10], [15,18]]

After sorting (already sorted):
  [[1,3], [2,6], [8,10], [15,18]]

Process:
1. merged = [[1,3]]
2. [2,6]: 2 <= 3 (overlaps), extend to [1,6]
   merged = [[1,6]]
3. [8,10]: 8 > 6 (no overlap), add new
   merged = [[1,6], [8,10]]
4. [15,18]: 15 > 10 (no overlap), add new
   merged = [[1,6], [8,10], [15,18]]

Output: [[1,6], [8,10], [15,18]]
```

### Visual Representation

```
Input intervals:
  [1---3]
    [2-------6]
              [8--10]
                      [15--18]

After merging:
  [1---------6]
              [8--10]
                      [15--18]
```

### Why Sort by Start?

```python
# Without sorting:
# [[8,10], [1,3], [2,6]] → can't detect [1,3] overlaps [2,6]

# After sorting by start:
# [[1,3], [2,6], [8,10]] → adjacent overlaps are easy to detect
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n log n) - dominated by sorting |
| Space | O(n) - worst case no overlaps |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 57: Insert Interval | Insert then merge |
| LC 435: Non-overlapping Intervals | Min removals |
| LC 252: Meeting Rooms | Check any overlap |



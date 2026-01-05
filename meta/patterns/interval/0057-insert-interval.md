## Insert Interval (LeetCode 57)

> **Problem**: Insert a new interval into a sorted list of non-overlapping intervals.
> **Invariant**: Three phases - before overlap, during overlap, after overlap.
> **Role**: VARIANT of merge pattern with insertion.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "insert interval" | → Three-phase processing |
| "sorted intervals" | → Binary search optimization possible |
| "merge with new" | → Track overlap region |

### Implementation

```python
# Pattern: interval_insert
# See: docs/patterns/interval/templates.md Section 2

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        """
        Insert new interval into sorted non-overlapping list.

        Key Insight:
        - Already sorted, process in three phases
        - Phase 1: Add all intervals ending before newInterval starts
        - Phase 2: Merge all overlapping intervals
        - Phase 3: Add all intervals starting after newInterval ends

        Why three phases?
        - Clean separation of logic
        - No need to re-sort after insertion
        """
        result: list[list[int]] = []
        i = 0
        n = len(intervals)

        # Phase 1: Add all intervals that end before newInterval starts
        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        # Phase 2: Merge overlapping intervals
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        result.append(newInterval)

        # Phase 3: Add remaining intervals
        while i < n:
            result.append(intervals[i])
            i += 1

        return result
```

### Trace Example

```
Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]

Phase 1: intervals ending before 4
  [1,2] ends at 2 < 4, add to result
  result = [[1,2]]

Phase 2: intervals overlapping with [4,8]
  [3,5]: 3 <= 8, merge → [3,8]
  [6,7]: 6 <= 8, merge → [3,8]
  [8,10]: 8 <= 8, merge → [3,10]
  result = [[1,2], [3,10]]

Phase 3: remaining intervals
  [12,16]: add
  result = [[1,2], [3,10], [12,16]]

Output: [[1,2],[3,10],[12,16]]
```

### Visual Representation

```
Input intervals:
  [1-2]
      [3--5]
           [6-7]
               [8--10]
                        [12----16]
New interval:
        [4------8]

After insertion:
  [1-2]
      [3-----------10]
                        [12----16]
```

### Edge Cases

```python
# Empty intervals
intervals = [], newInterval = [5,7]
# Result: [[5,7]]

# New interval before all
intervals = [[3,5]], newInterval = [1,2]
# Result: [[1,2], [3,5]]

# New interval after all
intervals = [[1,2]], newInterval = [5,7]
# Result: [[1,2], [5,7]]

# Complete overlap
intervals = [[1,5]], newInterval = [2,3]
# Result: [[1,5]]
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - single pass |
| Space | O(n) - output array |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 56: Merge Intervals | Merge all overlapping |
| LC 715: Range Module | Add/remove ranges |
| LC 352: Data Stream as Disjoint Intervals | Dynamic insertion |



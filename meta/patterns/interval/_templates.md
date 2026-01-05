---

## Code Templates Summary

### Template 1: Merge Intervals (LC 56)

```python
def merge(intervals: List[List[int]]) -> List[List[int]]:
    """Sort by start, merge adjacent overlaps."""
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for curr in intervals[1:]:
        if curr[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], curr[1])
        else:
            merged.append(curr)

    return merged
```

### Template 2: Insert Interval (LC 57)

```python
def insert(intervals: List[List[int]], new: List[int]) -> List[List[int]]:
    """Three-phase: before, merge, after."""
    result = []
    i = 0
    n = len(intervals)

    # Phase 1: Before overlap
    while i < n and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1

    # Phase 2: Merge overlapping
    while i < n and intervals[i][0] <= new[1]:
        new[0] = min(new[0], intervals[i][0])
        new[1] = max(new[1], intervals[i][1])
        i += 1
    result.append(new)

    # Phase 3: After overlap
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

### Template 3: Greedy Selection (LC 435, 452)

```python
def max_non_overlapping(intervals: List[List[int]]) -> int:
    """Sort by end, greedily select non-overlapping."""
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])
    count = 1
    prev_end = intervals[0][1]

    for curr in intervals[1:]:
        if curr[0] >= prev_end:  # No overlap
            count += 1
            prev_end = curr[1]

    return count

# LC 435: return len(intervals) - max_non_overlapping(intervals)
# LC 452: return max_non_overlapping(intervals)  # (with > instead of >=)
```

### Template 4: Interval Intersection (LC 986)

```python
def interval_intersection(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """Two-pointer merge for intersections."""
    result = []
    i, j = 0, 0

    while i < len(A) and j < len(B):
        start = max(A[i][0], B[j][0])
        end = min(A[i][1], B[j][1])

        if start <= end:
            result.append([start, end])

        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1

    return result
```

### Helper Functions

```python
def overlaps(a: List[int], b: List[int]) -> bool:
    """Check if two intervals overlap (closed intervals)."""
    return a[0] <= b[1] and b[0] <= a[1]

def merge_two(a: List[int], b: List[int]) -> List[int]:
    """Merge two overlapping intervals."""
    return [min(a[0], b[0]), max(a[1], b[1])]

def intersection(a: List[int], b: List[int]) -> Optional[List[int]]:
    """Get intersection of two intervals, or None."""
    start = max(a[0], b[0])
    end = min(a[1], b[1])
    return [start, end] if start <= end else None
```

### Pattern Selection Cheat Sheet

| Problem Signal | Template | Sort By |
|---------------|----------|---------|
| "merge overlapping" | Template 1 | Start |
| "insert interval" | Template 2 | (Already sorted) |
| "min removals" | Template 3 | End |
| "min arrows" | Template 3 | End |
| "intersection" | Template 4 | (Two pointers) |



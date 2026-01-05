# Interval Patterns: Complete Reference

> **API Kernel**: `IntervalMerge`, `IntervalScheduling`
> **Core Mechanism**: Process intervals by sorting and then merging or selecting based on overlap relationships.

This document presents the **canonical interval templates** covering merge, insert, overlap detection, greedy selection, and intersection problems. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Core Concepts

### Interval Representation

```python
# Standard interval format
intervals: list[list[int]] = [[1, 3], [2, 6], [8, 10], [15, 18]]
# Each interval: [start, end] where start <= end

# Interval with open/closed boundaries
# [1, 3] = closed interval, includes both endpoints
# (1, 3) = open interval, excludes both endpoints
# Most LeetCode problems use closed intervals
```

### Sorting Strategy

```python
# Sort by start time (most common)
intervals.sort(key=lambda x: x[0])

# Sort by end time (greedy selection problems)
intervals.sort(key=lambda x: x[1])

# Sort by start, then by end (for tie-breaking)
intervals.sort(key=lambda x: (x[0], x[1]))
```

### Overlap Detection

```python
# Two intervals [a_start, a_end] and [b_start, b_end] overlap if:
#   NOT (a_end < b_start OR b_end < a_start)
# Equivalently:
#   a_start <= b_end AND b_start <= a_end

def overlaps(a: list[int], b: list[int]) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]

# After sorting by start, simplified check:
# Current interval starts before previous ends
def overlaps_sorted(prev: list[int], curr: list[int]) -> bool:
    return curr[0] <= prev[1]
```

### Merge Operation

```python
# Merge two overlapping intervals
def merge_two(a: list[int], b: list[int]) -> list[int]:
    return [min(a[0], b[0]), max(a[1], b[1])]
```

### Pattern Variants

| Variant | API Kernel | Use When | Key Insight |
|---------|------------|----------|-------------|
| **Merge Overlapping** | `IntervalMerge` | Combine overlapping intervals | Sort by start, extend end |
| **Insert Interval** | `IntervalMerge` | Insert new interval into sorted list | Three-phase: before, overlap, after |
| **Non-Overlapping Selection** | `IntervalScheduling` | Max intervals without overlap | Sort by end, greedy selection |
| **Min Removals** | `IntervalScheduling` | Min intervals to remove for no overlap | Total - max non-overlapping |
| **Interval Intersection** | `IntervalMerge` | Find overlapping regions | Two-pointer merge |

### Time Complexity

| Operation | Complexity |
|-----------|------------|
| Sort intervals | O(n log n) |
| Single pass merge/select | O(n) |
| Overall (sort-dominated) | O(n log n) |



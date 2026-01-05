# Interval Patterns: Complete Reference

> **API Kernel**: `IntervalMerge`, `IntervalScheduling`
> **Core Mechanism**: Process intervals by sorting and then merging or selecting based on overlap relationships.

This document presents the **canonical interval templates** covering merge, insert, overlap detection, greedy selection, and intersection problems. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Merge Intervals (LeetCode 56)](#2-base-template-merge-intervals-leetcode-56)
3. [Insert Interval (LeetCode 57)](#3-insert-interval-leetcode-57)
4. [Non-overlapping Intervals (LeetCode 435)](#4-non-overlapping-intervals-leetcode-435)
5. [Minimum Number of Arrows to Burst Balloons (LeetCode 452)](#5-minimum-number-of-arrows-to-burst-balloons-leetcode-452)
6. [Interval List Intersections (LeetCode 986)](#6-interval-list-intersections-leetcode-986)
7. [Pattern Comparison](#7-pattern-comparison)
8. [Decision Framework](#8-decision-framework)
9. [Code Templates Summary](#9-code-templates-summary)

---

## 1. Core Concepts

### 1.1 Interval Representation

```python
# Standard interval format
intervals: list[list[int]] = [[1, 3], [2, 6], [8, 10], [15, 18]]
# Each interval: [start, end] where start <= end

# Interval with open/closed boundaries
# [1, 3] = closed interval, includes both endpoints
# (1, 3) = open interval, excludes both endpoints
# Most LeetCode problems use closed intervals
```

### 1.2 Sorting Strategy

```python
# Sort by start time (most common)
intervals.sort(key=lambda x: x[0])

# Sort by end time (greedy selection problems)
intervals.sort(key=lambda x: x[1])

# Sort by start, then by end (for tie-breaking)
intervals.sort(key=lambda x: (x[0], x[1]))
```

### 1.3 Overlap Detection

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

### 1.4 Merge Operation

```python
# Merge two overlapping intervals
def merge_two(a: list[int], b: list[int]) -> list[int]:
    return [min(a[0], b[0]), max(a[1], b[1])]
```

### 1.5 Pattern Variants

| Variant | API Kernel | Use When | Key Insight |
|---------|------------|----------|-------------|
| **Merge Overlapping** | `IntervalMerge` | Combine overlapping intervals | Sort by start, extend end |
| **Insert Interval** | `IntervalMerge` | Insert new interval into sorted list | Three-phase: before, overlap, after |
| **Non-Overlapping Selection** | `IntervalScheduling` | Max intervals without overlap | Sort by end, greedy selection |
| **Min Removals** | `IntervalScheduling` | Min intervals to remove for no overlap | Total - max non-overlapping |
| **Interval Intersection** | `IntervalMerge` | Find overlapping regions | Two-pointer merge |

### 1.6 Time Complexity

| Operation | Complexity |
|-----------|------------|
| Sort intervals | O(n log n) |
| Single pass merge/select | O(n) |
| Overall (sort-dominated) | O(n log n) |

---

## 2. Base Template: Merge Intervals (LeetCode 56)

> **Problem**: Merge all overlapping intervals.
> **Invariant**: After sorting, overlapping intervals are adjacent.
> **Role**: BASE TEMPLATE for interval merge pattern.

### 2.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "merge overlapping" | → Sort by start, extend end |
| "combine intervals" | → IntervalMerge kernel |
| "non-overlapping result" | → Merge adjacent overlaps |

### 2.2 Implementation

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

### 2.3 Trace Example

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

### 2.4 Visual Representation

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

### 2.5 Why Sort by Start?

```python
# Without sorting:
# [[8,10], [1,3], [2,6]] → can't detect [1,3] overlaps [2,6]

# After sorting by start:
# [[1,3], [2,6], [8,10]] → adjacent overlaps are easy to detect
```

### 2.6 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n log n) - dominated by sorting |
| Space | O(n) - worst case no overlaps |

### 2.7 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 57: Insert Interval | Insert then merge |
| LC 435: Non-overlapping Intervals | Min removals |
| LC 252: Meeting Rooms | Check any overlap |

---

## 3. Insert Interval (LeetCode 57)

> **Problem**: Insert a new interval into a sorted list of non-overlapping intervals.
> **Invariant**: Three phases - before overlap, during overlap, after overlap.
> **Role**: VARIANT of merge pattern with insertion.

### 3.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "insert interval" | → Three-phase processing |
| "sorted intervals" | → Binary search optimization possible |
| "merge with new" | → Track overlap region |

### 3.2 Implementation

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

### 3.3 Trace Example

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

### 3.4 Visual Representation

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

### 3.5 Edge Cases

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

### 3.6 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - single pass |
| Space | O(n) - output array |

### 3.7 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 56: Merge Intervals | Merge all overlapping |
| LC 715: Range Module | Add/remove ranges |
| LC 352: Data Stream as Disjoint Intervals | Dynamic insertion |

---

## 4. Non-overlapping Intervals (LeetCode 435)

> **Problem**: Find minimum number of intervals to remove for no overlaps.
> **Invariant**: Sort by end time, greedily keep earliest-ending intervals.
> **Role**: BASE TEMPLATE for interval scheduling (greedy selection).

### 4.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "minimum removals" | → Total - max non-overlapping |
| "no overlapping" | → Greedy interval scheduling |
| "maximum non-overlapping" | → Sort by end, greedy select |

### 4.2 Implementation

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

### 4.3 Trace Example

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

### 4.4 Visual: Why Sort by End?

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

### 4.5 Alternative: Count Overlaps Directly

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

### 4.6 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n log n) - dominated by sorting |
| Space | O(1) - excluding sort space |

### 4.7 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 452: Minimum Arrows | Max non-overlapping (balloons) |
| LC 646: Maximum Length of Pair Chain | Similar greedy |
| LC 1235: Maximum Profit in Job Scheduling | Weighted interval |

---

## 5. Minimum Number of Arrows to Burst Balloons (LeetCode 452)

> **Problem**: Find minimum arrows to burst all balloons (overlapping groups).
> **Invariant**: One arrow bursts all balloons in an overlapping region.
> **Role**: VARIANT of interval scheduling (count overlapping groups).

### 5.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "minimum arrows/points" | → Count overlapping groups |
| "burst all" | → Cover all intervals |
| "one arrow per group" | → Greedy grouping |

### 5.2 Implementation

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

### 5.3 Trace Example

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

### 5.4 Visual Representation

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

### 5.5 Connection to Non-overlapping Intervals

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

### 5.6 Edge Cases

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

### 5.7 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n log n) - dominated by sorting |
| Space | O(1) - excluding sort space |

### 5.8 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 435: Non-overlapping Intervals | Count removals instead |
| LC 253: Meeting Rooms II | Max concurrent |
| LC 56: Merge Intervals | Merge groups |

---

## 6. Interval List Intersections (LeetCode 986)

> **Problem**: Find intersections of two sorted interval lists.
> **Invariant**: Two-pointer merge with intersection detection.
> **Role**: VARIANT applying two-pointer technique to intervals.

### 6.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "two sorted lists" | → Two-pointer merge |
| "find intersections" | → Compute overlap region |
| "common intervals" | → max(starts), min(ends) |

### 6.2 Implementation

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

### 6.3 Trace Example

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

### 6.4 Visual Representation

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

### 6.5 Edge Cases

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

### 6.6 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(m + n) - each pointer advances at most once per interval |
| Space | O(min(m,n)) - intersection list (worst case) |

### 6.7 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 56: Merge Intervals | Merge instead of intersect |
| LC 88: Merge Sorted Array | Same two-pointer idea |
| LC 349: Intersection of Two Arrays | Set intersection |

---

---

## 7. Pattern Comparison

### 7.1 Sort Key Decision

| Sort By | When to Use | Problems |
|---------|-------------|----------|
| **Start time** | Merge overlapping, insert interval | LC 56, 57 |
| **End time** | Greedy selection, min removals | LC 435, 452 |
| **Both pointers** | Two sorted lists | LC 986 |

### 7.2 Overlap Definition Variants

```python
# Standard overlap (closed intervals)
# Intervals [a,b] and [c,d] overlap if: a <= d AND c <= b

# After sorting by start:
# Current overlaps with previous if: curr_start <= prev_end

# After sorting by end:
# Current overlaps with previous if: curr_start < prev_end
# Note: < not <= because we're greedy (want equality to mean "touch")
```

### 7.3 Problem Type Recognition

| Problem Type | Key Signal | Approach |
|--------------|------------|----------|
| **Merge overlapping** | "combine", "merge" | Sort by start, extend end |
| **Insert interval** | "insert", "add to sorted" | Three-phase: before/during/after |
| **Min removals** | "remove", "erase for no overlap" | Sort by end, count non-overlapping |
| **Count groups** | "minimum to cover all" | Sort by end, count groups |
| **Intersections** | "common part", "overlap region" | Two-pointer merge |

### 7.4 Code Pattern Comparison

```python
# MERGE PATTERN (sort by start)
intervals.sort(key=lambda x: x[0])
for curr in intervals[1:]:
    if curr[0] <= merged[-1][1]:  # Overlap
        merged[-1][1] = max(merged[-1][1], curr[1])  # Extend
    else:
        merged.append(curr)

# SCHEDULING PATTERN (sort by end)
intervals.sort(key=lambda x: x[1])
for curr in intervals[1:]:
    if curr[0] >= prev_end:  # No overlap
        count += 1
        prev_end = curr[1]

# INTERSECTION PATTERN (two pointers)
while i < len(A) and j < len(B):
    start, end = max(A[i][0], B[j][0]), min(A[i][1], B[j][1])
    if start <= end:
        result.append([start, end])
    if A[i][1] < B[j][1]:
        i += 1
    else:
        j += 1
```

### 7.5 Greedy Property Analysis

| Problem | Greedy Choice | Why Optimal |
|---------|--------------|-------------|
| LC 435 | Keep earliest-ending | Leaves most room for future intervals |
| LC 452 | Shoot at rightmost safe position | Maximizes balloons per arrow |
| LC 56 | Merge all overlapping | No choice - must merge |
| LC 57 | Process in phases | Already sorted, single pass optimal |

---

---

## 8. Decision Framework

### 8.1 Quick Reference Decision Tree

```
START: Given interval problem
│
├─ "Merge" or "combine" intervals?
│   └─ YES → Sort by START, merge adjacent
│            (LC 56 pattern)
│
├─ "Insert" new interval into sorted list?
│   └─ YES → Three-phase processing
│            (LC 57 pattern)
│
├─ "Remove minimum" for no overlaps?
│   └─ YES → Sort by END, greedy count
│            Answer = n - non_overlapping
│            (LC 435 pattern)
│
├─ "Minimum arrows/points" to cover all?
│   └─ YES → Sort by END, count groups
│            (LC 452 pattern)
│
├─ "Intersection" of two sorted lists?
│   └─ YES → Two-pointer merge
│            (LC 986 pattern)
│
└─ None of above?
    └─ Consider: Line sweep, Meeting rooms variant
```

### 8.2 Sort Strategy Selection

```
Need to MERGE intervals?
  → Sort by START
  → Reason: Adjacent overlaps become consecutive

Need to SELECT maximum non-overlapping?
  → Sort by END
  → Reason: Greedy - earliest end leaves most room

Need to INTERSECT two lists?
  → Already sorted, use TWO POINTERS
  → Reason: Linear merge technique
```

### 8.3 Common Mistakes to Avoid

| Mistake | Why Wrong | Correct Approach |
|---------|-----------|------------------|
| Sort by start for greedy selection | Suboptimal: may exclude intervals unnecessarily | Sort by end |
| Sort by end for merging | Misses overlaps: [1,5], [2,3] won't merge correctly | Sort by start |
| Check `>` instead of `>=` for overlap | Off-by-one: [1,2], [2,3] touch but may not be considered overlapping | Depends on problem definition |
| Update end without max() | Wrong: [1,5], [2,3] → should remain [1,5] not [1,3] | Always use max(ends) |

### 8.4 Problem Variants Quick Map

| If asked... | Think... | Key Pattern |
|-------------|----------|-------------|
| "Minimum intervals to remove" | Total - max_selected | Greedy scheduling |
| "Maximum non-overlapping" | Sort by end, greedy | Greedy scheduling |
| "Merge overlapping" | Sort by start, extend | Merge pattern |
| "Insert and merge" | Three phases | Insert pattern |
| "Find common intervals" | Two pointers | Intersection |
| "Minimum to cover all" | Count groups | Arrow/covering |

### 8.5 Complexity Expectations

| Operation | Expected Complexity |
|-----------|-------------------|
| Any interval problem with sorting | O(n log n) |
| Post-sort processing | O(n) |
| Two-list intersection | O(m + n) |
| Space (typical) | O(n) for output |

---

---

## 9. Code Templates Summary

### 9.1 Template 1: Merge Intervals (LC 56)

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

### 9.2 Template 2: Insert Interval (LC 57)

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

### 9.3 Template 3: Greedy Selection (LC 435, 452)

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

### 9.4 Template 4: Interval Intersection (LC 986)

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

### 9.5 Helper Functions

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

### 9.6 Pattern Selection Cheat Sheet

| Problem Signal | Template | Sort By |
|---------------|----------|---------|
| "merge overlapping" | Template 1 | Start |
| "insert interval" | Template 2 | (Already sorted) |
| "min removals" | Template 3 | End |
| "min arrows" | Template 3 | End |
| "intersection" | Template 4 | (Two pointers) |



---



*Document generated for NeetCode Practice Framework — API Kernel: IntervalMerge*

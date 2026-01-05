---

## Pattern Comparison

### Sort Key Decision

| Sort By | When to Use | Problems |
|---------|-------------|----------|
| **Start time** | Merge overlapping, insert interval | LC 56, 57 |
| **End time** | Greedy selection, min removals | LC 435, 452 |
| **Both pointers** | Two sorted lists | LC 986 |

### Overlap Definition Variants

```python
# Standard overlap (closed intervals)
# Intervals [a,b] and [c,d] overlap if: a <= d AND c <= b

# After sorting by start:
# Current overlaps with previous if: curr_start <= prev_end

# After sorting by end:
# Current overlaps with previous if: curr_start < prev_end
# Note: < not <= because we're greedy (want equality to mean "touch")
```

### Problem Type Recognition

| Problem Type | Key Signal | Approach |
|--------------|------------|----------|
| **Merge overlapping** | "combine", "merge" | Sort by start, extend end |
| **Insert interval** | "insert", "add to sorted" | Three-phase: before/during/after |
| **Min removals** | "remove", "erase for no overlap" | Sort by end, count non-overlapping |
| **Count groups** | "minimum to cover all" | Sort by end, count groups |
| **Intersections** | "common part", "overlap region" | Two-pointer merge |

### Code Pattern Comparison

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

### Greedy Property Analysis

| Problem | Greedy Choice | Why Optimal |
|---------|--------------|-------------|
| LC 435 | Keep earliest-ending | Leaves most room for future intervals |
| LC 452 | Shoot at rightmost safe position | Maximizes balloons per arrow |
| LC 56 | Merge all overlapping | No choice - must merge |
| LC 57 | Process in phases | Already sorted, single pass optimal |



## Decision Tree

```
Start: Optimal way to process an interval?
            │
            ▼
    ┌───────────────────┐
    │ What operation?   │
    └───────────────────┘
            │
    ┌───────┼───────┬───────────┐
    ▼       ▼       ▼           ▼
Remove   Split    Print      Triangulate
items    at point sequence   polygon
    │       │       │           │
    ▼       ▼       ▼           ▼
LC 312   LC 1547  LC 664     LC 1039
Burst    Cut      Strange    Polygon
Balloons Stick    Printer    Score
```

## Pattern Selection Guide

### Use Burst Balloons Style (LC 312) when:
- Removing items changes neighbors
- Need to consider "last operation"
- Boundaries provide context for removal

### Use Polygon Triangulation Style (LC 1039) when:
- Geometric interpretation exists
- Edge-based subproblem definition
- Third point splits into smaller polygons

### Use Cut Stick Style (LC 1547) when:
- Cutting/splitting operations
- Cost depends on segment size
- Need to preprocess with boundaries

### Use Strange Printer Style (LC 664) when:
- Character/value matching matters
- Can "extend" operations for matching elements
- Non-standard split point selection

## Complexity Guide

All Interval DP problems share:
- Time: O(n³) - three nested loops
- Space: O(n²) - 2D DP table

## Key Indicators for Interval DP

| Clue | Pattern |
|------|---------|
| "burst balloons", "remove and merge" | LC 312 style |
| "triangulate polygon" | LC 1039 style |
| "minimum cost to cut/split" | LC 1547 style |
| "minimum operations to print/transform" | LC 664 style |
| "matrix chain multiplication" | Classic interval DP |

## Decision Tree

```
Start: Grid problem involving distances or propagation?
                    │
                    ▼
        ┌───────────────────────┐
        │ Multiple starting     │
        │ points (sources)?     │
        └───────────────────────┘
                    │
            ┌───────┴───────┐
            ▼               ▼
           YES              NO
            │               │
            ▼               ▼
    ┌───────────────┐  Single-source BFS
    │ Need minimum  │  or other approach
    │ distance to   │
    │ ANY source?   │
    └───────────────┘
            │
            ▼
     Multi-Source BFS
            │
    ┌───────┴───────────┬────────────────┐
    ▼                   ▼                ▼
"Time until all?"  "Distance field?"  "Fill to nearest?"
    │                   │                │
    ▼                   ▼                ▼
Rotting Oranges    01 Matrix       Walls and Gates
 (count levels)    (store dist)    (store dist)
```

## Pattern Selection Guide

### Use Multi-Source BFS when:

- ✅ Multiple cells serve as starting points
- ✅ Need shortest distance to the **nearest** source
- ✅ Simultaneous propagation/spread semantics
- ✅ BFS level = distance relationship is needed
- ✅ Grid is unweighted (all edges have cost 1)

### Use Single-Source BFS when:

- ✅ Only one starting point
- ✅ Need distance from a specific source to all targets
- ✅ Path finding from A to B

### Use Dijkstra instead when:

- ✅ Weighted edges (different movement costs)
- ✅ Non-uniform grid (some cells cost more to traverse)

### Use DP instead when:

- ✅ Only need to check reachability (no actual distances)
- ✅ Bounded directions (e.g., only down/right movement)
- ✅ Two-pass approach is simpler

## Problem Identification Checklist

When you see a grid problem, ask:

1. **How many sources?** Single vs Multiple
2. **What's the question?** Time/count vs Distance vs Reachability
3. **Simultaneous or sequential?** Multi-source implies simultaneous
4. **Uniform cost?** BFS for uniform, Dijkstra for weighted

## Quick Pattern Recognition

| Keyword in Problem | Likely Pattern |
|--------------------|----------------|
| "minimum time until all" | Multi-source BFS (timer) |
| "distance to nearest" | Multi-source BFS (distance field) |
| "fill from boundary" | Multi-source BFS from edges |
| "spread/propagate/infect" | Multi-source BFS (propagation) |
| "shortest path from A to B" | Single-source BFS |



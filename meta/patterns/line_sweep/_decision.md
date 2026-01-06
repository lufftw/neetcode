## When to Use Line Sweep

### Pattern Recognition Signals

Use line sweep when you see:

1. **Multiple intervals** that can overlap
2. **Questions about overlap** (count, max, capacity)
3. **Aggregate state** at positions (how many active? max height?)
4. **Temporal or spatial ordering** (sort by time/position makes sense)

### Decision Flowchart

```
Problem has intervals/ranges?
├── No → Not line sweep
└── Yes → What do you need to track?
    ├── Count of overlaps → Event Counting
    │   └── Examples: Meeting Rooms II, Course Schedule III
    ├── Sum/capacity → Capacity Tracking
    │   └── Examples: Car Pooling, Range Addition
    └── Max/min of active set → Height Tracking
        └── Examples: Skyline, Falling Squares
```

### Line Sweep vs Other Patterns

| Alternative | When to Prefer Alternative |
|-------------|---------------------------|
| **Merge Intervals** | Need to collapse overlapping intervals, not count them |
| **Interval Scheduling** | Greedy selection (maximize non-overlap) |
| **Difference Array** | Bounded positions, avoid sorting |
| **Segment Tree** | Complex range queries with updates |

### Problem Transformation Hints

If problem says... | Think about...
---|---
"minimum rooms" | Event counting, find max
"can all fit" | Capacity tracking, check threshold
"silhouette/outline" | Height tracking with sorted container
"at any point in time" | Track state during sweep

### Common Pitfalls

1. **Wrong tie-breaking**: End before start vs start before end depends on semantics
2. **Off-by-one**: Half-open intervals `[start, end)` vs closed `[start, end]`
3. **Missing ground level**: Skyline needs height 0 as baseline
4. **Lazy deletion bugs**: Heap approach requires careful cleanup

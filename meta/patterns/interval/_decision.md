---

## Decision Framework

### Quick Reference Decision Tree

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

### Sort Strategy Selection

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

### Common Mistakes to Avoid

| Mistake | Why Wrong | Correct Approach |
|---------|-----------|------------------|
| Sort by start for greedy selection | Suboptimal: may exclude intervals unnecessarily | Sort by end |
| Sort by end for merging | Misses overlaps: [1,5], [2,3] won't merge correctly | Sort by start |
| Check `>` instead of `>=` for overlap | Off-by-one: [1,2], [2,3] touch but may not be considered overlapping | Depends on problem definition |
| Update end without max() | Wrong: [1,5], [2,3] → should remain [1,5] not [1,3] | Always use max(ends) |

### Problem Variants Quick Map

| If asked... | Think... | Key Pattern |
|-------------|----------|-------------|
| "Minimum intervals to remove" | Total - max_selected | Greedy scheduling |
| "Maximum non-overlapping" | Sort by end, greedy | Greedy scheduling |
| "Merge overlapping" | Sort by start, extend | Merge pattern |
| "Insert and merge" | Three phases | Insert pattern |
| "Find common intervals" | Two pointers | Intersection |
| "Minimum to cover all" | Count groups | Arrow/covering |

### Complexity Expectations

| Operation | Expected Complexity |
|-----------|-------------------|
| Any interval problem with sorting | O(n log n) |
| Post-sort processing | O(n) |
| Two-list intersection | O(m + n) |
| Space (typical) | O(n) for output |



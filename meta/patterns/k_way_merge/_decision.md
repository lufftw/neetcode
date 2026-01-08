## Decision Tree

```
Start: Merging sorted sequences?
                    │
                    ▼
        ┌───────────────────────┐
        │ How many sequences    │
        │ to merge?             │
        └───────────────────────┘
                    │
            ┌───────┴───────┐
            ▼               ▼
          K = 2            K > 2
            │               │
            ▼               ▼
    ┌───────────────┐   ┌───────────────┐
    │ In-place      │   │ Use Heap      │
    │ constraint?   │   │ O(N log K)    │
    └───────────────┘   └───────────────┘
            │                   │
      ┌─────┴─────┐            │
      ▼           ▼            │
     YES          NO           ▼
      │           │        ┌────────────────┐
      ▼           ▼        │ Alternative:   │
  Backward    Forward      │ Divide-Conquer │
   Merge       Merge       │ (log K rounds) │
(LC 88)      (LC 21)       └────────────────┘
```

## Pattern Selection Guide

### Use Heap-based K-Way Merge when:

- ✅ K is large (heap maintains only K elements)
- ✅ Input is streams/iterators (don't need all data at once)
- ✅ Elements arrive incrementally
- ✅ K varies at runtime

### Use Divide-and-Conquer when:

- ✅ All data is available upfront
- ✅ Want to avoid heap allocation
- ✅ Implementing merge sort
- ✅ K is moderate and recursion depth is acceptable

### Use Two-Pointer Merge when:

- ✅ K = 2 (exactly two sequences)
- ✅ In-place merge required (backward direction)
- ✅ Simple case where heap overhead isn't worth it

## Quick Pattern Recognition

| Problem Characteristics | Approach |
|------------------------|----------|
| "Merge K sorted X" | Heap-based K-way |
| "Merge two sorted X" | Two-pointer |
| "Merge in-place with extra space" | Backward merge |
| "External sort / streaming" | Heap-based |
| "Merge k sorted iterators" | Heap-based |

## Complexity Trade-offs

| Approach | Time | Space | Best For |
|----------|------|-------|----------|
| Heap | O(N log K) | O(K) | Large K, streaming |
| Divide-Conquer | O(N log K) | O(log K) stack | All data available |
| Two-Pointer | O(N) | O(1) | K = 2 |
| Naive Sort | O(N log N) | O(N) | Never optimal |



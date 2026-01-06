## Decision Tree

```
Start: Need window extrema (max/min)?
            │
            ▼
    ┌───────────────────┐
    │ Fixed or variable │
    │ window size?      │
    └───────────────────┘
            │
    ┌───────┴───────┐
    ▼               ▼
Fixed           Variable
    │               │
    ▼               ▼
LC 239          Need both
Single          max AND min?
deque               │
                ┌───┴───┐
                ▼       ▼
              Yes      No
                │       │
                ▼       ▼
            LC 1438   Negative
            Two       numbers?
            deques        │
                      ┌───┴───┐
                      ▼       ▼
                    Yes      No
                      │       │
                      ▼       ▼
                  LC 862   Simple
                  Prefix   sliding
                  sum      window
```

## Pattern Selection Guide

### Use Single Decreasing Deque (LC 239) when:
- Fixed window size
- Need maximum in each window
- Standard sliding window

### Use Two Deques (LC 1438) when:
- Need both max and min simultaneously
- Constraint involves max-min difference
- Variable window based on constraint

### Use Prefix Sum + Deque (LC 862) when:
- Subarray sum problems
- Array has negative numbers
- Need shortest subarray with sum >= k

### Use Transform + Deque (LC 1499) when:
- Equation can be rewritten to separate indices
- Window based on non-index metric (distance, time)
- Pair optimization problems

## Monotonic Deque vs Other Approaches

| Approach | Use When | Complexity |
|----------|----------|------------|
| Monotonic Deque | Sliding window max/min | O(n) |
| Heap | Dynamic max/min, no window constraint | O(n log n) |
| Segment Tree | Random access range queries | O(n log n) |
| Monotonic Stack | Next greater/smaller element | O(n) |

## Key Indicators for Monotonic Deque

| Clue | Pattern |
|------|---------|
| "sliding window maximum/minimum" | LC 239 |
| "longest subarray with max-min <= limit" | LC 1438 |
| "shortest subarray with sum >= k" (with negatives) | LC 862 |
| "maximize expression with distance constraint" | LC 1499 |

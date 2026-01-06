---

## Decision Flowchart

```
Start: "Select items to reach target/capacity?"
       │
       ▼
  ┌─────────────────────┐
  │ Can items be        │
  │ reused?             │
  └─────────────────────┘
       │
   ┌───┴───┐
   │       │
  No      Yes
   │       │
   ▼       ▼
  0/1    Unbounded
   │       │
   ▼       ▼
  ┌─────────────────────┐
  │ What's the goal?    │
  └─────────────────────┘
       │
   ┌───┼───┬───┐
   │   │   │   │
   ▼   ▼   ▼   ▼
Reach? Count Min Enumerate
   │   │   │   │
   ▼   ▼   ▼   ▼
  or  +=  min  Backtrack
```

### Pattern Selection Guide

| Problem Signal | Pattern | Iteration |
|----------------|---------|-----------|
| "Partition into two equal subsets" | 0/1 Boolean | Backwards |
| "Number of ways with +/-" | 0/1 Count | Backwards |
| "Minimum coins" (unlimited supply) | Unbounded Min | Forwards |
| "Number of combinations" (reusable) | Unbounded Count | Forwards |
| "List all subsets" | Backtracking | N/A |

### Iteration Direction Decision

| Question | If Yes |
|----------|--------|
| Can items be reused? | Forward iteration |
| Each item used at most once? | Backward iteration |
| Counting combinations (not permutations)? | Items outer loop |
| Counting permutations? | Amount/target outer loop |

### Transformation Patterns

Some problems need transformation before applying knapsack:

| Original Problem | Transformation |
|------------------|----------------|
| Target Sum (+/-) | subset_sum = (total + target) / 2 |
| Partition | target = total / 2 |
| Last Stone Weight | Same as partition |



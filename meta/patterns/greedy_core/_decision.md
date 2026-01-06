---

## Decision Flowchart

```
Start: "Optimization problem with local choices?"
       │
       ▼
  ┌─────────────────────┐
  │ Can reach / traverse│
  │ positions in array? │───Yes──▶ Reachability Greedy (LC 55, 45)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Circular route with │
  │ resource tracking?  │───Yes──▶ Prefix Min/Reset Greedy (LC 134)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Match/assign items  │
  │ from two sequences? │───Yes──▶ Sort + Match Greedy (LC 455, 1029)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Satisfy constraints │
  │ from both sides?    │───Yes──▶ Two-Pass Greedy (LC 135)
  └─────────────────────┘
       │ No
       ▼
  Consider Interval Greedy / Heap Greedy / DP
```

### Kernel Selection Guide

| Problem Signal | Kernel | Example |
|----------------|--------|---------|
| "Can reach", "maximum jump" | Reachability | LC 55, 45 |
| "Complete circuit", "balance tracking" | Prefix Min/Reset | LC 134 |
| "Distribute", "assign", "match" | Sort + Match | LC 455, 1029 |
| "Satisfy neighbors", "bidirectional constraint" | Two-Pass | LC 135 |

### When Greedy Fails

Greedy Core does NOT apply when:

1. **Overlapping subproblems**: Same state reached multiple ways
   - Example: Coin change (LC 322) needs DP

2. **Non-local dependencies**: Future choices affect current
   - Example: 0/1 Knapsack needs DP

3. **Multiple constraint dimensions**: Can't sort by single metric
   - Example: Meeting scheduling with rooms needs heap

### Proving Greedy Correctness

For Greedy Core problems, verify:

1. **Greedy Choice Property**: Local optimal leads to global optimal
2. **Optimal Substructure**: Solution contains optimal solutions to subproblems
3. **No need to reconsider**: Once a choice is made, it's final



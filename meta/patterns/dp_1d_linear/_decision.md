---

## Decision Flowchart

```
Start: "Optimization over a sequence?"
       │
       ▼
  ┌─────────────────────┐
  │ Count ways to       │
  │ reach end/target?   │───Yes──▶ Additive DP (LC 70, 746)
  └─────────────────────┘          dp[i] = sum of valid previous states
       │ No
       ▼
  ┌─────────────────────┐
  │ Maximize/Minimize   │
  │ with adjacency      │───Yes──▶ Include/Exclude DP (LC 198, 213)
  │ constraint?         │          dp[i] = max(dp[i-1], dp[i-2] + val)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Track running       │
  │ min/max prefix?     │───Yes──▶ Implicit DP / Kadane-style (LC 121)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Circular array      │
  │ constraint?         │───Yes──▶ Split into linear subproblems (LC 213)
  └─────────────────────┘
       │ No
       ▼
  Consider 2D DP or other patterns
```

### Pattern Selection Guide

| Problem Signal | Pattern | Example |
|----------------|---------|---------|
| "Number of ways" | Additive DP | LC 70 |
| "Minimum cost to reach" | Min DP | LC 746 |
| "Can't take adjacent" | Include/Exclude | LC 198 |
| "Circular arrangement" | Split + Linear DP | LC 213 |
| "One transaction" | Running min/max | LC 121 |

### State Definition Checklist

When defining `dp[i]`, ask:
1. What does the index `i` represent? (step, house, day)
2. What value does `dp[i]` hold? (count, max, min)
3. What are valid transitions to `dp[i]`?
4. What are the base cases?
5. Where is the final answer? (`dp[n]`, `dp[n-1]`, `max(dp)`)

### Space Optimization Decision

| Question | If Yes | If No |
|----------|--------|-------|
| Transition uses only last k states? | Optimize to O(k) | Keep O(n) array |
| Need to reconstruct path? | Keep full array | Can optimize |
| Multiple queries on same array? | Keep prefix array | Can optimize |



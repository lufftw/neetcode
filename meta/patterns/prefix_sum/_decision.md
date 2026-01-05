---

## Decision Flowchart

```
Start: "Range/subarray problem?"
       │
       ▼
  ┌─────────────────────┐
  │ Multiple range sum  │
  │ queries on STATIC   │───Yes──▶ Prefix Sum Range Query (LC 303, 304)
  │ array?              │
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Count/find subarrays│
  │ with target sum?    │───Yes──▶ Prefix Sum + Hash Map (LC 560, 525, 523)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Range UPDATE        │
  │ operations?         │───Yes──▶ Difference Array (LC 1094, 1109)
  └─────────────────────┘
       │ No
       ▼
  ┌─────────────────────┐
  │ Product of all      │
  │ except current?     │───Yes──▶ Prefix/Suffix Products (LC 238)
  └─────────────────────┘
       │ No
       ▼
  Consider other patterns
```

### Pattern Selection Guide

| Problem Signal | Pattern to Use | Example |
|----------------|----------------|---------|
| "Range sum query" + "immutable" | `PrefixSumRangeQuery` | LC 303, 304 |
| "Subarray sum equals k" | `PrefixSumSubarraySum` + Hash Map | LC 560 |
| "Equal count of X and Y" | Transform + Prefix Sum | LC 525 |
| "Subarray sum divisible by k" | Prefix Sum + Modular Arithmetic | LC 523 |
| "Add value to range [i, j]" | Difference Array | LC 1094, 1109 |
| "Product except self" | Prefix/Suffix Products | LC 238 |
| "2D rectangle sum" | 2D Prefix Sum | LC 304 |

### Hash Map Initialization Decision

| Problem Type | Initialize With | Why |
|--------------|-----------------|-----|
| Count subarrays with sum k | `{0: 1}` | Count empty prefix |
| Longest subarray with sum k | `{0: -1}` | First occurrence at "index -1" |
| Check existence of sum k | `{0}` | Just need membership |



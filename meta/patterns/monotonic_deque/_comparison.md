## Problem Comparison

| Problem | Core Pattern | Deque Order | Window Type | Key Insight |
|---------|-------------|-------------|-------------|-------------|
| **LC 239 Sliding Max** | Single max deque | Decreasing | Fixed size | Front = current max |
| **LC 1438 Max-Min Limit** | Two deques (max+min) | Decreasing + Increasing | Variable | Shrink when max-min > limit |
| **LC 862 Shortest Sum >= K** | Prefix sum + deque | Increasing | Variable | Pop when valid, handles negatives |
| **LC 1499 Max Equation** | Transform + deque | Decreasing | x-distance | Rewrite equation to fit pattern |

## Pattern Evolution

```
LC 239 Sliding Window Maximum
    │
    │ Add second deque for min
    │ Variable window size
    ↓
LC 1438 Longest Subarray (Max-Min <= Limit)
    │
    │ Add prefix sum transformation
    │ Handle negative numbers
    ↓
LC 862 Shortest Subarray with Sum >= K
    │
    │ Algebraic transformation
    │ Non-index-based window
    ↓
LC 1499 Max Value of Equation
```

## Key Differences

### Deque Order

| Problem | Order | Why |
|---------|-------|-----|
| LC 239, 1499 | Decreasing | Need maximum value |
| LC 1438 | Both | Need both max and min |
| LC 862 | Increasing | Minimize prefix for max difference |

### Window Removal

| Problem | When to Remove from Front |
|---------|---------------------------|
| LC 239 | Index out of fixed window |
| LC 1438 | Index before left pointer |
| LC 862 | After using for valid answer |
| LC 1499 | x-distance exceeds k |

### What's Stored in Deque

| Problem | Stores |
|---------|--------|
| LC 239 | Indices |
| LC 1438 | Indices |
| LC 862 | Indices (into prefix array) |
| LC 1499 | (x, y-x) tuples |

## Problem Comparison

| Problem | Interval Meaning | Split Point | Merge Cost | Optimization |
|---------|------------------|-------------|------------|--------------|
| **LC 312 Burst Balloons** | Balloons in (i, j) | Last to burst | `nums[i]*nums[k]*nums[j]` | Maximize |
| **LC 1039 Polygon** | Vertices i to j | Third vertex | `v[i]*v[k]*v[j]` | Minimize |
| **LC 1547 Cut Stick** | Between cuts i, j | Cut position | `cuts[j] - cuts[i]` | Minimize |
| **LC 664 Strange Printer** | Characters i to j | Matching char | N/A (special) | Minimize |

## Pattern Evolution

```
LC 312 Burst Balloons (Base)
    │
    │ Same structure, geometric interpretation
    ↓
LC 1039 Polygon Triangulation
    │
    │ Apply to cuts instead of items
    │ Add boundary preprocessing
    ↓
LC 1547 Minimum Cost to Cut a Stick
    │
    │ Character-based optimization
    │ Different recurrence
    ↓
LC 664 Strange Printer
```

## Key Differences

### Interval Definition

| Problem | `dp[i][j]` Meaning |
|---------|-------------------|
| LC 312 | Max coins bursting balloons in (i, j) exclusive |
| LC 1039 | Min cost triangulating vertices [i, j] inclusive |
| LC 1547 | Min cost cutting between positions cuts[i] and cuts[j] |
| LC 664 | Min turns printing s[i:j+1] |

### Preprocessing Required

| Problem | Preprocessing |
|---------|---------------|
| LC 312 | Add virtual balloons [1] at boundaries |
| LC 1039 | None |
| LC 1547 | Add 0 and n to cuts, sort |
| LC 664 | Remove consecutive duplicate characters |

### Loop Structure

| Problem | Outer Loop | Inner Split |
|---------|------------|-------------|
| LC 312 | length 2 to n | k from i+1 to j-1 |
| LC 1039 | length 3 to n | k from i+1 to j-1 |
| LC 1547 | gap 2 to m-1 | k from i+1 to j-1 |
| LC 664 | length 2 to n | k where s[k] == s[i] |

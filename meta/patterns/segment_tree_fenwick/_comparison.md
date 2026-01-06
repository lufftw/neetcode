## Pattern Comparison

| Problem | Pattern | Data Structure | Key Technique |
|---------|---------|----------------|---------------|
| LC 307 | Range Sum + Update | BIT or Segment Tree | Direct point update |
| LC 315 | Count Inversions | BIT + Compression | Right-to-left counting |
| LC 327 | Range Sum Count | Merge Sort or BIT | Prefix sum + range counting |

### When to Use Which

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| Simple range sum with updates | **Fenwick Tree** | Simpler, less code |
| Range min/max queries | **Segment Tree** | BIT only works for prefix sums |
| Counting/frequency with compression | **BIT** | Natural fit for prefix queries |
| 2D range queries | **2D Segment Tree** | More flexible than 2D BIT |

### Complexity Summary

| Problem | Time Complexity | Space Complexity |
|---------|-----------------|------------------|
| LC 307 | O(n) build + O(log n) ops | O(n) |
| LC 315 | O(n log n) | O(n) |
| LC 327 | O(n log n) | O(n) |

---


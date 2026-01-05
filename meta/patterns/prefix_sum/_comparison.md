---

## Pattern Comparison

### Prefix Sum vs Sliding Window

| Aspect | Prefix Sum | Sliding Window |
|--------|------------|----------------|
| **Use When** | Negative numbers allowed | All positive or monotonic |
| **Window Type** | Any subarray (computed via difference) | Contiguous, expanding/shrinking |
| **Complexity** | O(n) time, O(n) space | O(n) time, O(1) space |
| **Key Insight** | Sum difference = subarray sum | Monotonic sum/count |

**Example**: Find subarray with sum = k
- Negative numbers: Use Prefix Sum + Hash Map (LC 560)
- Positive only: Can use Sliding Window (LC 209)

### Prefix Sum vs Difference Array

| Aspect | Prefix Sum | Difference Array |
|--------|------------|------------------|
| **Direction** | Point values → Range sums | Range updates → Point values |
| **Build** | `prefix[i] = prefix[i-1] + nums[i-1]` | `diff[start] += val, diff[end+1] -= val` |
| **Query** | `prefix[r+1] - prefix[l]` → O(1) | Prefix sum of diff → O(n) |
| **Best For** | Many range sum queries | Many range update operations |

They are **inverses** of each other:
```
Prefix Sum: nums → prefix (cumulative sum)
Difference: prefix → nums (consecutive differences)
```

### 1D vs 2D Prefix Sum

| Aspect | 1D Prefix Sum | 2D Prefix Sum |
|--------|---------------|---------------|
| **Formula** | `prefix[j+1] - prefix[i]` | Inclusion-exclusion with 4 terms |
| **Build** | O(n) | O(m * n) |
| **Query** | O(1) | O(1) |
| **Space** | O(n) | O(m * n) |



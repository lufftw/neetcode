# Prefix Sum Patterns: Complete Reference

> **API Kernel**: `PrefixSumRangeQuery`
> **Core Mechanism**: Precompute cumulative sums for O(1) range sum queries.

This document presents the **canonical prefix sum template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Core Concepts

### The Prefix Sum Principle

Given an array `nums`, the prefix sum `P[i]` represents the sum of elements from index 0 to i-1:

```
nums:   [a, b, c, d, e]
        ↓  ↓  ↓  ↓  ↓
prefix: [0, a, a+b, a+b+c, a+b+c+d, a+b+c+d+e]
         ↑
         Empty prefix (crucial for index 0 queries)
```

**Key Formula**: Range sum `[i, j]` = `prefix[j+1] - prefix[i]`

### Universal Template Structure

```python
def build_prefix_sum(nums: List[int]) -> List[int]:
    """
    Build prefix sum array.

    prefix[i] = sum of nums[0..i-1] (elements BEFORE index i)
    Range sum [left, right] = prefix[right+1] - prefix[left]

    Why prefix[0] = 0?
    - Handles range queries starting at index 0: sum[0..right] = prefix[right+1] - prefix[0]
    - Without it, we'd need special case handling for left=0
    """
    prefix = [0]  # Empty prefix
    for num in nums:
        prefix.append(prefix[-1] + num)
    return prefix
```

### Pattern Variants

| Variant | API Kernel | Use When | Key Insight |
|---------|------------|----------|-------------|
| **Range Query** | `PrefixSumRangeQuery` | Multiple range sum queries | Precompute once, query O(1) |
| **Subarray Sum = K** | `PrefixSumSubarraySum` | Count/find subarrays with target sum | Hash map: `prefix - k` |
| **Difference Array** | `DifferenceArray` | Range update operations | Inverse of prefix sum |
| **2D Prefix Sum** | `PrefixSum2D` | Rectangle sum queries | Inclusion-exclusion principle |
| **Prefix Product** | `PrefixProduct` | Product of array except self | Prefix and suffix products |

### Why Sliding Window Fails for Subarray Sum

With negative numbers, adding an element may increase or decrease the sum, breaking the monotonicity required for sliding window. Prefix sum + hash map handles this in O(n).

```
nums = [1, -1, 1]  k = 1
Window [0,0] sum=1  ✓
Window [0,1] sum=0  ✗ (but subarrays [0,0], [2,2], [0,2] all sum to 1!)

Sliding window would miss valid subarrays because sum is not monotonic.
```



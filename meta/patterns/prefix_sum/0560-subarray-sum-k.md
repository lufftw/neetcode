## Subarray Sum Equals K (LeetCode 560)

> **Problem**: Count the number of contiguous subarrays with sum equal to k.
> **Invariant**: Hash map stores count of each prefix sum seen so far.
> **Role**: CORE VARIANT for `PrefixSumSubarraySum` API Kernel.

### Why Prefix Sum + Hash Map?

If `prefix[j] - prefix[i] = k`, then subarray `(i, j]` sums to k.

**Key Insight**: For each position j, count how many positions i exist where `prefix[i] = prefix[j] - k`.

```
nums = [1, 2, 3], k = 3

Position 0: prefix = 1, need prefix = -2 (count: 0)
Position 1: prefix = 3, need prefix = 0  (count: 1 from init)  -> Found: subarray [0,1]
Position 2: prefix = 6, need prefix = 3  (count: 1)            -> Found: subarray [2,2]

Answer: 2 subarrays with sum = 3
```

### Implementation

```python
class SolutionPrefixSum:
    """
    Count subarrays with sum = k using prefix sum + hash map.

    Algorithm:
    1. Track running prefix sum
    2. For each position, count how many times (prefix_sum - k) appeared before
    3. Record current prefix sum for future positions

    Why Initialize {0: 1}?
    - Handles subarrays starting from index 0
    - If prefix_sum == k at position i, the subarray [0..i] sums to k
    - We need to count the "empty prefix" (sum 0 before index 0)

    Time: O(n) | Space: O(n)
    """
    def subarraySum(self, nums: List[int], k: int) -> int:
        subarray_count = 0
        prefix_sum = 0

        # Map: prefix_sum value -> count of occurrences
        # Initialize with {0: 1} for subarrays starting at index 0
        sum_frequency: dict[int, int] = {0: 1}

        for num in nums:
            # Extend prefix sum with current element
            prefix_sum += num

            # Count subarrays ending here with sum = k
            # If (prefix_sum - k) was seen before, those positions mark valid starts
            complement = prefix_sum - k
            subarray_count += sum_frequency.get(complement, 0)

            # Record current prefix sum for future elements
            sum_frequency[prefix_sum] = sum_frequency.get(prefix_sum, 0) + 1

        return subarray_count
```

### Trace Example

```
nums = [1, 1, 1], k = 2

Step 0: prefix=1, complement=-1, count=0, map={0:1, 1:1}
Step 1: prefix=2, complement=0,  count=1, map={0:1, 1:1, 2:1}  [subarray [0,1]]
Step 2: prefix=3, complement=1,  count=2, map={0:1, 1:1, 2:1, 3:1}  [subarray [1,2]]

Answer: 2
```

### Why {0: 1} Initialization is Critical

Without `{0: 1}`:
```
nums = [3], k = 3
prefix = 3, complement = 0
sum_frequency = {} -> count = 0  WRONG! Should be 1.
```

With `{0: 1}`:
```
nums = [3], k = 3
prefix = 3, complement = 0
sum_frequency = {0: 1} -> count = 1  ✓
```



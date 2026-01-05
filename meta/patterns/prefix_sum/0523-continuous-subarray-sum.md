## Continuous Subarray Sum (LeetCode 523)

> **Problem**: Check if array has a contiguous subarray of size >= 2 that sums to a multiple of k.
> **Invariant**: If `prefix[j] % k == prefix[i] % k`, then subarray (i, j] sum is divisible by k.
> **Role**: MODULAR ARITHMETIC VARIANT of prefix sum.

### The Modular Arithmetic Insight

If `prefix[j] - prefix[i]` is divisible by k, then:
`prefix[j] % k == prefix[i] % k`

This is because:
```
prefix[j] = q1 * k + r
prefix[i] = q2 * k + r  (same remainder r)
prefix[j] - prefix[i] = (q1 - q2) * k  (divisible by k!)
```

### Implementation

```python
class SolutionModular:
    """
    Check if subarray of size >= 2 sums to multiple of k.

    Modular Arithmetic Insight:
    - (prefix[j] - prefix[i]) % k == 0 iff prefix[j] % k == prefix[i] % k
    - Track first occurrence of each remainder
    - Ensure subarray length >= 2: j - i >= 2

    Edge Case: k = 0 is not possible per constraints (k >= 1)

    Time: O(n) | Space: O(min(n, k))
    """
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        # Map: remainder -> first index with this remainder
        # Initialize with {0: -1} for subarrays starting at index 0
        remainder_first_index: dict[int, int] = {0: -1}
        prefix_sum = 0

        for index, num in enumerate(nums):
            prefix_sum += num
            remainder = prefix_sum % k

            if remainder in remainder_first_index:
                # Check if subarray length >= 2
                if index - remainder_first_index[remainder] >= 2:
                    return True
            else:
                # Only store first occurrence (to maximize length)
                remainder_first_index[remainder] = index

        return False
```

### Trace Example

```
nums = [23, 2, 4, 6, 7], k = 6

Index 0: prefix=23, rem=5, map={0:-1, 5:0}
Index 1: prefix=25, rem=1, map={0:-1, 5:0, 1:1}
Index 2: prefix=29, rem=5, 5 in map at 0, length=2-0=2 >= 2  -> True!

Subarray [2, 4] sums to 6, divisible by 6 ✓
```

### Why Length >= 2 Check

Problem requires subarray of size at least 2:
```
nums = [5], k = 5
prefix = 5, remainder = 0

0 is in map at -1, length = 0 - (-1) = 1 < 2  -> False (correct!)
```

### Edge Cases

| Case | Handling |
|------|----------|
| Consecutive zeros `[0, 0]` | prefix = 0 at both, 0 % k = 0, length 2 ✓ |
| Single element | Always false (length < 2) |
| k = 1 | Any subarray of size >= 2 works |



## Variation: Contribution / Counting via Boundaries

> **Problem**: Sum of subarray minimums (LeetCode 907).
> **Key Insight**: Each element's contribution = element × (left_count) × (right_count).

### Contribution Counting Formula

For element at index `i` with value `v`:
- Let `L` = number of consecutive elements to the left where `v` is the minimum
- Let `R` = number of consecutive elements to the right where `v` is the minimum
- Element's contribution to total sum = `v × L × R`

This counts exactly how many subarrays have `v` as their minimum.

```
Array: [3, 1, 2, 4]
Element 1 at index 1:
  L = 2 (can extend to include index 0)
  R = 3 (can extend to include indices 2, 3)
  Contribution = 1 × 2 × 3 = 6

  Subarrays where 1 is minimum:
  [3,1], [1], [1,2], [1,2,4], [3,1,2], [3,1,2,4] → 6 subarrays
```

### Sum of Subarray Minimums (LeetCode 907)

```python
def sum_of_subarray_minimums(arr: list[int]) -> int:
    """
    Sum of minimums of all subarrays.

    Algorithm:
    - For each element, find left/right boundaries (previous/next smaller)
    - Use asymmetric tie-breaking to avoid double-counting duplicates:
      - Left boundary: strictly smaller (<)
      - Right boundary: smaller or equal (<=)

    Time: O(n), Space: O(n)
    """
    MOD = 10**9 + 7
    n = len(arr)

    # left[i] = distance to previous smaller element
    # right[i] = distance to next smaller or equal element
    left = [0] * n
    right = [0] * n

    # Compute left boundaries (previous strictly smaller)
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:  # >= for strict <
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    # Compute right boundaries (next smaller or equal)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:  # > for <=
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)

    # Sum contributions
    result = 0
    for i in range(n):
        result = (result + arr[i] * left[i] * right[i]) % MOD

    return result
```

### Asymmetric Tie-Breaking for Duplicates

When duplicates exist, we must avoid counting the same subarray twice:
- **Left boundary**: Use strict comparison (`<`) → previous strictly smaller
- **Right boundary**: Use non-strict comparison (`<=`) → next smaller or equal

This creates a "left-closed, right-open" style where each subarray is counted exactly once.

### Sum of Subarray Ranges (LeetCode 2104)

```python
def sum_of_subarray_ranges(nums: list[int]) -> int:
    """
    Sum of (max - min) for all subarrays.

    = Sum of all subarray maximums - Sum of all subarray minimums

    Use dual stacks: one for max contribution, one for min contribution.

    Time: O(n), Space: O(n)
    """
    n = len(nums)

    def sum_of_extremes(compare_greater: bool) -> int:
        """Compute sum of subarray max (if True) or min (if False)."""
        left = [0] * n
        right = [0] * n
        stack = []

        # Comparison functions for max vs min
        def dominates(a, b):
            return a > b if compare_greater else a < b

        def dominates_or_equal(a, b):
            return a >= b if compare_greater else a <= b

        # Left boundaries
        for i in range(n):
            while stack and dominates_or_equal(nums[i], nums[stack[-1]]):
                stack.pop()
            left[i] = i - stack[-1] if stack else i + 1
            stack.append(i)

        # Right boundaries
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and dominates(nums[i], nums[stack[-1]]):
                stack.pop()
            right[i] = stack[-1] - i if stack else n - i
            stack.append(i)

        return sum(nums[i] * left[i] * right[i] for i in range(n))

    sum_max = sum_of_extremes(True)
    sum_min = sum_of_extremes(False)
    return sum_max - sum_min
```



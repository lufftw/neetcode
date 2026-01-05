## Base Template: Range Sum Query (LeetCode 303)

> **Problem**: Handle multiple range sum queries on an immutable array efficiently.
> **Invariant**: `prefix[i]` = sum of all elements before index `i`.
> **Role**: BASE TEMPLATE for `PrefixSumRangeQuery` API Kernel.

### Implementation

```python
class NumArray:
    """
    Range sum query with O(n) preprocessing and O(1) queries.

    Prefix Sum Mechanics:
    - prefix[0] = 0 (empty prefix, handles edge case of full array sum)
    - prefix[i] = sum(nums[0:i])
    - Range sum [left, right] = prefix[right+1] - prefix[left]

    Why prefix[right+1] - prefix[left]?
    prefix[right+1] = nums[0] + nums[1] + ... + nums[right]
    prefix[left]    = nums[0] + nums[1] + ... + nums[left-1]
    Difference      = nums[left] + nums[left+1] + ... + nums[right]

    Time: O(n) init, O(1) query | Space: O(n)
    """
    def __init__(self, nums: List[int]):
        # Initialize with 0 for empty prefix
        self.prefix_sum: List[int] = [0]
        for num in nums:
            self.prefix_sum.append(self.prefix_sum[-1] + num)

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix_sum[right + 1] - self.prefix_sum[left]
```

### Why This Works

```
Index:    0   1   2   3   4    5
nums:   [-2,  0,  3, -5,  2,  -1]
prefix: [0, -2, -2,  1, -4, -2, -3]
         ^
         Empty prefix

Query sumRange(0, 2):
  = prefix[3] - prefix[0]
  = 1 - 0 = 1
  = nums[0] + nums[1] + nums[2] = -2 + 0 + 3 = 1 ✓

Query sumRange(2, 5):
  = prefix[6] - prefix[2]
  = -3 - (-2) = -1
  = nums[2] + nums[3] + nums[4] + nums[5] = 3 + (-5) + 2 + (-1) = -1 ✓
```

### Edge Cases

| Case | How Handled |
|------|-------------|
| Query entire array `[0, n-1]` | `prefix[n] - prefix[0]` = total sum |
| Single element `[i, i]` | `prefix[i+1] - prefix[i]` = `nums[i]` |
| Empty array | `prefix = [0]`, no valid queries |



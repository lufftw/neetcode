## Variant: House Robber (LeetCode 198)

> **Problem**: Maximize loot from non-adjacent houses (can't rob two consecutive houses).
> **State**: `dp[i]` = maximum loot considering houses 0 to i.
> **Delta from Base**: Include/exclude decision at each house.

### Implementation

```python
class Solution:
    """
    1D DP: Include/Exclude decision at each step.

    State: dp[i] = maximum loot from houses[0..i]
    Transition: dp[i] = max(
        dp[i-1],           # Skip current house, keep previous best
        dp[i-2] + nums[i]  # Rob current house, add to best before adjacent
    )
    Base: dp[0] = nums[0], dp[1] = max(nums[0], nums[1])

    The classic "take or skip" pattern.

    Time: O(n) | Space: O(1)
    """
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        # Space-optimized
        prev2 = nums[0]                    # Best up to house i-2
        prev1 = max(nums[0], nums[1])      # Best up to house i-1

        for i in range(2, len(nums)):
            current = max(prev1, prev2 + nums[i])
            prev2 = prev1
            prev1 = current

        return prev1
```

### The Include/Exclude Framework

At each house, you have two choices:
1. **Skip** (exclude): Take whatever you had before → `dp[i-1]`
2. **Rob** (include): Take this house + best non-adjacent → `dp[i-2] + nums[i]`

This framework applies to many DP problems!

### Trace Example

```
nums: [2, 7, 9, 3, 1]

i=0: prev2 = 2
i=1: prev1 = max(2, 7) = 7
i=2: current = max(7, 2+9) = 11, prev2=7, prev1=11
i=3: current = max(11, 7+3) = 11, prev2=11, prev1=11
i=4: current = max(11, 11+1) = 12

Result: 12 (rob houses 0, 2, 4 → 2+9+1=12)
```

### Edge Cases

| Case | Input | Output | Handling |
|------|-------|--------|----------|
| Single house | [5] | 5 | Base case |
| Two houses | [2, 3] | 3 | max of both |
| All same value | [1, 1, 1, 1] | 2 | Rob alternate |



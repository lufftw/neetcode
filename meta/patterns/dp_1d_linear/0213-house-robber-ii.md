## Variant: House Robber II (LeetCode 213)

> **Problem**: Houses are arranged in a circle; first and last house are adjacent.
> **State**: Same as House Robber, but handle circular constraint.
> **Delta from Base**: Split into two subproblems to avoid circular conflict.

### Implementation

```python
class Solution:
    """
    Circular DP: Split into two linear subproblems.

    Key Insight: First and last houses are adjacent, so we can't rob both.
    Solution: Take the maximum of two scenarios:
        1. Rob houses[0..n-2] (exclude last house)
        2. Rob houses[1..n-1] (exclude first house)

    This transforms circular DP into two linear DP problems.

    Time: O(n) | Space: O(1)
    """
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        # Helper: linear house robber on subarray
        def rob_linear(houses: List[int]) -> int:
            if not houses:
                return 0
            if len(houses) == 1:
                return houses[0]

            prev2 = houses[0]
            prev1 = max(houses[0], houses[1])

            for i in range(2, len(houses)):
                current = max(prev1, prev2 + houses[i])
                prev2 = prev1
                prev1 = current

            return prev1

        # Two scenarios: exclude last OR exclude first
        return max(
            rob_linear(nums[:-1]),  # Houses 0 to n-2
            rob_linear(nums[1:])   # Houses 1 to n-1
        )
```

### Why Split Works

The circular constraint means: "Don't rob both first and last."

By splitting into two ranges:
- `[0, n-2]`: First house is eligible, last is excluded → no conflict
- `[1, n-1]`: Last house is eligible, first is excluded → no conflict

One of these must contain the optimal solution.

### Trace Example

```
nums: [2, 3, 2]

Scenario 1: nums[0..1] = [2, 3] → max = 3
Scenario 2: nums[1..2] = [3, 2] → max = 3

Result: max(3, 3) = 3
(Can't rob all three because first and last are adjacent)
```

### Pattern: Circular → Linear Decomposition

This technique generalizes:
- Circular array problems often decompose into linear subproblems
- Break the circle by fixing one element's state (include/exclude)



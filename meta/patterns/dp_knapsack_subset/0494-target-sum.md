## Variant: Target Sum (LeetCode 494)

> **Problem**: Count ways to assign +/- to each number to reach target sum.
> **State**: `dp[s]` = number of ways to reach sum s.
> **Delta from Base**: Count instead of boolean, transform to subset sum.

### Implementation

```python
class Solution:
    """
    0/1 Knapsack: Count ways to reach target.

    Key Insight: Transform +/- assignment to subset selection.
    - Let P = sum of numbers with + sign
    - Let N = sum of numbers with - sign
    - P - N = target, P + N = total
    - Therefore: P = (target + total) / 2

    We need to count subsets summing to P (positive group).

    State: dp[s] = number of ways to form sum s
    Transition: dp[s] += dp[s - num]
    Base: dp[0] = 1 (one way: empty subset)

    Time: O(n * sum) | Space: O(sum)
    """
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = sum(nums)

        # Check feasibility
        if (total + target) % 2 != 0 or total + target < 0:
            return 0

        subset_sum = (total + target) // 2
        dp = [0] * (subset_sum + 1)
        dp[0] = 1  # One way to form sum 0

        for num in nums:
            # Backwards for 0/1 (each number used once)
            for s in range(subset_sum, num - 1, -1):
                dp[s] += dp[s - num]

        return dp[subset_sum]
```

### The Transformation Trick

The problem says: assign + or - to each number.
- Numbers with + form set P
- Numbers with - form set N

Equations:
- P - N = target (given)
- P + N = total (sum of all)

Solving: P = (target + total) / 2

**This transforms the problem into: count subsets summing to P.**

### Trace Example

```
nums: [1, 1, 1, 1, 1], target = 3
total = 5, P = (3 + 5) / 2 = 4

Count subsets summing to 4:
- {1,1,1,1} from indices 0,1,2,3
- {1,1,1,1} from indices 0,1,2,4
- {1,1,1,1} from indices 0,1,3,4
- {1,1,1,1} from indices 0,2,3,4
- {1,1,1,1} from indices 1,2,3,4

Result: 5 ways
```



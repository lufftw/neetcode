## Base Template: Partition Equal Subset Sum (LeetCode 416)

> **Problem**: Can array be partitioned into two subsets with equal sum?
> **State**: `dp[s]` = True if sum s is achievable.
> **Role**: BASE TEMPLATE for 0/1 subset sum.

### Implementation

```python
class Solution:
    """
    0/1 Knapsack: Can we select items to reach target sum?

    Key Insight: If total sum is S, we need to find a subset summing to S/2.
    If such a subset exists, the remaining elements also sum to S/2.

    State: dp[s] = True if sum s is achievable using some subset
    Transition: dp[s] = dp[s] or dp[s - num] (take or skip)
    Base: dp[0] = True (empty subset has sum 0)

    Why iterate backwards? Each number can only be used once.
    Forward iteration would use the same number multiple times.

    Time: O(n * sum) | Space: O(sum)
    """
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # Odd sum can't be split evenly
        if total % 2 != 0:
            return False

        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True  # Empty subset

        for num in nums:
            # Iterate backwards to ensure each num used at most once
            for s in range(target, num - 1, -1):
                dp[s] = dp[s] or dp[s - num]

        return dp[target]
```

### Why Backwards Iteration?

Consider `nums = [1, 5, 5]`, target = 5:

**Forward (wrong for 0/1):**
```
dp = [T, F, F, F, F, F]
num = 1: dp[1] = dp[0] = T → [T, T, F, F, F, F]
         dp[2] = dp[1] = T → [T, T, T, F, F, F]  # Used 1 twice!
```

**Backwards (correct):**
```
dp = [T, F, F, F, F, F]
num = 1: dp[1] = dp[0] = T → [T, T, F, F, F, F]
num = 5: dp[5] = dp[0] = T → [T, T, F, F, F, T]
```

### Trace Example

```
nums: [1, 5, 11, 5], total = 22, target = 11

dp = [T, F, F, F, F, F, F, F, F, F, F, F]

num=1:  dp[1] = T
num=5:  dp[6] = dp[1] = T, dp[5] = dp[0] = T
num=11: dp[11] = dp[0] = T ✓

Result: True (subsets: {11} and {1,5,5})
```



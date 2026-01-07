## Variant: Predict the Winner (LeetCode 486)

> **Problem**: Two players take turns selecting numbers from either end of array. Predict if Player 1 can win or tie (not strictly less than Player 2).
> **Invariant**: Track score difference from current player's perspective.
> **Delta from Base**: Handle tie case (>=0 instead of >0), odd number of elements allowed.

### Key Insight

This is almost identical to Stone Game (LC 877), but:
1. Works with any number of elements (not just even)
2. Tie counts as Player 1 winning (>= 0 instead of > 0)
3. Player 1 wins if `dp(0, n-1) >= 0`

### Implementation

```python
class Solution:
    def predictTheWinner(self, nums: list[int]) -> bool:
        """
        Return True if Player 1 can win or tie.

        dp(i, j) = max score difference current player can achieve
                   from nums[i..j].

        Player 1 wins if dp(0, n-1) >= 0.
        """
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(left: int, right: int) -> int:
            if left > right:
                return 0

            take_left = nums[left] - dp(left + 1, right)
            take_right = nums[right] - dp(left, right - 1)

            return max(take_left, take_right)

        return dp(0, len(nums) - 1) >= 0
```

### Bottom-Up Alternative

```python
class SolutionBottomUp:
    def predictTheWinner(self, nums: list[int]) -> bool:
        """
        Bottom-up DP with O(n) space optimization.

        dp[j] represents score difference for interval ending at j.
        """
        n = len(nums)
        dp = nums[:]  # Base case: single element intervals

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                # dp[j] currently holds dp[i+1][j] from previous iteration
                take_left = nums[i] - dp[j]
                # After this update, dp[j-1] holds dp[i][j-1]
                take_right = nums[j] - dp[j - 1]
                dp[j] = max(take_left, take_right)

        return dp[n - 1] >= 0
```

### Trace Example

```
nums = [1, 5, 2]

Base cases:
dp(0, 0) = 1, dp(1, 1) = 5, dp(2, 2) = 2

dp(0, 1):
  - Take 1: 1 - dp(1, 1) = 1 - 5 = -4
  - Take 5: 5 - dp(0, 0) = 5 - 1 = 4
  → dp(0, 1) = 4

dp(1, 2):
  - Take 5: 5 - dp(2, 2) = 5 - 2 = 3
  - Take 2: 2 - dp(1, 1) = 2 - 5 = -3
  → dp(1, 2) = 3

dp(0, 2):
  - Take 1: 1 - dp(1, 2) = 1 - 3 = -2
  - Take 2: 2 - dp(0, 1) = 2 - 4 = -2
  → dp(0, 2) = -2

Player 1 score diff = -2 < 0, so Player 1 loses.
```

### Comparison with Stone Game

| Aspect | Stone Game (877) | Predict Winner (486) |
|--------|------------------|----------------------|
| Elements | Even only | Any number |
| Win condition | diff > 0 | diff >= 0 |
| Tie handling | N/A | Counts as P1 win |
| Math solution | Yes (always True) | No (need DP) |

### Complexity

- Time: O(n²) with memoization
- Space: O(n²) with memoization, O(n) with bottom-up optimization

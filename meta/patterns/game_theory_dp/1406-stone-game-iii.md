## Variant: Stone Game III (LeetCode 1406)

> **Problem**: Alice and Bob play with stone values (can be negative). Each turn, player takes 1, 2, or 3 stones from the front. Return "Alice", "Bob", or "Tie".
> **Invariant**: Track score difference from current player's perspective.
> **Delta from Base**: Fixed 1-3 choices per turn, negative values allowed, taken from front only.

### Key Insight

Similar to interval games but:
1. Always take from the front (start index only)
2. Fixed choices: 1, 2, or 3 stones
3. Negative values make strategy non-trivial

### Implementation

```python
class Solution:
    def stoneGameIII(self, stoneValue: list[int]) -> str:
        """
        Return winner: "Alice", "Bob", or "Tie".

        dp(start) = max score difference current player can achieve
                    starting from index start.
        """
        n = len(stoneValue)

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(start: int) -> int:
            if start >= n:
                return 0

            best = float('-inf')
            stones_taken = 0

            for take in range(1, 4):
                if start + take > n:
                    break

                stones_taken += stoneValue[start + take - 1]

                # Score gained minus opponent's best outcome
                value = stones_taken - dp(start + take)
                best = max(best, value)

            return best

        diff = dp(0)

        if diff > 0:
            return "Alice"
        elif diff < 0:
            return "Bob"
        else:
            return "Tie"
```

### Bottom-Up with Space Optimization

```python
class SolutionBottomUp:
    def stoneGameIII(self, stoneValue: list[int]) -> str:
        """
        Bottom-up DP with O(1) space using rolling array.

        Only need dp[i+1], dp[i+2], dp[i+3] to compute dp[i].
        """
        n = len(stoneValue)

        # dp[i] = best score difference from position i
        # Only need last 3 values
        dp = [0] * 4  # dp[i % 4]

        for i in range(n - 1, -1, -1):
            best = float('-inf')
            stones = 0

            for take in range(1, 4):
                if i + take > n:
                    break
                stones += stoneValue[i + take - 1]
                value = stones - dp[(i + take) % 4]
                best = max(best, value)

            dp[i % 4] = best

        diff = dp[0]

        if diff > 0:
            return "Alice"
        elif diff < 0:
            return "Bob"
        else:
            return "Tie"
```

### Trace Example

```
stoneValue = [1, 2, 3, 7]

dp(3): only take 1 stone (7)
  → 7 - dp(4) = 7 - 0 = 7

dp(2): can take 1, 2, or 3 stones
  Take 1: 3 - dp(3) = 3 - 7 = -4
  Take 2: 3+7 - dp(4) = 10 - 0 = 10
  → dp(2) = max(-4, 10) = 10

dp(1): can take 1, 2, or 3
  Take 1: 2 - dp(2) = 2 - 10 = -8
  Take 2: 2+3 - dp(3) = 5 - 7 = -2
  Take 3: 2+3+7 - dp(4) = 12 - 0 = 12
  → dp(1) = max(-8, -2, 12) = 12

dp(0): can take 1, 2, or 3
  Take 1: 1 - dp(1) = 1 - 12 = -11
  Take 2: 1+2 - dp(2) = 3 - 10 = -7
  Take 3: 1+2+3 - dp(3) = 6 - 7 = -1
  → dp(0) = max(-11, -7, -1) = -1

diff = -1 < 0 → "Bob" wins
```

### Key Insights

1. **Negative Values Matter**: Can't just take maximum - might set up opponent.
2. **Fixed Choices**: Unlike Stone Game II, always 1-3 choices.
3. **Space Optimization**: Rolling array since only need 3 previous values.

### Comparison Table

| Game | Choices | Direction | Values |
|------|---------|-----------|--------|
| 877 | 1 (ends) | Either end | Positive |
| 486 | 1 (ends) | Either end | Any |
| 1140 | 1 to 2M | Front | Positive |
| 1406 | 1, 2, 3 | Front | Any |

### Complexity

- Time: O(n) with memoization
- Space: O(n) with memoization, O(1) with rolling array

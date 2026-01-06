## Variant: Coin Change (LeetCode 322)

> **Problem**: Minimum coins needed to make amount (coins can be reused).
> **State**: `dp[a]` = minimum coins to make amount a.
> **Delta from Base**: Unbounded (reuse allowed), minimize instead of count.

### Implementation

```python
class Solution:
    """
    Unbounded Knapsack: Minimum items to reach target.

    Key Differences from 0/1:
    - Coins can be reused → iterate forwards
    - Goal is minimize → use min() instead of sum/or
    - Initialize with infinity (impossible until proven otherwise)

    State: dp[a] = minimum coins to make amount a
    Transition: dp[a] = min(dp[a], dp[a - coin] + 1)
    Base: dp[0] = 0 (zero coins for amount 0)

    Why iterate forwards? To allow reusing coins.
    dp[a - coin] might already include the current coin.

    Time: O(n * amount) | Space: O(amount)
    """
    def coinChange(self, coins: List[int], amount: int) -> int:
        # Initialize with "impossible" value
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0  # Zero coins for amount 0

        for coin in coins:
            # Forward iteration: coins can be reused
            for a in range(coin, amount + 1):
                dp[a] = min(dp[a], dp[a - coin] + 1)

        return dp[amount] if dp[amount] != float('inf') else -1
```

### Why Forward Iteration for Unbounded?

Consider `coins = [2]`, amount = 4:

**Forward (correct for unbounded):**
```
dp = [0, inf, inf, inf, inf]
coin = 2:
  a=2: dp[2] = min(inf, dp[0]+1) = 1
  a=4: dp[4] = min(inf, dp[2]+1) = 2  # Reused coin 2!
```

**Backwards (wrong for unbounded):**
```
dp = [0, inf, inf, inf, inf]
coin = 2:
  a=4: dp[4] = min(inf, dp[2]+1) = inf  # dp[2] not yet computed
  a=2: dp[2] = min(inf, dp[0]+1) = 1
```

### Trace Example

```
coins: [1, 2, 5], amount = 11

dp = [0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]

coin=1: dp[1]=1, dp[2]=2, ..., dp[11]=11
coin=2: dp[2]=1, dp[3]=2, dp[4]=2, ..., dp[11]=6
coin=5: dp[5]=1, dp[6]=2, dp[7]=2, ..., dp[10]=2, dp[11]=3

Result: 3 coins (5 + 5 + 1)
```



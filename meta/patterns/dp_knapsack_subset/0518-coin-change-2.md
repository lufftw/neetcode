## Variant: Coin Change 2 (LeetCode 518)

> **Problem**: Count number of ways to make amount (coins can be reused).
> **State**: `dp[a]` = number of ways to make amount a.
> **Delta from Coin Change: Count ways instead of minimize.

### Implementation

```python
class Solution:
    """
    Unbounded Knapsack: Count ways to reach target.

    Key Insight: Same as Coin Change but counting instead of minimizing.
    - Coins can be reused → forward iteration
    - Count ways → use += instead of min()
    - Combinations (not permutations) → coins outer, amount inner

    State: dp[a] = number of ways to make amount a
    Transition: dp[a] += dp[a - coin]
    Base: dp[0] = 1 (one way to make amount 0: use no coins)

    Why coins outer loop? To count combinations, not permutations.
    Amount outer would count [1,2] and [2,1] as different.

    Time: O(n * amount) | Space: O(amount)
    """
    def change(self, amount: int, coins: List[int]) -> int:
        dp = [0] * (amount + 1)
        dp[0] = 1  # One way to make amount 0

        for coin in coins:
            # Forward for unbounded
            for a in range(coin, amount + 1):
                dp[a] += dp[a - coin]

        return dp[amount]
```

### Combinations vs Permutations

The loop order matters:

**Coins outer (combinations):**
```python
for coin in coins:
    for a in range(coin, amount + 1):
        dp[a] += dp[a - coin]
```
→ Each coin is considered in sequence, so [1,2] and [2,1] are the same.

**Amount outer (permutations):**
```python
for a in range(1, amount + 1):
    for coin in coins:
        if coin <= a:
            dp[a] += dp[a - coin]
```
→ At each amount, all coins are considered, so [1,2] and [2,1] are different.

### Trace Example

```
coins: [1, 2, 5], amount = 5

dp = [1, 0, 0, 0, 0, 0]

coin=1: dp = [1, 1, 1, 1, 1, 1]
        (1), (1,1), (1,1,1), (1,1,1,1), (1,1,1,1,1)

coin=2: dp = [1, 1, 2, 2, 3, 3]
        +1 way each for (2), (1,2), (2,2), (1,1,2), (1,2,2) etc.

coin=5: dp = [1, 1, 2, 2, 3, 4]
        +1 way for (5)

Result: 4 ways: (5), (2,2,1), (2,1,1,1), (1,1,1,1,1)
```



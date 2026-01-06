## Variant: Best Time to Buy and Sell Stock (LeetCode 121)

> **Problem**: Find maximum profit from one buy-sell transaction.
> **State**: Track minimum price seen so far.
> **Delta from Base**: Implicit DP with running minimum.

### Implementation

```python
class Solution:
    """
    Implicit 1D DP: Track best buy price for each potential sell day.

    Key Insight: For each day as potential sell day, the best buy day
    is the minimum price seen before it.

    State (implicit): min_price = lowest price up to current day
    Transition: max_profit = max(max_profit, price - min_price)

    Time: O(n) | Space: O(1)
    """
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float('inf')
        max_profit = 0

        for price in prices:
            # Update best buy price seen so far
            min_price = min(min_price, price)

            # Calculate profit if we sell today
            profit_if_sell_today = price - min_price

            # Update best profit
            max_profit = max(max_profit, profit_if_sell_today)

        return max_profit
```

### Why This is 1D DP

The explicit DP formulation:
- `dp[i]` = maximum profit achievable selling on or before day i
- `min_so_far[i]` = minimum price in days 0 to i

Transition: `dp[i] = max(dp[i-1], prices[i] - min_so_far[i])`

We optimize away the array since we only need the previous values.

### Connection to House Robber Pattern

| Problem | Track | Decision |
|---------|-------|----------|
| House Robber | Best loot so far | Include or exclude current |
| Stock Buy/Sell | Min price so far | Sell today or wait |

Both follow the "optimal prefix" pattern.

### Trace Example

```
prices: [7, 1, 5, 3, 6, 4]

Day 0: min=7, profit=0
Day 1: min=1, profit=0 (would be negative)
Day 2: min=1, profit=4 (buy at 1, sell at 5)
Day 3: min=1, profit=4
Day 4: min=1, profit=5 (buy at 1, sell at 6)
Day 5: min=1, profit=5

Result: 5
```

### Edge Cases

| Case | Input | Output | Handling |
|------|-------|--------|----------|
| Decreasing prices | [7, 6, 4, 3, 1] | 0 | Never sell (profit would be negative) |
| Single day | [5] | 0 | Can't complete transaction |
| Two days, profit | [1, 5] | 4 | Buy day 0, sell day 1 |



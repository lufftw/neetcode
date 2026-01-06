---

## Template Quick Reference

### 1. 0/1 Knapsack - Boolean (Can Reach?)

```python
def can_partition(nums: List[int], target: int) -> bool:
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for s in range(target, num - 1, -1):  # Backwards!
            dp[s] = dp[s] or dp[s - num]

    return dp[target]
```

### 2. 0/1 Knapsack - Count Ways

```python
def count_subsets(nums: List[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1

    for num in nums:
        for s in range(target, num - 1, -1):  # Backwards!
            dp[s] += dp[s - num]

    return dp[target]
```

### 3. Unbounded Knapsack - Minimum Items

```python
def min_coins(coins: List[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for a in range(coin, amount + 1):  # Forwards!
            dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

### 4. Unbounded Knapsack - Count Combinations

```python
def count_combinations(coins: List[int], amount: int) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:  # Coins outer for combinations
        for a in range(coin, amount + 1):  # Forwards!
            dp[a] += dp[a - coin]

    return dp[amount]
```

### 5. Target Sum Transformation

```python
def target_sum_ways(nums: List[int], target: int) -> int:
    total = sum(nums)

    # Transform: P - N = target, P + N = total → P = (target + total) / 2
    if (total + target) % 2 != 0 or total + target < 0:
        return 0

    subset_target = (total + target) // 2
    return count_subsets(nums, subset_target)  # Use 0/1 count template
```

### 6. Generic 2D Knapsack (When 1D Won't Work)

```python
def knapsack_2d(items: List[Tuple[int, int]], capacity: int) -> int:
    """
    items: list of (weight, value)
    Returns: maximum value achievable within capacity
    """
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight, value = items[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i-1][c]  # Skip item
            if c >= weight:
                dp[i][c] = max(dp[i][c], dp[i-1][c - weight] + value)  # Take item

    return dp[n][capacity]
```

### Variable Naming Convention

| Variable | Purpose | Example |
|----------|---------|---------|
| `dp[s]` / `dp[a]` | DP array for sum/amount | `dp[target]` |
| `target` / `amount` | Goal value | `target = total // 2` |
| `num` / `coin` / `item` | Current item being processed | `for num in nums:` |
| `s` / `a` / `c` | Loop variable for sum/amount/capacity | `for s in range(target, ...)` |



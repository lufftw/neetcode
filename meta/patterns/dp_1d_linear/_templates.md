---

## Template Quick Reference

### 1. Fibonacci-Style (Count Ways)

```python
def count_ways(n: int) -> int:
    """Count ways to reach step n (1 or 2 steps at a time)."""
    if n <= 2:
        return n

    prev2, prev1 = 1, 2
    for i in range(3, n + 1):
        prev2, prev1 = prev1, prev2 + prev1

    return prev1
```

### 2. Min Cost Path

```python
def min_cost(costs: List[int]) -> int:
    """Minimum cost to reach beyond last step."""
    n = len(costs)
    if n == 1:
        return costs[0]

    prev2 = costs[0]
    prev1 = costs[1]

    for i in range(2, n):
        current = min(prev1, prev2) + costs[i]
        prev2, prev1 = prev1, current

    return min(prev1, prev2)
```

### 3. Include/Exclude (House Robber)

```python
def max_non_adjacent(nums: List[int]) -> int:
    """Maximum sum of non-adjacent elements."""
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        current = max(prev1, prev2 + nums[i])
        prev2, prev1 = prev1, current

    return prev1
```

### 4. Circular Array Decomposition

```python
def max_circular(nums: List[int]) -> int:
    """Maximum non-adjacent sum in circular array."""
    if len(nums) == 1:
        return nums[0]

    def max_linear(arr: List[int]) -> int:
        if len(arr) == 1:
            return arr[0]
        prev2 = arr[0]
        prev1 = max(arr[0], arr[1])
        for i in range(2, len(arr)):
            prev2, prev1 = prev1, max(prev1, prev2 + arr[i])
        return prev1

    return max(
        max_linear(nums[:-1]),  # Exclude last
        max_linear(nums[1:])    # Exclude first
    )
```

### 5. Running Min/Max (Kadane-Style)

```python
def max_profit_single_transaction(prices: List[int]) -> int:
    """Maximum profit from single buy-sell."""
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)

    return max_profit
```

### 6. Generic 1D DP Template

```python
def solve_1d_dp(arr: List[int], combine, initial_values: List) -> int:
    """
    Generic 1D DP template.

    Args:
        arr: Input array
        combine: Function (prev2, prev1, current_val) -> new_value
        initial_values: Base case values [dp[0], dp[1], ...]
    """
    n = len(arr)
    if n <= len(initial_values):
        return initial_values[n - 1] if n > 0 else 0

    # Initialize from base cases
    prev_values = initial_values[:]

    for i in range(len(initial_values), n):
        new_value = combine(prev_values, arr[i])
        prev_values.pop(0)
        prev_values.append(new_value)

    return prev_values[-1]
```

### Variable Naming Convention

| Variable | Purpose | Example |
|----------|---------|---------|
| `prev2` / `prev1` | Space-optimized DP values | `prev2, prev1 = prev1, current` |
| `current` | Current DP value being computed | `current = max(prev1, prev2 + val)` |
| `min_price` / `max_val` | Running minimum/maximum | `min_price = min(min_price, price)` |
| `dp[i]` | DP array (when not optimized) | `dp[i] = dp[i-1] + dp[i-2]` |



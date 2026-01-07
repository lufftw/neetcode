## Ready-to-Use Templates

### Template 1: Interval Game (Take from Ends)

```python
from functools import lru_cache

def interval_game(values: list[int]) -> int:
    """
    Two players take turns taking from either end.
    Return score difference (positive = first player wins).
    """
    @lru_cache(maxsize=None)
    def dp(left: int, right: int) -> int:
        if left > right:
            return 0

        take_left = values[left] - dp(left + 1, right)
        take_right = values[right] - dp(left, right - 1)

        return max(take_left, take_right)

    return dp(0, len(values) - 1)

# Usage:
# first_player_wins = interval_game(values) > 0  # Stone Game
# first_player_wins_or_ties = interval_game(values) >= 0  # Predict Winner
```

### Template 2: Linear Game (Take from Front)

```python
from functools import lru_cache

def linear_game(values: list[int], max_take: int = 3) -> int:
    """
    Take 1 to max_take elements from front each turn.
    Return score difference (positive = first player wins).
    """
    n = len(values)

    @lru_cache(maxsize=None)
    def dp(start: int) -> int:
        if start >= n:
            return 0

        best = float('-inf')
        total = 0

        for take in range(1, max_take + 1):
            if start + take > n:
                break
            total += values[start + take - 1]
            value = total - dp(start + take)
            best = max(best, value)

        return best

    return dp(0)

# Usage (Stone Game III):
# diff = linear_game(stones, 3)
# winner = "Alice" if diff > 0 else "Bob" if diff < 0 else "Tie"
```

### Template 3: Bitmask Game (Use Once)

```python
from functools import lru_cache

def bitmask_game(max_choice: int, target: int) -> bool:
    """
    Choose integers 1 to max_choice, each used once.
    First to reach target wins.
    Return True if first player can force a win.
    """
    total_sum = max_choice * (max_choice + 1) // 2
    if total_sum < target:
        return False
    if target <= 0:
        return True

    @lru_cache(maxsize=None)
    def can_win(mask: int, remaining: int) -> bool:
        for choice in range(1, max_choice + 1):
            if mask & (1 << choice):
                continue

            if choice >= remaining:
                return True

            if not can_win(mask | (1 << choice), remaining - choice):
                return True

        return False

    return can_win(0, target)
```

### Template 4: Variable Take with M Parameter

```python
from functools import lru_cache

def variable_take_game(piles: list[int]) -> int:
    """
    Take 1 to 2*M piles each turn, M updates to max(M, taken).
    Return max stones first player can get.
    """
    n = len(piles)

    # Precompute suffix sums
    suffix_sum = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_sum[i] = suffix_sum[i + 1] + piles[i]

    @lru_cache(maxsize=None)
    def dp(start: int, M: int) -> int:
        if start >= n:
            return 0

        if start + 2 * M >= n:
            return suffix_sum[start]

        max_stones = 0
        for take in range(1, 2 * M + 1):
            if start + take > n:
                break
            opponent_best = dp(start + take, max(M, take))
            stones = suffix_sum[start] - opponent_best
            max_stones = max(max_stones, stones)

        return max_stones

    return dp(0, 1)
```

### Template 5: Bottom-Up Space Optimized

```python
def linear_game_optimized(values: list[int], max_take: int = 3) -> int:
    """
    Same as linear_game but O(max_take) space.
    """
    n = len(values)
    dp = [0] * (max_take + 1)  # Rolling array

    for i in range(n - 1, -1, -1):
        best = float('-inf')
        total = 0

        for take in range(1, max_take + 1):
            if i + take > n:
                break
            total += values[i + take - 1]
            value = total - dp[(i + take) % (max_take + 1)]
            best = max(best, value)

        dp[i % (max_take + 1)] = best

    return dp[0]
```

## Template Selection Guide

| Scenario | Template |
|----------|----------|
| Take from either end | Template 1 (Interval) |
| Take fixed amount from front | Template 2 (Linear) |
| Select from pool, no reuse | Template 3 (Bitmask) |
| Variable take amount | Template 4 (M Parameter) |
| Need space optimization | Template 5 (Bottom-Up) |

## Variant: Stone Game II (LeetCode 1140)

> **Problem**: Alice and Bob play with piles. On each turn, if current M value is M, player can take 1 to 2*M piles from the start. M updates to max(M, X) where X is piles taken. Return max stones Alice can get.
> **Invariant**: Track (start_index, M) state; each player maximizes their stones.
> **Delta from Base**: Variable number of piles per turn, M parameter grows.

### Key Insight

State: `(start_index, M)` - position in array and current M value.

At each turn:
- Can take X piles where 1 ≤ X ≤ 2*M
- Next player's M = max(M, X)
- Use suffix sums for efficient total calculation

### Implementation

```python
class Solution:
    def stoneGameII(self, piles: list[int]) -> int:
        """
        Return maximum stones Alice can get.

        dp(start, M) = max stones current player can get from piles[start:]
                       with current M value.

        Use suffix sums: current_player_gets = suffix_sum[start] - opponent_gets
        """
        n = len(piles)

        # Compute suffix sums
        suffix_sum = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix_sum[i] = suffix_sum[i + 1] + piles[i]

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(start: int, M: int) -> int:
            if start >= n:
                return 0

            # If we can take all remaining, do it
            if start + 2 * M >= n:
                return suffix_sum[start]

            max_stones = 0
            for take in range(1, 2 * M + 1):
                if start + take > n:
                    break

                # Stones we get = total remaining - opponent's best
                opponent_best = dp(start + take, max(M, take))
                stones = suffix_sum[start] - opponent_best
                max_stones = max(max_stones, stones)

            return max_stones

        return dp(0, 1)
```

### Alternative: Track Score Directly

```python
class SolutionDirect:
    def stoneGameII(self, piles: list[int]) -> int:
        """Direct tracking of stones taken."""
        n = len(piles)
        suffix_sum = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix_sum[i] = suffix_sum[i + 1] + piles[i]

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(start: int, M: int) -> int:
            """Return max stones current player gets."""
            if start >= n:
                return 0

            if start + 2 * M >= n:
                return suffix_sum[start]

            best = 0
            stones_taken = 0
            for take in range(1, 2 * M + 1):
                if start + take > n:
                    break
                stones_taken += piles[start + take - 1]

                # I get stones_taken now
                # Plus whatever remains after opponent takes their best
                remaining_after_me = suffix_sum[start + take]
                opponent_gets = dp(start + take, max(M, take))
                my_total = stones_taken + (remaining_after_me - opponent_gets)
                best = max(best, my_total)

            return best

        return dp(0, 1)
```

### Trace Example

```
piles = [2, 7, 9, 4, 4]
suffix_sum = [26, 24, 17, 8, 4, 0]

dp(0, 1):  # Alice, M=1, can take 1-2 piles
  Take 1 (pile[0]=2):
    opponent_best = dp(1, 1)
      Take 1: dp(2, 1) → ...
      Take 2: dp(3, 2) → ...
    my_stones = 26 - opponent_best

  Take 2 (piles[0:2]=2+7=9):
    opponent_best = dp(2, 2)
    my_stones = 26 - opponent_best

Continue recursively...
```

### Key Insights

1. **Suffix Sum Trick**: Computing "my stones" = suffix_sum[start] - opponent's stones.
2. **M Growth**: M only increases (max(M, take)), limiting state space.
3. **Greedy Doesn't Work**: Taking maximum piles isn't always optimal.

### Complexity

- Time: O(n³) worst case - n² states, O(n) transitions per state
- Space: O(n²) for memoization

The M parameter is bounded by n, so states are O(n * n) = O(n²).

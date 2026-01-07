## Base Template: Stone Game (LeetCode 877)

> **Problem**: Alice and Bob play with piles of stones (even number). Each turn, a player takes an entire pile from either end. The player with more stones wins. Alice goes first.
> **Invariant**: At each turn, current player maximizes their score advantage.
> **Key insight**: With even number of piles, Alice can always win (mathematical proof), but DP solution is more instructive.

### Mathematical Solution (O(1))

With an even number of piles, Alice can always guarantee a win:
- Color piles alternately: odd-indexed vs even-indexed
- One color will have more total stones
- Alice can always take all of one color by controlling which end to pick

```python
class SolutionMath:
    def stoneGame(self, piles: list[int]) -> bool:
        """Alice always wins with even number of piles."""
        return True
```

### DP Solution (Educational)

```python
class SolutionDP:
    def stoneGame(self, piles: list[int]) -> bool:
        """
        Track score difference from current player's perspective.

        dp(i, j) = max score difference current player can achieve
                   when piles[i..j] remain.

        At each state:
        - Take left: gain piles[i], opponent gets dp(i+1, j)
        - Take right: gain piles[j], opponent gets dp(i, j-1)

        Since opponent's gain is our loss:
        - take_left = piles[i] - dp(i+1, j)
        - take_right = piles[j] - dp(i, j-1)
        """
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(left: int, right: int) -> int:
            if left > right:
                return 0

            take_left = piles[left] - dp(left + 1, right)
            take_right = piles[right] - dp(left, right - 1)

            return max(take_left, take_right)

        # Alice wins if her score difference >= 0
        return dp(0, len(piles) - 1) > 0
```

### Trace Example

```
piles = [5, 3, 4, 5]

dp(0, 3): Alice's turn
  - Take left (5): 5 - dp(1, 3)
    dp(1, 3): Bob's turn
      - Take left (3): 3 - dp(2, 3)
        dp(2, 3): Alice's turn
          - Take left (4): 4 - dp(3, 3) = 4 - 5 = -1
          - Take right (5): 5 - dp(2, 2) = 5 - 4 = 1
          → dp(2, 3) = max(-1, 1) = 1
      - Take right (5): 5 - dp(1, 2)
        dp(1, 2): Alice's turn
          - Take left (3): 3 - dp(2, 2) = 3 - 4 = -1
          - Take right (4): 4 - dp(1, 1) = 4 - 3 = 1
          → dp(1, 2) = max(-1, 1) = 1
    → dp(1, 3) = max(3 - 1, 5 - 1) = max(2, 4) = 4
  - Take right (5): 5 - dp(0, 2) = ...

Final: dp(0, 3) = 1 > 0, Alice wins
```

### Key Insights

1. **Perspective Switching**: The subtraction `- dp(...)` accounts for opponent playing optimally.
2. **Interval DP Structure**: State is (left, right) interval of remaining piles.
3. **Positive = Win**: Score difference > 0 means current player (Alice) wins.

### Complexity

- Time: O(n²) - each (i, j) pair computed once
- Space: O(n²) - memoization table

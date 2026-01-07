## Variant: Can I Win (LeetCode 464)

> **Problem**: Players take turns choosing integers 1 to maxChoosableInteger. Each number can only be used once. First to reach/exceed desiredTotal wins. Determine if the first player can force a win.
> **Invariant**: At each state, current player wins if ANY move leads to opponent losing.
> **Delta from Base**: Bitmask state encoding instead of interval; track running total.

### Key Insight

Use bitmask to track which numbers have been used:
- State = (used_mask, remaining_to_reach)
- Current player wins if any unused number either:
  1. Immediately reaches/exceeds target, OR
  2. Leads to a state where opponent loses

### Implementation

```python
class Solution:
    def canIWin(self, maxChoosableInteger: int, desiredTotal: int) -> bool:
        """
        Return True if first player can force a win.

        State: (bitmask of used numbers, remaining to reach)
        """
        # Edge case: if sum of all choices can't reach target, no one wins
        total_sum = maxChoosableInteger * (maxChoosableInteger + 1) // 2
        if total_sum < desiredTotal:
            return False

        # Edge case: if target is 0 or less, first player wins immediately
        if desiredTotal <= 0:
            return True

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def can_win(mask: int, remaining: int) -> bool:
            """Return True if current player can force a win."""
            for choice in range(1, maxChoosableInteger + 1):
                bit = 1 << choice

                if mask & bit:
                    continue  # Already used

                # Win immediately if choice >= remaining
                if choice >= remaining:
                    return True

                # Win if this choice makes opponent lose
                new_mask = mask | bit
                if not can_win(new_mask, remaining - choice):
                    return True

            # No winning move found
            return False

        return can_win(0, desiredTotal)
```

### Trace Example

```
maxChoosableInteger = 4, desiredTotal = 6

can_win(0b00000, 6):  # P1's turn, need 6
  Try 1: can_win(0b00010, 5)?
    Try 2: can_win(0b00110, 3)?
      Try 3: 3 >= 3, win! → can_win(0b00110, 3) = True
    P2 can win by picking 3, so can_win(0b00010, 5) = True
  P1 picking 1 doesn't guarantee win...

  Try 2: can_win(0b00100, 4)?
    Try 1: can_win(0b00110, 3)?
      Try 3: 3 >= 3, win! → True
    P2 wins...

  Try 3: can_win(0b01000, 3)?
    Try 1: can_win(0b01010, 2)?
      Try 2: 2 >= 2, win! → True
    P2 wins...

  Try 4: 4 < 6, can_win(0b10000, 2)?
    Try 1: can_win(0b10010, 1)?
      Try 2: 2 >= 1, win! → True
    P2 wins...

P1 cannot force a win → return False
```

### Optimization: Only Store Mask

Since remaining = desiredTotal - sum(used_numbers), we can derive remaining from mask:

```python
class SolutionOptimized:
    def canIWin(self, maxChoosableInteger: int, desiredTotal: int) -> bool:
        total_sum = maxChoosableInteger * (maxChoosableInteger + 1) // 2
        if total_sum < desiredTotal:
            return False
        if desiredTotal <= 0:
            return True

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def can_win(mask: int) -> bool:
            # Calculate remaining from mask
            used_sum = sum(i for i in range(1, maxChoosableInteger + 1)
                          if mask & (1 << i))
            remaining = desiredTotal - used_sum

            for choice in range(1, maxChoosableInteger + 1):
                if mask & (1 << choice):
                    continue

                if choice >= remaining:
                    return True

                if not can_win(mask | (1 << choice)):
                    return True

            return False

        return can_win(0)
```

### Key Insights

1. **Bitmask State**: Perfect for "use each item once" games with small n (≤20).
2. **Win Condition**: Current player wins if ANY move leads to opponent losing.
3. **Early Check**: If total sum < target, return False immediately.

### Complexity

- Time: O(2^n * n) where n = maxChoosableInteger
- Space: O(2^n) for memoization

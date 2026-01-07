# Game Theory DP Patterns: Complete Reference

> **API Kernel**: `GameTheoryDP`
> **Core Mechanism**: Minimax DP for two-player games with optimal play assumption.

## Pattern Overview

Game Theory DP solves two-player competitive games where:
1. Both players play optimally
2. Players alternate turns
3. Outcome determined by final score/state

The key insight: **At each state, the current player maximizes their advantage, knowing the opponent will do the same.**

## Core Algorithms

### Minimax Principle

```
At state S:
- Current player chooses action that maximizes their outcome
- This assumes opponent will minimize our outcome on their turn
- Recurse until base case (no moves left)

Mathematical formulation:
- value(state) = max over all actions (immediate_gain - value(next_state))
- The subtraction accounts for perspective switch (opponent's gain is our loss)
```

### Standard Recurrence Patterns

**Pattern 1: Score Difference Tracking**
```python
def can_win(state):
    """Track score difference from current player's perspective."""
    if base_case:
        return 0

    # Current player tries all moves, picks best
    best = -infinity
    for action in available_actions(state):
        # Score gained minus what opponent will achieve
        value = gain(action) - can_win(next_state(state, action))
        best = max(best, value)

    return best

# Winner check: can_win(initial_state) >= 0 for current player
```

**Pattern 2: Win/Lose State Tracking**
```python
def current_player_wins(state, memo):
    """Return True if current player can force a win."""
    if state in memo:
        return memo[state]

    if base_case:
        return base_result

    # Current player wins if ANY move leads to opponent losing
    for action in available_actions(state):
        opponent_wins = current_player_wins(next_state, memo)
        if not opponent_wins:
            memo[state] = True
            return True

    memo[state] = False
    return False
```

**Pattern 3: Interval Game (Taking from Ends)**
```python
def interval_game(piles, i, j, memo):
    """Game where players take from either end."""
    if i > j:
        return 0
    if (i, j) in memo:
        return memo[(i, j)]

    # Take left or right, opponent gets best of remaining
    take_left = piles[i] - interval_game(piles, i+1, j, memo)
    take_right = piles[j] - interval_game(piles, i, j-1, memo)

    memo[(i, j)] = max(take_left, take_right)
    return memo[(i, j)]
```

## Key Insights

1. **Perspective Switching**: When we recurse, we're computing from opponent's view. Their gain is our loss, hence the subtraction.

2. **Optimal Play Assumption**: Both players play perfectly - neither makes mistakes. This simplifies analysis.

3. **State Encoding**:
   - For interval games: `(left_index, right_index)`
   - For bitmask games: `integer` representing used elements
   - For pile games: `(remaining_amount)`

4. **Memoization Is Critical**: Game trees are exponential; without memoization, timeout guaranteed.

## Complexity Analysis

| Game Type | Time | Space |
|-----------|------|-------|
| Interval (n elements) | O(n²) | O(n²) |
| Bitmask (n choices) | O(2^n) | O(2^n) |
| Single pile (sum S) | O(S) | O(S) |

## Template Code

### Score Difference (Interval Game)

```python
from functools import lru_cache

def score_difference_game(piles: list[int]) -> int:
    """
    Return score difference if both players play optimally.
    Positive = first player wins, Negative = second player wins.
    """
    @lru_cache(maxsize=None)
    def dp(left: int, right: int) -> int:
        if left > right:
            return 0

        # Try taking from left or right
        take_left = piles[left] - dp(left + 1, right)
        take_right = piles[right] - dp(left, right - 1)

        return max(take_left, take_right)

    return dp(0, len(piles) - 1)
```

### Bitmask Game State

```python
from functools import lru_cache

def bitmask_game(max_choice: int, target: int) -> bool:
    """
    Can current player force a win given choices 1 to max_choice?
    """
    @lru_cache(maxsize=None)
    def can_win(mask: int, remaining: int) -> bool:
        for choice in range(1, max_choice + 1):
            if mask & (1 << choice):
                continue  # Already used

            if choice >= remaining:
                return True  # Win immediately

            new_mask = mask | (1 << choice)
            if not can_win(new_mask, remaining - choice):
                return True  # Opponent loses after this move

        return False  # No winning move

    return can_win(0, target)
```

### Multi-Choice Per Turn

```python
from functools import lru_cache

def multi_choice_game(piles: list[int]) -> str:
    """
    Each turn: take 1, 2, or 3 from the front.
    Return winner: "Alice" or "Bob" or "Tie".
    """
    n = len(piles)

    # Compute suffix sums
    suffix_sum = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_sum[i] = suffix_sum[i + 1] + piles[i]

    @lru_cache(maxsize=None)
    def dp(start: int) -> int:
        """Return score difference from current player's view."""
        if start >= n:
            return 0

        best = float('-inf')
        current_sum = 0
        for take in range(1, 4):
            if start + take - 1 >= n:
                break
            current_sum += piles[start + take - 1]
            # Score gained minus opponent's best outcome
            value = current_sum - dp(start + take)
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

## Common Patterns

1. **Even Piles Always Wins**: LC 877 - mathematical proof that first player always wins with even piles.

2. **Square Numbers**: LC 1140 - track whether current state is losing (all moves lead to opponent winning).

3. **Bitmask + Target Sum**: LC 464 - use bitmask to track used numbers, memoize on (mask, remaining).

4. **Multi-Element Take**: LC 1406 - take 1-3 elements per turn, track suffix sums for efficiency.

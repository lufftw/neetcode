# Game Theory DP - Intuition Guide

## The Mental Model: Think Like Your Opponent

Imagine playing chess:
- You don't just think about your next move
- You think: "If I do this, what will my opponent do? And then what's my best response?"

**Game Theory DP formalizes this recursive reasoning.**

## The Core Insight: Minimax

At any game state, the current player faces a choice:

```
I want to MAXIMIZE my outcome
But I know my opponent will MINIMIZE my outcome on their turn
So I must choose the move that gives me the best result
ASSUMING my opponent plays perfectly
```

This is the **minimax principle**: maximize your minimum guaranteed outcome.

## Why "Score Difference" Works

Consider a game where we track score difference from the current player's perspective:

```
If I'm ahead by 5 points, that's +5 for me
When my opponent plays, THEIR +3 becomes MY -3
So the scores naturally flip with each turn

dp(state) = my_gain - dp(next_state)
                      ↑
                      This is opponent's score difference
                      (positive for them = negative for me)
```

The subtraction handles the perspective switch automatically!

## Pattern 1: Taking from Ends (Stone Game)

**Scenario**: Array of values, take from either end each turn.

```
piles = [3, 9, 1, 2]

My turn: I can take 3 (left) or 2 (right)
If I take 3:
  - I gain 3
  - Opponent faces [9, 1, 2]
  - My total outcome = 3 - (opponent's best from [9, 1, 2])

Key insight: dp[i][j] = max score DIFFERENCE for current player
             when piles[i..j] remain
```

**Why this works**:
- State is interval [i, j] of remaining piles
- Each move shrinks interval by 1
- Eventually interval is empty (base case)

## Pattern 2: Taking from Front (Stone Game III)

**Scenario**: Array of values, take 1-3 from front each turn.

```
values = [1, 2, 3, -9]

My turn: I can take 1, 12, or 123
If I take first 2 (gaining 3):
  - Opponent faces [3, -9]
  - My outcome = 3 - dp([3, -9])

Key insight: dp[start] = max score diff starting from index start
```

**Why the -9 matters**:
- Naive: "Take as much as possible!"
- Smart: Taking -9 might help if it forces opponent into worse position
- Negative values make strategy non-trivial

## Pattern 3: Bitmask Games (Can I Win)

**Scenario**: Pool of numbers 1 to n, each used once, first to reach target wins.

```
Numbers: {1, 2, 3, 4}, Target: 6

If I pick 4:
  - Remaining: {1, 2, 3}, Need: 2
  - Opponent can pick 2 or 3 to win!

If I pick 3:
  - Remaining: {1, 2, 4}, Need: 3
  - Opponent picks any, I might recover...
```

**Why bitmask**:
- State = which numbers are still available
- With n numbers, 2^n possible states
- Memoize on the bitmask integer

## The "I Win If Opponent Loses" Pattern

For win/lose games (not score games):

```python
def can_win(state):
    for move in all_moves:
        if not can_win(state_after_move):
            return True  # This move makes opponent lose!
    return False  # All moves let opponent win :(
```

**Insight**: I need just ONE move that leads to opponent losing.
Opponent needs ALL my moves to lead to them winning.

## Trace Through: Predict the Winner

```
nums = [1, 5, 2]

Build up from base cases:
dp[0][0] = 1 (only pile 0, I take it)
dp[1][1] = 5 (only pile 1, I take it)
dp[2][2] = 2 (only pile 2, I take it)

dp[0][1]: piles 0 and 1 remain
  Take left (1): 1 - dp[1][1] = 1 - 5 = -4
  Take right (5): 5 - dp[0][0] = 5 - 1 = 4
  → dp[0][1] = max(-4, 4) = 4 (take the 5!)

dp[1][2]: piles 1 and 2 remain
  Take left (5): 5 - dp[2][2] = 5 - 2 = 3
  Take right (2): 2 - dp[1][1] = 2 - 5 = -3
  → dp[1][2] = max(3, -3) = 3 (take the 5!)

dp[0][2]: all piles remain (THIS IS THE ANSWER)
  Take left (1): 1 - dp[1][2] = 1 - 3 = -2
  Take right (2): 2 - dp[0][1] = 2 - 4 = -2
  → dp[0][2] = max(-2, -2) = -2

Player 1's advantage = -2 < 0 → Player 2 wins!
```

## Common Pitfalls

1. **Forgetting perspective flip**: The subtraction `- dp(next)` is crucial!

2. **Wrong win condition**:
   - `> 0` for strict win
   - `>= 0` when tie counts as win

3. **Not handling edge cases**:
   - Empty array
   - Single element
   - All elements same

4. **Inefficient state**:
   - Using (left, right, whose_turn) when (left, right) suffices
   - The turn is implicit in the recursion

## Complexity Guide

| Game Type | States | Per-State Work | Total |
|-----------|--------|----------------|-------|
| Interval [i,j] | O(n²) | O(1) | O(n²) |
| Linear (start) | O(n) | O(k) | O(nk) |
| Bitmask | O(2^n) | O(n) | O(n·2^n) |
| (start, M) | O(n·n) | O(n) | O(n³) |

## The Universal Game Theory DP Template

```python
from functools import lru_cache

def game_theory_dp(initial_state):
    """
    Template for two-player optimal games.

    Returns: outcome for first player
             (positive = win, negative = loss, 0 = tie)
    """
    @lru_cache(maxsize=None)
    def dp(state):
        if is_terminal(state):
            return terminal_value(state)

        best = float('-inf')
        for action in possible_actions(state):
            gain = immediate_gain(state, action)
            next_state = apply_action(state, action)

            # Key: subtract opponent's best outcome
            value = gain - dp(next_state)
            best = max(best, value)

        return best

    return dp(initial_state)
```

Fill in:
- `is_terminal`: game over?
- `terminal_value`: score when game ends
- `possible_actions`: what moves can I make?
- `immediate_gain`: points I get from this move
- `apply_action`: new state after move

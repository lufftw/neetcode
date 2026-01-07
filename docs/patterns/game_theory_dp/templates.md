# Game Theory DP Patterns: Complete Reference

> **API Kernel**: `GameTheoryDP`
> **Core Mechanism**: Minimax DP for two-player games with optimal play assumption.

## Table of Contents

1. [Pattern Overview](#1-pattern-overview)
2. [Core Algorithms](#2-core-algorithms)
3. [Key Insights](#3-key-insights)
4. [Complexity Analysis](#4-complexity-analysis)
5. [Template Code](#5-template-code)
6. [Common Patterns](#6-common-patterns)
7. [Base Template: Stone Game (LeetCode 877)](#7-base-template-stone-game-leetcode-877)
8. [Variant: Predict the Winner (LeetCode 486)](#8-variant-predict-the-winner-leetcode-486)
9. [Variant: Can I Win (LeetCode 464)](#9-variant-can-i-win-leetcode-464)
10. [Variant: Stone Game II (LeetCode 1140)](#10-variant-stone-game-ii-leetcode-1140)
11. [Variant: Stone Game III (LeetCode 1406)](#11-variant-stone-game-iii-leetcode-1406)
12. [Algorithm Comparison](#12-algorithm-comparison)
13. [Pattern Selection Guide](#13-pattern-selection-guide)
14. [Key Technique Comparison](#14-key-technique-comparison)
15. [Score Tracking Methods](#15-score-tracking-methods)
16. [Decision Flowchart](#16-decision-flowchart)
17. [Quick Selection Table](#17-quick-selection-table)
18. [Ready-to-Use Templates](#18-ready-to-use-templates)
19. [Template Selection Guide](#19-template-selection-guide)

---

## 1. Pattern Overview

Game Theory DP solves two-player competitive games where:
1. Both players play optimally
2. Players alternate turns
3. Outcome determined by final score/state

The key insight: **At each state, the current player maximizes their advantage, knowing the opponent will do the same.**

## 2. Core Algorithms

### 2.1 Minimax Principle

```
At state S:
- Current player chooses action that maximizes their outcome
- This assumes opponent will minimize our outcome on their turn
- Recurse until base case (no moves left)

Mathematical formulation:
- value(state) = max over all actions (immediate_gain - value(next_state))
- The subtraction accounts for perspective switch (opponent's gain is our loss)
```

### 2.2 Standard Recurrence Patterns

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

## 3. Key Insights

1. **Perspective Switching**: When we recurse, we're computing from opponent's view. Their gain is our loss, hence the subtraction.

2. **Optimal Play Assumption**: Both players play perfectly - neither makes mistakes. This simplifies analysis.

3. **State Encoding**:
   - For interval games: `(left_index, right_index)`
   - For bitmask games: `integer` representing used elements
   - For pile games: `(remaining_amount)`

4. **Memoization Is Critical**: Game trees are exponential; without memoization, timeout guaranteed.

## 4. Complexity Analysis

| Game Type | Time | Space |
|-----------|------|-------|
| Interval (n elements) | O(n²) | O(n²) |
| Bitmask (n choices) | O(2^n) | O(2^n) |
| Single pile (sum S) | O(S) | O(S) |

## 5. Template Code

### 5.1 Score Difference (Interval Game)

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

### 5.2 Bitmask Game State

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

### 5.3 Multi-Choice Per Turn

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

## 6. Common Patterns

1. **Even Piles Always Wins**: LC 877 - mathematical proof that first player always wins with even piles.

2. **Square Numbers**: LC 1140 - track whether current state is losing (all moves lead to opponent winning).

3. **Bitmask + Target Sum**: LC 464 - use bitmask to track used numbers, memoize on (mask, remaining).

4. **Multi-Element Take**: LC 1406 - take 1-3 elements per turn, track suffix sums for efficiency.

---

## 7. Base Template: Stone Game (LeetCode 877)

> **Problem**: Alice and Bob play with piles of stones (even number). Each turn, a player takes an entire pile from either end. The player with more stones wins. Alice goes first.
> **Invariant**: At each turn, current player maximizes their score advantage.
> **Key insight**: With even number of piles, Alice can always win (mathematical proof), but DP solution is more instructive.

### 7.1 Mathematical Solution (O(1))

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

### 7.2 DP Solution (Educational)

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

### 7.3 Trace Example

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

### 7.4 Key Insights

1. **Perspective Switching**: The subtraction `- dp(...)` accounts for opponent playing optimally.
2. **Interval DP Structure**: State is (left, right) interval of remaining piles.
3. **Positive = Win**: Score difference > 0 means current player (Alice) wins.

### 7.5 Complexity

- Time: O(n²) - each (i, j) pair computed once
- Space: O(n²) - memoization table

---

## 8. Variant: Predict the Winner (LeetCode 486)

> **Problem**: Two players take turns selecting numbers from either end of array. Predict if Player 1 can win or tie (not strictly less than Player 2).
> **Invariant**: Track score difference from current player's perspective.
> **Delta from Base**: Handle tie case (>=0 instead of >0), odd number of elements allowed.

### 8.1 Key Insight

This is almost identical to Stone Game (LC 877), but:
1. Works with any number of elements (not just even)
2. Tie counts as Player 1 winning (>= 0 instead of > 0)
3. Player 1 wins if `dp(0, n-1) >= 0`

### 8.2 Implementation

```python
class Solution:
    def predictTheWinner(self, nums: list[int]) -> bool:
        """
        Return True if Player 1 can win or tie.

        dp(i, j) = max score difference current player can achieve
                   from nums[i..j].

        Player 1 wins if dp(0, n-1) >= 0.
        """
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(left: int, right: int) -> int:
            if left > right:
                return 0

            take_left = nums[left] - dp(left + 1, right)
            take_right = nums[right] - dp(left, right - 1)

            return max(take_left, take_right)

        return dp(0, len(nums) - 1) >= 0
```

### 8.3 Bottom-Up Alternative

```python
class SolutionBottomUp:
    def predictTheWinner(self, nums: list[int]) -> bool:
        """
        Bottom-up DP with O(n) space optimization.

        dp[j] represents score difference for interval ending at j.
        """
        n = len(nums)
        dp = nums[:]  # Base case: single element intervals

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                # dp[j] currently holds dp[i+1][j] from previous iteration
                take_left = nums[i] - dp[j]
                # After this update, dp[j-1] holds dp[i][j-1]
                take_right = nums[j] - dp[j - 1]
                dp[j] = max(take_left, take_right)

        return dp[n - 1] >= 0
```

### 8.4 Trace Example

```
nums = [1, 5, 2]

Base cases:
dp(0, 0) = 1, dp(1, 1) = 5, dp(2, 2) = 2

dp(0, 1):
  - Take 1: 1 - dp(1, 1) = 1 - 5 = -4
  - Take 5: 5 - dp(0, 0) = 5 - 1 = 4
  → dp(0, 1) = 4

dp(1, 2):
  - Take 5: 5 - dp(2, 2) = 5 - 2 = 3
  - Take 2: 2 - dp(1, 1) = 2 - 5 = -3
  → dp(1, 2) = 3

dp(0, 2):
  - Take 1: 1 - dp(1, 2) = 1 - 3 = -2
  - Take 2: 2 - dp(0, 1) = 2 - 4 = -2
  → dp(0, 2) = -2

Player 1 score diff = -2 < 0, so Player 1 loses.
```

### 8.5 Comparison with Stone Game

| Aspect | Stone Game (877) | Predict Winner (486) |
|--------|------------------|----------------------|
| Elements | Even only | Any number |
| Win condition | diff > 0 | diff >= 0 |
| Tie handling | N/A | Counts as P1 win |
| Math solution | Yes (always True) | No (need DP) |

### 8.6 Complexity

- Time: O(n²) with memoization
- Space: O(n²) with memoization, O(n) with bottom-up optimization

---

## 9. Variant: Can I Win (LeetCode 464)

> **Problem**: Players take turns choosing integers 1 to maxChoosableInteger. Each number can only be used once. First to reach/exceed desiredTotal wins. Determine if the first player can force a win.
> **Invariant**: At each state, current player wins if ANY move leads to opponent losing.
> **Delta from Base**: Bitmask state encoding instead of interval; track running total.

### 9.1 Key Insight

Use bitmask to track which numbers have been used:
- State = (used_mask, remaining_to_reach)
- Current player wins if any unused number either:
  1. Immediately reaches/exceeds target, OR
  2. Leads to a state where opponent loses

### 9.2 Implementation

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

### 9.3 Trace Example

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

### 9.4 Optimization: Only Store Mask

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

### 9.5 Key Insights

1. **Bitmask State**: Perfect for "use each item once" games with small n (≤20).
2. **Win Condition**: Current player wins if ANY move leads to opponent losing.
3. **Early Check**: If total sum < target, return False immediately.

### 9.6 Complexity

- Time: O(2^n * n) where n = maxChoosableInteger
- Space: O(2^n) for memoization

---

## 10. Variant: Stone Game II (LeetCode 1140)

> **Problem**: Alice and Bob play with piles. On each turn, if current M value is M, player can take 1 to 2*M piles from the start. M updates to max(M, X) where X is piles taken. Return max stones Alice can get.
> **Invariant**: Track (start_index, M) state; each player maximizes their stones.
> **Delta from Base**: Variable number of piles per turn, M parameter grows.

### 10.1 Key Insight

State: `(start_index, M)` - position in array and current M value.

At each turn:
- Can take X piles where 1 ≤ X ≤ 2*M
- Next player's M = max(M, X)
- Use suffix sums for efficient total calculation

### 10.2 Implementation

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

### 10.3 Alternative: Track Score Directly

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

### 10.4 Trace Example

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

### 10.5 Key Insights

1. **Suffix Sum Trick**: Computing "my stones" = suffix_sum[start] - opponent's stones.
2. **M Growth**: M only increases (max(M, take)), limiting state space.
3. **Greedy Doesn't Work**: Taking maximum piles isn't always optimal.

### 10.6 Complexity

- Time: O(n³) worst case - n² states, O(n) transitions per state
- Space: O(n²) for memoization

The M parameter is bounded by n, so states are O(n * n) = O(n²).

---

## 11. Variant: Stone Game III (LeetCode 1406)

> **Problem**: Alice and Bob play with stone values (can be negative). Each turn, player takes 1, 2, or 3 stones from the front. Return "Alice", "Bob", or "Tie".
> **Invariant**: Track score difference from current player's perspective.
> **Delta from Base**: Fixed 1-3 choices per turn, negative values allowed, taken from front only.

### 11.1 Key Insight

Similar to interval games but:
1. Always take from the front (start index only)
2. Fixed choices: 1, 2, or 3 stones
3. Negative values make strategy non-trivial

### 11.2 Implementation

```python
class Solution:
    def stoneGameIII(self, stoneValue: list[int]) -> str:
        """
        Return winner: "Alice", "Bob", or "Tie".

        dp(start) = max score difference current player can achieve
                    starting from index start.
        """
        n = len(stoneValue)

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(start: int) -> int:
            if start >= n:
                return 0

            best = float('-inf')
            stones_taken = 0

            for take in range(1, 4):
                if start + take > n:
                    break

                stones_taken += stoneValue[start + take - 1]

                # Score gained minus opponent's best outcome
                value = stones_taken - dp(start + take)
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

### 11.3 Bottom-Up with Space Optimization

```python
class SolutionBottomUp:
    def stoneGameIII(self, stoneValue: list[int]) -> str:
        """
        Bottom-up DP with O(1) space using rolling array.

        Only need dp[i+1], dp[i+2], dp[i+3] to compute dp[i].
        """
        n = len(stoneValue)

        # dp[i] = best score difference from position i
        # Only need last 3 values
        dp = [0] * 4  # dp[i % 4]

        for i in range(n - 1, -1, -1):
            best = float('-inf')
            stones = 0

            for take in range(1, 4):
                if i + take > n:
                    break
                stones += stoneValue[i + take - 1]
                value = stones - dp[(i + take) % 4]
                best = max(best, value)

            dp[i % 4] = best

        diff = dp[0]

        if diff > 0:
            return "Alice"
        elif diff < 0:
            return "Bob"
        else:
            return "Tie"
```

### 11.4 Trace Example

```
stoneValue = [1, 2, 3, 7]

dp(3): only take 1 stone (7)
  → 7 - dp(4) = 7 - 0 = 7

dp(2): can take 1, 2, or 3 stones
  Take 1: 3 - dp(3) = 3 - 7 = -4
  Take 2: 3+7 - dp(4) = 10 - 0 = 10
  → dp(2) = max(-4, 10) = 10

dp(1): can take 1, 2, or 3
  Take 1: 2 - dp(2) = 2 - 10 = -8
  Take 2: 2+3 - dp(3) = 5 - 7 = -2
  Take 3: 2+3+7 - dp(4) = 12 - 0 = 12
  → dp(1) = max(-8, -2, 12) = 12

dp(0): can take 1, 2, or 3
  Take 1: 1 - dp(1) = 1 - 12 = -11
  Take 2: 1+2 - dp(2) = 3 - 10 = -7
  Take 3: 1+2+3 - dp(3) = 6 - 7 = -1
  → dp(0) = max(-11, -7, -1) = -1

diff = -1 < 0 → "Bob" wins
```

### 11.5 Key Insights

1. **Negative Values Matter**: Can't just take maximum - might set up opponent.
2. **Fixed Choices**: Unlike Stone Game II, always 1-3 choices.
3. **Space Optimization**: Rolling array since only need 3 previous values.

### 11.6 Comparison Table

| Game | Choices | Direction | Values |
|------|---------|-----------|--------|
| 877 | 1 (ends) | Either end | Positive |
| 486 | 1 (ends) | Either end | Any |
| 1140 | 1 to 2M | Front | Positive |
| 1406 | 1, 2, 3 | Front | Any |

### 11.7 Complexity

- Time: O(n) with memoization
- Space: O(n) with memoization, O(1) with rolling array

---

## 12. Algorithm Comparison

| Aspect | Stone Game (877) | Predict Winner (486) | Can I Win (464) | Stone Game II (1140) | Stone Game III (1406) |
|--------|------------------|----------------------|-----------------|----------------------|----------------------|
| State | (i, j) interval | (i, j) interval | bitmask | (start, M) | start index |
| Choices | Left or right | Left or right | Any unused | 1 to 2*M | 1, 2, or 3 |
| Values | Positive | Any | Fixed 1..n | Positive | Any |
| Win Condition | diff > 0 | diff >= 0 | reach target | max stones | diff comparison |
| Time | O(n²) | O(n²) | O(2^n * n) | O(n³) | O(n) |
| Space | O(n²) | O(n²) | O(2^n) | O(n²) | O(1) optimized |

## 13. Pattern Selection Guide

```
Two-player game?
├── Taking from array ends?
│   ├── Even elements only → Stone Game (877) - always True
│   └── Any elements → Predict Winner (486)
├── Taking from array front?
│   ├── Variable amount based on M → Stone Game II (1140)
│   └── Fixed 1,2,3 choices → Stone Game III (1406)
└── Selecting from pool (no reuse)?
    └── Can I Win (464) - bitmask DP
```

## 14. Key Technique Comparison

| Technique | When to Use |
|-----------|-------------|
| Interval DP (i, j) | Taking from either end |
| Linear DP (start) | Taking from one end only |
| Bitmask DP | Selecting items without reuse |
| Math solution | Special structure (even piles) |

## 15. Score Tracking Methods

1. **Score Difference**: `dp = my_gain - dp(next_state)`
   - Used in: 877, 486, 1406
   - Positive = current player wins

2. **Direct Score**: `my_score = suffix_sum - opponent_score`
   - Used in: 1140
   - Track actual stones, not difference

3. **Win/Lose Boolean**: `can_win = any move leads to opponent losing`
   - Used in: 464
   - True = current player can force win

---

## 16. Decision Flowchart

```
START: Two-player optimal game
│
├── What are players choosing from?
│   │
│   ├── Array elements from ENDS
│   │   │
│   │   ├── Even length array?
│   │   │   └── Stone Game (877) - return True
│   │   │
│   │   └── Any length array?
│   │       └── Predict Winner (486)
│   │           ├── State: (left, right) interval
│   │           └── diff >= 0 means P1 wins
│   │
│   ├── Array elements from FRONT
│   │   │
│   │   ├── Variable choices (1 to 2*M)?
│   │   │   └── Stone Game II (1140)
│   │   │       ├── State: (start, M)
│   │   │       └── Use suffix sums
│   │   │
│   │   └── Fixed choices (1, 2, or 3)?
│   │       └── Stone Game III (1406)
│   │           ├── State: start index only
│   │           └── O(1) space possible
│   │
│   └── Pool of items (no reuse)?
│       └── Can I Win (464)
│           ├── State: bitmask of used items
│           └── Win if reach target first
│
└── How to track outcome?
    │
    ├── Score difference (most common)
    │   └── dp = gain - dp(next_state)
    │
    ├── Win/Lose boolean
    │   └── can_win = any(not opponent_can_win)
    │
    └── Direct score with suffix sum
        └── my_score = suffix[start] - opponent_score
```

## 17. Quick Selection Table

| Clue in Problem | Pattern |
|-----------------|---------|
| "take from either end" | Interval DP (877, 486) |
| "take 1-3 from front" | Linear DP (1406) |
| "take 1 to 2M" | State (start, M) (1140) |
| "each number once" | Bitmask DP (464) |
| "even number of piles" | Math: always True (877) |
| "reach target first" | Win/Lose tracking (464) |
| "maximize score" | Score difference DP |

---

## 18. Ready-to-Use Templates

### 18.1 Template 1: Interval Game (Take from Ends)

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

### 18.2 Template 2: Linear Game (Take from Front)

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

### 18.3 Template 3: Bitmask Game (Use Once)

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

### 18.4 Template 4: Variable Take with M Parameter

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

### 18.5 Template 5: Bottom-Up Space Optimized

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

## 19. Template Selection Guide

| Scenario | Template |
|----------|----------|
| Take from either end | Template 1 (Interval) |
| Take fixed amount from front | Template 2 (Linear) |
| Select from pool, no reuse | Template 3 (Bitmask) |
| Variable take amount | Template 4 (M Parameter) |
| Need space optimization | Template 5 (Bottom-Up) |



---



*Document generated for NeetCode Practice Framework — API Kernel: GameTheoryDP*

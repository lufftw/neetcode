"""
LeetCode 518: Coin Change 2
https://leetcode.com/problems/coin-change-ii/

Pattern: DP Knapsack/Subset - Unbounded Knapsack Count Combinations
API Kernel: DPKnapsackSubset

You are given an integer array coins representing coins of different denominations
and an integer amount representing a total amount of money.

Return the number of combinations that make up that amount. If that amount of money
cannot be made up by any combination of the coins, return 0.

You may assume that you have an infinite number of each kind of coin.
"""

import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDP",
        "method": "change",
        "complexity": "O(n * amount) time, O(amount) space",
        "description": "Unbounded knapsack count combinations (coins outer loop)",
    },
    "dp_unbounded": {
        "class": "SolutionDP",
        "method": "change",
        "complexity": "O(n * amount) time, O(amount) space",
        "description": "Space-optimized unbounded knapsack (coins outer loop)",
    },
    "memoization": {
        "class": "SolutionMemoization",
        "method": "change",
        "complexity": "O(n * amount) time, O(n * amount) space",
        "description": "Top-down recursive with memoization",
    },
}


def _reference_change(amount: int, coins: List[int]) -> int:
    """Reference implementation for validation."""
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]

    return dp[amount]


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    lines = input_data.strip().split("\n")
    amount = json.loads(lines[0])
    coins = json.loads(lines[1])
    correct = _reference_change(amount, coins)
    try:
        actual_val = int(actual) if isinstance(actual, str) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionDP:
    """
    Unbounded Knapsack - Count combinations.

    dp[a] = number of combinations to make amount a
    dp[a] += dp[a - coin]

    Key insights:
    1. Forward iteration for unbounded property
    2. Coins outer loop gives combinations (order doesn't matter)
       (Amount outer would give permutations)
    """

    def change(self, amount: int, coins: List[int]) -> int:
        """
        Count number of combinations to make up the amount.

        Core insight: Unbounded knapsack counting combinations. Coins as outer loop
        ensures each combination is counted once (not permutations). Forward inner
        loop allows unlimited coin reuse.

        Invariant: After processing coin c, dp[a] counts combinations using only
        coins processed so far to make amount a.

        Args:
            amount: Target amount
            coins: Available coin denominations

        Returns:
            Number of distinct combinations
        """
        dp = [0] * (amount + 1)
        dp[0] = 1

        # Coins outer loop: count combinations (not permutations)
        for coin in coins:
            # Forwards for unbounded property
            for a in range(coin, amount + 1):
                dp[a] += dp[a - coin]

        return dp[amount]


class SolutionMemoization:
    """
    Top-down recursive with memoization.

    Key insight: To count combinations (not permutations), we must track
    which coins we've "decided on" - hence (coin_index, remaining_amount).
    """

    def change(self, amount: int, coins: List[int]) -> int:
        """
        Count combinations using top-down memoization.

        Core insight: dp(coin_index, remaining) counts combinations using
        coins[coin_index:] to make remaining amount. For each coin, we can
        use it 0, 1, 2, ... times (unbounded), but we must process coins
        in order to avoid counting permutations.

        Args:
            amount: Target amount
            coins: Available coin denominations

        Returns:
            Number of distinct combinations
        """
        memo = {}

        def dp(coin_idx: int, remaining: int) -> int:
            """Count combinations using coins[coin_idx:] to make remaining."""
            if remaining == 0:
                return 1
            if remaining < 0 or coin_idx >= len(coins):
                return 0

            if (coin_idx, remaining) in memo:
                return memo[(coin_idx, remaining)]

            # Option 1: Use current coin at least once, stay at same coin_idx
            # Option 2: Skip to next coin
            use_coin = dp(coin_idx, remaining - coins[coin_idx])
            skip_coin = dp(coin_idx + 1, remaining)

            result = use_coin + skip_coin
            memo[(coin_idx, remaining)] = result
            return result

        return dp(0, amount)


def solve():
    lines = sys.stdin.read().strip().split("\n")

    amount = json.loads(lines[0])
    coins = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.change(amount, coins)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

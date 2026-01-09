"""
LeetCode 322: Coin Change
https://leetcode.com/problems/coin-change/

Pattern: DP Knapsack/Subset - Unbounded Knapsack Minimum
API Kernel: DPKnapsackSubset

You are given an integer array coins representing coins of different denominations
and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount.
If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.
"""

import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDP",
        "method": "coinChange",
        "complexity": "O(n * amount) time, O(amount) space",
        "description": "Unbounded knapsack with forward iteration for minimum count",
    },
}


def _reference_coin_change(coins: List[int], amount: int) -> int:
    """Reference implementation for validation."""
    if amount == 0:
        return 0

    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float("inf") else -1


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    lines = input_data.strip().split("\n")
    coins = json.loads(lines[0])
    amount = json.loads(lines[1])
    correct = _reference_coin_change(coins, amount)
    try:
        actual_val = int(actual) if isinstance(actual, str) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionDP:
    """
    Unbounded Knapsack - Minimum coins.

    dp[a] = minimum coins to make amount a
    dp[a] = min(dp[a], dp[a - coin] + 1)

    Key insight: Iterate forwards because coins can be reused (unbounded).
    """

    def coinChange(self, coins: List[int], amount: int) -> int:
        """
        Find minimum coins needed to make up the amount.

        Core insight: Unbounded knapsack for minimum count. dp[a] = min coins for
        amount a. For each coin, dp[a] = min(dp[a], dp[a-coin] + 1). Forward
        iteration allows reusing same coin multiple times.

        Invariant: After processing coin c, dp[a] is minimum coins using coins
        processed so far to make amount a.

        Args:
            coins: Available coin denominations
            amount: Target amount

        Returns:
            Minimum coins needed, or -1 if impossible
        """
        if amount == 0:
            return 0

        dp = [float("inf")] * (amount + 1)
        dp[0] = 0

        for coin in coins:
            # Forwards for unbounded property (coins can be reused)
            for a in range(coin, amount + 1):
                dp[a] = min(dp[a], dp[a - coin] + 1)

        return dp[amount] if dp[amount] != float("inf") else -1


def solve():
    lines = sys.stdin.read().strip().split("\n")

    coins = json.loads(lines[0])
    amount = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.coinChange(coins, amount)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

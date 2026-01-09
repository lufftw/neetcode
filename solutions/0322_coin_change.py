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
    "dp_bottom_up": {
        "class": "SolutionDP",
        "method": "coinChange",
        "complexity": "O(n * amount) time, O(amount) space",
        "description": "Canonical bottom-up DP, iterate by coin then amount",
    },
    "memoization": {
        "class": "SolutionMemoization",
        "method": "coinChange",
        "complexity": "O(n * amount) time, O(amount) space",
        "description": "Top-down DP with memoization, recursive approach",
    },
    "bfs": {
        "class": "SolutionBFS",
        "method": "coinChange",
        "complexity": "O(n * amount) time, O(amount) space",
        "description": "BFS level-order traversal, finds shortest path (fewest coins)",
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


class SolutionMemoization:
    """
    Top-down DP with memoization.

    Recursive approach: minCoins(amount) = min(minCoins(amount - coin) + 1) for all coins.

    Key insight: Same subproblems as bottom-up, but starts from target and works down.
    More intuitive for some; matches the problem's recursive structure directly.
    """

    def coinChange(self, coins: List[int], amount: int) -> int:
        """
        Find minimum coins using top-down memoization.

        Core insight: Define subproblem as "minimum coins to make amount a".
        For each amount, try all coins and take minimum. Memoize to avoid
        recomputation of overlapping subproblems.

        Args:
            coins: Available coin denominations
            amount: Target amount

        Returns:
            Minimum coins needed, or -1 if impossible
        """
        if amount == 0:
            return 0

        memo = {}

        def dp(remaining: int) -> int:
            if remaining == 0:
                return 0
            if remaining < 0:
                return float("inf")
            if remaining in memo:
                return memo[remaining]

            result = float("inf")
            for coin in coins:
                result = min(result, dp(remaining - coin) + 1)

            memo[remaining] = result
            return result

        ans = dp(amount)
        return ans if ans != float("inf") else -1


class SolutionBFS:
    """
    BFS level-order traversal for minimum coins.

    Model as graph: each amount is a node, edges connect amount to (amount - coin).
    BFS finds shortest path from 'amount' to 0.

    Key insight: BFS guarantees first time we reach 0, we've used minimum coins.
    Each level represents one coin added.
    """

    def coinChange(self, coins: List[int], amount: int) -> int:
        """
        Find minimum coins using BFS shortest path.

        Core insight: Model as unweighted graph where each node is an amount,
        and edges represent subtracting a coin. BFS level = number of coins used.
        First path to reach 0 is optimal.

        Args:
            coins: Available coin denominations
            amount: Target amount

        Returns:
            Minimum coins needed, or -1 if impossible
        """
        if amount == 0:
            return 0

        from collections import deque

        visited = set([amount])
        queue = deque([amount])
        level = 0

        while queue:
            level += 1
            for _ in range(len(queue)):
                curr = queue.popleft()
                for coin in coins:
                    next_amount = curr - coin
                    if next_amount == 0:
                        return level
                    if next_amount > 0 and next_amount not in visited:
                        visited.add(next_amount)
                        queue.append(next_amount)

        return -1


def solve():
    lines = sys.stdin.read().strip().split("\n")

    coins = json.loads(lines[0])
    amount = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.coinChange(coins, amount)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

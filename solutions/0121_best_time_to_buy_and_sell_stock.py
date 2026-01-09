"""
LeetCode 121: Best Time to Buy and Sell Stock
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

Pattern: DP 1D Linear - Running Min/Max (Kadane-Style)
API Kernel: DP1DLinear

You are given an array prices where prices[i] is the price of a given stock on the ith day.
You want to maximize your profit by choosing a single day to buy one stock and choosing a
different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
"""

import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDP",
        "method": "maxProfit",
        "complexity": "O(n) time, O(1) space",
        "description": "Track running minimum price and maximum profit",
    },
    "running_min": {
        "class": "SolutionDP",
        "method": "maxProfit",
        "complexity": "O(n) time, O(1) space",
        "description": "Optimal: track running min price (Kadane-style)",
    },
    "bruteforce": {
        "class": "SolutionBruteforce",
        "method": "maxProfit",
        "complexity": "O(n²) time, O(1) space",
        "description": "Baseline: check all buy-sell pairs",
    },
}


def _reference_max_profit(prices: List[int]) -> int:
    """Reference implementation for validation."""
    if not prices or len(prices) < 2:
        return 0

    min_price = float("inf")
    max_profit = 0

    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)

    return max_profit


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    prices = json.loads(input_data.strip())
    correct = _reference_max_profit(prices)
    try:
        actual_val = int(actual) if isinstance(actual, str) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionDP:
    """
    Track running minimum price and maximum profit.

    For each day, we compute:
    - min_price = minimum price seen so far (best buying opportunity)
    - max_profit = max(max_profit, current_price - min_price)

    This is equivalent to Kadane's algorithm applied to the difference array.
    """

    def maxProfit(self, prices: List[int]) -> int:
        if not prices or len(prices) < 2:
            return 0

        min_price = float("inf")
        max_profit = 0

        for price in prices:
            min_price = min(min_price, price)
            max_profit = max(max_profit, price - min_price)

        return max_profit


class SolutionBruteforce:
    """
    Brute force: check all (buy, sell) pairs.

    O(n²) baseline to show why tracking running minimum is important.
    """

    def maxProfit(self, prices: List[int]) -> int:
        """
        Find maximum profit by checking all buy-sell pairs.

        Core insight: For each possible buy day i, check all sell days j > i.
        This is the naive approach that shows O(n²) → O(n) optimization.

        Time: O(n²) - nested loops
        Space: O(1)

        Args:
            prices: Stock prices by day

        Returns:
            Maximum possible profit (0 if no profit possible)
        """
        if not prices or len(prices) < 2:
            return 0

        max_profit = 0
        n = len(prices)

        for i in range(n):  # Buy day
            for j in range(i + 1, n):  # Sell day
                profit = prices[j] - prices[i]
                max_profit = max(max_profit, profit)

        return max_profit


def solve():
    lines = sys.stdin.read().strip().split("\n")

    prices = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.maxProfit(prices)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

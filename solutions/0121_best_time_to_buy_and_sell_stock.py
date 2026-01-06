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


def solve():
    lines = sys.stdin.read().strip().split("\n")

    prices = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.maxProfit(prices)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

"""
Problem: Sell Diminishing-Valued Colored Balls
Link: https://leetcode.com/problems/sell-diminishing-valued-colored-balls/

Maximize total value selling `orders` balls where ball value = current count.

Constraints:
- 1 <= inventory.length <= 10^5
- 1 <= inventory[i] <= 10^9
- 1 <= orders <= min(sum(inventory[i]), 10^9)

Topics: Array, Math, Binary Search, Greedy, Sorting, Heap
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "maxProfit",
        "complexity": "O(n log M) time, O(1) space",
        "description": "Binary search for threshold, arithmetic sum for profit",
    },
}


MOD = 10 ** 9 + 7


# JUDGE_FUNC for generated tests
def _reference(inventory: List[int], orders: int) -> int:
    """Reference implementation."""
    lo, hi = 0, max(inventory)
    while lo < hi:
        mid = (lo + hi) // 2
        count = sum(max(0, inv - mid) for inv in inventory)
        if count <= orders:
            hi = mid
        else:
            lo = mid + 1
    threshold = lo
    total = 0
    remaining = orders
    for inv in inventory:
        if inv > threshold:
            count = inv - threshold
            total += (inv + threshold + 1) * count // 2
            total %= MOD
            remaining -= count
    total += remaining * threshold
    return total % MOD


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    inventory = json.loads(lines[0])
    orders = int(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(inventory, orders)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Binary Search for Threshold
# Time: O(n log M), Space: O(1)
# ============================================================================
class Solution:
    # Key insight: Always sell highest-value balls first.
    # If we sell down to threshold t, we take sum(max(0, inv[i] - t)) balls.
    #
    # Binary search for t such that this sum ~= orders.
    # Then compute total value using arithmetic series.
    #
    # Sum from a down to b+1 = (a+b+1)(a-b)/2

    def maxProfit(self, inventory: List[int], orders: int) -> int:
        # Binary search for threshold t
        # count(t) = number of balls with value > t
        # Find SMALLEST t such that count(t) <= orders
        lo, hi = 0, max(inventory)

        while lo < hi:
            mid = (lo + hi) // 2  # Lower mid for finding smallest valid
            # Count balls with value > mid
            count = sum(max(0, inv - mid) for inv in inventory)
            if count <= orders:
                # Valid, try lower threshold (sell more)
                hi = mid
            else:
                # Too many balls, need higher threshold
                lo = mid + 1

        # Threshold found: sell all balls with value > threshold
        threshold = lo

        # Calculate profit
        total = 0
        remaining = orders

        for inv in inventory:
            if inv > threshold:
                # Sell from inv down to threshold+1
                count = inv - threshold
                # Sum = inv + (inv-1) + ... + (threshold+1)
                # = (inv + threshold + 1) * count / 2
                total += (inv + threshold + 1) * count // 2
                total %= MOD
                remaining -= count

        # Sell remaining at threshold value (remaining balls at exactly threshold)
        total += remaining * threshold
        total %= MOD

        return total


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: inventory (JSON array)
        Line 2: orders (integer)

    Example:
        [2,5]
        4
        -> 14
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    inventory = json.loads(lines[0])
    orders = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.maxProfit(inventory, orders)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

"""
Problem: Online Stock Span
Link: https://leetcode.com/problems/online-stock-span/

Design an algorithm that collects daily price quotes for some stock and returns the span of that stock's price for the current day.
The span of the stock's price in one day is the maximum number of consecutive days (starting from that day and going backward) for which the stock price was less than or equal to the price of that day.

Example 1:

Constraints:
- 1 <= price <= 10^5
- At most 10^4 calls will be made to next.

Topics: Stack, Design, Monotonic Stack, Data Stream
"""

import json

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "StockSpanner",
        "method": "next",
        "complexity": "O(1) amortized per call, O(n) space",
        "description": "Monotonic decreasing stack with span accumulation",
    },
}


# ============================================================================
# Solution 1: Monotonic Decreasing Stack with Span Accumulation
# Time: O(1) amortized per call, Space: O(n) total
#   - Stack stores (price, accumulated_span) pairs
#   - When new price dominates stack top, pop and absorb its span
#   - Each element pushed once, popped at most once -> amortized O(1)
#
# Key Insight: Span = 1 (current day) + sum of spans of all dominated days.
# When we pop a dominated element, its entire span transfers to current day.
# This is "Previous Greater Element" but we track span instead of index.
# ============================================================================
class StockSpanner:
    def __init__(self) -> None:
        # Stack of (price, span) tuples
        # Maintains decreasing price order for efficient span computation
        self.price_span_stack: list[tuple[int, int]] = []

    def next(self, price: int) -> int:
        current_span = 1  # Current day always counts

        # Absorb spans of all days with price <= current price
        while self.price_span_stack and self.price_span_stack[-1][0] <= price:
            _, dominated_span = self.price_span_stack.pop()
            current_span += dominated_span

        # Push current day with its accumulated span
        self.price_span_stack.append((price, current_span))

        return current_span


def solve():
    """
    Input format (LeetCode-style method calls):
        Line 1: JSON array of method names, e.g., ["StockSpanner","next","next"]
        Line 2: JSON array of argument lists, e.g., [[],[100],[80]]

    Output format:
        JSON array of return values, e.g., [null,1,1]
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    methods = json.loads(lines[0])
    arguments = json.loads(lines[1])

    results: list = []
    spanner: StockSpanner | None = None

    for method_name, args in zip(methods, arguments):
        if method_name == "StockSpanner":
            spanner = StockSpanner()
            results.append(None)
        elif method_name == "next":
            assert spanner is not None
            result = spanner.next(args[0])
            results.append(result)

    print(json.dumps(results))


if __name__ == "__main__":
    solve()

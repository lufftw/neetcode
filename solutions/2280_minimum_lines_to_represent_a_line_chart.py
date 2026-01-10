"""
Problem: Minimum Lines to Represent a Line Chart
Link: https://leetcode.com/problems/minimum-lines-to-represent-a-line-chart/

Count minimum line segments to represent stock price chart.
Each segment connects consecutive sorted points with same slope.

Constraints:
- 1 <= stockPrices.length <= 10^5
- 1 <= day_i, price_i <= 10^9
- All day_i distinct

Topics: Array, Math, Geometry, Sorting
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minimumLines",
        "complexity": "O(n log n) time, O(1) space",
        "description": "Sort by day, count slope changes using cross-multiplication",
    },
}


# JUDGE_FUNC for generated tests
def _reference(stockPrices: List[List[int]]) -> int:
    """Reference implementation."""
    n = len(stockPrices)
    if n == 1:
        return 0

    points = sorted(stockPrices)
    lines = 1

    for i in range(2, n):
        # Compare slopes: (y2-y1)/(x2-x1) vs (y1-y0)/(x1-x0)
        # Cross multiply to avoid floating point
        x0, y0 = points[i - 2]
        x1, y1 = points[i - 1]
        x2, y2 = points[i]

        dy1 = y1 - y0
        dx1 = x1 - x0
        dy2 = y2 - y1
        dx2 = x2 - x1

        # Different slope if dy1 * dx2 != dy2 * dx1
        if dy1 * dx2 != dy2 * dx1:
            lines += 1

    return lines


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    stockPrices = json.loads(lines[0])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(stockPrices)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Sort and Count Slope Changes
# Time: O(n log n), Space: O(1)
# ============================================================================
class Solution:
    # Key insight:
    #   - Sort points by day (x-coordinate)
    #   - A new line segment starts when slope changes
    #   - Compare slopes using cross-multiplication to avoid floating point:
    #     (y2-y1)/(x2-x1) == (y3-y2)/(x3-x2)
    #     ↔ (y2-y1)*(x3-x2) == (y3-y2)*(x2-x1)
    #
    # Edge case: Single point needs 0 lines

    def minimumLines(self, stockPrices: List[List[int]]) -> int:
        n = len(stockPrices)
        if n == 1:
            return 0

        # Sort by day
        stockPrices.sort()

        # Count line segments (starts at 1 for first two points)
        lines = 1

        for i in range(2, n):
            # Previous segment: points[i-2] to points[i-1]
            # Current segment: points[i-1] to points[i]
            x0, y0 = stockPrices[i - 2]
            x1, y1 = stockPrices[i - 1]
            x2, y2 = stockPrices[i]

            # Compare slopes via cross-multiplication
            dy_prev = y1 - y0
            dx_prev = x1 - x0
            dy_curr = y2 - y1
            dx_curr = x2 - x1

            # Slope changed if dy_prev/dx_prev != dy_curr/dx_curr
            if dy_prev * dx_curr != dy_curr * dx_prev:
                lines += 1

        return lines


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: stockPrices (JSON 2D array)

    Example:
        [[1,7],[2,6],[3,5],[4,4],[5,4],[6,3],[7,2],[8,1]]
        -> 3
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    stockPrices = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minimumLines(stockPrices)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

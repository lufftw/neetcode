"""
Problem: Max Points on a Line
Link: https://leetcode.com/problems/max-points-on-a-line/

Find maximum number of points on the same straight line.

Constraints:
- 1 <= points.length <= 300
- points[i].length == 2
- -10^4 <= xi, yi <= 10^4
- All points are unique

Topics: Array, Hash Table, Math, Geometry
"""
from typing import List
from _runner import get_solver
import json
from math import gcd
from collections import defaultdict


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "maxPoints",
        "complexity": "O(n^2) time, O(n) space",
        "description": "For each anchor point, count slopes using reduced fractions",
    },
}


# JUDGE_FUNC for generated tests
def _reference(points: List[List[int]]) -> int:
    """Reference implementation."""
    n = len(points)
    if n <= 2:
        return n
    result = 1
    for i in range(n):
        slopes = defaultdict(int)
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            dx, dy = x2 - x1, y2 - y1
            g = gcd(dx, dy)
            dx, dy = dx // g, dy // g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            slopes[(dx, dy)] += 1
        if slopes:
            result = max(result, max(slopes.values()) + 1)
    return result


def judge(actual, expected, input_data: str) -> bool:
    points = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(points)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Slope Counting with GCD Normalization
# Time: O(n^2), Space: O(n)
# ============================================================================
class Solution:
    # Key insight: Points on same line share same slope with any anchor point.
    #
    # For each point p, calculate slope to all other points.
    # Represent slope as reduced fraction (dx, dy) to avoid float precision.
    # Use GCD to normalize: (dx/g, dy/g) with consistent sign.
    #
    # Edge cases:
    # - Vertical lines: dx=0, represent as (0, 1)
    # - Horizontal lines: dy=0, represent as (1, 0)

    def maxPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 2:
            return n

        result = 1

        for i in range(n):
            slopes = defaultdict(int)
            x1, y1 = points[i]

            for j in range(i + 1, n):
                x2, y2 = points[j]
                dx = x2 - x1
                dy = y2 - y1

                # Normalize using GCD
                g = gcd(dx, dy)
                dx //= g
                dy //= g

                # Ensure consistent sign: make dx positive, or if dx=0, make dy positive
                if dx < 0 or (dx == 0 and dy < 0):
                    dx = -dx
                    dy = -dy

                slopes[(dx, dy)] += 1

            # Maximum points through point i = max slope count + 1 (for point i itself)
            if slopes:
                result = max(result, max(slopes.values()) + 1)

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: points (JSON 2D array)

    Example:
        [[1,1],[2,2],[3,3]]
        -> 3
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    points = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.maxPoints(points)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

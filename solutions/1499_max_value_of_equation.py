"""
Problem: Max Value of Equation
Link: https://leetcode.com/problems/max-value-of-equation/

You are given an array points containing the coordinates of points on a 2D
plane, sorted by x-values, where points[i] = [xi, yi]. You are also given
an integer k.

Return the maximum value of the equation yi + yj + |xi - xj| where
|xi - xj| <= k and 1 <= i < j <= points.length.

It is guaranteed that there exists at least one pair of points that
satisfies the constraint |xi - xj| <= k.

Example 1:
    Input: points = [[1,3],[2,0],[5,10],[6,-10]], k = 1
    Output: 4
    Explanation: The first two points satisfy |xi - xj| <= 1 and
    yi + yj + |xi - xj| = 3 + 0 + |1 - 2| = 4. Points [5,10] and [6,-10]
    also satisfy but yi + yj + |xi - xj| = 10 - 10 + 1 = 1.

Example 2:
    Input: points = [[0,0],[3,0],[9,2]], k = 3
    Output: 3
    Explanation: yi + yj + |xi - xj| = 0 + 0 + |0 - 3| = 3.

Constraints:
- 2 <= points.length <= 10^5
- points[i].length == 2
- -10^8 <= xi, yi <= 10^8
- 0 <= k <= 2 * 10^8
- xi < xj for all 1 <= i < j <= points.length
- xi form a strictly increasing sequence

Topics: Array, Queue, Sliding Window, Heap (Priority Queue), Monotonic Queue
"""

import json
from collections import deque
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionMonotonicDeque",
        "method": "findMaxValueOfEquation",
        "complexity": "O(n) time, O(n) space",
        "description": "Monotonic deque maximizing y-x with distance constraint",
    },
    "deque": {
        "class": "SolutionMonotonicDeque",
        "method": "findMaxValueOfEquation",
        "complexity": "O(n) time, O(n) space",
        "description": "Monotonic deque maximizing y-x with distance constraint",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual is the correct max equation value.

    Args:
        actual: Program output (int as string or int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (JSON array and k)

    Returns:
        bool: True if correct max value
    """
    lines = input_data.strip().split("\n")
    points = json.loads(lines[0]) if lines[0] else []
    k = int(lines[1])

    # Compute correct answer using reference solution
    correct = _reference_max_value(points, k)

    # Parse actual output
    if isinstance(actual, int):
        actual_val = actual
    else:
        actual_str = str(actual).strip()
        try:
            actual_val = int(actual_str)
        except ValueError:
            return False

    return actual_val == correct


def _reference_max_value(points: List[List[int]], k: int) -> int:
    """O(n) reference using monotonic deque."""
    dq: deque[tuple[int, int]] = deque()  # Store (x, y-x) with decreasing y-x
    result = float("-inf")

    for x, y in points:
        # Remove points outside window (xj - xi > k)
        while dq and x - dq[0][0] > k:
            dq.popleft()

        # Calculate answer if we have valid candidates
        if dq:
            result = max(result, y + x + dq[0][1])  # yj + xj + (yi - xi)

        # Maintain decreasing order of y-x
        while dq and dq[-1][1] <= y - x:
            dq.pop()

        dq.append((x, y - x))

    return result if result != float("-inf") else 0


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Monotonic Deque with Algebraic Transformation
# Time: O(n), Space: O(n)
#   - Transform equation: yi + yj + |xi - xj| = (yj + xj) + (yi - xi)
#   - For each point j, maximize (yi - xi) among valid i (where xj - xi <= k)
#   - This is sliding window maximum on transformed values
#
# Key Insight: Since points are sorted by x and i < j, |xi - xj| = xj - xi.
# Splitting the equation shows we want to maximize yi - xi in a window.
# ============================================================================
class SolutionMonotonicDeque:
    def findMaxValueOfEquation(self, points: List[List[int]], k: int) -> int:
        """
        Maximize yi + yj + |xi - xj| where |xi - xj| <= k and i < j.

        Core insight: Since points sorted by x and i < j, |xi - xj| = xj - xi.
        Rewrite as (yj + xj) + (yi - xi). For each j, maximize (yi - xi) among
        valid i. This is sliding window maximum on transformed values (y - x).

        Invariant: Deque contains (x, y-x) with decreasing y-x values; all points
        are within distance k of current point.

        Args:
            points: List of [x, y] coordinates sorted by x
            k: Maximum allowed x-distance between points

        Returns:
            Maximum value of the equation
        """
        # Deque stores (x, y-x) tuples with y-x in decreasing order
        candidates: deque[tuple[int, int]] = deque()
        max_value = float("-inf")

        for x, y in points:
            # 1. Remove points outside the window (xj - xi > k)
            while candidates and x - candidates[0][0] > k:
                candidates.popleft()

            # 2. Calculate answer using best candidate (if exists)
            #    Equation: yj + xj + (yi - xi) where front has max (yi - xi)
            if candidates:
                max_value = max(max_value, y + x + candidates[0][1])

            # 3. Maintain decreasing order of y-x
            #    Remove worse candidates from back
            while candidates and candidates[-1][1] <= y - x:
                candidates.pop()

            # 4. Add current point to candidates
            candidates.append((x, y - x))

        return max_value if max_value != float("-inf") else 0


def solve():
    """
    Input format (JSON):
        Line 1: points as JSON 2D array [[x1,y1], [x2,y2], ...]
        Line 2: k as integer

    Output format:
        Integer representing maximum equation value
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    points = json.loads(lines[0])
    k = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.findMaxValueOfEquation(points, k)

    print(result)


if __name__ == "__main__":
    solve()

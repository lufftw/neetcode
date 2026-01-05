# solutions/0452_minimum_number_of_arrows_to_burst_balloons.py
"""
Problem: Minimum Number of Arrows to Burst Balloons
Link: https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/

There are some spherical balloons taped onto a flat wall that represents the XY-plane. The balloons
are represented as a 2D integer array points where points[i] = [xstart, xend] denotes a balloon
whose horizontal diameter stretches between xstart and xend. You do not know the exact y-coordinates
of the balloons.

Arrows can be shot up directly vertically (in the positive y direction) from different points along
the x-axis. A balloon with xstart and xend is burst by an arrow shot at x if xstart <= x <= xend.
There is no limit to the number of arrows that can be shot. A shot arrow keeps traveling up
infinitely, bursting any balloons in its path.

Given the array points, return the minimum number of arrows that must be shot to burst all balloons.

Example 1:
    Input: points = [[10,16],[2,8],[1,6],[7,12]]
    Output: 2
    Explanation: The balloons can be burst by 2 arrows:
    - Shoot an arrow at x = 6, bursting the balloons [2,8] and [1,6].
    - Shoot an arrow at x = 11, bursting the balloons [10,16] and [7,12].

Example 2:
    Input: points = [[1,2],[3,4],[5,6],[7,8]]
    Output: 4
    Explanation: One arrow needs to be shot for each balloon for a total of 4 arrows.

Example 3:
    Input: points = [[1,2],[2,3],[3,4],[4,5]]
    Output: 2
    Explanation: The balloons can be burst by 2 arrows:
    - Shoot an arrow at x = 2, bursting the balloons [1,2] and [2,3].
    - Shoot an arrow at x = 4, bursting the balloons [3,4] and [4,5].

Constraints:
- 1 <= points.length <= 10^5
- points[i].length == 2
- -2^31 <= xstart < xend <= 2^31 - 1

Topics: Array, Greedy, Sorting
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Minimum Arrows solution."""
    import json

    # Parse input
    points = json.loads(input_data.strip())

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected
    expected_result = _find_min_arrows(points)
    return actual == expected_result


def _find_min_arrows(points):
    """Reference solution for validation."""
    if not points:
        return 0

    points.sort(key=lambda x: x[1])
    arrows = 1
    arrow_pos = points[0][1]

    for i in range(1, len(points)):
        if points[i][0] > arrow_pos:
            arrows += 1
            arrow_pos = points[i][1]

    return arrows


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "findMinArrowPoints",
        "complexity": "O(n log n) time, O(1) space",
        "description": "Sort by end, count overlapping groups",
        "api_kernels": ["IntervalScheduling"],
        "patterns": ["interval_scheduling"],
    },
}


# ============================================
# Solution 1: Greedy Group Counting
# Time: O(n log n), Space: O(1)
#   - Sort by end position
#   - Count number of overlapping groups
# ============================================
class Solution:
    def findMinArrowPoints(self, points: List[List[int]]) -> int:
        """
        Minimum arrows to burst all balloons.

        Key Insight:
        - Equivalent to counting non-overlapping groups
        - Sort by end, greedily extend groups
        - New arrow needed when balloon starts after current arrow position

        Why this works:
        - Arrow at x bursts all balloons where start <= x <= end
        - Greedy: shoot at rightmost safe position (end of first balloon)
        """
        if not points:
            return 0

        # Sort by end position
        points.sort(key=lambda x: x[1])

        arrows = 1
        arrow_pos = points[0][1]  # Shoot at end of first balloon

        for i in range(1, len(points)):
            # If balloon starts after current arrow position
            if points[i][0] > arrow_pos:
                arrows += 1
                arrow_pos = points[i][1]

        return arrows


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array points

    Output format:
    Integer: minimum arrows
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    points = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.findMinArrowPoints(points)

    print(result)


if __name__ == "__main__":
    solve()

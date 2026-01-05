# solutions/0986_interval_list_intersections.py
"""
Problem: Interval List Intersections
Link: https://leetcode.com/problems/interval-list-intersections/

You are given two lists of closed intervals, firstList and secondList, where
firstList[i] = [starti, endi] and secondList[j] = [startj, endj]. Each list of intervals is
pairwise disjoint and in sorted order.

Return the intersection of these two interval lists.

A closed interval [a, b] (with a <= b) denotes the set of real numbers x with a <= x <= b.

The intersection of two closed intervals is a set of real numbers that is either empty, or
represented as a closed interval. For example, the intersection of [1, 3] and [2, 4] is [2, 3].

Example 1:
    Input: firstList = [[0,2],[5,10],[13,23],[24,25]], secondList = [[1,5],[8,12],[15,24],[25,26]]
    Output: [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]

Example 2:
    Input: firstList = [[1,3],[5,9]], secondList = []
    Output: []

Constraints:
- 0 <= firstList.length, secondList.length <= 1000
- firstList.length + secondList.length >= 1
- 0 <= starti < endi <= 10^9
- 0 <= startj < endj <= 10^9

Topics: Array, Two Pointers
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Interval List Intersections solution."""
    import json

    # Parse input
    lines = input_data.strip().split('\n')
    firstList = json.loads(lines[0])
    secondList = json.loads(lines[1])

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected
    expected_result = _interval_intersection(firstList, secondList)
    return actual == expected_result


def _interval_intersection(firstList, secondList):
    """Reference solution for validation."""
    result = []
    i, j = 0, 0

    while i < len(firstList) and j < len(secondList):
        a_start, a_end = firstList[i]
        b_start, b_end = secondList[j]

        start = max(a_start, b_start)
        end = min(a_end, b_end)

        if start <= end:
            result.append([start, end])

        if a_end < b_end:
            i += 1
        else:
            j += 1

    return result


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "intervalIntersection",
        "complexity": "O(m + n) time, O(min(m,n)) space",
        "description": "Two-pointer merge for intersections",
        "api_kernels": ["IntervalMerge"],
        "patterns": ["interval_intersection"],
    },
}


# ============================================
# Solution 1: Two-Pointer Intersection
# Time: O(m + n), Space: O(min(m, n))
#   - Use two pointers like merge sort
#   - Compute intersection for each pair
# ============================================
class Solution:
    def intervalIntersection(
        self, firstList: List[List[int]], secondList: List[List[int]]
    ) -> List[List[int]]:
        """
        Find all intersections of two sorted interval lists.

        Key Insight:
        - Use two pointers (like merge sort)
        - Intersection exists if max(starts) <= min(ends)
        - Advance pointer with smaller end (exhausted earlier)

        Why advance smaller end?
        - Interval with smaller end can't intersect future intervals
        - The other interval might still intersect with next intervals
        """
        result: list[list[int]] = []
        i, j = 0, 0

        while i < len(firstList) and j < len(secondList):
            a_start, a_end = firstList[i]
            b_start, b_end = secondList[j]

            # Check for intersection
            start = max(a_start, b_start)
            end = min(a_end, b_end)

            if start <= end:
                result.append([start, end])

            # Advance pointer with smaller end
            if a_end < b_end:
                i += 1
            else:
                j += 1

        return result


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array firstList
    Line 2: 2D array secondList

    Output format:
    2D array of intersections
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    firstList = json.loads(lines[0])
    secondList = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.intervalIntersection(firstList, secondList)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

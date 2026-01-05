# solutions/0435_non_overlapping_intervals.py
"""
Problem: Non-overlapping Intervals
Link: https://leetcode.com/problems/non-overlapping-intervals/

Given an array of intervals intervals where intervals[i] = [starti, endi], return the minimum number
of intervals you need to remove to make the rest of the intervals non-overlapping.

Example 1:
    Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
    Output: 1
    Explanation: [1,3] can be removed and the rest of the intervals are non-overlapping.

Example 2:
    Input: intervals = [[1,2],[1,2],[1,2]]
    Output: 2
    Explanation: You need to remove two [1,2] to make the rest of the intervals non-overlapping.

Example 3:
    Input: intervals = [[1,2],[2,3]]
    Output: 0
    Explanation: You don't need to remove any of the intervals since they're already non-overlapping.

Constraints:
- 1 <= intervals.length <= 10^5
- intervals[i].length == 2
- -5 * 10^4 <= starti < endi <= 5 * 10^4

Topics: Array, Dynamic Programming, Greedy, Sorting
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Non-overlapping Intervals solution."""
    import json

    # Parse input
    intervals = json.loads(input_data.strip())

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected
    expected_result = _erase_overlap_intervals(intervals)
    return actual == expected_result


def _erase_overlap_intervals(intervals):
    """Reference solution for validation."""
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])
    non_overlapping = 1
    prev_end = intervals[0][1]

    for i in range(1, len(intervals)):
        if intervals[i][0] >= prev_end:
            non_overlapping += 1
            prev_end = intervals[i][1]

    return len(intervals) - non_overlapping


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "eraseOverlapIntervals",
        "complexity": "O(n log n) time, O(1) space",
        "description": "Sort by end, greedy selection",
        "api_kernels": ["IntervalScheduling"],
        "patterns": ["interval_scheduling"],
    },
}


# ============================================
# Solution 1: Greedy Scheduling
# Time: O(n log n), Space: O(1)
#   - Sort by end time
#   - Greedily keep non-overlapping intervals
# ============================================
class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        """
        Minimum intervals to remove for no overlaps.

        Key Insight:
        - Equivalent to: total - max non-overlapping intervals
        - Greedy: always keep interval that ends earliest
        - Sort by END time (not start!) for optimal selection

        Why sort by end?
        - Earlier ending = more room for future intervals
        - Greedy choice property: locally optimal → globally optimal
        """
        if not intervals:
            return 0

        # Sort by end time (critical for greedy!)
        intervals.sort(key=lambda x: x[1])

        # Greedy selection: count non-overlapping
        non_overlapping = 1
        prev_end = intervals[0][1]

        for i in range(1, len(intervals)):
            # If current starts at or after previous ends (no overlap)
            if intervals[i][0] >= prev_end:
                non_overlapping += 1
                prev_end = intervals[i][1]
            # Else: skip current (implicit removal)

        return len(intervals) - non_overlapping


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array intervals

    Output format:
    Integer: minimum removals
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    intervals = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.eraseOverlapIntervals(intervals)

    print(result)


if __name__ == "__main__":
    solve()

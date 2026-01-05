# solutions/0056_merge_intervals.py
"""
Problem: Merge Intervals
Link: https://leetcode.com/problems/merge-intervals/

Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping
intervals, and return an array of the non-overlapping intervals that cover all the
intervals in the input.

Example 1:
    Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
    Output: [[1,6],[8,10],[15,18]]
    Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Example 2:
    Input: intervals = [[1,4],[4,5]]
    Output: [[1,5]]
    Explanation: Intervals [1,4] and [4,5] are considered overlapping.

Constraints:
- 1 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= starti <= endi <= 10^4

Topics: Array, Sorting
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Merge Intervals solution."""
    import json

    # Parse input
    intervals = json.loads(input_data.strip())

    # If expected is available, compare directly
    if expected is not None:
        # Sort both for comparison (order doesn't matter)
        return sorted(actual) == sorted(expected)

    # Judge-only mode: compute expected using reference solution
    expected_result = _merge_intervals(intervals)
    return sorted(actual) == sorted(expected_result)


def _merge_intervals(intervals):
    """Reference solution for validation."""
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for curr in intervals[1:]:
        if curr[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], curr[1])
        else:
            merged.append(curr)

    return merged


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "merge",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Sort by start, merge adjacent overlaps",
        "api_kernels": ["IntervalMerge"],
        "patterns": ["interval_merge"],
    },
}


# ============================================
# Solution 1: Sort and Merge
# Time: O(n log n), Space: O(n)
#   - Sort by start time
#   - Merge overlapping intervals
# ============================================
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Merge overlapping intervals.

        Key Insight:
        - After sorting by start, overlapping intervals are adjacent
        - Maintain current interval, extend end if overlap, else add new
        - Overlap check: curr[0] <= prev_end (since sorted)
        """
        if not intervals:
            return []

        # Sort by start time
        intervals.sort(key=lambda x: x[0])

        merged: list[list[int]] = [intervals[0]]

        for interval in intervals[1:]:
            # If current overlaps with last merged
            if interval[0] <= merged[-1][1]:
                # Extend the end
                merged[-1][1] = max(merged[-1][1], interval[1])
            else:
                # No overlap, add new interval
                merged.append(interval)

        return merged


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array intervals

    Output format:
    2D array of merged intervals
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    intervals = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.merge(intervals)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

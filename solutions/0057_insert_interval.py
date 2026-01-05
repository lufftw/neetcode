# solutions/0057_insert_interval.py
"""
Problem: Insert Interval
Link: https://leetcode.com/problems/insert-interval/

You are given an array of non-overlapping intervals intervals where intervals[i] = [starti, endi]
represent the start and the end of the ith interval and intervals is sorted in ascending order by
starti. You are also given an interval newInterval = [start, end] that represents the start and end
of another interval.

Insert newInterval into intervals such that intervals is still sorted in ascending order by starti
and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).

Return intervals after the insertion.

Example 1:
    Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
    Output: [[1,5],[6,9]]

Example 2:
    Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
    Output: [[1,2],[3,10],[12,16]]
    Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].

Constraints:
- 0 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= starti <= endi <= 10^5
- intervals is sorted by starti in ascending order.
- newInterval.length == 2
- 0 <= start <= end <= 10^5

Topics: Array
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Insert Interval solution."""
    import json

    # Parse input
    lines = input_data.strip().split('\n')
    intervals = json.loads(lines[0])
    newInterval = json.loads(lines[1])

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected
    expected_result = _insert_interval(intervals, newInterval)
    return actual == expected_result


def _insert_interval(intervals, newInterval):
    """Reference solution for validation."""
    result = []
    i = 0
    n = len(intervals)

    # Phase 1: Before overlap
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1

    # Phase 2: Merge overlapping
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)

    # Phase 3: After overlap
    while i < n:
        result.append(intervals[i])
        i += 1

    return result


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "insert",
        "complexity": "O(n) time, O(n) space",
        "description": "Three-phase processing: before, merge, after",
        "api_kernels": ["IntervalMerge"],
        "patterns": ["interval_insert"],
    },
}


# ============================================
# Solution 1: Three-Phase Insert
# Time: O(n), Space: O(n)
#   - Phase 1: Add all before overlap
#   - Phase 2: Merge overlapping
#   - Phase 3: Add all after overlap
# ============================================
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        """
        Insert new interval into sorted non-overlapping list.

        Key Insight:
        - Already sorted, process in three phases
        - Phase 1: Add all intervals ending before newInterval starts
        - Phase 2: Merge all overlapping intervals
        - Phase 3: Add all intervals starting after newInterval ends
        """
        result: list[list[int]] = []
        i = 0
        n = len(intervals)

        # Phase 1: Add all intervals that end before newInterval starts
        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        # Phase 2: Merge overlapping intervals
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        result.append(newInterval)

        # Phase 3: Add remaining intervals
        while i < n:
            result.append(intervals[i])
            i += 1

        return result


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array intervals
    Line 2: Array newInterval

    Output format:
    2D array of merged intervals
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    intervals = json.loads(lines[0])
    newInterval = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.insert(intervals, newInterval)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

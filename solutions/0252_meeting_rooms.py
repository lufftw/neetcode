# solutions/0252_meeting_rooms.py
"""
Problem: Meeting Rooms
https://leetcode.com/problems/meeting-rooms/

Given an array of meeting time intervals [start, end], determine if
a person could attend all meetings.

Key insight: After sorting by start time, two meetings conflict if
the previous meeting's end time > next meeting's start time.

Constraints:
- 0 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= starti < endi <= 10^6
"""
import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionSorting",
        "method": "canAttendMeetings",
        "complexity": "O(n log n) time, O(1) space",
        "description": "Sort by start time, check consecutive overlaps",
    },
}


class SolutionSorting:
    """
    Sorting approach.

    WHY: To detect conflicts, we need to know when each meeting starts.
    Sorting brings potentially overlapping meetings adjacent. Then we
    only need to check if any meeting starts before the previous ends.

    HOW: Sort intervals by start time. For each consecutive pair,
    check if intervals[i][1] > intervals[i+1][0]. If so, there's a conflict.
    """

    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        if not intervals:
            return True

        # Sort by start time
        intervals.sort(key=lambda x: x[0])

        # Check for overlaps between consecutive meetings
        for i in range(1, len(intervals)):
            # Previous meeting ends after next meeting starts
            if intervals[i - 1][1] > intervals[i][0]:
                return False

        return True


def judge(actual, expected, input_data: str) -> bool:
    """Validate meeting rooms result."""
    if isinstance(actual, str):
        actual = json.loads(actual)

    # Compute expected from input
    intervals = json.loads(input_data.strip())
    expected_result = _can_attend_ref(intervals)

    return actual == expected_result


def _can_attend_ref(intervals: List[List[int]]) -> bool:
    """Reference implementation."""
    if not intervals:
        return True
    intervals_sorted = sorted(intervals, key=lambda x: x[0])
    for i in range(1, len(intervals_sorted)):
        if intervals_sorted[i - 1][1] > intervals_sorted[i][0]:
            return False
    return True


JUDGE_FUNC = judge


def solve():
    lines = sys.stdin.read().strip().split("\n")
    intervals = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.canAttendMeetings(intervals)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

# solutions/0253_meeting_rooms_ii.py
"""
Problem: Meeting Rooms II
Link: https://leetcode.com/problems/meeting-rooms-ii/

Given an array of meeting time intervals intervals where intervals[i] = [starti, endi],
return the minimum number of conference rooms required.

Example 1:
    Input: intervals = [[0,30],[5,10],[15,20]]
    Output: 2

Example 2:
    Input: intervals = [[7,10],[2,4]]
    Output: 1

Constraints:
- 1 <= intervals.length <= 10^4
- 0 <= starti < endi <= 10^6

Topics: Array, Two Pointers, Greedy, Sorting, Heap Priority Queue, Prefix Sum
"""

import json
from typing import List
import heapq

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionHeap",
        "method": "minMeetingRooms",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Min-heap of end times for greedy room assignment",
    },
    "heap": {
        "class": "SolutionHeap",
        "method": "minMeetingRooms",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Min-heap of end times for greedy room assignment",
    },
    "sweep": {
        "class": "SolutionSweepLine",
        "method": "minMeetingRooms",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Sweep line with event processing",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is correct minimum rooms.

    Args:
        actual: Program output (integer as string or int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (intervals as JSON)

    Returns:
        bool: True if correct minimum rooms
    """
    lines = input_data.strip().split("\n")
    intervals = json.loads(lines[0]) if lines[0] else []

    # Compute correct answer
    correct = _reference_min_rooms(intervals)

    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _reference_min_rooms(intervals: List[List[int]]) -> int:
    """Reference implementation using sweep line."""
    if not intervals:
        return 0

    events = []
    for start, end in intervals:
        events.append((start, 1))   # Meeting starts
        events.append((end, -1))    # Meeting ends

    # Sort by time; if same time, process ends before starts
    events.sort(key=lambda x: (x[0], x[1]))

    max_rooms = 0
    current_rooms = 0

    for time, delta in events:
        current_rooms += delta
        max_rooms = max(max_rooms, current_rooms)

    return max_rooms


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Min-Heap of End Times
# Time: O(n log n), Space: O(n)
#
# Pattern: heap_interval_scheduling
# See: docs/patterns/heap/templates.md Section 5 (Meeting Rooms)
# ============================================================================
class SolutionHeap:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Find minimum meeting rooms using min-heap of end times.

        Key Insight:
        - Sort meetings by start time (process chronologically)
        - Min-heap tracks when each room becomes free (end times)
        - For each meeting:
          - If starts after earliest end → reuse that room
          - Otherwise → allocate new room

        Why min-heap of end times?
        - We need the room that frees up earliest
        - If meeting starts >= earliest end, room can be reused
        - Pop old end time, push new end time
        - Heap size = number of rooms in use
        """
        if not intervals:
            return 0

        # Sort by start time
        intervals.sort(key=lambda x: x[0])

        # Min-heap of end times (when rooms become free)
        end_times: list[int] = []

        for start, end in intervals:
            # Check if earliest-ending room is now free
            if end_times and end_times[0] <= start:
                # Room is free, reuse it (pop old end, push new end)
                heapq.heapreplace(end_times, end)
            else:
                # All rooms busy or no rooms yet, allocate new room
                heapq.heappush(end_times, end)

        # Number of rooms = size of heap
        return len(end_times)


# ============================================================================
# Solution 2: Sweep Line
# Time: O(n log n), Space: O(n)
#
# Pattern: sweep_line
# See: docs/patterns/heap/templates.md Section 5 (Meeting Rooms)
# ============================================================================
class SolutionSweepLine:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Sweep line approach: track events at each time point.

        Events:
        - +1 at start time (meeting begins, need room)
        - -1 at end time (meeting ends, room freed)

        Key Insight:
        - Maximum concurrent meetings = maximum rooms needed
        - Process events in time order
        - If same time: process ends (-1) before starts (+1)
          (room frees up before new meeting uses it)
        """
        events: list[tuple[int, int]] = []
        for start, end in intervals:
            events.append((start, 1))   # Meeting starts
            events.append((end, -1))    # Meeting ends

        # Sort by time; if same time, ends (-1) before starts (+1)
        events.sort(key=lambda x: (x[0], x[1]))

        max_rooms = 0
        current_rooms = 0

        for time, delta in events:
            current_rooms += delta
            max_rooms = max(max_rooms, current_rooms)

        return max_rooms


def solve():
    """
    Input format (JSON per line):
        Line 1: intervals as JSON array [[start, end], ...]

    Output format:
        Integer - minimum number of rooms
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    intervals = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minMeetingRooms(intervals)

    print(result)


if __name__ == "__main__":
    solve()

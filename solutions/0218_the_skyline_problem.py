"""
LeetCode 218: The Skyline Problem
https://leetcode.com/problems/the-skyline-problem/

A city's skyline is the outer contour of the silhouette formed by all the
buildings when viewed from a distance. Given the locations and heights of all
the buildings, return the skyline formed by these buildings collectively.

Pattern: Line Sweep - Height Tracking
API Kernel: LineSweep

The geometric information of each building is given in the array buildings where
buildings[i] = [lefti, righti, heighti].

Example:
    Input: buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
    Output: [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]
"""

import heapq
import json
import sys
from typing import List

SOLUTIONS = {
    "default": {
        "class": "SolutionHeapLazy",
        "method": "getSkyline",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Max-heap with lazy deletion",
    },
    "heap": {
        "class": "SolutionHeapLazy",
        "method": "getSkyline",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Max-heap with lazy deletion",
    },
    "sortedlist": {
        "class": "SolutionSortedList",
        "method": "getSkyline",
        "complexity": "O(n log n) time, O(n) space",
        "description": "SortedList for O(log n) add/remove/max",
    },
}


def judge(actual, expected, input_data: str) -> bool:
    """Validate skyline output."""
    lines = input_data.strip().split("\n")
    buildings = json.loads(lines[0])

    correct = _reference_skyline(buildings)

    if isinstance(actual, str):
        actual = json.loads(actual)

    return actual == correct


def _reference_skyline(buildings: List[List[int]]) -> List[List[int]]:
    """Reference implementation using heap with lazy deletion."""
    if not buildings:
        return []

    events = []
    for left, right, height in buildings:
        events.append((left, -height, right))  # Start: negative height for max-heap
        events.append((right, 0, 0))  # End marker

    events.sort()
    result = []
    heap = [(0, float("inf"))]  # (neg_height, end_x)

    for x, neg_h, end_x in events:
        while heap[0][1] <= x:
            heapq.heappop(heap)

        if neg_h:  # Start event
            heapq.heappush(heap, (neg_h, end_x))

        curr_max = -heap[0][0]
        if not result or result[-1][1] != curr_max:
            result.append([x, curr_max])

    return result


JUDGE_FUNC = judge


class SolutionHeapLazy:
    """
    Heap Approach with Lazy Deletion:

    Events: (x, type, height)
    - Start: (left, -height, right) - negative height for max-heap simulation
    - End: (right, 0, 0) - marker to trigger cleanup

    Algorithm:
    1. Create events from all buildings
    2. Sort events by x-coordinate
    3. For each x, lazy-delete expired buildings, then add new ones
    4. If max height changed, add to result

    Why lazy deletion?
    - Python's heapq doesn't support efficient removal
    - Instead, mark buildings as "deleted" when their end_x is passed
    - Clean up expired entries when they reach heap top
    """

    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        if not buildings:
            return []

        # Create events: (x, neg_height, end_x)
        # neg_height: negative for starts (for max-heap), 0 for ends
        events = []
        for left, right, height in buildings:
            events.append((left, -height, right))  # Building starts
            events.append((right, 0, 0))  # End marker

        # Sort by x; at same x, process by neg_height (starts before ends)
        events.sort()

        result = []
        # Max-heap: (-height, end_x)
        # Initialize with ground level that never expires
        heap = [(0, float("inf"))]

        for x, neg_height, end_x in events:
            # Lazy deletion: remove buildings that have ended
            while heap[0][1] <= x:
                heapq.heappop(heap)

            if neg_height:  # Start event (neg_height is negative)
                heapq.heappush(heap, (neg_height, end_x))

            # Current max height (negate because of max-heap simulation)
            current_max = -heap[0][0]

            # Only add to result if max height changed
            if not result or result[-1][1] != current_max:
                result.append([x, current_max])

        return result


class SolutionSortedList:
    """
    SortedList Approach:

    Uses sortedcontainers.SortedList for O(log n) operations:
    - add(height): Insert height
    - remove(height): Delete height
    - [-1]: Get max height

    Events: (x, type, height)
    - type=0: Start (add height)
    - type=1: End (remove height)

    Sort order:
    - By x-coordinate
    - At same x: starts before ends (type 0 before type 1)
    - For starts: taller first (-height in sort key)
    - For ends: shorter first (height in sort key)
    """

    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        try:
            from sortedcontainers import SortedList
        except ImportError:
            # Fallback to heap solution if sortedcontainers not available
            return SolutionHeapLazy().getSkyline(buildings)

        if not buildings:
            return []

        # Create events: (x, type, height)
        # type: 0 = start, 1 = end
        events = []
        for left, right, height in buildings:
            events.append((left, 0, height))  # Building starts
            events.append((right, 1, height))  # Building ends

        # Sort: by x, then starts before ends, then by height
        # For starts: process taller first (-height)
        # For ends: process shorter first (+height)
        events.sort(key=lambda e: (e[0], e[1], -e[2] if e[1] == 0 else e[2]))

        result = []
        # SortedList of active heights, always includes 0 (ground level)
        active_heights = SortedList([0])

        for x, event_type, height in events:
            if event_type == 0:  # Start
                active_heights.add(height)
            else:  # End
                active_heights.remove(height)

            current_max = active_heights[-1]

            # Add to result if max height changed
            if not result or result[-1][1] != current_max:
                result.append([x, current_max])

        return result


def solve():
    """
    Input format (JSON per line):
        Line 1: buildings as JSON array [[left, right, height], ...]

    Output format:
        JSON array of critical points [[x, height], ...]
    """
    lines = sys.stdin.read().strip().split("\n")
    buildings = json.loads(lines[0])

    from _runner import get_solver

    solver = get_solver(SOLUTIONS)
    result = solver.getSkyline(buildings)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

"""
Problem: The Latest Time to Catch a Bus
Link: https://leetcode.com/problems/the-latest-time-to-catch-a-bus/

Find the latest arrival time to catch a bus without clashing with other passengers.

Constraints:
- n == buses.length
- m == passengers.length
- 1 <= n, m, capacity <= 10^5
- 2 <= buses[i], passengers[i] <= 10^9
- All buses[i] and passengers[i] are unique

Topics: Array, Two Pointers, Binary Search, Sorting
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "latestTimeCatchTheBus",
        "complexity": "O(n log n + m log m) time, O(sort) space",
        "description": "Simulate boarding, then backtrack to find gap",
    },
}


# JUDGE_FUNC for generated tests
def _reference(buses: List[int], passengers: List[int], capacity: int) -> int:
    """Reference implementation."""
    buses.sort()
    passengers.sort()
    passenger_set = set(passengers)

    j = 0  # Passenger index
    last_boarded = -1

    for bus_time in buses:
        seats = capacity
        while seats > 0 and j < len(passengers) and passengers[j] <= bus_time:
            last_boarded = passengers[j]
            j += 1
            seats -= 1

    # Try to arrive at last bus time if there's room
    if seats > 0:
        ans = buses[-1]
    else:
        ans = last_boarded

    # Backtrack to find time not clashing with any passenger
    while ans in passenger_set:
        ans -= 1

    return ans


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    buses = json.loads(lines[0])
    passengers = json.loads(lines[1])
    capacity = int(lines[2])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(buses[:], passengers[:], capacity)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Simulate + Backtrack
# Time: O(n log n + m log m), Space: O(sort)
# ============================================================================
class Solution:
    # Key insight: Simulate boarding process to find:
    # 1. If last bus has empty seats -> try arriving at bus departure time
    # 2. Otherwise -> try arriving just before the last boarded passenger
    #
    # In either case, backtrack until we find a time not occupied by passengers.
    #
    # Why this works:
    # - If we have a seat, arriving at bus time guarantees catching it
    # - If full, we need to "steal" a spot from the last boarded passenger
    # - Backtracking finds the gap in passenger arrivals

    def latestTimeCatchTheBus(self, buses: List[int], passengers: List[int], capacity: int) -> int:
        buses.sort()
        passengers.sort()
        passenger_set = set(passengers)

        j = 0  # Passenger pointer
        last_boarded = -1

        # Simulate boarding
        for bus_time in buses:
            seats = capacity
            while seats > 0 and j < len(passengers) and passengers[j] <= bus_time:
                last_boarded = passengers[j]
                j += 1
                seats -= 1

        # Determine best candidate time
        if seats > 0:
            # Last bus has room - try to arrive at departure
            ans = buses[-1]
        else:
            # Last bus was full - try to arrive before last boarded
            ans = last_boarded

        # Backtrack to find non-conflicting time
        while ans in passenger_set:
            ans -= 1

        return ans


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: buses (JSON array)
        Line 2: passengers (JSON array)
        Line 3: capacity (integer)

    Example:
        [10,20]
        [2,17,18,19]
        2
        -> 16
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    buses = json.loads(lines[0])
    passengers = json.loads(lines[1])
    capacity = int(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.latestTimeCatchTheBus(buses, passengers, capacity)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

"""
Problem: Corporate Flight Bookings
Link: https://leetcode.com/problems/corporate-flight-bookings/

There are n flights that are labeled from 1 to n.

You are given an array of flight bookings bookings, where
bookings[i] = [first_i, last_i, seats_i] represents a booking for flights
first_i through last_i (inclusive) with seats_i seats reserved for each
flight in the range.

Return an array answer of length n, where answer[i] is the total number of
seats reserved for flight i.

Example 1:
    Input: bookings = [[1,2,10],[2,3,20],[2,5,25]], n = 5
    Output: [10,55,45,25,25]
    Explanation:
        Flight labels:        1   2   3   4   5
        Booking 1 reserved:  10  10
        Booking 2 reserved:      20  20
        Booking 3 reserved:      25  25  25  25
        Total seats:         10  55  45  25  25

Example 2:
    Input: bookings = [[1,2,10],[2,2,15]], n = 2
    Output: [10,25]

Constraints:
- 1 <= n <= 2 * 10^4
- 1 <= bookings.length <= 2 * 10^4
- bookings[i].length == 3
- 1 <= first_i <= last_i <= n
- 1 <= seats_i <= 10^4

Topics: Array, Prefix Sum
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionDifferenceArray",
        "method": "corpFlightBookings",
        "complexity": "O(n + m) time, O(n) space where m = bookings",
        "description": "Difference array for range updates, prefix sum to get final counts",
    },
    "difference": {
        "class": "SolutionDifferenceArray",
        "method": "corpFlightBookings",
        "complexity": "O(n + m) time, O(n) space where m = bookings",
        "description": "Difference array for range updates, prefix sum to get final counts",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate result: seat count array."""
    lines = input_data.strip().split("\n")
    bookings = json.loads(lines[0])
    n = int(lines[1])

    correct = _reference_corp_flight_bookings(bookings, n)

    if isinstance(actual, list):
        return actual == correct

    try:
        actual_list = json.loads(str(actual).strip())
        return actual_list == correct
    except (ValueError, json.JSONDecodeError):
        return False


def _reference_corp_flight_bookings(bookings: List[List[int]], n: int) -> List[int]:
    """O(n + m) reference using difference array."""
    diff = [0] * (n + 1)

    for first, last, seats in bookings:
        diff[first - 1] += seats
        if last < n:
            diff[last] -= seats

    result = []
    current = 0
    for i in range(n):
        current += diff[i]
        result.append(current)

    return result


JUDGE_FUNC = judge


# ============================================================================
# Solution: Difference Array (Canonical Range Update)
# Time: O(n + m) where n = flights, m = bookings
# Space: O(n)
#   - Classic difference array problem: apply range updates efficiently
#   - diff[i] represents the change in seat count at flight i
#   - Mark +seats at first flight, -seats at (last+1) flight
#   - Prefix sum reconstructs actual seat counts
#
# Key Insight: Difference Array is the inverse of Prefix Sum.
# - Prefix Sum: given point values, compute range sums in O(1)
# - Difference Array: given range updates, compute point values in O(n)
#
# To add 'seats' to range [first, last] (inclusive):
#   diff[first] += seats      (start adding seats)
#   diff[last+1] -= seats     (stop adding seats after last)
# Prefix sum of diff gives the actual seat count for each flight.
#
# Note: Flights are 1-indexed in problem, but we use 0-indexed arrays.
#
# Pattern: difference_array
# See: docs/patterns/prefix_sum/templates.md Section 8 (Flight Bookings)
# ============================================================================
class SolutionDifferenceArray:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        """
        Compute total seats reserved for each flight using difference array.

        Each booking [first, last, seats] reserves 'seats' for flights
        first through last (inclusive). We use difference array to handle
        these range updates efficiently.
        """
        # Difference array: diff[i] = change in seat count at flight i
        # Use n+1 to handle the boundary case when last == n
        seat_change = [0] * (n + 1)

        # Apply range updates using difference array technique
        for first_flight, last_flight, seat_count in bookings:
            # Convert to 0-indexed: first_flight=1 → index 0
            seat_change[first_flight - 1] += seat_count    # Start adding seats
            seat_change[last_flight] -= seat_count         # Stop after last flight

        # Prefix sum to reconstruct actual seat counts
        total_seats = []
        current_seats = 0
        for flight_index in range(n):
            current_seats += seat_change[flight_index]
            total_seats.append(current_seats)

        return total_seats


def solve():
    """
    Input format (JSON per line):
        Line 1: bookings as JSON array of [first, last, seats]
        Line 2: n as integer

    Output format:
        JSON array of seat counts for each flight
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    bookings = json.loads(lines[0])
    n = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.corpFlightBookings(bookings, n)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

"""
Problem: Car Pooling
Link: https://leetcode.com/problems/car-pooling/

There is a car with capacity empty seats. The vehicle only drives east
(i.e., it cannot turn around and drive west).

You are given the integer capacity and an array trips where
trips[i] = [numPassengers_i, from_i, to_i] indicates that the ith trip has
numPassengers_i passengers and the locations to pick them up and drop them
off are from_i and to_i respectively.

Return true if it is possible to pick up and drop off all passengers for
all the given trips, or false otherwise.

Example 1:
    Input: trips = [[2,1,5],[3,3,7]], capacity = 4
    Output: false

Example 2:
    Input: trips = [[2,1,5],[3,3,7]], capacity = 5
    Output: true

Constraints:
- 1 <= trips.length <= 1000
- trips[i].length == 3
- 1 <= numPassengers_i <= 100
- 0 <= from_i < to_i <= 1000
- 1 <= capacity <= 10^5

Topics: Array, Sorting, Heap (Priority Queue), Simulation, Prefix Sum
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionDifferenceArray",
        "method": "carPooling",
        "complexity": "O(n + m) time, O(m) space where m = max location",
        "description": "Difference array for range updates, prefix sum to check capacity",
    },
    "difference": {
        "class": "SolutionDifferenceArray",
        "method": "carPooling",
        "complexity": "O(n + m) time, O(m) space where m = max location",
        "description": "Difference array for range updates, prefix sum to check capacity",
    },
    "events": {
        "class": "SolutionEvents",
        "method": "carPooling",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Event-based: sort pickup/dropoff events and simulate",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate result: check if car pooling is possible."""
    lines = input_data.strip().split("\n")
    trips = json.loads(lines[0])
    capacity = int(lines[1])

    correct = _reference_car_pooling(trips, capacity)

    if isinstance(actual, bool):
        return actual == correct

    if isinstance(actual, str):
        actual_lower = actual.strip().lower()
        if actual_lower == "true":
            return correct is True
        elif actual_lower == "false":
            return correct is False

    return False


def _reference_car_pooling(trips: List[List[int]], capacity: int) -> bool:
    """O(n + m) reference using difference array."""
    max_loc = max(trip[2] for trip in trips)
    diff = [0] * (max_loc + 1)

    for passengers, start, end in trips:
        diff[start] += passengers
        if end <= max_loc:
            diff[end] -= passengers

    current = 0
    for delta in diff:
        current += delta
        if current > capacity:
            return False

    return True


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Difference Array
# Time: O(n + m) where n = trips, m = max location
# Space: O(m)
#   - Mark +passengers at pickup location, -passengers at dropoff location
#   - Prefix sum of difference array gives actual passenger count
#   - Check if any location exceeds capacity
#
# Key Insight: Difference Array is the inverse of Prefix Sum.
# - Prefix Sum: given point values, compute range sums
# - Difference Array: given range updates, compute point values
#
# To add 'passengers' to range [from, to):
#   diff[from] += passengers   (pickup)
#   diff[to] -= passengers     (dropoff, passengers exit at 'to')
# Then prefix sum gives actual passenger count at each location.
#
# Pattern: difference_array
# See: docs/patterns/prefix_sum/templates.md Section 7 (Car Pooling)
# ============================================================================
class SolutionDifferenceArray:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        """
        Check if car can handle all trips without exceeding capacity.

        Uses difference array technique:
        1. Record passenger changes at pickup/dropoff locations
        2. Prefix sum gives actual passenger count at each location
        3. Verify no location exceeds capacity
        """
        # Find max location to determine array size
        max_location = max(trip[2] for trip in trips)

        # Difference array: diff[i] = change in passenger count at location i
        passenger_change = [0] * (max_location + 1)

        # Build difference array
        for passengers, pickup_location, dropoff_location in trips:
            passenger_change[pickup_location] += passengers    # Passengers board
            passenger_change[dropoff_location] -= passengers   # Passengers exit

        # Prefix sum to compute actual passenger count at each location
        current_passengers = 0
        for delta in passenger_change:
            current_passengers += delta
            if current_passengers > capacity:
                return False

        return True


# ============================================================================
# Solution 2: Event-Based Simulation
# Time: O(n log n), Space: O(n)
#   - Create pickup (+) and dropoff (-) events
#   - Sort events by location (dropoffs before pickups at same location)
#   - Simulate to track passenger count
#
# When to Use: Useful when locations are sparse (large range, few events).
# ============================================================================
class SolutionEvents:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        """
        Check car pooling feasibility using event-based simulation.

        Creates discrete events for pickups and dropoffs, then processes
        in location order to track passenger count.
        """
        events = []

        for passengers, pickup_location, dropoff_location in trips:
            events.append((pickup_location, passengers))    # Positive = pickup
            events.append((dropoff_location, -passengers))  # Negative = dropoff

        # Sort by location; at same location, process dropoffs first (negative values)
        # This ensures passengers exit before new ones board at same stop
        events.sort(key=lambda event: (event[0], event[1]))

        current_passengers = 0
        for _location, passenger_delta in events:
            current_passengers += passenger_delta
            if current_passengers > capacity:
                return False

        return True


def solve():
    """
    Input format (JSON per line):
        Line 1: trips as JSON array of [passengers, from, to]
        Line 2: capacity as integer

    Output format:
        true or false
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    trips = json.loads(lines[0])
    capacity = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.carPooling(trips, capacity)

    print("true" if result else "false")


if __name__ == "__main__":
    solve()

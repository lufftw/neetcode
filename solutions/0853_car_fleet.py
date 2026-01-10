"""
Problem: Car Fleet
Link: https://leetcode.com/problems/car-fleet/

There are n cars at given miles away from the starting mile 0, heading towards
the same destination at mile target.

You are given two integer arrays position and speed, both of length n, where
position[i] is the starting position of the ith car and speed[i] is the speed
of the ith car (in miles per hour).

A car cannot pass another car, but it can catch up and then travel at the same
speed as the car ahead. A car fleet is a non-empty set of cars driving at the
same position and speed. Note that a single car is also a car fleet.

If a car catches up to a car fleet the moment the fleet reaches the destination,
it is still considered one fleet.

Return the number of car fleets that will arrive at the destination.

Example 1:
    Input: target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
    Output: 3
    Explanation:
    - Car at position 10 (speed 2) -> reaches target at time (12-10)/2 = 1
    - Car at position 8 (speed 4) -> reaches target at time (12-8)/4 = 1
      But car at position 10 is ahead, so they form a fleet at time 1.
    - Car at position 0 (speed 1) -> reaches target at time 12
    - Car at position 5 (speed 1) -> reaches target at time 7
    - Car at position 3 (speed 3) -> reaches target at time 3
      Cars at positions 0, 5, 3 each form their own fleet.
    Total: 3 fleets

Example 2:
    Input: target = 10, position = [3], speed = [3]
    Output: 1
    Explanation: There is only one car, hence only one fleet.

Example 3:
    Input: target = 100, position = [0,2,4], speed = [4,2,1]
    Output: 1
    Explanation: All cars eventually catch up and form one fleet.

Constraints:
- n == position.length == speed.length
- 1 <= n <= 10^5
- 0 < target <= 10^6
- 0 <= position[i] < target
- All the values of position are unique.
- 0 < speed[i] <= 10^6

Topics: Array, Stack, Sorting, Monotonic Stack
"""

import json
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionSort",
        "method": "carFleet",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Sort by position descending, count non-decreasing arrival times",
    },
    "stack": {
        "class": "SolutionStack",
        "method": "carFleet",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Monotonic stack tracking fleet leaders (latest arrivals)",
    },
}


# ============================================================================
# Solution 1: Sorting by Position
# Time: O(n log n) for sorting, Space: O(n)
#
# Key Insight:
#   A car can only catch up to and merge with cars AHEAD of it (closer to target).
#   Cars behind cannot affect cars ahead. This means we should process cars from
#   closest to target to farthest.
#
#   The arrival time of car i (assuming no blocking) is: (target - position[i]) / speed[i]
#
#   When processing from front to back:
#   - If car i has arrival time <= car ahead, it catches up (same fleet)
#   - If car i has arrival time > car ahead, it forms a new fleet
#
# Algorithm:
#   1. Pair (position, arrival_time) for each car
#   2. Sort by position descending (closest to target first)
#   3. Count how many times arrival time INCREASES (new fleet)
#
# Why This Works:
#   Cars closer to target can never be caught by their own fleet merge - they
#   set the pace. A slower-arriving car ahead blocks all faster cars behind.
# ============================================================================
class SolutionSort:
    """
    Sort by position and count distinct fleet leaders.

    Process cars from closest to farthest from target. A car forms a new
    fleet if its arrival time exceeds all previous cars (it won't be blocked).
    Cars with arrival time <= the slowest car ahead join that fleet.
    """

    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        if not position:
            return 0

        # Calculate arrival time for each car
        # arrival_time = (target - position) / speed
        cars = [(pos, (target - pos) / spd) for pos, spd in zip(position, speed)]

        # Sort by position descending (closest to target first)
        cars.sort(reverse=True)

        fleets = 0
        max_time = 0  # Slowest arrival time seen so far (sets the pace)

        for _, time in cars:
            if time > max_time:
                # This car arrives later than all cars ahead
                # It forms a new fleet (won't be caught)
                fleets += 1
                max_time = time
            # else: this car catches up to the fleet ahead (same fleet)

        return fleets


# ============================================================================
# Solution 2: Monotonic Stack
# Time: O(n log n) for sorting, Space: O(n)
#
# Key Insight:
#   We can use a monotonic stack to explicitly track fleet "leaders" - the
#   cars that set the pace for each fleet. A car is a fleet leader if it
#   arrives later than any car behind it.
#
# Algorithm:
#   1. Sort cars by position (closest to target first)
#   2. For each car, push its arrival time onto stack
#   3. While current time >= stack top, pop (merge into current fleet)
#   4. Push current time
#   5. Stack size = number of fleets
#
# This is conceptually the same as Solution 1 but makes the "blocking"
# relationship more explicit through stack operations.
# ============================================================================
class SolutionStack:
    """
    Monotonic stack tracking fleet leaders.

    Stack contains arrival times of fleet leaders. When processing a car,
    if it arrives no later than the top of stack, it merges with that fleet.
    The stack maintains decreasing arrival times (each is a fleet leader).
    """

    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        if not position:
            return 0

        # Calculate arrival time and sort by position descending
        cars = sorted(
            [(pos, (target - pos) / spd) for pos, spd in zip(position, speed)],
            reverse=True,
        )

        # Stack stores arrival times of fleet leaders
        stack = []

        for _, time in cars:
            # If this car doesn't catch up to the fleet ahead, it's a new leader
            if not stack or time > stack[-1]:
                stack.append(time)
            # else: car merges with fleet at stack top (don't push)

        return len(stack)


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: target as integer
        Line 2: position as JSON array
        Line 3: speed as JSON array

    Example:
        12
        [10,8,0,5,3]
        [2,4,1,1,3]
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    target = json.loads(lines[0])
    position = json.loads(lines[1])
    speed = json.loads(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.carFleet(target, position, speed)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

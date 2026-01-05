"""
Problem: Daily Temperatures
Link: https://leetcode.com/problems/daily-temperatures/

Given an array of integers temperatures represents the daily temperatures,
return an array answer such that answer[i] is the number of days you have
to wait after the i-th day to get a warmer temperature.

If there is no future day for which this is possible, keep answer[i] == 0.

Constraints:
- 1 <= temperatures.length <= 10^5
- 30 <= temperatures[i] <= 100

Topics: Array, Stack, Monotonic Stack
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionMonotonicStack",
        "method": "dailyTemperatures",
        "complexity": "O(n) time, O(n) space",
        "description": "Monotonic decreasing stack storing indices",
    },
    "stack": {
        "class": "SolutionMonotonicStack",
        "method": "dailyTemperatures",
        "complexity": "O(n) time, O(n) space",
        "description": "Monotonic decreasing stack storing indices",
    },
    "backward": {
        "class": "SolutionBackwardScan",
        "method": "dailyTemperatures",
        "complexity": "O(n) time, O(1) space",
        "description": "Backward iteration with jump optimization",
    },
}


# ============================================================================
# Solution 1: Monotonic Decreasing Stack
# Time: O(n), Space: O(n)
#   - Stack stores indices of days waiting for a warmer temperature
#   - Temperatures at stacked indices form a decreasing sequence
#   - When warmer temp found, pop and compute distance for all colder days
#
# Key Insight: This is "Next Greater Element Distance" - we need the gap,
# not the value. Storing indices allows: distance = current_idx - popped_idx
# ============================================================================
class SolutionMonotonicStack:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        num_days = len(temperatures)
        days_until_warmer = [0] * num_days
        waiting_days_stack: list[int] = []  # Indices of unresolved days

        for current_day, current_temp in enumerate(temperatures):
            # Resolve all days that found their warmer temperature
            while (
                waiting_days_stack
                and temperatures[waiting_days_stack[-1]] < current_temp
            ):
                resolved_day = waiting_days_stack.pop()
                days_until_warmer[resolved_day] = current_day - resolved_day

            waiting_days_stack.append(current_day)

        # Days remaining in stack have no warmer future day (already 0)
        return days_until_warmer


# ============================================================================
# Solution 2: Backward Scan with Jump Optimization
# Time: O(n), Space: O(1) extra (output array doesn't count)
#   - Process from right to left, using already-computed results as "jumps"
#   - If temperatures[j] <= temperatures[i], jump by result[j] to skip days
#   - Amortized O(n) due to jump optimization avoiding redundant comparisons
#
# Key Insight: When scanning backward, previously computed results form a
# "jump table" - if day j isn't warmer than day i, we can skip to j's answer.
# ============================================================================
class SolutionBackwardScan:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        num_days = len(temperatures)
        days_until_warmer = [0] * num_days

        # Process from second-to-last day backward
        for current_day in range(num_days - 2, -1, -1):
            next_day = current_day + 1

            # Follow jump chain until warmer day found or no more days
            while (
                next_day < num_days
                and temperatures[next_day] <= temperatures[current_day]
            ):
                if days_until_warmer[next_day] == 0:
                    # No warmer day exists after next_day
                    next_day = num_days  # Will exit loop with result 0
                    break
                # Jump to next_day's warmer day (skip intermediate days)
                next_day += days_until_warmer[next_day]

            if next_day < num_days:
                days_until_warmer[current_day] = next_day - current_day

        return days_until_warmer


def solve():
    """
    Input format (JSON):
        Line 1: temperatures as JSON array

    Output format:
        JSON array of days until warmer temperature
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    temperatures = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.dailyTemperatures(temperatures)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

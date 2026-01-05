"""
Problem: Daily Temperatures
Link: https://leetcode.com/problems/daily-temperatures/

Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.

Example 1:
    Input: temperatures = [73,74,75,71,69,72,76,73]
    Output: [1,1,4,2,1,1,0,0]

Example 2:
    Input: temperatures = [30,40,50,60]
    Output: [1,1,1,0]

Example 3:
    Input: temperatures = [30,60,90]
    Output: [1,1,0]

Constraints:
- 1 <= temperatures.length <= 10^5
- 30 <= temperatures[i] <= 100

Topics: Array, Stack, Monotonic Stack

Hint 1: If the temperature is say, 70 today, then in the future a warmer temperature must be either 71, 72, 73, ..., 99, or 100.  We could remember when all of them occur next.
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
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is the correct wait days array.

    Args:
        actual: Program output (list as string or list)
        expected: Expected output (None if from generator)
        input_data: Raw input string (JSON array)

    Returns:
        bool: True if correct wait days for warmer temperatures
    """
    line = input_data.strip()
    temperatures = json.loads(line) if line else []

    # Compute correct answer using reference solution
    correct = _reference_daily_temps(temperatures)

    # Parse actual output
    actual_str = actual.strip()
    try:
        actual_list = json.loads(actual_str) if actual_str else []
        return actual_list == correct
    except (ValueError, json.JSONDecodeError):
        return False


def _reference_daily_temps(temps: List[int]) -> List[int]:
    """O(n) reference using monotonic stack."""
    n = len(temps)
    result = [0] * n
    stack: list[int] = []

    for i, temp in enumerate(temps):
        while stack and temps[stack[-1]] < temp:
            prev_day = stack.pop()
            result[prev_day] = i - prev_day
        stack.append(i)

    return result


JUDGE_FUNC = judge


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

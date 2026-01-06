"""
Problem: Jump Game
Link: https://leetcode.com/problems/jump-game/

You are given an integer array nums. You are initially positioned at the
array's first index, and each element in the array represents your maximum
jump length at that position.

Return true if you can reach the last index, or false otherwise.

Example 1:
    Input: nums = [2,3,1,1,4]
    Output: true
    Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:
    Input: nums = [3,2,1,0,4]
    Output: false
    Explanation: You will always arrive at index 3 no matter what. Its maximum
                 jump length is 0, which makes it impossible to reach the last index.

Constraints:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 10^5

Topics: Array, Dynamic Programming, Greedy
Pattern: GreedyCore - Reachability Kernel
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionGreedy",
        "method": "canJump",
        "complexity": "O(n) time, O(1) space",
        "description": "Track farthest reachable position",
    },
    "greedy": {
        "class": "SolutionGreedy",
        "method": "canJump",
        "complexity": "O(n) time, O(1) space",
        "description": "Track farthest reachable position",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "canJump",
        "complexity": "O(n^2) time, O(n) space",
        "description": "Dynamic programming with reachability array",
    },
}


# ============================================================================
# JUDGE_FUNC - Validate reachability result
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output matches expected reachability.

    Args:
        actual: Program output (bool as string or bool)
        expected: Expected output (None if from generator)
        input_data: Raw input string (nums as JSON)

    Returns:
        bool: True if correct reachability result
    """
    nums = json.loads(input_data.strip())
    correct = _reference_can_jump(nums)

    # Parse actual output
    if isinstance(actual, bool):
        actual_bool = actual
    elif isinstance(actual, str):
        actual_str = actual.strip().lower()
        if actual_str == "true":
            actual_bool = True
        elif actual_str == "false":
            actual_bool = False
        else:
            return False
    else:
        return False

    return actual_bool == correct


def _reference_can_jump(nums: List[int]) -> bool:
    """O(n) reference using greedy farthest reach."""
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)
        if farthest >= len(nums) - 1:
            return True
    return True


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Greedy - Farthest Reachable Position
# Time: O(n), Space: O(1)
#
# Core Insight (Reachability Kernel):
#   At each position i, we can reach any position up to i + nums[i].
#   Track the farthest position reachable so far.
#   If current position > farthest, we're stuck.
#   If farthest >= last index, we can reach the end.
#
# Greedy Choice Property:
#   We don't need to track the exact path - only whether each position
#   is reachable from some previous position.
#
# Pattern Reference: GreedyCore - Reachability
# See: docs/patterns/greedy_core/templates.md
# ============================================================================
class SolutionGreedy:
    def canJump(self, nums: List[int]) -> bool:
        farthest_reachable = 0
        last_index = len(nums) - 1

        for current_position, max_jump in enumerate(nums):
            # If current position is beyond farthest reachable, we're stuck
            if current_position > farthest_reachable:
                return False

            # Update farthest reachable position
            farthest_reachable = max(farthest_reachable, current_position + max_jump)

            # Early termination: can already reach the end
            if farthest_reachable >= last_index:
                return True

        return True


# ============================================================================
# Solution 2: Dynamic Programming
# Time: O(n^2), Space: O(n)
#
# State: dp[i] = True if position i is reachable from start
# Transition: dp[j] = True if any dp[i] where i + nums[i] >= j
#
# Educational Value: Shows the DP approach before optimization to greedy.
# ============================================================================
class SolutionDP:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        reachable = [False] * n
        reachable[0] = True

        for i in range(n):
            if not reachable[i]:
                continue
            # Mark all positions reachable from i
            for j in range(i + 1, min(i + nums[i] + 1, n)):
                reachable[j] = True
            # Early termination
            if reachable[n - 1]:
                return True

        return reachable[n - 1]


def solve():
    """
    Input format (JSON per line):
        Line 1: nums as JSON array

    Output format:
        true or false
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.canJump(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

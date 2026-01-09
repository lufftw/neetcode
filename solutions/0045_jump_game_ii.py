"""
Problem: Jump Game II
Link: https://leetcode.com/problems/jump-game-ii/

You are given a 0-indexed array of integers nums of length n. You are
initially positioned at nums[0].

Each element nums[i] represents the maximum length of a forward jump from
index i. In other words, if you are at nums[i], you can jump to any
nums[i + j] where:
- 0 <= j <= nums[i] and
- i + j < n

Return the minimum number of jumps to reach nums[n - 1]. The test cases
are generated such that you can reach nums[n - 1].

Example 1:
    Input: nums = [2,3,1,1,4]
    Output: 2
    Explanation: The minimum number of jumps to reach the last index is 2.
                 Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:
    Input: nums = [2,3,0,1,4]
    Output: 2

Constraints:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 1000
- It's guaranteed that you can reach nums[n - 1].

Topics: Array, Dynamic Programming, Greedy
Pattern: GreedyCore - Reachability Kernel (Minimum Jumps Variant)
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionGreedy",
        "method": "jump",
        "complexity": "O(n) time, O(1) space",
        "description": "BFS-like level traversal with farthest reach",
    },
    "greedy": {
        "class": "SolutionGreedy",
        "method": "jump",
        "complexity": "O(n) time, O(1) space",
        "description": "BFS-like level traversal with farthest reach",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "jump",
        "complexity": "O(n²) time, O(n) space",
        "description": "DP: min jumps to reach each position",
    },
}


# ============================================================================
# JUDGE_FUNC - Validate minimum jumps result
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate minimum jumps result."""
    nums = json.loads(input_data.strip())
    correct = _reference_jump(nums)

    if isinstance(actual, int):
        actual_int = actual
    elif isinstance(actual, str):
        try:
            actual_int = int(actual.strip())
        except ValueError:
            return False
    else:
        return False

    return actual_int == correct


def _reference_jump(nums: List[int]) -> int:
    """O(n) reference using greedy BFS-like approach."""
    if len(nums) <= 1:
        return 0

    jumps = 0
    current_end = 0
    farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
            if current_end >= len(nums) - 1:
                break

    return jumps


JUDGE_FUNC = judge


# ============================================================================
# Solution: Greedy BFS-like Level Traversal
# Time: O(n), Space: O(1)
#
# Core Insight:
#   Think of jumps as BFS levels. From position 0, we can reach positions
#   in range [1, nums[0]] with 1 jump. From those positions, we can reach
#   further positions with 2 jumps, etc.
#
#   Key variables:
#   - current_end: rightmost position reachable with current number of jumps
#   - farthest: rightmost position reachable with one more jump
#
#   When we reach current_end, we must take another jump.
#
# Pattern Reference: GreedyCore - Reachability (min jumps variant)
# ============================================================================
class SolutionGreedy:
    def jump(self, nums: List[int]) -> int:
        if len(nums) <= 1:
            return 0

        jump_count = 0
        current_level_end = 0  # Rightmost position reachable with current jumps
        next_level_farthest = 0  # Rightmost position reachable with one more jump

        # Don't need to process last element - we just need to reach it
        for position in range(len(nums) - 1):
            # Update farthest reachable with one more jump
            next_level_farthest = max(next_level_farthest, position + nums[position])

            # If we've reached the end of current level, must jump
            if position == current_level_end:
                jump_count += 1
                current_level_end = next_level_farthest

                # Early termination: can reach the end
                if current_level_end >= len(nums) - 1:
                    break

        return jump_count


# ============================================================================
# Solution 2: Dynamic Programming
# Time: O(n²), Space: O(n)
#   - dp[i] = minimum jumps to reach position i
#   - For each position, try all reachable positions
#   - Less efficient than greedy but shows DP perspective
# ============================================================================
class SolutionDP:
    def jump(self, nums: List[int]) -> int:
        """
        DP approach: compute minimum jumps to each position.

        State: dp[i] = minimum jumps to reach position i
        Transition: dp[j] = min(dp[j], dp[i] + 1) for all j reachable from i

        O(n²) because for each position we may update many destinations.
        """
        n = len(nums)
        if n <= 1:
            return 0

        # dp[i] = min jumps to reach position i
        dp = [float('inf')] * n
        dp[0] = 0

        for i in range(n):
            # Try all positions reachable from i
            max_reach = min(i + nums[i], n - 1)
            for j in range(i + 1, max_reach + 1):
                dp[j] = min(dp[j], dp[i] + 1)

        return dp[n - 1]


def solve():
    """
    Input format (JSON per line):
        Line 1: nums as JSON array

    Output format:
        Integer (minimum number of jumps)
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.jump(nums)

    print(result)


if __name__ == "__main__":
    solve()

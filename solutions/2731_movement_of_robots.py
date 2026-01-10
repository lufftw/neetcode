"""
Problem: Movement of Robots
Link: https://leetcode.com/problems/movement-of-robots/

Robots on number line move L/R. When they collide, they reverse. After d seconds,
return sum of pairwise distances modulo 10^9 + 7.

Constraints:
- 2 <= nums.length <= 10^5
- -2 * 10^9 <= nums[i] <= 2 * 10^9
- 0 <= d <= 10^9

Topics: Array, Brainteaser, Sorting, Prefix Sum
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "sumDistance",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Collision trick + prefix sum for pairwise distances",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int], s: str, d: int) -> int:
    """Reference implementation."""
    MOD = 10**9 + 7
    pos = [nums[i] + d if s[i] == 'R' else nums[i] - d for i in range(len(nums))]
    pos.sort()
    result = prefix = 0
    for i, p in enumerate(pos):
        result = (result + i * p - prefix) % MOD
        prefix += p
    return result


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    s = json.loads(lines[1])
    d = int(lines[2])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(nums, s, d)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Ignore Collisions + Prefix Sum
# Time: O(n log n), Space: O(n)
# ============================================================================
class Solution:
    # Key insight (brain teaser):
    #   - When robots collide and reverse, from an identity-agnostic view,
    #     it's as if they "pass through" each other
    #   - Final POSITIONS are the same whether we track collisions or not
    #   - Only identities swap, but we don't care about identities for distance
    #
    # Algorithm:
    #   1. Compute final positions ignoring collisions
    #   2. Sort positions
    #   3. Use prefix sum to compute sum of all pairwise distances
    #
    # For sorted array: contribution of pos[i] = i * pos[i] - prefix[i]
    #   (distance to all i previous elements)

    def sumDistance(self, nums: List[int], s: str, d: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        # Final positions ignoring collisions
        pos = [nums[i] + d if s[i] == 'R' else nums[i] - d for i in range(n)]
        pos.sort()

        # Sum of all pairwise distances using prefix sum
        result = 0
        prefix = 0
        for i in range(n):
            # pos[i] contributes (pos[i] - pos[j]) for all j < i
            # = i * pos[i] - sum(pos[0..i-1])
            result = (result + i * pos[i] - prefix) % MOD
            prefix += pos[i]

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)
        Line 2: s (JSON string)
        Line 3: d (integer)

    Example:
        [-2,0,2]
        "RLL"
        3
        -> 8
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])
    s = json.loads(lines[1])
    d = int(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.sumDistance(nums, s, d)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

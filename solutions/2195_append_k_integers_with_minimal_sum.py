"""
Problem: Append K Integers With Minimal Sum
Link: https://leetcode.com/problems/append-k-integers-with-minimal-sum/

Find sum of k smallest positive integers not in nums.

Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^9
- 1 <= k <= 10^8

Topics: Array, Math, Greedy, Sorting
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minimalKSum",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Sort nums, adjust sum formula for blocked numbers",
    },
}


def sum_1_to_n(n):
    """Sum of 1 + 2 + ... + n."""
    return n * (n + 1) // 2


# JUDGE_FUNC for generated tests
def _reference(nums: List[int], k: int) -> int:
    """Reference implementation."""
    nums_set = set(nums)

    # Find k smallest positive integers not in nums
    result = 0
    current = 1
    count = 0

    while count < k:
        if current not in nums_set:
            result += current
            count += 1
        current += 1

    return result


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    k = json.loads(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    # For small k, use reference
    if k <= 10000:
        return actual == _reference(nums, k)
    return isinstance(actual, int) and actual > 0


JUDGE_FUNC = judge


# ============================================================================
# Solution: Math with Sorted Unique Elements
# Time: O(n log n), Space: O(n)
# ============================================================================
class Solution:
    # Key insight:
    #   - Ideally we want sum(1..k) = k*(k+1)/2
    #   - For each num in nums that's within our range, it "blocks" a spot
    #   - We need to extend range to accommodate blocked numbers
    #
    # Algorithm:
    #   - Sort and dedupe nums
    #   - Track 'end' = k (we want k numbers from [1, end])
    #   - For each num in sorted unique nums:
    #     - If num <= end, it blocks a spot, so end += 1
    #   - Final answer = sum(1..end) - sum(blocked nums <= end)

    def minimalKSum(self, nums: List[int], k: int) -> int:
        # Sort and deduplicate
        sorted_unique = sorted(set(nums))

        # Start with target range [1, k]
        end = k

        # Track sum of blocked numbers
        blocked_sum = 0

        for num in sorted_unique:
            if num <= end:
                # This number blocks a spot in [1, end]
                blocked_sum += num
                end += 1  # Extend range by 1
            else:
                # Numbers beyond our range don't matter
                break

        # Sum of [1, end] minus blocked numbers
        return sum_1_to_n(end) - blocked_sum


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)
        Line 2: k (integer)

    Example:
        [1,4,25,10,25]
        2
        -> 5
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])
    k = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.minimalKSum(nums, k)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

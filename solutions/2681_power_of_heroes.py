"""
Problem: Power of Heroes
Link: https://leetcode.com/problems/power-of-heroes/

You are given a 0-indexed integer array nums representing the strength of some
heroes. The power of a group of heroes is defined as follows:

Let i_0, i_1, ... ,i_k be the indices of the heroes in a group. Then, the power
of this group is: max(nums[i_0], nums[i_1], ... ,nums[i_k])^2 * min(nums[i_0], nums[i_1], ... ,nums[i_k])

Return the sum of the power of all non-empty groups of heroes possible.
Since the sum could be very large, return it modulo 10^9 + 7.

Example 1:
    Input: nums = [2,1,4]
    Output: 141
    Explanation:
    - [2]: power = 2^2 * 2 = 8
    - [1]: power = 1^2 * 1 = 1
    - [4]: power = 4^2 * 4 = 64
    - [2,1]: power = 2^2 * 1 = 4
    - [2,4]: power = 4^2 * 2 = 32
    - [1,4]: power = 4^2 * 1 = 16
    - [2,1,4]: power = 4^2 * 1 = 16
    Total = 8 + 1 + 64 + 4 + 32 + 16 + 16 = 141

Example 2:
    Input: nums = [1,1,1]
    Output: 7

Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^9

Topics: Array, Math, Dynamic Programming, Prefix Sum, Sorting
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "sumOfPower",
        "complexity": "O(n log n) time, O(1) space",
        "description": "Sorted iteration with contribution tracking",
    },
}


# ============================================================================
# Solution: Sorted Iteration with Contribution Tracking
# Time: O(n log n), Space: O(1)
#
# Key insight: After sorting in ascending order, for element at position i:
# - nums[i] is the MAX of all groups containing only elements from [0..i]
# - For each previous element nums[j] (j < i) as the MIN:
#   - Elements between j and i (exclusive) can be included or excluded
#   - That gives 2^(i-j-1) different groups
#   - Each contributes: nums[i]^2 * nums[j]
#
# Define s_i = sum(nums[j] * 2^(i-j-1) for j < i)
# Then: s_{i+1} = 2 * s_i + nums[i]
#
# Contribution at position i = nums[i]^3 + nums[i]^2 * s_i
# ============================================================================
class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        """
        Calculate sum of powers of all non-empty hero groups.

        After sorting, for each element x:
        - x^3: contribution when x is alone (single-element group)
        - x^2 * s: contribution when x is MAX and previous elements are MIN
          where s = sum(prev_element * 2^(distance)) accounts for all subsets

        The recurrence s = 2*s + x doubles previous contributions (each prev
        subset can include or exclude x) and adds x for future iterations.

        Args:
            nums: Array of hero strengths

        Returns:
            Sum of powers of all groups modulo 10^9 + 7
        """
        MOD = 10**9 + 7

        nums.sort()

        result = 0
        s = 0  # Weighted sum: sum(nums[j] * 2^(i-j-1) for j < i)

        for x in nums:
            # x^3: single-element contribution
            # x^2 * s: x is max, previous elements contribute as potential mins
            result = (result + x * x % MOD * x % MOD + x * x % MOD * s % MOD) % MOD

            # Update s for next iteration: s = 2*s + x
            # - 2*s: double previous contributions (include/exclude x)
            # - x: current element can be min for future max elements
            s = (2 * s % MOD + x) % MOD

        return result


def solve():
    """
    Input format:
    Line 1: nums (JSON array of integers)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.sumOfPower(nums)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

"""
Problem: Maximum Strength of a Group
Link: https://leetcode.com/problems/maximum-strength-of-a-group/

Find maximum product of any non-empty subset of the array.
Return the maximum strength (product).

Constraints:
- 1 <= nums.length <= 13
- -9 <= nums[i] <= 9

Topics: Array, Greedy, Sorting
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "maxStrength",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Greedy: use all positives, pair negatives by magnitude",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int]) -> int:
    """Reference implementation using subset enumeration."""
    n = len(nums)
    max_strength = float('-inf')

    # Try all non-empty subsets
    for mask in range(1, 1 << n):
        product = 1
        for i in range(n):
            if mask & (1 << i):
                product *= nums[i]
        max_strength = max(max_strength, product)

    return max_strength


def judge(actual, expected, input_data: str) -> bool:
    import json
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(nums)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Greedy with Sorting
# Time: O(n log n), Space: O(n)
# ============================================================================
class Solution:
    # Key insight:
    #   - Positive numbers always increase product (include all)
    #   - Negative numbers: pair them (neg * neg = pos)
    #   - Sort negatives by absolute value, include largest pairs
    #   - Zero: skip unless we need it to avoid negative result
    #
    # Cases:
    #   1. If product can be positive, return it
    #   2. If only negatives and zeros, return 0 (if any zero exists)
    #   3. If single negative, return it (must pick at least one)
    #
    # Greedy: Include all positives and even number of largest-magnitude negatives

    def maxStrength(self, nums: List[int]) -> int:
        positives = [x for x in nums if x > 0]
        negatives = [x for x in nums if x < 0]
        zeros = [x for x in nums if x == 0]

        # Sort negatives by absolute value descending
        negatives.sort(key=lambda x: -abs(x))

        # Start with product of all positives (1 if none)
        product = 1
        has_positive = len(positives) > 0

        for p in positives:
            product *= p

        # Include pairs of negatives (they make positive product)
        pairs = len(negatives) // 2
        for i in range(pairs * 2):
            product *= negatives[i]
            has_positive = True  # We have positive contribution now

        # Edge cases
        if has_positive:
            return product

        # No positives and no pairs of negatives
        # Options: single negative, or zero
        if zeros:
            return 0

        # Must pick something - only option is single negative
        return max(negatives) if negatives else 0


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)

    Example:
        [3,-1,-5,2,5,-9]
        -> 1350
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.maxStrength(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

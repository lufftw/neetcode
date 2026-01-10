"""
Problem: Non-decreasing Array
Link: https://leetcode.com/problems/non-decreasing-array/

Check if array can become non-decreasing by modifying at most one element.
Return true if possible, false otherwise.

Constraints:
- 1 <= nums.length <= 10^4
- -10^5 <= nums[i] <= 10^5

Topics: Array, Greedy
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "checkPossibility",
        "complexity": "O(n) time, O(1) space",
        "description": "Single pass greedy with violation counting",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int]) -> bool:
    """Reference implementation."""
    n = len(nums)
    if n <= 2:
        return True

    # Count violations where nums[i] > nums[i+1]
    violations = []
    for i in range(n - 1):
        if nums[i] > nums[i + 1]:
            violations.append(i)

    if len(violations) == 0:
        return True
    if len(violations) > 1:
        return False

    # Exactly one violation at index i
    i = violations[0]

    # Option 1: Lower nums[i] to nums[i+1]
    # Valid if i == 0 or nums[i-1] <= nums[i+1]
    if i == 0 or nums[i - 1] <= nums[i + 1]:
        return True

    # Option 2: Raise nums[i+1] to nums[i]
    # Valid if i+1 == n-1 or nums[i] <= nums[i+2]
    if i + 1 == n - 1 or nums[i] <= nums[i + 2]:
        return True

    return False


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
# Solution: Single Pass Greedy
# Time: O(n), Space: O(1)
# ============================================================================
class Solution:
    # Key insight:
    #   - Find all violations where nums[i] > nums[i+1]
    #   - If 0 violations: already non-decreasing
    #   - If 2+ violations: impossible with one change
    #   - If 1 violation at index i: try fixing by either
    #     lowering nums[i] or raising nums[i+1]
    #
    # When to lower nums[i] (preferred to maintain smaller values):
    #   - i == 0 (no left constraint)
    #   - nums[i-1] <= nums[i+1] (won't create new violation)
    #
    # When to raise nums[i+1]:
    #   - i+1 == n-1 (no right constraint)
    #   - nums[i] <= nums[i+2] (won't create new violation)

    def checkPossibility(self, nums: List[int]) -> bool:
        n = len(nums)
        if n <= 2:
            return True

        modified = False
        for i in range(n - 1):
            if nums[i] > nums[i + 1]:
                if modified:
                    # Second violation - impossible
                    return False
                modified = True

                # Try to fix: prefer lowering nums[i]
                if i == 0 or nums[i - 1] <= nums[i + 1]:
                    # Lower nums[i] to nums[i+1]
                    nums[i] = nums[i + 1]
                else:
                    # Must raise nums[i+1] to nums[i]
                    nums[i + 1] = nums[i]

        return True


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)

    Example:
        [4,2,3]
        -> true
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.checkPossibility(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

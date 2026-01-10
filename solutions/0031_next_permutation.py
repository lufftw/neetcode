# solutions/0031_next_permutation.py
"""
Problem: Next Permutation
https://leetcode.com/problems/next-permutation/

Find the next lexicographically greater permutation of nums.
If not possible (descending order), rearrange to lowest (ascending).
Must be in-place with O(1) extra memory.

Key insight: Find rightmost ascending pair, swap with next larger element
from right, then reverse the suffix to get smallest arrangement.

Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100
"""
import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointer",
        "method": "nextPermutation",
        "complexity": "O(n) time, O(1) space",
        "description": "Find pivot, swap, reverse suffix in-place",
    },
}


class SolutionTwoPointer:
    """
    Standard next permutation algorithm.

    WHY: To get next permutation, we need to make the smallest increase.
    Find the rightmost position where we can make an increase (first
    descending element from right), swap it with the smallest larger
    element to its right, then sort the suffix to minimize it.

    HOW:
    1. Find pivot: rightmost index i where nums[i] < nums[i+1]
    2. Find swap target: rightmost index j where nums[j] > nums[i]
    3. Swap nums[i] and nums[j]
    4. Reverse nums[i+1:] to get smallest suffix
    If no pivot exists, array is descending—reverse entire array.
    """

    def nextPermutation(self, nums: List[int]) -> None:
        """
        Modify nums in-place to its next permutation.
        """
        n = len(nums)

        # Step 1: Find the pivot (rightmost ascending adjacent pair)
        # Look for first index from right where nums[i] < nums[i+1]
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        # Step 2: If pivot found, find rightmost element > pivot and swap
        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]

        # Step 3: Reverse the suffix after pivot position
        # This works because suffix is in descending order after step 1 & 2
        left, right = i + 1, n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate next permutation result.
    Since the function modifies in-place and we capture output,
    we need to compute expected from input.
    """
    if isinstance(actual, str):
        actual = json.loads(actual)

    # Compute expected from input
    nums = json.loads(input_data.strip())
    expected_result = _compute_next_permutation(nums)

    return actual == expected_result


def _compute_next_permutation(nums: List[int]) -> List[int]:
    """Compute next permutation for validation."""
    n = len(nums)
    nums = nums.copy()

    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]

    # Reverse suffix
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1

    return nums


JUDGE_FUNC = judge


def solve():
    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    solver.nextPermutation(nums)

    print(json.dumps(nums, separators=(",", ":")))


if __name__ == "__main__":
    solve()

# solutions/0704_binary_search.py
"""
Problem: Binary Search
https://leetcode.com/problems/binary-search/

Given an array of integers nums which is sorted in ascending order, and
an integer target, write a function to search target in nums. If target
exists, return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

Constraints:
- 1 <= nums.length <= 10^4
- -10^4 < nums[i], target < 10^4
- All integers in nums are unique
- nums is sorted in ascending order
"""
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionIterative",
        "method": "search",
        "complexity": "O(log n) time, O(1) space",
        "description": "Classic iterative binary search",
    },
    "recursive": {
        "class": "SolutionRecursive",
        "method": "search",
        "complexity": "O(log n) time, O(log n) space",
        "description": "Recursive binary search with divide and conquer",
    },
}


class SolutionIterative:
    """
    Classic iterative binary search implementation.

    The algorithm maintains a search interval [left, right] and repeatedly
    halves it. At each step, we compare the middle element with target:
    - If equal, we found it
    - If target is smaller, search left half
    - If target is larger, search right half

    Loop terminates when left > right, meaning target doesn't exist.
    This is the textbook implementation taught in algorithms courses.
    """

    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            # Avoid overflow: (left + right) // 2 can overflow in some languages
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                # Target is in right half
                left = mid + 1
            else:
                # Target is in left half
                right = mid - 1

        # Target not found
        return -1


class SolutionRecursive:
    """
    Recursive binary search using divide and conquer paradigm.

    Same algorithm as iterative, but expressed recursively. Each call
    handles a subarray, dividing the problem until base case (empty
    interval or target found).

    Uses O(log n) stack space due to recursion depth. The iterative
    version is preferred in practice for constant space.
    """

    def search(self, nums: List[int], target: int) -> int:
        return self._binary_search(nums, target, 0, len(nums) - 1)

    def _binary_search(
        self, nums: List[int], target: int, left: int, right: int
    ) -> int:
        # Base case: empty interval
        if left > right:
            return -1

        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            return self._binary_search(nums, target, mid + 1, right)
        else:
            return self._binary_search(nums, target, left, mid - 1)


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate binary search result.
    """
    import json

    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0])
    target = json.loads(lines[1])

    # Compute expected using simple search
    expected_result = -1
    for i, num in enumerate(nums):
        if num == target:
            expected_result = i
            break

    return actual == expected_result


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: array and target
    nums = json.loads(lines[0])
    target = json.loads(lines[1])

    # Get solver and search
    solver = get_solver(SOLUTIONS)
    result = solver.search(nums, target)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

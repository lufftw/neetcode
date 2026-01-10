# solutions/0217_contains_duplicate.py
"""
Problem: Contains Duplicate
https://leetcode.com/problems/contains-duplicate/

Given an integer array nums, return true if any value appears at least
twice in the array, and return false if every element is distinct.

Key insight: HashSet lookup is O(1), so we can detect duplicates in O(n).

Constraints:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
"""
import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionHashSet",
        "method": "containsDuplicate",
        "complexity": "O(n) time, O(n) space",
        "description": "HashSet for O(1) lookup while iterating",
    },
    "sorting": {
        "class": "SolutionSorting",
        "method": "containsDuplicate",
        "complexity": "O(n log n) time, O(1) space",
        "description": "Sort then check adjacent elements",
    },
}


class SolutionHashSet:
    """
    HashSet approach.

    WHY: A set provides O(1) average lookup. As we iterate through nums,
    we check if each element was seen before. First duplicate found,
    we return True immediately.

    HOW: Maintain a set of seen values. For each num, if already in set,
    return True. Otherwise add to set. If loop completes, all unique.
    """

    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False


class SolutionSorting:
    """
    Sorting approach.

    WHY: After sorting, duplicates become adjacent. We only need to
    check consecutive pairs. Trades space for time—no extra data structure
    but O(n log n) sort.

    HOW: Sort the array, then scan for any two adjacent equal elements.
    """

    def containsDuplicate(self, nums: List[int]) -> bool:
        nums.sort()
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                return True
        return False


def judge(actual, expected, input_data: str) -> bool:
    """Validate contains duplicate result."""
    if isinstance(actual, str):
        actual = json.loads(actual)

    # Compute expected from input
    nums = json.loads(input_data.strip())
    expected_result = len(nums) != len(set(nums))

    return actual == expected_result


JUDGE_FUNC = judge


def solve():
    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.containsDuplicate(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

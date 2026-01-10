# solutions/0136_single_number.py
"""
Problem: Single Number
https://leetcode.com/problems/single-number/

Given a non-empty array of integers nums, every element appears twice
except for one. Find that single one.

You must implement a solution with O(n) runtime and O(1) extra space.

Constraints:
- 1 <= nums.length <= 3 * 10^4
- -3 * 10^4 <= nums[i] <= 3 * 10^4
- Each element appears twice except for one element which appears once
"""
from typing import List
from functools import reduce
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionXOR",
        "method": "singleNumber",
        "complexity": "O(n) time, O(1) space",
        "description": "XOR all elements; pairs cancel to zero",
    },
    "reduce": {
        "class": "SolutionReduce",
        "method": "singleNumber",
        "complexity": "O(n) time, O(1) space",
        "description": "Functional reduce with XOR operator",
    },
}


class SolutionXOR:
    """
    XOR-based approach exploiting self-inverse property.

    Key XOR properties:
    - a ^ a = 0 (self-inverse)
    - a ^ 0 = a (identity)
    - XOR is commutative and associative

    When we XOR all numbers, pairs cancel to zero, leaving only the
    single number. This achieves O(n) time with O(1) space, which is
    optimal for this problem.
    """

    def singleNumber(self, nums: List[int]) -> int:
        result = 0
        # XOR all elements; paired elements cancel to 0
        # Final result is the unpaired element
        for num in nums:
            result ^= num
        return result


class SolutionReduce:
    """
    Functional approach using reduce with XOR.

    Same algorithm as iterative XOR, expressed functionally. The reduce
    operation folds the array with XOR, equivalent to the explicit loop.

    This is more Pythonic and concise, though the explicit loop may be
    clearer for those unfamiliar with functional programming.
    """

    def singleNumber(self, nums: List[int]) -> int:
        # reduce(xor, [a, b, c, d]) = ((a ^ b) ^ c) ^ d
        return reduce(lambda a, b: a ^ b, nums)


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate single number using XOR.
    """
    import json

    nums = json.loads(input_data.strip())
    expected_result = 0
    for num in nums:
        expected_result ^= num

    return actual == expected_result


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: array
    nums = json.loads(lines[0])

    # Get solver and find single number
    solver = get_solver(SOLUTIONS)
    result = solver.singleNumber(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

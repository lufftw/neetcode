# solutions/0268_missing_number.py
"""
Problem: Missing Number
https://leetcode.com/problems/missing-number/

Given an array nums containing n distinct numbers in the range [0, n],
return the only number in the range that is missing from the array.

Constraints:
- n == nums.length
- 1 <= n <= 10^4
- 0 <= nums[i] <= n
- All the numbers of nums are unique
"""
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionXOR",
        "method": "missingNumber",
        "complexity": "O(n) time, O(1) space",
        "description": "XOR all indices and values for cancellation",
    },
    "sum": {
        "class": "SolutionSum",
        "method": "missingNumber",
        "complexity": "O(n) time, O(1) space",
        "description": "Gauss sum formula minus actual sum",
    },
}


class SolutionXOR:
    """
    XOR-based approach exploiting self-inverse property.

    For complete sequence [0, 1, ..., n], XOR of all numbers equals
    XOR of all indices (0 to n-1) XOR n. In the given array, one
    number is missing. XORing indices (0 to n-1), n, and all array
    values cancels matching pairs, leaving only the missing number.

    This leverages: a XOR a = 0, and a XOR 0 = a.
    """

    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        result = n  # Start with n since we only iterate to n-1

        # XOR index and corresponding value
        # Matching pairs cancel to 0, leaving missing number
        for i in range(n):
            result ^= i ^ nums[i]

        return result


class SolutionSum:
    """
    Arithmetic sum formula approach.

    The sum of 0 + 1 + ... + n equals n*(n+1)/2 (Gauss formula).
    Subtracting the actual sum of array elements gives the missing
    number directly.

    This approach is mathematically elegant but risks integer overflow
    for very large n in some languages. Python handles arbitrary
    precision, so no overflow concern here.
    """

    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        # Gauss formula: sum of 0 to n
        expected_sum = n * (n + 1) // 2
        # Actual sum of array elements
        actual_sum = sum(nums)
        # Difference is the missing number
        return expected_sum - actual_sum


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate missing number using sum formula.
    """
    import json

    nums = json.loads(input_data.strip())
    n = len(nums)
    expected_result = n * (n + 1) // 2 - sum(nums)

    return actual == expected_result


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: array
    nums = json.loads(lines[0])

    # Get solver and find missing number
    solver = get_solver(SOLUTIONS)
    result = solver.missingNumber(nums)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

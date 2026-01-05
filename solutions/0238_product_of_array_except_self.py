"""
Problem: Product of Array Except Self
Link: https://leetcode.com/problems/product-of-array-except-self/

Given an integer array nums, return an array answer such that answer[i] is
equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit
integer.

You must write an algorithm that runs in O(n) time and without using the
division operation.

Example 1:
    Input: nums = [1,2,3,4]
    Output: [24,12,8,6]

Example 2:
    Input: nums = [-1,1,0,-3,3]
    Output: [0,0,9,0,0]

Constraints:
- 2 <= nums.length <= 10^5
- -30 <= nums[i] <= 30
- The product of any prefix or suffix of nums is guaranteed to fit in a
  32-bit integer.

Follow up: Can you solve the problem in O(1) extra space complexity? (The
output array does not count as extra space for space complexity analysis.)

Topics: Array, Prefix Sum
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionPrefixSuffix",
        "method": "productExceptSelf",
        "complexity": "O(n) time, O(1) space",
        "description": "Left-to-right prefix, right-to-left suffix in single output array",
    },
    "prefix_suffix": {
        "class": "SolutionPrefixSuffix",
        "method": "productExceptSelf",
        "complexity": "O(n) time, O(1) space",
        "description": "Left-to-right prefix, right-to-left suffix in single output array",
    },
    "two_pass": {
        "class": "SolutionTwoArrays",
        "method": "productExceptSelf",
        "complexity": "O(n) time, O(n) space",
        "description": "Separate prefix and suffix product arrays",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate result: product array."""
    lines = input_data.strip().split("\n")
    nums = json.loads(lines[0])

    correct = _reference_product_except_self(nums)

    if isinstance(actual, list):
        return actual == correct

    try:
        actual_list = json.loads(str(actual).strip())
        return actual_list == correct
    except (ValueError, json.JSONDecodeError):
        return False


def _reference_product_except_self(nums: List[int]) -> List[int]:
    """O(n) reference using prefix/suffix products."""
    n = len(nums)
    result = [1] * n

    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Optimized Prefix/Suffix (O(1) Extra Space)
# Time: O(n), Space: O(1) excluding output
#   - First pass: Build prefix products directly in result array
#   - Second pass: Multiply by suffix products using single variable
#   - Avoids division operation as required by problem constraints
#
# Key Insight: product_except_self[i] = prefix_product[0..i-1] * suffix_product[i+1..n-1]
# This is similar to prefix sum but with multiplication instead of addition.
#
# Pattern: prefix_suffix_product
# See: docs/patterns/prefix_sum/templates.md Section 6 (Prefix/Suffix Products)
# ============================================================================
class SolutionPrefixSuffix:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Compute product of array except self without division.

        Two-pass approach:
        1. Left-to-right: result[i] = product of elements before i
        2. Right-to-left: multiply result[i] by product of elements after i
        """
        array_length = len(nums)
        result = [1] * array_length

        # Pass 1: Build prefix products
        # After this pass, result[i] = product of nums[0..i-1]
        prefix_product = 1
        for index in range(array_length):
            result[index] = prefix_product
            prefix_product *= nums[index]

        # Pass 2: Multiply by suffix products
        # After this pass, result[i] = prefix[0..i-1] * suffix[i+1..n-1]
        suffix_product = 1
        for index in range(array_length - 1, -1, -1):
            result[index] *= suffix_product
            suffix_product *= nums[index]

        return result


# ============================================================================
# Solution 2: Two Separate Arrays (Educational)
# Time: O(n), Space: O(n)
#   - Build separate prefix and suffix product arrays
#   - More intuitive and easier to understand
#   - Shows the concept clearly before space optimization
#
# Educational Value: Use this to understand the concept, then optimize.
# ============================================================================
class SolutionTwoArrays:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Compute product of array except self using explicit prefix/suffix arrays.

        This version uses O(n) extra space but is easier to understand.
        """
        array_length = len(nums)

        # prefix_product[i] = product of nums[0..i-1]
        prefix_product = [1] * array_length
        for i in range(1, array_length):
            prefix_product[i] = prefix_product[i - 1] * nums[i - 1]

        # suffix_product[i] = product of nums[i+1..n-1]
        suffix_product = [1] * array_length
        for i in range(array_length - 2, -1, -1):
            suffix_product[i] = suffix_product[i + 1] * nums[i + 1]

        # result[i] = prefix_product[i] * suffix_product[i]
        return [prefix_product[i] * suffix_product[i] for i in range(array_length)]


def solve():
    """
    Input format (JSON per line):
        Line 1: nums as JSON array

    Output format:
        JSON array of products
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.productExceptSelf(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

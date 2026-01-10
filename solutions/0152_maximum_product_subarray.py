"""
Problem: Maximum Product Subarray
Link: https://leetcode.com/problems/maximum-product-subarray/

Given an integer array nums, find a subarray that has the largest product,
and return the product.

The test cases are generated so that the answer will fit in a 32-bit integer.

Example 1:
    Input: nums = [2,3,-2,4]
    Output: 6
    Explanation: [2,3] has the largest product 6.

Example 2:
    Input: nums = [-2,0,-1]
    Output: 0
    Explanation: The result cannot be 2, because [-2,-1] is not a subarray.

Constraints:
- 1 <= nums.length <= 2 * 10^4
- -10 <= nums[i] <= 10
- The product of any prefix or suffix of nums fits in a 32-bit integer.

Topics: Array, Dynamic Programming
"""
import json
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionMinMax",
        "method": "maxProduct",
        "complexity": "O(n) time, O(1) space",
        "description": "Track both min and max products at each position",
    },
    "minmax": {
        "class": "SolutionMinMax",
        "method": "maxProduct",
        "complexity": "O(n) time, O(1) space",
        "description": "Track both min and max products",
    },
    "prefix_suffix": {
        "class": "SolutionPrefixSuffix",
        "method": "maxProduct",
        "complexity": "O(n) time, O(1) space",
        "description": "Prefix and suffix products from both directions",
    },
}


# ============================================================================
# Solution 1: Track Min and Max Products
# Time: O(n), Space: O(1)
#   - Unlike sum, negative * negative = positive
#   - Track both min and max product ending at each position
#   - Negative number can turn min into new max
# ============================================================================
class SolutionMinMax:
    """
    Track both minimum and maximum product ending at each position.

    Key insight: Unlike Maximum Subarray (sum), with products a negative
    number can flip min to max. So we track both.

    At each position i:
    - max_prod = max(nums[i], max_prod * nums[i], min_prod * nums[i])
    - min_prod = min(nums[i], max_prod * nums[i], min_prod * nums[i])

    The answer is the maximum max_prod seen.

    Critical: When nums[i] is negative, it swaps max and min roles.
    """

    def maxProduct(self, nums: List[int]) -> int:
        if not nums:
            return 0

        # Track max and min products ending at current position
        max_prod = nums[0]
        min_prod = nums[0]
        result = nums[0]

        for i in range(1, len(nums)):
            curr = nums[i]

            # If current is negative, swap max and min (they'll swap roles)
            if curr < 0:
                max_prod, min_prod = min_prod, max_prod

            # Update max and min products ending at current position
            max_prod = max(curr, max_prod * curr)
            min_prod = min(curr, min_prod * curr)

            # Update global maximum
            result = max(result, max_prod)

        return result


# ============================================================================
# Solution 2: Prefix and Suffix Products
# Time: O(n), Space: O(1)
#   - Maximum product subarray is either:
#     - A prefix from start (reset at zeros)
#     - A suffix from end (reset at zeros)
#   - Compute products from both directions
# ============================================================================
class SolutionPrefixSuffix:
    """
    Compute prefix and suffix products, resetting at zeros.

    Key insight: The maximum product subarray must be either:
    1. A prefix of the array (possibly after skipping first negative)
    2. A suffix of the array (possibly before the last negative)

    Why? If there are no zeros, with even negatives we want the whole array.
    With odd negatives, we want to exclude either the leftmost or rightmost
    negative (whichever gives larger product).

    Zeros split the array into independent subarrays.

    We compute prefix products left-to-right and suffix products right-to-left,
    resetting to 1 after each zero.
    """

    def maxProduct(self, nums: List[int]) -> int:
        n = len(nums)
        result = nums[0]

        # Prefix product (left to right)
        prefix = 1
        for i in range(n):
            prefix *= nums[i]
            result = max(result, prefix)
            if prefix == 0:
                prefix = 1

        # Suffix product (right to left)
        suffix = 1
        for i in range(n - 1, -1, -1):
            suffix *= nums[i]
            result = max(result, suffix)
            if suffix == 0:
                suffix = 1

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums as JSON array

    Example:
        [2,3,-2,4]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.maxProduct(nums)

    print(result)


if __name__ == "__main__":
    solve()

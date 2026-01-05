"""
Problem: Next Greater Element II
Link: https://leetcode.com/problems/next-greater-element-ii/

Given a circular integer array nums (i.e., the next element of nums[nums.length - 1] is nums[0]), return the next greater number for every element in nums.
The next greater number of a number x is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn't exist, return -1 for this number.

Example 1:
    Input: nums = [1,2,1]
    Output: [2,-1,2]
Explanation: The first 1's next greater number is 2; 
The number 2 can't find next greater number. 
The second 1's next greater number needs to search circularly, which is also 2.

Example 2:
    Input: nums = [1,2,3,4,3]
    Output: [2,3,4,-1,4]

Constraints:
- 1 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9

Topics: Array, Stack, Monotonic Stack
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionCircularTwoPass",
        "method": "nextGreaterElements",
        "complexity": "O(n) time, O(n) space",
        "description": "Two-pass circular traversal with modulo indexing",
    },
    "twopass": {
        "class": "SolutionCircularTwoPass",
        "method": "nextGreaterElements",
        "complexity": "O(n) time, O(n) space",
        "description": "Two-pass circular traversal with modulo indexing",
    },
    "concat": {
        "class": "SolutionDoubleArray",
        "method": "nextGreaterElements",
        "complexity": "O(n) time, O(n) space",
        "description": "Conceptual array doubling (virtual concatenation)",
    },
}


# ============================================================================
# Solution 1: Two-Pass Circular Traversal
# Time: O(n), Space: O(n)
#   - Traverse the array twice (2n iterations) to simulate circular wrap
#   - Use modulo arithmetic: index % n maps virtual indices to real indices
#   - Only push indices during first pass (indices 0 to n-1)
#   - Second pass allows resolving elements that wrap around
#
# Key Insight: A circular array is equivalent to processing the array twice.
# The second pass provides the "wrap-around" elements for unresolved candidates.
# ============================================================================
class SolutionCircularTwoPass:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        array_length = len(nums)
        next_greater_result = [-1] * array_length
        candidate_stack: list[int] = []  # Stores indices awaiting resolution

        # Process array twice: first pass builds candidates, second resolves wraps
        for virtual_idx in range(2 * array_length):
            actual_idx = virtual_idx % array_length
            current_value = nums[actual_idx]

            # Resolve all candidates whose next greater element is current_value
            while candidate_stack and nums[candidate_stack[-1]] < current_value:
                resolved_idx = candidate_stack.pop()
                next_greater_result[resolved_idx] = current_value

            # Only add new candidates during the first pass
            # Second pass is purely for resolving wrap-around cases
            if virtual_idx < array_length:
                candidate_stack.append(actual_idx)

        return next_greater_result


# ============================================================================
# Solution 2: Virtual Array Doubling
# Time: O(n), Space: O(n)
#   - Conceptually double the array: [a, b, c] becomes [a, b, c, a, b, c]
#   - Standard NGE on doubled array, but only store results for first n elements
#   - More intuitive for understanding, same complexity as two-pass
#
# Trade-off: Slightly more memory for intermediate processing, but clearer logic.
# ============================================================================
class SolutionDoubleArray:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        array_length = len(nums)
        next_greater_result = [-1] * array_length
        candidate_stack: list[int] = []

        # Create virtual doubled array via modulo access
        doubled_length = 2 * array_length

        for i in range(doubled_length):
            actual_idx = i % array_length
            current_value = nums[actual_idx]

            # Standard NGE resolution
            while candidate_stack and nums[candidate_stack[-1]] < current_value:
                resolved_idx = candidate_stack.pop()
                # Only update if this is a real index (from first pass)
                if resolved_idx < array_length:
                    next_greater_result[resolved_idx] = current_value

            # Track all indices (modulo will handle duplicates naturally)
            candidate_stack.append(actual_idx)

        return next_greater_result


def solve():
    """
    Input format (JSON):
        Line 1: nums as JSON array

    Output format:
        JSON array of next greater elements (circular)
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.nextGreaterElements(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

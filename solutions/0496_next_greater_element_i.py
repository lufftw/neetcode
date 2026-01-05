"""
Problem: Next Greater Element I
Link: https://leetcode.com/problems/next-greater-element-i/

The next greater element of some element x in an array is the first greater
element that is to the right of x in the same array.

Given two distinct 0-indexed integer arrays nums1 and nums2, where nums1 is
a subset of nums2, for each element in nums1, find its next greater element
in nums2 and return the results.

Constraints:
- 1 <= nums1.length <= nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 10^4
- All integers in nums1 and nums2 are unique
- All integers of nums1 also appear in nums2

Topics: Array, Hash Table, Stack, Monotonic Stack
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionMonotonicStack",
        "method": "nextGreaterElement",
        "complexity": "O(n + m) time, O(n) space",
        "description": "Monotonic decreasing stack with hash map lookup",
    },
    "stack": {
        "class": "SolutionMonotonicStack",
        "method": "nextGreaterElement",
        "complexity": "O(n + m) time, O(n) space",
        "description": "Monotonic decreasing stack with hash map lookup",
    },
    "brute": {
        "class": "SolutionBruteForce",
        "method": "nextGreaterElement",
        "complexity": "O(m * n) time, O(1) space",
        "description": "Linear scan for each query element",
    },
}


# ============================================================================
# Solution 1: Monotonic Decreasing Stack + Hash Map
# Time: O(n + m), Space: O(n)
#   - Precompute NGE for all elements in nums2 using monotonic stack
#   - Stack stores indices of candidates awaiting their next greater element
#   - When a larger element appears, it becomes NGE for all smaller candidates
#   - Hash map enables O(1) lookup for nums1 queries
#
# Key Insight: The stack maintains a decreasing sequence of unresolved elements.
# When we encounter a larger element, it "resolves" all smaller elements on top.
# ============================================================================
class SolutionMonotonicStack:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        next_greater_map: dict[int, int] = {}
        candidate_stack: list[int] = []  # Stores values (not indices) since unique

        # Build NGE map: process nums2 to find next greater for each element
        for current_value in nums2:
            # Resolve all candidates that found their next greater element
            while candidate_stack and candidate_stack[-1] < current_value:
                resolved_value = candidate_stack.pop()
                next_greater_map[resolved_value] = current_value

            # Current element becomes a new candidate awaiting its NGE
            candidate_stack.append(current_value)

        # Elements remaining in stack have no next greater element
        # They will return -1 via dict.get() default

        # Look up NGE for each query element
        return [next_greater_map.get(query, -1) for query in nums1]


# ============================================================================
# Solution 2: Brute Force Linear Scan
# Time: O(m * n), Space: O(1)
#   - For each element in nums1, find its position in nums2
#   - Scan right from that position to find the first greater element
#   - Simple but inefficient for large inputs
#
# Educational Value: Establishes baseline before optimization.
# ============================================================================
class SolutionBruteForce:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result: list[int] = []
        nums2_length = len(nums2)

        for query in nums1:
            # Find position of query element in nums2
            position = nums2.index(query)

            # Scan rightward for next greater element
            next_greater = -1
            for scan_idx in range(position + 1, nums2_length):
                if nums2[scan_idx] > query:
                    next_greater = nums2[scan_idx]
                    break

            result.append(next_greater)

        return result


def solve():
    """
    Input format (JSON per line):
        Line 1: nums1 as JSON array
        Line 2: nums2 as JSON array

    Output format:
        JSON array of next greater elements
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums1 = json.loads(lines[0])
    nums2 = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.nextGreaterElement(nums1, nums2)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

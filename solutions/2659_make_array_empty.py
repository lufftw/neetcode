"""
Problem: Make Array Empty
Link: https://leetcode.com/problems/make-array-empty/

Count operations to empty array: remove first if smallest, else move to end.
All elements are distinct.

Constraints:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- All values distinct

Topics: Array, Sorting, Greedy
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "countOperationsToEmptyArray",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Sort by value, count wrap-arounds",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int]) -> int:
    """O(n^2) simulation for small inputs."""
    if len(nums) > 1000:
        return None  # Too slow

    from collections import deque
    q = deque(nums)
    ops = 0

    while q:
        if q[0] == min(q):
            q.popleft()
        else:
            q.append(q.popleft())
        ops += 1

    return ops


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    ref = _reference(nums)
    if ref is not None:
        return actual == ref
    return isinstance(actual, int) and actual >= len(nums)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Sort and Count Wrap-arounds
# Time: O(n log n), Space: O(n)
# ============================================================================
class Solution:
    # Key insight:
    #   - Elements are removed in sorted order (smallest first)
    #   - Each removal costs 1 operation
    #   - Moving from index A to index B (in sorted removal order):
    #     - If B > A: just move forward, no wrap
    #     - If B < A: wrap around, passing all remaining elements once
    #
    # Formula:
    #   result = n + sum((n - i) for inversions in sorted indices)
    #
    # An inversion occurs when sorted_idx[i] < sorted_idx[i-1]
    # Each inversion adds (n - i) = number of remaining elements

    def countOperationsToEmptyArray(self, nums: List[int]) -> int:
        n = len(nums)

        # Get indices sorted by value
        sorted_indices = sorted(range(n), key=lambda i: nums[i])

        # Base: n operations for n removals
        result = n

        # Add cost for each wrap-around
        for i in range(1, n):
            if sorted_indices[i] < sorted_indices[i - 1]:
                # Wrap-around: pass through (n - i) remaining elements
                result += n - i

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)

    Example:
        [3,4,-1]
        -> 5
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.countOperationsToEmptyArray(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

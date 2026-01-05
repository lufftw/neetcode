"""
Problem: Sum of Subarray Minimums
Link: https://leetcode.com/problems/sum-of-subarray-minimums/

Given an array of integers arr, find the sum of min(b), where b ranges over every (contiguous) subarray of arr. Since the answer may be large, return the answer modulo 109 + 7.

Example 1:
    Input: arr = [3,1,2,4]
    Output: 17
    Explanation: Subarrays are [3], [1], [2], [4], [3,1], [1,2], [2,4], [3,1,2], [1,2,4], [3,1,2,4]. 
                 Minimums are 3, 1, 2, 4, 1, 1, 2, 1, 1, 1.
                 Sum is 17.

Example 2:
    Input: arr = [11,81,94,43,3]
    Output: 444

Constraints:
- 1 <= arr.length <= 3 * 10^4
- 1 <= arr[i] <= 3 * 10^4

Topics: Array, Dynamic Programming, Stack, Monotonic Stack
"""


from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionContributionCounting",
        "method": "sumSubarrayMins",
        "complexity": "O(n) time, O(n) space",
        "description": "Contribution counting with asymmetric boundaries",
    },
    "contribution": {
        "class": "SolutionContributionCounting",
        "method": "sumSubarrayMins",
        "complexity": "O(n) time, O(n) space",
        "description": "Contribution counting with asymmetric boundaries",
    },
    "single": {
        "class": "SolutionSinglePass",
        "method": "sumSubarrayMins",
        "complexity": "O(n) time, O(n) space",
        "description": "Single-pass with on-pop contribution calculation",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is the correct sum mod 10^9+7.

    Args:
        actual: Program output (integer as string or int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (JSON array)

    Returns:
        bool: True if correct sum of subarray minimums
    """
    import json
    line = input_data.strip()
    arr = json.loads(line) if line else []

    # Compute correct answer using reference solution
    correct = _reference_sum_subarray_mins(arr)

    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _reference_sum_subarray_mins(arr: List[int]) -> int:
    """O(n) reference using contribution counting."""
    MOD = 10**9 + 7
    n = len(arr)
    if n == 0:
        return 0

    # Find previous less element (strictly less for left boundary)
    left = [0] * n
    stack: list[int] = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    # Find next less element (less or equal for right boundary - handles duplicates)
    right = [0] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)

    # Contribution of each element
    result = 0
    for i in range(n):
        result = (result + arr[i] * left[i] * right[i]) % MOD

    return result


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Contribution Counting with Boundary Precomputation
# Time: O(n), Space: O(n)
#   - For each element, find left/right boundaries using monotonic stack
#   - Contribution of arr[i] = arr[i] * left_count * right_count
#   - left_count = subarrays where arr[i] is minimum extending left
#   - right_count = subarrays where arr[i] is minimum extending right
#
# Key Insight: Each element contributes to exactly (left * right) subarrays
# as the minimum. Asymmetric tie-breaking (< for left, <= for right) ensures
# each subarray is counted exactly once when duplicates exist.
# ============================================================================
class SolutionContributionCounting:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        MOD = 10**9 + 7
        array_length = len(arr)

        # left_distance[i] = distance to previous strictly smaller element
        left_distance = [0] * array_length
        # right_distance[i] = distance to next smaller-or-equal element
        right_distance = [0] * array_length

        # Compute left boundaries (previous strictly smaller)
        index_stack: list[int] = []
        for i in range(array_length):
            # Pop while stack top >= current (strict < for left boundary)
            while index_stack and arr[index_stack[-1]] >= arr[i]:
                index_stack.pop()
            left_distance[i] = i - index_stack[-1] if index_stack else i + 1
            index_stack.append(i)

        # Compute right boundaries (next smaller or equal)
        index_stack = []
        for i in range(array_length - 1, -1, -1):
            # Pop while stack top > current (non-strict for right boundary)
            while index_stack and arr[index_stack[-1]] > arr[i]:
                index_stack.pop()
            right_distance[i] = index_stack[-1] - i if index_stack else array_length - i
            index_stack.append(i)

        # Sum contributions: element * left_count * right_count
        total_sum = 0
        for i in range(array_length):
            contribution = arr[i] * left_distance[i] * right_distance[i]
            total_sum = (total_sum + contribution) % MOD

        return total_sum


# ============================================================================
# Solution 2: Single-Pass with On-Pop Contribution
# Time: O(n), Space: O(n)
#   - Process left-to-right, compute contribution when element is popped
#   - When popped, we know both left boundary (remaining stack top) and
#     right boundary (current element)
#   - Append sentinel 0 to force complete stack flush
#
# Trade-off: More elegant single-pass, but contribution formula is computed
# at pop time which can be less intuitive than precomputation.
# ============================================================================
class SolutionSinglePass:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        MOD = 10**9 + 7
        arr_with_sentinel = arr + [0]  # Sentinel forces all pops
        total_sum = 0

        # Stack stores (index, accumulated_sum) for efficient contribution
        # Alternative: just store indices and compute on pop
        index_stack: list[int] = [-1]  # Virtual left boundary

        for current_idx, current_val in enumerate(arr_with_sentinel):
            while index_stack[-1] != -1 and arr[index_stack[-1]] > current_val:
                popped_idx = index_stack.pop()
                popped_val = arr[popped_idx]

                left_boundary = index_stack[-1]
                left_count = popped_idx - left_boundary
                right_count = current_idx - popped_idx

                contribution = popped_val * left_count * right_count
                total_sum = (total_sum + contribution) % MOD

            index_stack.append(current_idx)

        return total_sum


def solve():
    """
    Input format (JSON literal, one per line):
        arr: List[int]

    Output: int
    """
    import sys
    import json

    data = sys.stdin.read().strip().split('\n')

    arr = json.loads(data[0].strip())

    solver = get_solver(SOLUTIONS)
    result = solver.sumSubarrayMins(arr)

    print(result)


if __name__ == "__main__":
    solve()

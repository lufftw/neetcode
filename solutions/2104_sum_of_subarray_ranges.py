"""
Problem: Sum of Subarray Ranges
Link: https://leetcode.com/problems/sum-of-subarray-ranges/

You are given an integer array nums. The range of a subarray of nums is the difference between the largest and smallest element in the subarray.
Return the sum of all subarray ranges of nums.
A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:
    Input: nums = [1,2,3]
    Output: 4
    Explanation: The 6 subarrays of nums are the following:
                 [1], range = largest - smallest = 1 - 1 = 0
                 [2], range = 2 - 2 = 0
                 [3], range = 3 - 3 = 0
                 [1,2], range = 2 - 1 = 1
                 [2,3], range = 3 - 2 = 1
                 [1,2,3], range = 3 - 1 = 2
                 So the sum of all ranges is 0 + 0 + 0 + 1 + 1 + 2 = 4.

Example 2:
    Input: nums = [1,3,3]
    Output: 4
    Explanation: The 6 subarrays of nums are the following:
                 [1], range = largest - smallest = 1 - 1 = 0
                 [3], range = 3 - 3 = 0
                 [3], range = 3 - 3 = 0
                 [1,3], range = 3 - 1 = 2
                 [3,3], range = 3 - 3 = 0
                 [1,3,3], range = 3 - 1 = 2
                 So the sum of all ranges is 0 + 0 + 0 + 2 + 0 + 2 = 4.

Example 3:
    Input: nums = [4,-2,-3,4,1]
    Output: 59
    Explanation: The sum of all subarray ranges of nums is 59.

Constraints:
- 1 <= nums.length <= 1000
- -10^9 <= nums[i] <= 10^9

Topics: Array, Stack, Monotonic Stack

Hint 1: Can you get the max/min of a certain subarray by using the max/min of a smaller subarray within it?

Hint 2: Notice that the max of the subarray from index i to j is equal to max of (max of the subarray from index i to j-1) and nums[j].

Follow-up: Could you find a solution with O(n) time complexity?
"""


from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionMonotonicStack",
        "method": "subArrayRanges",
        "complexity": "O(n) time, O(n) space",
        "description": "Sum of maxs - sum of mins via dual monotonic stacks",
    },
    "stack": {
        "class": "SolutionMonotonicStack",
        "method": "subArrayRanges",
        "complexity": "O(n) time, O(n) space",
        "description": "Sum of maxs - sum of mins via dual monotonic stacks",
    },
    "brute": {
        "class": "SolutionBruteForce",
        "method": "subArrayRanges",
        "complexity": "O(n^2) time, O(1) space",
        "description": "Enumerate all subarrays and track running min/max",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is the correct sum of ranges.

    Args:
        actual: Program output (integer as string or int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (JSON array)

    Returns:
        bool: True if correct sum of subarray ranges
    """
    import json
    line = input_data.strip()
    nums = json.loads(line) if line else []

    # Compute correct answer using reference solution
    correct = _reference_subarray_ranges(nums)

    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _reference_subarray_ranges(nums: List[int]) -> int:
    """O(n^2) reference using brute force for verification."""
    n = len(nums)
    result = 0

    for i in range(n):
        min_val = max_val = nums[i]
        for j in range(i, n):
            min_val = min(min_val, nums[j])
            max_val = max(max_val, nums[j])
            result += max_val - min_val

    return result


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Dual Monotonic Stacks (Contribution Counting)
# Time: O(n), Space: O(n)
#   - Range sum = sum of all subarray maxs - sum of all subarray mins
#   - Use contribution counting for both max and min separately
#   - Each element's max contribution = value * left_count * right_count
#     (where left/right count subarrays where element is the maximum)
#
# Key Insight: Decompose range(max - min) into two independent sums.
# Reuse the same asymmetric boundary technique for both max and min counting.
# ============================================================================
class SolutionMonotonicStack:
    def subArrayRanges(self, nums: List[int]) -> int:
        array_length = len(nums)

        def compute_contribution_sum(find_max: bool) -> int:
            """
            Compute sum of contributions for all elements.
            find_max=True: sum of all subarray maximums
            find_max=False: sum of all subarray minimums
            """
            left_distance = [0] * array_length
            right_distance = [0] * array_length

            # Comparison functions based on whether we're finding max or min
            def dominates(a: int, b: int) -> bool:
                return a > b if find_max else a < b

            def dominates_or_equal(a: int, b: int) -> bool:
                return a >= b if find_max else a <= b

            # Compute left boundaries (previous dominating element)
            index_stack: list[int] = []
            for i in range(array_length):
                while index_stack and dominates_or_equal(nums[i], nums[index_stack[-1]]):
                    index_stack.pop()
                left_distance[i] = i - index_stack[-1] if index_stack else i + 1
                index_stack.append(i)

            # Compute right boundaries (next dominating element)
            index_stack = []
            for i in range(array_length - 1, -1, -1):
                while index_stack and dominates(nums[i], nums[index_stack[-1]]):
                    index_stack.pop()
                right_distance[i] = index_stack[-1] - i if index_stack else array_length - i
                index_stack.append(i)

            # Sum all contributions
            total = 0
            for i in range(array_length):
                total += nums[i] * left_distance[i] * right_distance[i]
            return total

        sum_of_maximums = compute_contribution_sum(find_max=True)
        sum_of_minimums = compute_contribution_sum(find_max=False)

        return sum_of_maximums - sum_of_minimums


# ============================================================================
# Solution 2: Brute Force with Running Min/Max
# Time: O(n^2), Space: O(1)
#   - Enumerate all subarrays by fixing left endpoint
#   - Extend right endpoint while tracking running min and max
#   - Accumulate (max - min) for each subarray
#
# Educational Value: Simple baseline showing O(n^2) can still be efficient
# for n <= 1000. Good for verification and understanding.
# ============================================================================
class SolutionBruteForce:
    def subArrayRanges(self, nums: List[int]) -> int:
        array_length = len(nums)
        total_range_sum = 0

        for left in range(array_length):
            running_min = nums[left]
            running_max = nums[left]

            for right in range(left, array_length):
                running_min = min(running_min, nums[right])
                running_max = max(running_max, nums[right])
                total_range_sum += running_max - running_min

        return total_range_sum


def solve():
    """
    Input format (JSON literal, one per line):
        nums: List[int]

    Output: int
    """
    import sys
    import json

    data = sys.stdin.read().strip().split('\n')

    nums = json.loads(data[0].strip())

    solver = get_solver(SOLUTIONS)
    result = solver.subArrayRanges(nums)

    print(result)


if __name__ == "__main__":
    solve()

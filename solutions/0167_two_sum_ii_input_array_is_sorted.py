# solutions/0167_two_sum_ii_input_array_is_sorted.py
"""
Problem: Two Sum II - Input Array Is Sorted
Link: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.
Return the indices of the two numbers, index1 and index2, added by one as an integer array [index1, index2] of length 2.
The tests are generated such that there is exactly one solution. You may not use the same element twice.
Your solution must use only constant extra space.

Example 1:
    Input: numbers = [2,7,11,15], target = 9
    Output: [1,2]
    Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].

Example 2:
    Input: numbers = [2,3,4], target = 6
    Output: [1,3]
    Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].

Example 3:
    Input: numbers = [-1,0], target = -1
    Output: [1,2]
    Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].

Constraints:
- 2 <= numbers.length <= 3 * 10^4
- -1000 <= numbers[i] <= 1000
- numbers is sorted in non-decreasing order.
- -1000 <= target <= 1000
- The tests are generated such that there is exactly one solution.

Topics: Array, Two Pointers, Binary Search
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",
        "method": "twoSum",
        "complexity": "O(n) time, O(1) space",
        "description": "Opposite pointers exploiting sorted property",
    },
    "two_pointers": {
        "class": "SolutionTwoPointers",
        "method": "twoSum",
        "complexity": "O(n) time, O(1) space",
        "description": "Opposite pointers exploiting sorted property",
    },
    "binary_search": {
        "class": "SolutionBinarySearch",
        "method": "twoSum",
        "complexity": "O(n log n) time, O(1) space",
        "description": "For each element, binary search for complement",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output contains correct indices.

    Args:
        actual: Program output (list of two 1-indexed integers)
        expected: Expected output (None if from generator)
        input_data: Raw input string (Line 1: numbers, Line 2: target)

    Returns:
        bool: True if indices are correct
    """
    import json
    lines = input_data.strip().split('\n')
    numbers = json.loads(lines[0]) if lines[0] else []
    target = int(lines[1]) if len(lines) > 1 else 0

    # Parse actual output
    if isinstance(actual, str):
        actual_indices = json.loads(actual) if actual.strip() else []
    elif isinstance(actual, list):
        actual_indices = actual
    else:
        return False

    if len(actual_indices) != 2:
        return False

    # Convert to 0-indexed and verify
    i1, i2 = actual_indices[0] - 1, actual_indices[1] - 1

    if i1 < 0 or i2 < 0 or i1 >= len(numbers) or i2 >= len(numbers):
        return False
    if i1 >= i2:  # index1 must be less than index2
        return False

    return numbers[i1] + numbers[i2] == target


JUDGE_FUNC = judge


# ============================================
# Solution 1: Two Pointers (Optimal)
# Time: O(n), Space: O(1)
#   - Opposite pointers from both ends
#   - Exploits sorted property for direction decisions
#   - Single pass through array
# ============================================
class SolutionTwoPointers:
    """
    Optimal solution using opposite pointers.

    Since the array is sorted, we can use two pointers from both ends
    and adjust based on whether the current sum is too small or too large.
    """

    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """
        Find two numbers that add up to target.

        Core insight: In a sorted array, if sum < target, move left pointer right
        to increase sum. If sum > target, move right pointer left to decrease sum.
        Sorted property guarantees we won't miss the answer.

        Invariant: The answer, if it exists, involves indices in [left, right].

        Args:
            numbers: Sorted array of integers (1-indexed in problem)
            target: Target sum to find

        Returns:
            List of two 1-indexed positions [index1, index2]
        """
        left: int = 0
        right: int = len(numbers) - 1

        while left < right:
            current_sum: int = numbers[left] + numbers[right]

            if current_sum == target:
                # Found the pair (convert to 1-indexed)
                return [left + 1, right + 1]
            elif current_sum < target:
                # Sum too small: need larger value, move left pointer right
                left += 1
            else:
                # Sum too large: need smaller value, move right pointer left
                right -= 1

        # Problem guarantees exactly one solution
        return []


# ============================================
# Solution 2: Binary Search
# Time: O(n log n), Space: O(1)
#   - For each element, binary search for its complement
#   - Less efficient but demonstrates alternative approach
# ============================================
class SolutionBinarySearch:
    """
    Alternative using binary search for each element's complement.

    For each number, binary search for (target - number) in the remaining array.
    Less efficient than two pointers but useful for understanding.
    """

    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        import bisect

        for i in range(len(numbers)):
            complement = target - numbers[i]
            # Binary search for complement in numbers[i+1:]
            j = bisect.bisect_left(numbers, complement, i + 1)

            if j < len(numbers) and numbers[j] == complement:
                return [i + 1, j + 1]  # Convert to 1-indexed

        return []


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: JSON array of sorted integers
        Line 2: Target integer

    Output format:
        JSON array of two 1-indexed positions

    Example:
        Input:
        [2,7,11,15]
        9
        Output: [1,2]
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    numbers = json.loads(lines[0])
    target = int(lines[1])

    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.twoSum(numbers, target)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

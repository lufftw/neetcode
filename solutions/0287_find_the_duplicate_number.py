# solutions/0287_find_the_duplicate_number.py
"""
Problem: Find the Duplicate Number
Link: https://leetcode.com/problems/find-the-duplicate-number/

Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.
There is only one repeated number in nums, return this repeated number.
You must solve the problem without modifying the array nums and uses only constant extra space.

Example 1:
    Input: nums = [1,3,4,2,2]
    Output: 2

Example 2:
    Input: nums = [3,1,3,4,2]
    Output: 3

Example 3:
    Input: nums = [3,3,3,3,3]
    Output: 3

Constraints:
- 1 <= n <= 10^5
- nums.length == n + 1
- 1 <= nums[i] <= n
- All the integers in nums appear only once except for precisely one integer which appears two or more times.

Topics: Array, Two Pointers, Binary Search, Bit Manipulation

Follow-up:
- How can we prove that at least one duplicate number must exist in nums?
- Can you solve the problem in linear runtime complexity?
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionFloyd",
        "method": "findDuplicate",
        "complexity": "O(n) time, O(1) space",
        "description": "Floyd's cycle detection treating array as implicit linked list",
    },
    "floyd": {
        "class": "SolutionFloyd",
        "method": "findDuplicate",
        "complexity": "O(n) time, O(1) space",
        "description": "Floyd's cycle detection treating array as implicit linked list",
    },
    "binary_search": {
        "class": "SolutionBinarySearch",
        "method": "findDuplicate",
        "complexity": "O(n log n) time, O(1) space",
        "description": "Binary search on value range counting elements",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is the duplicate number.

    Args:
        actual: Program output (integer)
        expected: Expected output (None if from generator)
        input_data: Raw input string (JSON array)

    Returns:
        bool: True if correct duplicate found
    """
    import json
    from collections import Counter

    line = input_data.strip()
    nums = json.loads(line) if line else []

    # Find the actual duplicate
    counts = Counter(nums)
    correct = [num for num, count in counts.items() if count > 1]

    if not correct:
        return False

    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val in correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


# ============================================
# Solution 1: Floyd's Cycle Detection
# Time: O(n), Space: O(1)
#   - Treats array as implicit linked list: index -> nums[index]
#   - Duplicate creates a cycle (two indices point to same value)
#   - Phase 1: Find meeting point inside cycle
#   - Phase 2: Find cycle entrance (the duplicate)
# ============================================
class SolutionFloyd:
    """
    Optimal solution using Floyd's Tortoise and Hare algorithm.

    Treats the array as an implicit linked list where each value
    points to the next index. A duplicate creates a cycle.
    """

    def findDuplicate(self, nums: List[int]) -> int:
        """
        Find the duplicate number without modifying the array.

        Core insight: Treat array as linked list (index i -> index nums[i]).
        A duplicate means two indices point to the same node, creating a cycle.
        The cycle entrance is the duplicate value.

        Invariant: After phase 1, slow and fast meet inside the cycle. After
        phase 2, finder and slow meet at the cycle entrance (duplicate value).

        Args:
            nums: Array with n+1 integers in range [1,n], one duplicate

        Returns:
            The duplicate number
        """
        # ==== PHASE 1: Detect cycle and find meeting point ====
        slow: int = nums[0]
        fast: int = nums[0]

        while True:
            slow = nums[slow]           # Move slow by 1 step
            fast = nums[nums[fast]]     # Move fast by 2 steps

            if slow == fast:
                break

        # ==== PHASE 2: Find cycle entrance (the duplicate) ====
        finder: int = nums[0]

        while finder != slow:
            finder = nums[finder]
            slow = nums[slow]

        return finder


# ============================================
# Solution 2: Binary Search on Value Range
# Time: O(n log n), Space: O(1)
#   - Binary search on the value range [1, n]
#   - For each mid, count elements <= mid
#   - If count > mid, duplicate is in [1, mid]
#   - Otherwise, duplicate is in [mid+1, n]
# ============================================
class SolutionBinarySearch:
    """
    Alternative using binary search on the value range.

    Uses pigeonhole principle: if count of numbers <= mid exceeds mid,
    the duplicate must be in the range [1, mid].
    """

    def findDuplicate(self, nums: List[int]) -> int:
        left: int = 1
        right: int = len(nums) - 1

        while left < right:
            mid: int = (left + right) // 2

            # Count elements <= mid
            count: int = sum(1 for num in nums if num <= mid)

            if count > mid:
                # Duplicate is in range [left, mid]
                right = mid
            else:
                # Duplicate is in range [mid+1, right]
                left = mid + 1

        return left


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: JSON array of integers

    Output format:
        The duplicate number

    Example:
        Input:  [1,3,4,2,2]
        Output: 2
    """
    import sys
    import json

    line = sys.stdin.read().strip()
    nums = json.loads(line)

    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.findDuplicate(nums)

    print(result)


if __name__ == "__main__":
    solve()

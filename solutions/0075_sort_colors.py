# solutions/0075_sort_colors.py
"""
Problem: Sort Colors
Link: https://leetcode.com/problems/sort-colors/

Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.
We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.
You must solve this problem without using the library's sort function.

Example 1:
    Input: nums = [2,0,2,1,1,0]
    Output: [0,0,1,1,2,2]

Example 2:
    Input: nums = [2,0,1]
    Output: [0,1,2]

Constraints:
- n == nums.length
- 1 <= n <= 300
- nums[i] is either 0, 1, or 2.

Topics: Array, Two Pointers, Sorting

Hint 1: A rather straight forward solution is a two-pass algorithm using counting sort.

Hint 2: Iterate the array counting number of 0's, 1's, and 2's.

Hint 3: Overwrite array with the total number of 0's, then 1's and followed by 2's.

Follow-up: Could you come up with a one-pass algorithm using only constant extra space?
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDutchFlag",
        "method": "sortColors",
        "complexity": "O(n) time, O(1) space",
        "description": "Dutch National Flag algorithm (one-pass three-way partition)",
    },
    "dutch_flag": {
        "class": "SolutionDutchFlag",
        "method": "sortColors",
        "complexity": "O(n) time, O(1) space",
        "description": "Dutch National Flag algorithm (one-pass three-way partition)",
    },
    "counting": {
        "class": "SolutionCounting",
        "method": "sortColors",
        "complexity": "O(n) time, O(1) space",
        "description": "Two-pass counting sort approach",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is correctly sorted (0s, 1s, 2s).
    
    Args:
        actual: Program output (space-separated integers as string, list, or single int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (space-separated integers 0, 1, or 2)
    
    Returns:
        bool: True if correctly sorted
    """
    import json
    line = input_data.strip()
    nums = json.loads(line) if line else []
    
    # Parse actual output - handle int (from ast.literal_eval), str, or list
    if isinstance(actual, int):
        actual_nums = [actual]
    elif isinstance(actual, str):
        actual_nums = list(map(int, actual.strip().split())) if actual.strip() else []
    elif isinstance(actual, list):
        actual_nums = actual
    else:
        return False
    
    # Compute correct answer (sorted)
    correct_nums = sorted(nums)
    
    # Check if arrays match
    return actual_nums == correct_nums


JUDGE_FUNC = judge


# ============================================
# Solution 1: Dutch National Flag Algorithm
# Time: O(n), Space: O(1)
#   - Each element examined once
#   - In-place swaps only
#   - Optimal one-pass solution
# ============================================
class SolutionDutchFlag:
    """
    Optimal one-pass solution using Dutch National Flag algorithm.
    
    Maintains three regions for 0s, 1s, and 2s while scanning through
    the array exactly once.
    """
    
    def sortColors(self, nums: List[int]) -> None:
        """
        Sort array containing only 0s, 1s, and 2s in-place.

        Core insight: Dutch National Flag maintains three regions and classifies
        each element in one pass. Don't increment mid when swapping with high
        because the swapped element is unexamined.

        Invariant: [0,low) = 0s, [low,mid) = 1s, (high,n) = 2s, [mid,high] = unclassified.

        Args:
            nums: Array of integers (0, 1, or 2) to sort in-place
        """
        # POINTERS: Define three region boundaries
        low: int = 0              # Next position for 0
        mid: int = 0              # Current position being examined
        high: int = len(nums) - 1 # Next position for 2
        
        # Process until mid crosses high
        while mid <= high:
            if nums[mid] == 0:
                # CASE 0: Move to "red" section (beginning)
                # Swap with low and advance both pointers
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
                # We can increment mid because swapped element from low
                # is either 0 (already processed) or 1 (correct position)
            
            elif nums[mid] == 2:
                # CASE 2: Move to "blue" section (end)
                # Swap with high and decrement high only
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
                # DON'T increment mid — swapped element is unexamined
            
            else:
                # CASE 1: Already in correct section ("white")
                # Just advance mid
                mid += 1


# ============================================
# Solution 2: Counting Sort Approach
# Time: O(n), Space: O(1)
#   - Two passes: count then overwrite
#   - Simpler logic but requires two passes
#   - Uses O(1) space for count array (only 3 values)
# ============================================
class SolutionCounting:
    """
    Alternative using counting sort approach.
    
    Two passes: first count each color, then overwrite array.
    Simpler to understand but requires two passes.
    """
    
    def sortColors(self, nums: List[int]) -> None:
        # Count occurrences of each color
        count = [0, 0, 0]
        for num in nums:
            count[num] += 1
        
        # Overwrite array with sorted colors
        index = 0
        for color in range(3):
            for _ in range(count[color]):
                nums[index] = color
                index += 1


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    import json
    """
    Input format:
        Line 1: Space-separated integers (0, 1, or 2)
    
    Output format:
        Sorted array (space-separated)
    
    Example:
        Input:  2 0 2 1 1 0
        Output: 0 0 1 1 2 2
    """
    import sys
    import json
    
    line = sys.stdin.read().strip()
    nums = json.loads(line) if line else []
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    solver.sortColors(nums)
    
    print(json.dumps(nums, separators=(',', ':')))


if __name__ == "__main__":
    solve()

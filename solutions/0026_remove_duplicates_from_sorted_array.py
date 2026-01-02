# solutions/0026_remove_duplicates_from_sorted_array.py
"""
Problem: Remove Duplicates from Sorted Array
Link: https://leetcode.com/problems/remove-duplicates-from-sorted-array/

Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Then return the number of unique elements in nums.
Consider the number of unique elements of nums to be k, to get accepted, you need to do the following things:
- Change the array nums such that the first k elements of nums contain the unique elements in the order they were present in nums initially. The remaining elements of nums are not important as well as the size of nums.
- Return k.

Example 1:
    Input: nums = [1,1,2]
    Output: 2, nums = [1,2,_]
    Explanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
                 It does not matter what you leave beyond the returned k (hence they are underscores).

Example 2:
    Input: nums = [0,0,1,1,1,2,2,3,3,4]
    Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
    Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
                 It does not matter what you leave beyond the returned k (hence they are underscores).

Constraints:
- 1 <= nums.length <= 3 * 10^4
- -100 <= nums[i] <= 100
- nums is sorted in non-decreasing order.

Topics: Array, Two Pointers

Hint 1: In this problem, the key point to focus on is the input array being sorted. As far as duplicate elements are concerned, what is their positioning in the array when the given array is sorted? Look at the image above for the answer. If we know the position of one of the elements, do we also know the positioning of all the duplicate elements?

<br>
<img src="https://assets.leetcode.com/uploads/2019/10/20/hint_rem_dup.png" width="500"/>

Hint 2: We need to modify the array in-place and the size of the final array would potentially be smaller than the size of the input array. So, we ought to use a two-pointer approach here. One, that would keep track of the current element in the original array and another one for just the unique elements.

Hint 3: Essentially, once an element is encountered, you simply need to <b>bypass</b> its duplicates and move on to the next unique element.
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",
        "method": "removeDuplicates",
        "complexity": "O(n) time, O(1) space",
        "description": "Reader/writer pointer pattern for in-place deduplication",
    },
    "two_pointers": {
        "class": "SolutionTwoPointers",
        "method": "removeDuplicates",
        "complexity": "O(n) time, O(1) space",
        "description": "Reader/writer pointer pattern for in-place deduplication",
    },
    "enumerate": {
        "class": "SolutionEnumerate",
        "method": "removeDuplicates",
        "complexity": "O(n) time, O(1) space",
        "description": "Using enumerate for cleaner iteration",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output correctly removes duplicates.
    
    Args:
        actual: Program output (may be string with newlines or tuple)
        expected: Expected output (None if from generator)
        input_data: Raw input string (canonical JSON format)
    
    Returns:
        bool: True if correct deduplication
    """
    import json
    line = input_data.strip()
    nums = json.loads(line) if line else []
    
    # Parse actual output
    if isinstance(actual, str):
        lines = actual.strip().split('\n')
        if len(lines) >= 2:
            k = int(lines[0])
            result_nums = json.loads(lines[1]) if lines[1] else []
        else:
            return False
    elif isinstance(actual, tuple) and len(actual) == 2:
        k, result_nums = actual
    else:
        return False
    
    # Compute correct answer
    correct_k, correct_nums = _brute_force_remove_duplicates(nums)
    
    # Check count and values match
    return k == correct_k and result_nums == correct_nums


def _brute_force_remove_duplicates(nums: List[int]) -> tuple[int, List[int]]:
    """Brute force deduplication."""
    if not nums:
        return 0, []
    
    unique = [nums[0]]
    for i in range(1, len(nums)):
        if nums[i] != nums[i - 1]:
            unique.append(nums[i])
    
    return len(unique), unique


JUDGE_FUNC = judge


# ============================================
# Solution 1: Reader/Writer Two Pointers
# Time: O(n), Space: O(1)
#   - Single pass through array
#   - In-place modification with two indices
#   - Optimal for sorted array deduplication
# ============================================
class SolutionTwoPointers:
    """
    Optimal solution using reader/writer pointer pattern.
    
    Maintains the invariant that nums[0:write_index] contains exactly
    one copy of each unique value seen so far.
    """
    
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        Remove duplicates in-place, keeping one copy of each unique element.
        
        Args:
            nums: Sorted array of integers (modified in-place)
            
        Returns:
            Number of unique elements (new logical length)
        """
        if len(nums) == 0:
            return 0
        
        # WRITE POINTER: Position where next unique element will be placed
        # Start at 1 because nums[0] is always kept (first element is unique)
        write_index: int = 1
        
        # READ POINTER: Scan through array looking for new unique values
        for read_index in range(1, len(nums)):
            # CHECK CONDITION: Is this a new unique value?
            # Compare with the last written element (nums[write_index - 1])
            if nums[read_index] != nums[write_index - 1]:
                # WRITE: Copy unique value to write position
                nums[write_index] = nums[read_index]
                write_index += 1
        
        # write_index now equals the count of unique elements
        return write_index


# ============================================
# Solution 2: Using Enumerate
# Time: O(n), Space: O(1)
#   - Functionally identical to SolutionTwoPointers
#   - Uses enumerate for cleaner iteration
#   - May be more readable for some developers
# ============================================
class SolutionEnumerate:
    """
    Alternative using enumerate for cleaner iteration.
    
    Functionally identical but may be more readable for some developers.
    """
    
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        
        write_index: int = 1
        
        for read_index, value in enumerate(nums):
            if read_index > 0 and value != nums[write_index - 1]:
                nums[write_index] = value
                write_index += 1
        
        return write_index


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    import json
    """
    Input format:
        Line 1: Space-separated integers (sorted array)
    
    Output format:
        Line 1: Number of unique elements
        Line 2: The unique elements (space-separated)
    
    Example:
        Input:  1 1 2
        Output: 
        2
        1 2
    """
    import sys
    import json
    
    line = sys.stdin.read().strip()
    if not line:
        # Multi-output: k and nums[:k]
        print(0)
        print("[]")
        return
    
    nums = json.loads(line)
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    k = solver.removeDuplicates(nums)
    
    # Multi-output validation: return value + modified array
    print(k)
    print(json.dumps(nums[:k], separators=(',', ':')))


if __name__ == "__main__":
    solve()

# solutions/0027_remove_element.py
"""
Problem: Remove Element
Link: https://leetcode.com/problems/remove-element/

Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The order of the elements may be changed. Then return the number of elements in nums which are not equal to val.
Consider the number of elements in nums which are not equal to val be k, to get accepted, you need to do the following things:
- Change the array nums such that the first k elements of nums contain the elements which are not equal to val. The remaining elements of nums are not important as well as the size of nums.
- Return k.

Example 1:
    Input: nums = [3,2,2,3], val = 3
    Output: 2, nums = [2,2,_,_]
    Explanation: Your function should return k = 2, with the first two elements of nums being 2.
                 It does not matter what you leave beyond the returned k (hence they are underscores).

Example 2:
    Input: nums = [0,1,2,2,3,0,4,2], val = 2
    Output: 5, nums = [0,1,4,0,3,_,_,_]
    Explanation: Your function should return k = 5, with the first five elements of nums containing 0, 0, 1, 3, and 4.
                 Note that the five elements can be returned in any order.
                 It does not matter what you leave beyond the returned k (hence they are underscores).

Constraints:
- 0 <= nums.length <= 100
- 0 <= nums[i] <= 50
- 0 <= val <= 100

Topics: Array, Two Pointers

Hint 1: The problem statement clearly asks us to modify the array in-place and it also says that the element beyond the new length of the array can be anything. Given an element, we need to remove all the occurrences of it from the array. We don't technically need to <b>remove</b> that element per-say, right?

Hint 2: We can move all the occurrences of this element to the end of the array. Use two pointers!
<br><img src="https://assets.leetcode.com/uploads/2019/10/20/hint_remove_element.png" width="500"/>

Hint 3: Yet another direction of thought is to consider the elements to be removed as non-existent. In a single pass, if we keep copying the visible elements in-place, that should also solve this problem for us.
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",
        "method": "removeElement",
        "complexity": "O(n) time, O(1) space",
        "description": "Reader/writer pointer pattern for in-place removal",
    },
    "two_pointers": {
        "class": "SolutionTwoPointers",
        "method": "removeElement",
        "complexity": "O(n) time, O(1) space",
        "description": "Reader/writer pointer pattern for in-place removal",
    },
    "two_ends": {
        "class": "SolutionTwoEnds",
        "method": "removeElement",
        "complexity": "O(n) time, O(1) space",
        "description": "Opposite pointers swapping from both ends (efficient when val is rare)",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output correctly removes all occurrences of val.
    
    Args:
        actual: Program output (may be string with newlines, tuple, or int when k=0)
        expected: Expected output (None if from generator)
        input_data: Raw input string (Line 1: nums, Line 2: val)
    
    Returns:
        bool: True if correct removal
    """
    lines = input_data.strip().split('\n')
    nums = list(map(int, lines[0].split())) if lines[0] else []
    val = int(lines[1]) if len(lines) > 1 else 0
    
    # Parse actual output - handle various formats
    if isinstance(actual, int):
        # ast.literal_eval parsed single number (k=0 case, no second line)
        k = actual
        result_nums = []
    elif isinstance(actual, str):
        lines_out = actual.strip().split('\n')
        k = int(lines_out[0])
        if len(lines_out) >= 2 and lines_out[1]:
            result_nums = list(map(int, lines_out[1].split()))
        else:
            # k=0 case: no elements remaining
            result_nums = []
    elif isinstance(actual, tuple) and len(actual) == 2:
        k, result_nums = actual
    else:
        return False
    
    # Compute correct answer
    correct_k, correct_nums = _brute_force_remove_element(nums, val)
    
    # Check count and values match
    return k == correct_k and result_nums == correct_nums


def _brute_force_remove_element(nums: List[int], val: int) -> tuple[int, List[int]]:
    """Brute force element removal."""
    result = [x for x in nums if x != val]
    return len(result), result


JUDGE_FUNC = judge


# ============================================
# Solution 1: Reader/Writer Two Pointers
# Time: O(n), Space: O(1)
#   - Single pass through array
#   - In-place modification
#   - Optimal when val appears frequently
# ============================================
class SolutionTwoPointers:
    """
    Optimal solution using reader/writer pointer pattern.
    
    Simple and efficient: elements not equal to val are copied forward,
    effectively "overwriting" the vals.
    """
    
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        Remove all occurrences of val in-place.
        
        Args:
            nums: Array of integers (modified in-place)
            val: Value to remove
            
        Returns:
            Number of elements remaining (not equal to val)
        """
        # WRITE POINTER: Position for next element to keep
        write_index: int = 0
        
        # READ POINTER: Scan through all elements
        for read_index in range(len(nums)):
            # CHECK CONDITION: Keep if not equal to val
            if nums[read_index] != val:
                nums[write_index] = nums[read_index]
                write_index += 1
        
        return write_index


# ============================================
# Solution 2: Two Pointers from Both Ends
# Time: O(n), Space: O(1)
#   - More efficient when val is rare
#   - Swaps val elements with elements from end
#   - Minimizes total writes
# ============================================
class SolutionTwoEnds:
    """
    Alternative using pointers from both ends.
    
    More efficient when val is rare: we swap val elements with elements
    from the end, minimizing total writes.
    
    Useful when:
    - Elements to remove are rare
    - We want to minimize write operations
    """
    
    def removeElement(self, nums: List[int], val: int) -> int:
        left: int = 0
        right: int = len(nums) - 1
        
        while left <= right:
            if nums[left] == val:
                # Swap with element from end
                nums[left] = nums[right]
                right -= 1
                # Don't increment left - need to check swapped element
            else:
                left += 1
        
        return left


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (array)
        Line 2: Value to remove
    
    Output format:
        Line 1: Number of remaining elements
        Line 2: Remaining elements (space-separated)
    
    Example:
        Input:
        3 2 2 3
        3
        Output:
        2
        2 2
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    nums = list(map(int, lines[0].split())) if lines[0] else []
    val = int(lines[1])
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    k = solver.removeElement(nums, val)
    
    print(k)
    if k > 0:
        print(' '.join(map(str, nums[:k])))


if __name__ == "__main__":
    solve()

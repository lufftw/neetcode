# solutions/0027_remove_element.py
"""
================================================================================
LeetCode 27: Remove Element
================================================================================

Problem: Given an integer array nums and an integer val, remove all occurrences
         of val in nums in-place. The order of elements may be changed.
         Return the number of elements not equal to val.

API Kernel: TwoPointersTraversal
Pattern: same_direction_writer
Family: in_place_array_modification

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: SAME-DIRECTION (READER/WRITER)
--------------------------------------------------------------------------------

This problem uses the same-direction pattern with a simple keep condition:
keep the element if it's not equal to the target value.

DELTA from Remove Duplicates (LeetCode 26):
- Condition changes from "different from last written" to "not equal to val"
- Array need not be sorted
- Write index starts at 0 (no guaranteed first element to keep)

INVARIANT: nums[0:write] contains all elements != val from nums[0:read].

Algorithm:
1. Scan through array with read pointer
2. If current element != val, copy to write position and increment write
3. Return write (count of elements kept)

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Single pass through the array
Space: O(1) - In-place modification

================================================================================
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
        actual: Program output (may be string with newlines or tuple)
        expected: Expected output (None if from generator)
        input_data: Raw input string (Line 1: nums, Line 2: val)
    
    Returns:
        bool: True if correct removal
    """
    lines = input_data.strip().split('\n')
    nums = list(map(int, lines[0].split())) if lines[0] else []
    val = int(lines[1]) if len(lines) > 1 else 0
    
    # Parse actual output
    if isinstance(actual, str):
        lines_out = actual.strip().split('\n')
        if len(lines_out) >= 2:
            k = int(lines_out[0])
            result_nums = list(map(int, lines_out[1].split())) if lines_out[1] else []
        else:
            return False
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

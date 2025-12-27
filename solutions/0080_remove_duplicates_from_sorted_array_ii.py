# solutions/0080_remove_duplicates_from_sorted_array_ii.py
"""
Problem: Remove Duplicates from Sorted Array II
Link: https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/

Given an integer array nums sorted in non-decreasing order, remove some duplicates in-place such that each unique element appears at most twice. The relative order of the elements should be kept the same.
Since it is impossible to change the length of the array in some languages, you must instead have the result be placed in the first part of the array nums. More formally, if there are k elements after removing the duplicates, then the first k elements of nums should hold the final result. It does not matter what you leave beyond the first k elements.
Return k after placing the final result in the first k slots of nums.
Do not allocate extra space for another array. You must do this by modifying the input array in-place with O(1) extra memory.

Example 1:
    Input: nums = [1,1,1,2,2,3]
    Output: 5, nums = [1,1,2,2,3,_]
    Explanation: Your function should return k = 5, with the first five elements of nums being 1, 1, 2, 2 and 3 respectively.
                 It does not matter what you leave beyond the returned k (hence they are underscores).

Example 2:
    Input: nums = [0,0,1,1,1,1,2,3,3]
    Output: 7, nums = [0,0,1,1,2,3,3,_,_]
    Explanation: Your function should return k = 7, with the first seven elements of nums being 0, 0, 1, 1, 2, 3 and 3 respectively.
                 It does not matter what you leave beyond the returned k (hence they are underscores).

Constraints:
- 1 <= nums.length <= 3 * 10^4
- -10^4 <= nums[i] <= 10^4
- nums is sorted in non-decreasing order.

Topics: Array, Two Pointers
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
        "description": "Reader/writer pattern with K=2 lookback check",
    },
    "two_pointers": {
        "class": "SolutionTwoPointers",
        "method": "removeDuplicates",
        "complexity": "O(n) time, O(1) space",
        "description": "Reader/writer pattern with K=2 lookback check",
    },
    "k_copies": {
        "class": "SolutionKCopies",
        "method": "removeDuplicates",
        "complexity": "O(n) time, O(1) space",
        "description": "Generalized solution allowing up to K copies (default K=2)",
    },
    "counter": {
        "class": "SolutionCounter",
        "method": "removeDuplicates",
        "complexity": "O(n) time, O(1) space",
        "description": "Explicit counter tracking approach",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output allows at most 2 copies of each element.
    
    Args:
        actual: Program output (may be string with newlines or tuple)
        expected: Expected output (None if from generator)
        input_data: Raw input string (space-separated sorted integers)
    
    Returns:
        bool: True if correct deduplication (max 2 copies)
    """
    line = input_data.strip()
    nums = list(map(int, line.split())) if line else []
    
    # Parse actual output
    if isinstance(actual, str):
        lines = actual.strip().split('\n')
        if len(lines) >= 2:
            k = int(lines[0])
            result_nums = list(map(int, lines[1].split())) if lines[1] else []
        else:
            return False
    elif isinstance(actual, tuple) and len(actual) == 2:
        k, result_nums = actual
    else:
        return False
    
    # Compute correct answer
    correct_k, correct_nums = _brute_force_remove_duplicates_ii(nums)
    
    # Check count and values match
    return k == correct_k and result_nums == correct_nums


def _brute_force_remove_duplicates_ii(nums: List[int]) -> tuple[int, List[int]]:
    """Brute force deduplication allowing at most 2 copies."""
    if not nums:
        return 0, []
    
    result = [nums[0]]
    count = 1
    
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            count += 1
            if count <= 2:
                result.append(nums[i])
        else:
            count = 1
            result.append(nums[i])
    
    return len(result), result


JUDGE_FUNC = judge


# ============================================
# Solution 1: Reader/Writer with K-Allowance
# Time: O(n), Space: O(1)
#   - Single pass through array
#   - Checks nums[write-2] to allow at most 2 copies
#   - Generalizes to any K by changing lookback distance
# ============================================
class SolutionTwoPointers:
    """
    Optimal solution allowing at most 2 copies of each element.
    
    The key insight is that we compare with nums[write_index - 2] to determine
    if we already have 2 copies of the current value.
    """
    
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        Remove duplicates allowing at most 2 copies of each element.
        
        Args:
            nums: Sorted array of integers (modified in-place)
            
        Returns:
            New length with at most 2 copies per unique element
        """
        n: int = len(nums)
        if n <= 2:
            return n
        
        # WRITE POINTER: Start at 2 (first two elements always kept)
        write_index: int = 2
        
        # READ POINTER: Start scanning from index 2
        for read_index in range(2, n):
            # CHECK CONDITION: Keep if different from element 2 positions back
            # If nums[read] != nums[write-2], we don't yet have 2 copies
            if nums[read_index] != nums[write_index - 2]:
                nums[write_index] = nums[read_index]
                write_index += 1
        
        return write_index


# ============================================
# Solution 2: Generalized K-Copies Solution
# Time: O(n), Space: O(1)
#   - Generalizes to any K by parameter
#   - Template for K=1 case (original problem) and K=2 case
#   - Single parameter change adapts to different K values
# ============================================
class SolutionKCopies:
    """
    Generalized solution that allows up to K copies of each element.
    
    This template can solve the K=1 case (original problem) and K=2 case
    (this problem) with a single parameter change.
    """
    
    def removeDuplicates(self, nums: List[int], k: int = 2) -> int:
        """
        Remove duplicates allowing at most k copies of each element.
        
        Args:
            nums: Sorted array of integers
            k: Maximum allowed copies (default 2)
            
        Returns:
            New length with at most k copies per unique element
        """
        n: int = len(nums)
        if n <= k:
            return n
        
        write_index: int = k
        
        for read_index in range(k, n):
            # Compare with element k positions back
            if nums[read_index] != nums[write_index - k]:
                nums[write_index] = nums[read_index]
                write_index += 1
        
        return write_index


# ============================================
# Solution 3: Explicit Counter Approach
# Time: O(n), Space: O(1)
#   - Uses explicit count tracking
#   - More verbose but clearer for understanding logic
#   - Tracks consecutive duplicates explicitly
# ============================================
class SolutionCounter:
    """
    Alternative using explicit count tracking.
    
    More verbose but may be clearer for understanding the logic.
    """
    
    def removeDuplicates(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return len(nums)
        
        write_index: int = 1
        count: int = 1
        
        for read_index in range(1, len(nums)):
            if nums[read_index] == nums[read_index - 1]:
                count += 1
            else:
                count = 1
            
            # Keep element if we haven't seen it twice yet
            if count <= 2:
                nums[write_index] = nums[read_index]
                write_index += 1
        
        return write_index


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (sorted array)
    
    Output format:
        Line 1: New length
        Line 2: Modified array (first k elements)
    
    Example:
        Input:  1 1 1 2 2 3
        Output:
        5
        1 1 2 2 3
    """
    import sys
    
    line = sys.stdin.read().strip()
    if not line:
        print(0)
        return
    
    nums = list(map(int, line.split()))
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    k = solver.removeDuplicates(nums)
    
    print(k)
    if k > 0:
        print(' '.join(map(str, nums[:k])))


if __name__ == "__main__":
    solve()

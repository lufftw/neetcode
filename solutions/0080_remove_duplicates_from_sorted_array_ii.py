# solutions/0080_remove_duplicates_from_sorted_array_ii.py
"""
================================================================================
LeetCode 80: Remove Duplicates from Sorted Array II
================================================================================

Problem: Given a sorted array nums, remove some duplicates in-place such that
         each unique element appears at most twice. Return the new length.

API Kernel: TwoPointersTraversal
Pattern: same_direction_writer_k_allowed
Family: in_place_array_modification

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: SAME-DIRECTION WITH K-ALLOWANCE
--------------------------------------------------------------------------------

This problem generalizes the basic deduplication pattern to allow up to K copies.

DELTA from Remove Duplicates (LeetCode 26):
- Instead of "different from nums[write-1]", check "different from nums[write-K]"
- K=2 for this problem (each element appears at most twice)
- Generalizes to any K by changing the lookback distance

INVARIANT: nums[0:write] contains at most K copies of each unique element.

Key Insight:
    We can allow K copies by checking nums[write-K] instead of nums[write-1].
    If the current element equals nums[write-K], we already have K copies,
    so we skip it. Otherwise, we write it.

Why This Works:
    If nums[read] == nums[write-K], then nums[write-K], ..., nums[write-1] are
    all equal (since array is sorted), meaning we already have K copies.

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Single pass through the array
Space: O(1) - In-place modification

================================================================================
"""
from typing import List
import os


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "method": "solve_two_pointers",
        "complexity": "O(n) time, O(1) space",
        "description": "Reader/writer pattern with K=2 lookback check",
    },
    "two_pointers": {
        "method": "solve_two_pointers",
        "complexity": "O(n) time, O(1) space",
        "description": "Reader/writer pattern with K=2 lookback check",
    },
    "k_copies": {
        "method": "solve_k_copies",
        "complexity": "O(n) time, O(1) space",
        "description": "Generalized solution allowing up to K copies (default K=2)",
    },
    "counter": {
        "method": "solve_counter",
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
# Solution: Reader/Writer with K-Allowance
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


# ============================================
# Wrapper functions for test_runner integration
# ============================================
def solve_two_pointers(nums: List[int]) -> int:
    """Wrapper for SolutionTwoPointers."""
    return SolutionTwoPointers().removeDuplicates(nums)


def solve_k_copies(nums: List[int]) -> int:
    """Wrapper for SolutionKCopies."""
    return SolutionKCopies().removeDuplicates(nums, 2)


def solve_counter(nums: List[int]) -> int:
    """Wrapper for SolutionCounter."""
    return SolutionCounter().removeDuplicates(nums)


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
    
    # Read environment variable to select which solution method to use
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    method_info = SOLUTIONS.get(method_name, SOLUTIONS['default'])
    method_func_name = method_info['method']
    
    # Dynamically call the selected solution method
    method_func = globals()[method_func_name]
    k = method_func(nums)
    
    print(k)
    if k > 0:
        print(' '.join(map(str, nums[:k])))


if __name__ == "__main__":
    solve()

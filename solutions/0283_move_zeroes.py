# solutions/0283_move_zeroes.py
"""
Problem: Move Zeroes
Link: https://leetcode.com/problems/move-zeroes/

Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.
Note that you must do this in-place without making a copy of the array.

Example 1:
    Input: nums = [0,1,0,3,12]
    Output: [1,3,12,0,0]

Example 2:
    Input: nums = [0]
    Output: [0]

Constraints:
- 1 <= nums.length <= 10^4
- -2^31 <= nums[i] <= 2^31 - 1

Topics: Array, Two Pointers

Hint 1: <b>In-place</b> means we should not be allocating any space for extra array. But we are allowed to modify the existing array. However, as a first step, try coming up with a solution that makes use of additional space. For this problem as well, first apply the idea discussed using an additional array and the in-place solution will pop up eventually.

Hint 2: A <b>two-pointer</b> approach could be helpful here. The idea would be to have one pointer for iterating the array and another pointer that just works on the non-zero elements of the array.

Follow-up: Could you minimize the total number of operations done?
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
        "method": "moveZeroes",
        "complexity": "O(n) time, O(1) space",
        "description": "Reader/writer pattern with zero-fill phase",
    },
    "two_pointers": {
        "class": "SolutionTwoPointers",
        "method": "moveZeroes",
        "complexity": "O(n) time, O(1) space",
        "description": "Reader/writer pattern with zero-fill phase",
    },
    "swap": {
        "class": "SolutionSwap",
        "method": "moveZeroes",
        "complexity": "O(n) time, O(1) space",
        "description": "Swap-based approach in single pass",
    },
    "optimized_swap": {
        "class": "SolutionOptimizedSwap",
        "method": "moveZeroes",
        "complexity": "O(n) time, O(1) space",
        "description": "Optimized swap avoiding unnecessary self-swaps",
    },
    "snowball": {
        "class": "SolutionSnowball",
        "method": "moveZeroes",
        "complexity": "O(n) time, O(1) space",
        "description": "Snowball method tracking zeros rolling through array",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output has all zeros moved to end.
    
    Args:
        actual: Program output (space-separated integers as string, list, or single int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (space-separated integers)
    
    Returns:
        bool: True if zeros are at end and relative order preserved
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
    
    # Compute correct answer
    correct_nums = _brute_force_move_zeroes(nums.copy())
    
    # Check if arrays match
    return actual_nums == correct_nums


def _brute_force_move_zeroes(nums: List[int]) -> List[int]:
    """Brute force move zeroes to end."""
    non_zeros = [x for x in nums if x != 0]
    zeros = [0] * (len(nums) - len(non_zeros))
    return non_zeros + zeros


JUDGE_FUNC = judge


# ============================================
# Solution 1: Reader/Writer with Fill
# Time: O(n), Space: O(1)
#   - Phase 1: Move non-zeros to front O(n)
#   - Phase 2: Fill remaining with zeros O(n)
#   - Minimizes writes when zeros are sparse
# ============================================
class SolutionTwoPointers:
    """
    Optimal solution using reader/writer pattern with zero-fill phase.
    
    This approach minimizes writes when there are few zeros, as we only
    write non-zero elements once each.
    """
    
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Move all zeros to the end while maintaining relative order of non-zeros.

        Core insight: Reader/writer pattern with zero-fill. Non-zeros are copied
        forward preserving order, then remaining positions are filled with zeros.
        This minimizes writes when zeros are sparse.

        Invariant: nums[0:write_index] contains all non-zero elements in original order.

        Args:
            nums: Array of integers (modified in-place)
        """
        n: int = len(nums)
        
        # PHASE 1: Move all non-zero elements to the front
        write_index: int = 0
        
        for read_index in range(n):
            if nums[read_index] != 0:
                nums[write_index] = nums[read_index]
                write_index += 1
        
        # PHASE 2: Fill remaining positions with zeros
        for i in range(write_index, n):
            nums[i] = 0


# ============================================
# Solution 2: Swap-Based Approach
# Time: O(n), Space: O(1)
#   - Single pass with swaps
#   - Zeros naturally accumulate at end
#   - More writes when zeros are sparse
# ============================================
class SolutionSwap:
    """
    Alternative using swaps instead of overwrite + fill.
    
    Each non-zero element is swapped with the element at write_index.
    Zeros naturally accumulate at the end through swapping.
    
    This approach uses more writes when zeros are sparse, but is more
    intuitive and works in a single pass.
    """
    
    def moveZeroes(self, nums: List[int]) -> None:
        write_index: int = 0
        
        for read_index in range(len(nums)):
            if nums[read_index] != 0:
                # SWAP: Exchange non-zero with position at write_index
                # This moves zeros toward the end
                nums[write_index], nums[read_index] = nums[read_index], nums[write_index]
                write_index += 1


# ============================================
# Solution 3: Optimized Swap (Avoid Self-Swap)
# Time: O(n), Space: O(1)
#   - Avoids unnecessary self-swaps
#   - Better when zeros are rare
#   - Checks if swap is needed before swapping
# ============================================
class SolutionOptimizedSwap:
    """
    Optimized swap version that avoids unnecessary self-swaps.
    
    When write_index == read_index, swapping is unnecessary.
    This optimization helps when zeros are rare.
    """
    
    def moveZeroes(self, nums: List[int]) -> None:
        write_index: int = 0
        
        for read_index in range(len(nums)):
            if nums[read_index] != 0:
                if write_index != read_index:
                    nums[write_index], nums[read_index] = nums[read_index], nums[write_index]
                write_index += 1


# ============================================
# Solution 4: Snowball Method
# Time: O(n), Space: O(1)
#   - Tracks "snowball" of zeros rolling through array
#   - Conceptually different but equivalent to swap approach
#   - As zeros accumulate, snowball grows; swap non-zero with front
# ============================================
class SolutionSnowball:
    """
    Snowball method: track the "snowball" of zeros rolling through the array.
    
    As we encounter zeros, the snowball grows. When we encounter a non-zero,
    we swap it with the front of the snowball.
    
    Conceptually different but equivalent to the swap approach.
    """
    
    def moveZeroes(self, nums: List[int]) -> None:
        snowball_size: int = 0  # Number of zeros accumulated
        
        for i in range(len(nums)):
            if nums[i] == 0:
                snowball_size += 1
            elif snowball_size > 0:
                # Swap current element with front of snowball
                nums[i - snowball_size], nums[i] = nums[i], nums[i - snowball_size]


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers
    
    Output format:
        Space-separated integers (zeros moved to end)
    
    Example:
        Input:  0 1 0 3 12
        Output: 1 3 12 0 0
    """
    import sys
    import json
    
    line = sys.stdin.read().strip()
    if not line:
        return
    
    nums = json.loads(line)
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    solver.moveZeroes(nums)
    
    print(json.dumps(nums, separators=(',', ':')))


if __name__ == "__main__":
    solve()

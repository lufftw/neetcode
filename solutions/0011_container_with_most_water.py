# solutions/0011_container_with_most_water.py
"""
================================================================================
LeetCode 11: Container With Most Water
================================================================================

Problem: Given n non-negative integers representing heights of vertical lines,
         find two lines that together with the x-axis form a container that
         holds the most water.

API Kernel: TwoPointersTraversal
Pattern: opposite_pointers_maximize
Family: two_pointers_optimization

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: OPPOSITE POINTERS (MAXIMIZE)
--------------------------------------------------------------------------------

This problem demonstrates the classic opposite pointers pattern for optimization.
We start with pointers at both ends and greedily move the pointer pointing to
the shorter line.

INVARIANT: The maximum area must involve lines at or between left and right.

Key Insight:
    Area = min(height[left], height[right]) × (right - left)
    
    Moving the pointer with the LARGER height can only DECREASE area because:
    - Width definitely decreases
    - min(heights) can only stay same or decrease
    
    Moving the pointer with the SMALLER height MIGHT increase area because:
    - Width decreases, but
    - min(heights) might increase enough to compensate

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Each pointer moves at most n times
Space: O(1) - Only two pointer indices stored

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
        "method": "maxArea",
        "complexity": "O(n) time, O(1) space",
        "description": "Two pointers from both ends with greedy movement",
    },
    "two_pointers": {
        "class": "SolutionTwoPointers",
        "method": "maxArea",
        "complexity": "O(n) time, O(1) space",
        "description": "Two pointers from both ends with greedy movement",
    },
    "optimized": {
        "class": "SolutionTwoPointersOptimized",
        "method": "maxArea",
        "complexity": "O(n) time, O(1) space",
        "description": "Two pointers with skip optimization for consecutive smaller heights",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is the maximum area.
    
    Args:
        actual: Program output (integer as string or int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (space-separated heights)
    
    Returns:
        bool: True if correct maximum area
    """
    line = input_data.strip()
    height = list(map(int, line.split())) if line else []
    
    # Compute correct answer using brute force
    correct = _brute_force_max_area(height)
    
    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _brute_force_max_area(height: List[int]) -> int:
    """O(n²) brute force solution for verification."""
    n = len(height)
    if n < 2:
        return 0
    
    max_area = 0
    for i in range(n):
        for j in range(i + 1, n):
            area = min(height[i], height[j]) * (j - i)
            max_area = max(max_area, area)
    
    return max_area


JUDGE_FUNC = judge


# ============================================
# Solution 1: Two Pointers Greedy
# Time: O(n), Space: O(1)
#   - Each pointer moves at most n times
#   - Only two pointer indices stored
#   - Greedy choice: always move the shorter pointer
# ============================================
class SolutionTwoPointers:
    """
    Optimal solution using opposite pointers with greedy movement.
    
    The greedy choice of always moving the shorter pointer is correct because
    keeping the shorter pointer fixed cannot lead to a larger area (the height
    is already bottlenecked, and width can only decrease).
    """
    
    def maxArea(self, height: List[int]) -> int:
        """
        Find the maximum area of water that can be contained.
        
        Args:
            height: List of non-negative integers representing line heights
            
        Returns:
            Maximum area of water that can be contained
        """
        left: int = 0
        right: int = len(height) - 1
        max_area: int = 0
        
        while left < right:
            # CALCULATE: Current container area
            # Width is the distance between pointers
            width: int = right - left
            # Height is limited by the shorter line
            current_height: int = min(height[left], height[right])
            current_area: int = width * current_height
            
            # UPDATE ANSWER: Track maximum area seen
            max_area = max(max_area, current_area)
            
            # MOVE: Advance the pointer pointing to the shorter line
            # This is the greedy choice - moving the taller line cannot help
            # because the area is already bounded by the shorter line
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        
        return max_area


# ============================================
# Solution 2: Two Pointers with Skip Optimization
# Time: O(n), Space: O(1)
#   - Same time complexity as basic two pointers
#   - Skips consecutive heights that cannot improve answer
#   - May reduce constant factors in practice
# ============================================
class SolutionTwoPointersOptimized:
    """
    Optimized version that skips lines that cannot improve the answer.
    
    If we move left and the new height is still <= previous height,
    the area cannot improve (both width and height decreased or stayed same).
    """
    
    def maxArea(self, height: List[int]) -> int:
        left: int = 0
        right: int = len(height) - 1
        max_area: int = 0
        
        while left < right:
            # Calculate current area
            h: int = min(height[left], height[right])
            max_area = max(max_area, h * (right - left))
            
            # Move pointer(s), skipping heights that can't improve
            if height[left] < height[right]:
                current_left_height = height[left]
                while left < right and height[left] <= current_left_height:
                    left += 1
            else:
                current_right_height = height[right]
                while left < right and height[right] <= current_right_height:
                    right -= 1
        
        return max_area


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers representing heights
    
    Output format:
        Single integer: maximum area
    
    Example:
        Input:  1 8 6 2 5 4 8 3 7
        Output: 49
    """
    import sys
    
    line = sys.stdin.read().strip()
    height = list(map(int, line.split()))
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.maxArea(height)
    
    print(result)


if __name__ == "__main__":
    solve()

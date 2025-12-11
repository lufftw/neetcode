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


# ============================================================================
# Solution - O(n) Opposite Pointers
# ============================================================================

class Solution:
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


# ============================================================================
# Alternative: With Skip Optimization
# ============================================================================

class SolutionOptimized:
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
    
    solution = Solution()
    result = solution.maxArea(height)
    
    print(result)


if __name__ == "__main__":
    solve()


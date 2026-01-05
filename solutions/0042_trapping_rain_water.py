"""
Problem: Trapping Rain Water
Link: https://leetcode.com/problems/trapping-rain-water/

Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

Example 1:

    Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
    Output: 6
    Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

Example 2:

    Input: height = [4,2,0,3,2,5]
    Output: 9


Constraints:

- n == height.length

- 1 <= n <= 2 * 10^4

- 0 <= height[i] <= 10^5

Topics: Array, Two Pointers, Dynamic Programming, Stack, Monotonic Stack
"""


from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionMonotonicStack",
        "method": "trap",
        "complexity": "O(n) time, O(n) space",
        "description": "Monotonic decreasing stack with valley resolution",
    },
    "stack": {
        "class": "SolutionMonotonicStack",
        "method": "trap",
        "complexity": "O(n) time, O(n) space",
        "description": "Monotonic decreasing stack with valley resolution",
    },
    "twopointer": {
        "class": "SolutionTwoPointers",
        "method": "trap",
        "complexity": "O(n) time, O(1) space",
        "description": "Two pointers with running max boundaries",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "trap",
        "complexity": "O(n) time, O(n) space",
        "description": "Precomputed left_max and right_max arrays",
    },
}


# ============================================================================
# Solution 1: Monotonic Decreasing Stack (Valley Resolution)
# Time: O(n), Space: O(n)
#   - Maintain stack of indices with decreasing heights
#   - When taller bar seen, resolve valleys layer by layer
#   - Each pop completes a "container" between left wall, bottom, right wall
#   - Water width = current_idx - left_wall_idx - 1
#   - Water height = min(left_wall, right_wall) - bottom_height
#
# Key Insight: Each pop finalizes a horizontal layer of water. The stack
# ensures we process valleys from bottom to top, accumulating water layer
# by layer as we find increasingly tall bounding walls.
# ============================================================================
class SolutionMonotonicStack:
    def trap(self, height: List[int]) -> int:
        trapped_water = 0
        index_stack: list[int] = []  # Indices with decreasing heights

        for current_idx, current_height in enumerate(height):
            # Process all valley bottoms that current bar can bound
            while index_stack and height[index_stack[-1]] < current_height:
                valley_bottom_idx = index_stack.pop()

                if not index_stack:
                    # No left wall, water flows out to the left
                    break

                left_wall_idx = index_stack[-1]
                left_wall_height = height[left_wall_idx]
                right_wall_height = current_height
                bottom_height = height[valley_bottom_idx]

                # Compute water trapped in this horizontal layer
                water_width = current_idx - left_wall_idx - 1
                bounded_height = min(left_wall_height, right_wall_height) - bottom_height
                trapped_water += water_width * bounded_height

            index_stack.append(current_idx)

        return trapped_water


# ============================================================================
# Solution 2: Two Pointers with Running Max
# Time: O(n), Space: O(1)
#   - Maintain left and right pointers, and their respective max heights
#   - Water at position = min(left_max, right_max) - height[position]
#   - Move the pointer on the side with smaller max (it determines the bound)
#
# Key Insight: Water level at any position is bounded by the minimum of
# left_max and right_max. By always advancing the smaller side, we ensure
# the other side's max is >= current side's max, making calculation safe.
# ============================================================================
class SolutionTwoPointers:
    def trap(self, height: List[int]) -> int:
        if len(height) <= 2:
            return 0

        trapped_water = 0
        left_ptr, right_ptr = 0, len(height) - 1
        left_max, right_max = height[left_ptr], height[right_ptr]

        while left_ptr < right_ptr:
            if left_max <= right_max:
                # Left side is the constraining boundary
                left_ptr += 1
                left_max = max(left_max, height[left_ptr])
                # Water bounded by left_max (since left_max <= right_max)
                trapped_water += left_max - height[left_ptr]
            else:
                # Right side is the constraining boundary
                right_ptr -= 1
                right_max = max(right_max, height[right_ptr])
                trapped_water += right_max - height[right_ptr]

        return trapped_water


# ============================================================================
# Solution 3: Dynamic Programming (Precomputed Boundaries)
# Time: O(n), Space: O(n)
#   - Precompute left_max[i] = max height in [0, i]
#   - Precompute right_max[i] = max height in [i, n-1]
#   - Water at i = min(left_max[i], right_max[i]) - height[i]
#
# Trade-off: Most intuitive approach, but uses O(n) extra space.
# Good for understanding before optimizing to two-pointer solution.
# ============================================================================
class SolutionDP:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        array_length = len(height)

        # left_max[i] = tallest bar from index 0 to i (inclusive)
        left_max = [0] * array_length
        left_max[0] = height[0]
        for i in range(1, array_length):
            left_max[i] = max(left_max[i - 1], height[i])

        # right_max[i] = tallest bar from index i to n-1 (inclusive)
        right_max = [0] * array_length
        right_max[-1] = height[-1]
        for i in range(array_length - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])

        # Compute water at each position
        trapped_water = 0
        for i in range(array_length):
            water_level = min(left_max[i], right_max[i])
            trapped_water += water_level - height[i]

        return trapped_water


def solve():
    """
    Input format (JSON literal, one per line):
        height: List[int]

    Output: int
    """
    import sys
    import json

    data = sys.stdin.read().strip().split('\n')

    height = json.loads(data[0].strip())

    solver = get_solver(SOLUTIONS)
    result = solver.trap(height)

    print(result)


if __name__ == "__main__":
    solve()

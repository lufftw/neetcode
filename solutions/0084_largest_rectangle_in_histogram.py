"""
Problem: Largest Rectangle in Histogram
Link: https://leetcode.com/problems/largest-rectangle-in-histogram/

Given an array of integers heights representing the histogram's bar height
where the width of each bar is 1, return the area of the largest rectangle
in the histogram.

Constraints:
- 1 <= heights.length <= 10^5
- 0 <= heights[i] <= 10^4

Topics: Array, Stack, Monotonic Stack
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionSinglePassSentinel",
        "method": "largestRectangleArea",
        "complexity": "O(n) time, O(n) space",
        "description": "Single-pass with sentinel for complete resolution",
    },
    "sentinel": {
        "class": "SolutionSinglePassSentinel",
        "method": "largestRectangleArea",
        "complexity": "O(n) time, O(n) space",
        "description": "Single-pass with sentinel for complete resolution",
    },
    "twopass": {
        "class": "SolutionTwoPass",
        "method": "largestRectangleArea",
        "complexity": "O(n) time, O(n) space",
        "description": "Two-pass boundary precomputation",
    },
}


# ============================================================================
# Solution 1: Single-Pass with Sentinel
# Time: O(n), Space: O(n)
#   - Append height 0 as sentinel to force complete stack flush
#   - Stack stores indices with monotonically increasing heights
#   - When smaller height seen, pop and compute area with popped height
#   - Width = current_idx - stack_top - 1 (left boundary from remaining stack)
#
# Key Insight: Each bar's maximum rectangle is determined by its left and
# right boundaries (first shorter bar on each side). The stack maintains
# candidates; when we pop, the current bar is right boundary, stack top is left.
# ============================================================================
class SolutionSinglePassSentinel:
    def largestRectangleArea(self, heights: List[int]) -> int:
        # Sentinel: height 0 forces all remaining bars to be popped
        heights_with_sentinel = heights + [0]
        max_rectangle_area = 0

        # Stack stores indices; -1 serves as virtual left boundary
        index_stack: list[int] = [-1]

        for current_idx, current_height in enumerate(heights_with_sentinel):
            # Pop bars that are taller than current (they found right boundary)
            while index_stack[-1] != -1 and heights[index_stack[-1]] > current_height:
                popped_idx = index_stack.pop()
                popped_height = heights[popped_idx]

                # Width: from left boundary (exclusive) to right boundary (exclusive)
                left_boundary = index_stack[-1]
                rectangle_width = current_idx - left_boundary - 1

                rectangle_area = popped_height * rectangle_width
                max_rectangle_area = max(max_rectangle_area, rectangle_area)

            index_stack.append(current_idx)

        return max_rectangle_area


# ============================================================================
# Solution 2: Two-Pass Boundary Precomputation
# Time: O(n), Space: O(n)
#   - First pass: compute left boundary (previous smaller) for each bar
#   - Second pass: compute right boundary (next smaller) for each bar
#   - Final pass: compute area for each bar using precomputed boundaries
#
# Trade-off: More memory for boundary arrays, but logic is more explicit.
# Useful for problems needing both boundaries for other computations.
# ============================================================================
class SolutionTwoPass:
    def largestRectangleArea(self, heights: List[int]) -> int:
        num_bars = len(heights)

        # left_boundary[i] = index of first shorter bar to the left (-1 if none)
        left_boundary = [-1] * num_bars

        # right_boundary[i] = index of first shorter bar to the right (n if none)
        right_boundary = [num_bars] * num_bars

        # Pass 1: Compute left boundaries (previous smaller element)
        index_stack: list[int] = []
        for i in range(num_bars):
            while index_stack and heights[index_stack[-1]] >= heights[i]:
                index_stack.pop()
            left_boundary[i] = index_stack[-1] if index_stack else -1
            index_stack.append(i)

        # Pass 2: Compute right boundaries (next smaller element)
        index_stack = []
        for i in range(num_bars - 1, -1, -1):
            while index_stack and heights[index_stack[-1]] >= heights[i]:
                index_stack.pop()
            right_boundary[i] = index_stack[-1] if index_stack else num_bars
            index_stack.append(i)

        # Compute maximum area using precomputed boundaries
        max_rectangle_area = 0
        for i in range(num_bars):
            width = right_boundary[i] - left_boundary[i] - 1
            area = heights[i] * width
            max_rectangle_area = max(max_rectangle_area, area)

        return max_rectangle_area


def solve():
    """
    Input format (JSON):
        Line 1: heights as JSON array

    Output format:
        Maximum rectangle area as integer
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    heights = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.largestRectangleArea(heights)

    print(result)


if __name__ == "__main__":
    solve()

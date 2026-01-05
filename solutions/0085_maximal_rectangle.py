"""
Problem: Maximal Rectangle
Link: https://leetcode.com/problems/maximal-rectangle/

Given a rows x cols binary matrix filled with 0's and 1's, find the largest
rectangle containing only 1's and return its area.

Constraints:
- rows == matrix.length
- cols == matrix[i].length
- 1 <= rows, cols <= 200
- matrix[i][j] is '0' or '1'

Topics: Array, Dynamic Programming, Stack, Matrix, Monotonic Stack
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionHistogramStack",
        "method": "maximalRectangle",
        "complexity": "O(rows * cols) time, O(cols) space",
        "description": "Row-by-row histogram with monotonic stack",
    },
    "stack": {
        "class": "SolutionHistogramStack",
        "method": "maximalRectangle",
        "complexity": "O(rows * cols) time, O(cols) space",
        "description": "Row-by-row histogram with monotonic stack",
    },
    "dp": {
        "class": "SolutionDP",
        "method": "maximalRectangle",
        "complexity": "O(rows * cols) time, O(cols) space",
        "description": "DP tracking height, left, and right boundaries",
    },
}


# ============================================================================
# Solution 1: Row-by-Row Histogram with Monotonic Stack
# Time: O(rows * cols), Space: O(cols)
#   - Transform each row into a histogram: height[j] = consecutive 1s above
#   - Apply "Largest Rectangle in Histogram" to each row's histogram
#   - Maximum across all rows is the answer
#
# Key Insight: A 2D matrix can be decomposed into n 1D histogram problems.
# For each row, the histogram height at column j is the count of consecutive
# 1s directly above (including current cell). This reduces 2D to 1D elegantly.
# ============================================================================
class SolutionHistogramStack:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        num_cols = len(matrix[0])
        histogram_heights = [0] * num_cols
        max_rectangle_area = 0

        for row in matrix:
            # Update histogram: extend height for '1', reset for '0'
            for col_idx in range(num_cols):
                if row[col_idx] == "1":
                    histogram_heights[col_idx] += 1
                else:
                    histogram_heights[col_idx] = 0

            # Compute largest rectangle in current histogram
            row_max_area = self._largest_rectangle_in_histogram(histogram_heights)
            max_rectangle_area = max(max_rectangle_area, row_max_area)

        return max_rectangle_area

    def _largest_rectangle_in_histogram(self, heights: List[int]) -> int:
        """Standard monotonic stack solution for histogram problem."""
        heights_with_sentinel = heights + [0]
        max_area = 0
        index_stack: list[int] = [-1]

        for current_idx, current_height in enumerate(heights_with_sentinel):
            while index_stack[-1] != -1 and heights[index_stack[-1]] > current_height:
                popped_idx = index_stack.pop()
                width = current_idx - index_stack[-1] - 1
                area = heights[popped_idx] * width
                max_area = max(max_area, area)
            index_stack.append(current_idx)

        return max_area


# ============================================================================
# Solution 2: Dynamic Programming with Boundaries
# Time: O(rows * cols), Space: O(cols)
#   - For each cell, track: height (consecutive 1s above)
#   - Also track left/right boundaries (leftmost/rightmost column where
#     rectangle of this height can extend)
#   - Area at each cell = height * (right - left)
#
# Key Insight: Instead of recomputing boundaries per row, we can update them
# incrementally. Left boundary expands only if current row allows; right
# boundary contracts only if current row restricts.
# ============================================================================
class SolutionDP:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        num_cols = len(matrix[0])

        # height[j] = consecutive 1s above current cell in column j
        height = [0] * num_cols

        # left[j] = leftmost column where rectangle of height[j] can start
        left_boundary = [0] * num_cols

        # right[j] = rightmost column (exclusive) where rectangle can end
        right_boundary = [num_cols] * num_cols

        max_rectangle_area = 0

        for row in matrix:
            # Track current row's leftmost 1 and rightmost 1
            current_left = 0
            current_right = num_cols

            # Update heights and left boundaries (left to right)
            for col_idx in range(num_cols):
                if row[col_idx] == "1":
                    height[col_idx] += 1
                    # Left boundary is max of previous and current row's constraint
                    left_boundary[col_idx] = max(left_boundary[col_idx], current_left)
                else:
                    height[col_idx] = 0
                    left_boundary[col_idx] = 0
                    current_left = col_idx + 1

            # Update right boundaries (right to left)
            for col_idx in range(num_cols - 1, -1, -1):
                if row[col_idx] == "1":
                    # Right boundary is min of previous and current row's constraint
                    right_boundary[col_idx] = min(right_boundary[col_idx], current_right)
                else:
                    right_boundary[col_idx] = num_cols
                    current_right = col_idx

            # Compute area for each column
            for col_idx in range(num_cols):
                width = right_boundary[col_idx] - left_boundary[col_idx]
                area = height[col_idx] * width
                max_rectangle_area = max(max_rectangle_area, area)

        return max_rectangle_area


def solve():
    """
    Input format (JSON):
        Line 1: matrix as 2D JSON array of "0"/"1" strings

    Output format:
        Maximum rectangle area as integer
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    matrix = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.maximalRectangle(matrix)

    print(result)


if __name__ == "__main__":
    solve()

"""
Problem: Maximum Strictly Increasing Cells in a Matrix
Link: https://leetcode.com/problems/maximum-strictly-increasing-cells-in-a-matrix/

Given a 1-indexed m x n integer matrix mat, you can select any cell as your
starting cell. From the starting cell, you can move to any other cell in the
same row or column, but only if the value of the destination cell is strictly
greater than the value of the current cell.

You can repeat this process as many times as possible, moving from cell to cell
until you can no longer make any moves.

Return the maximum number of cells that you can visit by starting from some cell.

Example 1:
    Input: mat = [[3,1],[3,4]]
    Output: 2

Example 2:
    Input: mat = [[1,1],[1,1]]
    Output: 1

Example 3:
    Input: mat = [[3,1,6],[-9,5,7]]
    Output: 4

Constraints:
- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 10^5
- 1 <= m * n <= 10^5
- -10^5 <= mat[i][j] <= 10^5

Topics: Array, Binary Search, Dynamic Programming, Matrix, Sorting
"""
from typing import List
from collections import defaultdict
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "maxIncreasingCells",
        "complexity": "O(m*n*log(m*n)) time, O(m*n) space",
        "description": "Sort by value + DP with row/col max tracking",
    },
}


# ============================================================================
# Solution: Sort by Value + Dynamic Programming
# Time: O(m*n*log(m*n)), Space: O(m*n)
#
# Key insight: Process cells in order of increasing value. For each cell (i,j),
# the max path length ending at this cell is: 1 + max(best in row i, best in col j)
# where "best" only considers cells with SMALLER values (already processed).
#
# We maintain row_max[i] and col_max[j] to track the maximum path length
# that ended at any cell in row i or column j (with value < current).
#
# Important: When multiple cells have the same value, we must process them
# as a batch - compute all their DP values before updating row_max/col_max.
# ============================================================================
class Solution:
    def maxIncreasingCells(self, mat: List[List[int]]) -> int:
        """
        Find maximum number of cells visitiable on a strictly increasing path.

        Strategy:
        1. Group cells by their value
        2. Process values in ascending order
        3. For each cell, dp[i][j] = 1 + max(row_max[i], col_max[j])
        4. After processing all cells of same value, update row/col max

        The batch processing for same-value cells is crucial because we can
        only move to STRICTLY greater values, not equal values.

        Args:
            mat: The input matrix

        Returns:
            Maximum number of cells on any valid path
        """
        m, n = len(mat), len(mat[0])

        # Group cells by value: value -> list of (row, col)
        cells_by_value = defaultdict(list)
        for i in range(m):
            for j in range(n):
                cells_by_value[mat[i][j]].append((i, j))

        # Track max path length ending in each row/column
        row_max = [0] * m
        col_max = [0] * n

        result = 1

        # Process values in ascending order
        for val in sorted(cells_by_value.keys()):
            cells = cells_by_value[val]

            # Compute DP for all cells with this value (before updating max)
            # dp_vals[k] = DP value for cells[k]
            dp_vals = []
            for i, j in cells:
                dp = 1 + max(row_max[i], col_max[j])
                dp_vals.append(dp)
                result = max(result, dp)

            # Now update row_max and col_max
            # Multiple cells with same value might be in same row/col
            for k, (i, j) in enumerate(cells):
                row_max[i] = max(row_max[i], dp_vals[k])
                col_max[j] = max(col_max[j], dp_vals[k])

        return result


def solve():
    """
    Input format:
    Line 1: mat (JSON 2D array)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    mat = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.maxIncreasingCells(mat)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

"""
Problem: Set Matrix Zeroes
Link: https://leetcode.com/problems/set-matrix-zeroes/

Given an m x n integer matrix matrix, if an element is 0, set its entire row
and column to 0's.

You must do it in place.

Example 1:
    Input: matrix = [[1,1,1],[1,0,1],[1,1,1]]
    Output: [[1,0,1],[0,0,0],[1,0,1]]

Example 2:
    Input: matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
    Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]

Constraints:
- m == matrix.length
- n == matrix[0].length
- 1 <= m, n <= 200
- -2^31 <= matrix[i][j] <= 2^31 - 1

Follow-up:
- O(mn) space is straightforward but not optimal
- O(m+n) space is better
- O(1) space is the challenge

Topics: Array, Hash Table, Matrix
"""
import json
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionConstant",
        "method": "setZeroes",
        "complexity": "O(m*n) time, O(1) space",
        "description": "Use first row/column as markers",
    },
    "constant": {
        "class": "SolutionConstant",
        "method": "setZeroes",
        "complexity": "O(m*n) time, O(1) space",
        "description": "Use first row/column as markers",
    },
    "sets": {
        "class": "SolutionSets",
        "method": "setZeroes",
        "complexity": "O(m*n) time, O(m+n) space",
        "description": "Track zero rows/columns in sets",
    },
}


# ============================================================================
# Solution 1: O(1) Space - First Row/Column as Markers
# Time: O(m*n), Space: O(1)
#   - Use matrix[0][j] to mark column j needs zeroing
#   - Use matrix[i][0] to mark row i needs zeroing
#   - Special handling for first row/column (they overlap at [0][0])
# ============================================================================
class SolutionConstant:
    """
    Constant space solution using first row/column as markers.

    The key insight is we can repurpose the first row and first column
    to store which rows/columns need to be zeroed.

    Problem: matrix[0][0] is shared by both first row and first column.
    Solution: Use separate flag for first column; [0][0] marks first row.

    Algorithm:
    1. Check if first row/column have zeros (store in flags)
    2. Use first row/column as markers for rest of matrix
    3. Zero cells based on markers (skip first row/column)
    4. Zero first row/column based on saved flags
    """

    def setZeroes(self, matrix: List[List[int]]) -> None:
        if not matrix or not matrix[0]:
            return

        rows, cols = len(matrix), len(matrix[0])

        # Flags for first row and first column
        first_row_has_zero = any(matrix[0][j] == 0 for j in range(cols))
        first_col_has_zero = any(matrix[i][0] == 0 for i in range(rows))

        # Use first row/column as markers for remaining cells
        for i in range(1, rows):
            for j in range(1, cols):
                if matrix[i][j] == 0:
                    matrix[0][j] = 0  # Mark column
                    matrix[i][0] = 0  # Mark row

        # Zero cells based on markers (skip first row/column)
        for i in range(1, rows):
            for j in range(1, cols):
                if matrix[0][j] == 0 or matrix[i][0] == 0:
                    matrix[i][j] = 0

        # Zero first row if needed
        if first_row_has_zero:
            for j in range(cols):
                matrix[0][j] = 0

        # Zero first column if needed
        if first_col_has_zero:
            for i in range(rows):
                matrix[i][0] = 0


# ============================================================================
# Solution 2: O(m+n) Space - Sets for Rows and Columns
# Time: O(m*n), Space: O(m+n)
#   - Track which rows and columns contain zeros
#   - Second pass: zero all cells in marked rows/columns
# ============================================================================
class SolutionSets:
    """
    Use sets to track which rows and columns need zeroing.

    Simple two-pass approach:
    1. First pass: collect all row/column indices containing zero
    2. Second pass: set cells to zero if their row or column is marked

    More intuitive but uses O(m+n) extra space.
    """

    def setZeroes(self, matrix: List[List[int]]) -> None:
        if not matrix or not matrix[0]:
            return

        rows, cols = len(matrix), len(matrix[0])
        zero_rows = set()
        zero_cols = set()

        # First pass: find all zero positions
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == 0:
                    zero_rows.add(i)
                    zero_cols.add(j)

        # Second pass: set zeros
        for i in range(rows):
            for j in range(cols):
                if i in zero_rows or j in zero_cols:
                    matrix[i][j] = 0


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: matrix as JSON 2D array

    Output format:
        Modified matrix as JSON 2D array

    Example:
        [[1,1,1],[1,0,1],[1,1,1]]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    matrix = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    solver.setZeroes(matrix)

    print(json.dumps(matrix, separators=(',', ':')))


if __name__ == "__main__":
    solve()

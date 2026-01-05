"""
Problem: Range Sum Query 2D - Immutable
Link: https://leetcode.com/problems/range-sum-query-2d-immutable/

Given a 2D matrix matrix, handle multiple queries of the following type:
Calculate the sum of the elements of matrix inside the rectangle defined by
its upper left corner (row1, col1) and lower right corner (row2, col2).

Implement the NumMatrix class:
- NumMatrix(int[][] matrix) Initializes the object with the integer matrix.
- int sumRegion(int row1, int col1, int row2, int col2) Returns the sum of the
  elements of matrix inside the rectangle defined by corners.

Example 1:
    Input: ["NumMatrix", "sumRegion", "sumRegion", "sumRegion"]
           [[[[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]]],
            [2,1,4,3],[1,1,2,2],[1,2,2,4]]
    Output: [null, 8, 11, 12]

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 200
- -10^4 <= matrix[i][j] <= 10^4
- 0 <= row1 <= row2 < m
- 0 <= col1 <= col2 < n
- At most 10^4 calls will be made to sumRegion.

Topics: Array, Design, Matrix, Prefix Sum
"""

import json
from typing import List


SOLUTIONS = {
    "default": {
        "class": "NumMatrix",
        "method": "sumRegion",
        "complexity": "O(m*n) init, O(1) query, O(m*n) space",
        "description": "2D prefix sum for O(1) rectangle sum queries",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate result for design class problems."""
    lines = input_data.strip().split("\n")
    commands = json.loads(lines[0])
    args_list = json.loads(lines[1])

    correct = _reference_solution(commands, args_list)

    if isinstance(actual, list):
        actual_list = actual
    else:
        actual_str = actual.strip()
        try:
            actual_list = json.loads(actual_str) if actual_str else []
        except (ValueError, json.JSONDecodeError):
            return False

    return actual_list == correct


def _reference_solution(commands: List[str], args_list: List[List]) -> List:
    """Reference implementation."""
    results = []
    obj = None

    for cmd, args in zip(commands, args_list):
        if cmd == "NumMatrix":
            obj = _RefNumMatrix(args[0])
            results.append(None)
        elif cmd == "sumRegion":
            results.append(obj.sumRegion(args[0], args[1], args[2], args[3]))

    return results


class _RefNumMatrix:
    """Reference implementation for validation."""

    def __init__(self, matrix: List[List[int]]):
        if not matrix or not matrix[0]:
            self.prefix = [[0]]
            return

        m, n = len(matrix), len(matrix[0])
        self.prefix = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                self.prefix[i][j] = (
                    matrix[i - 1][j - 1]
                    + self.prefix[i - 1][j]
                    + self.prefix[i][j - 1]
                    - self.prefix[i - 1][j - 1]
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self.prefix[row2 + 1][col2 + 1]
            - self.prefix[row1][col2 + 1]
            - self.prefix[row2 + 1][col1]
            + self.prefix[row1][col1]
        )


JUDGE_FUNC = judge


# ============================================================================
# Solution: 2D Prefix Sum Matrix
# Time: O(m*n) initialization, O(1) per query
# Space: O(m*n) for prefix sum matrix
#   - prefix[i][j] = sum of all elements in rectangle (0,0) to (i-1,j-1)
#   - Use inclusion-exclusion principle for rectangle sum queries
#   - Formula: sumRegion = prefix[r2+1][c2+1] - prefix[r1][c2+1]
#                         - prefix[r2+1][c1] + prefix[r1][c1]
#
# Key Insight: 2D prefix sum extends 1D concept using inclusion-exclusion.
# Visualize as overlapping rectangles: total minus two strips plus corner.
#
# Building prefix[i][j]:
#   prefix[i][j] = matrix[i-1][j-1] + prefix[i-1][j] + prefix[i][j-1]
#                  - prefix[i-1][j-1]
# We add top and left, subtract top-left corner (counted twice).
#
# Pattern: prefix_sum_2d
# See: docs/patterns/prefix_sum/templates.md Section 5 (2D Prefix Sum)
# ============================================================================
class NumMatrix:
    """
    2D range sum query with O(m*n) preprocessing and O(1) queries.

    Extends 1D prefix sum to 2D using the inclusion-exclusion principle.
    """

    def __init__(self, matrix: List[List[int]]):
        """
        Build 2D prefix sum matrix in O(m*n) time.

        prefix[i][j] = sum of rectangle from (0,0) to (i-1,j-1).
        Extra row and column of zeros simplify boundary handling.
        """
        if not matrix or not matrix[0]:
            self.prefix_sum = [[0]]
            return

        row_count, col_count = len(matrix), len(matrix[0])

        # Extra row and column of zeros for boundary handling
        self.prefix_sum = [[0] * (col_count + 1) for _ in range(row_count + 1)]

        # Build prefix sum using inclusion-exclusion
        for row in range(1, row_count + 1):
            for col in range(1, col_count + 1):
                self.prefix_sum[row][col] = (
                    matrix[row - 1][col - 1]
                    + self.prefix_sum[row - 1][col]      # Top rectangle
                    + self.prefix_sum[row][col - 1]      # Left rectangle
                    - self.prefix_sum[row - 1][col - 1]  # Subtract overlap
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        """
        Return sum of rectangle (row1,col1) to (row2,col2) in O(1).

        Uses inclusion-exclusion:
        ┌─────────────────────────┐
        │  A  │        B          │
        ├─────┼──────────┬────────┤
        │     │ ████████ │        │
        │  C  │ █TARGET█ │   D    │
        │     │ ████████ │        │
        ├─────┴──────────┴────────┤
        │           E             │
        └─────────────────────────┘

        Target = Total - B - C + A (A was subtracted twice)
        """
        return (
            self.prefix_sum[row2 + 1][col2 + 1]  # Total (origin to bottom-right)
            - self.prefix_sum[row1][col2 + 1]    # Subtract top strip
            - self.prefix_sum[row2 + 1][col1]    # Subtract left strip
            + self.prefix_sum[row1][col1]        # Add back top-left (subtracted twice)
        )


def solve():
    """
    Input format (JSON per line):
        Line 1: List of commands ["NumMatrix", "sumRegion", ...]
        Line 2: List of arguments [[[matrix]], [row1, col1, row2, col2], ...]

    Output format:
        JSON array of results [null, result1, result2, ...]
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    commands = json.loads(lines[0])
    args_list = json.loads(lines[1])

    results = []
    obj = None

    for cmd, args in zip(commands, args_list):
        if cmd == "NumMatrix":
            obj = NumMatrix(args[0])
            results.append(None)
        elif cmd == "sumRegion":
            results.append(obj.sumRegion(args[0], args[1], args[2], args[3]))

    print(json.dumps(results))


if __name__ == "__main__":
    solve()

"""
Problem: Spiral Matrix
Link: https://leetcode.com/problems/spiral-matrix/

Given an m x n matrix, return all elements of the matrix in spiral order.

Example 1:
    Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
    Output: [1,2,3,6,9,8,7,4,5]

Example 2:
    Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
    Output: [1,2,3,4,8,12,11,10,9,5,6,7]

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 10
- -100 <= matrix[i][j] <= 100

Topics: Array, Matrix, Simulation
"""
import json
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionBoundary",
        "method": "spiralOrder",
        "complexity": "O(m*n) time, O(1) space",
        "description": "Layer-by-layer boundary traversal",
    },
    "boundary": {
        "class": "SolutionBoundary",
        "method": "spiralOrder",
        "complexity": "O(m*n) time, O(1) space",
        "description": "Layer-by-layer boundary traversal",
    },
    "direction": {
        "class": "SolutionDirection",
        "method": "spiralOrder",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "Direction-based simulation with visited tracking",
    },
}


# ============================================================================
# Solution 1: Boundary Layer Traversal
# Time: O(m*n), Space: O(1) excluding output
#   - Process matrix layer by layer from outside to inside
#   - Each layer: right -> down -> left -> up
#   - Shrink boundaries after each layer
# ============================================================================
class SolutionBoundary:
    """
    Layer-by-layer boundary traversal - clean and intuitive.

    We maintain four boundaries (top, bottom, left, right) and process
    each layer in order: traverse right along top row, down right column,
    left along bottom row, up left column. Then shrink boundaries inward.

    Key insight: After moving right and down, we must check if boundaries
    still valid before moving left and up (handles single row/column cases).
    """

    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix or not matrix[0]:
            return []

        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            # Traverse right along top row
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1

            # Traverse down along right column
            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1

            # Traverse left along bottom row (if rows remain)
            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1

            # Traverse up along left column (if columns remain)
            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1

        return result


# ============================================================================
# Solution 2: Direction-Based Simulation
# Time: O(m*n), Space: O(m*n) for visited set
#   - Start at (0,0), move in current direction
#   - When hitting boundary or visited cell, turn right (clockwise)
#   - Continue until all cells visited
# ============================================================================
class SolutionDirection:
    """
    Direction-based simulation with clockwise turns.

    We simulate walking through the matrix. When we hit a wall or a
    previously visited cell, we turn 90 degrees clockwise.

    Direction order (clockwise): right -> down -> left -> up
    This naturally creates the spiral pattern.
    """

    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix or not matrix[0]:
            return []

        rows, cols = len(matrix), len(matrix[0])
        total = rows * cols

        # Direction vectors: right, down, left, up (clockwise order)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        dir_idx = 0  # Start moving right

        visited = [[False] * cols for _ in range(rows)]
        result = []

        row, col = 0, 0

        for _ in range(total):
            result.append(matrix[row][col])
            visited[row][col] = True

            # Try to continue in current direction
            next_row = row + directions[dir_idx][0]
            next_col = col + directions[dir_idx][1]

            # If out of bounds or already visited, turn clockwise
            if (next_row < 0 or next_row >= rows or
                next_col < 0 or next_col >= cols or
                visited[next_row][next_col]):
                dir_idx = (dir_idx + 1) % 4
                next_row = row + directions[dir_idx][0]
                next_col = col + directions[dir_idx][1]

            row, col = next_row, next_col

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: matrix as JSON 2D array

    Example:
        [[1,2,3],[4,5,6],[7,8,9]]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    matrix = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.spiralOrder(matrix)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

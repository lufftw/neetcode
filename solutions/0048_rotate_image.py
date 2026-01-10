"""
Problem: Rotate Image
Link: https://leetcode.com/problems/rotate-image/

You are given an n x n 2D matrix representing an image, rotate the image by
90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the
input 2D matrix directly. DO NOT allocate another 2D matrix.

Example 1:
    Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
    Output: [[7,4,1],[8,5,2],[9,6,3]]

Example 2:
    Input: matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
    Output: [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]

Constraints:
- n == matrix.length == matrix[i].length
- 1 <= n <= 20
- -1000 <= matrix[i][j] <= 1000

Topics: Array, Math, Matrix
"""
import json
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionTransposeReverse",
        "method": "rotate",
        "complexity": "O(n²) time, O(1) space",
        "description": "Transpose then reverse rows",
    },
    "transpose": {
        "class": "SolutionTransposeReverse",
        "method": "rotate",
        "complexity": "O(n²) time, O(1) space",
        "description": "Transpose then reverse rows",
    },
    "layer": {
        "class": "SolutionLayerRotation",
        "method": "rotate",
        "complexity": "O(n²) time, O(1) space",
        "description": "Rotate layer by layer",
    },
}


# ============================================================================
# Solution 1: Transpose + Reverse
# Time: O(n²), Space: O(1)
#   - Transpose: swap matrix[i][j] with matrix[j][i]
#   - Reverse each row
#   - Combined effect: 90° clockwise rotation
# ============================================================================
class SolutionTransposeReverse:
    """
    Transpose + Reverse approach - elegant and intuitive.

    Key insight: 90° clockwise rotation = transpose + reverse each row.

    Why this works:
    - Transpose flips the matrix along the main diagonal
    - Reversing rows then mirrors it horizontally
    - Together: each element moves from (i, j) to (j, n-1-i)

    Example for 3x3:
    Original:    Transpose:    Reverse rows:
    1 2 3        1 4 7         7 4 1
    4 5 6   ->   2 5 8    ->   8 5 2
    7 8 9        3 6 9         9 6 3

    Note: For counter-clockwise, reverse then transpose.
    """

    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)

        # Step 1: Transpose the matrix
        # Swap elements across the main diagonal
        for i in range(n):
            for j in range(i + 1, n):  # Only upper triangle to avoid double swap
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        # Step 2: Reverse each row
        for i in range(n):
            matrix[i].reverse()


# ============================================================================
# Solution 2: Layer by Layer Rotation
# Time: O(n²), Space: O(1)
#   - Rotate outer layer, then inner layers
#   - Each layer: 4 elements rotate in a cycle
# ============================================================================
class SolutionLayerRotation:
    """
    Layer-by-layer rotation - direct approach.

    Process the matrix from outer layers to inner layers.
    For each layer, rotate 4 elements at a time in a cycle:
        top -> right -> bottom -> left -> top

    For a 4x4 matrix:
    Layer 0 (outer): corners at (0,0), (0,3), (3,3), (3,0)
    Layer 1 (inner): corners at (1,1), (1,2), (2,2), (2,1)

    This approach directly performs the rotation without needing
    to understand the transpose+reverse decomposition.
    """

    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)

        # Process each layer from outside to inside
        # For n=4, we have layers 0 and 1
        # For n=5, we have layers 0, 1 (center element doesn't move)
        for layer in range(n // 2):
            first = layer
            last = n - 1 - layer

            # Rotate each position in this layer
            for i in range(first, last):
                offset = i - first

                # Save top element
                top = matrix[first][i]

                # Move left to top
                matrix[first][i] = matrix[last - offset][first]

                # Move bottom to left
                matrix[last - offset][first] = matrix[last][last - offset]

                # Move right to bottom
                matrix[last][last - offset] = matrix[i][last]

                # Move top (saved) to right
                matrix[i][last] = top


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

    # Parse JSON 2D array
    matrix = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    solver.rotate(matrix)  # In-place modification

    # Output the rotated matrix
    print(json.dumps(matrix, separators=(',', ':')))


if __name__ == "__main__":
    solve()

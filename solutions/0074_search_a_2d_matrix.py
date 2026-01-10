"""
Problem: Search a 2D Matrix
Link: https://leetcode.com/problems/search-a-2d-matrix/

You are given an m x n integer matrix matrix with the following two properties:
- Each row is sorted in non-decreasing order.
- The first integer of each row is greater than the last integer of the previous row.

Given an integer target, return true if target is in matrix or false otherwise.

You must write a solution in O(log(m * n)) time complexity.

Example 1:
    Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
    Output: true

Example 2:
    Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
    Output: false

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 100
- -10^4 <= matrix[i][j], target <= 10^4

Topics: Array, Binary Search, Matrix
"""
import json
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionSingleBinarySearch",
        "method": "searchMatrix",
        "complexity": "O(log(m*n)) time, O(1) space",
        "description": "Treat matrix as flattened sorted array",
    },
    "single": {
        "class": "SolutionSingleBinarySearch",
        "method": "searchMatrix",
        "complexity": "O(log(m*n)) time, O(1) space",
        "description": "Treat matrix as flattened sorted array",
    },
    "two_binary": {
        "class": "SolutionTwoBinarySearch",
        "method": "searchMatrix",
        "complexity": "O(log m + log n) time, O(1) space",
        "description": "Binary search row, then binary search column",
    },
}


# ============================================================================
# Solution 1: Single Binary Search (Flatten Conceptually)
# Time: O(log(m*n)), Space: O(1)
#   - Matrix is essentially a sorted 1D array split into rows
#   - Map 1D index to 2D: row = idx // n, col = idx % n
#   - Standard binary search on virtual 1D array
# ============================================================================
class SolutionSingleBinarySearch:
    """
    Treat the matrix as a flattened sorted array.

    Since each row is sorted and the first element of each row is greater
    than the last element of the previous row, the entire matrix is sorted
    when read row by row.

    We can apply binary search as if it were a 1D array of size m*n:
    - For index i, row = i // n, col = i % n
    - Search range: [0, m*n - 1]

    This achieves the required O(log(m*n)) complexity.
    """

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False

        rows, cols = len(matrix), len(matrix[0])
        left, right = 0, rows * cols - 1

        while left <= right:
            mid = (left + right) // 2
            # Convert 1D index to 2D coordinates
            row = mid // cols
            col = mid % cols
            value = matrix[row][col]

            if value == target:
                return True
            elif value < target:
                left = mid + 1
            else:
                right = mid - 1

        return False


# ============================================================================
# Solution 2: Two Binary Searches
# Time: O(log m + log n), Space: O(1)
#   - First binary search: find the row where target could be
#   - Second binary search: search within that row
# ============================================================================
class SolutionTwoBinarySearch:
    """
    Two-phase binary search approach.

    Phase 1: Binary search to find the correct row.
             Target is in row i if: matrix[i][0] <= target <= matrix[i][n-1]
             We find the largest row where matrix[row][0] <= target.

    Phase 2: Standard binary search within the identified row.

    Note: O(log m + log n) = O(log(m*n)) so complexity is equivalent.
    """

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False

        rows, cols = len(matrix), len(matrix[0])

        # Phase 1: Find the row using binary search
        # Find largest row where matrix[row][0] <= target
        top, bottom = 0, rows - 1
        while top <= bottom:
            mid = (top + bottom) // 2
            if matrix[mid][0] <= target <= matrix[mid][cols - 1]:
                # Target could be in this row, search it
                return self._binary_search_row(matrix[mid], target)
            elif matrix[mid][0] > target:
                bottom = mid - 1
            else:  # matrix[mid][cols - 1] < target
                top = mid + 1

        return False

    def _binary_search_row(self, row: List[int], target: int) -> bool:
        """Standard binary search within a row."""
        left, right = 0, len(row) - 1
        while left <= right:
            mid = (left + right) // 2
            if row[mid] == target:
                return True
            elif row[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return False


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: matrix as JSON 2D array
        Line 2: target as integer

    Example:
        [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
        3
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    matrix = json.loads(lines[0])
    target = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.searchMatrix(matrix, target)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

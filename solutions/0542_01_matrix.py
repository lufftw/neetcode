# solutions/0542_01_matrix.py
"""
Problem: 01 Matrix
Link: https://leetcode.com/problems/01-matrix/

Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell.
The distance between two adjacent cells is 1.

Example 1:
    Input: mat = [[0,0,0],[0,1,0],[0,0,0]]
    Output: [[0,0,0],[0,1,0],[0,0,0]]

Example 2:
    Input: mat = [[0,0,0],[0,1,0],[1,1,1]]
    Output: [[0,0,0],[0,1,0],[1,2,1]]

Constraints:
- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 10^4
- 1 <= m * n <= 10^4
- mat[i][j] is either 0 or 1
- There is at least one 0 in mat

Topics: Array, Dynamic Programming, Breadth First Search, Matrix
"""
from typing import List
from collections import deque
from _runner import get_solver


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate 01 Matrix solution."""
    import json

    # Parse input
    mat = json.loads(input_data.strip())

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected using reference solution
    expected_result = _compute_distance_matrix(mat)
    return actual == expected_result


def _compute_distance_matrix(mat: List[List[int]]) -> List[List[int]]:
    """Reference solution for validation."""
    rows, cols = len(mat), len(mat[0])
    dist = [[0 if mat[r][c] == 0 else float('inf')
             for c in range(cols)] for r in range(rows)]

    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                queue.append((r, c))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_dist = dist[r][c] + 1
                if new_dist < dist[nr][nc]:
                    dist[nr][nc] = new_dist
                    queue.append((nr, nc))

    return dist


JUDGE_FUNC = judge


# ============================================================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "updateMatrix",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "Multi-source BFS from all zeros",
        "api_kernels": ["GridBFSMultiSource"],
        "patterns": ["grid_bfs_propagation"],
    },
    "bfs": {
        "class": "Solution",
        "method": "updateMatrix",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "Multi-source BFS from all zeros",
        "api_kernels": ["GridBFSMultiSource"],
        "patterns": ["grid_bfs_propagation"],
    },
    "dp": {
        "class": "SolutionDP",
        "method": "updateMatrix",
        "complexity": "O(m*n) time, O(1) extra space",
        "description": "Two-pass DP: top-left then bottom-right",
        "api_kernels": ["DP2D"],
        "patterns": ["dp_grid_two_pass"],
    },
}


# ============================================================================
# Solution 1: Multi-Source BFS
# Time: O(m * n), Space: O(m * n)
#
# Pattern: GridBFSMultiSource - Distance Field
# Insight: All zeros are sources at distance 0. BFS from all zeros
#          simultaneously computes minimum distance to any zero for each cell.
# ============================================================================
class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        """
        Return matrix where each cell contains distance to nearest zero.

        Multi-source BFS approach:
        1. Initialize all zeros with distance 0, ones with infinity
        2. Add all zeros to queue
        3. BFS expansion: first reach guarantees minimum distance
        """
        rows, cols = len(mat), len(mat[0])
        queue = deque()

        # Phase 1: Initialize distance matrix
        # Zeros have distance 0 (they ARE zeros)
        # Ones start with infinity (will be updated by BFS)
        dist = [[0 if mat[r][c] == 0 else float('inf')
                 for c in range(cols)] for r in range(rows)]

        # Add all zeros to queue as BFS sources
        for r in range(rows):
            for c in range(cols):
                if mat[r][c] == 0:
                    queue.append((r, c))

        # Phase 2: BFS from all zeros simultaneously
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            r, c = queue.popleft()

            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if we found a shorter path
                    new_dist = dist[r][c] + 1
                    if new_dist < dist[nr][nc]:
                        dist[nr][nc] = new_dist
                        queue.append((nr, nc))

        return dist


# ============================================================================
# Solution 2: Two-Pass Dynamic Programming
# Time: O(m * n), Space: O(1) extra (modify in-place)
#
# Alternative approach that doesn't use BFS.
# Key insight: Distance to nearest zero can only come from 4 directions.
# We can compute in two passes:
#   Pass 1: Consider only top and left neighbors
#   Pass 2: Consider only bottom and right neighbors
# ============================================================================
class SolutionDP:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        """
        Two-pass DP to compute distance to nearest zero.

        Pass 1 (top-left to bottom-right):
        - dist[r][c] = min(dist[r][c], dist[r-1][c]+1, dist[r][c-1]+1)

        Pass 2 (bottom-right to top-left):
        - dist[r][c] = min(dist[r][c], dist[r+1][c]+1, dist[r][c+1]+1)
        """
        rows, cols = len(mat), len(mat[0])

        # Initialize: zeros stay 0, ones become large value
        MAX_DIST = rows + cols  # Maximum possible distance in grid
        dist = [[0 if mat[r][c] == 0 else MAX_DIST
                 for c in range(cols)] for r in range(rows)]

        # Pass 1: Top-left to bottom-right
        # Each cell gets min of itself, top neighbor + 1, left neighbor + 1
        for r in range(rows):
            for c in range(cols):
                if mat[r][c] == 1:  # Only update non-zero cells
                    if r > 0:
                        dist[r][c] = min(dist[r][c], dist[r - 1][c] + 1)
                    if c > 0:
                        dist[r][c] = min(dist[r][c], dist[r][c - 1] + 1)

        # Pass 2: Bottom-right to top-left
        # Each cell gets min of itself, bottom neighbor + 1, right neighbor + 1
        for r in range(rows - 1, -1, -1):
            for c in range(cols - 1, -1, -1):
                if mat[r][c] == 1:  # Only update non-zero cells
                    if r < rows - 1:
                        dist[r][c] = min(dist[r][c], dist[r + 1][c] + 1)
                    if c < cols - 1:
                        dist[r][c] = min(dist[r][c], dist[r][c + 1] + 1)

        return dist


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array mat (binary matrix)

    Output format:
    2D array with distances to nearest zero
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    mat = json.loads(lines[0])

    # Get solver and call method
    solver = get_solver(SOLUTIONS)
    result = solver.updateMatrix(mat)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

"""
Problem: Longest Increasing Path in a Matrix
Link: https://leetcode.com/problems/longest-increasing-path-in-a-matrix/

Given an m x n integers matrix, return the length of the longest increasing path
in matrix.

From each cell, you can either move in four directions: left, right, up, or down.
You may not move diagonally or move outside the boundary.

Example 1:
    Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
    Output: 4
    Explanation: The longest increasing path is [1, 2, 6, 9].

Example 2:
    Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
    Output: 4
    Explanation: The longest increasing path is [3, 4, 5, 6].

Example 3:
    Input: matrix = [[1]]
    Output: 1

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 200
- 0 <= matrix[i][j] <= 2^31 - 1

Topics: Array, Dynamic Programming, Depth-First Search, Breadth-First Search,
        Graph, Topological Sort, Memoization, Matrix
"""

import json
from typing import List
from functools import lru_cache
from collections import deque
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDFSMemo",
        "method": "longestIncreasingPath",
        "complexity": "O(mn) time, O(mn) space",
        "description": "DFS with memoization - each cell computed exactly once",
    },
    "topological": {
        "class": "SolutionTopological",
        "method": "longestIncreasingPath",
        "complexity": "O(mn) time, O(mn) space",
        "description": "Topological sort / BFS from smallest cells",
    },
}


# ============================================================================
# Solution 1: DFS with Memoization
# Time: O(mn), Space: O(mn)
#
# Key Insight:
#   The longest increasing path from any cell depends only on paths from
#   neighboring cells with larger values. This creates a DAG (directed acyclic
#   graph) structure because edges only go from smaller to larger values.
#
#   For DAGs, we can use DFS with memoization: the longest path from cell (i,j)
#   is 1 + max(longest paths from valid neighbors). Each cell is computed once.
#
# Why No Cycles:
#   Since we only move to strictly larger values, we can never return to a
#   visited cell. This guarantees no cycles, making memoization correct.
#
# Algorithm:
#   - For each cell, recursively compute longest path starting there
#   - Cache results in memo array
#   - Answer is maximum over all starting cells
# ============================================================================
class SolutionDFSMemo:
    """
    DFS with memoization exploiting the DAG structure.

    The strictly increasing constraint means no cycles exist, allowing us
    to memoize safely. Each cell stores the longest path starting from it,
    computed as 1 + max of paths from valid larger neighbors.
    """

    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        @lru_cache(maxsize=None)
        def dfs(row: int, col: int) -> int:
            """Return longest increasing path starting from (row, col)."""
            max_length = 1  # At minimum, the path includes this cell

            for dr, dc in directions:
                nr, nc = row + dr, col + dc

                # Check bounds and strictly increasing
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[row][col]:
                    max_length = max(max_length, 1 + dfs(nr, nc))

            return max_length

        # Find maximum path starting from any cell
        result = 0
        for i in range(m):
            for j in range(n):
                result = max(result, dfs(i, j))

        return result


# ============================================================================
# Solution 2: Topological Sort / BFS
# Time: O(mn), Space: O(mn)
#
# Key Insight:
#   View the matrix as a graph where edges go from smaller to larger values.
#   The longest path in a DAG can be found via topological sort: process
#   nodes in order, and for each node, update the path lengths of neighbors.
#
#   Alternatively, think of it as BFS from "leaf" nodes (cells with no smaller
#   neighbors). We process layer by layer, where each layer represents cells
#   at a certain path length from the leaves.
#
# Algorithm:
#   - Compute outdegree (count of larger neighbors) for each cell
#   - Start BFS from cells with outdegree 0 (no larger neighbors)
#   - Process level by level, counting levels
#   - When a cell's all incoming edges are processed, add it to queue
# ============================================================================
class SolutionTopological:
    """
    Topological sort approach using BFS from leaves.

    Process cells in reverse topological order (from largest to smallest
    path endpoints). Each BFS level represents one step in path length.
    The number of levels is the answer.
    """

    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Compute outdegree: count of neighbors with larger values
        outdegree = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                for dr, dc in directions:
                    ni, nj = i + dr, j + dc
                    if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                        outdegree[i][j] += 1

        # Start BFS from cells with outdegree 0 (path endpoints)
        queue = deque()
        for i in range(m):
            for j in range(n):
                if outdegree[i][j] == 0:
                    queue.append((i, j))

        # BFS level by level
        path_length = 0

        while queue:
            path_length += 1
            # Process all cells at current level
            for _ in range(len(queue)):
                row, col = queue.popleft()

                # Update neighbors with smaller values
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] < matrix[row][col]:
                        outdegree[nr][nc] -= 1
                        if outdegree[nr][nc] == 0:
                            queue.append((nr, nc))

        return path_length


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: matrix as JSON 2D array

    Example:
        [[9,9,4],[6,6,8],[2,1,1]]
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    matrix = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.longestIncreasingPath(matrix)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

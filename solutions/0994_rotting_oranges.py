# solutions/0994_rotting_oranges.py
"""
Problem: Rotting Oranges
Link: https://leetcode.com/problems/rotting-oranges/

You are given an m x n grid where each cell can have one of three values:
0 representing an empty cell,
1 representing a fresh orange, or
2 representing a rotten orange.
Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.
Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

Example 1:
    <img alt="" src="https://assets.leetcode.com/uploads/2019/02/16/oranges.png" style="width: 650px; height: 137px;" />
    Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
    Output: 4

Example 2:
    Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
    Output: -1
    Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.

Example 3:
    Input: grid = [[0,2]]
    Output: 0
    Explanation: Since there are already no fresh oranges at minute 0, the answer is just 0.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 10
- grid[i][j] is 0, 1, or 2.

Topics: Array, Breadth First Search, Matrix
"""
from typing import List
from collections import deque
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "orangesRotting",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "BFS approach",
    },
}


# ============================================
# Solution 1: BFS (Breadth-First Search)
# Time: O(m * n), Space: O(m * n)
#   - BFS traversal from all initial rotten oranges
#   - Queue stores positions of rotten oranges
#   - Each minute processes one level of BFS
# ============================================
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # Dimensions of the grid
        rows, cols = len(grid), len(grid[0])

        # Queue for BFS (store positions of rotten oranges)
        queue = deque()
        # Count of fresh oranges
        fresh = 0

        # Initialize queue with all rotten oranges and count the fresh ones
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 2:
                    queue.append((row, col))
                elif grid[row][col] == 1:
                    fresh += 1

        # If there are no fresh oranges from the beginning, no time is needed
        if fresh == 0:
            return 0

        # Directions for 4-neighbors: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        minutes = -1
        # Use level-order (BFS) traversal to compute how long it takes for all rotten oranges to spread.
        while queue:
            size = len(queue)

            for _ in range(size):
                row, col = queue.popleft()

                # Explore all four directions from the current cell
                for dr, dc in directions:
                    next_row = row + dr
                    next_col = col + dc

                    # Check boundaries and ensure the neighboring cell is fresh
                    if 0 <= next_row < rows and 0 <= next_col < cols:
                        if grid[next_row][next_col] == 1:
                            queue.append((next_row, next_col))  # Add newly rotted orange to queue
                            grid[next_row][next_col] = 2  # Mark as rotten
                            fresh -= 1  # Decrease count of remaining fresh oranges

            # One BFS layer corresponds to one minute of infection spread
            minutes += 1

        # If there are still fresh oranges, it's impossible to rot them all
        return minutes if fresh == 0 else -1


def solve():
    """
    Input format:
    Line 1: m (rows)
    Line 2: n (cols)
    Next m lines: n numbers separated by commas

    Example:
    3
    3
    2,1,1
    1,1,0
    0,1,1
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    m = int(lines[0])
    n = int(lines[1])

    grid = []
    for i in range(2, 2 + m):
        row = list(map(int, lines[i].split(',')))
        grid.append(row)

    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.orangesRotting(grid)

    print(result)


if __name__ == "__main__":
    solve()


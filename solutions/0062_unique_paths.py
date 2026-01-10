"""
Problem: Unique Paths
Link: https://leetcode.com/problems/unique-paths/

There is a robot on an m x n grid. The robot is initially located at the
top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right
corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right
at any point in time.

Given the two integers m and n, return the number of possible unique paths that
the robot can take to reach the bottom-right corner.

Example 1:
    Input: m = 3, n = 7
    Output: 28

Example 2:
    Input: m = 3, n = 2
    Output: 3

Constraints:
- 1 <= m, n <= 100

Topics: Math, Dynamic Programming, Combinatorics
"""
import json
from math import comb
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDP1D",
        "method": "uniquePaths",
        "complexity": "O(m*n) time, O(n) space",
        "description": "Space-optimized DP with single row",
    },
    "dp_2d": {
        "class": "SolutionDP2D",
        "method": "uniquePaths",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "Standard 2D DP approach",
    },
    "dp_1d": {
        "class": "SolutionDP1D",
        "method": "uniquePaths",
        "complexity": "O(m*n) time, O(n) space",
        "description": "Space-optimized DP",
    },
    "math": {
        "class": "SolutionMath",
        "method": "uniquePaths",
        "complexity": "O(min(m,n)) time, O(1) space",
        "description": "Combinatorics: C(m+n-2, m-1)",
    },
}


# ============================================================================
# Solution 1: Dynamic Programming 2D
# Time: O(m*n), Space: O(m*n)
#   - dp[i][j] = number of ways to reach cell (i, j)
#   - Each cell reachable from top or left
#   - Base case: first row and column all 1 (only one way)
# ============================================================================
class SolutionDP2D:
    """
    Standard 2D dynamic programming approach.

    State: dp[i][j] = number of unique paths to reach cell (i, j)
    Transition: dp[i][j] = dp[i-1][j] + dp[i][j-1]
                (paths from above + paths from left)
    Base case: dp[0][j] = dp[i][0] = 1 (only one way along edges)

    This builds up the solution from top-left to bottom-right.
    """

    def uniquePaths(self, m: int, n: int) -> int:
        # Initialize grid with 1s (base case for edges)
        dp = [[1] * n for _ in range(m)]

        # Fill from (1,1) to (m-1, n-1)
        for row in range(1, m):
            for col in range(1, n):
                dp[row][col] = dp[row - 1][col] + dp[row][col - 1]

        return dp[m - 1][n - 1]


# ============================================================================
# Solution 2: Dynamic Programming 1D (Space Optimized)
# Time: O(m*n), Space: O(n)
#   - Only need previous row to compute current row
#   - Reuse single array: dp[j] = dp[j] (from above) + dp[j-1] (from left)
# ============================================================================
class SolutionDP1D:
    """
    Space-optimized DP using single row.

    Key observation: Each cell only depends on cell above and cell to left.
    When processing row by row from left to right:
    - dp[j] still holds value from row above (not yet updated)
    - dp[j-1] already holds value from current row (just updated)

    So: dp[j] = dp[j] + dp[j-1] gives us paths from above + left.
    """

    def uniquePaths(self, m: int, n: int) -> int:
        # Single row initialized to 1 (first row has all 1s)
        dp = [1] * n

        # Process remaining rows
        for row in range(1, m):
            for col in range(1, n):
                # dp[col] = paths from above (old dp[col]) + left (dp[col-1])
                dp[col] += dp[col - 1]

        return dp[n - 1]


# ============================================================================
# Solution 3: Combinatorics
# Time: O(min(m,n)), Space: O(1)
#   - Total moves: (m-1) down + (n-1) right = m+n-2 moves
#   - Choose which (m-1) moves are down: C(m+n-2, m-1)
#   - Equivalently: C(m+n-2, n-1)
# ============================================================================
class SolutionMath:
    """
    Mathematical solution using combinatorics.

    Insight: Any path from (0,0) to (m-1, n-1) requires exactly:
    - (m-1) down moves
    - (n-1) right moves
    - Total: (m+n-2) moves

    The number of unique paths is the number of ways to arrange these moves.
    This is simply "choose which positions are down moves" = C(m+n-2, m-1).

    Using Python's math.comb for efficient computation.
    """

    def uniquePaths(self, m: int, n: int) -> int:
        # C(m+n-2, m-1) = C(m+n-2, n-1)
        # Use smaller value for fewer iterations
        return comb(m + n - 2, min(m - 1, n - 1))


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: m (rows)
        Line 2: n (columns)

    Example:
        3
        7
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    m = json.loads(lines[0])
    n = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.uniquePaths(m, n)

    print(result)


if __name__ == "__main__":
    solve()

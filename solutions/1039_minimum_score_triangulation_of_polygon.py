"""
1039. Minimum Score Triangulation of Polygon
https://leetcode.com/problems/minimum-score-triangulation-of-polygon/

Pattern: Interval DP - Polygon Triangulation
API Kernel: IntervalDP

Key insight: For edge (i, j), choose a third vertex k to form triangle.
This splits polygon into two smaller polygons with edges (i, k) and (k, j).
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minScoreTriangulation",
        "complexity": "O(n³) time, O(n²) space",
        "description": "Interval DP choosing third vertex for each edge",
    },
}


class Solution:
    def minScoreTriangulation(self, values: List[int]) -> int:
        """
        Minimum score to triangulate a convex polygon.

        dp[i][j] = min score to triangulate polygon with edge (i, j)

        For each vertex k between i and j:
        - Form triangle (i, k, j) with cost values[i] * values[k] * values[j]
        - Plus dp[i][k] and dp[k][j] for remaining polygons
        """
        n = len(values)

        # dp[i][j] = min score for polygon with vertices [i, j]
        dp = [[0] * n for _ in range(n)]

        # Fill by interval length (start from 3 for triangles)
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = float('inf')

                # Try each vertex k as the third vertex of triangle
                for k in range(i + 1, j):
                    cost = values[i] * values[k] * values[j]
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cost)

        return dp[0][n - 1]


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    values = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minScoreTriangulation(values)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

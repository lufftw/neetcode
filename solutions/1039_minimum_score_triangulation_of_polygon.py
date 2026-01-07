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


# ============================================================================
# Solution 1: Interval DP (Polygon Triangulation)
# Time: O(n³), Space: O(n²)
#   - For edge (i, j), choose third vertex k to form triangle
#   - Splits polygon into two smaller polygons: [i,k] and [k,j]
#   - min_score[i][j] = min over k of: left + right + values[i]*values[k]*values[j]
# ============================================================================
class Solution:
    def minScoreTriangulation(self, values: List[int]) -> int:
        vertex_count = len(values)

        # min_score[i][j] = min cost to triangulate polygon [i, j]
        min_score: list[list[int]] = [
            [0] * vertex_count for _ in range(vertex_count)
        ]

        # Fill by interval length (need at least 3 vertices for a triangle)
        for interval_len in range(3, vertex_count + 1):
            for start in range(vertex_count - interval_len + 1):
                end = start + interval_len - 1
                min_score[start][end] = float('inf')

                # Try each vertex as third point of triangle with edge (start, end)
                for third_vertex in range(start + 1, end):
                    triangle_cost = values[start] * values[third_vertex] * values[end]
                    total = min_score[start][third_vertex] + min_score[third_vertex][end] + triangle_cost
                    min_score[start][end] = min(min_score[start][end], total)

        return min_score[0][vertex_count - 1]


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

"""
1547. Minimum Cost to Cut a Stick
https://leetcode.com/problems/minimum-cost-to-cut-a-stick/

Pattern: Interval DP - Cutting Problems
API Kernel: IntervalDP

Key insight: Think about which cut to make LAST in each segment.
If k is cut last, cost = length of segment + cost of left + cost of right.
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minCost",
        "complexity": "O(m³) time, O(m²) space where m = len(cuts) + 2",
        "description": "Interval DP with 'last cut' approach",
    },
}


class Solution:
    def minCost(self, n: int, cuts: List[int]) -> int:
        """
        Minimum cost to make all cuts on a stick of length n.

        dp[i][j] = min cost to cut segment between cuts[i] and cuts[j]

        For each cut position k in (i, j):
        - If k is the LAST cut, cost = segment length = cuts[j] - cuts[i]
        - Total = dp[i][k] + dp[k][j] + cost
        """
        # Add boundaries and sort
        cuts = sorted([0] + cuts + [n])
        m = len(cuts)

        # dp[i][j] = min cost to cut segment [cuts[i], cuts[j]]
        dp = [[0] * m for _ in range(m)]

        # Fill by gap between cut indices
        for gap in range(2, m):
            for i in range(m - gap):
                j = i + gap
                dp[i][j] = float('inf')

                # Try each intermediate cut as the LAST cut
                for k in range(i + 1, j):
                    cost = cuts[j] - cuts[i]  # Length of current segment
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cost)

        return dp[0][m - 1]


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    n = json.loads(lines[0])
    cuts = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.minCost(n, cuts)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

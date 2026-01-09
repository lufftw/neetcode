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
    "memoization": {
        "class": "SolutionMemoization",
        "method": "minCost",
        "complexity": "O(m³) time, O(m²) space",
        "description": "Top-down recursive with memoization",
    },
}


# ============================================================================
# Solution 1: Interval DP (Cutting Problems)
# Time: O(m³), Space: O(m²) where m = len(cuts) + 2
#   - Think which cut to make LAST (not first)
#   - Add boundaries (0, n) and sort cuts
#   - Fill DP table by increasing gap between cut indices
# ============================================================================
class Solution:
    def minCost(self, n: int, cuts: List[int]) -> int:
        """
        Find minimum cost to make all cuts.

        Core insight: Think about which cut to make LAST in each segment.
        If k is cut last, cost = length of segment + cost of left subproblem
        + cost of right subproblem.

        Invariant: min_cost[i][j] contains minimum cost to make all cuts
        in the segment [cuts[i], cuts[j]].

        Args:
            n: Length of the stick
            cuts: Positions where cuts must be made

        Returns:
            Minimum total cost to make all cuts
        """
        # Add boundaries (0 and n) and sort
        cuts = sorted([0] + cuts + [n])
        cut_count = len(cuts)

        min_cost: list[list[int]] = [
            [0] * cut_count for _ in range(cut_count)
        ]

        # Fill by gap between cut indices
        for gap in range(2, cut_count):
            for start in range(cut_count - gap):
                end = start + gap
                min_cost[start][end] = float('inf')

                # Try each intermediate position as the LAST cut
                for last_cut in range(start + 1, end):
                    segment_length = cuts[end] - cuts[start]
                    total = min_cost[start][last_cut] + min_cost[last_cut][end] + segment_length
                    min_cost[start][end] = min(min_cost[start][end], total)

        return min_cost[0][cut_count - 1]


# ============================================================================
# Solution 2: Top-Down Memoization
# Time: O(m³), Space: O(m²)
#   - Recursive approach with memoization
#   - Directly models subproblem: min cost for segment [cuts[i], cuts[j]]
#   - Same complexity as bottom-up
# ============================================================================
class SolutionMemoization:
    def minCost(self, n: int, cuts: List[int]) -> int:
        """
        Find minimum cost using top-down memoization.

        Core insight: Recursively solve "min cost to make all cuts between
        cuts[left] and cuts[right]?" by trying each intermediate cut as
        the last one and taking minimum.

        Invariant: memo[(left, right)] stores optimal solution for the segment
        [cuts[left], cuts[right]] once computed.

        Args:
            n: Length of the stick
            cuts: Positions where cuts must be made

        Returns:
            Minimum total cost to make all cuts
        """
        # Add boundaries and sort
        cuts = sorted([0] + cuts + [n])
        m = len(cuts)
        memo = {}

        def dp(left: int, right: int) -> int:
            # Base case: no cuts needed between adjacent positions
            if right - left <= 1:
                return 0

            if (left, right) in memo:
                return memo[(left, right)]

            # Try each intermediate position as the LAST cut
            result = float('inf')
            segment_length = cuts[right] - cuts[left]

            for k in range(left + 1, right):
                cost = dp(left, k) + dp(k, right) + segment_length
                result = min(result, cost)

            memo[(left, right)] = result
            return result

        return dp(0, m - 1)


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

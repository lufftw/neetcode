"""
Problem: Sum of Matrix After Queries
Link: https://leetcode.com/problems/sum-of-matrix-after-queries/

You are given an integer n and a 0-indexed 2D array queries where
queries[i] = [typei, indexi, vali].

Initially, there is a 0-indexed n x n matrix filled with 0's. For each query:
- If typei == 0, set all values in row indexi to vali (overwrites previous)
- If typei == 1, set all values in column indexi to vali (overwrites previous)

Return the sum of integers in the matrix after all queries are applied.

Example 1:
    Input: n = 3, queries = [[0,0,1],[1,2,2],[0,2,3],[1,0,4]]
    Output: 23

Example 2:
    Input: n = 3, queries = [[0,0,4],[0,1,2],[1,0,1],[0,2,3],[1,2,1]]
    Output: 17

Constraints:
- 1 <= n <= 10^4
- 1 <= queries.length <= 5 * 10^4
- queries[i].length == 3
- 0 <= typei <= 1
- 0 <= indexi < n
- 0 <= vali <= 10^5

Topics: Array, Hash Table
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "matrixSumQueries",
        "complexity": "O(q) time, O(n) space",
        "description": "Reverse traversal with row/col tracking",
    },
}


# ============================================================================
# Solution: Reverse Traversal with Row/Col Tracking
# Time: O(q), Space: O(n) where q = len(queries)
#
# Key insight: Process queries in REVERSE order. The final value of any cell
# is determined by the LAST query that affects it (either its row or column).
#
# When processing in reverse:
# - If we see a row update for row i (and haven't seen it before), this row
#   will have value v in all cells NOT yet assigned by later column operations.
#   So contribute: v * (n - number_of_columns_already_processed)
# - Similarly for column updates.
#
# This elegantly handles overwriting: later operations (in original order)
# take precedence, which becomes "earlier operations" in reverse order.
# ============================================================================
class Solution:
    def matrixSumQueries(self, n: int, queries: List[List[int]]) -> int:
        """
        Calculate sum of matrix after all queries.

        Process queries in reverse order. For each row/column query:
        - Only count it if not already processed (later queries overwrite earlier)
        - Contribution = value * (n - cells_already_overwritten_by_perpendicular_ops)

        Args:
            n: Matrix dimension (n x n)
            queries: List of [type, index, value] where type 0=row, 1=column

        Returns:
            Sum of all matrix values after all queries
        """
        seen_rows = set()
        seen_cols = set()
        result = 0

        # Process queries in reverse order
        for query_type, index, val in reversed(queries):
            if query_type == 0:
                # Row operation
                if index not in seen_rows:
                    # This row hasn't been overwritten by a later row operation
                    # Count cells not already filled by later column operations
                    result += val * (n - len(seen_cols))
                    seen_rows.add(index)
            else:
                # Column operation
                if index not in seen_cols:
                    # This column hasn't been overwritten by a later column operation
                    # Count cells not already filled by later row operations
                    result += val * (n - len(seen_rows))
                    seen_cols.add(index)

        return result


def solve():
    """
    Input format:
    Line 1: n (integer)
    Line 2: queries (JSON 2D array)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    n = json.loads(lines[0])
    queries = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.matrixSumQueries(n, queries)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

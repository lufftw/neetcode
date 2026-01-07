"""
664. Strange Printer
https://leetcode.com/problems/strange-printer/

Pattern: Interval DP - Character Printing
API Kernel: IntervalDP

Key insight: When s[k] == s[i], we can extend the first print to cover s[k],
reducing the number of turns needed.
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "strangePrinter",
        "complexity": "O(n³) time, O(n²) space",
        "description": "Interval DP with character matching optimization",
    },
}


class Solution:
    def strangePrinter(self, s: str) -> int:
        """
        Minimum turns to print the string.

        dp[i][j] = min turns to print s[i:j+1]

        Base: print s[i] to cover entire interval, then handle rest.
        Optimization: if s[k] == s[i] for some k > i, extend first print.
        """
        # Remove consecutive duplicates (they don't affect answer)
        s = ''.join(c for i, c in enumerate(s) if i == 0 or c != s[i - 1])
        n = len(s)

        if n == 0:
            return 0

        # dp[i][j] = min turns to print s[i:j+1]
        dp = [[0] * n for _ in range(n)]

        # Base case: single character needs 1 turn
        for i in range(n):
            dp[i][i] = 1

        # Fill by increasing length
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1

                # Worst case: print s[i] alone, then handle rest
                dp[i][j] = dp[i + 1][j] + 1

                # Optimization: extend s[i]'s print if s[k] == s[i]
                for k in range(i + 1, j + 1):
                    if s[k] == s[i]:
                        left = dp[i + 1][k - 1] if k > i + 1 else 0
                        right = dp[k][j]
                        dp[i][j] = min(dp[i][j], left + right)

        return dp[0][n - 1]


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    s = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.strangePrinter(s)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

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
    "memoization": {
        "class": "SolutionMemoization",
        "method": "strangePrinter",
        "complexity": "O(n³) time, O(n²) space",
        "description": "Top-down recursive with memoization",
    },
}


# ============================================================================
# Solution 1: Interval DP (Character Printing)
# Time: O(n³), Space: O(n²)
#   - When s[k] == s[i], extend first print to cover s[k] (saves one turn)
#   - Preprocess: remove consecutive duplicates (don't affect answer)
#   - Fill DP table by increasing interval length
# ============================================================================
class Solution:
    def strangePrinter(self, s: str) -> int:
        """
        Find minimum turns to print the string.

        Core insight: When s[k] == s[i], extend the first print to cover s[k],
        reducing turns needed. The first character's print can extend to any
        matching character, effectively merging their costs.

        Invariant: min_turns[i][j] is optimal solution for substring s[i..j]
        after all positions in [i, j] have been assigned characters.

        Args:
            s: Target string to print

        Returns:
            Minimum number of printing turns needed
        """
        # Remove consecutive duplicates (they don't affect answer)
        s = ''.join(c for idx, c in enumerate(s) if idx == 0 or c != s[idx - 1])
        string_length = len(s)

        if string_length == 0:
            return 0

        min_turns: list[list[int]] = [
            [0] * string_length for _ in range(string_length)
        ]

        # Base case
        for idx in range(string_length):
            min_turns[idx][idx] = 1

        # Fill by increasing interval length
        for interval_len in range(2, string_length + 1):
            for start in range(string_length - interval_len + 1):
                end = start + interval_len - 1

                # Worst case: print s[start] alone, then handle rest
                min_turns[start][end] = min_turns[start + 1][end] + 1

                # Optimization: if s[match_pos] == s[start], extend first print
                for match_pos in range(start + 1, end + 1):
                    if s[match_pos] == s[start]:
                        left_cost = min_turns[start + 1][match_pos - 1] if match_pos > start + 1 else 0
                        right_cost = min_turns[match_pos][end]
                        min_turns[start][end] = min(min_turns[start][end], left_cost + right_cost)

        return min_turns[0][string_length - 1]


# ============================================================================
# Solution 2: Top-Down Memoization
# Time: O(n³), Space: O(n²)
#   - Recursive approach with memoization
#   - Directly models subproblem: min turns for s[i..j]
#   - Same complexity as bottom-up
# ============================================================================
class SolutionMemoization:
    def strangePrinter(self, s: str) -> int:
        """
        Find minimum turns using top-down memoization.

        Core insight: Recursively solve "min turns to print s[i..j]?" by
        trying to extend the first character's print to matching positions.

        Invariant: memo[(start, end)] stores optimal solution for substring
        s[start..end] once computed.

        Args:
            s: Target string to print

        Returns:
            Minimum number of printing turns needed
        """
        # Remove consecutive duplicates
        s = ''.join(c for i, c in enumerate(s) if i == 0 or c != s[i - 1])
        n = len(s)

        if n == 0:
            return 0

        memo = {}

        def dp(start: int, end: int) -> int:
            if start > end:
                return 0
            if start == end:
                return 1

            if (start, end) in memo:
                return memo[(start, end)]

            # Worst case: print s[start] alone, then handle rest
            result = dp(start + 1, end) + 1

            # Optimization: if s[k] == s[start], extend first print
            for k in range(start + 1, end + 1):
                if s[k] == s[start]:
                    result = min(result, dp(start + 1, k - 1) + dp(k, end))

            memo[(start, end)] = result
            return result

        return dp(0, n - 1)


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

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


# ============================================================================
# Solution 1: Interval DP (Character Printing)
# Time: O(n³), Space: O(n²)
#   - State: min_turns[i][j] = min turns to print s[i:j+1]
#   - Base case: min_turns[i][i] = 1 (single char needs 1 turn)
#   - Transition: if s[k] == s[i], extend first print to cover s[k]
#   - Preprocess: remove consecutive duplicates (don't affect answer)
# ============================================================================
class Solution:
    def strangePrinter(self, s: str) -> int:
        # Remove consecutive duplicates (they don't affect answer)
        s = ''.join(c for idx, c in enumerate(s) if idx == 0 or c != s[idx - 1])
        string_length = len(s)

        if string_length == 0:
            return 0

        # min_turns[i][j] = minimum turns to print s[i:j+1]
        min_turns: list[list[int]] = [
            [0] * string_length for _ in range(string_length)
        ]

        # Base case: single character needs 1 turn
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

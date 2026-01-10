"""
Problem: Distinct Subsequences
Link: https://leetcode.com/problems/distinct-subsequences/

Given two strings s and t, return the number of distinct subsequences of s which
equals t.

The test cases are generated so that the answer fits on a 32-bit signed integer.

Example 1:
    Input: s = "rabbbit", t = "rabbit"
    Output: 3
    Explanation: There are 3 ways to select "rabbit" from "rabbbit":
        - ra_bbit (skip 3rd b)
        - rab_bit (skip 4th b)
        - rabb_it (skip 5th b)

Example 2:
    Input: s = "babgbag", t = "bag"
    Output: 5
    Explanation: There are 5 ways to select "bag" from "babgbag":
        ba__bag, ba___ag, b__gbag, b___bag, ____bag

Constraints:
- 1 <= s.length, t.length <= 1000
- s and t consist of English letters.

Topics: String, Dynamic Programming
"""

import json
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDP2D",
        "method": "numDistinct",
        "complexity": "O(mn) time, O(mn) space",
        "description": "2D DP: dp[i][j] = ways to form t[0:j] from s[0:i]",
    },
    "dp_1d": {
        "class": "SolutionDP1D",
        "method": "numDistinct",
        "complexity": "O(mn) time, O(n) space",
        "description": "Space-optimized 1D DP, process right-to-left",
    },
}


# ============================================================================
# Solution 1: 2D Dynamic Programming
# Time: O(mn), Space: O(mn) where m = len(s), n = len(t)
#
# Key Insight:
#   Define dp[i][j] = number of distinct subsequences of s[0:i] that equal t[0:j].
#
#   Recurrence:
#   - If s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
#     * dp[i-1][j-1]: use s[i-1] to match t[j-1], count ways to match rest
#     * dp[i-1][j]: skip s[i-1], find t[0:j] in s[0:i-1]
#   - If s[i-1] != t[j-1]: dp[i][j] = dp[i-1][j]
#     * Must skip s[i-1] since it doesn't match
#
#   Base cases:
#   - dp[i][0] = 1: empty t can be formed from any prefix (by selecting nothing)
#   - dp[0][j] = 0 for j > 0: non-empty t can't be formed from empty s
#
# Why This Works:
#   At each position in s, we have a choice: include it in the subsequence
#   (if it matches the current target character) or skip it. The DP counts
#   all valid combinations of these choices.
# ============================================================================
class SolutionDP2D:
    """
    2D DP counting distinct subsequences.

    The key insight is the choice at each character: when s[i] matches t[j],
    we can either use it (advancing both pointers) or skip it (only advancing
    in s). This branching creates the counting structure.
    """

    def numDistinct(self, s: str, t: str) -> int:
        m, n = len(s), len(t)

        # dp[i][j] = ways to form t[0:j] from s[0:i]
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base case: empty t can be formed from any prefix of s
        for i in range(m + 1):
            dp[i][0] = 1

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Always have option to skip s[i-1]
                dp[i][j] = dp[i - 1][j]

                # If characters match, can also use s[i-1] to match t[j-1]
                if s[i - 1] == t[j - 1]:
                    dp[i][j] += dp[i - 1][j - 1]

        return dp[m][n]


# ============================================================================
# Solution 2: Space-Optimized 1D DP
# Time: O(mn), Space: O(n)
#
# Key Insight:
#   The 2D recurrence only depends on the previous row (i-1). We can optimize
#   to 1D by processing each row right-to-left. This ensures when we update
#   dp[j], we haven't yet modified the values we need (dp[j-1] and dp[j]).
#
# Why Right-to-Left:
#   dp[i][j] depends on dp[i-1][j] and dp[i-1][j-1]. If we process left-to-right,
#   updating dp[j-1] would corrupt the value needed for dp[j]. Right-to-left
#   avoids this dependency issue.
# ============================================================================
class SolutionDP1D:
    """
    Space-optimized 1D DP with right-to-left processing.

    By processing columns right-to-left, we ensure each dp[j] is updated
    using values from the previous row before they're overwritten.
    This reduces space from O(mn) to O(n).
    """

    def numDistinct(self, s: str, t: str) -> int:
        m, n = len(s), len(t)

        # dp[j] = ways to form t[0:j] from current prefix of s
        dp = [0] * (n + 1)
        dp[0] = 1  # Empty t can always be formed

        for i in range(1, m + 1):
            # Process right-to-left to use previous row's values
            for j in range(min(i, n), 0, -1):
                if s[i - 1] == t[j - 1]:
                    dp[j] += dp[j - 1]
                # If not matching, dp[j] stays the same (skip s[i-1])

        return dp[n]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: string s (JSON or raw)
        Line 2: string t (JSON or raw)

    Example:
        "rabbbit"
        "rabbit"
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    # Handle both JSON quoted and raw strings
    s = json.loads(lines[0]) if lines[0].startswith('"') else lines[0]
    t = json.loads(lines[1]) if lines[1].startswith('"') else lines[1]

    solver = get_solver(SOLUTIONS)
    result = solver.numDistinct(s, t)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

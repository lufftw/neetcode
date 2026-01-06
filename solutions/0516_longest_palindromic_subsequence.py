"""
Problem: Longest Palindromic Subsequence
Link: https://leetcode.com/problems/longest-palindromic-subsequence/

Given a string s, find the longest palindromic subsequence's length in s.

A subsequence is a sequence that can be derived from another sequence by
deleting some or no elements without changing the order of the remaining
elements.

Example 1:
    Input: s = "bbbab"
    Output: 4
    Explanation: One possible longest palindromic subsequence is "bbbb".

Example 2:
    Input: s = "cbbd"
    Output: 2
    Explanation: One possible longest palindromic subsequence is "bb".

Constraints:
- 1 <= s.length <= 1000
- s consists only of lowercase English letters.

Topics: String, Dynamic Programming
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "longestPalindromeSubseq",
        "complexity": "O(n^2) time, O(n^2) space",
        "description": "LCS of s and reverse(s)",
    },
    "interval_dp": {
        "class": "SolutionIntervalDP",
        "method": "longestPalindromeSubseq",
        "complexity": "O(n^2) time, O(n^2) space",
        "description": "Interval DP with dp[i][j] = LPS of s[i:j+1]",
    },
}


# ============================================================================
# Solution: LCS with Reversed String
# Time: O(n^2), Space: O(n^2)
#   - Key insight: LPS(s) = LCS(s, reverse(s))
#   - Any common subsequence between s and reverse(s) is a palindrome
# ============================================================================
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        t = s[::-1]  # Reversed string

        # LCS of s and t
        dp = [[0] * (n + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if s[i - 1] == t[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[n][n]


# ============================================================================
# Solution: Interval DP
# Time: O(n^2), Space: O(n^2)
#   - dp[i][j] = length of LPS in s[i:j+1]
#   - Base case: dp[i][i] = 1 (single character)
#   - Fill by increasing interval length
# ============================================================================
class SolutionIntervalDP:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        dp = [[0] * n for _ in range(n)]

        # Base case: single characters
        for i in range(n):
            dp[i][i] = 1

        # Fill by increasing interval length
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

        return dp[0][n - 1] if n > 0 else 0


def solve():
    """
    Input format:
    Line 1: s (string)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    s = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.longestPalindromeSubseq(s)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

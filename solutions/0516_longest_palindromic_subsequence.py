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
# Solution 1: LCS with Reversed String
# Time: O(n^2), Space: O(n^2)
#   - Key insight: LPS(s) = LCS(s, reverse(s))
#   - Reduces to classic LCS problem
# ============================================================================
class Solution:
    # State: lcs_length[i][j] = LCS length for s[0:i] and reversed_s[0:j]
    # Base case: lcs_length[i][0] = lcs_length[0][j] = 0
    # Transition: if match, lcs_length[i][j] = lcs_length[i-1][j-1] + 1
    #             else, lcs_length[i][j] = max(lcs_length[i-1][j], lcs_length[i][j-1])

    def longestPalindromeSubseq(self, s: str) -> int:
        string_len = len(s)
        reversed_s = s[::-1]

        lcs_length: list[list[int]] = [
            [0] * (string_len + 1) for _ in range(string_len + 1)
        ]

        for i in range(1, string_len + 1):
            for j in range(1, string_len + 1):
                if s[i - 1] == reversed_s[j - 1]:
                    lcs_length[i][j] = lcs_length[i - 1][j - 1] + 1
                else:
                    lcs_length[i][j] = max(lcs_length[i - 1][j], lcs_length[i][j - 1])

        return lcs_length[string_len][string_len]


# ============================================================================
# Solution 2: Interval DP
# Time: O(n^2), Space: O(n^2)
#   - lps_length[i][j] = LPS length in substring s[i:j+1]
#   - Fill by increasing interval length; endpoints match → extend inner + 2
# ============================================================================
class SolutionIntervalDP:
    def longestPalindromeSubseq(self, s: str) -> int:
        string_len = len(s)

        # lps_length[i][j] = LPS length for s[i:j+1]
        lps_length: list[list[int]] = [[0] * string_len for _ in range(string_len)]

        # Base case: single character is palindrome of length 1
        for i in range(string_len):
            lps_length[i][i] = 1

        # Fill by increasing interval length
        for interval_len in range(2, string_len + 1):
            for start in range(string_len - interval_len + 1):
                end = start + interval_len - 1
                if s[start] == s[end]:
                    # Endpoints match: extend inner palindrome by 2
                    lps_length[start][end] = lps_length[start + 1][end - 1] + 2
                else:
                    # Mismatch: take best of excluding either endpoint
                    lps_length[start][end] = max(
                        lps_length[start + 1][end], lps_length[start][end - 1]
                    )

        return lps_length[0][string_len - 1] if string_len > 0 else 0


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

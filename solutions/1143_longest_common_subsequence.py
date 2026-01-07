"""
Problem: Longest Common Subsequence
Link: https://leetcode.com/problems/longest-common-subsequence/

Given two strings text1 and text2, return the length of their longest common
subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string
with some characters (can be none) deleted without changing the relative order
of the remaining characters.

Example 1:
    Input: text1 = "abcde", text2 = "ace"
    Output: 3
    Explanation: The longest common subsequence is "ace" and its length is 3.

Example 2:
    Input: text1 = "abc", text2 = "abc"
    Output: 3
    Explanation: The longest common subsequence is "abc" and its length is 3.

Example 3:
    Input: text1 = "abc", text2 = "def"
    Output: 0
    Explanation: There is no such common subsequence.

Constraints:
- 1 <= text1.length, text2.length <= 1000
- text1 and text2 consist of only lowercase English characters.

Topics: String, Dynamic Programming
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "longestCommonSubsequence",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "2D DP with dp[i][j] = LCS length for text1[0:i] and text2[0:j]",
    },
    "space_optimized": {
        "class": "SolutionSpaceOptimized",
        "method": "longestCommonSubsequence",
        "complexity": "O(m*n) time, O(min(m,n)) space",
        "description": "Space-optimized using only two rows",
    },
}


# ============================================================================
# Solution 1: 2D DP
# Time: O(m*n), Space: O(m*n)
#   - lcs_length[i][j] = LCS length for text1[0:i] and text2[0:j]
#   - Match: extend from diagonal; Mismatch: max of skip either string
# ============================================================================
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        len_1, len_2 = len(text1), len(text2)

        # lcs_length[i][j] = LCS length for text1[0:i] and text2[0:j]
        lcs_length: list[list[int]] = [
            [0] * (len_2 + 1) for _ in range(len_1 + 1)
        ]

        for i in range(1, len_1 + 1):
            for j in range(1, len_2 + 1):
                if text1[i - 1] == text2[j - 1]:
                    # Characters match: extend LCS from diagonal
                    lcs_length[i][j] = lcs_length[i - 1][j - 1] + 1
                else:
                    # Mismatch: take best of skipping either character
                    lcs_length[i][j] = max(lcs_length[i - 1][j], lcs_length[i][j - 1])

        return lcs_length[len_1][len_2]


# ============================================================================
# Solution 2: Space-Optimized
# Time: O(m*n), Space: O(min(m,n))
#   - Only need previous row to compute current row
#   - Swap shorter string to column dimension for minimal space
# ============================================================================
class SolutionSpaceOptimized:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # Make text2 the shorter one for better space
        if len(text1) < len(text2):
            text1, text2 = text2, text1

        len_1, len_2 = len(text1), len(text2)
        previous_row: list[int] = [0] * (len_2 + 1)
        current_row: list[int] = [0] * (len_2 + 1)

        for i in range(1, len_1 + 1):
            for j in range(1, len_2 + 1):
                if text1[i - 1] == text2[j - 1]:
                    current_row[j] = previous_row[j - 1] + 1
                else:
                    current_row[j] = max(previous_row[j], current_row[j - 1])
            previous_row, current_row = current_row, previous_row

        return previous_row[len_2]


def solve():
    """
    Input format:
    Line 1: text1 (string)
    Line 2: text2 (string)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    text1 = json.loads(lines[0])
    text2 = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.longestCommonSubsequence(text1, text2)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

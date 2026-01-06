"""
Problem: Edit Distance
Link: https://leetcode.com/problems/edit-distance/

Given two strings word1 and word2, return the minimum number of operations
required to convert word1 to word2.

You have the following three operations permitted on a word:
- Insert a character
- Delete a character
- Replace a character

Example 1:
    Input: word1 = "horse", word2 = "ros"
    Output: 3
    Explanation:
    horse -> rorse (replace 'h' with 'r')
    rorse -> rose (remove 'r')
    rose -> ros (remove 'e')

Example 2:
    Input: word1 = "intention", word2 = "execution"
    Output: 5
    Explanation:
    intention -> inention (remove 't')
    inention -> enention (replace 'i' with 'e')
    enention -> exention (replace 'n' with 'x')
    exention -> exection (replace 'n' with 'c')
    exection -> execution (insert 'u')

Constraints:
- 0 <= word1.length, word2.length <= 500
- word1 and word2 consist of lowercase English letters.

Topics: String, Dynamic Programming
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minDistance",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "2D DP with dp[i][j] = min edits for word1[0:i] to word2[0:j]",
    },
    "space_optimized": {
        "class": "SolutionSpaceOptimized",
        "method": "minDistance",
        "complexity": "O(m*n) time, O(min(m,n)) space",
        "description": "Space-optimized using only two rows",
    },
}


# ============================================================================
# Solution: 2D DP
# Time: O(m*n), Space: O(m*n)
#   - dp[i][j] = minimum edits to convert word1[0:i] to word2[0:j]
#   - Base cases: dp[i][0] = i (delete all), dp[0][j] = j (insert all)
#   - If chars match: dp[i][j] = dp[i-1][j-1]
#   - If not: dp[i][j] = 1 + min(replace, delete, insert)
# ============================================================================
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base cases
        for i in range(m + 1):
            dp[i][0] = i  # Delete all characters from word1
        for j in range(n + 1):
            dp[0][j] = j  # Insert all characters of word2

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]  # No operation needed
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j - 1],  # Replace
                        dp[i - 1][j],  # Delete from word1
                        dp[i][j - 1],  # Insert to word1
                    )

        return dp[m][n]


# ============================================================================
# Solution: Space-Optimized
# Time: O(m*n), Space: O(min(m,n))
#   - Only need previous row plus one extra variable for diagonal
# ============================================================================
class SolutionSpaceOptimized:
    def minDistance(self, word1: str, word2: str) -> int:
        # Make word2 the shorter one for better space
        if len(word1) < len(word2):
            word1, word2 = word2, word1

        m, n = len(word1), len(word2)
        prev = list(range(n + 1))  # Base case: dp[0][j] = j
        curr = [0] * (n + 1)

        for i in range(1, m + 1):
            curr[0] = i  # Base case: dp[i][0] = i
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    curr[j] = prev[j - 1]
                else:
                    curr[j] = 1 + min(prev[j - 1], prev[j], curr[j - 1])
            prev, curr = curr, prev

        return prev[n]


def solve():
    """
    Input format:
    Line 1: word1 (string)
    Line 2: word2 (string)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    word1 = json.loads(lines[0])
    word2 = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.minDistance(word1, word2)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

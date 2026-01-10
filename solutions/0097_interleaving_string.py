"""
Problem: Interleaving String
Link: https://leetcode.com/problems/interleaving-string/

Given strings s1, s2, and s3, find whether s3 is formed by an interleaving
of s1 and s2.

An interleaving of two strings s and t is a configuration where s and t are
divided into n and m substrings respectively, such that:
- s = s_1 + s_2 + ... + s_n
- t = t_1 + t_2 + ... + t_m
- |n - m| <= 1
- The interleaving is s_1 + t_1 + s_2 + t_2 + ... or t_1 + s_1 + t_2 + s_2 + ...

Example 1:
    Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
    Output: true

Example 2:
    Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
    Output: false

Example 3:
    Input: s1 = "", s2 = "", s3 = ""
    Output: true

Constraints:
- 0 <= s1.length, s2.length <= 100
- 0 <= s3.length <= 200
- s1, s2, and s3 consist of lowercase English letters.

Follow-up: Could you solve it using only O(s2.length) additional memory space?

Topics: String, Dynamic Programming
"""
import json
from functools import lru_cache
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDP1D",
        "method": "isInterleave",
        "complexity": "O(m*n) time, O(n) space",
        "description": "Space-optimized 1D DP",
    },
    "dp_2d": {
        "class": "SolutionDP2D",
        "method": "isInterleave",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "2D DP table",
    },
    "dp_1d": {
        "class": "SolutionDP1D",
        "method": "isInterleave",
        "complexity": "O(m*n) time, O(n) space",
        "description": "Space-optimized 1D DP",
    },
    "memo": {
        "class": "SolutionMemo",
        "method": "isInterleave",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "Top-down with memoization",
    },
}


# ============================================================================
# Solution 1: 2D Dynamic Programming
# Time: O(m*n), Space: O(m*n) where m = len(s1), n = len(s2)
#   - dp[i][j] = can s1[0:i] and s2[0:j] interleave to form s3[0:i+j]?
#   - Transition: check if extending s1 or s2 matches next char in s3
# ============================================================================
class SolutionDP2D:
    """
    2D Dynamic Programming approach.

    State: dp[i][j] = True if s1[0:i] and s2[0:j] can interleave to form s3[0:i+j]

    Transition:
    - dp[i][j] = True if:
      - dp[i-1][j] is True and s1[i-1] == s3[i+j-1] (extend from s1)
      - OR dp[i][j-1] is True and s2[j-1] == s3[i+j-1] (extend from s2)

    Base case: dp[0][0] = True (empty strings interleave to empty)
    Answer: dp[m][n]
    """

    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)

        # Length check
        if m + n != len(s3):
            return False

        # dp[i][j] = can s1[0:i] and s2[0:j] form s3[0:i+j]?
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True

        # Initialize first column (using only s1)
        for i in range(1, m + 1):
            dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]

        # Initialize first row (using only s2)
        for j in range(1, n + 1):
            dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]

        # Fill the table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                k = i + j - 1  # Index in s3
                # Try extending from s1 or s2
                dp[i][j] = (
                    (dp[i - 1][j] and s1[i - 1] == s3[k]) or
                    (dp[i][j - 1] and s2[j - 1] == s3[k])
                )

        return dp[m][n]


# ============================================================================
# Solution 2: 1D Dynamic Programming (Space Optimized)
# Time: O(m*n), Space: O(n)
#   - Only need previous row to compute current row
#   - Satisfies follow-up requirement
# ============================================================================
class SolutionDP1D:
    """
    Space-optimized DP using 1D array.

    Since dp[i][j] only depends on dp[i-1][j] and dp[i][j-1],
    we can use a single row and update in place.

    - dp[j] represents dp[i][j] for current row i
    - Before update, dp[j] holds dp[i-1][j]
    - After update of dp[j-1], it holds dp[i][j-1]
    """

    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)

        if m + n != len(s3):
            return False

        # Use shorter string for dp array to minimize space
        if m < n:
            s1, s2 = s2, s1
            m, n = n, m

        dp = [False] * (n + 1)
        dp[0] = True

        # Initialize first row (using only s2)
        for j in range(1, n + 1):
            dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]

        # Fill row by row
        for i in range(1, m + 1):
            # First column: can only use s1
            dp[0] = dp[0] and s1[i - 1] == s3[i - 1]

            for j in range(1, n + 1):
                k = i + j - 1
                dp[j] = (
                    (dp[j] and s1[i - 1] == s3[k]) or
                    (dp[j - 1] and s2[j - 1] == s3[k])
                )

        return dp[n]


# ============================================================================
# Solution 3: Memoization (Top-Down)
# Time: O(m*n), Space: O(m*n)
#   - Recursive with caching
#   - More intuitive problem decomposition
# ============================================================================
class SolutionMemo:
    """
    Top-down DP with memoization.

    canForm(i, j) = can s1[i:] and s2[j:] interleave to form s3[i+j:]?

    At each state, we try:
    - If s1[i] matches s3[i+j], try using it
    - If s2[j] matches s3[i+j], try using it
    """

    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)

        if m + n != len(s3):
            return False

        @lru_cache(maxsize=None)
        def canForm(i: int, j: int) -> bool:
            k = i + j  # Position in s3

            # Base case: used all characters
            if i == m and j == n:
                return True

            result = False

            # Try taking from s1
            if i < m and s1[i] == s3[k]:
                result = result or canForm(i + 1, j)

            # Try taking from s2
            if j < n and s2[j] == s3[k]:
                result = result or canForm(i, j + 1)

            return result

        return canForm(0, 0)


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: s1 as JSON string
        Line 2: s2 as JSON string
        Line 3: s3 as JSON string

    Example:
        "aabcc"
        "dbbca"
        "aadbbcbcac"
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    s1 = json.loads(lines[0])
    s2 = json.loads(lines[1])
    s3 = json.loads(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.isInterleave(s1, s2, s3)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

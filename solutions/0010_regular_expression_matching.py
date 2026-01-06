"""
Problem: Regular Expression Matching
Link: https://leetcode.com/problems/regular-expression-matching/

Given an input string s and a pattern p, implement regular expression matching
with support for '.' and '*' where:
- '.' Matches any single character.
- '*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).

Example 1:
    Input: s = "aa", p = "a"
    Output: false
    Explanation: "a" does not match the entire string "aa".

Example 2:
    Input: s = "aa", p = "a*"
    Output: true
    Explanation: '*' means zero or more of the preceding element, 'a'.
    Therefore, by repeating 'a' once, it becomes "aa".

Example 3:
    Input: s = "ab", p = ".*"
    Output: true
    Explanation: ".*" means "zero or more (*) of any character (.)".

Constraints:
- 1 <= s.length <= 20
- 1 <= p.length <= 20
- s contains only lowercase English letters.
- p contains only lowercase English letters, '.', and '*'.
- It is guaranteed for each appearance of the character '*', there will be
  a previous valid character to match.

Topics: String, Dynamic Programming, Recursion
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "isMatch",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "2D DP with dp[i][j] = True if s[0:i] matches p[0:j]",
    },
    "recursive": {
        "class": "SolutionRecursive",
        "method": "isMatch",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "Top-down recursion with memoization",
    },
}


# ============================================================================
# Solution: 2D DP (Bottom-Up)
# Time: O(m*n), Space: O(m*n)
#   - dp[i][j] = True if s[0:i] matches p[0:j]
#   - Handle '*' specially: zero or more of preceding element
# ============================================================================
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)

        # dp[i][j] = True if s[0:i] matches p[0:j]
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True  # Empty string matches empty pattern

        # Base case: empty string can match patterns like a*, a*b*, etc.
        for j in range(2, n + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 2]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == '*':
                    # Option 1: Use zero occurrences of preceding element
                    dp[i][j] = dp[i][j - 2]

                    # Option 2: Use one or more (if current char matches)
                    if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                        dp[i][j] = dp[i][j] or dp[i - 1][j]
                elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                    # Direct match or wildcard .
                    dp[i][j] = dp[i - 1][j - 1]

        return dp[m][n]


# ============================================================================
# Solution: Top-Down with Memoization
# Time: O(m*n), Space: O(m*n)
#   - Recursive approach with caching
# ============================================================================
class SolutionRecursive:
    def isMatch(self, s: str, p: str) -> bool:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(i: int, j: int) -> bool:
            """Check if s[i:] matches p[j:]"""
            # Base case: pattern exhausted
            if j == len(p):
                return i == len(s)

            # Check if first character matches
            first_match = i < len(s) and (p[j] == '.' or p[j] == s[i])

            # Handle '*' - zero or more of preceding
            if j + 1 < len(p) and p[j + 1] == '*':
                # Option 1: Use zero of p[j] (skip p[j] and *)
                # Option 2: Use one+ of p[j] (if first matches, advance s)
                return dp(i, j + 2) or (first_match and dp(i + 1, j))
            else:
                # Normal match: advance both if first matches
                return first_match and dp(i + 1, j + 1)

        return dp(0, 0)


def solve():
    """
    Input format:
    Line 1: s (string)
    Line 2: p (pattern)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    s = json.loads(lines[0])
    p = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.isMatch(s, p)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

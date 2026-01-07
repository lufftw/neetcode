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
# Solution 1: 2D DP (Bottom-Up)
# Time: O(m*n), Space: O(m*n)
#   - is_match[i][j] = True if s[0:i] matches p[0:j]
#   - '*' means zero or more of PRECEDING char (look back to p[j-2])
# ============================================================================
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        text_len, pattern_len = len(s), len(p)

        # is_match[i][j] = True if s[0:i] matches p[0:j]
        is_match: list[list[bool]] = [
            [False] * (pattern_len + 1) for _ in range(text_len + 1)
        ]
        is_match[0][0] = True  # Empty string matches empty pattern

        # Base case: empty string can match patterns like a*, a*b*, etc.
        for j in range(2, pattern_len + 1):
            if p[j - 1] == '*':
                # '*' can eliminate preceding char, check j-2
                is_match[0][j] = is_match[0][j - 2]

        for i in range(1, text_len + 1):
            for j in range(1, pattern_len + 1):
                pattern_char = p[j - 1]

                if pattern_char == '*':
                    preceding_char = p[j - 2]
                    # Option 1: Use zero occurrences (skip preceding + '*')
                    zero_match = is_match[i][j - 2]
                    # Option 2: Use one+ (if current text char matches preceding)
                    char_matches = (preceding_char == '.' or preceding_char == s[i - 1])
                    one_or_more = char_matches and is_match[i - 1][j]
                    is_match[i][j] = zero_match or one_or_more

                elif pattern_char == '.' or pattern_char == s[i - 1]:
                    # Direct match or '.' wildcard
                    is_match[i][j] = is_match[i - 1][j - 1]

        return is_match[text_len][pattern_len]


# ============================================================================
# Solution 2: Top-Down with Memoization
# Time: O(m*n), Space: O(m*n)
#   - Recursive with lru_cache; check_match(i, j) = does s[i:] match p[j:]?
#   - More intuitive flow but same complexity as bottom-up
# ============================================================================
class SolutionRecursive:
    def isMatch(self, s: str, p: str) -> bool:
        from functools import lru_cache

        text_len, pattern_len = len(s), len(p)

        @lru_cache(maxsize=None)
        def check_match(text_idx: int, pattern_idx: int) -> bool:
            """Check if s[text_idx:] matches p[pattern_idx:]."""
            # Base case: pattern exhausted
            if pattern_idx == pattern_len:
                return text_idx == text_len

            # Check if first character matches
            first_char_matches = (
                text_idx < text_len and
                (p[pattern_idx] == '.' or p[pattern_idx] == s[text_idx])
            )

            # Handle '*' - zero or more of preceding char
            if pattern_idx + 1 < pattern_len and p[pattern_idx + 1] == '*':
                # Option 1: Use zero (skip pattern char + '*')
                # Option 2: Use one+ (if first matches, consume text char)
                zero_match = check_match(text_idx, pattern_idx + 2)
                one_or_more = first_char_matches and check_match(text_idx + 1, pattern_idx)
                return zero_match or one_or_more
            else:
                # Normal match: advance both if first matches
                return first_char_matches and check_match(text_idx + 1, pattern_idx + 1)

        return check_match(0, 0)


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

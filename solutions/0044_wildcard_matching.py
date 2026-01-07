"""
Problem: Wildcard Matching
Link: https://leetcode.com/problems/wildcard-matching/

Given an input string s and a pattern p, implement wildcard pattern matching
with support for '?' and '*' where:
- '?' Matches any single character.
- '*' Matches any sequence of characters (including the empty sequence).

The matching should cover the entire input string (not partial).

Example 1:
    Input: s = "aa", p = "a"
    Output: false
    Explanation: "a" does not match the entire string "aa".

Example 2:
    Input: s = "aa", p = "*"
    Output: true
    Explanation: '*' matches any sequence.

Example 3:
    Input: s = "cb", p = "?a"
    Output: false
    Explanation: '?' matches 'c', but the second letter is 'a',
    which does not match 'b'.

Constraints:
- 0 <= s.length, p.length <= 2000
- s contains only lowercase English letters.
- p contains only lowercase English letters, '?' or '*'.

Topics: String, Dynamic Programming, Greedy, Recursion
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "isMatch",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "2D DP with dp[i][j] = True if s[0:i] matches p[0:j]",
    },
    "space_optimized": {
        "class": "SolutionSpaceOptimized",
        "method": "isMatch",
        "complexity": "O(m*n) time, O(n) space",
        "description": "Space-optimized using two rows",
    },
    "greedy": {
        "class": "SolutionGreedy",
        "method": "isMatch",
        "complexity": "O(m*n) worst, O(m+n) average time, O(1) space",
        "description": "Greedy with backtracking on '*'",
    },
}


# ============================================================================
# Solution: 2D DP (Bottom-Up)
# Time: O(m*n), Space: O(m*n)
#   - dp[i][j] = True if s[0:i] matches p[0:j]
#   - '*' matches empty (left) or extends match (up)
#   - Simpler than regex since '*' is self-contained
# ============================================================================
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Implement wildcard pattern matching with '?' and '*'.

        The key difference from regex matching:
        - Wildcard '*' matches ANY sequence (including empty)
        - Regex '*' matches zero or more of the PRECEDING character

        Transitions:
        - If p[j-1] is letter: must match s[i-1]
        - If p[j-1] is '?': matches any single char
        - If p[j-1] is '*': matches empty (dp[i][j-1]) or extends (dp[i-1][j])
        """
        text_length = len(s)
        pattern_length = len(p)

        # dp[i][j] = True if s[0:i] matches p[0:j]
        is_match: list[list[bool]] = [
            [False] * (pattern_length + 1)
            for _ in range(text_length + 1)
        ]

        # Base case: empty string matches empty pattern
        is_match[0][0] = True

        # Base case: empty string can match pattern of only '*'s
        # Once we hit a non-'*', no more matches possible
        for j in range(1, pattern_length + 1):
            if p[j - 1] == '*':
                is_match[0][j] = is_match[0][j - 1]
            else:
                break

        # Fill DP table
        for i in range(1, text_length + 1):
            for j in range(1, pattern_length + 1):
                pattern_char = p[j - 1]
                text_char = s[i - 1]

                if pattern_char == '*':
                    # '*' can match:
                    # 1. Empty sequence: look left (dp[i][j-1])
                    # 2. One more character: look up (dp[i-1][j])
                    match_empty = is_match[i][j - 1]
                    match_one_more = is_match[i - 1][j]
                    is_match[i][j] = match_empty or match_one_more

                elif pattern_char == '?' or pattern_char == text_char:
                    # Direct match: carry result from diagonal
                    is_match[i][j] = is_match[i - 1][j - 1]

                # else: mismatch, stays False

        return is_match[text_length][pattern_length]


# ============================================================================
# Solution: Space-Optimized DP
# Time: O(m*n), Space: O(n)
#   - Use two rows instead of full table
#   - Current row depends on previous row and current row (left)
# ============================================================================
class SolutionSpaceOptimized:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Space-optimized wildcard matching using rolling rows.

        Key insight: dp[i][j] depends on:
        - dp[i][j-1] (left, for '*' empty match)
        - dp[i-1][j] (up, for '*' extend match)
        - dp[i-1][j-1] (diagonal, for direct match)

        We can use two rows: previous and current.
        """
        text_length = len(s)
        pattern_length = len(p)

        # Initialize previous row (representing empty string matching)
        previous_row: list[bool] = [False] * (pattern_length + 1)
        previous_row[0] = True

        # Empty string can match leading '*'s
        for j in range(1, pattern_length + 1):
            if p[j - 1] == '*':
                previous_row[j] = previous_row[j - 1]
            else:
                break

        # Process each character in s
        for i in range(1, text_length + 1):
            current_row: list[bool] = [False] * (pattern_length + 1)
            # current_row[0] = False (non-empty can't match empty pattern)

            for j in range(1, pattern_length + 1):
                pattern_char = p[j - 1]

                if pattern_char == '*':
                    # Empty match (left) or extend match (up)
                    current_row[j] = current_row[j - 1] or previous_row[j]

                elif pattern_char == '?' or pattern_char == s[i - 1]:
                    # Direct match from diagonal
                    current_row[j] = previous_row[j - 1]

            previous_row = current_row

        return previous_row[pattern_length]


# ============================================================================
# Solution: Greedy with Backtracking
# Time: O(m*n) worst case, O(m+n) average, Space: O(1)
#   - Match character by character
#   - On '*', remember position and try empty match first
#   - On mismatch, backtrack to last '*' and try matching one more char
# ============================================================================
class SolutionGreedy:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Greedy approach with backtracking on '*'.

        Strategy:
        1. Match character by character for exact and '?' matches
        2. On '*', record position and try matching empty first
        3. On mismatch, backtrack to last '*' and extend its match

        This works because '*' is greedy: if matching fails, we just
        try having '*' consume one more character from s.
        """
        text_idx = 0
        pattern_idx = 0
        text_length = len(s)
        pattern_length = len(p)

        # Track last '*' position and how many chars it matched
        last_star_pattern_idx = -1
        last_star_text_idx = 0

        while text_idx < text_length:
            # Case 1: Exact match or '?' wildcard
            if (pattern_idx < pattern_length and
                (p[pattern_idx] == s[text_idx] or p[pattern_idx] == '?')):
                text_idx += 1
                pattern_idx += 1

            # Case 2: '*' found - record and match empty initially
            elif pattern_idx < pattern_length and p[pattern_idx] == '*':
                last_star_pattern_idx = pattern_idx
                last_star_text_idx = text_idx
                pattern_idx += 1  # Move past '*', try matching empty

            # Case 3: Mismatch - backtrack to last '*' if exists
            elif last_star_pattern_idx != -1:
                # Reset pattern to right after last '*'
                pattern_idx = last_star_pattern_idx + 1
                # Have '*' match one more character
                last_star_text_idx += 1
                text_idx = last_star_text_idx

            # Case 4: No match possible
            else:
                return False

        # After consuming all of s, remaining pattern must be all '*'s
        while pattern_idx < pattern_length and p[pattern_idx] == '*':
            pattern_idx += 1

        return pattern_idx == pattern_length


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

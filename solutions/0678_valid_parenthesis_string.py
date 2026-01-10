"""
Problem: Valid Parenthesis String
Link: https://leetcode.com/problems/valid-parenthesis-string/

Given a string s containing only three types of characters: '(', ')' and '*',
return true if s is valid.

The following rules define a valid string:
- Any left parenthesis '(' must have a corresponding right parenthesis ')'.
- Any right parenthesis ')' must have a corresponding left parenthesis '('.
- Left parenthesis '(' must go before the corresponding right parenthesis ')'.
- '*' could be treated as a single right parenthesis ')' or a single left
  parenthesis '(' or an empty string "".

Example 1:
    Input: s = "()"
    Output: true

Example 2:
    Input: s = "(*)"
    Output: true

Example 3:
    Input: s = "(*))"
    Output: true

Constraints:
- 1 <= s.length <= 100
- s[i] is '(', ')' or '*'.

Topics: String, Dynamic Programming, Stack, Greedy
"""

import json
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionGreedy",
        "method": "checkValidString",
        "complexity": "O(n) time, O(1) space",
        "description": "Track min/max possible open count, greedy range narrowing",
    },
    "two_pass": {
        "class": "SolutionTwoPass",
        "method": "checkValidString",
        "complexity": "O(n) time, O(1) space",
        "description": "Two passes: left-to-right and right-to-left validation",
    },
}


# ============================================================================
# Solution 1: Greedy with Min/Max Open Count
# Time: O(n), Space: O(1)
#
# Key Insight:
#   Instead of tracking exact count of open parentheses (which is ambiguous
#   due to '*'), track a RANGE of possible open counts:
#   - min_open: minimum possible unclosed '(' (assume '*' is ')' or empty)
#   - max_open: maximum possible unclosed '(' (assume '*' is '(')
#
#   For each character:
#   - '(': both min and max increase by 1
#   - ')': both min and max decrease by 1
#   - '*': min decreases (could be ')'), max increases (could be '(')
#
#   Validity conditions:
#   - If max_open < 0: too many ')' even if all '*' are '(', invalid
#   - If min_open < 0: clamp to 0 (we can choose '*' to be empty or ')')
#   - At end: valid if min_open == 0 (we can balance all '(')
#
# Why This Works:
#   The range [min_open, max_open] represents all possible states of unclosed
#   '(' counts. If 0 is within this range at the end, some assignment of '*'
#   makes the string valid.
# ============================================================================
class SolutionGreedy:
    """
    Greedy approach tracking the range of possible open parenthesis counts.

    The key insight is that '*' creates uncertainty, but we can track the
    entire range of possible states simultaneously. Valid if 0 is achievable
    at the end.
    """

    def checkValidString(self, s: str) -> bool:
        min_open = 0  # Minimum possible unclosed '('
        max_open = 0  # Maximum possible unclosed '('

        for char in s:
            if char == "(":
                min_open += 1
                max_open += 1
            elif char == ")":
                min_open -= 1
                max_open -= 1
            else:  # '*'
                min_open -= 1  # Treat as ')' or empty
                max_open += 1  # Treat as '('

            # If max_open < 0, too many ')' even with all '*' as '('
            if max_open < 0:
                return False

            # min_open can't go negative; if it does, use '*' as empty or ')'
            min_open = max(min_open, 0)

        # Valid if we can have exactly 0 unclosed '('
        return min_open == 0


# ============================================================================
# Solution 2: Two-Pass Validation
# Time: O(n), Space: O(1)
#
# Key Insight:
#   A valid string must satisfy two conditions:
#   1. Left-to-right: every ')' has a matching '(' or '*' before it
#   2. Right-to-left: every '(' has a matching ')' or '*' after it
#
#   We check both conditions with separate passes. In each pass, '*' can
#   act as the opposite parenthesis to help balance.
#
# Algorithm:
#   - Pass 1 (L→R): Treat '*' as '(' when needed, count balance
#   - Pass 2 (R→L): Treat '*' as ')' when needed, count balance
#   - Valid if both passes succeed (balance never goes negative)
# ============================================================================
class SolutionTwoPass:
    """
    Two-pass approach: validate from both directions.

    First pass ensures every ')' is matched. Second pass ensures every '('
    is matched. If both pass, the string is valid.
    """

    def checkValidString(self, s: str) -> bool:
        # Pass 1: Left to right
        # Treat '*' as '(' to help balance ')' characters
        balance = 0
        for char in s:
            if char == "(" or char == "*":
                balance += 1
            else:  # ')'
                balance -= 1

            if balance < 0:
                return False  # Unmatched ')'

        # Pass 2: Right to left
        # Treat '*' as ')' to help balance '(' characters
        balance = 0
        for char in reversed(s):
            if char == ")" or char == "*":
                balance += 1
            else:  # '('
                balance -= 1

            if balance < 0:
                return False  # Unmatched '('

        return True


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: string s (JSON or raw)

    Example:
        "(*))"
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    # Handle both JSON quoted and raw strings
    s = json.loads(lines[0]) if lines[0].startswith('"') else lines[0]

    solver = get_solver(SOLUTIONS)
    result = solver.checkValidString(s)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

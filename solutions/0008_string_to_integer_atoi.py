"""
Problem: String to Integer (atoi)
Link: https://leetcode.com/problems/string-to-integer-atoi/

Convert string to 32-bit signed integer following atoi rules:
1. Skip leading whitespace (space ' ' only)
2. Read optional sign (+/-)
3. Read consecutive digits until non-digit
4. Clamp to [-2^31, 2^31 - 1]

Constraints:
- 0 <= s.length <= 200
- s consists of letters, digits (0-9), ' ', '+', '-', and '.'.

Topics: String
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "myAtoi",
        "complexity": "O(n) time, O(1) space",
        "description": "Linear scan with state machine approach",
    },
}


# JUDGE_FUNC for generated tests
INT_MIN = -(2 ** 31)
INT_MAX = 2 ** 31 - 1


def _reference(s: str) -> int:
    """Reference implementation."""
    s = s.lstrip(' ')
    if not s:
        return 0

    sign = 1
    idx = 0

    if s[0] == '-':
        sign = -1
        idx = 1
    elif s[0] == '+':
        idx = 1

    result = 0
    while idx < len(s) and s[idx].isdigit():
        result = result * 10 + int(s[idx])
        idx += 1

    result *= sign
    return max(INT_MIN, min(INT_MAX, result))


def judge(actual, expected, input_data: str) -> bool:
    import json
    s = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(s)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Linear Scan with Early Clamping
# Time: O(n), Space: O(1)
#   - Single pass through the string
#   - Early termination on overflow detection
# ============================================================================
class Solution:
    # Key insight: Process character by character, handle overflow early
    #
    # Steps:
    #   1. Skip leading spaces (only ' ', not other whitespace)
    #   2. Read sign if present (only one allowed)
    #   3. Read digits, accumulate result
    #   4. Clamp if result exceeds 32-bit signed range

    INT_MIN = -(2 ** 31)
    INT_MAX = 2 ** 31 - 1

    def myAtoi(self, s: str) -> int:
        n = len(s)
        idx = 0

        # Step 1: Skip leading whitespace
        while idx < n and s[idx] == ' ':
            idx += 1

        if idx == n:
            return 0

        # Step 2: Check for sign
        sign = 1
        if s[idx] == '-':
            sign = -1
            idx += 1
        elif s[idx] == '+':
            idx += 1

        # Step 3: Read digits
        result = 0
        while idx < n and s[idx].isdigit():
            digit = int(s[idx])

            # Check for overflow before adding digit
            # result * 10 + digit > INT_MAX
            if result > (self.INT_MAX - digit) // 10:
                return self.INT_MIN if sign == -1 else self.INT_MAX

            result = result * 10 + digit
            idx += 1

        return sign * result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: s (JSON string with quotes)

    Example:
        "42"
        -> 42
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    s = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.myAtoi(s)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

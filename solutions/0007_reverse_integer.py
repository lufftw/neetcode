# solutions/0007_reverse_integer.py
"""
Problem: Reverse Integer
https://leetcode.com/problems/reverse-integer/

Given a signed 32-bit integer x, return x with its digits reversed.
If reversing x causes the value to go outside the signed 32-bit integer
range [-2^31, 2^31 - 1], then return 0.

Key insight: We must handle overflow BEFORE it happens, not after.
Since we can't use 64-bit integers, we check if the next operation
would overflow by comparing against the threshold before multiplying.

Constraints:
- -2^31 <= x <= 2^31 - 1
"""
import json
import sys

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionMath",
        "method": "reverse",
        "complexity": "O(log n) time, O(1) space",
        "description": "Mathematical digit extraction with overflow check",
    },
    "string": {
        "class": "SolutionString",
        "method": "reverse",
        "complexity": "O(log n) time, O(log n) space",
        "description": "String reversal with boundary check",
    },
}


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate reverse integer result.
    For generated tests without expected output, we compute the answer.
    """
    if isinstance(actual, str):
        actual = json.loads(actual)

    # For generated tests, compute expected from input
    if expected is None:
        x = json.loads(input_data.strip())
        expected = _compute_reverse(x)
    elif isinstance(expected, str):
        expected = json.loads(expected)

    return actual == expected


def _compute_reverse(x: int) -> int:
    """Compute reversed integer with overflow check."""
    INT_MAX = 2**31 - 1
    INT_MIN = -(2**31)

    sign = 1 if x >= 0 else -1
    x = abs(x)

    reversed_str = str(x)[::-1]
    result = int(reversed_str) * sign

    if result < INT_MIN or result > INT_MAX:
        return 0
    return result


JUDGE_FUNC = judge


class SolutionMath:
    """
    Mathematical approach: Extract digits from right to left.

    WHY: We extract the last digit using mod 10 and build the reversed
    number by multiplying by 10. The key is checking for overflow BEFORE
    the operation, not after—we compare against INT_MAX/10 and INT_MIN/10.

    HOW: For x=123: extract 3, then 2, then 1. Build: 0→3→32→321.
    Check overflow at each step before multiplying.
    """

    def reverse(self, x: int) -> int:
        INT_MAX = 2**31 - 1  # 2147483647
        INT_MIN = -(2**31)   # -2147483648

        result = 0
        # Preserve sign for Python's mod behavior with negatives
        sign = 1 if x >= 0 else -1
        x = abs(x)

        while x != 0:
            digit = x % 10
            x //= 10

            # Check overflow BEFORE multiplying
            # If result > INT_MAX // 10, then result * 10 will overflow
            # If result == INT_MAX // 10, check if digit would push it over
            if result > INT_MAX // 10:
                return 0
            if result == INT_MAX // 10 and digit > 7:  # INT_MAX ends in 7
                return 0

            result = result * 10 + digit

        result *= sign

        # Final range check
        if result < INT_MIN or result > INT_MAX:
            return 0

        return result


class SolutionString:
    """
    String conversion approach.

    WHY: Python strings make reversal trivial with slicing [::-1].
    We convert to string, reverse, convert back, and check bounds.

    HOW: Convert abs(x) to string, reverse it, parse as int, apply sign,
    then check if result is within 32-bit signed integer range.
    """

    def reverse(self, x: int) -> int:
        INT_MAX = 2**31 - 1
        INT_MIN = -(2**31)

        sign = 1 if x >= 0 else -1
        x = abs(x)

        # Reverse string and convert back to int
        reversed_str = str(x)[::-1]
        result = int(reversed_str) * sign

        # Check 32-bit bounds
        if result < INT_MIN or result > INT_MAX:
            return 0

        return result


def solve():
    lines = sys.stdin.read().strip().split("\n")
    x = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.reverse(x)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

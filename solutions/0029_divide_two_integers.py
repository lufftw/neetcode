"""
Problem: Divide Two Integers
Link: https://leetcode.com/problems/divide-two-integers/

Given two integers dividend and divisor, divide two integers without using
multiplication, division, and mod operator.

The integer division should truncate toward zero.

Return the quotient after dividing dividend by divisor.

Note: Assume 32-bit signed integer environment. Clamp result to [-2^31, 2^31-1].

Constraints:
- -2^31 <= dividend, divisor <= 2^31 - 1
- divisor != 0

Topics: Math, Bit Manipulation
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "divide",
        "complexity": "O(log^2 n) time, O(1) space",
        "description": "Bit shifting with exponential search",
    },
}


# JUDGE_FUNC for generated tests
INT_MIN = -(2 ** 31)
INT_MAX = 2 ** 31 - 1


def _reference(dividend: int, divisor: int) -> int:
    """Reference implementation using Python's integer division."""
    # Handle overflow case
    if dividend == INT_MIN and divisor == -1:
        return INT_MAX

    # Python's // rounds toward negative infinity, we need toward zero
    sign = -1 if (dividend < 0) != (divisor < 0) else 1
    result = abs(dividend) // abs(divisor)
    return sign * result


def judge(actual, expected, input_data: str) -> bool:
    import json
    lines = input_data.strip().split('\n')
    dividend = json.loads(lines[0])
    divisor = json.loads(lines[1])
    # Parse actual if it's a string (JSON format from stdout)
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(dividend, divisor)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Bit Shifting with Exponential Search
# Time: O(log^2 n), Space: O(1)
#   - Outer loop runs O(log n) times as we halve the remaining dividend
#   - Inner loop finds the largest 2^k multiple, runs O(log n) times
#   - Cannot use *, /, % operators per problem constraints
# ============================================================================
class Solution:
    # Key insight: Division is repeated subtraction, but naive O(n) is too slow
    # Optimization: Use bit shifting to find largest 2^k such that divisor * 2^k <= dividend
    #
    # Algorithm:
    #   1. Handle sign separately, work with absolute values
    #   2. Repeatedly find largest power-of-2 multiple that fits
    #   3. Subtract that multiple and accumulate the quotient
    #
    # Edge case: -2^31 / -1 = 2^31 which overflows 32-bit signed int

    INT_MIN = -(2 ** 31)
    INT_MAX = 2 ** 31 - 1

    def divide(self, dividend: int, divisor: int) -> int:
        # Special case: overflow when dividing INT_MIN by -1
        if dividend == self.INT_MIN and divisor == -1:
            return self.INT_MAX

        # Determine sign of result
        negative = (dividend < 0) != (divisor < 0)

        # Work with positive values (use abs carefully for INT_MIN)
        dividend = abs(dividend)
        divisor = abs(divisor)

        quotient = 0

        # Keep subtracting the largest possible multiple of divisor
        while dividend >= divisor:
            # Find the largest k such that divisor << k <= dividend
            temp_divisor = divisor
            multiple = 1

            # Double temp_divisor while it's still <= dividend
            # Use (temp_divisor << 1) > dividend to avoid potential overflow
            while (temp_divisor << 1) <= dividend:
                temp_divisor <<= 1
                multiple <<= 1

            # Subtract this multiple from dividend, add to quotient
            dividend -= temp_divisor
            quotient += multiple

        return -quotient if negative else quotient


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: dividend (integer)
        Line 2: divisor (integer)

    Example:
        10
        3
        -> 3
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    dividend = json.loads(lines[0])
    divisor = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.divide(dividend, divisor)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

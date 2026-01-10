"""
Problem: Fraction to Recurring Decimal
Link: https://leetcode.com/problems/fraction-to-recurring-decimal/

Convert fraction to decimal string, with repeating part in parentheses.

Constraints:
- -2^31 <= numerator, denominator <= 2^31 - 1
- denominator != 0

Topics: Hash Table, Math, String
"""
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "fractionToDecimal",
        "complexity": "O(d) time and space where d is period length",
        "description": "Long division with remainder tracking to detect cycles",
    },
}


# ============================================================================
# JUDGE_FUNC: Verify decimal string represents the exact fraction
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate that actual decimal string correctly represents numerator/denominator.

    Parses the decimal string (with optional repeating part in parentheses)
    and verifies it equals the input fraction using arithmetic.
    """
    lines = input_data.strip().split('\n')
    numerator = int(lines[0])
    denominator = int(lines[1])

    # Convert actual to string (runner may parse as float for simple decimals)
    s = str(actual).strip().strip('"')

    if not s:
        return False

    # Handle sign
    negative = s.startswith('-')
    if negative:
        s = s[1:]

    # Split integer and fractional parts
    if '.' not in s:
        # Integer result
        try:
            value = int(s)
            if negative:
                value = -value
            return value * denominator == numerator
        except ValueError:
            return False

    int_part, frac_part = s.split('.', 1)

    # Parse repeating part if present
    if '(' in frac_part:
        # Format: "non_repeat(repeat)"
        idx = frac_part.index('(')
        non_repeat = frac_part[:idx]
        repeat = frac_part[idx + 1:-1]  # Remove ( and )
    else:
        non_repeat = frac_part
        repeat = ""

    # Convert to fraction using formula:
    # If decimal is a.bc(de) where bc is non-repeating and de is repeating:
    # value = a + bc/10^len(bc) + de/(10^len(bc) * (10^len(de) - 1))

    from fractions import Fraction

    try:
        result = Fraction(int(int_part) if int_part else 0)

        if non_repeat:
            result += Fraction(int(non_repeat), 10 ** len(non_repeat))

        if repeat:
            # Repeating part: repeat / (10^len(non_repeat) * (10^len(repeat) - 1))
            repeat_denom = (10 ** len(non_repeat)) * (10 ** len(repeat) - 1)
            result += Fraction(int(repeat), repeat_denom)

        if negative:
            result = -result

        target = Fraction(numerator, denominator)
        return result == target

    except (ValueError, ZeroDivisionError):
        return False


JUDGE_FUNC = judge


# ============================================================================
# Solution: Long Division with Remainder Map
# Time: O(d), Space: O(d) where d is the period of the repeating decimal
# ============================================================================
class Solution:
    # Key insight: In long division, if we see the same remainder twice,
    # the decimal starts repeating from that point.
    #
    # Track (remainder -> position in result) to detect cycle start.
    #
    # Edge cases:
    # - Negative numbers: handle sign separately
    # - Integer result: no decimal point
    # - Overflow: use abs() carefully with -2^31

    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        if numerator == 0:
            return "0"

        result = []

        # Handle sign
        if (numerator < 0) != (denominator < 0):
            result.append("-")

        # Work with absolute values
        num = abs(numerator)
        den = abs(denominator)

        # Integer part
        result.append(str(num // den))
        remainder = num % den

        if remainder == 0:
            return "".join(result)

        result.append(".")

        # Fractional part with cycle detection
        remainder_map = {}  # remainder -> position in result
        while remainder != 0:
            if remainder in remainder_map:
                # Found cycle - insert parentheses
                pos = remainder_map[remainder]
                result.insert(pos, "(")
                result.append(")")
                break

            remainder_map[remainder] = len(result)
            remainder *= 10
            result.append(str(remainder // den))
            remainder %= den

        return "".join(result)


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: numerator (integer)
        Line 2: denominator (integer)

    Example:
        2
        3
        -> "0.(6)"
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    numerator = int(lines[0])
    denominator = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.fractionToDecimal(numerator, denominator)

    print(result)


if __name__ == "__main__":
    solve()

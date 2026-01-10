"""
Problem: Abbreviating the Product of a Range
Link: https://leetcode.com/problems/abbreviating-the-product-of-a-range/

Compute product of [left, right] and format as:
- "preC" if digits <= 10
- "pre...sufeC" if digits > 10
where C = trailing zeros, pre = first 5 digits, suf = last 5 non-zero digits

Constraints:
- 1 <= left <= right <= 10^4

Topics: Math
"""
import math
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "abbreviateProduct",
        "complexity": "O(n) time, O(1) space",
        "description": "Factor counting + modular arithmetic + logarithms",
    },
}


# JUDGE_FUNC for generated tests
def _reference(left: int, right: int) -> str:
    """Reference implementation."""
    # Compute actual product for correctness check
    product = 1
    for i in range(left, right + 1):
        product *= i

    # Count trailing zeros
    trailing_zeros = 0
    temp = product
    while temp % 10 == 0:
        trailing_zeros += 1
        temp //= 10

    # Get non-zero product
    s = str(temp)

    if len(s) <= 10:
        return f"{s}e{trailing_zeros}"
    else:
        return f"{s[:5]}...{s[-5:]}e{trailing_zeros}"


def judge(actual, expected, input_data: str) -> bool:
    import json
    lines = input_data.strip().split('\n')
    left = json.loads(lines[0])
    right = json.loads(lines[1])
    if isinstance(actual, str):
        # actual is already a string in quotes from JSON output
        if actual.startswith('"') and actual.endswith('"'):
            actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            if expected.startswith('"') and expected.endswith('"'):
                expected = json.loads(expected)
        return actual == expected
    return actual == _reference(left, right)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Factor Counting + Modular Arithmetic + Logarithms
# Time: O(n), Space: O(1)
# ============================================================================
class Solution:
    def abbreviateProduct(self, left: int, right: int) -> str:
        # Count factors of 2 and 5 to determine trailing zeros
        twos = fives = 0
        for i in range(left, right + 1):
            x = i
            while x % 2 == 0:
                twos += 1
                x //= 2
            x = i
            while x % 5 == 0:
                fives += 1
                x //= 5

        trailing_zeros = min(twos, fives)

        # Compute last 5 digits (mod 10^5) after removing trailing zeros
        # We need to divide out exactly 'trailing_zeros' 2s and 5s
        MOD = 10 ** 5
        suffix = 1
        twos_to_remove = trailing_zeros
        fives_to_remove = trailing_zeros

        for i in range(left, right + 1):
            x = i
            while twos_to_remove > 0 and x % 2 == 0:
                x //= 2
                twos_to_remove -= 1
            while fives_to_remove > 0 and x % 5 == 0:
                x //= 5
                fives_to_remove -= 1
            suffix = (suffix * x) % MOD

        # Compute first 5 digits using logarithms
        log_sum = 0.0
        for i in range(left, right + 1):
            log_sum += math.log10(i)

        log_sum -= trailing_zeros  # Remove trailing zeros

        # Check if we need abbreviation (more than 10 digits)
        total_digits = int(log_sum) + 1

        if total_digits <= 10:
            # Compute exact product without trailing zeros
            product = 1
            twos_to_remove = trailing_zeros
            fives_to_remove = trailing_zeros
            for i in range(left, right + 1):
                x = i
                while twos_to_remove > 0 and x % 2 == 0:
                    x //= 2
                    twos_to_remove -= 1
                while fives_to_remove > 0 and x % 5 == 0:
                    x //= 5
                    fives_to_remove -= 1
                product *= x
            return f"{product}e{trailing_zeros}"

        # Get first 5 digits
        frac_part = log_sum - int(log_sum)
        prefix = int(10 ** (frac_part + 4))

        # Format suffix with leading zeros if needed
        suffix_str = str(suffix).zfill(5)[-5:]

        return f"{prefix}...{suffix_str}e{trailing_zeros}"


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: left (integer)
        Line 2: right (integer)

    Example:
        1
        4
        -> "24e0"
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    left = json.loads(lines[0])
    right = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.abbreviateProduct(left, right)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

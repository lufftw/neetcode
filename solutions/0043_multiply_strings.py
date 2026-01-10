# solutions/0043_multiply_strings.py
"""
Problem 0043 - Multiply Strings

Given two non-negative integers num1 and num2 represented as strings,
return the product of num1 and num2, also represented as a string.

Note: You must not use any built-in BigInteger library or convert
the inputs to integer directly.

LeetCode Constraints:
- 1 <= num1.length, num2.length <= 200
- num1 and num2 consist of digits only
- Both num1 and num2 do not contain any leading zero, except "0" itself

Key Insight:
For two numbers with m and n digits, the product has at most m+n digits.
Position i in num1 times position j in num2 contributes to position (i+j)
and (i+j+1) in the result (when indexed from the end).

Grade-school multiplication:
     123
   x  45
   -----
     615   (123 * 5)
    492    (123 * 4, shifted)
   -----
    5535

We can compute all digit products, accumulate in result array, then
handle carries and convert to string.

Solution Approaches:
1. Grade-school multiplication with result array: O(m*n) time, O(m+n) space
2. Optimized single-pass: same complexity but cleaner implementation
"""
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionGradeSchool",
        "method": "multiply",
        "complexity": "O(m*n) time, O(m+n) space",
        "description": "Grade-school multiplication with position tracking",
    },
    "optimized": {
        "class": "SolutionOptimized",
        "method": "multiply",
        "complexity": "O(m*n) time, O(m+n) space",
        "description": "Single-pass accumulation with deferred carry",
    },
}


class SolutionGradeSchool:
    """
    Grade-school multiplication simulating manual computation.

    Create a result array of size m+n (max possible digits).
    For each pair of digits at positions i (num1) and j (num2):
    - The product contributes to positions (i+j) and (i+j+1) in result
    - Accumulate products, then propagate carries

    Key observation: digit at num1[i] * num2[j] affects result positions
    when both are indexed from the END. So we work right-to-left.
    """

    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"

        m, n = len(num1), len(num2)
        result = [0] * (m + n)

        # Multiply each digit pair
        # Reverse iteration: rightmost digit first
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                product = int(num1[i]) * int(num2[j])

                # Positions in result array
                p1 = i + j      # Higher position (carry goes here)
                p2 = i + j + 1  # Lower position

                # Add to existing value
                total = product + result[p2]

                result[p2] = total % 10
                result[p1] += total // 10

        # Convert to string, skip leading zeros
        result_str = "".join(map(str, result))
        return result_str.lstrip("0") or "0"


class SolutionOptimized:
    """
    Optimized approach with cleaner index handling.

    Same algorithm but with explicit carry handling at each step
    and cleaner accumulation logic.

    The result array stores intermediate sums that may exceed 9.
    After all multiplications, we do a final pass to normalize carries.
    """

    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"

        m, n = len(num1), len(num2)
        # Result array to accumulate products (can be > 9 temporarily)
        result = [0] * (m + n)

        # Convert to digit arrays (reversed for easier indexing)
        d1 = [int(c) for c in reversed(num1)]
        d2 = [int(c) for c in reversed(num2)]

        # Multiply and accumulate
        for i, digit1 in enumerate(d1):
            for j, digit2 in enumerate(d2):
                result[i + j] += digit1 * digit2

        # Propagate carries
        carry = 0
        for i in range(len(result)):
            total = result[i] + carry
            result[i] = total % 10
            carry = total // 10

        # Convert to string (reverse back)
        result_str = "".join(map(str, reversed(result)))
        return result_str.lstrip("0") or "0"


def solve():
    import sys

    lines = sys.stdin.read().strip().split("\n")

    # Handle both raw and JSON-quoted strings
    num1 = lines[0].strip('"')
    num2 = lines[1].strip('"')

    solver = get_solver(SOLUTIONS)
    result = solver.multiply(num1, num2)

    # Output string directly without JSON quotes
    print(result)


if __name__ == "__main__":
    solve()

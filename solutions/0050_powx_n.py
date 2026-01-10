# solutions/0050_powx_n.py
"""
Problem: Pow(x, n)
https://leetcode.com/problems/powx-n/

Implement pow(x, n), which calculates x raised to the power n.

Constraints:
- -100.0 < x < 100.0
- -2^31 <= n <= 2^31 - 1
- n is an integer
- Either x is not zero or n > 0
- -10^4 <= x^n <= 10^4
"""
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionIterative",
        "method": "myPow",
        "complexity": "O(log n) time, O(1) space",
        "description": "Iterative binary exponentiation",
    },
    "recursive": {
        "class": "SolutionRecursive",
        "method": "myPow",
        "complexity": "O(log n) time, O(log n) space",
        "description": "Recursive binary exponentiation",
    },
}


class SolutionIterative:
    """
    Iterative binary exponentiation (exponentiation by squaring).

    Key insight: x^n can be computed in O(log n) multiplications by
    decomposing n into binary. For example, x^13 = x^8 * x^4 * x^1
    since 13 = 1101 in binary.

    At each step, we check if current bit is set (n & 1). If so,
    multiply result by current power of x. Then square x and shift n.
    Handles negative exponents by inverting x and negating n.
    """

    def myPow(self, x: float, n: int) -> float:
        # Handle negative exponent: x^(-n) = (1/x)^n
        if n < 0:
            x = 1 / x
            n = -n

        result = 1.0

        while n > 0:
            # If current bit is set, multiply result by current power
            if n & 1:
                result *= x

            # Square x for next bit position
            x *= x
            # Move to next bit
            n >>= 1

        return result


class SolutionRecursive:
    """
    Recursive binary exponentiation with divide and conquer.

    The recurrence relation is:
    - x^n = (x^(n/2))^2 if n is even
    - x^n = x * (x^(n/2))^2 if n is odd
    - x^0 = 1 (base case)

    This naturally halves the problem each step, giving O(log n) depth.
    Uses O(log n) stack space for recursion.
    """

    def myPow(self, x: float, n: int) -> float:
        # Handle negative exponent
        if n < 0:
            x = 1 / x
            n = -n

        return self._pow(x, n)

    def _pow(self, x: float, n: int) -> float:
        # Base case
        if n == 0:
            return 1.0

        # Recursive case: compute x^(n/2)
        half = self._pow(x, n // 2)

        # Square the result
        if n % 2 == 0:
            return half * half
        else:
            return half * half * x


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate power computation with tolerance for floating point.
    """
    import json

    lines = input_data.strip().split("\n")
    x = json.loads(lines[0])
    n = json.loads(lines[1])

    # Compute expected using Python's pow
    expected_result = pow(x, n)

    # Allow small relative error for floating point
    if expected_result == 0:
        return abs(actual) < 1e-9
    return abs(actual - expected_result) / abs(expected_result) < 1e-5


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: x and n
    x = json.loads(lines[0])
    n = json.loads(lines[1])

    # Get solver and compute power
    solver = get_solver(SOLUTIONS)
    result = solver.myPow(x, n)

    # Output with reasonable precision
    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

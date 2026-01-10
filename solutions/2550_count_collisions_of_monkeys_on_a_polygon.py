"""
Problem: Count Collisions of Monkeys on a Polygon
Link: https://leetcode.com/problems/count-collisions-of-monkeys-on-a-polygon/

Count ways monkeys can move such that at least one collision happens.

Constraints:
- 3 <= n <= 10^9

Topics: Math, Recursion
"""
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "monkeyMove",
        "complexity": "O(log n) time, O(1) space",
        "description": "Combinatorics: total ways - collision-free ways = 2^n - 2",
    },
}


# JUDGE_FUNC for generated tests
def _reference(n: int) -> int:
    """Reference implementation."""
    MOD = 10 ** 9 + 7
    return (pow(2, n, MOD) - 2) % MOD


def judge(actual, expected, input_data: str) -> bool:
    n = int(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(n)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Combinatorics with Modular Exponentiation
# Time: O(log n), Space: O(1)
# ============================================================================
class Solution:
    # Key insight: Each monkey has 2 choices (clockwise or counter-clockwise).
    # Total possible movements = 2^n
    #
    # Collision-free scenarios: All monkeys move in the SAME direction.
    # - All clockwise: no vertex/edge collision
    # - All counter-clockwise: no vertex/edge collision
    # That's exactly 2 collision-free ways.
    #
    # Answer = 2^n - 2 (mod 10^9 + 7)
    #
    # Use Python's built-in pow(base, exp, mod) for efficient modular exponentiation.

    def monkeyMove(self, n: int) -> int:
        MOD = 10 ** 9 + 7
        # 2^n mod MOD, then subtract 2
        return (pow(2, n, MOD) - 2) % MOD


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: n (integer)

    Example:
        3
        -> 6
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.monkeyMove(n)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

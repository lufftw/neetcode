"""
Problem: Sum of Numbers With Units Digit K
Link: https://leetcode.com/problems/sum-of-numbers-with-units-digit-k/

Find minimum count of positive integers, each with units digit k, that sum to num.

Constraints:
- 0 <= num <= 3000
- 0 <= k <= 9

Topics: Math, Dynamic Programming, Greedy, Enumeration
"""
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minimumNumbers",
        "complexity": "O(1) time, O(1) space",
        "description": "Check n from 1 to 10 for valid units digit match",
    },
}


# JUDGE_FUNC for generated tests
def _reference(num: int, k: int) -> int:
    """Reference implementation."""
    if num == 0:
        return 0
    for n in range(1, 11):
        if (n * k) % 10 == num % 10 and n * k <= num:
            return n
    return -1


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    num = int(lines[0])
    k = int(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(num, k)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Units Digit Cycle
# Time: O(1), Space: O(1)
# ============================================================================
class Solution:
    # Key insight:
    #   - n numbers with units digit k → sum has units digit (n * k) % 10
    #   - We need (n * k) % 10 == num % 10
    #   - Also n * k <= num (minimum sum using k n times)
    #
    # Why check only n from 1 to 10:
    #   - Units digit cycles every 10 values of n
    #   - If a valid n exists, the smallest is within 1-10

    def minimumNumbers(self, num: int, k: int) -> int:
        if num == 0:
            return 0

        for n in range(1, 11):
            # n numbers with units digit k: min sum is n*k
            # sum has units digit (n*k) % 10
            if (n * k) % 10 == num % 10 and n * k <= num:
                return n

        return -1


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: num (integer)
        Line 2: k (integer)

    Example:
        58
        9
        -> 2
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    num = int(lines[0])
    k = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.minimumNumbers(num, k)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

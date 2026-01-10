"""
Problem: Prime Palindrome
Link: https://leetcode.com/problems/prime-palindrome/

Given n, return smallest prime palindrome >= n.

Constraints:
- 1 <= n <= 10^8
- Answer always in range [2, 2 * 10^8]

Topics: Math
"""
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "primePalindrome",
        "complexity": "O(sqrt(N) * N^(1/2)) time, O(log N) space",
        "description": "Generate odd-digit palindromes, skip even-digit (divisible by 11)",
    },
}


# JUDGE_FUNC for generated tests
def _reference(n: int) -> int:
    """Reference implementation."""
    def is_prime(x):
        if x < 2:
            return False
        if x == 2:
            return True
        if x % 2 == 0:
            return False
        for i in range(3, int(x**0.5) + 1, 2):
            if x % i == 0:
                return False
        return True

    for p in [2, 3, 5, 7, 11]:
        if p >= n:
            return p

    for length in range(3, 10, 2):
        half_len = (length + 1) // 2
        start = 10 ** (half_len - 1)
        end = 10 ** half_len
        for half in range(start, end):
            s = str(half)
            pal = int(s + s[-2::-1])
            if pal >= n and is_prime(pal):
                return pal
    return -1


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
# Solution: Generate Palindromes
# Time: O(sqrt(N) per primality check), Space: O(log N) for string
# ============================================================================
class Solution:
    # Key insight:
    #   - All even-digit palindromes > 11 are divisible by 11
    #   - Proof: ABBA = 1001A + 110B = 11(91A + 10B)
    #   - So only check: single digits, 11, and odd-digit palindromes
    #
    # Generate palindromes by constructing from left half:
    #   - For 3-digit (half_len=2): "10" -> "101", "12" -> "121"
    #   - For 5-digit (half_len=3): "100" -> "10001", "123" -> "12321"

    def primePalindrome(self, n: int) -> int:
        def is_prime(x: int) -> bool:
            if x < 2:
                return False
            if x == 2:
                return True
            if x % 2 == 0:
                return False
            for i in range(3, int(x**0.5) + 1, 2):
                if x % i == 0:
                    return False
            return True

        # Handle small primes and 11 (only even-digit prime palindrome)
        for p in [2, 3, 5, 7, 11]:
            if p >= n:
                return p

        # Generate odd-digit palindromes (3, 5, 7, 9 digits)
        for length in range(3, 10, 2):
            half_len = (length + 1) // 2
            start = 10 ** (half_len - 1)
            end = 10 ** half_len

            for half in range(start, end):
                s = str(half)
                # Mirror all but last char to create palindrome
                palindrome_str = s + s[-2::-1]
                palindrome = int(palindrome_str)

                if palindrome >= n and is_prime(palindrome):
                    return palindrome

        return -1  # Should not reach here per problem constraints


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: n (integer)

    Example:
        6
        -> 7
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.primePalindrome(n)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

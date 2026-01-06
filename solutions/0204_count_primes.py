"""
LeetCode 204: Count Primes
https://leetcode.com/problems/count-primes/

Pattern: Math / Number Theory - Prime Sieve
API Kernel: MathNumberTheory

Given an integer n, return the number of prime numbers that are strictly less than n.
"""

import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionSieve",
        "method": "countPrimes",
        "complexity": "O(n log log n) time, O(n) space",
        "description": "Sieve of Eratosthenes",
    },
}


def _reference_count_primes(n: int) -> int:
    """Reference implementation for validation."""
    if n < 2:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if is_prime[p]:
            for m in range(p * p, n, p):
                is_prime[m] = False
    return sum(is_prime)


def judge(actual, expected, input_data: str) -> bool:
    """Custom judge using reference implementation."""
    n = json.loads(input_data.strip())
    correct = _reference_count_primes(n)
    try:
        actual_val = int(actual) if isinstance(actual, str) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


class SolutionSieve:
    """
    Sieve of Eratosthenes.

    1. Create boolean array is_prime[0..n-1], init all True
    2. Mark 0 and 1 as not prime
    3. For each p from 2 to sqrt(n):
       - If p is prime, mark all multiples p*p, p*p+p, ... as not prime
    4. Count remaining Trues

    Optimization: Start marking from p*p (smaller multiples already marked)
    """

    def countPrimes(self, n: int) -> int:
        if n < 2:
            return 0

        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False

        for p in range(2, int(n ** 0.5) + 1):
            if is_prime[p]:
                # Mark multiples starting from p*p
                for m in range(p * p, n, p):
                    is_prime[m] = False

        return sum(is_prime)


def solve():
    lines = sys.stdin.read().strip().split("\n")

    n = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.countPrimes(n)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

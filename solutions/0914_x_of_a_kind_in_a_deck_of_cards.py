"""
Problem: X of a Kind in a Deck of Cards
Link: https://leetcode.com/problems/x-of-a-kind-in-a-deck-of-cards/

Check if deck can be partitioned into groups of X cards with same number.

Constraints:
- 1 <= deck.length <= 10^4
- 0 <= deck[i] < 10^4

Topics: Array, Hash Table, Math, Counting, Number Theory
"""
from typing import List
from _runner import get_solver
import json
from math import gcd
from functools import reduce
from collections import Counter


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "hasGroupsSizeX",
        "complexity": "O(n log^2 n) time, O(n) space",
        "description": "Count cards, check if GCD of all counts >= 2",
    },
}


# JUDGE_FUNC for generated tests
def _reference(deck: List[int]) -> bool:
    """Reference implementation."""
    counts = Counter(deck).values()
    return reduce(gcd, counts) >= 2


def judge(actual, expected, input_data: str) -> bool:
    deck = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(deck)


JUDGE_FUNC = judge


# ============================================================================
# Solution: GCD of Counts
# Time: O(n log^2 n), Space: O(n)
# ============================================================================
class Solution:
    # Key insight: We need a group size X that divides ALL counts.
    # X must be >= 2 (at least pairs).
    #
    # The largest such X is the GCD of all counts.
    # If GCD >= 2, we can partition into groups of size GCD (or any divisor).
    # If GCD == 1, no valid partition exists.

    def hasGroupsSizeX(self, deck: List[int]) -> bool:
        counts = Counter(deck).values()
        return reduce(gcd, counts) >= 2


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: deck (JSON array)

    Example:
        [1,2,3,4,4,3,2,1]
        -> true
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    deck = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.hasGroupsSizeX(deck)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

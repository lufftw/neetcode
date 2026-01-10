"""
Problem: Stone Game IX
Link: https://leetcode.com/problems/stone-game-ix/

Two players remove stones; player loses if sum of removed stones is divisible by 3.
Bob wins if no stones remain. Determine if Alice wins with optimal play.

Constraints:
- 1 <= stones.length <= 10^5
- 1 <= stones[i] <= 10^4

Topics: Array, Math, Counting, Game Theory
"""
from typing import List
from _runner import get_solver
import json
from collections import Counter


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "stoneGameIX",
        "complexity": "O(n) time, O(1) space",
        "description": "Count stones by mod 3 remainder, analyze game states",
    },
}


# JUDGE_FUNC for generated tests
def _reference(stones: List[int]) -> bool:
    """Reference implementation."""
    cnt = Counter(s % 3 for s in stones)
    if cnt[0] % 2 == 0:
        return min(cnt[1], cnt[2]) > 0
    return abs(cnt[1] - cnt[2]) > 2


def judge(actual, expected, input_data: str) -> bool:
    stones = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(stones)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Modular Arithmetic Game Analysis
# Time: O(n), Space: O(1)
# ============================================================================
class Solution:
    # Key insight: Only value mod 3 matters. Count stones by remainder.
    #
    # Let cnt[0], cnt[1], cnt[2] = counts of stones with remainder 0, 1, 2.
    #
    # Stones with remainder 0 don't change sum mod 3, just flip turn parity.
    # Game strategy depends on who forces whom into a losing position.
    #
    # Analysis:
    # - Alice must avoid sum divisible by 3 on her turns
    # - First stone: Alice picks 1 or 2 (picking 0 immediately loses)
    # - After picking 1: next must pick 1 to avoid sum=3 (mod 3)
    # - After picking 2: next must pick 2 to avoid sum=3 (mod 3)
    #
    # If cnt[0] is even (turn parity unchanged):
    #   Alice wins if min(cnt[1], cnt[2]) > 0
    #   (She can start a sequence and force Bob to run out)
    #
    # If cnt[0] is odd (turn parity flipped):
    #   Alice wins if |cnt[1] - cnt[2]| > 2
    #   (The extra 0's allow Bob to survive unless big imbalance)

    def stoneGameIX(self, stones: List[int]) -> bool:
        cnt = Counter(s % 3 for s in stones)

        if cnt[0] % 2 == 0:
            # Even zeros: Alice wins if both 1's and 2's exist
            return min(cnt[1], cnt[2]) > 0
        else:
            # Odd zeros: Alice needs significant imbalance
            return abs(cnt[1] - cnt[2]) > 2


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: stones (JSON array)

    Example:
        [2,1]
        -> true
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    stones = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.stoneGameIX(stones)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

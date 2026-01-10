"""
Problem: Can Place Flowers
Link: https://leetcode.com/problems/can-place-flowers/

Check if n flowers can be planted without adjacent flowers.
0 = empty, 1 = occupied.

Constraints:
- 1 <= flowerbed.length <= 2 * 10^4
- 0 <= n <= flowerbed.length
- No two adjacent flowers initially

Topics: Array, Greedy
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "canPlaceFlowers",
        "complexity": "O(n) time, O(1) space",
        "description": "Greedy placement when position and neighbors are empty",
    },
}


# JUDGE_FUNC for generated tests
def _reference(flowerbed: List[int], n: int) -> bool:
    """Reference implementation."""
    fb = flowerbed[:]
    count = 0
    for i in range(len(fb)):
        if fb[i] == 0:
            left_ok = (i == 0) or (fb[i-1] == 0)
            right_ok = (i == len(fb)-1) or (fb[i+1] == 0)
            if left_ok and right_ok:
                fb[i] = 1
                count += 1
    return count >= n


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    flowerbed = json.loads(lines[0])
    n = int(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(flowerbed, n)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Greedy
# Time: O(n), Space: O(1)
# ============================================================================
class Solution:
    # Greedy: scan and plant whenever valid (left, current, right all 0)
    # Treat boundaries as 0 (can plant at edge if neighbor is 0)

    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        length = len(flowerbed)
        count = 0

        for i in range(length):
            if flowerbed[i] == 0:
                left_empty = (i == 0) or (flowerbed[i - 1] == 0)
                right_empty = (i == length - 1) or (flowerbed[i + 1] == 0)

                if left_empty and right_empty:
                    flowerbed[i] = 1  # Plant flower
                    count += 1
                    if count >= n:
                        return True

        return count >= n


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: flowerbed (JSON array)
        Line 2: n (integer)

    Example:
        [1,0,0,0,1]
        1
        -> true
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    flowerbed = json.loads(lines[0])
    n = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.canPlaceFlowers(flowerbed, n)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

# solutions/1046_last_stone_weight.py
"""
Problem: Last Stone Weight
Link: https://leetcode.com/problems/last-stone-weight/

You are given an array of integers stones where stones[i] is the weight of the ith stone.

We are playing a game with the stones. On each turn, we choose the heaviest two stones
and smash them together. Suppose the heaviest two stones have weights x and y with x <= y.
The result of this smash is:
- If x == y, both stones are destroyed, and
- If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.

At the end of the game, there is at most one stone left.
Return the weight of the last remaining stone. If there are no stones left, return 0.

Example 1:
    Input: stones = [2,7,4,1,8,1]
    Output: 1
    Explanation:
        We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
        we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
        we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
        we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.

Example 2:
    Input: stones = [1]
    Output: 1

Constraints:
- 1 <= stones.length <= 30
- 1 <= stones[i] <= 1000

Topics: Array, Heap Priority Queue
"""

import json
from typing import List
import heapq

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionHeap",
        "method": "lastStoneWeight",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Max-heap simulation of stone smashing",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is correct last stone weight.

    Args:
        actual: Program output (integer as string or int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (stones as JSON)

    Returns:
        bool: True if correct last stone weight
    """
    lines = input_data.strip().split("\n")
    stones = json.loads(lines[0]) if lines[0] else []

    # Compute correct answer
    correct = _reference_last_stone(stones)

    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _reference_last_stone(stones: List[int]) -> int:
    """Reference implementation using max-heap."""
    max_heap = [-stone for stone in stones]
    heapq.heapify(max_heap)

    while len(max_heap) > 1:
        largest = -heapq.heappop(max_heap)
        second = -heapq.heappop(max_heap)
        if largest != second:
            heapq.heappush(max_heap, -(largest - second))

    return -max_heap[0] if max_heap else 0


JUDGE_FUNC = judge


# ============================================================================
# Solution: Max-Heap Simulation
# Time: O(n log n), Space: O(n)
#
# Pattern: heap_greedy_simulation
# See: docs/patterns/heap/templates.md Section 7 (Last Stone Weight)
# ============================================================================
class SolutionHeap:
    def lastStoneWeight(self, stones: List[int]) -> int:
        """
        Simulate stone smashing using max-heap.

        Game Rules:
        1. Pick two heaviest stones x, y (x <= y)
        2. If x == y: both destroyed
        3. If x != y: stone of weight y - x remains

        Why max-heap?
        - Need repeated access to two largest elements
        - Python heapq is min-heap, so negate values
        - O(log n) per smash vs O(n) for linear search

        Time Analysis:
        - Heapify: O(n)
        - Each smash: 2 pops + 0-1 push = O(log n)
        - At most n-1 smashes (each reduces count by at least 1)
        - Total: O(n log n)
        """
        # Convert to max-heap (negate all values)
        max_heap: list[int] = [-stone for stone in stones]
        heapq.heapify(max_heap)  # O(n) heapify

        # Simulate until 0 or 1 stone remains
        while len(max_heap) > 1:
            # Pop two largest (remember to negate)
            largest = -heapq.heappop(max_heap)
            second = -heapq.heappop(max_heap)

            # If different weights, push the difference
            if largest != second:
                heapq.heappush(max_heap, -(largest - second))

        # Return last stone weight (or 0 if no stones left)
        return -max_heap[0] if max_heap else 0


def solve():
    """
    Input format (JSON per line):
        Line 1: stones as JSON array

    Output format:
        Integer - weight of last stone (or 0)
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    stones = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.lastStoneWeight(stones)

    print(result)


if __name__ == "__main__":
    solve()

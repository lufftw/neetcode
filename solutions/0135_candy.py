"""
Problem: Candy
Link: https://leetcode.com/problems/candy/

There are n children standing in a line. Each child is assigned a rating value
given in the integer array ratings.

You are giving candies to these children subjected to the following requirements:
- Each child must have at least one candy.
- Children with a higher rating get more candies than their neighbors.

Return the minimum number of candies you need to have to distribute the candies
to the children.

Example 1:
    Input: ratings = [1,0,2]
    Output: 5
    Explanation: You can allocate to the first, second and third child with
                 2, 1, 2 candies respectively.

Example 2:
    Input: ratings = [1,2,2]
    Output: 4
    Explanation: You can allocate to the first, second and third child with
                 1, 2, 1 candies respectively.
                 The third child gets 1 candy because it satisfies the above conditions.

Constraints:
- n == ratings.length
- 1 <= n <= 2 * 10^4
- 0 <= ratings[i] <= 2 * 10^4

Topics: Array, Greedy
Pattern: GreedyCore - Two-Pass Greedy
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPass",
        "method": "candy",
        "complexity": "O(n) time, O(n) space",
        "description": "Two-pass: left-to-right then right-to-left",
    },
    "two_pass": {
        "class": "SolutionTwoPass",
        "method": "candy",
        "complexity": "O(n) time, O(n) space",
        "description": "Two-pass: left-to-right then right-to-left",
    },
}


# ============================================================================
# JUDGE_FUNC - Validate candy distribution
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate minimum candies result."""
    ratings = json.loads(input_data.strip())
    correct = _reference_candy(ratings)

    if isinstance(actual, int):
        actual_int = actual
    elif isinstance(actual, str):
        try:
            actual_int = int(actual.strip())
        except ValueError:
            return False
    else:
        return False

    return actual_int == correct


def _reference_candy(ratings: List[int]) -> int:
    """O(n) reference using two-pass greedy."""
    n = len(ratings)
    candies = [1] * n

    # Left to right: handle increasing sequences
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # Right to left: handle decreasing sequences
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Two-Pass Greedy
# Time: O(n), Space: O(n)
#
# Core Insight:
#   The constraint "higher rating than neighbor -> more candy" creates
#   two independent sub-problems:
#   1. Each child must have more candy than LEFT neighbor if rating is higher
#   2. Each child must have more candy than RIGHT neighbor if rating is higher
#
#   We handle each direction separately, then take max at each position.
#
# Two-Pass Strategy:
#   Pass 1 (left-to-right): If rating[i] > rating[i-1], give more than left
#   Pass 2 (right-to-left): If rating[i] > rating[i+1], ensure more than right
#
# Why Two Passes Work:
#   - Single pass can't handle both increasing and decreasing sequences
#   - Example: [1, 2, 3, 2, 1] needs peak at index 2 to satisfy both sides
#
# Pattern Reference: GreedyCore - Two-Pass
# ============================================================================
class SolutionTwoPass:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        candies = [1] * n  # Everyone starts with 1 candy

        # Pass 1: Left to right
        # Ensure higher rating than left neighbor -> more candy
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1

        # Pass 2: Right to left
        # Ensure higher rating than right neighbor -> more candy
        # Take max to preserve left-to-right constraints
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)

        return sum(candies)


def solve():
    """
    Input format (JSON per line):
        Line 1: ratings as JSON array

    Output format:
        Integer (minimum total candies)
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    ratings = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.candy(ratings)

    print(result)


if __name__ == "__main__":
    solve()

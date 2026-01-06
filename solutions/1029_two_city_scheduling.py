"""
Problem: Two City Scheduling
Link: https://leetcode.com/problems/two-city-scheduling/

A company is planning to interview 2n people. Given the array costs where
costs[i] = [aCosti, bCosti], the cost of flying the ith person to city a
is aCosti, and the cost of flying the ith person to city b is bCosti.

Return the minimum cost to fly every person to a city such that exactly n
people arrive in each city.

Example 1:
    Input: costs = [[10,20],[30,200],[400,50],[30,20]]
    Output: 110
    Explanation:
    The first person goes to city a for a cost of 10.
    The second person goes to city a for a cost of 30.
    The third person goes to city b for a cost of 50.
    The fourth person goes to city b for a cost of 20.
    The total minimum cost is 10 + 30 + 50 + 20 = 110 to have half the people
    interviewing in each city.

Example 2:
    Input: costs = [[259,770],[448,54],[926,667],[184,139],[840,118],[577,469]]
    Output: 1859

Example 3:
    Input: costs = [[515,563],[451,713],[537,709],[343,819],[855,779],[457,60],[650,359],[631,42]]
    Output: 3086

Constraints:
- 2 * n == costs.length
- 2 <= costs.length <= 100
- costs.length is even.
- 1 <= aCosti, bCosti <= 1000

Topics: Array, Greedy, Sorting
Pattern: GreedyCore - Sort + Match (Cost Difference)
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionGreedy",
        "method": "twoCitySchedCost",
        "complexity": "O(n log n) time, O(1) space",
        "description": "Sort by cost difference (a - b), send first half to A",
    },
    "greedy": {
        "class": "SolutionGreedy",
        "method": "twoCitySchedCost",
        "complexity": "O(n log n) time, O(1) space",
        "description": "Sort by cost difference (a - b), send first half to A",
    },
}


# ============================================================================
# JUDGE_FUNC - Validate minimum scheduling cost
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate minimum cost result."""
    costs = json.loads(input_data.strip())
    correct = _reference_two_city(costs)

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


def _reference_two_city(costs: List[List[int]]) -> int:
    """O(n log n) reference using cost difference sorting."""
    # Sort by (cost_a - cost_b): people who save more by going to A first
    costs.sort(key=lambda x: x[0] - x[1])
    n = len(costs) // 2
    total = 0
    for i in range(n):
        total += costs[i][0]  # First half goes to A
    for i in range(n, 2 * n):
        total += costs[i][1]  # Second half goes to B
    return total


JUDGE_FUNC = judge


# ============================================================================
# Solution: Greedy Sort by Cost Difference
# Time: O(n log n), Space: O(1) excluding sort
#
# Core Insight:
#   For each person, the "benefit" of sending them to city A vs city B is:
#   benefit_A = cost_B - cost_A (how much we save by choosing A)
#
#   To minimize total cost:
#   1. Sort people by (cost_A - cost_B) in ascending order
#   2. Send first n people to city A (they benefit most from A)
#   3. Send remaining n people to city B
#
# Why This Works:
#   Sorting by (cost_A - cost_B) puts people who prefer A (negative difference)
#   at the front. We send exactly n people to each city, so we send the
#   n strongest A-preferrers to A.
#
# Alternative View:
#   Imagine everyone goes to B first (total = sum of all cost_B).
#   Moving someone from B to A costs: cost_A - cost_B (the "refund" or "penalty").
#   We want to move n people with the smallest penalties (most negative).
#
# Pattern Reference: GreedyCore - Sort + Match (Cost Difference)
# ============================================================================
class SolutionGreedy:
    def twoCitySchedCost(self, costs: List[List[int]]) -> int:
        # Sort by (cost_A - cost_B): smaller = more benefit from choosing A
        sorted_costs = sorted(costs, key=lambda x: x[0] - x[1])

        n = len(costs) // 2
        total_cost = 0

        # First n people go to city A
        for i in range(n):
            total_cost += sorted_costs[i][0]

        # Remaining n people go to city B
        for i in range(n, 2 * n):
            total_cost += sorted_costs[i][1]

        return total_cost


def solve():
    """
    Input format (JSON per line):
        Line 1: costs as JSON array of [aCost, bCost] pairs

    Output format:
        Integer (minimum total cost)
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    costs = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.twoCitySchedCost(costs)

    print(result)


if __name__ == "__main__":
    solve()

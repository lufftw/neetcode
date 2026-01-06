"""
Problem: Gas Station
Link: https://leetcode.com/problems/gas-station/

There are n gas stations along a circular route, where the amount of gas
at the ith station is gas[i].

You have a car with an unlimited gas tank and it costs cost[i] of gas to
travel from the ith station to its next (i + 1)th station. You begin the
journey with an empty tank at one of the gas stations.

Given two integer arrays gas and cost, return the starting gas station's
index if you can travel around the circuit once in the clockwise direction,
otherwise return -1. If there exists a solution, it is guaranteed to be unique.

Example 1:
    Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
    Output: 3
    Explanation:
    Start at station 3 (index 3) and fill up with 4 unit of gas. Your tank = 0 + 4 = 4
    Travel to station 4. Your tank = 4 - 1 + 5 = 8
    Travel to station 0. Your tank = 8 - 2 + 1 = 7
    Travel to station 1. Your tank = 7 - 3 + 2 = 6
    Travel to station 2. Your tank = 6 - 4 + 3 = 5
    Travel to station 3. The cost is 5. Your gas is just enough to travel back to station 3.
    Therefore, return 3 as the starting index.

Example 2:
    Input: gas = [2,3,4], cost = [3,4,3]
    Output: -1
    Explanation:
    You can't start at station 0 or 1, as there is not enough gas to travel to the next station.
    Let's start at station 2 and fill up with 4 unit of gas. Your tank = 0 + 4 = 4
    Travel to station 0. Your tank = 4 - 3 + 2 = 3
    Travel to station 1. Your tank = 3 - 3 + 3 = 3
    You cannot travel back to station 2, as it requires 4 unit of gas but you only have 3.
    Therefore, you can't travel around the circuit once no matter where you start.

Constraints:
- n == gas.length == cost.length
- 1 <= n <= 10^5
- 0 <= gas[i], cost[i] <= 10^4

Topics: Array, Greedy
Pattern: GreedyCore - Prefix Minimum / Reset Kernel
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionGreedy",
        "method": "canCompleteCircuit",
        "complexity": "O(n) time, O(1) space",
        "description": "Single pass with deficit tracking and candidate reset",
    },
    "greedy": {
        "class": "SolutionGreedy",
        "method": "canCompleteCircuit",
        "complexity": "O(n) time, O(1) space",
        "description": "Single pass with deficit tracking and candidate reset",
    },
}


# ============================================================================
# JUDGE_FUNC - Validate gas station result
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate starting station index."""
    lines = input_data.strip().split("\n")
    gas = json.loads(lines[0])
    cost = json.loads(lines[1])
    correct = _reference_gas_station(gas, cost)

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


def _reference_gas_station(gas: List[int], cost: List[int]) -> int:
    """O(n) reference using greedy with reset."""
    total_tank = 0
    current_tank = 0
    start_station = 0

    for i in range(len(gas)):
        net_gain = gas[i] - cost[i]
        total_tank += net_gain
        current_tank += net_gain

        if current_tank < 0:
            start_station = i + 1
            current_tank = 0

    return start_station if total_tank >= 0 else -1


JUDGE_FUNC = judge


# ============================================================================
# Solution: Greedy with Prefix Deficit and Reset
# Time: O(n), Space: O(1)
#
# Core Insight (Prefix Minimum / Reset Kernel):
#   1. If total gas >= total cost, a solution exists (pigeonhole principle)
#   2. If we run out of gas at station j starting from station i,
#      we can't complete the circuit starting from any station between i and j.
#      Why? Those intermediate stations would have even less accumulated gas.
#   3. So when we fail, reset and try station j+1 as new candidate.
#
# Key Variables:
#   - total_tank: tracks overall feasibility
#   - current_tank: tracks current attempt's balance
#   - start_station: candidate starting position
#
# Pattern Reference: GreedyCore - Prefix Minimum / Reset
# ============================================================================
class SolutionGreedy:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total_tank = 0  # Total gas balance for feasibility check
        current_tank = 0  # Current attempt's gas balance
        candidate_start = 0  # Current candidate starting station

        for station in range(len(gas)):
            net_gain = gas[station] - cost[station]
            total_tank += net_gain
            current_tank += net_gain

            # If we can't reach next station, reset candidate
            if current_tank < 0:
                # All stations from candidate_start to station are invalid
                # Try next station as new candidate
                candidate_start = station + 1
                current_tank = 0

        # If total gas >= total cost, candidate_start is the answer
        return candidate_start if total_tank >= 0 else -1


def solve():
    """
    Input format (JSON per line):
        Line 1: gas as JSON array
        Line 2: cost as JSON array

    Output format:
        Integer (starting station index, or -1 if impossible)
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    gas = json.loads(lines[0])
    cost = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.canCompleteCircuit(gas, cost)

    print(result)


if __name__ == "__main__":
    solve()

# solutions/1011_capacity_to_ship_packages_within_d_days.py
"""
Problem: Capacity To Ship Packages Within D Days
Link: https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/

A conveyor belt has packages that must be shipped from one port to another
within days days.

The ith package on the conveyor belt has a weight of weights[i]. Each day,
we load the ship with packages on the conveyor belt (in the order given by
weights). We may not load more weight than the maximum weight capacity of
the ship.

Return the least weight capacity of the ship that will result in all the
packages on the conveyor belt being shipped within days days.

Example 1:
    Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
    Output: 15
    Explanation: A ship capacity of 15 is the minimum to ship all the packages
    in 5 days like this:
    1st day: 1, 2, 3, 4, 5
    2nd day: 6, 7
    3rd day: 8
    4th day: 9
    5th day: 10

Example 2:
    Input: weights = [3,2,2,4,1,4], days = 3
    Output: 6

Example 3:
    Input: weights = [1,2,3,1,1], days = 4
    Output: 3

Constraints:
- 1 <= days <= weights.length <= 5 * 10^4
- 1 <= weights[i] <= 500

Topics: Array, Binary Search
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate minimum ship capacity result.

    For this problem, there's only one correct answer.
    """
    import json
    lines = input_data.strip().split('\n')
    weights = json.loads(lines[0])
    days = int(lines[1])

    # actual should be positive integer
    if not isinstance(actual, int) or actual < 1:
        return False

    # actual must be at least max(weights)
    if actual < max(weights):
        return False

    # Calculate days needed at this capacity
    def days_needed(capacity):
        day_count = 1
        current_load = 0
        for weight in weights:
            if current_load + weight > capacity:
                day_count += 1
                current_load = weight
            else:
                current_load += weight
        return day_count

    # Verify actual capacity can ship in <= days
    if days_needed(actual) > days:
        return False

    # Verify actual - 1 cannot ship in <= days (actual is minimum)
    if actual > max(weights) and days_needed(actual - 1) <= days:
        return False

    return True


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "shipWithinDays",
        "complexity": "O(n log S) time, O(1) space, where S = sum(weights)",
        "description": "Binary search on answer space (minimum feasible capacity)",
    },
}


# ============================================
# Solution 1: Binary Search on Answer Space
# Time: O(n log S) where S = sum(weights), Space: O(1)
#   - Answer space: [max(weights), sum(weights)]
#   - Minimum capacity must fit largest single package
#   - Maximum capacity ships everything in one day
#   - Greedy feasibility check: fill each day up to capacity
# ============================================
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        """
        Find minimum ship capacity to ship all packages within given days.

        Key Insight:
        - This is a classic "minimize the maximum" problem
        - Answer space: [max(weights), sum(weights)]
        - Minimum capacity = max(weights) (must fit largest single package)
        - Maximum capacity = sum(weights) (ship everything in one day)
        - If capacity C works, C+1 also works (monotonic)

        Algorithm:
        1. Define answer space: [max(weights), sum(weights)]
        2. Binary search for first capacity where can_ship is True
        3. can_ship greedily checks if days_needed <= days

        Feasibility Check (Greedy):
        - Load packages day by day in order
        - Start a new day when adding next package exceeds capacity
        - Count total days needed
        - Return days_needed <= allowed_days

        Greedy Correctness:
        - Packages must be shipped in order (no reordering)
        - Fitting as many packages as possible per day is optimal
        - If we can do it in fewer days, we can certainly do it in more

        Time Complexity: O(n log S) where S = sum(weights)
            - O(log S) binary search iterations
            - O(n) feasibility check per iteration
        Space Complexity: O(1) - only counters

        Args:
            weights: Array of package weights (in order)
            days: Number of days to ship all packages

        Returns:
            Minimum ship capacity
        """
        def days_needed(capacity: int) -> int:
            """
            Calculate days needed to ship all packages at given capacity.

            Greedy algorithm:
            - Load packages into current day until next would exceed capacity
            - When exceeded, start a new day
            """
            day_count = 1
            current_load = 0

            for weight in weights:
                if current_load + weight > capacity:
                    # Start a new day
                    day_count += 1
                    current_load = weight
                else:
                    # Add to current day
                    current_load += weight

            return day_count

        def can_ship(capacity: int) -> bool:
            """Check if all packages can be shipped within allowed days."""
            return days_needed(capacity) <= days

        # Answer space: [max(weights), sum(weights)]
        # Must be able to fit the largest single package
        lo = max(weights)
        # At capacity = sum(weights), ship everything in one day
        hi = sum(weights)

        # Binary search for minimum feasible capacity
        while lo < hi:
            mid = lo + (hi - lo) // 2

            if can_ship(mid):
                # This capacity works, but maybe smaller also works
                hi = mid
            else:
                # Need more capacity
                lo = mid + 1

        return lo


# ============================================
# Entry point
# ============================================
def solve():
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    weights = json.loads(lines[0])
    days = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.shipWithinDays(weights, days)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

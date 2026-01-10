"""
Problem: Merge Triplets to Form Target Triplet
Link: https://leetcode.com/problems/merge-triplets-to-form-target-triplet/

A triplet is an array of three integers. You are given a 2D integer array
triplets, where triplets[i] = [a_i, b_i, c_i] describes the i^th triplet.
You are also given an integer array target = [x, y, z] that describes the
triplet you want to obtain.

To obtain target, you may apply the following operation on triplets any
number of times (possibly zero):
- Choose two indices i and j (i != j) and update triplets[j] to become
  [max(a_i, a_j), max(b_i, b_j), max(c_i, c_j)].

Return true if it is possible to obtain the target triplet [x, y, z] as
an element of triplets, or false otherwise.

Example 1:
    Input: triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]
    Output: true

Example 2:
    Input: triplets = [[3,4,5],[4,5,6]], target = [3,2,5]
    Output: false

Example 3:
    Input: triplets = [[2,5,3],[2,3,4],[1,2,5],[5,2,3]], target = [5,5,5]
    Output: true

Constraints:
- 1 <= triplets.length <= 10^5
- triplets[i].length == target.length == 3
- 1 <= a_i, b_i, c_i, x, y, z <= 1000

Topics: Array, Greedy
"""

import json
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionGreedy",
        "method": "mergeTriplets",
        "complexity": "O(n) time, O(1) space",
        "description": "Filter valid triplets, track which target positions can be matched",
    },
    "set": {
        "class": "SolutionSet",
        "method": "mergeTriplets",
        "complexity": "O(n) time, O(1) space",
        "description": "Use set to track matched positions",
    },
}


# ============================================================================
# Solution 1: Greedy Filtering
# Time: O(n), Space: O(1)
#
# Key Insight:
#   A triplet is "usable" only if ALL its values are <= the corresponding
#   target values. If any value exceeds the target, using that triplet
#   would make it impossible to reach the target (max can only increase).
#
#   Among usable triplets, we just need to check if we can collectively
#   reach each target value. We track whether we've seen:
#   - A usable triplet with first value == target[0]
#   - A usable triplet with second value == target[1]
#   - A usable triplet with third value == target[2]
#
#   If all three are satisfied, we can merge those triplets to get target.
#
# Why This Works:
#   - max() operation is monotonic: values can only increase or stay same
#   - If triplet[i] > target[i] for any position, using it "pollutes" that position
#   - We only need to find triplets that can contribute each exact target value
#   - Since max(a, b) <= max(a, c) when b <= c, we can combine valid triplets freely
# ============================================================================
class SolutionGreedy:
    """
    Greedy approach: filter valid triplets and check coverage.

    A triplet is valid if it doesn't exceed target in any position.
    Valid triplets can be freely merged without overshooting the target.
    We just need to verify that some valid triplet can contribute each
    required target value.
    """

    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        x, y, z = target

        # Track whether we can achieve each target value
        can_reach_x = False
        can_reach_y = False
        can_reach_z = False

        for a, b, c in triplets:
            # Skip triplets that exceed target in any position
            # Using such a triplet would make it impossible to reach target
            if a > x or b > y or c > z:
                continue

            # This triplet is "usable" - check what target values it can contribute
            if a == x:
                can_reach_x = True
            if b == y:
                can_reach_y = True
            if c == z:
                can_reach_z = True

        # Can form target if all positions are covered
        return can_reach_x and can_reach_y and can_reach_z


# ============================================================================
# Solution 2: Set-based Tracking
# Time: O(n), Space: O(1)
#
# Same logic as Solution 1, but uses a set to track matched positions.
# This is slightly more elegant and generalizes to k-tuples.
# ============================================================================
class SolutionSet:
    """
    Set-based approach for tracking matched positions.

    Instead of three boolean flags, we collect which positions (0, 1, 2)
    have been matched by at least one valid triplet. If all three positions
    are in the set, we can form the target.
    """

    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        matched = set()

        for triplet in triplets:
            # Skip if any value exceeds target (would overshoot)
            if any(triplet[i] > target[i] for i in range(3)):
                continue

            # Record which positions this triplet can contribute
            for i in range(3):
                if triplet[i] == target[i]:
                    matched.add(i)

        # Need all three positions to be covered
        return len(matched) == 3


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: triplets as JSON 2D array
        Line 2: target as JSON array

    Example:
        [[2,5,3],[1,8,4],[1,7,5]]
        [2,7,5]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    triplets = json.loads(lines[0])
    target = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.mergeTriplets(triplets, target)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

# solutions/0875_koko_eating_bananas.py
"""
Problem: Koko Eating Bananas
Link: https://leetcode.com/problems/koko-eating-bananas/

Koko loves to eat bananas. There are n piles of bananas, the ith pile has
piles[i] bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses
some pile of bananas and eats k bananas from that pile. If the pile has less
than k bananas, she eats all of them instead and will not eat any more bananas
during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas
before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.

Example 1:
    Input: piles = [3,6,7,11], h = 8
    Output: 4

Example 2:
    Input: piles = [30,11,23,4,20], h = 5
    Output: 30

Example 3:
    Input: piles = [30,11,23,4,20], h = 6
    Output: 23

Constraints:
- 1 <= piles.length <= 10^4
- piles.length <= h <= 10^9
- 1 <= piles[i] <= 10^9

Topics: Array, Binary Search
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate minimum eating speed result.

    For this problem, there's only one correct answer.
    """
    import json
    lines = input_data.strip().split('\n')
    piles = json.loads(lines[0])
    h = int(lines[1])

    # actual should be positive integer
    if not isinstance(actual, int) or actual < 1:
        return False

    # Calculate hours needed at this speed
    def hours_needed(speed):
        return sum((pile + speed - 1) // speed for pile in piles)

    # Verify actual speed can finish in h hours
    if hours_needed(actual) > h:
        return False

    # Verify actual - 1 cannot finish in h hours (actual is minimum)
    if actual > 1 and hours_needed(actual - 1) <= h:
        return False

    return True


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minEatingSpeed",
        "complexity": "O(n log m) time, O(1) space, where m = max(piles)",
        "description": "Binary search on answer space (minimum feasible speed)",
    },
}


# ============================================
# Solution 1: Binary Search on Answer Space
# Time: O(n log m) where m = max(piles), Space: O(1)
#   - Answer space: [1, max(piles)]
#   - Predicate: can_finish(k) = total_hours(k) <= h
#   - Monotonic: if speed k works, any larger speed also works
#   - Total hours = sum(ceil(pile / k)) for each pile
# ============================================
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """
        Find minimum eating speed to finish all bananas within h hours.

        Key Insight:
        - The answer itself is what we binary search, not an index
        - Answer space is [1, max(piles)]
        - At speed k, we need ceil(pile/k) hours per pile
        - Total hours is monotonically decreasing with speed
        - If speed k works, any larger speed also works

        Algorithm:
        1. Define answer space: [1, max(piles)]
        2. Binary search for first speed where can_finish is True
        3. can_finish checks if total hours needed <= h

        Predicate:
        - can_finish(k) = sum(ceil(pile/k) for pile in piles) <= h
        - This predicate is monotonic: once True, stays True

        Time Complexity: O(n log m) where m = max(piles)
            - O(log m) binary search iterations
            - O(n) feasibility check per iteration
        Space Complexity: O(1) - only counters

        Args:
            piles: Array of banana pile sizes
            h: Available hours

        Returns:
            Minimum eating speed (bananas per hour)
        """
        def hours_needed(speed: int) -> int:
            """
            Calculate total hours needed at given eating speed.

            For each pile, hours = ceil(pile / speed).
            Using ceiling division: (pile + speed - 1) // speed
            """
            total = 0
            for pile in piles:
                total += (pile + speed - 1) // speed
            return total

        def can_finish(speed: int) -> bool:
            """Check if Koko can finish within h hours at this speed."""
            return hours_needed(speed) <= h

        # Answer space: [1, max(piles)]
        # At speed = max(piles), each pile takes exactly 1 hour
        # At speed = 1, would take sum(piles) hours
        lo = 1
        hi = max(piles)

        # Binary search for first feasible speed
        while lo < hi:
            mid = lo + (hi - lo) // 2

            if can_finish(mid):
                # This speed works, but maybe smaller also works
                hi = mid
            else:
                # Too slow, need to eat faster
                lo = mid + 1

        return lo


# ============================================
# Entry point
# ============================================
def solve():
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    piles = json.loads(lines[0])
    h = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.minEatingSpeed(piles, h)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

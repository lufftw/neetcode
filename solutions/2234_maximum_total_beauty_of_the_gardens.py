"""
Problem: Maximum Total Beauty of the Gardens
Link: https://leetcode.com/problems/maximum-total-beauty-of-the-gardens/

Maximize total beauty = (complete gardens) * full + (min flowers in incomplete) * partial.
Can plant at most newFlowers additional flowers.

Constraints:
- 1 <= flowers.length <= 10^5
- 1 <= flowers[i], target <= 10^5
- 1 <= newFlowers <= 10^10
- 1 <= full, partial <= 10^5

Topics: Array, Two Pointers, Binary Search, Greedy, Sorting
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "maximumBeauty",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Sort + enumerate complete gardens + two-pointer for min",
    },
}


# ============================================================================
# Solution: Sort + Enumerate + Two Pointers
# Time: O(n log n), Space: O(n)
# ============================================================================
class Solution:
    # Key insight: Sort gardens. For each split point:
    # - Gardens to the right (larger) become complete
    # - Gardens to the left (smaller) remain incomplete, maximize their minimum
    #
    # Two-pointer approach: as we complete more gardens (move split left),
    # we have fewer flowers but also fewer incomplete gardens to raise.
    #
    # For incomplete gardens [0..i-1], use prefix sum to calculate cost
    # of raising all to some minimum value.

    def maximumBeauty(
        self, flowers: List[int], newFlowers: int, target: int, full: int, partial: int
    ) -> int:
        n = len(flowers)

        # Cap flowers at target (excess doesn't help)
        flowers = [min(f, target) for f in flowers]
        flowers.sort()

        # If all gardens are already complete
        if flowers[0] >= target:
            return n * full

        # Calculate cost to make gardens [i..n-1] complete
        # cost[i] = sum of (target - flowers[j]) for j in [i..n-1]
        cost_to_complete = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            cost_to_complete[i] = cost_to_complete[i + 1] + max(0, target - flowers[i])

        # Prefix sum for incomplete gardens
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + flowers[i]

        def flowers_needed_to_raise_min(count: int, min_val: int) -> int:
            """Cost to raise gardens [0..count-1] to at least min_val."""
            # Each garden needs max(0, min_val - flowers[i])
            # Total = count * min_val - prefix[count]
            return count * min_val - prefix[count]

        result = 0
        remaining = newFlowers
        j = 0  # Pointer for incomplete gardens

        # Enumerate: gardens [i..n-1] will be complete
        for i in range(n, -1, -1):
            # Check if we have enough flowers to complete [i..n-1]
            if cost_to_complete[i] > remaining:
                continue

            # Flowers left after completing [i..n-1]
            extra = remaining - cost_to_complete[i]

            # Number of incomplete gardens: i (indices 0 to i-1)
            if i == 0:
                # All gardens complete
                result = max(result, n * full)
                break

            # Find maximum min value for incomplete gardens [0..i-1]
            # Use two-pointer: j increases as we raise minimum
            # Cap flowers at target-1 for incomplete gardens
            incomplete = [min(f, target - 1) for f in flowers[:i]]

            # Binary search for maximum achievable minimum
            lo, hi = flowers[0], target - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                # Cost to raise all incomplete gardens to mid
                # For gardens already >= mid, no cost
                # Find how many gardens < mid using binary search
                import bisect
                k = bisect.bisect_left(flowers, mid, 0, i)
                # Cost = k * mid - prefix[k]
                need = k * mid - prefix[k]
                if need <= extra:
                    lo = mid
                else:
                    hi = mid - 1

            min_val = lo
            beauty = (n - i) * full + min_val * partial
            result = max(result, beauty)

        return result


# ============================================================================
# JUDGE_FUNC: Verify using reference implementation
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Verify answer using a reference implementation.
    """
    lines = input_data.strip().split('\n')
    flowers = json.loads(lines[0])
    newFlowers = int(lines[1])
    target = int(lines[2])
    full = int(lines[3])
    partial = int(lines[4])

    # Reference implementation (same algorithm, standalone)
    import bisect

    n = len(flowers)
    flowers = [min(f, target) for f in flowers]
    flowers.sort()

    if flowers[0] >= target:
        return actual == n * full

    cost_to_complete = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        cost_to_complete[i] = cost_to_complete[i + 1] + max(0, target - flowers[i])

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + flowers[i]

    correct = 0
    for i in range(n, -1, -1):
        if cost_to_complete[i] > newFlowers:
            continue
        extra = newFlowers - cost_to_complete[i]
        if i == 0:
            correct = max(correct, n * full)
            break
        lo, hi = flowers[0], target - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            k = bisect.bisect_left(flowers, mid, 0, i)
            need = k * mid - prefix[k]
            if need <= extra:
                lo = mid
            else:
                hi = mid - 1
        beauty = (n - i) * full + lo * partial
        correct = max(correct, beauty)

    return actual == correct


JUDGE_FUNC = judge


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: flowers as JSON array
        Line 2: newFlowers (integer)
        Line 3: target (integer)
        Line 4: full (integer)
        Line 5: partial (integer)

    Example:
        [1,3,1,1]
        7
        6
        12
        1
        -> 14
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    flowers = json.loads(lines[0])
    newFlowers = int(lines[1])
    target = int(lines[2])
    full = int(lines[3])
    partial = int(lines[4])

    solver = get_solver(SOLUTIONS)
    result = solver.maximumBeauty(flowers, newFlowers, target, full, partial)

    print(result)


if __name__ == "__main__":
    solve()

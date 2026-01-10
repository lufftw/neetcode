"""
Problem: Minimum Sum of Squared Difference
Link: https://leetcode.com/problems/minimum-sum-of-squared-difference/

Minimize sum of (nums1[i] - nums2[i])^2 using at most k1+k2 operations.
Each operation changes an element by +1 or -1.

Constraints:
- 1 <= n <= 10^5
- 0 <= nums1[i], nums2[i] <= 10^5
- 0 <= k1, k2 <= 10^9

Topics: Array, Math, Sorting, Heap, Binary Search
"""
from typing import List
from _runner import get_solver
import json
from collections import Counter


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minSumSquareDiff",
        "complexity": "O(n log M) time, O(n) space",
        "description": "Binary search target max difference, then compute result",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums1: List[int], nums2: List[int], k1: int, k2: int) -> int:
    """Greedy simulation for small inputs."""
    n = len(nums1)
    k = k1 + k2

    diff = [abs(nums1[i] - nums2[i]) for i in range(n)]

    # Simple greedy: reduce largest difference each time
    import heapq
    heap = [-d for d in diff]  # Max heap via negation
    heapq.heapify(heap)

    for _ in range(min(k, sum(diff))):
        largest = -heapq.heappop(heap)
        if largest == 0:
            break
        heapq.heappush(heap, -(largest - 1))

    return sum(d * d for d in [-x for x in heap])


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    nums1 = json.loads(lines[0])
    nums2 = json.loads(lines[1])
    k1 = json.loads(lines[2])
    k2 = json.loads(lines[3])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(nums1, nums2, k1, k2)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Binary Search + Counting
# Time: O(n log M), Space: O(n) where M = max difference
# ============================================================================
class Solution:
    # Key insight:
    #   - k1 and k2 are interchangeable: total k = k1 + k2
    #   - Compute diff[i] = |nums1[i] - nums2[i]|
    #   - To minimize sum of squares, reduce largest differences first
    #   - Binary search for the target max difference t after using k operations
    #
    # Binary search:
    #   - For target t, cost = sum(diff[i] - t) for all diff[i] > t
    #   - Find smallest t where cost <= k
    #
    # Final answer:
    #   - Differences > t become t (or t-1 if we have leftover k)
    #   - Sum of squares of final differences

    def minSumSquareDiff(self, nums1: List[int], nums2: List[int], k1: int, k2: int) -> int:
        n = len(nums1)
        k = k1 + k2

        # Compute absolute differences
        diff = [abs(nums1[i] - nums2[i]) for i in range(n)]
        total_diff = sum(diff)

        # If we have enough operations to make all differences 0
        if k >= total_diff:
            return 0

        # Count frequency of each difference
        count = Counter(diff)
        max_diff = max(diff)

        # Binary search for target max difference
        # Find smallest t such that cost to reduce all > t to t is <= k
        def cost_to_reduce_to(t):
            """Cost to reduce all differences > t to t."""
            return sum((d - t) * cnt for d, cnt in count.items() if d > t)

        # Binary search
        lo, hi = 0, max_diff
        while lo < hi:
            mid = (lo + hi) // 2
            if cost_to_reduce_to(mid) <= k:
                hi = mid
            else:
                lo = mid + 1

        target = lo

        # Now compute the answer
        # All differences > target become target (initially)
        # We may have leftover operations to reduce some targets to target-1
        cost = cost_to_reduce_to(target)
        leftover = k - cost

        # Count how many elements will be at 'target' level
        # Original at target + those reduced to target
        at_target = count.get(target, 0)
        for d, cnt in count.items():
            if d > target:
                at_target += cnt

        # Use leftover operations to reduce some from target to target-1
        reduce_count = min(leftover, at_target)

        # Calculate sum of squares
        result = 0

        # Elements below target stay the same
        for d, cnt in count.items():
            if d < target:
                result += d * d * cnt

        # Elements at or reduced to target
        at_target_final = at_target - reduce_count
        at_target_minus_1 = reduce_count

        result += target * target * at_target_final
        if target > 0:
            result += (target - 1) * (target - 1) * at_target_minus_1

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums1 (JSON array)
        Line 2: nums2 (JSON array)
        Line 3: k1 (integer)
        Line 4: k2 (integer)

    Example:
        [1,2,3,4]
        [2,10,20,19]
        0
        0
        -> 579
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums1 = json.loads(lines[0])
    nums2 = json.loads(lines[1])
    k1 = json.loads(lines[2])
    k2 = json.loads(lines[3])

    solver = get_solver(SOLUTIONS)
    result = solver.minSumSquareDiff(nums1, nums2, k1, k2)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

"""
Problem: Partition Array Into Two Arrays to Minimize Sum Difference
Link: https://leetcode.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/

Partition 2n integers into two arrays of n elements each.
Minimize the absolute difference of their sums.

Constraints:
- 1 <= n <= 15
- nums.length == 2 * n
- -10^7 <= nums[i] <= 10^7

Topics: Meet in the Middle, Binary Search
"""
from typing import List
from bisect import bisect_left
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minimumDifference",
        "complexity": "O(n * 2^n * log(2^n)) time, O(2^n) space",
        "description": "Meet in the Middle with binary search",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int]) -> int:
    """Reference implementation using Meet in the Middle."""
    n = len(nums) // 2
    total = sum(nums)

    # Split into left and right halves
    left = nums[:n]
    right = nums[n:]

    # Generate all subset sums grouped by size
    def get_sums_by_size(arr):
        m = len(arr)
        sums = [[] for _ in range(m + 1)]
        for mask in range(1 << m):
            s = 0
            cnt = 0
            for i in range(m):
                if mask & (1 << i):
                    s += arr[i]
                    cnt += 1
            sums[cnt].append(s)
        return sums

    left_sums = get_sums_by_size(left)
    right_sums = get_sums_by_size(right)

    # Sort right sums for binary search
    for k in range(n + 1):
        right_sums[k].sort()

    result = float('inf')

    # For partition with k elements from left, we need n-k from right
    for k in range(n + 1):
        for s1 in left_sums[k]:
            # We want s1 + s2 closest to total / 2
            target = (total - 2 * s1) // 2
            r_sums = right_sums[n - k]

            # Binary search for closest value
            idx = bisect_left(r_sums, target)

            # Check idx and idx-1
            for i in [idx - 1, idx]:
                if 0 <= i < len(r_sums):
                    s2 = r_sums[i]
                    diff = abs(total - 2 * (s1 + s2))
                    result = min(result, diff)

    return result


def judge(actual, expected, input_data: str) -> bool:
    import json
    nums = json.loads(input_data.strip())
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(nums)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Meet in the Middle with Binary Search
# Time: O(n * 2^n * log(2^n)), Space: O(2^n)
#   - Generate 2^n subsets for each half
#   - Binary search for optimal complement
# ============================================================================
class Solution:
    # Key insight: Brute force is O(C(2n,n)) which is too slow for n=15
    # Meet in the Middle: Split problem into two smaller subproblems
    #
    # Algorithm:
    #   1. Split array into left (first n) and right (last n) elements
    #   2. For each half, generate all subset sums grouped by subset size
    #   3. For partition taking k elements from left, we need n-k from right
    #   4. Binary search in right[n-k] for sum closest to (total/2 - left_sum)
    #
    # The goal: minimize |sum_left - sum_right| = |2*sum_left - total|

    def minimumDifference(self, nums: List[int]) -> int:
        n = len(nums) // 2
        total = sum(nums)

        left = nums[:n]
        right = nums[n:]

        # Generate all subset sums grouped by count
        def get_sums_by_size(arr):
            m = len(arr)
            sums = [[] for _ in range(m + 1)]
            for mask in range(1 << m):
                s = 0
                cnt = 0
                for i in range(m):
                    if mask & (1 << i):
                        s += arr[i]
                        cnt += 1
                sums[cnt].append(s)
            return sums

        left_sums = get_sums_by_size(left)
        right_sums = get_sums_by_size(right)

        # Sort right sums for binary search
        for k in range(n + 1):
            right_sums[k].sort()

        result = float('inf')

        # Try all ways to pick k elements from left (need n-k from right)
        for k in range(n + 1):
            for s1 in left_sums[k]:
                # Target: s1 + s2 = total / 2, so s2 = total/2 - s1
                target = (total - 2 * s1) // 2
                r_sums = right_sums[n - k]

                # Binary search for closest value
                idx = bisect_left(r_sums, target)

                for i in [idx - 1, idx]:
                    if 0 <= i < len(r_sums):
                        s2 = r_sums[i]
                        diff = abs(total - 2 * (s1 + s2))
                        result = min(result, diff)

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)

    Example:
        [3,9,7,3]
        -> 2
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minimumDifference(nums)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

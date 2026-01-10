"""
Problem: Longest Increasing Subsequence II
Link: https://leetcode.com/problems/longest-increasing-subsequence-ii/

Find longest strictly increasing subsequence where adjacent elements differ by at most k.

Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i], k <= 10^5

Topics: Array, DP, Segment Tree
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "lengthOfLIS",
        "complexity": "O(n log M) time, O(M) space where M = max(nums)",
        "description": "Segment tree for range max query and point update",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums: List[int], k: int) -> int:
    """O(n^2) DP reference implementation."""
    n = len(nums)
    dp = [1] * n  # dp[i] = LIS length ending at index i

    for i in range(1, n):
        for j in range(i):
            # Check strictly increasing and difference <= k
            if nums[j] < nums[i] <= nums[j] + k:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    nums = json.loads(lines[0])
    k = json.loads(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    # For generated tests with small input, use reference
    if len(nums) <= 200:
        return actual == _reference(nums, k)
    # For larger inputs, just verify it's a positive integer
    return isinstance(actual, int) and actual >= 1


JUDGE_FUNC = judge


# ============================================================================
# Solution: Segment Tree
# Time: O(n log M), Space: O(M) where M = max(nums)
# ============================================================================
class Solution:
    # Key insight:
    #   - dp[val] = longest LIS ending with value 'val'
    #   - For each num, find max(dp[num-k], ..., dp[num-1]) and update dp[num]
    #   - Segment tree enables O(log M) range max query and point update
    #
    # Implementation:
    #   - Build segment tree of size max(nums)+1
    #   - For each num in nums:
    #     - Query max in range [max(1, num-k), num-1]
    #     - Update dp[num] = query_result + 1

    def lengthOfLIS(self, nums: List[int], k: int) -> int:
        max_val = max(nums)

        # Segment tree: tree[i] = max value in range for that node
        # Size 4*max_val is sufficient for segment tree
        tree = [0] * (4 * (max_val + 1))

        def query(node, start, end, l, r):
            """Query max in range [l, r]."""
            if r < start or end < l:
                return 0
            if l <= start and end <= r:
                return tree[node]
            mid = (start + end) // 2
            return max(
                query(2 * node, start, mid, l, r),
                query(2 * node + 1, mid + 1, end, l, r)
            )

        def update(node, start, end, idx, val):
            """Update value at index idx."""
            if start == end:
                tree[node] = max(tree[node], val)
                return
            mid = (start + end) // 2
            if idx <= mid:
                update(2 * node, start, mid, idx, val)
            else:
                update(2 * node + 1, mid + 1, end, idx, val)
            tree[node] = max(tree[2 * node], tree[2 * node + 1])

        result = 1
        for num in nums:
            # Query range [num-k, num-1] for best LIS length
            lo = max(1, num - k)
            hi = num - 1

            if lo <= hi:
                best = query(1, 1, max_val, lo, hi)
                length = best + 1
            else:
                length = 1

            result = max(result, length)

            # Update segment tree at position 'num'
            update(1, 1, max_val, num, length)

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums (JSON array)
        Line 2: k (integer)

    Example:
        [4,2,1,4,3,4,5,8,15]
        3
        -> 5
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])
    k = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.lengthOfLIS(nums, k)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

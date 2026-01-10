"""
Problem: Maximum Sum Queries
Link: https://leetcode.com/problems/maximum-sum-queries/

For each query (xi, yi), find max(nums1[j] + nums2[j]) where nums1[j] >= xi and nums2[j] >= yi.

Constraints:
- nums1.length == nums2.length == n
- 1 <= n <= 10^5
- 1 <= nums1[i], nums2[i] <= 10^9
- 1 <= queries.length <= 10^5
- 1 <= xi, yi <= 10^9

Topics: Array, Binary Search, Stack, Segment Tree, Monotonic Stack, Sorting
"""
from typing import List
from _runner import get_solver
import json
from bisect import bisect_left


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "maximumSumQueries",
        "complexity": "O((n + q) log n) time, O(n + q) space",
        "description": "Sort + monotonic stack for 2D range maximum queries",
    },
}


# JUDGE_FUNC for generated tests
def _reference(nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
    """Brute force reference implementation."""
    n = len(nums1)
    result = []
    for x, y in queries:
        max_sum = -1
        for j in range(n):
            if nums1[j] >= x and nums2[j] >= y:
                max_sum = max(max_sum, nums1[j] + nums2[j])
        result.append(max_sum)
    return result


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    nums1 = json.loads(lines[0])
    nums2 = json.loads(lines[1])
    queries = json.loads(lines[2])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(nums1, nums2, queries)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Sorted Queries + Monotonic Stack
# Time: O((n + q) log n), Space: O(n + q)
# ============================================================================
class Solution:
    # Key insight: Process queries in decreasing order of x_i.
    # As we process, add pairs where nums1[j] >= x_i to our structure.
    #
    # For pairs added, we need to answer: max sum where nums2[j] >= y_i.
    # Use a monotonic stack sorted by nums2 in decreasing order.
    #
    # Stack invariant: if nums2 decreases, sum must increase.
    # Otherwise, a pair with higher nums2 and higher sum dominates.
    #
    # Query: binary search for smallest nums2 >= y_i, return its sum.

    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        q = len(queries)

        # Combine and sort pairs by nums1 descending
        pairs = sorted(zip(nums1, nums2), key=lambda x: -x[0])

        # Sort queries by x descending, keeping original indices
        indexed_queries = sorted(enumerate(queries), key=lambda x: -x[1][0])

        # Monotonic stack: (nums2, sum) with decreasing nums2 and increasing sum
        stack = []  # (nums2_val, max_sum)

        result = [-1] * q
        pair_idx = 0

        for query_idx, (x, y) in indexed_queries:
            # Add all pairs where nums1 >= x
            while pair_idx < n and pairs[pair_idx][0] >= x:
                a, b = pairs[pair_idx]
                s = a + b
                pair_idx += 1

                # Maintain monotonic property: pop elements dominated by (b, s)
                # Element is dominated if it has smaller/equal nums2 AND smaller/equal sum
                while stack and stack[-1][0] <= b and stack[-1][1] <= s:
                    stack.pop()

                # Add (b, s) only if not dominated by stack top
                # Stack top dominates if it has higher nums2 AND higher/equal sum
                # After popping, if stack[-1][0] > b, check if (b, s) offers better sum
                if not stack or (stack[-1][0] > b and stack[-1][1] < s):
                    stack.append((b, s))

            # Binary search for smallest nums2 >= y
            # Stack is sorted by nums2 descending
            if stack:
                # Find rightmost position where nums2 >= y
                # Stack: [(b1, s1), (b2, s2), ...] with b1 > b2 > ...
                left, right = 0, len(stack)
                while left < right:
                    mid = (left + right) // 2
                    if stack[mid][0] >= y:
                        left = mid + 1
                    else:
                        right = mid
                if left > 0:
                    result[query_idx] = stack[left - 1][1]

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums1 (JSON array)
        Line 2: nums2 (JSON array)
        Line 3: queries (JSON 2D array)

    Example:
        [4,3,1,2]
        [2,4,9,5]
        [[4,1],[1,3],[2,5]]
        -> [6,10,7]
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums1 = json.loads(lines[0])
    nums2 = json.loads(lines[1])
    queries = json.loads(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.maximumSumQueries(nums1, nums2, queries)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

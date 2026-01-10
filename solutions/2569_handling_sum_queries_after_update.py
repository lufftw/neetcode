"""
Problem: Handling Sum Queries After Update
Link: https://leetcode.com/problems/handling-sum-queries-after-update/

Given nums1 (binary), nums2 (integers), and queries:
- Type 1 [1,l,r]: Toggle nums1[l..r] (0->1, 1->0)
- Type 2 [2,p,0]: Add p * nums1[i] to each nums2[i]
- Type 3 [3,0,0]: Return sum(nums2)

Constraints:
- 1 <= nums1.length, nums2.length <= 10^5
- 1 <= queries.length <= 10^5
- nums1[i] in {0, 1}
- 0 <= nums2[i] <= 10^9
- 0 <= p <= 10^6

Topics: Array, Segment Tree
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "handleQuery",
        "complexity": "O((n + q) log n) time, O(n) space",
        "description": "Segment tree with lazy propagation for range toggles",
    },
}


# ============================================================================
# JUDGE_FUNC: Brute-force simulation to verify result
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Simulate the queries with brute-force and verify result matches.
    For generated tests where we don't have expected output.
    """
    lines = input_data.strip().split('\n')
    nums1 = json.loads(lines[0])
    nums2 = json.loads(lines[1])
    queries = json.loads(lines[2])

    # Brute-force simulation
    sum2 = sum(nums2)
    correct = []

    for q in queries:
        if q[0] == 1:
            # Toggle nums1[l..r]
            for i in range(q[1], q[2] + 1):
                nums1[i] ^= 1
        elif q[0] == 2:
            # Add p * sum(nums1) to sum2
            sum2 += q[1] * sum(nums1)
        else:
            # Record sum(nums2)
            correct.append(sum2)

    return actual == correct


JUDGE_FUNC = judge


# ============================================================================
# Solution: Segment Tree with Lazy Propagation
# Time: O((n + q) log n), Space: O(n)
# ============================================================================
class Solution:
    # Key insight: We only need sum(nums1), not individual elements.
    # - Type 2 adds p * sum(nums1) to sum(nums2)
    # - Type 3 returns current sum(nums2)
    #
    # For nums1, use segment tree tracking count of 1s in each segment.
    # Toggle operation: count = segment_length - count
    # Lazy propagation: track pending toggle (XOR semantics: toggle twice = no change)

    def handleQuery(
        self, nums1: List[int], nums2: List[int], queries: List[List[int]]
    ) -> List[int]:
        n = len(nums1)

        # Segment tree: tree[i] = count of 1s in segment
        # Lazy: lazy[i] = 1 means segment needs toggle
        tree = [0] * (4 * n)
        lazy = [0] * (4 * n)

        def build(node: int, start: int, end: int) -> None:
            """Build segment tree from nums1."""
            if start == end:
                tree[node] = nums1[start]
                return
            mid = (start + end) // 2
            build(2 * node, start, mid)
            build(2 * node + 1, mid + 1, end)
            tree[node] = tree[2 * node] + tree[2 * node + 1]

        def push_down(node: int, start: int, end: int) -> None:
            """Propagate lazy toggle to children."""
            if lazy[node]:
                mid = (start + end) // 2
                # Toggle left child
                tree[2 * node] = (mid - start + 1) - tree[2 * node]
                lazy[2 * node] ^= 1
                # Toggle right child
                tree[2 * node + 1] = (end - mid) - tree[2 * node + 1]
                lazy[2 * node + 1] ^= 1
                # Clear lazy flag
                lazy[node] = 0

        def toggle(node: int, start: int, end: int, l: int, r: int) -> None:
            """Toggle all elements in [l, r]."""
            if r < start or end < l:
                return
            if l <= start and end <= r:
                # Entire segment covered - toggle and mark lazy
                tree[node] = (end - start + 1) - tree[node]
                lazy[node] ^= 1
                return
            push_down(node, start, end)
            mid = (start + end) // 2
            toggle(2 * node, start, mid, l, r)
            toggle(2 * node + 1, mid + 1, end, l, r)
            tree[node] = tree[2 * node] + tree[2 * node + 1]

        def query_sum() -> int:
            """Return total count of 1s in nums1."""
            return tree[1]

        # Build segment tree
        build(1, 0, n - 1)

        # Track sum(nums2) - we never need individual elements
        sum2 = sum(nums2)
        result = []

        for q in queries:
            if q[0] == 1:
                # Type 1: Toggle nums1[l..r]
                toggle(1, 0, n - 1, q[1], q[2])
            elif q[0] == 2:
                # Type 2: sum2 += p * count_of_ones
                sum2 += q[1] * query_sum()
            else:
                # Type 3: Record sum(nums2)
                result.append(sum2)

        return result


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: nums1 as JSON array
        Line 2: nums2 as JSON array
        Line 3: queries as JSON 2D array

    Example:
        [1,0,1]
        [0,0,0]
        [[1,1,1],[2,1,0],[3,0,0]]
        -> [3]
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    nums1 = json.loads(lines[0])
    nums2 = json.loads(lines[1])
    queries = json.loads(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.handleQuery(nums1, nums2, queries)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

"""
Problem: Range Sum Query - Mutable
Link: https://leetcode.com/problems/range-sum-query-mutable/

Given an integer array nums, handle multiple calls to update(index, val)
and sumRange(left, right).

Example 1:
    Input: ["NumArray", "sumRange", "update", "sumRange"]
           [[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
    Output: [null, 9, null, 8]
    Explanation:
        NumArray numArray = new NumArray([1, 3, 5]);
        numArray.sumRange(0, 2); // return 1 + 3 + 5 = 9
        numArray.update(1, 2);   // nums = [1, 2, 5]
        numArray.sumRange(0, 2); // return 1 + 2 + 5 = 8

Constraints:
- 1 <= nums.length <= 3 * 10^4
- -100 <= nums[i] <= 100
- 0 <= index < nums.length
- -100 <= val <= 100
- 0 <= left <= right < nums.length
- At most 3 * 10^4 calls will be made to update and sumRange.

Topics: Array, Design, Binary Indexed Tree, Segment Tree
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "NumArrayBIT",
        "method": "process_operations",
        "complexity": "O(n log n) build, O(log n) ops",
        "description": "Fenwick Tree (Binary Indexed Tree) implementation",
    },
    "bit": {
        "class": "NumArrayBIT",
        "method": "process_operations",
        "complexity": "O(n log n) build, O(log n) ops",
        "description": "Fenwick Tree (Binary Indexed Tree) implementation",
    },
    "segment_tree": {
        "class": "NumArraySegmentTree",
        "method": "process_operations",
        "complexity": "O(n) build, O(log n) ops",
        "description": "Segment Tree implementation",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result by simulating operations.

    Args:
        actual: Program output (list of results)
        expected: Expected output (None if from generator)
        input_data: Raw input string

    Returns:
        bool: True if results match expected
    """
    lines = input_data.strip().split("\n")
    ops = json.loads(lines[0])
    args = json.loads(lines[1])

    # Compute correct answer using reference solution
    correct = _reference_solution(ops, args)

    # Parse actual output
    if isinstance(actual, list):
        actual_list = actual
    else:
        actual_str = actual.strip()
        try:
            actual_list = json.loads(actual_str) if actual_str else []
        except (ValueError, json.JSONDecodeError):
            return False

    return actual_list == correct


def _reference_solution(ops: List[str], args: List[List]) -> List:
    """Reference implementation using Fenwick Tree."""
    result = []
    obj = None

    for op, arg in zip(ops, args):
        if op == "NumArray":
            nums = arg[0]
            n = len(nums)
            tree = [0] * (n + 1)
            nums_copy = nums[:]

            def lowbit(x):
                return x & (-x)

            def add(i, delta):
                while i <= n:
                    tree[i] += delta
                    i += lowbit(i)

            def prefix_sum(i):
                total = 0
                while i > 0:
                    total += tree[i]
                    i -= lowbit(i)
                return total

            for i, num in enumerate(nums):
                add(i + 1, num)

            obj = {"tree": tree, "nums": nums_copy, "n": n,
                   "add": add, "prefix_sum": prefix_sum, "lowbit": lowbit}
            result.append(None)

        elif op == "update":
            index, val = arg
            delta = val - obj["nums"][index]
            obj["nums"][index] = val
            obj["add"](index + 1, delta)
            result.append(None)

        elif op == "sumRange":
            left, right = arg
            total = obj["prefix_sum"](right + 1) - obj["prefix_sum"](left)
            result.append(total)

    return result


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Fenwick Tree (Binary Indexed Tree)
# Time: O(n log n) build, O(log n) per operation
# Space: O(n)
#
# Key Insight: BIT uses bit manipulation to efficiently compute prefix sums
# and handle point updates. lowbit(i) = i & (-i) gives the rightmost set bit.
# ============================================================================
class NumArrayBIT:
    def __init__(self, nums: List[int]) -> None:
        self.n = len(nums)
        self.nums = nums[:]
        self.tree = [0] * (self.n + 1)  # 1-indexed

        # Build BIT in O(n log n)
        for i, num in enumerate(nums):
            self._add(i + 1, num)

    def _lowbit(self, x: int) -> int:
        """Get rightmost set bit."""
        return x & (-x)

    def _add(self, i: int, delta: int) -> None:
        """Add delta to index i (1-indexed)."""
        while i <= self.n:
            self.tree[i] += delta
            i += self._lowbit(i)

    def _prefix_sum(self, i: int) -> int:
        """Get prefix sum [1..i]."""
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= self._lowbit(i)
        return total

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        self._add(index + 1, delta)

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix_sum(right + 1) - self._prefix_sum(left)

    def process_operations(self, ops: List[str], args: List[List]) -> List:
        """Process sequence of operations."""
        result = []
        for op, arg in zip(ops, args):
            if op == "NumArray":
                self.__init__(arg[0])
                result.append(None)
            elif op == "update":
                self.update(arg[0], arg[1])
                result.append(None)
            elif op == "sumRange":
                result.append(self.sumRange(arg[0], arg[1]))
        return result


# ============================================================================
# Solution 2: Segment Tree
# Time: O(n) build, O(log n) per operation
# Space: O(4n) = O(n)
#
# Key Insight: Each node stores sum of a range. Query/update traverse
# O(log n) nodes from root to leaf.
# ============================================================================
class NumArraySegmentTree:
    def __init__(self, nums: List[int]) -> None:
        self.n = len(nums)
        self.tree = [0] * (4 * self.n) if self.n > 0 else []
        self.nums = nums
        if nums:
            self._build(0, 0, self.n - 1)

    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = self.nums[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self._build(left_child, start, mid)
            self._build(right_child, mid + 1, end)
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def update(self, index: int, val: int) -> None:
        self._update(0, 0, self.n - 1, index, val)

    def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
        if start == end:
            self.tree[node] = val
            self.nums[idx] = val
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            if idx <= mid:
                self._update(left_child, start, mid, idx, val)
            else:
                self._update(right_child, mid + 1, end, idx, val)
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def sumRange(self, left: int, right: int) -> int:
        return self._query(0, 0, self.n - 1, left, right)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or l > end:
            return 0  # Out of range
        if l <= start and end <= r:
            return self.tree[node]  # Fully covered
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        return (self._query(left_child, start, mid, l, r) +
                self._query(right_child, mid + 1, end, l, r))

    def process_operations(self, ops: List[str], args: List[List]) -> List:
        """Process sequence of operations."""
        result = []
        for op, arg in zip(ops, args):
            if op == "NumArray":
                self.__init__(arg[0])
                result.append(None)
            elif op == "update":
                self.update(arg[0], arg[1])
                result.append(None)
            elif op == "sumRange":
                result.append(self.sumRange(arg[0], arg[1]))
        return result


def solve():
    """
    Input format (JSON per line):
        Line 1: operations array (e.g., ["NumArray", "sumRange", "update"])
        Line 2: arguments array (e.g., [[[1,3,5]], [0,2], [1,2]])

    Output format:
        JSON array of results
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    ops = json.loads(lines[0])
    args = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.process_operations(ops, args)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

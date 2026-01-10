# solutions/0703_kth_largest_element_in_a_stream.py
"""
Problem 0703 - Kth Largest Element in a Stream

Design a class to find the kth largest element in a stream.
Note that it is the kth largest element in the sorted order,
not the kth distinct element.

LeetCode Constraints:
- 1 <= k <= 10^4
- 0 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- -10^4 <= val <= 10^4
- At most 10^4 calls to add
- k <= nums.length + number of add calls

Key Insight:
The k-th largest is equivalent to having a min-heap of exactly k elements.
The heap root (minimum in the heap) is the k-th largest overall.
When adding: push new element, pop if size > k. Root = answer.

This transforms "find k-th largest" into "find minimum among top k".

Solution Approaches:
1. Min-heap of size k: O(log k) per add, O(k) space
   - Heap invariant: always contains the k largest seen so far
   - The smallest of these k elements is the k-th largest

2. Sorted list with bisect: O(n) per add due to insertion, O(n) space
   - Simpler logic but worse time complexity
"""
from typing import List, Optional
import heapq
import bisect
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "KthLargestHeap",
        "method": "_run_operations",
        "complexity": "O(n log k) time, O(k) space",
        "description": "Min-heap of size k, root is always k-th largest",
    },
    "bisect": {
        "class": "KthLargestBisect",
        "method": "_run_operations",
        "complexity": "O(n^2) time, O(n) space",
        "description": "Sorted list with binary search insertion",
    },
}


class KthLargestHeap:
    """
    Min-heap approach: maintain exactly k elements.

    The heap property ensures the minimum element is at the root.
    Since we keep only the k largest elements, the root (minimum
    among them) is exactly the k-th largest element overall.

    When adding a new element:
    1. If heap size < k: just push (we need more elements)
    2. If new element > root: push, then pop (new is in top k, old root isn't)
    3. If new element <= root: ignore (not in top k)

    Optimization: heappushpop is more efficient than push+pop when
    we know we'll pop immediately.
    """

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap: List[int] = []

        # Build initial heap with first k elements
        # Then use heappushpop for remaining elements
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        # If heap not full yet, just push
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        elif val > self.heap[0]:
            # New value should be in top k, evict smallest of current k
            heapq.heappushpop(self.heap, val)
        # else: val <= heap root, not in top k, ignore

        return self.heap[0]

    def _run_operations(
        self, operations: List[str], arguments: List[List[int]]
    ) -> List[Optional[int]]:
        """Test harness: execute operation sequence."""
        results: List[Optional[int]] = [None]  # Constructor returns null

        for op, args in zip(operations[1:], arguments[1:]):
            if op == "add":
                results.append(self.add(args[0]))
            else:
                results.append(None)

        return results


class KthLargestBisect:
    """
    Sorted list approach using binary search for insertion point.

    Maintains a sorted list of all elements seen so far.
    The k-th largest is at index (len - k) from the start,
    or equivalently at index (k - 1) from the end.

    Trade-off: simpler logic, but O(n) insertion cost per add
    due to list shifting. Better for understanding, worse for performance.
    """

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.sorted_nums = sorted(nums)

    def add(self, val: int) -> int:
        # Insert maintaining sorted order
        bisect.insort(self.sorted_nums, val)

        # Return k-th largest (k positions from the end)
        return self.sorted_nums[-self.k]

    def _run_operations(
        self, operations: List[str], arguments: List[List[int]]
    ) -> List[Optional[int]]:
        """Test harness: execute operation sequence."""
        results: List[Optional[int]] = [None]  # Constructor returns null

        for op, args in zip(operations[1:], arguments[1:]):
            if op == "add":
                results.append(self.add(args[0]))
            else:
                results.append(None)

        return results


def solve():
    import sys
    import json
    import os

    lines = sys.stdin.read().strip().split("\n")

    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    # Determine which solution class to use
    method_key = os.environ.get("_METHOD", "default")
    solution_info = SOLUTIONS.get(method_key, SOLUTIONS["default"])
    class_name = solution_info["class"]
    solver_class = globals()[class_name]

    # Instantiate with constructor arguments [k, nums]
    k, nums = arguments[0]
    obj = solver_class(k, nums)

    # Run operations
    result = obj._run_operations(operations, arguments)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

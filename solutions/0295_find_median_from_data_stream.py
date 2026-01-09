# solutions/0295_find_median_from_data_stream.py
"""
Problem: Find Median from Data Stream
Link: https://leetcode.com/problems/find-median-from-data-stream/

The median is the middle value in an ordered integer list. If the size of the list
is even, there is no middle value, and the median is the mean of the two middle values.

Implement the MedianFinder class:
- MedianFinder() initializes the MedianFinder object.
- void addNum(int num) adds the integer num from the data stream to the data structure.
- double findMedian() returns the median of all elements so far.

Example 1:
    Input: ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
           [[], [1], [2], [], [3], []]
    Output: [null, null, null, 1.5, null, 2.0]
    Explanation:
        MedianFinder medianFinder = new MedianFinder();
        medianFinder.addNum(1);    // arr = [1]
        medianFinder.addNum(2);    // arr = [1, 2]
        medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
        medianFinder.addNum(3);    // arr[1, 2, 3]
        medianFinder.findMedian(); // return 2.0

Constraints:
- -10^5 <= num <= 10^5
- There will be at least one element in the data structure before calling findMedian.
- At most 5 * 10^4 calls will be made to addNum and findMedian.

Follow up:
- If all integer numbers from the stream are in the range [0, 100], how would you optimize?
- If 99% of all integer numbers from the stream are in the range [0, 100], how would you optimize?

Topics: Two Pointers, Design, Sorting, Heap Priority Queue, Data Stream
"""

import json
from typing import List
import heapq

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "MedianFinder",
        "method": "findMedian",
        "complexity": "O(log n) add, O(1) find",
        "description": "Two heaps: max-heap for lower half, min-heap for upper half",
    },
    "sorted_list": {
        "class": "MedianFinderSortedList",
        "method": "findMedian",
        "complexity": "O(n) add, O(1) find",
        "description": "Maintain sorted list with bisect.insort",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate MedianFinder operations.

    Input format:
        Line 1: JSON array of operations ["MedianFinder", "addNum", ...]
        Line 2: JSON array of arguments [[], [1], [2], ...]

    Output: JSON array of results [null, null, null, 1.5, ...]
    """
    lines = input_data.strip().split("\n")
    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    # Execute operations and collect expected results
    correct = _reference_execute(operations, arguments)

    # Parse actual output
    if isinstance(actual, list):
        actual_list = actual
    else:
        actual_str = actual.strip()
        try:
            actual_list = json.loads(actual_str) if actual_str else []
        except (ValueError, json.JSONDecodeError):
            return False

    # Compare with tolerance for floating point
    if len(actual_list) != len(correct):
        return False

    for a, c in zip(actual_list, correct):
        if a is None and c is None:
            continue
        if a is None or c is None:
            return False
        if isinstance(c, float):
            if abs(a - c) > 1e-5:
                return False
        elif a != c:
            return False

    return True


def _reference_execute(operations: List[str], arguments: List[List]) -> List:
    """Execute operations and return results."""
    results = []
    finder = None

    for op, args in zip(operations, arguments):
        if op == "MedianFinder":
            finder = MedianFinder()
            results.append(None)
        elif op == "addNum":
            finder.addNum(args[0])
            results.append(None)
        elif op == "findMedian":
            results.append(finder.findMedian())

    return results


JUDGE_FUNC = judge


# ============================================================================
# Solution: Two Heaps (Max-Heap for Lower, Min-Heap for Upper)
# Time: O(log n) for addNum, O(1) for findMedian
# Space: O(n)
#
# Pattern: heap_median_stream
# See: docs/patterns/heap/templates.md Section 3 (Streaming Median)
# ============================================================================
class MedianFinder:
    """
    Maintain median of a data stream using two heaps.

    Data Structure Design:
    - lower_half: max-heap storing the smaller half of numbers
    - upper_half: min-heap storing the larger half of numbers

    Invariants:
    1. All elements in lower_half <= all elements in upper_half
    2. Size difference: |lower_half| - |upper_half| <= 1
    3. If odd count, lower_half has one more element

    Why Two Heaps?
    - Median requires the middle element(s)
    - Max-heap for lower half: O(1) access to largest of smaller numbers
    - Min-heap for upper half: O(1) access to smallest of larger numbers
    - Together they give O(1) median access
    """

    def __init__(self):
        # Max-heap for lower half (store negatives for max-heap behavior)
        self.lower_half: list[int] = []  # max-heap via negation
        # Min-heap for upper half
        self.upper_half: list[int] = []  # min-heap

    def addNum(self, num: int) -> None:
        """
        Add number while maintaining heap invariants.

        Strategy:
        1. Always add to lower_half first (max-heap)
        2. Move largest from lower to upper (ensures correct partitioning)
        3. If upper becomes larger, move smallest back to lower

        This guarantees:
        - All numbers in lower <= all numbers in upper
        - Sizes are balanced (lower has equal or one more)
        """
        # Step 1: Add to lower half (max-heap, store negative)
        heapq.heappush(self.lower_half, -num)

        # Step 2: Move largest from lower to upper
        # This ensures lower_half max <= upper_half min
        largest_lower = -heapq.heappop(self.lower_half)
        heapq.heappush(self.upper_half, largest_lower)

        # Step 3: Rebalance if upper has more elements
        if len(self.upper_half) > len(self.lower_half):
            smallest_upper = heapq.heappop(self.upper_half)
            heapq.heappush(self.lower_half, -smallest_upper)

    def findMedian(self) -> float:
        """
        Return median in O(1) time.

        Cases:
        - Odd count: median is the root of lower_half (the extra element)
        - Even count: median is average of both roots
        """
        if len(self.lower_half) > len(self.upper_half):
            # Odd count: lower has one more element
            return float(-self.lower_half[0])
        else:
            # Even count: average of two middle elements
            return (-self.lower_half[0] + self.upper_half[0]) / 2.0


# ============================================================================
# Solution 2: Sorted List with Binary Search Insert
# Time: O(n) for addNum (due to list insertion), O(1) for findMedian
# Space: O(n)
#
# Trade-off vs Two Heaps:
# - Simpler to understand and implement
# - O(n) insert vs O(log n), but O(1) median access for both
# - Better for small streams or when median is called frequently
# ============================================================================
class MedianFinderSortedList:
    """
    Maintain median using a sorted list.

    Uses bisect.insort for O(log n) binary search + O(n) insertion.
    Simple and intuitive but slower for large streams.
    """

    def __init__(self):
        self.sorted_nums: list[int] = []

    def addNum(self, num: int) -> None:
        """Insert number in sorted position. O(n) due to list insertion."""
        import bisect
        bisect.insort(self.sorted_nums, num)

    def findMedian(self) -> float:
        """Return median in O(1) time via direct index access."""
        n = len(self.sorted_nums)
        mid = n // 2
        if n % 2 == 1:
            return float(self.sorted_nums[mid])
        else:
            return (self.sorted_nums[mid - 1] + self.sorted_nums[mid]) / 2.0


def solve():
    """
    Input format (JSON per line):
        Line 1: JSON array of operations
        Line 2: JSON array of arguments

    Output format:
        JSON array of results
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    results = []
    finder = None

    for op, args in zip(operations, arguments):
        if op == "MedianFinder":
            finder = MedianFinder()
            results.append(None)
        elif op == "addNum":
            finder.addNum(args[0])
            results.append(None)
        elif op == "findMedian":
            results.append(finder.findMedian())

    print(json.dumps(results))


if __name__ == "__main__":
    solve()

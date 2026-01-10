"""
Problem: Minimum Interval to Include Each Query
Link: https://leetcode.com/problems/minimum-interval-to-include-each-query/

You are given a 2D integer array intervals, where intervals[i] = [left_i, right_i]
describes the i^th interval starting at left_i and ending at right_i (inclusive).
The size of an interval is defined as the number of integers it contains, or more
formally right_i - left_i + 1.

You are also given an integer array queries. The answer to the j^th query is the
size of the smallest interval i such that left_i <= queries[j] <= right_i.
If no such interval exists, the answer is -1.

Return an array containing the answers to the queries.

Example 1:
    Input: intervals = [[1,4],[2,4],[3,6],[4,4]], queries = [2,3,4,5]
    Output: [3,3,1,4]

Example 2:
    Input: intervals = [[2,3],[2,5],[1,8],[20,25]], queries = [2,19,5,22]
    Output: [2,-1,4,6]

Constraints:
- 1 <= intervals.length <= 10^5
- 1 <= queries.length <= 10^5
- intervals[i].length == 2
- 1 <= left_i <= right_i <= 10^7
- 1 <= queries[j] <= 10^7

Topics: Array, Binary Search, Line Sweep, Sorting, Heap Priority Queue
"""

import json
import heapq
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionSortAndHeap",
        "method": "minInterval",
        "complexity": "O((n + q) log n) time, O(n + q) space",
        "description": "Sort intervals by start, process queries in sorted order with min-heap",
    },
    "offline": {
        "class": "SolutionOfflineQuery",
        "method": "minInterval",
        "complexity": "O((n + q) log n) time, O(n + q) space",
        "description": "Offline query processing with sorted intervals and lazy heap removal",
    },
}


# ============================================================================
# Solution 1: Sort + Min-Heap (Offline Query Processing)
# Time: O((n + q) log n), Space: O(n + q)
#
# Key Insight:
#   Process queries in sorted order. For each query point, we want the smallest
#   interval that contains it. By sorting both intervals (by left endpoint) and
#   queries, we can efficiently:
#   1. Add all intervals whose left endpoint <= query point
#   2. Remove intervals whose right endpoint < query point (no longer valid)
#   3. The smallest valid interval is at the top of a min-heap keyed by size
#
# Algorithm:
#   - Sort intervals by left endpoint
#   - Sort queries but remember original indices for result placement
#   - Use min-heap ordered by interval size (right - left + 1)
#   - For each query in sorted order:
#       a) Push all intervals with left <= query onto heap
#       b) Pop intervals from heap where right < query (expired)
#       c) If heap non-empty, top has the answer; else -1
# ============================================================================
class SolutionSortAndHeap:
    """
    Offline query processing using sorting and a min-heap.

    The key observation is that if we process queries from left to right,
    we can incrementally add intervals as they become relevant (left <= query)
    and remove them when they expire (right < query).

    A min-heap keyed by interval size gives us O(log n) access to the
    smallest containing interval at any point.
    """

    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        # Sort intervals by left endpoint
        intervals_sorted = sorted(intervals, key=lambda x: x[0])

        # Pair queries with original indices, then sort by query value
        queries_with_idx = sorted(enumerate(queries), key=lambda x: x[1])

        result = [-1] * len(queries)

        # Min-heap: (interval_size, right_endpoint)
        # We track right_endpoint to know when to remove expired intervals
        heap = []
        interval_idx = 0
        n = len(intervals_sorted)

        for orig_idx, query in queries_with_idx:
            # Add all intervals whose left endpoint <= query
            while interval_idx < n and intervals_sorted[interval_idx][0] <= query:
                left, right = intervals_sorted[interval_idx]
                size = right - left + 1
                heapq.heappush(heap, (size, right))
                interval_idx += 1

            # Remove intervals that no longer contain the query point
            # An interval is invalid if its right endpoint < query
            while heap and heap[0][1] < query:
                heapq.heappop(heap)

            # The smallest valid interval is at the top of the heap
            if heap:
                result[orig_idx] = heap[0][0]

        return result


# ============================================================================
# Solution 2: Offline Query with Lazy Removal
# Time: O((n + q) log n), Space: O(n + q)
#
# This is conceptually the same as Solution 1 but emphasizes the "lazy removal"
# pattern: we don't eagerly remove intervals from the heap when they expire.
# Instead, we check validity only when we're about to use the top element.
#
# This pattern is common in competitive programming and interview settings
# where heap operations with removal are needed.
# ============================================================================
class SolutionOfflineQuery:
    """
    Same algorithm as SortAndHeap with explicit lazy deletion semantics.

    Lazy deletion means we leave expired elements in the heap and only
    remove them when they bubble to the top. This is efficient because:
    - We avoid O(n) heap rebuild for mid-heap deletions
    - Invalid elements are filtered out naturally during access
    """

    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        # Sort intervals by start point ascending
        sorted_intervals = sorted(intervals)

        # Create (query_value, original_index) pairs and sort
        indexed_queries = sorted(
            [(q, i) for i, q in enumerate(queries)],
            key=lambda x: x[0]
        )

        answers = [-1] * len(queries)
        min_heap = []  # (size, right_endpoint)
        i = 0  # Pointer into sorted_intervals

        for query_val, query_idx in indexed_queries:
            # Push all intervals that start at or before query_val
            while i < len(sorted_intervals) and sorted_intervals[i][0] <= query_val:
                left, right = sorted_intervals[i]
                interval_size = right - left + 1
                heapq.heappush(min_heap, (interval_size, right))
                i += 1

            # Lazy removal: discard intervals whose right endpoint < query_val
            # These intervals cannot contain the current query point
            while min_heap and min_heap[0][1] < query_val:
                heapq.heappop(min_heap)

            # Record answer if any valid interval exists
            if min_heap:
                answers[query_idx] = min_heap[0][0]

        return answers


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: intervals as JSON 2D array
        Line 2: queries as JSON array

    Example:
        [[1,4],[2,4],[3,6],[4,4]]
        [2,3,4,5]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    intervals = json.loads(lines[0])
    queries = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.minInterval(intervals, queries)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

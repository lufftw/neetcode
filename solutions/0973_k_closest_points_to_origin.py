# solutions/0973_k_closest_points_to_origin.py
"""
Problem 0973 - K Closest Points to Origin

Given an array of points where points[i] = [xi, yi] represents a point
on the X-Y plane and an integer k, return the k closest points to the
origin (0, 0).

The distance between two points is the Euclidean distance:
sqrt((x1-x2)^2 + (y1-y2)^2)

LeetCode Constraints:
- 1 <= k <= points.length <= 10^4
- -10^4 <= xi, yi <= 10^4

Key Insight:
We only need to compare distances, not compute exact values.
Use squared distance (x^2 + y^2) to avoid sqrt computation.

This is a classic "top k" problem with multiple approaches.

Solution Approaches:
1. Max-heap of size k: O(n log k) time, O(k) space
2. Sort all points: O(n log n) time, O(n) space
3. Quickselect: O(n) average, O(n^2) worst case
"""
from typing import List
import heapq
import random
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionHeap",
        "method": "kClosest",
        "complexity": "O(n log k) time, O(k) space",
        "description": "Max-heap of size k for top-k closest points",
    },
    "sort": {
        "class": "SolutionSort",
        "method": "kClosest",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Sort all points by distance, take first k",
    },
    "quickselect": {
        "class": "SolutionQuickselect",
        "method": "kClosest",
        "complexity": "O(n) average time, O(1) space",
        "description": "Quickselect partitioning to find k-th element",
    },
}


class SolutionHeap:
    """
    Max-heap approach for top-k smallest.

    Use a max-heap (negate distances for Python's min-heap) of size k.
    For each point:
    - If heap size < k, push the point
    - If current distance < max in heap, replace max with current

    This keeps the k smallest distances seen so far.

    Time: O(n log k) - each heap operation is O(log k)
    Space: O(k) for the heap
    """

    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # Max-heap: store (-distance, point) so largest distance is popped first
        heap: List[tuple] = []

        for x, y in points:
            dist = x * x + y * y
            if len(heap) < k:
                heapq.heappush(heap, (-dist, [x, y]))
            elif -dist > heap[0][0]:
                heapq.heapreplace(heap, (-dist, [x, y]))

        return [point for _, point in heap]


class SolutionSort:
    """
    Sorting approach.

    Sort all points by their squared distance from origin,
    then return the first k points.

    Simple and readable, but sorts more than necessary
    when k << n.

    Time: O(n log n) for sorting
    Space: O(n) for sorted array (or O(1) if sorting in place)
    """

    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # Sort by squared distance
        points.sort(key=lambda p: p[0] ** 2 + p[1] ** 2)
        return points[:k]


class SolutionQuickselect:
    """
    Quickselect approach for linear average time.

    Partition the array such that elements smaller than pivot
    are on the left, larger on the right. Then recurse on the
    appropriate partition.

    After quickselect, the first k elements are guaranteed to be
    the k closest (though not necessarily sorted).

    Time: O(n) average, O(n^2) worst case
    Space: O(1) excluding recursion stack

    Use random pivot selection to avoid worst case on sorted input.
    """

    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        def dist(p: List[int]) -> int:
            return p[0] ** 2 + p[1] ** 2

        def partition(left: int, right: int) -> int:
            """Partition around random pivot, return pivot index."""
            # Random pivot selection
            pivot_idx = random.randint(left, right)
            points[pivot_idx], points[right] = points[right], points[pivot_idx]

            pivot_dist = dist(points[right])
            store_idx = left

            for i in range(left, right):
                if dist(points[i]) < pivot_dist:
                    points[i], points[store_idx] = points[store_idx], points[i]
                    store_idx += 1

            points[store_idx], points[right] = points[right], points[store_idx]
            return store_idx

        left, right = 0, len(points) - 1

        while left <= right:
            pivot_idx = partition(left, right)

            if pivot_idx == k:
                break
            elif pivot_idx < k:
                left = pivot_idx + 1
            else:
                right = pivot_idx - 1

        return points[:k]


# Custom judge: order doesn't matter, just need the right k points
def judge(actual: List[List[int]], expected: List[List[int]], input_data: str) -> bool:
    """
    Custom judge: verify actual contains correct k closest points.
    Order may differ, so compare as sets of distances.
    """
    if len(actual) != len(expected):
        return False

    def dist(p: List[int]) -> int:
        return p[0] ** 2 + p[1] ** 2

    actual_dists = sorted(dist(p) for p in actual)
    expected_dists = sorted(dist(p) for p in expected)

    return actual_dists == expected_dists


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    points = json.loads(lines[0])
    k = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.kClosest(points, k)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

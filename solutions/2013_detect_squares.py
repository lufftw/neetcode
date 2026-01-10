"""
Problem: Detect Squares
Link: https://leetcode.com/problems/detect-squares/

You are given a stream of points on the X-Y plane. Design an algorithm that:
- Adds new points from the stream into a data structure. Duplicate points are
  allowed and should be treated as different points.
- Given a query point, counts the number of ways to choose three points from
  the data structure such that the three points and the query point form an
  axis-aligned square with positive area.

Implement the DetectSquares class:
- DetectSquares() Initializes the object with an empty data structure.
- void add(int[] point) Adds a new point point = [x, y] to the data structure.
- int count(int[] point) Counts the number of ways to form axis-aligned squares
  with point point = [x, y] as described above.

Example 1:
    Input: ["DetectSquares", "add", "add", "add", "count", "count", "add", "count"]
           [[], [[3, 10]], [[11, 2]], [[3, 2]], [[11, 10]], [[14, 8]], [[11, 2]], [[11, 10]]]
    Output: [null, null, null, null, 1, 0, null, 2]

Constraints:
- point.length == 2
- 0 <= x, y <= 1000
- At most 3000 calls in total will be made to add and count.

Topics: Array, Hash Table, Design, Counting
"""

import json
from collections import defaultdict
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "DetectSquaresHashMap",
        "method": "_run_operations",
        "complexity": "O(n) per count, O(1) per add",
        "description": "Hash map with point counts, iterate diagonal candidates",
    },
    "by_x": {
        "class": "DetectSquaresByX",
        "method": "_run_operations",
        "complexity": "O(n) per count, O(1) per add",
        "description": "Group points by x-coordinate for efficient lookup",
    },
}


# ============================================================================
# Solution 1: Hash Map with Point Counts
# Time: O(1) add, O(n) count where n = number of unique points
# Space: O(n)
#
# Key Insight:
#   Given query point (px, py), we need to find squares where (px, py) is one
#   corner. For an axis-aligned square, if we fix (px, py), the diagonal
#   corner (dx, dy) determines the entire square:
#   - The other two corners are (px, dy) and (dx, py)
#   - For it to be a square: |px - dx| == |py - dy| (side length must match)
#
# Algorithm:
#   1. Store all points with their counts (duplicates matter)
#   2. For count(px, py):
#      - Iterate through all points (dx, dy) where dx != px
#      - If |px - dx| == |py - dy|, this could be a diagonal corner
#      - Check if (px, dy) and (dx, py) exist in our point set
#      - Multiply counts: count[(dx,dy)] * count[(px,dy)] * count[(dx,py)]
#
# Why Diagonal Approach:
#   - Fixing the diagonal uniquely determines the square
#   - We only need to check points with different x (avoids degenerate cases)
#   - Multiplicative counting handles duplicates correctly
# ============================================================================
class DetectSquaresHashMap:
    """
    Hash map-based solution tracking point frequencies.

    We maintain a dictionary mapping (x, y) -> count.
    For queries, we iterate potential diagonal corners and verify
    the other two corners exist.
    """

    def __init__(self):
        # Map from (x, y) -> count of that point
        self.point_count = defaultdict(int)
        # Also keep list for iteration (or we can iterate the dict keys)
        self.points = []

    def add(self, point: List[int]) -> None:
        x, y = point
        self.point_count[(x, y)] += 1
        self.points.append((x, y))

    def count(self, point: List[int]) -> int:
        px, py = point
        total = 0

        # Iterate all stored points as potential diagonal corners
        for dx, dy in self.point_count:
            # Skip if same x-coordinate (would give zero side length horizontally)
            # Skip if not forming a square (|dx-px| must equal |dy-py|)
            if dx == px or abs(dx - px) != abs(dy - py):
                continue

            # Check if the other two corners exist
            # For diagonal (px,py)-(dx,dy), corners are (px,dy) and (dx,py)
            if (px, dy) in self.point_count and (dx, py) in self.point_count:
                # Multiply counts: diagonal corner * two adjacent corners
                total += (
                    self.point_count[(dx, dy)] *
                    self.point_count[(px, dy)] *
                    self.point_count[(dx, py)]
                )

        return total

    def _run_operations(self, operations: List[str], args: List[List]) -> List:
        """Run a sequence of operations for testing."""
        results = []
        for op, arg in zip(operations, args):
            if op == "DetectSquares":
                self.__init__()
                results.append(None)
            elif op == "add":
                self.add(arg[0])
                results.append(None)
            elif op == "count":
                results.append(self.count(arg[0]))
        return results


# ============================================================================
# Solution 2: Group by X-Coordinate
# Time: O(1) add, O(n) count
# Space: O(n)
#
# Optimization:
#   Instead of iterating all points, group by x-coordinate.
#   For count(px, py), we only care about points where |dx - px| == |dy - py|.
#   By grouping points by x, we can iterate points at each relevant x.
#
# This approach is cleaner for understanding the square formation logic.
# ============================================================================
class DetectSquaresByX:
    """
    Solution grouping points by x-coordinate.

    This makes the iteration pattern clearer: for a query point,
    we look at all points sharing the same x (potential vertical edge)
    and then check for the horizontal counterparts.
    """

    def __init__(self):
        self.point_count = defaultdict(int)
        # Group points by x-coordinate: x -> list of y values
        self.points_by_x = defaultdict(list)

    def add(self, point: List[int]) -> None:
        x, y = point
        # Only add to points_by_x if this is the first occurrence
        if self.point_count[(x, y)] == 0:
            self.points_by_x[x].append(y)
        self.point_count[(x, y)] += 1

    def count(self, point: List[int]) -> int:
        px, py = point
        total = 0

        # Look at all points sharing x-coordinate with query (vertical line)
        for y in self.points_by_x[px]:
            if y == py:
                continue  # Need positive area

            side_length = abs(y - py)

            # Two possible squares: one to the left, one to the right
            for dx in [px - side_length, px + side_length]:
                # Check if diagonal corner and adjacent corner exist
                if (dx, y) in self.point_count and (dx, py) in self.point_count:
                    total += (
                        self.point_count[(px, y)] *
                        self.point_count[(dx, y)] *
                        self.point_count[(dx, py)]
                    )

        return total

    def _run_operations(self, operations: List[str], args: List[List]) -> List:
        """Run a sequence of operations for testing."""
        results = []
        for op, arg in zip(operations, args):
            if op == "DetectSquares":
                self.__init__()
                results.append(None)
            elif op == "add":
                self.add(arg[0])
                results.append(None)
            elif op == "count":
                results.append(self.count(arg[0]))
        return results


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: operations as JSON array of strings
        Line 2: arguments as JSON 2D array

    Example:
        ["DetectSquares","add","add","add","count","count","add","count"]
        [[],[[3,10]],[[11,2]],[[3,2]],[[11,10]],[[14,8]],[[11,2]],[[11,10]]]
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    operations = json.loads(lines[0])
    args = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    results = solver._run_operations(operations, args)

    print(json.dumps(results, separators=(',', ':')))


if __name__ == "__main__":
    solve()

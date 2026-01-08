# solutions/0286_walls_and_gates.py
"""
Problem: Walls and Gates
Link: https://leetcode.com/problems/walls-and-gates/

You are given an m x n grid rooms initialized with these three possible values:
- -1: A wall or an obstacle
- 0: A gate
- INF (2^31 - 1): An empty room

Fill each empty room with the distance to its nearest gate. If it is impossible
to reach a gate, it should be filled with INF.

Example 1:
    Input: rooms = [[INF,-1,0,INF],[INF,INF,INF,-1],[INF,-1,INF,-1],[0,-1,INF,INF]]
    Output: [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]

Example 2:
    Input: rooms = [[-1]]
    Output: [[-1]]

Example 3:
    Input: rooms = [[INF]]
    Output: [[INF]]

Constraints:
- m == rooms.length
- n == rooms[i].length
- 1 <= m, n <= 250
- rooms[i][j] is -1, 0, or 2^31 - 1

Topics: Array, Breadth First Search, Matrix
"""
from typing import List
from collections import deque
from _runner import get_solver


INF = 2147483647


# ============================================================================
# JUDGE_FUNC - Required for problems with multiple valid answers
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Walls and Gates solution."""
    import json
    import copy

    # Parse input
    rooms = json.loads(input_data.strip())

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected using reference solution
    rooms_copy = copy.deepcopy(rooms)
    _walls_and_gates_reference(rooms_copy)
    return actual == rooms_copy


def _walls_and_gates_reference(rooms: List[List[int]]) -> None:
    """Reference solution for validation."""
    if not rooms or not rooms[0]:
        return

    rows, cols = len(rooms), len(rooms[0])
    queue = deque()

    # Find all gates
    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0:
                queue.append((r, c))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if rooms[nr][nc] == INF:
                    rooms[nr][nc] = rooms[r][c] + 1
                    queue.append((nr, nc))


JUDGE_FUNC = judge


# ============================================================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "wallsAndGates",
        "complexity": "O(m*n) time, O(m*n) space",
        "description": "Multi-source BFS from all gates",
        "api_kernels": ["GridBFSMultiSource"],
        "patterns": ["grid_bfs_propagation"],
    },
}


# ============================================================================
# Solution: Multi-Source BFS from Gates
# Time: O(m * n), Space: O(m * n)
#
# Pattern: GridBFSMultiSource - Distance Fill
# Insight: Instead of BFS from each room to find nearest gate (O(k*m*n)),
#          BFS from all gates simultaneously (O(m*n)).
#          First time a room is reached guarantees minimum distance.
# ============================================================================
class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Modify rooms in-place: fill each empty room with distance to nearest gate.

        Multi-source BFS approach:
        1. Initialize queue with all gates (distance 0)
        2. Expand BFS level by level
        3. First reach to each room is the minimum distance

        Why this works: BFS guarantees shortest path in unweighted graphs.
        All gates start at distance 0, so BFS naturally computes min distance.
        """
        if not rooms or not rooms[0]:
            return

        rows, cols = len(rooms), len(rooms[0])
        queue = deque()

        # Phase 1: Collect all gates as BFS sources
        # Gates are at distance 0 from themselves
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:
                    queue.append((r, c))

        # Phase 2: BFS expansion from all gates simultaneously
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            r, c = queue.popleft()

            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc

                # Check bounds and if cell is an empty room (INF)
                if 0 <= nr < rows and 0 <= nc < cols:
                    if rooms[nr][nc] == INF:
                        # Distance to this room = distance to current cell + 1
                        rooms[nr][nc] = rooms[r][c] + 1
                        queue.append((nr, nc))

        # No return needed - rooms is modified in place


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array rooms

    Output format:
    2D array with distances filled in
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    rooms = json.loads(lines[0])

    # Get solver and call method
    solver = get_solver(SOLUTIONS)
    solver.wallsAndGates(rooms)

    # Output the modified grid
    print(json.dumps(rooms, separators=(',', ':')))


if __name__ == "__main__":
    solve()

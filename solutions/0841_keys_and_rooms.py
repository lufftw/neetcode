# solutions/0841_keys_and_rooms.py
"""
Problem: Keys and Rooms
Link: https://leetcode.com/problems/keys-and-rooms/

There are n rooms labeled from 0 to n - 1 and all the rooms are locked except for room 0.
Your goal is to visit all the rooms. However, you cannot enter a locked room without having
its key.

When you visit a room, you may find a set of distinct keys in it. Each key has a number on it,
denoting which room it unlocks, and you can take all of them with you to unlock the other rooms.

Given an array rooms where rooms[i] is the set of keys that you can obtain if you visited room i,
return true if you can visit all the rooms, or false otherwise.

Example 1:
    Input: rooms = [[1],[2],[3],[]]
    Output: true
    Explanation:
    We visit room 0 and pick up key 1.
    We then visit room 1 and pick up key 2.
    We then visit room 2 and pick up key 3.
    We then visit room 3.
    Since we were able to visit every room, we return true.

Example 2:
    Input: rooms = [[1,3],[3,0,1],[2],[0]]
    Output: false
    Explanation: We can not enter room number 2 since the only key that unlocks it is in that room.

Constraints:
- n == rooms.length
- 2 <= n <= 1000
- 0 <= rooms[i].length <= 1000
- 1 <= sum(rooms[i].length) <= 3000
- 0 <= rooms[i][j] < n
- All the values of rooms[i] are unique.

Topics: DFS, BFS, Graph
"""
from typing import List, Set
from collections import deque
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Keys and Rooms solution."""
    import json

    # Parse input
    rooms = json.loads(input_data.strip())

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected using reference solution
    expected_result = _can_visit_all(rooms)
    return actual == expected_result


def _can_visit_all(rooms):
    """Reference solution for validation."""
    visited = {0}
    stack = [0]

    while stack:
        room = stack.pop()
        for key in rooms[room]:
            if key not in visited:
                visited.add(key)
                stack.append(key)

    return len(visited) == len(rooms)


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDFS",
        "method": "canVisitAllRooms",
        "complexity": "O(V+E) time, O(V) space",
        "description": "DFS reachability check",
        "api_kernels": ["GraphDFS"],
        "patterns": ["graph_dfs_reachability"],
    },
    "bfs": {
        "class": "SolutionBFS",
        "method": "canVisitAllRooms",
        "complexity": "O(V+E) time, O(V) space",
        "description": "BFS reachability check",
        "api_kernels": ["GraphBFS"],
        "patterns": ["graph_bfs_reachability"],
    },
}


# ============================================
# Solution 1: DFS Reachability
# Time: O(V + E), Space: O(V)
#   - rooms[i] = list of keys in room i
#   - Key to room j = directed edge i → j
#   - Question: Can we reach all nodes from node 0?
# ============================================
class SolutionDFS:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        n = len(rooms)
        visited: Set[int] = set()

        def dfs(room: int) -> None:
            if room in visited:
                return

            visited.add(room)

            # Each key in current room leads to another room
            for key in rooms[room]:
                dfs(key)

        # Start from room 0 (always unlocked)
        dfs(0)

        # Check if all rooms visited
        return len(visited) == n


# ============================================
# Solution 2: BFS Reachability
# Time: O(V + E), Space: O(V)
#   - Iterative traversal
# ============================================
class SolutionBFS:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        n = len(rooms)
        visited: Set[int] = {0}
        queue: deque[int] = deque([0])

        while queue:
            room = queue.popleft()

            for key in rooms[room]:
                if key not in visited:
                    visited.add(key)
                    queue.append(key)

        return len(visited) == n


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array rooms

    Output format:
    Boolean: true/false
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    rooms = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.canVisitAllRooms(rooms)

    print(str(result).lower())  # true/false format


if __name__ == "__main__":
    solve()

## Keys and Rooms (LeetCode 841)

> **Problem**: Determine if all rooms can be visited starting from room 0.
> **Pattern**: DFS/BFS reachability check
> **Key Insight**: Standard graph traversal - can we reach all nodes from source?

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "can visit all" / "reachability" | → Graph traversal from source |
| "keys to unlock" | → Directed edges (key → room) |
| "start from room 0" | → Single-source traversal |

### Implementation

```python
# Pattern: graph_dfs_reachability
# See: docs/patterns/graph/templates.md Section 1

class SolutionDFS:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        """
        Check if all rooms are reachable from room 0 using DFS.

        Key Insight:
        - rooms[i] = list of keys in room i
        - Key to room j = directed edge i → j
        - Question: Can we reach all nodes from node 0?

        This is a standard reachability problem:
        - DFS/BFS from start node
        - Track visited nodes
        - Check if all nodes visited
        """
        n = len(rooms)
        visited: set[int] = set()

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
```

### Trace Example

```
Input: rooms = [[1], [2], [3], []]
Room 0 has key to room 1
Room 1 has key to room 2
Room 2 has key to room 3
Room 3 has no keys

Graph representation:
0 → 1 → 2 → 3

DFS from room 0:
1. Visit 0, get key 1
2. Visit 1, get key 2
3. Visit 2, get key 3
4. Visit 3, no more keys

visited = {0, 1, 2, 3}
len(visited) == 4 == n → True

Input: rooms = [[1,3], [3,0,1], [2], [0]]
0 → 1, 3
1 → 3, 0, 1
2 → 2 (self-loop)
3 → 0

DFS from room 0:
1. Visit 0, get keys 1, 3
2. Visit 1, get keys (3, 0, 1 - all visited or will visit)
3. Visit 3, get key 0 (visited)

visited = {0, 1, 3}
Room 2 never visited!
len(visited) == 3 != 4 → False
```

### BFS Alternative

```python
from collections import deque

class SolutionBFS:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        """BFS approach - iterative traversal."""
        n = len(rooms)
        visited: set[int] = {0}
        queue: deque[int] = deque([0])

        while queue:
            room = queue.popleft()

            for key in rooms[room]:
                if key not in visited:
                    visited.add(key)
                    queue.append(key)

        return len(visited) == n
```

### Iterative DFS with Stack

```python
class SolutionIterativeDFS:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        """Iterative DFS using explicit stack."""
        n = len(rooms)
        visited: set[int] = {0}
        stack: list[int] = [0]

        while stack:
            room = stack.pop()

            for key in rooms[room]:
                if key not in visited:
                    visited.add(key)
                    stack.append(key)

        return len(visited) == n
```

### Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| DFS | O(V + E) | O(V) for visited + recursion |
| BFS | O(V + E) | O(V) for visited + queue |

Where V = number of rooms, E = total number of keys

### Related Problems

| Problem | Connection |
|---------|------------|
| LC 547: Number of Provinces | Count connected components |
| LC 1971: Find if Path Exists | Same reachability pattern |



---

## Quick Reference Templates

### Template 1: DFS Connected Components (Grid)

```python
def count_components(grid: List[List[str]]) -> int:
    """Count connected components in a grid."""
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(row: int, col: int) -> None:
        if (row < 0 or row >= rows or col < 0 or col >= cols or
            grid[row][col] != '1'):
            return
        grid[row][col] = '0'  # Mark visited
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)

    return count
```

### Template 2: BFS Shortest Path (Unweighted)

```python
from collections import deque

def shortest_path(graph: dict[int, list[int]], start: int, end: int) -> int:
    """Find shortest path in unweighted graph. Returns -1 if unreachable."""
    if start == end:
        return 0

    visited = {start}
    queue = deque([(start, 0)])  # (node, distance)

    while queue:
        node, dist = queue.popleft()

        for neighbor in graph[node]:
            if neighbor == end:
                return dist + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return -1
```

### Template 3: Multi-Source BFS

```python
from collections import deque

def multi_source_bfs(grid: List[List[int]], sources: List[tuple[int, int]]) -> int:
    """BFS from multiple sources simultaneously. Returns max distance."""
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    visited = set(sources)
    queue = deque(sources)
    distance = 0

    while queue:
        distance += 1
        for _ in range(len(queue)):  # Process level by level
            row, col = queue.popleft()

            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if (0 <= nr < rows and 0 <= nc < cols and
                    (nr, nc) not in visited and grid[nr][nc] == 1):
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    return distance - 1  # Adjust for initial increment
```

### Template 4: Graph Clone (DFS)

```python
def clone_graph(node: 'Node') -> 'Node':
    """Deep copy a graph using DFS."""
    if not node:
        return None

    old_to_new: dict[Node, Node] = {}

    def dfs(original: 'Node') -> 'Node':
        if original in old_to_new:
            return old_to_new[original]

        clone = Node(original.val)
        old_to_new[original] = clone

        for neighbor in original.neighbors:
            clone.neighbors.append(dfs(neighbor))

        return clone

    return dfs(node)
```

### Template 5: Bipartite Check (BFS)

```python
from collections import deque

def is_bipartite(graph: List[List[int]]) -> bool:
    """Check if graph is bipartite using BFS coloring."""
    n = len(graph)
    color = [-1] * n  # -1 = uncolored

    def bfs(start: int) -> bool:
        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
        return True

    for node in range(n):
        if color[node] == -1:
            if not bfs(node):
                return False

    return True
```

### Template 6: DFS Reachability

```python
def can_reach(graph: dict[int, list[int]], start: int, target: int) -> bool:
    """Check if target is reachable from start."""
    visited = set()

    def dfs(node: int) -> bool:
        if node == target:
            return True
        if node in visited:
            return False

        visited.add(node)

        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True

        return False

    return dfs(start)
```



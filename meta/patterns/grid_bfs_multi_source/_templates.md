## Universal Templates

### Template 1: Propagation Timer (Rotting Oranges Style)

```python
from collections import deque
from typing import List

def propagation_timer(grid: List[List[int]], SOURCE: int, TARGET: int) -> int:
    """
    Count levels until all targets are converted to sources.

    Returns: number of levels (time units), or -1 if impossible
    Use for: LC 994 (Rotting Oranges)
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    queue = deque()
    target_count = 0

    # Initialize: collect sources, count targets
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == SOURCE:
                queue.append((r, c))
            elif grid[r][c] == TARGET:
                target_count += 1

    if target_count == 0:
        return 0

    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    levels = 0

    while queue:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == TARGET:
                        grid[nr][nc] = SOURCE
                        queue.append((nr, nc))
                        target_count -= 1
        levels += 1

    return levels - 1 if target_count == 0 else -1
```

**Use for**: LC 994 (Rotting Oranges), similar "time to spread" problems

---

### Template 2: Distance Fill (Walls and Gates Style)

```python
from collections import deque
from typing import List

def distance_fill(grid: List[List[int]], SOURCE: int, INF: int) -> None:
    """
    Fill each INF cell with distance to nearest SOURCE.
    Modifies grid in-place.

    Use for: LC 286 (Walls and Gates)
    """
    if not grid or not grid[0]:
        return

    rows, cols = len(grid), len(grid[0])
    queue = deque()

    # Initialize: all sources at distance 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == SOURCE:
                queue.append((r, c))

    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == INF:
                    grid[nr][nc] = grid[r][c] + 1
                    queue.append((nr, nc))
```

**Use for**: LC 286 (Walls and Gates), boundary fill problems

---

### Template 3: Distance Matrix (01 Matrix Style)

```python
from collections import deque
from typing import List

def distance_matrix(mat: List[List[int]], SOURCE_VAL: int = 0) -> List[List[int]]:
    """
    Return new matrix where each cell contains distance to nearest source.

    Use for: LC 542 (01 Matrix)
    """
    rows, cols = len(mat), len(mat[0])
    queue = deque()

    # Initialize distance matrix
    dist = [[0 if mat[r][c] == SOURCE_VAL else float('inf')
             for c in range(cols)] for r in range(rows)]

    # Add all sources
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == SOURCE_VAL:
                queue.append((r, c))

    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_dist = dist[r][c] + 1
                if new_dist < dist[nr][nc]:
                    dist[nr][nc] = new_dist
                    queue.append((nr, nc))

    return dist
```

**Use for**: LC 542 (01 Matrix), distance field computations

---

### Template 4: Generic Multi-Source BFS

```python
from collections import deque
from typing import List, Callable

def multi_source_bfs_generic(
    grid: List[List[int]],
    is_source: Callable[[int], bool],
    is_target: Callable[[int], bool],
    mark_visited: Callable[[List[List[int]], int, int, int], None],
    directions: List[tuple] = None
) -> int:
    """
    Generic multi-source BFS with customizable predicates.

    Args:
        is_source: lambda cell_value -> bool
        is_target: lambda cell_value -> bool
        mark_visited: function(grid, r, c, dist) to mark cell as visited

    Returns: max distance reached
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    queue = deque()
    directions = directions or [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialize
    for r in range(rows):
        for c in range(cols):
            if is_source(grid[r][c]):
                queue.append((r, c, 0))

    max_dist = 0

    while queue:
        r, c, dist = queue.popleft()
        max_dist = max(max_dist, dist)

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if is_target(grid[nr][nc]):
                    mark_visited(grid, nr, nc, dist + 1)
                    queue.append((nr, nc, dist + 1))

    return max_dist
```

**Use for**: Custom multi-source BFS scenarios



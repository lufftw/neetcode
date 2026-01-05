# Graph Traversal Patterns: Complete Reference

> **API Kernel**: `GraphDFS`, `GraphBFS`
> **Core Mechanism**: Systematically explore all reachable nodes in a graph using depth-first or breadth-first strategies.

This document presents the **canonical graph traversal templates** covering DFS, BFS, connected components, bipartite checking, and shortest path problems. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Number of Islands (LeetCode 200)](#2-base-template-number-of-islands-leetcode-200)
3. [Clone Graph (LeetCode 133)](#3-clone-graph-leetcode-133)
4. [Pacific Atlantic Water Flow (LeetCode 417)](#4-pacific-atlantic-water-flow-leetcode-417)
5. [Rotting Oranges (LeetCode 994)](#5-rotting-oranges-leetcode-994)
6. [Is Graph Bipartite? (LeetCode 785)](#6-is-graph-bipartite-leetcode-785)
7. [Keys and Rooms (LeetCode 841)](#7-keys-and-rooms-leetcode-841)
8. [Find if Path Exists in Graph (LeetCode 1971)](#8-find-if-path-exists-in-graph-leetcode-1971)
9. [Pattern Comparison Matrix](#9-pattern-comparison-matrix)
10. [Pattern Decision Guide](#10-pattern-decision-guide)
11. [Quick Reference Templates](#11-quick-reference-templates)

---

## 1. Core Concepts

### 1.1 Graph Representation

```python
# Adjacency List (most common for sparse graphs)
graph: dict[int, list[int]] = {
    0: [1, 2],      # Node 0 connects to nodes 1 and 2
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}

# Edge List
edges: list[tuple[int, int]] = [(0, 1), (0, 2), (1, 3), (2, 3)]

# Adjacency Matrix (dense graphs)
matrix: list[list[int]] = [
    [0, 1, 1, 0],   # Node 0's connections
    [1, 0, 0, 1],   # Node 1's connections
    [1, 0, 0, 1],   # Node 2's connections
    [0, 1, 1, 0]    # Node 3's connections
]

# Grid as implicit graph
grid: list[list[int]] = [
    [1, 1, 0],
    [1, 1, 0],
    [0, 0, 1]
]
# Neighbors: (row±1, col±1) for 4-directional, add diagonals for 8-directional
```

### 1.2 DFS vs BFS

| Aspect | DFS | BFS |
|--------|-----|-----|
| **Data Structure** | Stack (or recursion) | Queue |
| **Exploration** | Deep first, backtrack | Level by level |
| **Memory** | O(height) for recursion | O(width) for queue |
| **Use Cases** | Pathfinding, cycles, components | Shortest path, levels |
| **When to Choose** | Existence queries, all paths | Distance/level queries |

### 1.3 Universal DFS Template

```python
def dfs(node: int, graph: dict, visited: set) -> None:
    """
    DFS template using recursion.

    Core invariant:
    - visited set prevents revisiting nodes
    - Process node BEFORE recursing (preorder) or AFTER (postorder)
    """
    if node in visited:
        return

    visited.add(node)

    # Process current node (preorder position)

    for neighbor in graph[node]:
        dfs(neighbor, graph, visited)

    # Process current node (postorder position)
```

### 1.4 Universal BFS Template

```python
from collections import deque

def bfs(start: int, graph: dict) -> None:
    """
    BFS template using queue.

    Core invariant:
    - Nodes at distance d are processed before nodes at distance d+1
    - visited set prevents revisiting and infinite loops
    """
    visited: set[int] = {start}
    queue: deque[int] = deque([start])

    while queue:
        node = queue.popleft()

        # Process current node

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)  # Mark visited BEFORE adding to queue
                queue.append(neighbor)
```

### 1.5 Pattern Variants

| Variant | API Kernel | Use When | Key Insight |
|---------|------------|----------|-------------|
| **Connected Components** | `GraphDFS` | Count/identify separate groups | DFS from each unvisited node |
| **Clone Graph** | `GraphDFS` | Deep copy graph structure | Map old nodes to new nodes |
| **Multi-source BFS** | `GraphBFS` | Propagation from multiple starts | Initialize queue with all sources |
| **Bipartite Check** | `GraphBFS` | Two-coloring problem | Alternate colors at each level |
| **Shortest Path** | `GraphBFS` | Unweighted graph distance | BFS guarantees shortest path |
| **Grid Traversal** | `GridBFSMultiSource` | 2D grid as graph | 4-directional neighbors |

### 1.6 Grid Traversal Helpers

```python
# 4-directional movement
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def get_neighbors(row: int, col: int, rows: int, cols: int) -> list[tuple[int, int]]:
    """Get valid 4-directional neighbors."""
    neighbors = []
    for dr, dc in DIRECTIONS:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

# 8-directional movement (includes diagonals)
DIRECTIONS_8 = [(0, 1), (0, -1), (1, 0), (-1, 0),
                (1, 1), (1, -1), (-1, 1), (-1, -1)]
```

### 1.7 When BFS Guarantees Shortest Path

BFS finds shortest path ONLY when:
1. **Unweighted graph**: All edges have equal weight (or weight = 1)
2. **Non-negative weights**: No negative edges

For weighted graphs, use Dijkstra's algorithm instead.

---

## 2. Base Template: Number of Islands (LeetCode 200)

> **Problem**: Count the number of islands in a 2D binary grid.
> **Invariant**: Each DFS marks all cells of one island as visited.
> **Role**: BASE TEMPLATE for connected components on grid.

### 2.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "count islands/regions" | → Connected components with DFS/BFS |
| "2D grid" | → Grid as implicit graph |
| "connected 4-directionally" | → 4-directional neighbors |

### 2.2 Implementation

```python
# Pattern: graph_dfs_connected_components
# See: docs/patterns/graph/templates.md Section 1 (Base Template)

class SolutionDFS:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Count islands using DFS to mark connected land cells.

        Key Insight:
        - Each unvisited '1' starts a new island
        - DFS from that cell marks all connected '1's as visited
        - Number of DFS calls = number of islands

        Why mark in-place?
        - Change '1' to '0' to mark as visited
        - Avoids separate visited set (saves space)
        - Alternatively, use visited set if grid shouldn't be modified
        """
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        island_count = 0

        def dfs(row: int, col: int) -> None:
            """Flood fill: mark all connected land cells."""
            # Boundary check and water/visited check
            if (row < 0 or row >= rows or
                col < 0 or col >= cols or
                grid[row][col] != '1'):
                return

            # Mark as visited (sink the land)
            grid[row][col] = '0'

            # Explore 4 directions
            dfs(row + 1, col)  # Down
            dfs(row - 1, col)  # Up
            dfs(row, col + 1)  # Right
            dfs(row, col - 1)  # Left

        # Main loop: find and count islands
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '1':
                    island_count += 1
                    dfs(row, col)  # Mark entire island as visited

        return island_count
```

### 2.3 Trace Example

```
Input grid:
  1 1 0 0 0
  1 1 0 0 0
  0 0 1 0 0
  0 0 0 1 1

Step 1: Start at (0,0), DFS marks island 1:
  0 0 0 0 0
  0 0 0 0 0
  0 0 1 0 0
  0 0 0 1 1
  island_count = 1

Step 2: Find (2,2), DFS marks island 2:
  0 0 0 0 0
  0 0 0 0 0
  0 0 0 0 0
  0 0 0 1 1
  island_count = 2

Step 3: Find (3,3), DFS marks island 3:
  0 0 0 0 0
  0 0 0 0 0
  0 0 0 0 0
  0 0 0 0 0
  island_count = 3

Result: 3 islands
```

### 2.4 BFS Alternative

```python
from collections import deque

class SolutionBFS:
    def numIslands(self, grid: List[List[str]]) -> int:
        """BFS approach - iterative, uses explicit queue."""
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        island_count = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def bfs(start_row: int, start_col: int) -> None:
            queue = deque([(start_row, start_col)])
            grid[start_row][start_col] = '0'

            while queue:
                row, col = queue.popleft()
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if (0 <= nr < rows and 0 <= nc < cols and
                        grid[nr][nc] == '1'):
                        grid[nr][nc] = '0'
                        queue.append((nr, nc))

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '1':
                    island_count += 1
                    bfs(row, col)

        return island_count
```

### 2.5 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| DFS | O(m × n) | O(m × n) recursion stack worst case |
| BFS | O(m × n) | O(min(m, n)) queue size |

### 2.6 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 695: Max Area of Island | Track area during DFS |
| LC 463: Island Perimeter | Count boundary edges |
| LC 827: Making A Large Island | Try flipping each 0 |

---

## 3. Clone Graph (LeetCode 133)

> **Problem**: Create a deep copy of a connected undirected graph.
> **Pattern**: DFS/BFS with node mapping
> **Variant**: Clone structure while maintaining references.

### 3.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "deep copy" / "clone" | → Map old to new nodes |
| "maintain structure" | → Copy edges during traversal |
| "connected graph" | → Single component, start from any node |

### 3.2 Implementation

```python
# Pattern: graph_clone
# See: docs/patterns/graph/templates.md Section 2

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors else []

class SolutionDFS:
    def cloneGraph(self, node: 'Node') -> 'Node':
        """
        Clone graph using DFS with hash map for node mapping.

        Key Insight:
        - Map: original node → cloned node
        - On first visit: create clone and add to map
        - On subsequent visits: return existing clone from map
        - This handles cycles: when we see a visited node, we use its clone

        Why hash map?
        - Detect already-cloned nodes (handles cycles)
        - Retrieve clone when building neighbor lists
        """
        if not node:
            return None

        # Map: original node → cloned node
        old_to_new: dict[Node, Node] = {}

        def dfs(original: Node) -> Node:
            # If already cloned, return the clone
            if original in old_to_new:
                return old_to_new[original]

            # Create clone (without neighbors yet)
            clone = Node(original.val)
            old_to_new[original] = clone

            # Clone all neighbors recursively
            for neighbor in original.neighbors:
                clone.neighbors.append(dfs(neighbor))

            return clone

        return dfs(node)
```

### 3.3 Trace Example

```
Original graph:
    1 --- 2
    |     |
    4 --- 3

DFS from node 1:
1. Visit 1: Create clone 1', map[1] = 1'
2. Visit neighbor 2: Create clone 2', map[2] = 2'
3. Visit neighbor 3: Create clone 3', map[3] = 3'
4. Visit neighbor 4: Create clone 4', map[4] = 4'
5. Visit neighbor 1 (from 4): Already in map, return 1'
6. Build neighbor lists using map lookups

Result: New graph with same structure, different nodes
```

### 3.4 BFS Alternative

```python
from collections import deque

class SolutionBFS:
    def cloneGraph(self, node: 'Node') -> 'Node':
        """BFS approach - iterative cloning."""
        if not node:
            return None

        old_to_new: dict[Node, Node] = {node: Node(node.val)}
        queue: deque[Node] = deque([node])

        while queue:
            original = queue.popleft()

            for neighbor in original.neighbors:
                if neighbor not in old_to_new:
                    # Create clone and add to map
                    old_to_new[neighbor] = Node(neighbor.val)
                    queue.append(neighbor)

                # Add cloned neighbor to cloned node's neighbors
                old_to_new[original].neighbors.append(old_to_new[neighbor])

        return old_to_new[node]
```

### 3.5 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| DFS | O(V + E) | O(V) for map + recursion |
| BFS | O(V + E) | O(V) for map + queue |

### 3.6 Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Creating duplicate clones | Infinite loop with cycles | Use hash map |
| Not handling null input | NullPointerException | Check `if not node` |
| Shallow copy of neighbors | Original and clone share references | Clone neighbor list |

---

## 4. Pacific Atlantic Water Flow (LeetCode 417)

> **Problem**: Find cells that can flow to both Pacific and Atlantic oceans.
> **Pattern**: Multi-source BFS/DFS from ocean borders
> **Key Insight**: Reverse the flow direction - find cells reachable FROM ocean.

### 4.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "flow from multiple sources" | → Multi-source BFS |
| "reach both destinations" | → Intersection of two reachability sets |
| "reverse direction" | → Start from destination, not source |

### 4.2 Implementation

```python
# Pattern: graph_bfs_multi_source
# See: docs/patterns/graph/templates.md Section 3

from collections import deque

class SolutionBFS:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        """
        Find cells that can reach both oceans using reverse BFS.

        Key Insight:
        - Forward: Check if water from cell reaches ocean (complex)
        - Reverse: Check if ocean can reach cell going UPHILL (simpler)

        Why reverse direction?
        - Ocean borders are known sources
        - Multi-source BFS finds all reachable cells efficiently
        - Intersection gives cells reaching both oceans
        """
        if not heights or not heights[0]:
            return []

        rows, cols = len(heights), len(heights[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def bfs(sources: list[tuple[int, int]]) -> set[tuple[int, int]]:
            """Multi-source BFS to find all reachable cells."""
            reachable: set[tuple[int, int]] = set(sources)
            queue: deque[tuple[int, int]] = deque(sources)

            while queue:
                row, col = queue.popleft()

                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    # Can flow uphill (from ocean's perspective)
                    if (0 <= nr < rows and 0 <= nc < cols and
                        (nr, nc) not in reachable and
                        heights[nr][nc] >= heights[row][col]):
                        reachable.add((nr, nc))
                        queue.append((nr, nc))

            return reachable

        # Pacific: top row + left column
        pacific_sources = (
            [(0, col) for col in range(cols)] +
            [(row, 0) for row in range(rows)]
        )

        # Atlantic: bottom row + right column
        atlantic_sources = (
            [(rows - 1, col) for col in range(cols)] +
            [(row, cols - 1) for row in range(rows)]
        )

        # Find cells reachable from each ocean
        pacific_reach = bfs(pacific_sources)
        atlantic_reach = bfs(atlantic_sources)

        # Return intersection
        return list(pacific_reach & atlantic_reach)
```

### 4.3 Trace Example

```
Heights:
  1 2 2 3 5   (Pacific top)
  3 2 3 4 4
  2 4 5 3 1
  6 7 1 4 5
  5 1 1 2 4   (Atlantic bottom)
  P         A
  (left)    (right)

Pacific reachable (going uphill from ocean):
  ✓ ✓ ✓ ✓ ✓
  ✓ ✓ ✓ ✓ ✓
  ✓ ✓ ✓ . .
  ✓ ✓ . . .
  ✓ . . . .

Atlantic reachable:
  . . . ✓ ✓
  . . . ✓ ✓
  . ✓ ✓ ✓ ✓
  ✓ ✓ ✓ ✓ ✓
  ✓ ✓ ✓ ✓ ✓

Intersection (both oceans):
  [[0,4], [1,3], [1,4], [2,2], [3,0], [3,1], [4,0]]
```

### 4.4 DFS Alternative

```python
class SolutionDFS:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        """DFS approach - recursive from ocean borders."""
        if not heights:
            return []

        rows, cols = len(heights), len(heights[0])
        pacific: set[tuple[int, int]] = set()
        atlantic: set[tuple[int, int]] = set()

        def dfs(row: int, col: int, reachable: set, prev_height: int) -> None:
            if (row < 0 or row >= rows or col < 0 or col >= cols or
                (row, col) in reachable or heights[row][col] < prev_height):
                return

            reachable.add((row, col))
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(row + dr, col + dc, reachable, heights[row][col])

        # DFS from ocean borders
        for col in range(cols):
            dfs(0, col, pacific, 0)
            dfs(rows - 1, col, atlantic, 0)

        for row in range(rows):
            dfs(row, 0, pacific, 0)
            dfs(row, cols - 1, atlantic, 0)

        return list(pacific & atlantic)
```

### 4.5 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(m × n) - each cell visited at most twice |
| Space | O(m × n) for reachable sets |

---

## 5. Rotting Oranges (LeetCode 994)

> **Problem**: Find minimum time for all oranges to rot (multi-source BFS).
> **Pattern**: Multi-source BFS for simultaneous propagation
> **Key Insight**: All rotten oranges spread simultaneously each minute.

### 5.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "minimum time/minutes" | → BFS level = time |
| "spread simultaneously" | → Multi-source BFS |
| "propagation from multiple sources" | → Initialize queue with all sources |

### 5.2 Implementation

```python
# Pattern: graph_bfs_multi_source
# See: docs/patterns/graph/templates.md Section 4

from collections import deque

class SolutionBFS:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        Find minimum minutes for all oranges to rot using multi-source BFS.

        Key Insight:
        - All rotten oranges spread at the same time (level = minute)
        - BFS naturally processes level by level
        - Initialize queue with ALL rotten oranges (multi-source)
        - Each BFS level = 1 minute of spreading

        Why BFS, not DFS?
        - BFS processes by "wavefront" (distance from sources)
        - Each wavefront = 1 minute
        - Time = number of wavefronts = BFS depth
        """
        if not grid or not grid[0]:
            return -1

        rows, cols = len(grid), len(grid[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Initialize: find all rotten oranges and count fresh
        queue: deque[tuple[int, int]] = deque()
        fresh_count = 0

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 2:
                    queue.append((row, col))
                elif grid[row][col] == 1:
                    fresh_count += 1

        # Edge case: no fresh oranges
        if fresh_count == 0:
            return 0

        minutes = 0

        # Multi-source BFS: process level by level
        while queue:
            minutes += 1
            level_size = len(queue)

            for _ in range(level_size):
                row, col = queue.popleft()

                for dr, dc in directions:
                    nr, nc = row + dr, col + dc

                    # Check bounds and if fresh orange
                    if (0 <= nr < rows and 0 <= nc < cols and
                        grid[nr][nc] == 1):
                        # Rot the orange
                        grid[nr][nc] = 2
                        fresh_count -= 1
                        queue.append((nr, nc))

        # Check if all oranges rotted
        return minutes - 1 if fresh_count == 0 else -1
```

### 5.3 Trace Example

```
Initial grid:
  2 1 1
  1 1 0
  0 1 1

Minute 0: Queue = [(0,0)]
  Fresh count = 6

Minute 1: Process (0,0), rot neighbors
  2 2 1
  2 1 0
  0 1 1
  Queue = [(0,1), (1,0)]
  Fresh = 4

Minute 2: Process (0,1), (1,0)
  2 2 2
  2 2 0
  0 1 1
  Queue = [(0,2), (1,1)]
  Fresh = 2

Minute 3: Process (0,2), (1,1)
  2 2 2
  2 2 0
  0 2 1
  Queue = [(2,1)]
  Fresh = 1

Minute 4: Process (2,1)
  2 2 2
  2 2 0
  0 2 2
  Queue = [(2,2)]
  Fresh = 0

Result: 4 minutes
```

### 5.4 Edge Cases

```python
# Case 1: Fresh orange unreachable
#   2 1 1
#   0 1 1
#   1 0 1   ← (2,0) is isolated
# Return: -1

# Case 2: No fresh oranges
#   2 2 2
#   0 2 0
# Return: 0

# Case 3: All fresh oranges adjacent to rotten
#   2 1
#   1 2
# Return: 1
```

### 5.5 Why -1 at the End?

```python
# After BFS completes:
# - minutes counted from 1 (first spreading)
# - But initial state is minute 0
# - Need to subtract 1 from final count

# Alternative: Start minutes = -1, increment before processing
minutes = -1
while queue:
    minutes += 1
    # process level...
```

### 5.6 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(m × n) - each cell visited once |
| Space | O(m × n) - worst case all oranges in queue |

---

## 6. Is Graph Bipartite? (LeetCode 785)

> **Problem**: Determine if a graph can be 2-colored (bipartite).
> **Pattern**: BFS/DFS with node coloring
> **Key Insight**: Alternate colors at each level; conflict = not bipartite.

### 6.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "two groups" / "bipartite" | → Two-coloring problem |
| "no edges within group" | → Adjacent nodes must differ |
| "can be divided" | → Graph coloring BFS/DFS |

### 6.2 Implementation

```python
# Pattern: graph_bipartite
# See: docs/patterns/graph/templates.md Section 5

from collections import deque

class SolutionBFS:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        """
        Check if graph is bipartite using BFS coloring.

        Key Insight:
        - Bipartite = can assign 2 colors so no adjacent nodes share color
        - BFS processes level by level
        - Alternate colors at each level
        - If we try to color a node that's already colored differently → conflict

        Why BFS?
        - Natural level-by-level processing
        - Each level gets opposite color
        - Easy to detect conflicts
        """
        n = len(graph)
        # -1 = uncolored, 0 = color A, 1 = color B
        color: list[int] = [-1] * n

        def bfs(start: int) -> bool:
            """BFS coloring from start node. Returns False if conflict."""
            queue: deque[int] = deque([start])
            color[start] = 0  # Start with color 0

            while queue:
                node = queue.popleft()

                for neighbor in graph[node]:
                    if color[neighbor] == -1:
                        # Uncolored: assign opposite color
                        color[neighbor] = 1 - color[node]
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:
                        # Same color as current node → conflict
                        return False

            return True

        # Check all components (graph may be disconnected)
        for node in range(n):
            if color[node] == -1:
                if not bfs(node):
                    return False

        return True
```

### 6.3 Trace Example

```
Graph: [[1,3], [0,2], [1,3], [0,2]]
Adjacency:
    0 --- 1
    |     |
    3 --- 2

BFS from node 0:
1. Color 0 with color A (0)
2. Visit neighbors 1, 3: color with B (1)
3. Visit neighbor of 1 (which is 2): color with A (0)
4. Visit neighbor of 3 (which is 2): already colored A ✓
5. Check neighbor of 2 (which is 3): already colored B ✓

Colors: [A, B, A, B] = [0, 1, 0, 1]
No conflicts → Bipartite!

Non-bipartite example:
    0 --- 1
     \   /
      \ /
       2

Coloring attempt:
1. Color 0 with A
2. Color 1, 2 with B
3. Check edge 1-2: both B → CONFLICT!
Not bipartite.
```

### 6.4 DFS Alternative

```python
class SolutionDFS:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        """DFS approach - recursive coloring."""
        n = len(graph)
        color: list[int] = [-1] * n

        def dfs(node: int, c: int) -> bool:
            """Try to color node with color c. Returns False if conflict."""
            if color[node] != -1:
                return color[node] == c  # Check for conflict

            color[node] = c

            for neighbor in graph[node]:
                if not dfs(neighbor, 1 - c):
                    return False

            return True

        for node in range(n):
            if color[node] == -1:
                if not dfs(node, 0):
                    return False

        return True
```

### 6.5 Why Disconnected Graph Check?

```python
# Graph may have multiple components
# Example: graph = [[1], [0], [3], [2]]
#   0 -- 1    2 -- 3
#
# Must check EACH component separately
# Only need to start BFS/DFS from uncolored nodes

for node in range(n):
    if color[node] == -1:  # New component
        if not bfs(node):
            return False
```

### 6.6 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| BFS | O(V + E) | O(V) for color array + queue |
| DFS | O(V + E) | O(V) for color array + recursion |

### 6.7 Related Problems

| Problem | Connection |
|---------|------------|
| LC 886: Possible Bipartition | Same pattern with edge list input |
| LC 207: Course Schedule | Graph cycle detection variant |

---

## 7. Keys and Rooms (LeetCode 841)

> **Problem**: Determine if all rooms can be visited starting from room 0.
> **Pattern**: DFS/BFS reachability check
> **Key Insight**: Standard graph traversal - can we reach all nodes from source?

### 7.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "can visit all" / "reachability" | → Graph traversal from source |
| "keys to unlock" | → Directed edges (key → room) |
| "start from room 0" | → Single-source traversal |

### 7.2 Implementation

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

### 7.3 Trace Example

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

### 7.4 BFS Alternative

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

### 7.5 Iterative DFS with Stack

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

### 7.6 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| DFS | O(V + E) | O(V) for visited + recursion |
| BFS | O(V + E) | O(V) for visited + queue |

Where V = number of rooms, E = total number of keys

### 7.7 Related Problems

| Problem | Connection |
|---------|------------|
| LC 547: Number of Provinces | Count connected components |
| LC 1971: Find if Path Exists | Same reachability pattern |

---

## 8. Find if Path Exists in Graph (LeetCode 1971)

> **Problem**: Determine if a path exists between source and destination.
> **Pattern**: DFS/BFS reachability OR Union-Find
> **Key Insight**: Standard connectivity check - multiple valid approaches.

### 8.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "path exists between" | → Reachability query |
| "undirected graph" | → Bidirectional edges |
| "source to destination" | → Point-to-point connectivity |

### 8.2 Implementation

```python
# Pattern: graph_dfs_reachability
# See: docs/patterns/graph/templates.md Section 1

from collections import defaultdict

class SolutionDFS:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        """
        Check if path exists from source to destination using DFS.

        Key Insight:
        - Build adjacency list from edge list
        - DFS from source
        - Return True if we reach destination

        Early termination: Stop as soon as destination is found.
        """
        if source == destination:
            return True

        # Build adjacency list
        graph: dict[int, list[int]] = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)  # Undirected

        visited: set[int] = set()

        def dfs(node: int) -> bool:
            if node == destination:
                return True

            visited.add(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True

            return False

        return dfs(source)
```

### 8.3 Trace Example

```
n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]]
source = 0, destination = 5

Graph:
  0 -- 1
  |
  2

  3 -- 5
   \  /
    4

Components: {0, 1, 2} and {3, 4, 5}

DFS from 0:
1. Visit 0, neighbors: 1, 2
2. Visit 1, neighbors: 0 (visited)
3. Visit 2, neighbors: 0 (visited)
4. Exhausted component, destination 5 not found

Result: False (different components)

If destination = 2:
DFS from 0:
1. Visit 0, neighbors: 1, 2
2. Visit 1... or
2. Visit 2 → FOUND!

Result: True
```

### 8.4 BFS Alternative

```python
from collections import deque, defaultdict

class SolutionBFS:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        """BFS approach with early termination."""
        if source == destination:
            return True

        graph: dict[int, list[int]] = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        visited: set[int] = {source}
        queue: deque[int] = deque([source])

        while queue:
            node = queue.popleft()

            for neighbor in graph[node]:
                if neighbor == destination:
                    return True
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return False
```

### 8.5 Union-Find Alternative

```python
class SolutionUnionFind:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        """
        Union-Find approach - check if source and destination are in same component.

        When to use Union-Find vs DFS/BFS:
        - Single query: DFS/BFS is simpler
        - Multiple queries: Union-Find is more efficient (preprocess once)
        - Dynamic connectivity: Union-Find handles edge additions
        """
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]

        def union(x: int, y: int) -> None:
            px, py = find(x), find(y)
            if px == py:
                return
            # Union by rank
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1

        # Union all edges
        for u, v in edges:
            union(u, v)

        # Check if same component
        return find(source) == find(destination)
```

### 8.6 Approach Comparison

| Approach | Time | Space | Best For |
|----------|------|-------|----------|
| DFS | O(V + E) | O(V + E) | Single query, simple implementation |
| BFS | O(V + E) | O(V + E) | Single query, shortest path needed |
| Union-Find | O(E × α(n)) | O(V) | Multiple queries, dynamic graphs |

α(n) = inverse Ackermann function, effectively constant

### 8.7 When to Choose Each

```python
# DFS: Simple reachability, recursive thinking
# - Easy to implement
# - Good for single query
# - Natural for exploring all paths

# BFS: Need shortest path or level information
# - Guaranteed shortest path in unweighted graph
# - Good for single query
# - Level-by-level exploration

# Union-Find: Multiple connectivity queries
# - Preprocess graph once
# - O(α(n)) per query after preprocessing
# - Handles edge additions efficiently
```

### 8.8 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| DFS | O(V + E) | O(V + E) graph + O(V) visited + recursion |
| BFS | O(V + E) | O(V + E) graph + O(V) visited + queue |
| Union-Find | O(E × α(n)) | O(V) for parent/rank arrays |

### 8.9 Related Problems

| Problem | Connection |
|---------|------------|
| LC 200: Number of Islands | Count connected components |
| LC 547: Number of Provinces | Same as Number of Islands |
| LC 684: Redundant Connection | Union-Find cycle detection |

---

---

## 9. Pattern Comparison Matrix

### 9.1 By Problem Type

| Problem Type | Best Pattern | Alternative | When to Switch |
|--------------|--------------|-------------|----------------|
| Count islands/regions | DFS flood fill | BFS | Large grid (avoid stack overflow) |
| Clone graph | DFS + hash map | BFS + hash map | Personal preference |
| Multi-source spread | Multi-source BFS | - | Always BFS for simultaneous spread |
| Bipartite check | BFS coloring | DFS coloring | Personal preference |
| Reachability | DFS | BFS, Union-Find | Multiple queries → Union-Find |
| Shortest path (unweighted) | BFS | - | Always BFS for shortest path |
| Shortest path (weighted) | Dijkstra | Bellman-Ford | Negative edges → Bellman-Ford |

### 9.2 DFS vs BFS Selection

| Factor | Choose DFS | Choose BFS |
|--------|------------|------------|
| **Goal** | Existence, all paths | Shortest path, levels |
| **Memory** | O(depth) | O(width) |
| **Implementation** | Recursive (simpler) | Iterative (queue) |
| **Early termination** | Good | Good |
| **Level tracking** | Harder | Natural |
| **Cycle detection** | Postorder time | Layer check |

### 9.3 By Data Structure

| Input | Pattern | Key Consideration |
|-------|---------|-------------------|
| Adjacency list | Standard DFS/BFS | Most common |
| Edge list | Build adj list first | O(E) preprocessing |
| Adjacency matrix | Iterate row for neighbors | O(V²) if dense |
| Grid | Implicit graph | 4/8 directional |

### 9.4 Time/Space Complexity Summary

| Pattern | Time | Space |
|---------|------|-------|
| DFS (recursive) | O(V + E) | O(V) visited + O(V) stack |
| DFS (iterative) | O(V + E) | O(V) visited + O(V) stack |
| BFS | O(V + E) | O(V) visited + O(V) queue |
| Multi-source BFS | O(V + E) | O(V) for multiple sources |
| Union-Find | O(E × α(V)) | O(V) for parent array |

---

---

## 10. Pattern Decision Guide

### 10.1 Quick Decision Tree

```
Graph Problem?
├── Need shortest path?
│   ├── Unweighted → BFS
│   ├── Non-negative weights → Dijkstra
│   └── Negative weights → Bellman-Ford
├── Count components?
│   └── DFS/BFS from each unvisited → Count DFS calls
├── Clone/copy structure?
│   └── DFS/BFS + hash map (old → new)
├── Spread from multiple sources?
│   └── Multi-source BFS (queue all sources)
├── Bipartite/two-coloring?
│   └── BFS/DFS with alternating colors
├── Reachability (can reach X from Y)?
│   ├── Single query → DFS/BFS
│   └── Multiple queries → Union-Find
└── Cycle detection?
    ├── Undirected → Union-Find or DFS with parent tracking
    └── Directed → DFS with coloring (white/gray/black)
```

### 10.2 Signal-to-Pattern Mapping

| Problem Signal | Pattern | Template |
|----------------|---------|----------|
| "count islands" | Connected components | LC 200 |
| "minimum time/distance" | BFS shortest path | LC 994 |
| "spread simultaneously" | Multi-source BFS | LC 994 |
| "reach both X and Y" | Two BFS + intersection | LC 417 |
| "deep copy" / "clone" | DFS + hash map | LC 133 |
| "two groups" / "divide" | Bipartite check | LC 785 |
| "can reach" / "visit all" | DFS reachability | LC 841 |
| "connected or not" | Union-Find / DFS | LC 1971 |

### 10.3 Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| Using DFS for shortest path | Won't find shortest | Use BFS instead |
| Not handling disconnected graphs | Missing components | Loop over all nodes |
| Not marking visited before enqueue | Duplicate processing | Mark when adding to queue |
| Modifying graph during traversal | Unexpected behavior | Use separate visited set |
| Stack overflow on large grids | Recursion limit | Use iterative DFS/BFS |

### 10.4 Grid-Specific Considerations

```python
# Grid traversal setup
rows, cols = len(grid), len(grid[0])
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def is_valid(r: int, c: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols

# Common patterns:
# - Mark visited in-place: grid[r][c] = '#' or '0'
# - Use visited set: visited.add((r, c))
# - Check condition: grid[r][c] == target_value
```

---

---

## 11. Quick Reference Templates

### 11.1 Template 1: DFS Connected Components (Grid)

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

### 11.2 Template 2: BFS Shortest Path (Unweighted)

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

### 11.3 Template 3: Multi-Source BFS

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

### 11.4 Template 4: Graph Clone (DFS)

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

### 11.5 Template 5: Bipartite Check (BFS)

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

### 11.6 Template 6: DFS Reachability

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



---



*Document generated for NeetCode Practice Framework — API Kernel: GraphDFS*

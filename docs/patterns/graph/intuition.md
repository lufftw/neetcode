# Graph Traversal: Intuition Guide

## The Mental Model

Imagine you're exploring a maze. You have two fundamental strategies:

1. **DFS (Depth-First Search)**: Follow one path as far as it goes before backtracking. Like exploring a maze by always turning right until you hit a dead end, then backing up.

2. **BFS (Breadth-First Search)**: Explore all paths simultaneously, one step at a time. Like water spreading from a source—it reaches all points at distance 1 before reaching points at distance 2.

The key insight: **BFS naturally measures distance** (levels = steps from source), while **DFS naturally finds existence** (is there any path?).

---

## Pattern Recognition Signals

### Signal: "Count islands/regions/components"

**Trigger phrases**: "count islands", "number of regions", "connected components"

**Mental model**: Each DFS/BFS from an unvisited node explores one complete component.

```
Grid:
  1 1 0 0 1
  1 1 0 0 1
  0 0 0 1 1

Start DFS at (0,0) → marks entire island 1
Start DFS at (0,4) → marks entire island 2
Start DFS at (2,3) → marks entire island 3

count = 3 (number of DFS calls)
```

**Key insight**: The answer equals the number of times you start a new traversal.

### Signal: "Minimum time/distance/steps"

**Trigger phrases**: "minimum time", "shortest path", "fewest steps", "minimum moves"

**Mental model**: BFS levels = distance from source. First time you reach target = shortest path.

```
Grid with obstacle:
  S . . .    Level 0: S
  . # . .    Level 1: adjacent to S
  . # . .    Level 2: two steps from S
  . . . E    Level 3: three steps from S
             ...

BFS guarantees: E reached at level N means shortest path is N.
```

**Why BFS, not DFS?** DFS might find a path of length 10, missing the path of length 3. BFS explores all length-3 paths before any length-4 paths.

### Signal: "Spread from multiple sources"

**Trigger phrases**: "spread simultaneously", "from all sources at once", "fire spreading"

**Mental model**: Multiple sources are like multiple fires starting at once. Each spreads at the same rate.

```
Rotting oranges spread:
  2 1 1      Minute 0: All rotten in queue
  1 1 0      Minute 1: All adjacent become rotten
  0 1 1      Minute 2: Next layer becomes rotten
             ...

Key: Initialize BFS queue with ALL sources, not just one.
```

### Signal: "Two groups" or "bipartite"

**Trigger phrases**: "divide into two groups", "two-coloring", "bipartite", "no conflict in same group"

**Mental model**: Color alternation. If you can paint a graph with two colors such that no adjacent nodes share a color, it's bipartite.

```
Bipartite:           Not bipartite (odd cycle):
  0 --- 1              0 --- 1
  |     |               \   /
  3 --- 2                 2

Colors: 0=A, 1=B, 2=A, 3=B   Colors: 0=A, 1=B, 2=? (conflict!)
```

**Key insight**: BFS levels naturally alternate. If a neighbor is already colored with the current color → conflict.

### Signal: "Clone/copy" graph structure

**Trigger phrases**: "deep copy", "clone graph", "duplicate structure"

**Mental model**: Build a translation dictionary (old node → new node). When you visit a node, create its clone. When you revisit, return the existing clone.

```
Original:    Clone process:
  1 --- 2    Visit 1: Create 1', map[1] = 1'
  |     |    Visit 2: Create 2', map[2] = 2'
  4 --- 3    Visit 3: Create 3', map[3] = 3'
             Visit 4: Create 4', map[4] = 4'
             Connect using map lookups.
```

### Signal: "Can reach destination" or "reachability"

**Trigger phrases**: "can reach", "path exists", "visit all", "accessible"

**Mental model**: Just run DFS/BFS and check what's reachable.

```
Graph:
  0 -- 1    3 -- 4
       \        |
        2       5

From 0: reachable = {0, 1, 2}
Can reach 5 from 0? No (different component)
```

---

## DFS vs BFS: When to Use Which

| Use DFS when... | Use BFS when... |
|-----------------|-----------------|
| Counting components | Finding shortest path |
| Detecting cycles | Finding minimum steps |
| Exploring all paths | Level-by-level processing |
| Memory is tight (recursion depth < width) | Graph is very deep |
| Need backtracking | Multi-source propagation |

**Memory comparison**:
- DFS: O(depth) for recursion stack
- BFS: O(width) for queue

For a balanced tree, width ≈ n/2 at bottom level, depth ≈ log(n). BFS uses more memory for trees.
For a long chain, depth = n, width = 1. DFS uses more memory for chains.

---

## Common Pitfalls

### Pitfall 1: Using DFS for shortest path

```python
# WRONG: DFS might find a long path first
def dfs_shortest(start, end):  # Don't do this!
    # DFS doesn't guarantee shortest path

# CORRECT: Use BFS for shortest path
def bfs_shortest(start, end):
    queue = deque([(start, 0)])  # (node, distance)
    # First time reaching end = shortest
```

### Pitfall 2: Not handling disconnected graphs

```python
# WRONG: Only checking one component
def count_components(graph):
    visited = set()
    dfs(0, visited)  # Only explores component containing node 0!

# CORRECT: Check all nodes
def count_components(graph):
    visited = set()
    count = 0
    for node in range(len(graph)):
        if node not in visited:
            dfs(node, visited)
            count += 1
    return count
```

### Pitfall 3: Marking visited at wrong time (BFS)

```python
# WRONG: Mark visited when popping
while queue:
    node = queue.popleft()
    visited.add(node)  # Too late! Node might be added multiple times

# CORRECT: Mark visited when adding to queue
for neighbor in graph[node]:
    if neighbor not in visited:
        visited.add(neighbor)  # Mark immediately
        queue.append(neighbor)
```

### Pitfall 4: Modifying grid during iteration

```python
# Be careful with in-place modification
# Either mark visited separately, or understand that
# grid[r][c] = '0' prevents revisiting
```

### Pitfall 5: Stack overflow on large grids

```python
# WRONG for large grids: Recursive DFS
def dfs(r, c):  # Might hit Python recursion limit
    dfs(r+1, c)
    dfs(r-1, c)
    ...

# CORRECT: Iterative DFS with explicit stack
def dfs_iterative(start_r, start_c):
    stack = [(start_r, start_c)]
    while stack:
        r, c = stack.pop()
        # process and add neighbors to stack
```

---

## Practice Progression

### Level 1: Basic DFS/BFS (Master First!)
1. **LC 200 - Number of Islands**: Classic connected components
2. **LC 733 - Flood Fill**: Basic DFS on grid

### Level 2: BFS for Shortest Path
3. **LC 994 - Rotting Oranges**: Multi-source BFS
4. **LC 1091 - Shortest Path in Binary Matrix**: BFS shortest path

### Level 3: Graph Structure
5. **LC 133 - Clone Graph**: Graph cloning
6. **LC 841 - Keys and Rooms**: Reachability check

### Level 4: Advanced Applications
7. **LC 785 - Is Graph Bipartite?**: Two-coloring
8. **LC 417 - Pacific Atlantic Water Flow**: Reverse BFS from multiple sources

### Level 5: Path Existence
9. **LC 1971 - Find if Path Exists in Graph**: Basic connectivity
10. **LC 547 - Number of Provinces**: Connected components (adjacency matrix)

---

## Quick Decision Tree

```
Problem type...
├── "Count islands/regions" → DFS/BFS from each unvisited (LC 200)
├── "Minimum time/distance" → BFS (LC 994)
├── "Spread from multiple sources" → Multi-source BFS (LC 994)
├── "Clone/copy graph" → DFS + hash map (LC 133)
├── "Two groups/bipartite" → BFS/DFS coloring (LC 785)
├── "Can reach all/visit all" → DFS reachability (LC 841)
├── "Path exists between X and Y"
│   ├── Single query → DFS/BFS (LC 1971)
│   └── Multiple queries → Union-Find
└── "Flow to destination" → Reverse from destination (LC 417)
```

---

## Related Patterns

| If you see... | Consider also... |
|--------------|------------------|
| Connected components | Union-Find (especially for dynamic) |
| Shortest path (weighted) | Dijkstra's algorithm |
| Shortest path (negative weights) | Bellman-Ford |
| All-pairs shortest path | Floyd-Warshall |
| Cycle detection (directed) | Topological sort |
| Minimum spanning tree | Kruskal's / Prim's |

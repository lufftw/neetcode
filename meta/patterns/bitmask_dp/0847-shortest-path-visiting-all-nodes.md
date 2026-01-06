# 847. Shortest Path Visiting All Nodes

## Problem Link
https://leetcode.com/problems/shortest-path-visiting-all-nodes/

## Difficulty
Hard

## Tags
- Bitmask DP
- BFS
- Graph
- State Compression

## Pattern
Bitmask DP - TSP-style / BFS with Bitmask State

## API Kernel
`BitmaskDP`

## Problem Summary
Given an undirected graph with n nodes, find the length of the shortest path that visits every node. You may start and stop at any node, revisit nodes, and reuse edges.

## Key Insight

State = (current_node, visited_mask):
- `visited_mask` tracks which nodes have been visited
- BFS explores all states level by level
- First state with `visited_mask == (1 << n) - 1` is the answer

Unlike classic TSP, we can revisit nodes, so BFS works (no need for DP minimum tracking).

## Template Mapping

```python
from collections import deque

def shortestPathLength(graph):
    n = len(graph)
    if n == 1:
        return 0

    full_mask = (1 << n) - 1

    # State: (node, visited_mask)
    # Initialize: start from every node
    queue = deque()
    visited = set()

    for i in range(n):
        state = (i, 1 << i)
        queue.append((i, 1 << i, 0))  # (node, mask, distance)
        visited.add(state)

    while queue:
        node, mask, dist = queue.popleft()

        for neighbor in graph[node]:
            new_mask = mask | (1 << neighbor)

            if new_mask == full_mask:
                return dist + 1

            state = (neighbor, new_mask)
            if state not in visited:
                visited.add(state)
                queue.append((neighbor, new_mask, dist + 1))

    return -1  # Should never reach here for connected graph
```

## Complexity
- Time: O(n × 2^n) - n nodes × 2^n possible masks
- Space: O(n × 2^n) - visited states

## Why This Problem Second?

1. **Combines BFS with bitmask** - State includes both position and visited set
2. **TSP variant** - Classic interview pattern
3. **State space explosion** - Shows why n ≤ 12 constraint is critical

## Key Observations

1. **Multi-source BFS** - Start from all nodes simultaneously
2. **State deduplication** - (node, mask) pair uniquely identifies state
3. **Early termination** - Return immediately when full_mask reached

## Common Mistakes

1. **Single-source BFS** - Must try all starting nodes
2. **Forgetting node in state** - State is (node, mask), not just mask
3. **Not handling n=1** - Edge case returns 0

## Related Problems
- LC 943: Find the Shortest Superstring
- LC 1494: Parallel Courses II
- LC 1066: Campus Bikes II

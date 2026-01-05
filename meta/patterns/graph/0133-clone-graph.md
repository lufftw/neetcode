## Clone Graph (LeetCode 133)

> **Problem**: Create a deep copy of a connected undirected graph.
> **Pattern**: DFS/BFS with node mapping
> **Variant**: Clone structure while maintaining references.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "deep copy" / "clone" | → Map old to new nodes |
| "maintain structure" | → Copy edges during traversal |
| "connected graph" | → Single component, start from any node |

### Implementation

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

### Trace Example

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

### BFS Alternative

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

### Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| DFS | O(V + E) | O(V) for map + recursion |
| BFS | O(V + E) | O(V) for map + queue |

### Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Creating duplicate clones | Infinite loop with cycles | Use hash map |
| Not handling null input | NullPointerException | Check `if not node` |
| Shallow copy of neighbors | Original and clone share references | Clone neighbor list |



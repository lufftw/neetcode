## Advanced: Sort Items by Groups (LeetCode 1203)

> **Problem**: Sort items respecting both group order and item dependencies.
> **Delta from Base**: Two-level topological sort (groups, then items within groups).
> **Role**: HARD problem demonstrating nested topological ordering.

### Problem Statement

There are `n` items, each belonging to zero or one group. A group can be empty. `group[i]` is the group that the `i`-th item belongs to (-1 means no group).

Items can have dependencies: `beforeItems[i]` contains items that must come before item `i`.

Return a sorted list of items such that:
1. Items in the same group appear consecutively
2. Dependencies are respected

Return empty array if impossible.

### Key Insight

This requires **two-level topological sort**:

1. **Build group graph**: If item `a` (group X) must come before item `b` (group Y) and X ≠ Y, then group X must come before group Y.

2. **Build item graph within each group**: Standard item dependencies within same group.

3. **Sort groups topologically**, then within each group, sort items topologically.

### Implementation

```python
class Solution:
    def sortItems(self, n: int, m: int, group: List[int], beforeItems: List[List[int]]) -> List[int]:
        """
        Two-level topological sort: groups first, then items within groups.
        """
        # Assign unique group IDs to ungrouped items (-1)
        group_id = m
        for i in range(n):
            if group[i] == -1:
                group[i] = group_id
                group_id += 1

        # Build graphs for groups and items
        num_groups = group_id
        group_graph: List[Set[int]] = [set() for _ in range(num_groups)]
        group_in_degree: List[int] = [0] * num_groups

        item_graph: List[List[int]] = [[] for _ in range(n)]
        item_in_degree: List[int] = [0] * n

        for item in range(n):
            for before in beforeItems[item]:
                # Item dependency
                item_graph[before].append(item)
                item_in_degree[item] += 1

                # Group dependency (if different groups)
                if group[before] != group[item]:
                    if group[item] not in group_graph[group[before]]:
                        group_graph[group[before]].add(group[item])
                        group_in_degree[group[item]] += 1

        def topo_sort(nodes: List[int], graph: List, in_degree: List[int]) -> List[int]:
            """Generic topological sort using Kahn's algorithm."""
            queue = deque([node for node in nodes if in_degree[node] == 0])
            result = []

            while queue:
                node = queue.popleft()
                result.append(node)

                for neighbor in (graph[node] if isinstance(graph[node], list) else list(graph[node])):
                    if neighbor in nodes or isinstance(nodes, range):
                        in_degree[neighbor] -= 1
                        if in_degree[neighbor] == 0:
                            queue.append(neighbor)

            return result if len(result) == len(nodes) else []

        # Sort groups topologically
        group_order = topo_sort(list(range(num_groups)), group_graph, group_in_degree)
        if not group_order:
            return []

        # Group items by their group
        group_items: List[List[int]] = [[] for _ in range(num_groups)]
        for item in range(n):
            group_items[group[item]].append(item)

        # Sort items within each group and build result
        result: List[int] = []
        for g in group_order:
            items = group_items[g]
            if not items:
                continue

            # Topological sort items in this group
            sorted_items = topo_sort(items, item_graph, item_in_degree.copy())
            if len(sorted_items) != len(items):
                return []

            result.extend(sorted_items)

        return result
```

### Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | O(V + E) where V = n + num_groups, E = total dependencies |
| Space | O(V + E) |

### Trace Example

```
Input: n=8, m=2, group=[-1,-1,1,0,0,1,0,-1],
       beforeItems=[[],[6],[5],[6],[3,6],[],[],[]]

After assigning group IDs:
  Items:  0  1  2  3  4  5  6  7
  Groups: 2  3  1  0  0  1  0  4

Group dependencies:
  0 → (nothing)
  1 → (nothing)
  2 → (nothing)
  3 → 0 (item 1 needs item 6, group 3 needs group 0)
  4 → (nothing)

Item dependencies (within groups):
  Group 0: 6 → 3, 6 → 4, 3 → 4?
  Group 1: 5 → 2

Group order: [0, 1, 2, 3, 4] (one valid)
Items in order: [6, 3, 4] + [5, 2] + [0] + [1] + [7]

Result: [6, 3, 4, 5, 2, 0, 1, 7]
```

---

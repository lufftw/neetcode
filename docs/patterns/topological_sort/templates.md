# Topological Sort Patterns: Complete Reference

> **API Kernel**: `TopologicalSort`
> **Core Mechanism**: Order nodes in a DAG such that for every directed edge u→v, u comes before v.

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Course Schedule (LeetCode 207)](#2-base-template-course-schedule-leetcode-207)
3. [Variant: Course Schedule II (LeetCode 210)](#3-variant-course-schedule-ii-leetcode-210)
4. [Variant: Find Eventual Safe States (LeetCode 802)](#4-variant-find-eventual-safe-states-leetcode-802)
5. [Advanced: Sort Items by Groups (LeetCode 1203)](#5-advanced-sort-items-by-groups-leetcode-1203)
6. [Pattern Comparison](#6-pattern-comparison)
7. [Decision Guide: When to Use Topological Sort](#7-decision-guide-when-to-use-topological-sort)
8. [Quick Reference Templates](#8-quick-reference-templates)

---

## 1. Core Concepts

### 1.1 The Topological Order Principle

A **topological order** is a linear ordering of vertices in a Directed Acyclic Graph (DAG) where for every directed edge (u, v), vertex u appears before vertex v.

**Key Properties**:
- Only exists for DAGs (no cycles)
- May have multiple valid orderings
- Detecting a cycle = no valid topological order exists

### 1.2 Two Canonical Algorithms

#### 1. Kahn's Algorithm (BFS / In-degree)

Process nodes with in-degree 0 first, then reduce neighbors' in-degrees:

```python
def kahn_topological_sort(num_nodes: int, edges: List[List[int]]) -> List[int]:
    """
    BFS-based topological sort using in-degree counting.
    Returns empty list if cycle detected.
    """
    # Build adjacency list and in-degree count
    graph: List[List[int]] = [[] for _ in range(num_nodes)]
    in_degree: List[int] = [0] * num_nodes

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Initialize queue with all nodes having in-degree 0
    queue: deque[int] = deque()
    for node in range(num_nodes):
        if in_degree[node] == 0:
            queue.append(node)

    topo_order: List[int] = []

    while queue:
        node = queue.popleft()
        topo_order.append(node)

        # Reduce in-degree of neighbors
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If not all nodes processed, cycle exists
    if len(topo_order) != num_nodes:
        return []  # Cycle detected

    return topo_order
```

#### 2. DFS Postorder (with Cycle Detection)

DFS explores deeply, adding nodes to result in reverse postorder:

```python
def dfs_topological_sort(num_nodes: int, edges: List[List[int]]) -> List[int]:
    """
    DFS-based topological sort using postorder reversal.
    Returns empty list if cycle detected.

    State colors:
    - WHITE (0): Unvisited
    - GRAY (1): In current DFS path (cycle detection)
    - BLACK (2): Fully processed
    """
    WHITE, GRAY, BLACK = 0, 1, 2

    # Build adjacency list
    graph: List[List[int]] = [[] for _ in range(num_nodes)]
    for u, v in edges:
        graph[u].append(v)

    color: List[int] = [WHITE] * num_nodes
    topo_order: List[int] = []
    has_cycle = False

    def dfs(node: int) -> None:
        nonlocal has_cycle
        if has_cycle:
            return

        color[node] = GRAY  # Mark as being processed

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                has_cycle = True  # Back edge = cycle
                return
            if color[neighbor] == WHITE:
                dfs(neighbor)

        color[node] = BLACK  # Mark as fully processed
        topo_order.append(node)  # Postorder: add after all descendants

    for node in range(num_nodes):
        if color[node] == WHITE:
            dfs(node)
            if has_cycle:
                return []

    return topo_order[::-1]  # Reverse for topological order
```

### 1.3 Cycle Detection

**Using Kahn's Algorithm**:
- If `len(result) < num_nodes`, a cycle exists
- Nodes in cycle never reach in-degree 0

**Using DFS**:
- Back edge (visiting a GRAY node) indicates cycle
- Three-color marking: WHITE → GRAY → BLACK

### 1.4 Pattern Variants

| Variant | Key Modification | Example Problem |
|---------|-----------------|-----------------|
| Cycle Detection | Return boolean instead of order | LC 207 |
| Full Order | Return one valid topological order | LC 210 |
| Safe States | Reverse graph, find nodes not in cycles | LC 802 |
| Multi-Level | Nested topological sort | LC 1203 |

---

## 2. Base Template: Course Schedule (LeetCode 207)

> **Problem**: Determine if all courses can be finished given prerequisites.
> **Invariant**: DAG has valid topological order ⟺ no cycle exists.
> **Role**: BASE TEMPLATE for cycle detection in directed graph.

### 2.1 Problem Statement

There are `numCourses` courses labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates you must take course `bi` before course `ai`.

Return `true` if you can finish all courses, or `false` otherwise.

### 2.2 Key Insight

This is **cycle detection** in a directed graph. If prerequisites form a cycle (A requires B, B requires C, C requires A), it's impossible to complete all courses.

### 2.3 Implementation (Kahn's Algorithm)

```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Detect if course dependency graph has no cycles.
        Use Kahn's algorithm: if we can process all nodes, no cycle exists.
        """
        # Build graph and in-degree count
        graph: List[List[int]] = [[] for _ in range(numCourses)]
        in_degree: List[int] = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1

        # Start with courses having no prerequisites
        queue: deque[int] = deque()
        for course in range(numCourses):
            if in_degree[course] == 0:
                queue.append(course)

        courses_taken = 0

        while queue:
            course = queue.popleft()
            courses_taken += 1

            for next_course in graph[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)

        # All courses taken = no cycle
        return courses_taken == numCourses
```

### 2.4 Implementation (DFS Three-Color)

```python
class SolutionDFS:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        DFS with three-color marking for cycle detection.
        GRAY node in path = back edge = cycle.
        """
        WHITE, GRAY, BLACK = 0, 1, 2

        graph: List[List[int]] = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            graph[prereq].append(course)

        color: List[int] = [WHITE] * numCourses

        def has_cycle(node: int) -> bool:
            color[node] = GRAY

            for neighbor in graph[node]:
                if color[neighbor] == GRAY:
                    return True  # Back edge = cycle
                if color[neighbor] == WHITE and has_cycle(neighbor):
                    return True

            color[node] = BLACK
            return False

        for course in range(numCourses):
            if color[course] == WHITE:
                if has_cycle(course):
                    return False

        return True
```

### 2.5 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Kahn's (BFS) | O(V + E) | O(V + E) |
| DFS Three-Color | O(V + E) | O(V + E) |

### 2.6 Trace Example

```
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]

Graph (prereq → course):
  0 → 1, 2
  1 → 3
  2 → 3

In-degrees: [0, 1, 1, 2]

Kahn's Algorithm:
  Queue: [0] (in-degree 0)
  Process 0 → Queue: [1, 2], taken = 1
  Process 1 → in_degree[3] = 1, Queue: [2], taken = 2
  Process 2 → in_degree[3] = 0, Queue: [3], taken = 3
  Process 3 → taken = 4

  4 == 4 → True (no cycle)
```

---

## 3. Variant: Course Schedule II (LeetCode 210)

> **Problem**: Return one valid order to take all courses, or empty if impossible.
> **Delta from Base**: Return the actual topological order, not just boolean.
> **Role**: BASE TEMPLATE for producing topological ordering.

### 3.1 Problem Statement

There are `numCourses` courses labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates you must take course `bi` before course `ai`.

Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it's impossible, return an empty array.

### 3.2 Key Insight

Same as LC 207, but instead of returning boolean, **collect the order** as nodes are processed. Kahn's naturally produces valid order; DFS requires reversal.

### 3.3 Implementation (Kahn's Algorithm)

```python
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Return one valid topological order of courses.
        Kahn's BFS naturally produces the order.
        """
        graph: List[List[int]] = [[] for _ in range(numCourses)]
        in_degree: List[int] = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1

        queue: deque[int] = deque()
        for course in range(numCourses):
            if in_degree[course] == 0:
                queue.append(course)

        order: List[int] = []

        while queue:
            course = queue.popleft()
            order.append(course)

            for next_course in graph[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)

        # Return order if all courses included, else empty (cycle)
        return order if len(order) == numCourses else []
```

### 3.4 Implementation (DFS Postorder)

```python
class SolutionDFS:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        DFS postorder: add node after processing all descendants.
        Reverse at end for topological order.
        """
        WHITE, GRAY, BLACK = 0, 1, 2

        graph: List[List[int]] = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            graph[prereq].append(course)

        color: List[int] = [WHITE] * numCourses
        order: List[int] = []
        has_cycle = False

        def dfs(node: int) -> None:
            nonlocal has_cycle
            if has_cycle:
                return

            color[node] = GRAY

            for neighbor in graph[node]:
                if color[neighbor] == GRAY:
                    has_cycle = True
                    return
                if color[neighbor] == WHITE:
                    dfs(neighbor)

            color[node] = BLACK
            order.append(node)  # Postorder

        for course in range(numCourses):
            if color[course] == WHITE:
                dfs(course)
                if has_cycle:
                    return []

        return order[::-1]  # Reverse for topological order
```

### 3.5 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Kahn's (BFS) | O(V + E) | O(V + E) |
| DFS Postorder | O(V + E) | O(V + E) |

### 3.6 Trace Example

```
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]

Kahn's produces order: [0, 1, 2, 3] or [0, 2, 1, 3]
(Both valid - 0 before 1,2; 1,2 before 3)

DFS Postorder (starting from 0):
  Visit 0 → Visit 1 → Visit 3 → Add 3
            ← Back to 1 → Add 1
          → Visit 2 → (3 already BLACK) → Add 2
  ← Back to 0 → Add 0

  Postorder: [3, 1, 2, 0]
  Reversed:  [0, 2, 1, 3] ✓
```

---

## 4. Variant: Find Eventual Safe States (LeetCode 802)

> **Problem**: Find all nodes that eventually lead only to terminal nodes.
> **Delta from Base**: Work on reversed graph; find nodes NOT in any cycle.
> **Role**: Demonstrates reverse topological analysis and safe state detection.

### 4.1 Problem Statement

There is a directed graph of `n` nodes with each node labeled from `0` to `n - 1`. The graph is represented by a 0-indexed 2D integer array `graph` where `graph[i]` is an integer array of nodes adjacent to node `i`.

A node is a **terminal node** if there are no outgoing edges. A node is a **safe node** if every possible path starting from that node leads to a terminal node (or another safe node).

Return an array containing all the safe nodes in ascending order.

### 4.2 Key Insight

A node is **safe** if and only if it's NOT part of a cycle and all paths from it lead to terminal nodes.

**Approach 1 (DFS)**: Color-based cycle detection. Nodes that finish (BLACK) without finding a cycle are safe.

**Approach 2 (Reverse + Kahn)**: Reverse graph direction, then terminal nodes have out-degree 0. Run Kahn's from terminals.

### 4.3 Implementation (DFS Three-Color)

```python
class Solution:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        """
        Find nodes not in any cycle using three-color DFS.
        Safe = reaches BLACK state without encountering GRAY.
        """
        n = len(graph)
        WHITE, GRAY, BLACK = 0, 1, 2
        color: List[int] = [WHITE] * n

        def is_safe(node: int) -> bool:
            if color[node] == GRAY:
                return False  # In cycle
            if color[node] == BLACK:
                return True   # Already verified safe

            color[node] = GRAY

            for neighbor in graph[node]:
                if not is_safe(neighbor):
                    return False  # Leads to cycle

            color[node] = BLACK
            return True

        return [node for node in range(n) if is_safe(node)]
```

### 4.4 Implementation (Reverse Graph + Kahn's)

```python
class SolutionKahn:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        """
        Reverse graph, then run Kahn's from terminal nodes.
        Nodes reachable in reverse = safe nodes.
        """
        n = len(graph)

        # Build reverse graph and out-degree
        reverse_graph: List[List[int]] = [[] for _ in range(n)]
        out_degree: List[int] = [0] * n

        for node in range(n):
            out_degree[node] = len(graph[node])
            for neighbor in graph[node]:
                reverse_graph[neighbor].append(node)

        # Start with terminal nodes (out-degree 0)
        queue: deque[int] = deque()
        for node in range(n):
            if out_degree[node] == 0:
                queue.append(node)

        safe: List[bool] = [False] * n

        while queue:
            node = queue.popleft()
            safe[node] = True

            # Process predecessors in reverse graph
            for pred in reverse_graph[node]:
                out_degree[pred] -= 1
                if out_degree[pred] == 0:
                    queue.append(pred)

        return [node for node in range(n) if safe[node]]
```

### 4.5 Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| DFS Three-Color | O(V + E) | O(V) |
| Reverse + Kahn | O(V + E) | O(V + E) |

### 4.6 Trace Example

```
Input: graph = [[1,2],[2,3],[5],[0],[5],[],[]]
       0 → 1, 2
       1 → 2, 3
       2 → 5
       3 → 0  (creates cycle: 0→1→3→0)
       4 → 5
       5 → (terminal)
       6 → (terminal)

DFS from 0:
  0 (GRAY) → 1 (GRAY) → 2 (GRAY) → 5 (GRAY→BLACK, safe)
           ← 2 (BLACK, safe)
           → 3 (GRAY) → 0 (GRAY!) → CYCLE!
  0, 1, 3 are NOT safe

DFS from 2: Already BLACK, safe
DFS from 4: 4→5 (BLACK), 4 is safe
DFS from 5, 6: Terminal, safe

Answer: [2, 4, 5, 6]
```

---

## 5. Advanced: Sort Items by Groups (LeetCode 1203)

> **Problem**: Sort items respecting both group order and item dependencies.
> **Delta from Base**: Two-level topological sort (groups, then items within groups).
> **Role**: HARD problem demonstrating nested topological ordering.

### 5.1 Problem Statement

There are `n` items, each belonging to zero or one group. A group can be empty. `group[i]` is the group that the `i`-th item belongs to (-1 means no group).

Items can have dependencies: `beforeItems[i]` contains items that must come before item `i`.

Return a sorted list of items such that:
1. Items in the same group appear consecutively
2. Dependencies are respected

Return empty array if impossible.

### 5.2 Key Insight

This requires **two-level topological sort**:

1. **Build group graph**: If item `a` (group X) must come before item `b` (group Y) and X ≠ Y, then group X must come before group Y.

2. **Build item graph within each group**: Standard item dependencies within same group.

3. **Sort groups topologically**, then within each group, sort items topologically.

### 5.3 Implementation

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

### 5.4 Complexity Analysis

| Metric | Value |
|--------|-------|
| Time | O(V + E) where V = n + num_groups, E = total dependencies |
| Space | O(V + E) |

### 5.5 Trace Example

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

## 6. Pattern Comparison

### 6.1 Kahn's Algorithm vs DFS Postorder

| Aspect | Kahn's (BFS) | DFS Postorder |
|--------|--------------|---------------|
| **Approach** | Process nodes with in-degree 0 | Explore deeply, add on backtrack |
| **Data Structure** | Queue + in-degree array | Recursion stack + color array |
| **Cycle Detection** | `len(result) < n` | Back edge (GRAY → GRAY) |
| **Order Production** | Natural forward order | Reverse of postorder |
| **Parallelism** | Easily parallelizable | Sequential by nature |
| **Best For** | Streaming/online processing | Simple implementation |

### 6.2 Problem Variant Comparison

| Problem | Core Task | Key Modification |
|---------|-----------|------------------|
| LC 207 | Detect if order exists | Return boolean only |
| LC 210 | Find valid order | Collect nodes during traversal |
| LC 802 | Find safe nodes | DFS color or reverse Kahn's |
| LC 1203 | Multi-level ordering | Two-level topo sort |

### 6.3 When to Choose Which Algorithm

```
Choose Kahn's (BFS) when:
├── Need to process in batches/levels
├── Parallelization is important
├── Need to handle dynamic insertions
└── Prefer iterative over recursive

Choose DFS when:
├── Simpler implementation preferred
├── Need to find all topological orderings
├── Stack depth is not a concern
└── Already doing other DFS operations
```

---

## 7. Decision Guide: When to Use Topological Sort

### 7.1 Pattern Recognition Signals

Use Topological Sort when you see:

| Signal | Example Phrases |
|--------|-----------------|
| **Prerequisites/Dependencies** | "must complete X before Y", "depends on" |
| **Ordering with Constraints** | "valid order", "schedule tasks" |
| **Cycle Detection in DAG** | "is it possible to", "can all be completed" |
| **Build Order** | "compilation order", "dependency resolution" |

### 7.2 Decision Flowchart

```
Problem involves ordering/dependencies?
├── Yes
│   ├── Is it a directed graph?
│   │   ├── Yes → Consider Topological Sort
│   │   │   ├── Just detect if order exists?
│   │   │   │   └── LC 207 style (return boolean)
│   │   │   ├── Need the actual order?
│   │   │   │   └── LC 210 style (return list)
│   │   │   ├── Find nodes not in cycles?
│   │   │   │   └── LC 802 style (safe states)
│   │   │   └── Multi-level dependencies?
│   │   │       └── LC 1203 style (nested topo)
│   │   │
│   │   └── No (undirected)
│   │       └── Consider Union-Find or other approaches
│   │
│   └── No ordering constraint
│       └── Different pattern (BFS, DFS, etc.)
│
└── No → Different pattern
```

### 7.3 Related Patterns

| If you see... | Consider... |
|---------------|-------------|
| Shortest path in DAG | Topological Sort + DP |
| Strongly Connected Components | Kosaraju's or Tarjan's |
| Undirected cycle detection | Union-Find |
| Task scheduling with resources | Topological Sort + Heap |
| Longest path in DAG | Topological Sort + DP |

### 7.4 Common Pitfalls

1. **Forgetting self-loops**: A node depending on itself is a cycle
2. **Wrong edge direction**: Prerequisite A→B means A must come BEFORE B
3. **Not handling disconnected components**: Process ALL unvisited nodes
4. **Stack overflow**: Use iterative version for deep graphs

---

## 8. Quick Reference Templates

### 8.1 Template 1: Kahn's Algorithm (BFS)

```python
def topological_sort_kahn(n: int, edges: List[Tuple[int, int]]) -> List[int]:
    """
    Kahn's algorithm for topological sort.
    edges: List of (from, to) pairs meaning from → to

    Returns:
        List of nodes in topological order, or [] if cycle exists.
    """
    from collections import deque

    # Build graph and in-degrees
    graph: List[List[int]] = [[] for _ in range(n)]
    in_degree: List[int] = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Initialize with in-degree 0 nodes
    queue: deque[int] = deque([i for i in range(n) if in_degree[i] == 0])
    result: List[int] = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == n else []
```

### 8.2 Template 2: DFS Postorder

```python
def topological_sort_dfs(n: int, edges: List[Tuple[int, int]]) -> List[int]:
    """
    DFS-based topological sort.
    edges: List of (from, to) pairs meaning from → to

    Returns:
        List of nodes in topological order, or [] if cycle exists.
    """
    WHITE, GRAY, BLACK = 0, 1, 2

    graph: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    color: List[int] = [WHITE] * n
    result: List[int] = []
    has_cycle = False

    def dfs(node: int) -> None:
        nonlocal has_cycle
        if has_cycle:
            return

        color[node] = GRAY

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                has_cycle = True
                return
            if color[neighbor] == WHITE:
                dfs(neighbor)

        color[node] = BLACK
        result.append(node)

    for node in range(n):
        if color[node] == WHITE:
            dfs(node)
            if has_cycle:
                return []

    return result[::-1]
```

### 8.3 Template 3: Cycle Detection Only

```python
def has_cycle(n: int, edges: List[Tuple[int, int]]) -> bool:
    """
    Check if directed graph has a cycle.
    Returns True if cycle exists.
    """
    from collections import deque

    graph: List[List[int]] = [[] for _ in range(n)]
    in_degree: List[int] = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue: deque[int] = deque([i for i in range(n) if in_degree[i] == 0])
    visited = 0

    while queue:
        node = queue.popleft()
        visited += 1

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return visited != n  # True if cycle exists
```

### 8.4 Template 4: Safe Nodes (LC 802 Style)

```python
def find_safe_nodes(graph: List[List[int]]) -> List[int]:
    """
    Find nodes that are not part of any cycle.
    graph[i] = list of nodes reachable from i.
    """
    n = len(graph)
    WHITE, GRAY, BLACK = 0, 1, 2
    color: List[int] = [WHITE] * n

    def is_safe(node: int) -> bool:
        if color[node] == GRAY:
            return False
        if color[node] == BLACK:
            return True

        color[node] = GRAY

        for neighbor in graph[node]:
            if not is_safe(neighbor):
                return False

        color[node] = BLACK
        return True

    return [i for i in range(n) if is_safe(i)]
```

### 8.5 Complexity Summary

| Algorithm | Time | Space |
|-----------|------|-------|
| Kahn's (BFS) | O(V + E) | O(V + E) |
| DFS Postorder | O(V + E) | O(V + E) |
| Cycle Detection | O(V + E) | O(V + E) |
| Safe Nodes | O(V + E) | O(V) |



---



*Document generated for NeetCode Practice Framework — API Kernel: TopologicalSort*

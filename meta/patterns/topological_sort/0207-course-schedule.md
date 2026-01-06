## Base Template: Course Schedule (LeetCode 207)

> **Problem**: Determine if all courses can be finished given prerequisites.
> **Invariant**: DAG has valid topological order ⟺ no cycle exists.
> **Role**: BASE TEMPLATE for cycle detection in directed graph.

### Problem Statement

There are `numCourses` courses labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates you must take course `bi` before course `ai`.

Return `true` if you can finish all courses, or `false` otherwise.

### Key Insight

This is **cycle detection** in a directed graph. If prerequisites form a cycle (A requires B, B requires C, C requires A), it's impossible to complete all courses.

### Implementation (Kahn's Algorithm)

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

### Implementation (DFS Three-Color)

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

### Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Kahn's (BFS) | O(V + E) | O(V + E) |
| DFS Three-Color | O(V + E) | O(V + E) |

### Trace Example

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

## Variant: Course Schedule II (LeetCode 210)

> **Problem**: Return one valid order to take all courses, or empty if impossible.
> **Delta from Base**: Return the actual topological order, not just boolean.
> **Role**: BASE TEMPLATE for producing topological ordering.

### Problem Statement

There are `numCourses` courses labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates you must take course `bi` before course `ai`.

Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it's impossible, return an empty array.

### Key Insight

Same as LC 207, but instead of returning boolean, **collect the order** as nodes are processed. Kahn's naturally produces valid order; DFS requires reversal.

### Implementation (Kahn's Algorithm)

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

### Implementation (DFS Postorder)

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

### Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Kahn's (BFS) | O(V + E) | O(V + E) |
| DFS Postorder | O(V + E) | O(V + E) |

### Trace Example

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

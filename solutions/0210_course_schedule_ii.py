# solutions/0210_course_schedule_ii.py
"""
Problem: Course Schedule II
Link: https://leetcode.com/problems/course-schedule-ii/

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you
must take course bi first if you want to take course ai.

Return the ordering of courses you should take to finish all courses. If there are many
valid answers, return any of them. If it is impossible to finish all courses, return
an empty array.

Example 1:
    Input: numCourses = 2, prerequisites = [[1,0]]
    Output: [0,1]
    Explanation: Take course 0 first, then course 1.

Example 2:
    Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
    Output: [0,2,1,3] or [0,1,2,3]
    Explanation: To take course 3 you should have finished both courses 1 and 2.

Example 3:
    Input: numCourses = 1, prerequisites = []
    Output: [0]

Constraints:
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= numCourses * (numCourses - 1)
- prerequisites[i].length == 2
- 0 <= ai, bi < numCourses
- ai != bi
- All the pairs [ai, bi] are distinct.

Topics: Depth-First Search, Breadth-First Search, Graph, Topological Sort
"""
from typing import List
from collections import deque
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Course Schedule II solution - any valid topological order."""
    import json

    lines = input_data.strip().split('\n')
    num_courses = int(lines[0])
    prerequisites = json.loads(lines[1]) if len(lines) > 1 else []

    # Parse actual result
    if isinstance(actual, str):
        actual = json.loads(actual)

    # Check if cycle exists (empty result expected)
    has_cycle = not _can_finish(num_courses, prerequisites)

    if has_cycle:
        return actual == []

    # Verify actual is a valid topological order
    if len(actual) != num_courses:
        return False

    # Check all courses are present
    if set(actual) != set(range(num_courses)):
        return False

    # Verify prerequisites are satisfied
    position = {course: i for i, course in enumerate(actual)}
    for course, prereq in prerequisites:
        if position[prereq] >= position[course]:
            return False

    return True


def _can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    """Check if all courses can be finished (no cycle)."""
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    visited = 0

    while queue:
        node = queue.popleft()
        visited += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return visited == num_courses


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionKahn",
        "method": "findOrder",
        "complexity": "O(V+E) time, O(V+E) space",
        "description": "Kahn's algorithm returning course order",
        "api_kernels": ["TopologicalSort"],
        "patterns": ["topological_sort_ordering"],
    },
    "dfs": {
        "class": "SolutionDFS",
        "method": "findOrder",
        "complexity": "O(V+E) time, O(V+E) space",
        "description": "DFS postorder (reverse of finish times)",
        "api_kernels": ["TopologicalSort"],
        "patterns": ["topological_sort_dfs_postorder"],
    },
}


# ============================================
# Solution 1: Kahn's Algorithm (BFS)
# Time: O(V + E), Space: O(V + E)
#   - Collect nodes as they reach in-degree 0
#   - Natural topological order produced
# ============================================
class SolutionKahn:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Return a valid course ordering, or empty array if impossible.

        Core insight: Kahn's algorithm produces topological order directly. Process
        nodes with in-degree 0, append to result, decrement neighbors' in-degrees.
        Order of processing = valid course sequence.

        Invariant: result contains courses in valid topological order; remaining
        courses in queue have all prerequisites already in result.

        Args:
            numCourses: Total number of courses
            prerequisites: List of [course, prereq] pairs

        Returns:
            Valid course order, or [] if cycle exists
        """
        # Build adjacency list and in-degree array
        graph: List[List[int]] = [[] for _ in range(numCourses)]
        in_degree: List[int] = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1

        # Initialize queue with nodes having in-degree 0
        queue: deque[int] = deque([i for i in range(numCourses) if in_degree[i] == 0])
        result: List[int] = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Return result if all courses visited, empty if cycle exists
        return result if len(result) == numCourses else []


# ============================================
# Solution 2: DFS Postorder
# Time: O(V + E), Space: O(V + E)
#   - Add node to result after all descendants processed
#   - Reverse at end for topological order
# ============================================
class SolutionDFS:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        WHITE, GRAY, BLACK = 0, 1, 2

        graph: List[List[int]] = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            graph[prereq].append(course)

        color: List[int] = [WHITE] * numCourses
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

        for node in range(numCourses):
            if color[node] == WHITE:
                dfs(node)
                if has_cycle:
                    return []

        return result[::-1]


def solve():
    """
    Input format (canonical JSON):
    Line 1: Integer numCourses
    Line 2: 2D array prerequisites (e.g. [[1,0],[2,1]])

    Output format:
    Array of integers representing course order
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    num_courses = int(lines[0])
    prerequisites = json.loads(lines[1]) if len(lines) > 1 else []

    solver = get_solver(SOLUTIONS)
    result = solver.findOrder(num_courses, prerequisites)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

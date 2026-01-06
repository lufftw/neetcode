# solutions/0207_course_schedule.py
"""
Problem: Course Schedule
Link: https://leetcode.com/problems/course-schedule/

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you
must take course bi first if you want to take course ai.

Return true if you can finish all courses. Otherwise, return false.

Example 1:
    Input: numCourses = 2, prerequisites = [[1,0]]
    Output: true
    Explanation: Take course 0, then course 1.

Example 2:
    Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
    Output: false
    Explanation: To take course 1 you should have finished course 0, and to take
    course 0 you should also have finished course 1. So it is impossible.

Constraints:
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= 5000
- prerequisites[i].length == 2
- 0 <= ai, bi < numCourses
- All the pairs prerequisites[i] are unique.

Topics: Depth-First Search, Breadth-First Search, Graph, Topological Sort
"""
from typing import List
from collections import deque
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Course Schedule solution."""
    import json

    # Normalize actual to boolean
    if isinstance(actual, str):
        actual = actual.lower() == 'true'

    # If expected is available, compare directly
    if expected is not None:
        if isinstance(expected, str):
            expected = expected.lower() == 'true'
        return actual == expected

    # Judge-only mode: compute expected using reference solution
    lines = input_data.strip().split('\n')
    num_courses = int(lines[0])
    prerequisites = json.loads(lines[1]) if len(lines) > 1 else []

    expected_result = _can_finish(num_courses, prerequisites)
    return actual == expected_result


def _can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    """Reference solution using Kahn's algorithm."""
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
        "method": "canFinish",
        "complexity": "O(V+E) time, O(V+E) space",
        "description": "Kahn's algorithm (BFS topological sort)",
        "api_kernels": ["TopologicalSort"],
        "patterns": ["topological_sort_cycle_detection"],
    },
    "dfs": {
        "class": "SolutionDFS",
        "method": "canFinish",
        "complexity": "O(V+E) time, O(V+E) space",
        "description": "DFS three-color cycle detection",
        "api_kernels": ["TopologicalSort"],
        "patterns": ["topological_sort_dfs"],
    },
}


# ============================================
# Solution 1: Kahn's Algorithm (BFS)
# Time: O(V + E), Space: O(V + E)
#   - Process nodes with in-degree 0
#   - If all nodes processed, no cycle exists
# ============================================
class SolutionKahn:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # Build adjacency list and in-degree array
        graph: List[List[int]] = [[] for _ in range(numCourses)]
        in_degree: List[int] = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1

        # Initialize queue with nodes having in-degree 0
        queue: deque[int] = deque([i for i in range(numCourses) if in_degree[i] == 0])
        visited = 0

        while queue:
            node = queue.popleft()
            visited += 1

            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # If all courses visited, no cycle exists
        return visited == numCourses


# ============================================
# Solution 2: DFS Three-Color
# Time: O(V + E), Space: O(V + E)
#   - WHITE: unvisited, GRAY: in progress, BLACK: done
#   - Back edge (GRAY -> GRAY) indicates cycle
# ============================================
class SolutionDFS:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        WHITE, GRAY, BLACK = 0, 1, 2

        graph: List[List[int]] = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            graph[prereq].append(course)

        color: List[int] = [WHITE] * numCourses

        def has_cycle(node: int) -> bool:
            if color[node] == GRAY:
                return True  # Back edge found
            if color[node] == BLACK:
                return False  # Already processed

            color[node] = GRAY

            for neighbor in graph[node]:
                if has_cycle(neighbor):
                    return True

            color[node] = BLACK
            return False

        # Check all components
        for node in range(numCourses):
            if color[node] == WHITE:
                if has_cycle(node):
                    return False

        return True


def solve():
    """
    Input format (canonical JSON):
    Line 1: Integer numCourses
    Line 2: 2D array prerequisites (e.g. [[1,0],[2,1]])

    Output format:
    Boolean: true/false
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    num_courses = int(lines[0])
    prerequisites = json.loads(lines[1]) if len(lines) > 1 else []

    solver = get_solver(SOLUTIONS)
    result = solver.canFinish(num_courses, prerequisites)

    print(str(result).lower())


if __name__ == "__main__":
    solve()

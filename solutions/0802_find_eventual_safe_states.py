# solutions/0802_find_eventual_safe_states.py
"""
Problem: Find Eventual Safe States
Link: https://leetcode.com/problems/find-eventual-safe-states/

There is a directed graph of n nodes with each node labeled from 0 to n - 1.
The graph is represented by a 0-indexed 2D integer array graph where graph[i]
is an integer array of nodes adjacent to node i.

A node is a terminal node if there are no outgoing edges. A node is a safe node
if every possible path starting from that node leads to a terminal node (or
another safe node).

Return an array containing all the safe nodes of the graph. The answer should
be sorted in ascending order.

Example 1:
    Input: graph = [[1,2],[2,3],[5],[0],[5],[],[]]
    Output: [2,4,5,6]
    Explanation: Nodes 5 and 6 are terminal nodes.
    Node 2 leads to node 5, so it's safe.
    Node 4 leads to node 5, so it's safe.
    Nodes 0, 1, 3 can reach each other in a cycle.

Example 2:
    Input: graph = [[1,2,3,4],[1,2],[3,4],[0,4],[]]
    Output: [4]

Constraints:
- n == graph.length
- 1 <= n <= 10^4
- 0 <= graph[i].length <= n
- 0 <= graph[i][j] <= n - 1
- graph[i] is sorted in a strictly increasing order.
- The graph may contain self-loops.
- The number of edges in the graph will be in the range [1, 4 * 10^4].

Topics: Depth-First Search, Breadth-First Search, Graph, Topological Sort
"""
from typing import List
from collections import deque
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Find Eventual Safe States solution."""
    import json

    # Parse actual result
    if isinstance(actual, str):
        actual = json.loads(actual)

    # If expected is available, compare directly
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return sorted(actual) == sorted(expected)

    # Judge-only mode: compute expected using reference solution
    graph = json.loads(input_data.strip())
    expected_result = _find_safe_nodes(graph)
    return sorted(actual) == sorted(expected_result)


def _find_safe_nodes(graph: List[List[int]]) -> List[int]:
    """Reference solution using DFS three-color."""
    n = len(graph)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

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


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDFS",
        "method": "eventualSafeNodes",
        "complexity": "O(V+E) time, O(V) space",
        "description": "DFS three-color safe node detection",
        "api_kernels": ["TopologicalSort"],
        "patterns": ["topological_sort_safe_states"],
    },
    "reverse_kahn": {
        "class": "SolutionReverseKahn",
        "method": "eventualSafeNodes",
        "complexity": "O(V+E) time, O(V+E) space",
        "description": "Reverse graph + Kahn's algorithm",
        "api_kernels": ["TopologicalSort"],
        "patterns": ["topological_sort_reverse_graph"],
    },
}


# ============================================
# Solution 1: DFS Three-Color
# Time: O(V + E), Space: O(V)
#   - Safe = reaches BLACK without encountering GRAY
#   - GRAY during traversal = in cycle
# ============================================
class SolutionDFS:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        n = len(graph)
        WHITE, GRAY, BLACK = 0, 1, 2
        color: List[int] = [WHITE] * n

        def is_safe(node: int) -> bool:
            if color[node] == GRAY:
                return False  # In cycle
            if color[node] == BLACK:
                return True  # Already verified safe

            color[node] = GRAY

            for neighbor in graph[node]:
                if not is_safe(neighbor):
                    return False  # Leads to cycle

            color[node] = BLACK
            return True

        return [node for node in range(n) if is_safe(node)]


# ============================================
# Solution 2: Reverse Graph + Kahn's
# Time: O(V + E), Space: O(V + E)
#   - Reverse edges: terminal nodes now have in-degree 0
#   - Propagate safety backwards via Kahn's
# ============================================
class SolutionReverseKahn:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
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


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array graph (e.g. [[1,2],[2,3],[5],[0],[5],[],[]])

    Output format:
    Array of safe node indices in ascending order
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    graph = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.eventualSafeNodes(graph)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

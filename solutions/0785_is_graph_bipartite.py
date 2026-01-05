# solutions/0785_is_graph_bipartite.py
"""
Problem: Is Graph Bipartite?
Link: https://leetcode.com/problems/is-graph-bipartite/

There is an undirected graph with n nodes, where each node is numbered between 0 and n - 1.
You are given a 2D array graph, where graph[u] is an array of nodes that node u is adjacent to.
More formally, for each v in graph[u], there is an undirected edge between node u and node v.
The graph has the following properties:

- There are no self-edges (graph[u] does not contain u).
- There are no parallel edges (graph[u] does not contain duplicate values).
- If v is in graph[u], then u is in graph[v] (the graph is undirected).
- The graph may not be connected, meaning there may be two nodes u and v such that there is
  no path between them.

A graph is bipartite if the nodes can be partitioned into two independent sets A and B such
that every edge in the graph connects a node in set A and a node in set B.

Return true if and only if it is bipartite.

Example 1:
    Input: graph = [[1,2,3],[0,2],[0,1,3],[0,2]]
    Output: false
    Explanation: There is no way to partition the nodes into two independent sets such that
    every edge connects a node in one and a node in the other.

Example 2:
    Input: graph = [[1,3],[0,2],[1,3],[0,2]]
    Output: true
    Explanation: We can partition the nodes into two sets: {0, 2} and {1, 3}.

Constraints:
- graph.length == n
- 1 <= n <= 100
- 0 <= graph[u].length < n
- 0 <= graph[u][i] <= n - 1
- graph[u] does not contain u.
- All the values of graph[u] are unique.
- If graph[u] contains v, then graph[v] contains u.

Topics: DFS, BFS, Union Find, Graph
"""
from typing import List
from collections import deque
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Is Graph Bipartite solution."""
    import json

    # Parse input
    graph = json.loads(input_data.strip())

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected using reference solution
    expected_result = _is_bipartite(graph)
    return actual == expected_result


def _is_bipartite(graph):
    """Reference solution for validation."""
    from collections import deque

    n = len(graph)
    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue
        queue = deque([start])
        color[start] = 0
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
    return True


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionBFS",
        "method": "isBipartite",
        "complexity": "O(V+E) time, O(V) space",
        "description": "BFS coloring approach",
        "api_kernels": ["GraphBFS"],
        "patterns": ["graph_bipartite"],
    },
    "dfs": {
        "class": "SolutionDFS",
        "method": "isBipartite",
        "complexity": "O(V+E) time, O(V) space",
        "description": "DFS coloring approach",
        "api_kernels": ["GraphDFS"],
        "patterns": ["graph_bipartite"],
    },
}


# ============================================
# Solution 1: BFS Coloring
# Time: O(V + E), Space: O(V)
#   - Alternate colors at each level
#   - If neighbor has same color → not bipartite
#   - Must check all components (graph may be disconnected)
# ============================================
class SolutionBFS:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        # -1 = uncolored, 0 = color A, 1 = color B
        color: List[int] = [-1] * n

        def bfs(start: int) -> bool:
            """BFS coloring from start node. Returns False if conflict."""
            queue: deque[int] = deque([start])
            color[start] = 0  # Start with color 0

            while queue:
                node = queue.popleft()

                for neighbor in graph[node]:
                    if color[neighbor] == -1:
                        # Uncolored: assign opposite color
                        color[neighbor] = 1 - color[node]
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:
                        # Same color as current node → conflict
                        return False

            return True

        # Check all components (graph may be disconnected)
        for node in range(n):
            if color[node] == -1:
                if not bfs(node):
                    return False

        return True


# ============================================
# Solution 2: DFS Coloring
# Time: O(V + E), Space: O(V)
#   - Recursive coloring approach
#   - Try to color node, check for conflicts
# ============================================
class SolutionDFS:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        color: List[int] = [-1] * n

        def dfs(node: int, c: int) -> bool:
            """Try to color node with color c. Returns False if conflict."""
            if color[node] != -1:
                return color[node] == c  # Check for conflict

            color[node] = c

            for neighbor in graph[node]:
                if not dfs(neighbor, 1 - c):
                    return False

            return True

        for node in range(n):
            if color[node] == -1:
                if not dfs(node, 0):
                    return False

        return True


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array graph (adjacency list)

    Output format:
    Boolean: true/false
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    graph = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.isBipartite(graph)

    print(str(result).lower())  # true/false format


if __name__ == "__main__":
    solve()

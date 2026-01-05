# solutions/1971_find_if_path_exists_in_graph.py
"""
Problem: Find if Path Exists in Graph
Link: https://leetcode.com/problems/find-if-path-exists-in-graph/

There is a bi-directional graph with n vertices, where each vertex is labeled from 0 to n - 1
(inclusive). The edges in the graph are represented as a 2D integer array edges, where each
edges[i] = [ui, vi] denotes a bi-directional edge between vertex ui and vertex vi. Every vertex
pair is connected by at most one edge, and no vertex has an edge to itself.

You want to determine if there is a valid path that exists from vertex source to vertex
destination.

Given edges and the integers n, source, and destination, return true if there is a valid path
from source to destination, or false otherwise.

Example 1:
    Input: n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2
    Output: true
    Explanation: There are two paths from vertex 0 to vertex 2:
    - 0 → 1 → 2
    - 0 → 2

Example 2:
    Input: n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5
    Output: false
    Explanation: There is no path from vertex 0 to vertex 5.

Constraints:
- 1 <= n <= 2 * 10^5
- 0 <= edges.length <= 2 * 10^5
- edges[i].length == 2
- 0 <= ui, vi <= n - 1
- ui != vi
- 0 <= source, destination <= n - 1
- There are no duplicate edges.
- There are no self edges.

Topics: DFS, BFS, Union Find, Graph
"""
from typing import List, Set, Dict
from collections import defaultdict, deque
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Find if Path Exists in Graph solution."""
    import json

    # Parse input
    lines = input_data.strip().split('\n')
    n = int(lines[0])
    edges = json.loads(lines[1])
    source = int(lines[2])
    destination = int(lines[3])

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected using Union-Find
    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu != pv:
            parent[pu] = pv

    expected_result = find(source) == find(destination)
    return actual == expected_result


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDFS",
        "method": "validPath",
        "complexity": "O(V+E) time, O(V+E) space",
        "description": "DFS reachability with early termination",
        "api_kernels": ["GraphDFS"],
        "patterns": ["graph_dfs_reachability"],
    },
    "bfs": {
        "class": "SolutionBFS",
        "method": "validPath",
        "complexity": "O(V+E) time, O(V+E) space",
        "description": "BFS reachability",
        "api_kernels": ["GraphBFS"],
        "patterns": ["graph_bfs_reachability"],
    },
    "union_find": {
        "class": "SolutionUnionFind",
        "method": "validPath",
        "complexity": "O(E*α(n)) time, O(V) space",
        "description": "Union-Find connectivity check",
        "api_kernels": ["UnionFind"],
        "patterns": ["union_find_connectivity"],
    },
}


# ============================================
# Solution 1: DFS Reachability
# Time: O(V + E), Space: O(V + E)
#   - Build adjacency list from edge list
#   - DFS from source with early termination
# ============================================
class SolutionDFS:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        if source == destination:
            return True

        # Build adjacency list
        graph: Dict[int, List[int]] = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)  # Undirected

        visited: Set[int] = set()

        def dfs(node: int) -> bool:
            if node == destination:
                return True

            visited.add(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True

            return False

        return dfs(source)


# ============================================
# Solution 2: BFS Reachability
# Time: O(V + E), Space: O(V + E)
#   - Iterative BFS with early termination
# ============================================
class SolutionBFS:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        if source == destination:
            return True

        graph: Dict[int, List[int]] = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        visited: Set[int] = {source}
        queue: deque[int] = deque([source])

        while queue:
            node = queue.popleft()

            for neighbor in graph[node]:
                if neighbor == destination:
                    return True
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return False


# ============================================
# Solution 3: Union-Find
# Time: O(E × α(n)), Space: O(V)
#   - Good for multiple queries
#   - α(n) is inverse Ackermann (effectively constant)
# ============================================
class SolutionUnionFind:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]

        def union(x: int, y: int) -> None:
            px, py = find(x), find(y)
            if px == py:
                return
            # Union by rank
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1

        # Union all edges
        for u, v in edges:
            union(u, v)

        # Check if same component
        return find(source) == find(destination)


def solve():
    """
    Input format (canonical JSON):
    Line 1: Integer n
    Line 2: 2D array edges
    Line 3: Integer source
    Line 4: Integer destination

    Output format:
    Boolean: true/false
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    n = int(lines[0])
    edges = json.loads(lines[1])
    source = int(lines[2])
    destination = int(lines[3])

    solver = get_solver(SOLUTIONS)
    result = solver.validPath(n, edges, source, destination)

    print(str(result).lower())  # true/false format


if __name__ == "__main__":
    solve()

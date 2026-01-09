# solutions/0684_redundant_connection.py
"""
Problem: Redundant Connection
Link: https://leetcode.com/problems/redundant-connection/

In this problem, a tree is an undirected graph that is connected and has no cycles.

You are given a graph that started as a tree with n nodes labeled from 1 to n, with one
additional edge added. The added edge has two different vertices chosen from 1 to n,
and was not an edge that already existed. The graph is represented as an array edges
of length n where edges[i] = [ai, bi] indicates that there is an edge between nodes ai
and bi in the graph.

Return an edge that can be removed so that the resulting graph is a tree of n nodes.
If there are multiple answers, return the answer that occurs last in the input.

Example 1:
    Input: edges = [[1,2],[1,3],[2,3]]
    Output: [2,3]

Example 2:
    Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
    Output: [1,4]

Constraints:
- n == edges.length
- 3 <= n <= 1000
- edges[i].length == 2
- 1 <= ai < bi <= edges.length
- ai != bi
- There are no repeated edges.
- The given graph is connected.

Topics: Depth-First Search, Breadth-First Search, Union Find, Graph
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Redundant Connection solution."""
    import json

    # Parse input
    edges = json.loads(input_data.strip())

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected
    expected_result = _find_redundant(edges)
    return actual == expected_result


def _find_redundant(edges):
    """Reference solution for validation."""
    n = len(edges)
    parent = list(range(n + 1))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return [u, v]
        parent[pv] = pu

    return []


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "findRedundantConnection",
        "complexity": "O(n × α(n)) time, O(n) space",
        "description": "Union-Find cycle detection",
        "api_kernels": ["UnionFindConnectivity"],
        "patterns": ["union_find_cycle_detection"],
    },
    "union_find": {
        "class": "Solution",
        "method": "findRedundantConnection",
        "complexity": "O(n × α(n)) time, O(n) space",
        "description": "Optimal: Union-Find with path compression",
    },
    "dfs": {
        "class": "SolutionDFS",
        "method": "findRedundantConnection",
        "complexity": "O(n²) time, O(n) space",
        "description": "DFS cycle detection - rebuild graph each edge",
    },
}


# ============================================
# Solution 1: Union-Find Cycle Detection
# Time: O(n × α(n)), Space: O(n)
# ============================================
class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        """
        Find the edge that creates a cycle in a tree with one extra edge.

        Core insight: Process edges in order. Before adding each edge, check if
        endpoints are already connected (same component). If yes, this edge would
        create a cycle — return it. Union-Find with path compression + rank gives
        near O(1) per operation.

        Invariant: After processing i edges, the Union-Find structure represents
        the forest formed by the first i edges that didn't create cycles.

        Args:
            edges: List of edges [u, v] in the graph

        Returns:
            The last edge that would create a cycle
        """
        n = len(edges)
        parent = list(range(n + 1))  # 1-indexed
        rank = [0] * (n + 1)

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> bool:
            px, py = find(x), find(y)
            if px == py:
                return False
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True

        for u, v in edges:
            if not union(u, v):
                return [u, v]

        return []


# ============================================
# Solution 2: DFS Cycle Detection
# Time: O(n²), Space: O(n)
# ============================================
class SolutionDFS:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        """
        Find redundant edge using DFS to detect cycles.

        Core insight: For each edge (u, v), check if u and v are already
        connected in the graph built so far. If they are, adding this edge
        creates a cycle. DFS checks connectivity.

        This is O(n²) because we do O(n) DFS for each of n edges.
        Union-Find is better but DFS shows the graph-thinking approach.

        Args:
            edges: List of edges [u, v] in the graph

        Returns:
            The last edge that would create a cycle
        """
        from collections import defaultdict

        graph = defaultdict(set)

        def has_path(source: int, target: int, visited: set) -> bool:
            """Check if there's a path from source to target using DFS."""
            if source == target:
                return True
            visited.add(source)
            for neighbor in graph[source]:
                if neighbor not in visited:
                    if has_path(neighbor, target, visited):
                        return True
            return False

        for u, v in edges:
            # Check if u and v are already connected
            if graph[u] and graph[v] and has_path(u, v, set()):
                return [u, v]
            # Add edge to graph
            graph[u].add(v)
            graph[v].add(u)

        return []


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array edges

    Output format:
    Array [u, v]: the redundant edge
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    edges = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.findRedundantConnection(edges)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

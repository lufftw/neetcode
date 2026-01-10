# solutions/0261_graph_valid_tree.py
"""
Problem: Graph Valid Tree
https://leetcode.com/problems/graph-valid-tree/

Given n nodes (0 to n-1) and undirected edges, determine if the graph
forms a valid tree.

Key insight: A tree has exactly n-1 edges, is connected, and has no cycles.
We can check either: (1) n-1 edges + all nodes reachable from node 0, or
(2) Union-Find detecting cycles while connecting all nodes.

Constraints:
- 1 <= n <= 2000
- 0 <= edges.length <= 5000
- edges[i].length == 2
- 0 <= ai, bi < n
- No duplicate edges, no self-loops
"""
import json
import sys
from collections import defaultdict
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionDFS",
        "method": "validTree",
        "complexity": "O(V + E) time, O(V + E) space",
        "description": "DFS checking connectivity and cycle-free",
    },
    "union_find": {
        "class": "SolutionUnionFind",
        "method": "validTree",
        "complexity": "O(V + E * α(V)) time, O(V) space",
        "description": "Union-Find detecting cycles during merge",
    },
}


class SolutionDFS:
    """
    DFS approach.

    WHY: A valid tree must have exactly n-1 edges (necessary for acyclic
    connected graph) and all nodes must be reachable (connected). We can
    verify both with DFS from any node.

    HOW: Quick check for n-1 edges first (if not, impossible to be a tree).
    Then DFS from node 0, tracking parent to avoid false cycle detection
    on undirected edges. If we visit all n nodes without revisiting any
    (except via parent), it's a valid tree.
    """

    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # Tree must have exactly n-1 edges
        if len(edges) != n - 1:
            return False

        # Build adjacency list
        adj = defaultdict(list)
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        # DFS to check all nodes reachable
        visited = set()

        def dfs(node: int, parent: int) -> bool:
            visited.add(node)
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue  # Skip edge back to parent
                if neighbor in visited:
                    return False  # Cycle detected
                if not dfs(neighbor, node):
                    return False
            return True

        # Start DFS from node 0
        if not dfs(0, -1):
            return False

        # All nodes must be visited
        return len(visited) == n


class SolutionUnionFind:
    """
    Union-Find approach.

    WHY: Union-Find efficiently tracks connected components. If adding an
    edge would connect two nodes already in the same component, that creates
    a cycle. For a valid tree, we need exactly n-1 successful unions (edges)
    resulting in one component.

    HOW: Initialize n disjoint sets. For each edge, if both endpoints share
    the same root, we'd create a cycle. Otherwise, union them. Finally,
    verify exactly n-1 edges created one connected component.
    """

    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # Tree must have exactly n-1 edges
        if len(edges) != n - 1:
            return False

        # Initialize Union-Find with path compression and rank
        parent = list(range(n))
        rank = [1] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]

        def union(x: int, y: int) -> bool:
            root_x, root_y = find(x), find(y)
            if root_x == root_y:
                return False  # Cycle detected
            # Union by rank
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1
            return True

        # Process all edges
        for a, b in edges:
            if not union(a, b):
                return False

        return True


def judge(actual, expected, input_data: str) -> bool:
    """Validate graph valid tree result."""
    if isinstance(actual, str):
        actual = json.loads(actual)

    lines = input_data.strip().split("\n")
    n = json.loads(lines[0])
    edges = json.loads(lines[1])
    expected_result = _is_valid_tree_ref(n, edges)

    return actual == expected_result


def _is_valid_tree_ref(n: int, edges: List[List[int]]) -> bool:
    """Reference implementation using DFS."""
    if len(edges) != n - 1:
        return False

    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor == parent:
                continue
            if neighbor in visited:
                return False
            if not dfs(neighbor, node):
                return False
        return True

    return dfs(0, -1) and len(visited) == n


JUDGE_FUNC = judge


def solve():
    lines = sys.stdin.read().strip().split("\n")
    n = json.loads(lines[0])
    edges = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.validTree(n, edges)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

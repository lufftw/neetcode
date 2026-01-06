# solutions/0547_number_of_provinces.py
"""
Problem: Number of Provinces
Link: https://leetcode.com/problems/number-of-provinces/

There are n cities. Some of them are connected, while some are not. If city a is connected directly
with city b, and city b is connected directly with city c, then city a is connected indirectly
with city c.

A province is a group of directly or indirectly connected cities and no other cities outside
of the group.

You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth
city are directly connected, and isConnected[i][j] = 0 otherwise.

Return the total number of provinces.

Example 1:
    Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
    Output: 2

Example 2:
    Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
    Output: 3

Constraints:
- 1 <= n <= 200
- n == isConnected.length
- n == isConnected[i].length
- isConnected[i][j] is 1 or 0.
- isConnected[i][i] == 1
- isConnected[i][j] == isConnected[j][i]

Topics: Depth-First Search, Breadth-First Search, Union Find, Graph
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Number of Provinces solution."""
    import json

    # Parse input
    isConnected = json.loads(input_data.strip())

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected
    expected_result = _find_circle_num(isConnected)
    return actual == expected_result


def _find_circle_num(isConnected):
    """Reference solution for validation."""
    n = len(isConnected)
    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    components = n
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                pi, pj = find(i), find(j)
                if pi != pj:
                    parent[pj] = pi
                    components -= 1

    return components


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionUnionFind",
        "method": "findCircleNum",
        "complexity": "O(n² × α(n)) time, O(n) space",
        "description": "Union-Find with path compression",
        "api_kernels": ["UnionFindConnectivity"],
        "patterns": ["union_find_connected_components"],
    },
    "dfs": {
        "class": "SolutionDFS",
        "method": "findCircleNum",
        "complexity": "O(n²) time, O(n) space",
        "description": "DFS flood fill",
        "api_kernels": ["GraphDFS"],
        "patterns": ["graph_dfs_connected_components"],
    },
}


# ============================================
# Solution 1: Union-Find
# Time: O(n² × α(n)), Space: O(n)
# ============================================
class SolutionUnionFind:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        parent = list(range(n))
        rank = [0] * n

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

        components = n
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j] == 1:
                    if union(i, j):
                        components -= 1

        return components


# ============================================
# Solution 2: DFS
# Time: O(n²), Space: O(n)
# ============================================
class SolutionDFS:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        visited = [False] * n

        def dfs(city: int) -> None:
            visited[city] = True
            for neighbor in range(n):
                if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                    dfs(neighbor)

        provinces = 0
        for city in range(n):
            if not visited[city]:
                dfs(city)
                provinces += 1

        return provinces


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array isConnected

    Output format:
    Integer: number of provinces
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    isConnected = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.findCircleNum(isConnected)

    print(result)


if __name__ == "__main__":
    solve()

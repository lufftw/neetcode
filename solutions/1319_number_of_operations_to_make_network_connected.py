# solutions/1319_number_of_operations_to_make_network_connected.py
"""
Problem: Number of Operations to Make Network Connected
Link: https://leetcode.com/problems/number-of-operations-to-make-network-connected/

There are n computers numbered from 0 to n - 1 connected by ethernet cables connections forming
a network where connections[i] = [ai, bi] represents a connection between computers ai and bi.
Any computer can reach any other computer directly or indirectly through the network.

You are given an initial computer network connections. You can extract certain cables between two
directly connected computers, and place them between any pair of disconnected computers to make
them directly connected.

Return the minimum number of times you need to do this in order to make all the computers connected.
If it is not possible, return -1.

Example 1:
    Input: n = 4, connections = [[0,1],[0,2],[1,2]]
    Output: 1
    Explanation: Remove cable between computer 1 and 2 and place between computers 1 and 3.

Example 2:
    Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]
    Output: 2

Example 3:
    Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]
    Output: -1
    Explanation: There are not enough cables.

Constraints:
- 1 <= n <= 10^5
- 1 <= connections.length <= min(n * (n - 1) / 2, 10^5)
- connections[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- There are no repeated connections.
- No two computers are connected by more than one cable.

Topics: Depth-First Search, Breadth-First Search, Union Find, Graph
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Network Connected solution."""
    import json

    # Parse input
    lines = input_data.strip().split('\n')
    n = int(lines[0])
    connections = json.loads(lines[1])

    # If expected is available, compare directly
    if expected is not None:
        return actual == expected

    # Judge-only mode: compute expected
    expected_result = _make_connected(n, connections)
    return actual == expected_result


def _make_connected(n, connections):
    """Reference solution for validation."""
    if len(connections) < n - 1:
        return -1

    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    components = n
    for a, b in connections:
        pa, pb = find(a), find(b)
        if pa != pb:
            parent[pb] = pa
            components -= 1

    return components - 1


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "makeConnected",
        "complexity": "O(E × α(n)) time, O(n) space",
        "description": "Union-Find component counting",
        "api_kernels": ["UnionFindConnectivity"],
        "patterns": ["union_find_connected_components"],
    },
}


# ============================================
# Solution 1: Union-Find Network Connectivity
# Time: O(E × α(n)), Space: O(n)
# ============================================
class Solution:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        """
        Minimum cables to move to connect all computers.

        Key Insight:
        - Need at least n-1 edges to connect n nodes
        - Redundant edges can be moved
        - Need (components - 1) moves to connect all
        """
        if len(connections) < n - 1:
            return -1

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
        for a, b in connections:
            if union(a, b):
                components -= 1

        return components - 1


def solve():
    """
    Input format (canonical JSON):
    Line 1: Integer n
    Line 2: 2D array connections

    Output format:
    Integer: minimum operations or -1
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    n = int(lines[0])
    connections = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.makeConnected(n, connections)

    print(result)


if __name__ == "__main__":
    solve()

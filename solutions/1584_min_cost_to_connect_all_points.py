"""
Problem: Min Cost to Connect All Points
Link: https://leetcode.com/problems/min-cost-to-connect-all-points/

You are given an array points representing integer coordinates of some points on
a 2D-plane, where points[i] = [xi, yi].

The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance
between them: |xi - xj| + |yi - yj|.

Return the minimum cost to make all points connected. All points are connected if
there is exactly one simple path between any two points.

Example 1:
    Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
    Output: 20
    Explanation: We can connect the points as follows to get minimum cost of 20.

Example 2:
    Input: points = [[3,12],[-2,5],[-4,1]]
    Output: 18

Constraints:
- 1 <= points.length <= 1000
- -10^6 <= xi, yi <= 10^6
- All pairs (xi, yi) are distinct.

Topics: Array, Union Find, Graph, Minimum Spanning Tree
"""

import json
import heapq
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionPrim",
        "method": "minCostConnectPoints",
        "complexity": "O(n^2 log n) time, O(n^2) space",
        "description": "Prim's algorithm using min-heap for MST construction",
    },
    "kruskal": {
        "class": "SolutionKruskal",
        "method": "minCostConnectPoints",
        "complexity": "O(n^2 log n) time, O(n^2) space",
        "description": "Kruskal's algorithm with Union-Find for MST",
    },
    "prim_optimized": {
        "class": "SolutionPrimOptimized",
        "method": "minCostConnectPoints",
        "complexity": "O(n^2) time, O(n) space",
        "description": "Prim's without heap - optimal for dense graphs",
    },
}


# ============================================================================
# Solution 1: Prim's Algorithm with Min-Heap
# Time: O(n^2 log n), Space: O(n^2) for edge storage, O(n) for visited set
#
# Key Insight:
#   This is a Minimum Spanning Tree (MST) problem on a complete graph where
#   each point is a node and the edge weight between any two points is their
#   Manhattan distance. Since the graph is complete (n^2 edges), we need an
#   efficient MST algorithm.
#
#   Prim's algorithm grows the MST by always adding the minimum-weight edge
#   that connects a visited node to an unvisited node.
#
# Algorithm:
#   - Start from node 0, add all its edges to min-heap
#   - Pop minimum edge, if destination unvisited:
#     - Add to MST, mark visited, add all edges from new node
#   - Repeat until all nodes visited
#
# Why This Works:
#   The greedy choice (smallest edge to unvisited node) is always safe because
#   any MST must include the minimum edge crossing the cut between visited
#   and unvisited vertices (Cut Property of MST).
# ============================================================================
class SolutionPrim:
    """
    Prim's MST algorithm using a min-heap priority queue.

    For complete graphs, Prim's is intuitive: we grow the tree one vertex
    at a time, always choosing the cheapest connection to an unconnected
    vertex. The heap ensures O(log n) extraction of minimum edges.
    """

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1:
            return 0

        def manhattan(i: int, j: int) -> int:
            return abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])

        # Min-heap: (cost, destination_node)
        # Start from node 0
        heap = [(0, 0)]
        visited = set()
        total_cost = 0

        while len(visited) < n:
            cost, node = heapq.heappop(heap)

            # Skip if already visited
            if node in visited:
                continue

            visited.add(node)
            total_cost += cost

            # Add edges to all unvisited neighbors
            for neighbor in range(n):
                if neighbor not in visited:
                    edge_cost = manhattan(node, neighbor)
                    heapq.heappush(heap, (edge_cost, neighbor))

        return total_cost


# ============================================================================
# Solution 2: Kruskal's Algorithm with Union-Find
# Time: O(n^2 log n), Space: O(n^2)
#
# Key Insight:
#   Kruskal's algorithm builds MST by processing edges in sorted order,
#   adding each edge if it doesn't create a cycle. Union-Find efficiently
#   detects cycles by tracking connected components.
#
# Algorithm:
#   - Generate all n*(n-1)/2 edges with their weights
#   - Sort edges by weight
#   - For each edge in sorted order:
#     - If endpoints in different components, add edge and union them
#     - Stop when we have n-1 edges (tree is complete)
#
# Trade-off vs Prim's:
#   Kruskal's requires storing and sorting all edges (O(n^2) space and
#   O(n^2 log n) sort time), but Union-Find operations are nearly O(1).
#   For complete graphs, Prim's with heap is often more practical.
# ============================================================================
class SolutionKruskal:
    """
    Kruskal's MST using Union-Find with path compression and union by rank.

    We process edges globally from smallest to largest, using Union-Find
    to efficiently determine if adding an edge would create a cycle.
    The algorithm terminates after adding n-1 edges.
    """

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1:
            return 0

        # Union-Find with path compression and union by rank
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]

        def union(x: int, y: int) -> bool:
            """Union two sets, return True if they were different sets."""
            px, py = find(x), find(y)
            if px == py:
                return False  # Already in same component (would create cycle)

            # Union by rank
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True

        # Generate all edges: (cost, node1, node2)
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                cost = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                edges.append((cost, i, j))

        # Sort by cost
        edges.sort()

        total_cost = 0
        edges_added = 0

        for cost, u, v in edges:
            if union(u, v):
                total_cost += cost
                edges_added += 1
                if edges_added == n - 1:  # MST complete
                    break

        return total_cost


# ============================================================================
# Solution 3: Optimized Prim's (No Heap)
# Time: O(n^2), Space: O(n)
#
# Key Insight:
#   For dense graphs (like complete graphs), using a min-heap in Prim's adds
#   O(log n) overhead per operation. Since we must examine all n^2 edges anyway,
#   we can achieve O(n^2) by using a simple array to track minimum distances.
#
# Algorithm:
#   - Maintain array min_dist[i] = minimum cost to connect node i to MST
#   - In each iteration, find unvisited node with smallest min_dist (O(n) scan)
#   - Add it to MST, update min_dist for all unvisited neighbors
#   - Repeat n-1 times
#
# Why O(n^2) is optimal for complete graphs:
#   Any MST algorithm must at least look at all edges once to verify minimality.
#   With n^2 edges, O(n^2) is the best we can achieve.
# ============================================================================
class SolutionPrimOptimized:
    """
    Prim's algorithm optimized for dense/complete graphs.

    Instead of a heap, we maintain an array of minimum distances to the
    growing MST. For complete graphs, the O(n) linear scan per iteration
    beats the O(log n) heap operations since we're updating O(n) edges anyway.
    """

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1:
            return 0

        def manhattan(i: int, j: int) -> int:
            return abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])

        # min_dist[i] = minimum cost edge from node i to any node in MST
        # Initialize with distance to node 0 (our starting point)
        min_dist = [manhattan(0, i) for i in range(n)]
        min_dist[0] = 0  # Node 0 is in MST

        in_mst = [False] * n
        in_mst[0] = True
        total_cost = 0

        # Add n-1 more nodes to complete MST
        for _ in range(n - 1):
            # Find unvisited node with minimum distance to MST
            min_cost = float("inf")
            next_node = -1

            for node in range(n):
                if not in_mst[node] and min_dist[node] < min_cost:
                    min_cost = min_dist[node]
                    next_node = node

            # Add next_node to MST
            in_mst[next_node] = True
            total_cost += min_cost

            # Update distances for remaining nodes
            for node in range(n):
                if not in_mst[node]:
                    dist = manhattan(next_node, node)
                    min_dist[node] = min(min_dist[node], dist)

        return total_cost


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: points as JSON 2D array

    Example:
        [[0,0],[2,2],[3,10],[5,2],[7,0]]
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    points = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.minCostConnectPoints(points)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

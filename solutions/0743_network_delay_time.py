# solutions/0743_network_delay_time.py
"""
Problem: Network Delay Time
Link: https://leetcode.com/problems/network-delay-time/

You are given a network of n nodes, labeled from 1 to n. You are given times,
a list of travel times as directed edges times[i] = (ui, vi, wi), where ui is
the source node, vi is the target node, and wi is the time it takes for a
signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes
for all the n nodes to receive the signal. If it is impossible for all the
n nodes to receive the signal, return -1.

Example 1:
    Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
    Output: 2

Example 2:
    Input: times = [[1,2,1]], n = 2, k = 1
    Output: 1

Example 3:
    Input: times = [[1,2,1]], n = 2, k = 2
    Output: -1

Constraints:
- 1 <= k <= n <= 100
- 1 <= times.length <= 6000
- times[i].length == 3
- 1 <= ui, vi <= n
- ui != vi
- 0 <= wi <= 100
- All the pairs (ui, vi) are unique.

Topics: Depth-First Search, Breadth-First Search, Graph, Heap, Shortest Path
"""
from typing import List, Dict, Tuple
from collections import defaultdict
from heapq import heappush, heappop
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Network Delay Time solution."""
    import json

    # Normalize actual
    if isinstance(actual, str):
        actual = int(actual)

    # If expected is available, compare directly
    if expected is not None:
        if isinstance(expected, str):
            expected = int(expected)
        return actual == expected

    # Judge-only mode: compute expected using reference solution
    lines = input_data.strip().split('\n')
    times = json.loads(lines[0])
    n = int(lines[1])
    k = int(lines[2])

    expected_result = _network_delay(times, n, k)
    return actual == expected_result


def _network_delay(times: List[List[int]], n: int, k: int) -> int:
    """Reference solution using Dijkstra."""
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = {}
    pq = [(0, k)]

    while pq:
        d, node = heappop(pq)
        if node in dist:
            continue
        dist[node] = d
        for neighbor, weight in graph[node]:
            if neighbor not in dist:
                heappush(pq, (d + weight, neighbor))

    if len(dist) != n:
        return -1
    return max(dist.values())


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDijkstra",
        "method": "networkDelayTime",
        "complexity": "O((V+E) log V) time, O(V+E) space",
        "description": "Dijkstra's algorithm with min-heap",
        "api_kernels": ["ShortestPath"],
        "patterns": ["shortest_path_dijkstra"],
    },
    "dijkstra": {
        "class": "SolutionDijkstra",
        "method": "networkDelayTime",
        "complexity": "O((V+E) log V) time, O(V+E) space",
        "description": "Optimal for sparse graphs with non-negative weights",
    },
    "bellman_ford": {
        "class": "SolutionBellmanFord",
        "method": "networkDelayTime",
        "complexity": "O(V × E) time, O(V) space",
        "description": "Edge relaxation - handles negative weights",
    },
}


# ============================================
# Solution: Dijkstra's Algorithm
# Time: O((V + E) log V), Space: O(V + E)
#   - Process each edge once
#   - Heap operations are O(log V)
# ============================================
class SolutionDijkstra:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        """
        Find minimum time for signal to reach all nodes from source k.

        Core insight: Dijkstra finds shortest paths from single source. Use min-heap
        to always process the node with smallest distance next. Once a node is popped,
        its distance is final (greedy property holds for non-negative weights).

        Invariant: dist[node] contains the shortest path distance for all finalized
        nodes; heap contains candidates with tentative distances.

        Args:
            times: Edge list [u, v, w] (source, target, weight)
            n: Number of nodes (1 to n)
            k: Source node to send signal from

        Returns:
            Maximum shortest path distance (time for last node), or -1 if unreachable
        """
        # Build adjacency list
        graph: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        # Dijkstra's algorithm
        dist: Dict[int, int] = {}
        pq: List[Tuple[int, int]] = [(0, k)]  # (distance, node)

        while pq:
            d, node = heappop(pq)

            if node in dist:
                continue  # Already processed

            dist[node] = d

            for neighbor, weight in graph[node]:
                if neighbor not in dist:
                    heappush(pq, (d + weight, neighbor))

        # Check if all nodes reachable
        if len(dist) != n:
            return -1

        return max(dist.values())


# ============================================
# Solution 2: Bellman-Ford Algorithm
# Time: O(V × E), Space: O(V)
# ============================================
class SolutionBellmanFord:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        """
        Find minimum time using Bellman-Ford algorithm.

        Core insight: Relax all edges V-1 times. After i iterations, dist[v]
        contains shortest path using at most i edges. Works with negative
        weights (unlike Dijkstra), though this problem has non-negative weights.

        Bellman-Ford is slower than Dijkstra for this problem but is important
        to know as it handles negative edge weights and can detect negative cycles.

        Args:
            times: Edge list [u, v, w] (source, target, weight)
            n: Number of nodes (1 to n)
            k: Source node to send signal from

        Returns:
            Maximum shortest path distance, or -1 if unreachable
        """
        # Initialize distances
        INF = float('inf')
        dist = [INF] * (n + 1)
        dist[k] = 0

        # Relax all edges V-1 times
        for _ in range(n - 1):
            updated = False
            for u, v, w in times:
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
            # Early termination if no updates
            if not updated:
                break

        # Find maximum distance (excluding dist[0] which is unused)
        max_dist = max(dist[1:])

        return max_dist if max_dist != INF else -1


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array times (e.g. [[2,1,1],[2,3,1],[3,4,1]])
    Line 2: Integer n
    Line 3: Integer k

    Output format:
    Integer: minimum time for all nodes to receive signal
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    times = json.loads(lines[0])
    n = int(lines[1])
    k = int(lines[2])

    solver = get_solver(SOLUTIONS)
    result = solver.networkDelayTime(times, n, k)

    print(result)


if __name__ == "__main__":
    solve()

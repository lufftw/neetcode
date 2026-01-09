# solutions/0787_cheapest_flights_within_k_stops.py
"""
Problem: Cheapest Flights Within K Stops
Link: https://leetcode.com/problems/cheapest-flights-within-k-stops/

There are n cities connected by some number of flights. You are given an array
flights where flights[i] = [fromi, toi, pricei] indicates that there is a flight
from city fromi to city toi with cost pricei.

You are also given three integers src, dst, and k, return the cheapest price
from src to dst with at most k stops. If there is no such route, return -1.

Example 1:
    Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]],
           src = 0, dst = 3, k = 1
    Output: 700
    Explanation: The optimal path with at most 1 stop is 0 -> 1 -> 3 with cost 700.

Example 2:
    Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1
    Output: 200

Example 3:
    Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0
    Output: 500

Constraints:
- 1 <= n <= 100
- 0 <= flights.length <= (n * (n - 1) / 2)
- flights[i].length == 3
- 0 <= fromi, toi < n
- fromi != toi
- 1 <= pricei <= 10^4
- 0 <= src, dst, k < n
- src != dst

Topics: Dynamic Programming, DFS, BFS, Graph, Heap, Shortest Path
"""
from typing import List, Dict, Tuple
from collections import defaultdict
from heapq import heappush, heappop
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Cheapest Flights solution."""
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
    n = int(lines[0])
    flights = json.loads(lines[1])
    src = int(lines[2])
    dst = int(lines[3])
    k = int(lines[4])

    expected_result = _cheapest_flight(n, flights, src, dst, k)
    return actual == expected_result


def _cheapest_flight(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """Reference solution using Bellman-Ford."""
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0

    for _ in range(k + 1):
        new_dist = dist.copy()
        for u, v, price in flights:
            if dist[u] != INF:
                new_dist[v] = min(new_dist[v], dist[u] + price)
        dist = new_dist

    return dist[dst] if dist[dst] != INF else -1


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionBellmanFord",
        "method": "findCheapestPrice",
        "complexity": "O(K*E) time, O(N) space",
        "description": "Bellman-Ford with K iterations",
        "api_kernels": ["ShortestPath"],
        "patterns": ["shortest_path_bellman_ford"],
    },
    "dijkstra": {
        "class": "SolutionDijkstra",
        "method": "findCheapestPrice",
        "complexity": "O(E*K log(E*K)) time, O(N*K) space",
        "description": "Modified Dijkstra with stops tracking",
        "api_kernels": ["ShortestPath"],
        "patterns": ["shortest_path_dijkstra_constrained"],
    },
}


# ============================================
# Solution 1: Bellman-Ford (K iterations)
# Time: O(K * E), Space: O(N)
#   - Relax all edges k+1 times
#   - Each iteration extends paths by one edge
# ============================================
class SolutionBellmanFord:
    def findCheapestPrice(self, n: int, flights: List[List[int]],
                          src: int, dst: int, k: int) -> int:
        """
        Find cheapest flight from src to dst with at most k stops.

        Core insight: Bellman-Ford naturally handles the k-stop constraint. Each
        iteration relaxes all edges, extending shortest paths by one hop. After
        k+1 iterations, we have shortest paths using at most k+1 edges (k stops).

        Invariant: After i iterations, dist[v] is the minimum cost to reach v
        using at most i edges.

        Args:
            n: Number of cities
            flights: Edge list [from, to, price]
            src: Source city
            dst: Destination city
            k: Maximum number of intermediate stops

        Returns:
            Minimum cost, or -1 if no valid route
        """
        INF = float('inf')
        dist: List[float] = [INF] * n
        dist[src] = 0

        # Relax edges k+1 times (k stops = k+1 edges)
        for _ in range(k + 1):
            # Use copy to avoid using updated values in same iteration
            new_dist = dist.copy()

            for u, v, price in flights:
                if dist[u] != INF:
                    new_dist[v] = min(new_dist[v], dist[u] + price)

            dist = new_dist

        return int(dist[dst]) if dist[dst] != INF else -1


# ============================================
# Solution 2: Modified Dijkstra
# Time: O(E*K log(E*K)), Space: O(N*K)
#   - Track (cost, node, stops_used) as state
#   - Different stop counts are different states
# ============================================
class SolutionDijkstra:
    def findCheapestPrice(self, n: int, flights: List[List[int]],
                          src: int, dst: int, k: int) -> int:
        # Build graph
        graph: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
        for u, v, price in flights:
            graph[u].append((v, price))

        # Track minimum cost for each (node, stops) state
        dist: Dict[Tuple[int, int], int] = {}

        # (cost, node, stops_used)
        pq: List[Tuple[int, int, int]] = [(0, src, 0)]

        while pq:
            cost, node, stops = heappop(pq)

            if node == dst:
                return cost

            if stops > k:
                continue  # Too many stops

            if (node, stops) in dist and dist[(node, stops)] <= cost:
                continue

            dist[(node, stops)] = cost

            for neighbor, price in graph[node]:
                new_cost = cost + price
                new_stops = stops + 1

                if (neighbor, new_stops) not in dist:
                    heappush(pq, (new_cost, neighbor, new_stops))

        return -1


def solve():
    """
    Input format (canonical JSON):
    Line 1: Integer n
    Line 2: 2D array flights
    Line 3: Integer src
    Line 4: Integer dst
    Line 5: Integer k

    Output format:
    Integer: cheapest price or -1
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    n = int(lines[0])
    flights = json.loads(lines[1])
    src = int(lines[2])
    dst = int(lines[3])
    k = int(lines[4])

    solver = get_solver(SOLUTIONS)
    result = solver.findCheapestPrice(n, flights, src, dst, k)

    print(result)


if __name__ == "__main__":
    solve()

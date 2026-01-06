# solutions/0847_shortest_path_visiting_all_nodes.py
"""
Problem: Shortest Path Visiting All Nodes
Link: https://leetcode.com/problems/shortest-path-visiting-all-nodes/

You have an undirected, connected graph of n nodes labeled from 0 to n - 1.
You are given an array graph where graph[i] is a list of all the nodes connected
with node i by an edge.

Return the length of the shortest path that visits every node. You may start
and stop at any node, you may revisit nodes multiple times, and you may reuse edges.

Example 1:
    Input: graph = [[1,2,3],[0],[0],[0]]
    Output: 4
    Explanation: One possible path is [1,0,2,0,3]

Example 2:
    Input: graph = [[1],[0,2,4],[1,3,4],[2],[1,2]]
    Output: 4
    Explanation: One possible path is [0,1,4,2,3]

Constraints:
- n == graph.length
- 1 <= n <= 12
- 0 <= graph[i].length < n
- graph[i] does not contain i.
- If graph[a] contains b, then graph[b] contains a.
- The input graph is always connected.

Topics: Dynamic Programming, Bit Manipulation, Breadth-First Search, Graph
"""
from typing import List
from collections import deque
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "shortestPathLength",
        "complexity": "O(n × 2^n) time, O(n × 2^n) space",
        "description": "BFS with bitmask state (node, visited_mask)",
    },
}


# ============================================================================
# Solution: BFS with Bitmask State
# Time: O(n × 2^n) - n nodes × 2^n possible masks
# Space: O(n × 2^n) - visited states
#
# Key Insight:
#   - State = (current_node, set_of_visited_nodes)
#   - Use bitmask to represent visited set efficiently
#   - BFS guarantees shortest path (all edges have weight 1)
#   - Start from ALL nodes simultaneously (multi-source BFS)
# ============================================================================
class Solution:
    def shortestPathLength(self, graph: List[List[int]]) -> int:
        """
        Find shortest path visiting all nodes using BFS with bitmask state.

        The key insight is that we need to track:
        1. Which node we're currently at
        2. Which nodes we've visited so far (as a bitmask)

        State: (node, visited_mask)

        We use multi-source BFS, starting from every node simultaneously,
        because we're allowed to start anywhere.

        Time: O(n × 2^n) - each state visited once
        Space: O(n × 2^n) - for visited set and queue
        """
        n = len(graph)

        # Edge case: single node
        if n == 1:
            return 0

        # Full mask: all nodes visited
        full_mask = (1 << n) - 1

        # Queue: (node, visited_mask, distance)
        queue = deque()

        # Visited set: (node, mask) pairs
        visited = set()

        # Multi-source BFS: start from every node
        for i in range(n):
            initial_mask = 1 << i  # Only node i visited
            state = (i, initial_mask)
            queue.append((i, initial_mask, 0))
            visited.add(state)

        # BFS
        while queue:
            node, mask, dist = queue.popleft()

            # Explore neighbors
            for neighbor in graph[node]:
                # Update visited mask (add neighbor)
                new_mask = mask | (1 << neighbor)

                # Check if we've visited all nodes
                if new_mask == full_mask:
                    return dist + 1

                # Add to queue if not visited
                state = (neighbor, new_mask)
                if state not in visited:
                    visited.add(state)
                    queue.append((neighbor, new_mask, dist + 1))

        # Should never reach here for connected graph
        return -1


def solve():
    """
    Input format:
    Line 1: graph (JSON array of arrays)

    Example:
    [[1,2,3],[0],[0],[0]]
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    graph = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.shortestPathLength(graph)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

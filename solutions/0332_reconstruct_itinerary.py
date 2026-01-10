"""
Problem: Reconstruct Itinerary
Link: https://leetcode.com/problems/reconstruct-itinerary/

You are given a list of airline tickets where tickets[i] = [fromi, toi] represent
the departure and arrival airports of one flight. Reconstruct the itinerary in
order and return it.

All of the tickets belong to a man who departs from "JFK", thus, the itinerary
must begin with "JFK". If there are multiple valid itineraries, you should return
the itinerary that has the smallest lexical order when read as a single string.

You may assume all tickets form at least one valid itinerary. You must use all
the tickets once and only once.

Example 1:
    Input: tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
    Output: ["JFK","MUC","LHR","SFO","SJC"]

Example 2:
    Input: tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
    Output: ["JFK","ATL","JFK","SFO","ATL","SFO"]
    Explanation: Another possible reconstruction is ["JFK","SFO","ATL","JFK","ATL","SFO"]
                 but it is larger in lexical order.

Constraints:
- 1 <= tickets.length <= 300
- tickets[i].length == 2
- fromi.length == 3
- toi.length == 3
- fromi and toi consist of uppercase English letters.
- fromi != toi

Topics: Depth-First Search, Graph, Eulerian Circuit
"""

import json
from typing import List, Dict
from collections import defaultdict
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionHierholzer",
        "method": "findItinerary",
        "complexity": "O(E log E) time, O(E) space",
        "description": "Hierholzer's algorithm for Eulerian path, reverse post-order DFS",
    },
    "iterative": {
        "class": "SolutionIterative",
        "method": "findItinerary",
        "complexity": "O(E log E) time, O(E) space",
        "description": "Iterative version using explicit stack",
    },
}


# ============================================================================
# Solution 1: Hierholzer's Algorithm (Recursive DFS)
# Time: O(E log E) for sorting edges, O(E) for traversal
# Space: O(E) for adjacency list and result
#
# Key Insight:
#   This problem asks for an Eulerian path: a path that visits every edge
#   exactly once. Hierholzer's algorithm finds such a path by:
#   1. Start at the designated source (JFK)
#   2. Greedily follow edges (smallest lexicographically), removing used edges
#   3. When stuck (no outgoing edges), backtrack and add current node to path
#   4. The path is built in reverse order
#
# Why Reverse Post-Order:
#   When we hit a dead end in an Eulerian path, that node must be the final
#   destination (or we'd have unused edges). By adding nodes in post-order
#   (after all their edges are used), we build the path backwards.
#
# Lexicographic Ordering:
#   By sorting destinations and always picking the smallest available next
#   destination, we ensure the lexicographically smallest valid itinerary.
# ============================================================================
class SolutionHierholzer:
    """
    Hierholzer's algorithm for Eulerian path finding.

    The key insight is that an Eulerian path visits every edge exactly once.
    We use DFS with post-order collection: when a node has no more outgoing
    edges, it becomes part of the path (added to front). Sorting adjacency
    lists ensures lexicographically smallest result.
    """

    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # Build adjacency list with sorted destinations (reversed for pop efficiency)
        graph: Dict[str, List[str]] = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):
            graph[src].append(dst)

        result = []

        def dfs(airport: str) -> None:
            # Visit all destinations from this airport
            while graph[airport]:
                # Pop the smallest destination (list is reverse-sorted)
                next_airport = graph[airport].pop()
                dfs(next_airport)
            # Post-order: add to result when no more outgoing edges
            result.append(airport)

        dfs("JFK")

        # Result is built in reverse order
        return result[::-1]


# ============================================================================
# Solution 2: Iterative with Explicit Stack
# Time: O(E log E), Space: O(E)
#
# Key Insight:
#   Same algorithm as recursive, but using an explicit stack to avoid
#   potential stack overflow on deep recursion. This is useful for very
#   long itineraries.
#
# The stack simulates the call stack of the recursive DFS. When we can't
# proceed (no outgoing edges), we pop and add to the result path.
# ============================================================================
class SolutionIterative:
    """
    Iterative Hierholzer's algorithm using explicit stack.

    Avoids recursion depth issues while maintaining the same logic:
    explore greedily, backtrack when stuck, build path in reverse.
    """

    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # Build adjacency list with sorted destinations (reversed for pop)
        graph: Dict[str, List[str]] = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):
            graph[src].append(dst)

        result = []
        stack = ["JFK"]

        while stack:
            # Peek at current airport
            current = stack[-1]

            if graph[current]:
                # There are still edges to explore
                next_airport = graph[current].pop()
                stack.append(next_airport)
            else:
                # No more edges, add to result (post-order)
                result.append(stack.pop())

        # Result is built in reverse order
        return result[::-1]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: tickets as JSON 2D array

    Example:
        [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    tickets = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.findItinerary(tickets)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

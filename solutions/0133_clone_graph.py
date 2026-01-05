# solutions/0133_clone_graph.py
"""
Problem: Clone Graph
Link: https://leetcode.com/problems/clone-graph/

Given a reference of a node in a connected undirected graph.
Return a deep copy (clone) of the graph.

Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

class Node {
    public int val;
    public List<Node> neighbors;
}

Test case format:
For simplicity, each node's value is the same as the node's index (1-indexed).
For example, the first node with val == 1, the second node with val == 2, and so on.
The graph is represented in the test case using an adjacency list.

An adjacency list is a collection of unordered lists used to represent a finite graph.
Each list describes the set of neighbors of a node in the graph.

The given node will always be the first node with val = 1.
You must return the copy of the given node as a reference to the cloned graph.

Example 1:
    Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
    Output: [[2,4],[1,3],[2,4],[1,3]]
    Explanation: There are 4 nodes in the graph.
    1st node (val = 1)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
    2nd node (val = 2)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
    3rd node (val = 3)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
    4th node (val = 4)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).

Example 2:
    Input: adjList = [[]]
    Output: [[]]
    Explanation: Note that the input contains one empty list. The graph consists of only one node with val = 1 and it does not have any neighbors.

Example 3:
    Input: adjList = []
    Output: []
    Explanation: This an empty graph, it does not have any nodes.

Constraints:
- The number of nodes in the graph is in the range [0, 100].
- 1 <= Node.val <= 100
- Node.val is unique for each node.
- There are no repeated edges and no self-loops in the graph.
- The Graph is connected and all nodes can be visited starting from the given node.

Topics: Hash Table, DFS, BFS, Graph
"""
from typing import Optional, Dict
from collections import deque
from _runner import get_solver


# Definition for a Node.
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionDFS",
        "method": "cloneGraph",
        "complexity": "O(V+E) time, O(V) space",
        "description": "DFS with hash map",
        "api_kernels": ["GraphDFS"],
        "patterns": ["graph_clone"],
    },
    "bfs": {
        "class": "SolutionBFS",
        "method": "cloneGraph",
        "complexity": "O(V+E) time, O(V) space",
        "description": "BFS with hash map",
        "api_kernels": ["GraphBFS"],
        "patterns": ["graph_clone"],
    },
}


# ============================================
# Solution 1: DFS with Hash Map
# Time: O(V + E), Space: O(V)
#   - Map: original node → cloned node
#   - On first visit: create clone and add to map
#   - On subsequent visits: return existing clone from map
# ============================================
class SolutionDFS:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None

        # Map: original node → cloned node
        old_to_new: Dict[Node, Node] = {}

        def dfs(original: Node) -> Node:
            # If already cloned, return the clone
            if original in old_to_new:
                return old_to_new[original]

            # Create clone (without neighbors yet)
            clone = Node(original.val)
            old_to_new[original] = clone

            # Clone all neighbors recursively
            for neighbor in original.neighbors:
                clone.neighbors.append(dfs(neighbor))

            return clone

        return dfs(node)


# ============================================
# Solution 2: BFS with Hash Map
# Time: O(V + E), Space: O(V)
#   - Iterative approach using queue
#   - Create clone when first discovered
#   - Add neighbor references when processing
# ============================================
class SolutionBFS:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None

        old_to_new: Dict[Node, Node] = {node: Node(node.val)}
        queue: deque[Node] = deque([node])

        while queue:
            original = queue.popleft()

            for neighbor in original.neighbors:
                if neighbor not in old_to_new:
                    # Create clone and add to map
                    old_to_new[neighbor] = Node(neighbor.val)
                    queue.append(neighbor)

                # Add cloned neighbor to cloned node's neighbors
                old_to_new[original].neighbors.append(old_to_new[neighbor])

        return old_to_new[node]


def _build_graph(adj_list):
    """Build graph from adjacency list."""
    if not adj_list:
        return None

    nodes = [Node(i + 1) for i in range(len(adj_list))]
    for i, neighbors in enumerate(adj_list):
        nodes[i].neighbors = [nodes[j - 1] for j in neighbors]

    return nodes[0] if nodes else None


def _graph_to_adj_list(node):
    """Convert graph back to adjacency list."""
    if not node:
        return []

    result = {}
    visited = set()
    queue = deque([node])
    visited.add(node.val)

    while queue:
        curr = queue.popleft()
        result[curr.val] = sorted([n.val for n in curr.neighbors])
        for neighbor in curr.neighbors:
            if neighbor.val not in visited:
                visited.add(neighbor.val)
                queue.append(neighbor)

    return [result[i] for i in range(1, len(result) + 1)]


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array adjacency list (e.g. [[2,4],[1,3],[2,4],[1,3]])

    Output format:
    2D array adjacency list of cloned graph
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    adj_list = json.loads(lines[0])
    node = _build_graph(adj_list)

    solver = get_solver(SOLUTIONS)
    cloned = solver.cloneGraph(node)

    result = _graph_to_adj_list(cloned)
    print(json.dumps(result))


if __name__ == "__main__":
    solve()

# generators/0133_clone_graph.py
"""
Test Case Generator for Problem 0133 - Clone Graph

LeetCode Constraints:
- The number of nodes in the graph is in the range [0, 100]
- 1 <= Node.val <= 100
- Node.val is unique for each node
- There are no repeated edges and no self-loops
- The graph is connected and all nodes can be visited starting from the given node
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Clone Graph.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Adjacency list in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first (adjacency list format - 1-indexed neighbors)
    edge_cases = [
        [[2, 4], [1, 3], [2, 4], [1, 3]],  # Classic 4-node square
        [[]],  # Single node with no neighbors
        [],  # Empty graph
        [[2], [1]],  # Two connected nodes
        [[2, 3], [1, 3], [1, 2]],  # Triangle
    ]

    for adj_list in edge_cases:
        yield json.dumps(adj_list, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random connected graph."""
    n = random.randint(1, 50)

    # Build adjacency list (1-indexed for LeetCode format)
    adj_list: List[List[int]] = [[] for _ in range(n)]

    # First ensure connectivity with a spanning tree
    for i in range(1, n):
        parent = random.randint(0, i - 1)
        # Convert to 1-indexed
        adj_list[parent].append(i + 1)
        adj_list[i].append(parent + 1)

    # Add some extra edges
    num_extra = random.randint(0, min(n, 20))
    for _ in range(num_extra):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (v + 1) not in adj_list[u]:
            adj_list[u].append(v + 1)
            adj_list[v].append(u + 1)

    return json.dumps(adj_list, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size.

    Args:
        n: Number of nodes

    Returns:
        str: Adjacency list with n nodes
    """
    n = max(1, min(100, n))
    adj_list: List[List[int]] = [[] for _ in range(n)]

    for i in range(1, n):
        parent = random.randint(0, i - 1)
        adj_list[parent].append(i + 1)
        adj_list[i].append(parent + 1)

    return json.dumps(adj_list, separators=(',', ':'))

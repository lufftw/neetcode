# generators/0785_is_graph_bipartite.py
"""
Test Case Generator for Problem 0785 - Is Graph Bipartite?

LeetCode Constraints:
- graph.length == n
- 1 <= n <= 100
- 0 <= graph[u].length < n
- 0 <= graph[u][i] <= n - 1
- graph[u] does not contain u
- All values of graph[u] are unique
- If graph[u] contains v, then graph[v] contains u
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Is Graph Bipartite.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Adjacency list in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]],  # Not bipartite (odd cycle)
        [[1, 3], [0, 2], [1, 3], [0, 2]],  # Bipartite (even cycle)
        [[]],  # Single isolated node
        [[1], [0]],  # Two connected nodes
        [[], []],  # Two isolated nodes
        [[1], [0, 2], [1]],  # Line graph (bipartite)
    ]

    for graph in edge_cases:
        yield json.dumps(graph, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    n = random.randint(1, 50)

    # Randomly decide if we want bipartite or not
    if random.random() < 0.5:
        return _generate_bipartite_graph(n)
    else:
        return _generate_random_graph(n)


def _generate_bipartite_graph(n: int) -> str:
    """Generate a bipartite graph (guaranteed bipartite)."""
    # Split nodes into two sets
    set_a = list(range(n // 2))
    set_b = list(range(n // 2, n))

    if not set_b:
        set_b = set_a  # Handle n=1

    graph: List[List[int]] = [[] for _ in range(n)]

    # Add edges only between sets
    num_edges = random.randint(0, min(n * 2, len(set_a) * len(set_b)))

    for _ in range(num_edges):
        if set_a and set_b:
            u = random.choice(set_a)
            v = random.choice(set_b)
            if v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)

    return json.dumps(graph, separators=(',', ':'))


def _generate_random_graph(n: int) -> str:
    """Generate a random graph (may or may not be bipartite)."""
    graph: List[List[int]] = [[] for _ in range(n)]

    # Add random edges
    num_edges = random.randint(0, n * 2)

    for _ in range(num_edges):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and v not in graph[u]:
            graph[u].append(v)
            graph[v].append(u)

    return json.dumps(graph, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size.

    Args:
        n: Number of nodes

    Returns:
        str: Graph with n nodes
    """
    return _generate_bipartite_graph(max(1, n))

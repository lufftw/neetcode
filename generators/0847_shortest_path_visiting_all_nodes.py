# generators/0847_shortest_path_visiting_all_nodes.py
"""
Random test generator for LC 847: Shortest Path Visiting All Nodes

Constraints:
- n == graph.length
- 1 <= n <= 12
- 0 <= graph[i].length < n
- graph[i] does not contain i
- The graph is connected and undirected
"""
import random
import json
from typing import Iterator, Optional


def generate_connected_graph(n: int) -> list:
    """
    Generate a random connected undirected graph.

    Strategy:
    1. Create a spanning tree to ensure connectivity
    2. Add random additional edges
    """
    # Adjacency list
    adj = [[] for _ in range(n)]

    if n == 1:
        return adj

    # Step 1: Create spanning tree (ensures connectivity)
    # Shuffle nodes and connect each to a random predecessor
    nodes = list(range(n))
    random.shuffle(nodes)

    for i in range(1, n):
        # Connect node nodes[i] to some node in nodes[0:i]
        parent = nodes[random.randint(0, i - 1)]
        child = nodes[i]
        adj[parent].append(child)
        adj[child].append(parent)

    # Step 2: Add random extra edges (up to n more)
    # Use a set to track existing edges
    edges = set()
    for u in range(n):
        for v in adj[u]:
            if u < v:
                edges.add((u, v))

    extra_edges = random.randint(0, n)
    for _ in range(extra_edges):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (min(u, v), max(u, v)) not in edges:
            edges.add((min(u, v), max(u, v)))
            adj[u].append(v)
            adj[v].append(u)

    return adj


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test cases for Shortest Path Visiting All Nodes.

    Yields test input strings in the format:
        [[neighbors_0], [neighbors_1], ...]
    """
    if seed is not None:
        random.seed(seed)

    for _ in range(count):
        # Random number of nodes (1 to 12, but prefer smaller for test speed)
        n = random.randint(1, 8)

        graph = generate_connected_graph(n)

        yield json.dumps(graph, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.

    Args:
        n: Number of nodes

    Returns:
        Test input string
    """
    # Cap n at 12 per constraints
    n = min(n, 12)

    graph = generate_connected_graph(n)

    return json.dumps(graph, separators=(',', ':'))


if __name__ == "__main__":
    # Test the generator
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")

    print("\nComplexity test (n=10):")
    print(generate_for_complexity(10))

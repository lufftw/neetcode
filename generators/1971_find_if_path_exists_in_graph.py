# generators/1971_find_if_path_exists_in_graph.py
"""
Test Case Generator for Problem 1971 - Find if Path Exists in Graph

LeetCode Constraints:
- 1 <= n <= 2 * 10^5
- 0 <= edges.length <= 2 * 10^5
- edges[i].length == 2
- 0 <= ui, vi <= n - 1
- ui != vi
- 0 <= source, destination <= n - 1
- No duplicate edges
- No self edges
"""
import json
import random
from typing import Iterator, Optional, List, Tuple


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Find if Path Exists in Graph.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: n, edges, source, destination in newline-separated format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        (3, [[0, 1], [1, 2], [2, 0]], 0, 2),  # Cycle, path exists
        (6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5),  # Disconnected
        (1, [], 0, 0),  # Single node, same source/dest
        (2, [[0, 1]], 0, 1),  # Two nodes connected
        (2, [], 0, 1),  # Two nodes disconnected
        (4, [[0, 1], [1, 2], [2, 3]], 0, 3),  # Linear path
    ]

    for n, edges, src, dst in edge_cases:
        yield _format_case(n, edges, src, dst)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _format_case(n: int, edges: List[List[int]], source: int, destination: int) -> str:
    """Format a test case as expected by solve()."""
    return f"{n}\n{json.dumps(edges, separators=(',', ':'))}\n{source}\n{destination}"


def _generate_case() -> str:
    """Generate a single random test case."""
    n = random.randint(1, 1000)

    # Decide if we want connected components or not
    connected = random.random() < 0.5

    if connected:
        edges = _generate_connected_graph(n)
        source = random.randint(0, n - 1)
        destination = random.randint(0, n - 1)
    else:
        edges = _generate_random_graph(n)
        source = random.randint(0, n - 1)
        destination = random.randint(0, n - 1)

    return _format_case(n, edges, source, destination)


def _generate_connected_graph(n: int) -> List[List[int]]:
    """Generate a connected graph (spanning tree + random edges)."""
    edges: List[List[int]] = []
    edge_set: set[Tuple[int, int]] = set()

    # Build spanning tree
    for i in range(1, n):
        parent = random.randint(0, i - 1)
        u, v = min(parent, i), max(parent, i)
        if (u, v) not in edge_set:
            edges.append([parent, i])
            edge_set.add((u, v))

    # Add some extra edges
    num_extra = random.randint(0, min(n, 100))
    for _ in range(num_extra):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            key = (min(u, v), max(u, v))
            if key not in edge_set:
                edges.append([u, v])
                edge_set.add(key)

    return edges


def _generate_random_graph(n: int) -> List[List[int]]:
    """Generate a random graph (may have multiple components)."""
    edges: List[List[int]] = []
    edge_set: set[Tuple[int, int]] = set()

    num_edges = random.randint(0, min(n * 2, 500))
    for _ in range(num_edges):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            key = (min(u, v), max(u, v))
            if key not in edge_set:
                edges.append([u, v])
                edge_set.add(key)

    return edges


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size.

    Args:
        n: Number of nodes

    Returns:
        str: Test case with n nodes
    """
    n = max(1, n)
    edges = _generate_connected_graph(n)
    source = 0
    destination = n - 1

    return _format_case(n, edges, source, destination)

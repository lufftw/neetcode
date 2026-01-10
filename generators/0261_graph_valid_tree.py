# generators/0261_graph_valid_tree.py
"""
Test Case Generator for Problem 0261 - Graph Valid Tree

LeetCode Constraints:
- 1 <= n <= 2000
- 0 <= edges.length <= 5000
- No duplicate edges, no self-loops
"""
import json
import random
from typing import Iterator, Optional, List, Tuple


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Graph Valid Tree."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        (5, [[0, 1], [0, 2], [0, 3], [1, 4]]),       # Valid tree
        (5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]),  # Has cycle
        (1, []),                                       # Single node
        (2, [[0, 1]]),                                # Two nodes
        (4, [[0, 1], [2, 3]]),                        # Disconnected
        (3, [[0, 1], [0, 2]]),                        # Simple valid tree
    ]

    for n, edges in edge_cases:
        yield f"{n}\n{json.dumps(edges, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate random graph (may or may not be valid tree)."""
    n = random.randint(3, 20)

    if random.random() < 0.5:
        # Generate valid tree
        edges = _generate_tree(n)
    else:
        # Generate random graph
        edges = _generate_random_graph(n)

    return f"{n}\n{json.dumps(edges, separators=(',', ':'))}"


def _generate_tree(n: int) -> List[List[int]]:
    """Generate a valid tree with n nodes."""
    if n == 1:
        return []

    edges = []
    nodes = list(range(n))
    random.shuffle(nodes)

    # Connect each node (except first) to a random previous node
    for i in range(1, n):
        parent = nodes[random.randint(0, i - 1)]
        edges.append([nodes[i], parent])

    random.shuffle(edges)
    return edges


def _generate_random_graph(n: int) -> List[List[int]]:
    """Generate random undirected graph."""
    # Random number of edges (may cause cycle or disconnection)
    num_edges = random.randint(n - 2, n + 2)
    num_edges = max(0, min(num_edges, n * (n - 1) // 2))

    edge_set = set()
    edges = []

    attempts = 0
    while len(edges) < num_edges and attempts < num_edges * 3:
        a = random.randint(0, n - 1)
        b = random.randint(0, n - 1)
        if a != b:
            edge = (min(a, b), max(a, b))
            if edge not in edge_set:
                edge_set.add(edge)
                edges.append(list(edge))
        attempts += 1

    return edges


def generate_for_complexity(n: int) -> str:
    """Generate tree with n nodes for complexity estimation."""
    n = max(1, min(n, 2000))
    edges = _generate_tree(n)
    return f"{n}\n{json.dumps(edges, separators=(',', ':'))}"


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}:\n{test}\n")

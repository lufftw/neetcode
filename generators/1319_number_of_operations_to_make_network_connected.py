# generators/1319_number_of_operations_to_make_network_connected.py
"""
Test Case Generator for Problem 1319 - Number of Operations to Make Network Connected

LeetCode Constraints:
- 1 <= n <= 10^5
- 1 <= connections.length <= min(n * (n - 1) / 2, 10^5)
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate test case inputs for Network Connected."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        (4, [[0, 1], [0, 2], [1, 2]]),  # Result: 1
        (6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]),  # Result: 2
        (6, [[0, 1], [0, 2], [0, 3], [1, 2]]),  # Result: -1 (not enough)
        (4, [[0, 1], [0, 2], [0, 3]]),  # Result: 0 (already connected)
    ]

    for n, connections in edge_cases:
        yield f"{n}\n{json.dumps(connections, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    n = random.randint(4, 50)
    num_edges = random.randint(n - 2, min(n * (n - 1) // 2, n + 10))

    edges = set()
    while len(edges) < num_edges:
        a = random.randint(0, n - 1)
        b = random.randint(0, n - 1)
        if a != b:
            edges.add((min(a, b), max(a, b)))

    connections = [[a, b] for a, b in edges]
    random.shuffle(connections)

    return f"{n}\n{json.dumps(connections, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size."""
    num_edges = n  # Roughly n edges
    edges = set()
    while len(edges) < num_edges:
        a = random.randint(0, n - 1)
        b = random.randint(0, n - 1)
        if a != b:
            edges.add((min(a, b), max(a, b)))
    connections = [[a, b] for a, b in edges]
    return f"{n}\n{json.dumps(connections, separators=(',', ':'))}"


if __name__ == "__main__":
    for i, case in enumerate(generate(3)):
        print(f"Case {i + 1}:\n{case}\n")

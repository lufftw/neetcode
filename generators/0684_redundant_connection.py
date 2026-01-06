# generators/0684_redundant_connection.py
"""
Test Case Generator for Problem 0684 - Redundant Connection

LeetCode Constraints:
- n == edges.length
- 3 <= n <= 1000
- edges[i].length == 2
- 1 <= ai < bi <= edges.length
- ai != bi
- There are no repeated edges
- The given graph is connected
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate test case inputs for Redundant Connection."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[1, 2], [1, 3], [2, 3]],  # Triangle
        [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],  # 4-cycle
        [[1, 2], [2, 3], [3, 1]],  # Minimal cycle
    ]

    for edges in edge_cases:
        yield json.dumps(edges, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a valid tree + one extra edge."""
    n = random.randint(4, 50)

    # Build a random tree with n-1 edges
    edges = []
    connected = {1}
    remaining = set(range(2, n + 1))

    while remaining:
        node = random.choice(list(remaining))
        parent = random.choice(list(connected))
        edge = [min(parent, node), max(parent, node)]
        edges.append(edge)
        connected.add(node)
        remaining.remove(node)

    # Add one extra edge to create a cycle
    nodes = list(range(1, n + 1))
    random.shuffle(nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a, b = min(nodes[i], nodes[j]), max(nodes[i], nodes[j])
            if [a, b] not in edges:
                edges.append([a, b])
                break
        else:
            continue
        break

    random.shuffle(edges)
    return json.dumps(edges, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size."""
    return _generate_case()


if __name__ == "__main__":
    for i, case in enumerate(generate(3)):
        print(f"Case {i + 1}: {case}")

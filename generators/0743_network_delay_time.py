# generators/0743_network_delay_time.py
"""
Test Case Generator for Problem 0743 - Network Delay Time

LeetCode Constraints:
- 1 <= k <= n <= 100
- 1 <= times.length <= 6000
- times[i].length == 3
- 1 <= ui, vi <= n
- ui != vi
- 0 <= wi <= 100
- All the pairs (ui, vi) are unique
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Network Delay Time.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: times, n, k in newline-separated format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2),  # Example 1
        ([[1, 2, 1]], 2, 1),  # Simple 2-node connected
        ([[1, 2, 1]], 2, 2),  # Unreachable
        ([[1, 2, 1], [2, 3, 1], [3, 1, 1]], 3, 1),  # Cycle
        ([[1, 2, 1], [1, 3, 2], [2, 3, 1]], 3, 1),  # Multiple paths
    ]

    for times, n, k in edge_cases:
        yield _format_case(times, n, k)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(times: List[List[int]], n: int, k: int) -> str:
    """Format a test case as input string."""
    return f"{json.dumps(times, separators=(',', ':'))}\n{n}\n{k}"


def _generate_random_case() -> str:
    """Generate a single random test case."""
    n = random.randint(2, 50)
    k = random.randint(1, n)

    # Generate random edges
    num_edges = random.randint(n - 1, min(n * 2, 100))
    edges = set()

    # Ensure connectivity from k by creating a spanning tree first
    nodes = list(range(1, n + 1))
    random.shuffle(nodes)

    # Find position of k
    k_pos = nodes.index(k)
    nodes[0], nodes[k_pos] = nodes[k_pos], nodes[0]

    # Create spanning tree from k
    for i in range(1, n):
        parent = random.choice(nodes[:i])
        weight = random.randint(1, 100)
        edges.add((parent, nodes[i], weight))

    # Add random additional edges
    for _ in range(num_edges - n + 1):
        u = random.randint(1, n)
        v = random.randint(1, n)
        if u != v and (u, v) not in {(e[0], e[1]) for e in edges}:
            weight = random.randint(1, 100)
            edges.add((u, v, weight))

    times = [list(e) for e in edges]
    return _format_case(times, n, k)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target number of nodes

    Returns:
        str: Test case with approximately n nodes
    """
    num_nodes = max(2, n)
    k = 1

    # Create a connected graph
    edges = []
    for i in range(2, num_nodes + 1):
        parent = random.randint(1, i - 1)
        weight = random.randint(1, 100)
        edges.append([parent, i, weight])

    # Add extra edges
    for _ in range(min(num_nodes, 50)):
        u = random.randint(1, num_nodes)
        v = random.randint(1, num_nodes)
        if u != v:
            weight = random.randint(1, 100)
            edges.append([u, v, weight])

    return _format_case(edges, num_nodes, k)

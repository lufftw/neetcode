# generators/0802_find_eventual_safe_states.py
"""
Test Case Generator for Problem 0802 - Find Eventual Safe States

LeetCode Constraints:
- n == graph.length
- 1 <= n <= 10^4
- 0 <= graph[i].length <= n
- 0 <= graph[i][j] <= n - 1
- graph[i] is sorted in a strictly increasing order
- The graph may contain self-loops
- The number of edges in the graph will be in the range [1, 4 * 10^4]
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Find Eventual Safe States.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Graph adjacency list in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[1, 2], [2, 3], [5], [0], [5], [], []],  # Example 1: safe = [2,4,5,6]
        [[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []],  # Example 2: safe = [4]
        [[]],  # Single terminal node
        [[1], []],  # Two nodes, one terminal
        [[0]],  # Single node with self-loop (not safe)
        [[1], [2], [3], []],  # Chain to terminal
        [[1], [0]],  # 2-node cycle (neither safe)
    ]

    for graph in edge_cases:
        yield json.dumps(graph, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    n = random.randint(2, 50)

    # Decide graph structure
    graph_type = random.choice(['dag', 'cyclic', 'mixed'])

    if graph_type == 'dag':
        graph = _generate_dag(n)
    elif graph_type == 'cyclic':
        graph = _generate_cyclic(n)
    else:
        graph = _generate_mixed(n)

    return json.dumps(graph, separators=(',', ':'))


def _generate_dag(n: int) -> List[List[int]]:
    """Generate a DAG (all nodes safe or terminal)."""
    graph = [[] for _ in range(n)]

    # Only allow edges from lower to higher index
    for i in range(n - 1):
        num_edges = random.randint(0, min(3, n - i - 1))
        targets = random.sample(range(i + 1, n), num_edges)
        graph[i] = sorted(targets)

    return graph


def _generate_cyclic(n: int) -> List[List[int]]:
    """Generate a graph with cycles."""
    graph = _generate_dag(n)

    # Add back edges to create cycles
    num_back_edges = random.randint(1, min(5, n))
    for _ in range(num_back_edges):
        u = random.randint(1, n - 1)
        v = random.randint(0, u - 1)
        if v not in graph[u]:
            graph[u] = sorted(graph[u] + [v])

    return graph


def _generate_mixed(n: int) -> List[List[int]]:
    """Generate a graph with some cycles and some safe nodes."""
    graph = [[] for _ in range(n)]

    # Create some terminal nodes (last few)
    num_terminals = random.randint(1, max(1, n // 3))

    # Create paths to terminals
    for i in range(n - num_terminals):
        if random.random() < 0.7:
            targets = []
            num_edges = random.randint(1, min(3, n - i))
            for _ in range(num_edges):
                target = random.randint(i + 1, n - 1) if i < n - 1 else i
                if target not in targets:
                    targets.append(target)
            graph[i] = sorted(targets)

    # Add some back edges for cycles
    num_back_edges = random.randint(0, min(3, n // 2))
    for _ in range(num_back_edges):
        if n > 1:
            u = random.randint(1, n - 1)
            v = random.randint(0, u - 1)
            if v not in graph[u]:
                graph[u] = sorted(graph[u] + [v])

    return graph


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target number of nodes

    Returns:
        str: Graph with approximately n nodes
    """
    num_nodes = max(2, n)
    graph = [[] for _ in range(num_nodes)]

    # Create a mix of safe and unsafe nodes
    for i in range(num_nodes - 1):
        num_edges = random.randint(0, min(3, num_nodes - i - 1))
        targets = random.sample(range(i + 1, num_nodes), num_edges)
        graph[i] = sorted(targets)

    return json.dumps(graph, separators=(',', ':'))

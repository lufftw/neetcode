"""
Generator for 1494 - Parallel Courses II

Generates test cases with:
- Course count n (1-15)
- DAG relations (prerequisites)
- Courses per semester k (1-n)
"""

import random
from typing import Iterator, Optional
import json


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Parallel Courses II."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # No prerequisites, k=1
        (3, [], 1),
        # No prerequisites, k=n
        (4, [], 4),
        # Linear chain
        (3, [[1, 2], [2, 3]], 1),
        # Star dependency (many converge to one)
        (4, [[1, 4], [2, 4], [3, 4]], 2),
        # Diamond dependency
        (4, [[1, 2], [1, 3], [2, 4], [3, 4]], 2),
        # Single course
        (1, [], 1),
        # Two independent chains
        (4, [[1, 2], [3, 4]], 2),
    ]

    yielded = 0
    for n, relations, k in edge_cases:
        if yielded >= count:
            return
        yield f"{n}\n{json.dumps(relations)}\n{k}"
        yielded += 1

    # Random cases
    while yielded < count:
        n = random.randint(2, 12)  # Keep n small for test performance
        k = random.randint(1, min(n, 5))

        # Generate random DAG edges
        relations = []
        max_edges = min(n * (n - 1) // 4, 15)  # Limit edges
        num_edges = random.randint(0, max_edges)

        # Create random topological order
        order = list(range(1, n + 1))
        random.shuffle(order)

        for _ in range(num_edges):
            i = random.randint(0, n - 2)
            j = random.randint(i + 1, n - 1)
            edge = [order[i], order[j]]
            if edge not in relations:
                relations.append(edge)

        yield f"{n}\n{json.dumps(relations)}\n{k}"
        yielded += 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n courses.

    Creates a challenging DAG structure with moderate dependencies.
    """
    n = min(n, 15)  # Cap at constraint limit
    k = max(1, n // 3)

    relations = []
    # Create layers of dependencies
    layer_size = max(1, n // 3)
    for layer in range(0, n - layer_size, layer_size):
        for i in range(layer, min(layer + layer_size, n)):
            for j in range(layer + layer_size, min(layer + 2 * layer_size, n)):
                if random.random() < 0.5:
                    relations.append([i + 1, j + 1])

    return f"{n}\n{json.dumps(relations)}\n{k}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, case in enumerate(generate(3, seed=42)):
        print(f"Case {i+1}:")
        print(case)
        print()

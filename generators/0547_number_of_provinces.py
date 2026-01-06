# generators/0547_number_of_provinces.py
"""
Test Case Generator for Problem 0547 - Number of Provinces

LeetCode Constraints:
- 1 <= n <= 200
- n == isConnected.length
- isConnected[i][j] is 1 or 0
- isConnected[i][i] == 1
- isConnected[i][j] == isConnected[j][i]
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate test case inputs for Number of Provinces."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[1, 1, 0], [1, 1, 0], [0, 0, 1]],  # 2 provinces
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],  # 3 provinces (all isolated)
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],  # 1 province (all connected)
        [[1]],  # Single city
        [[1, 1], [1, 1]],  # 2 cities, 1 province
    ]

    for matrix in edge_cases:
        yield json.dumps(matrix, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    n = random.randint(2, 50)
    density = random.uniform(0.1, 0.5)

    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1
        for j in range(i + 1, n):
            if random.random() < density:
                matrix[i][j] = 1
                matrix[j][i] = 1

    return json.dumps(matrix, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size."""
    density = 0.3
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1
        for j in range(i + 1, n):
            if random.random() < density:
                matrix[i][j] = 1
                matrix[j][i] = 1
    return json.dumps(matrix, separators=(',', ':'))


if __name__ == "__main__":
    for i, case in enumerate(generate(3)):
        print(f"Case {i + 1}: {case[:50]}...")

# generators/0973_k_closest_points_to_origin.py
"""
Test Case Generator for Problem 0973 - K Closest Points to Origin

LeetCode Constraints:
- 1 <= k <= points.length <= 10^4
- -10^4 <= xi, yi <= 10^4
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for K Closest Points to Origin."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        ([[0, 0]], 1),                           # Origin point
        ([[1, 0], [0, 1]], 1),                   # Tie in distance
        ([[1, 1], [2, 2], [3, 3]], 2),          # Sorted by distance
        ([[-1, -1], [1, 1]], 2),                # All points
    ]

    for points, k in edge_cases:
        yield f"{json.dumps(points)}\n{k}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random test case."""
    n = random.randint(5, 30)
    k = random.randint(1, n)
    points = [[random.randint(-100, 100), random.randint(-100, 100)] for _ in range(n)]
    return f"{json.dumps(points)}\n{k}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n points for complexity estimation.
    """
    n = max(1, min(n, 10000))
    k = max(1, n // 2)
    points = [[random.randint(-10000, 10000), random.randint(-10000, 10000)] for _ in range(n)]
    return f"{json.dumps(points)}\n{k}"


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}:")
        print(test)
        print()

"""
Test Case Generator for Problem 1029 - Two City Scheduling

LeetCode Constraints:
- 2 * n == costs.length
- 2 <= costs.length <= 100
- costs.length is even
- 1 <= aCosti, bCosti <= 1000
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in .in file format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[10, 20], [30, 200], [400, 50], [30, 20]],  # Classic example
        [[259, 770], [448, 54], [926, 667], [184, 139], [840, 118], [577, 469]],
        [[1, 1], [1, 1]],  # All equal costs
        [[1, 1000], [1000, 1]],  # Extreme preferences
        [[100, 100], [100, 100], [100, 100], [100, 100]],  # All same
        [[1, 2], [2, 1]],  # Minimal case
    ]

    for costs in edge_cases:
        yield json.dumps(costs, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    # n = number of people going to each city
    n = random.randint(1, 50)  # So 2n people total
    num_people = 2 * n

    costs = []
    for _ in range(num_people):
        cost_a = random.randint(1, 1000)
        cost_b = random.randint(1, 1000)
        costs.append([cost_a, cost_b])

    return json.dumps(costs, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    # n must be even for this problem
    if n % 2 == 1:
        n += 1
    costs = [[random.randint(1, 1000), random.randint(1, 1000)] for _ in range(n)]
    return json.dumps(costs, separators=(',', ':'))

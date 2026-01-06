"""
Test Case Generator for Problem 134 - Gas Station

LeetCode Constraints:
- n == gas.length == cost.length
- 1 <= n <= 10^5
- 0 <= gas[i], cost[i] <= 10^4
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
        str: Test input in .in file format (gas on line 1, cost on line 2)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]),  # Classic example, answer = 3
        ([2, 3, 4], [3, 4, 3]),  # No solution, answer = -1
        ([5], [4]),  # Single station, feasible
        ([4], [5]),  # Single station, infeasible
        ([1, 1, 1], [1, 1, 1]),  # All equal, answer = 0
        ([3, 1, 1], [1, 1, 1]),  # Extra gas at start
    ]

    for gas, cost in edge_cases:
        yield f"{json.dumps(gas, separators=(',', ':'))}\n{json.dumps(cost, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    n = random.randint(1, 1000)

    # Mix of feasible and infeasible cases
    if random.random() < 0.6:
        # Generate feasible case: ensure total gas >= total cost
        gas = [random.randint(0, 100) for _ in range(n)]
        total_gas = sum(gas)
        cost = []
        remaining = total_gas  # Ensure we don't exceed total gas
        for i in range(n - 1):
            c = random.randint(0, min(100, remaining // (n - i)))
            cost.append(c)
            remaining -= c
        cost.append(remaining)  # Last cost uses remaining
        random.shuffle(cost)  # Shuffle to make it interesting
    else:
        # Generate potentially infeasible case
        gas = [random.randint(0, 100) for _ in range(n)]
        cost = [random.randint(0, 100) for _ in range(n)]

    return f"{json.dumps(gas, separators=(',', ':'))}\n{json.dumps(cost, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    gas = [random.randint(1, 100) for _ in range(n)]
    cost = [random.randint(1, 100) for _ in range(n)]
    # Make it feasible
    if sum(gas) < sum(cost):
        gas[0] += sum(cost) - sum(gas) + 1
    return f"{json.dumps(gas, separators=(',', ':'))}\n{json.dumps(cost, separators=(',', ':'))}"

"""
Test Case Generator for Problem 1648 - Sell Diminishing-Valued Colored Balls

LeetCode Constraints:
- 1 <= inventory.length <= 10^5
- 1 <= inventory[i] <= 10^9
- 1 <= orders <= min(sum(inventory[i]), 10^9)
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([2, 5], 4),                    # Example 1
        ([3, 5], 6),                    # Example 2
        ([1000000000], 1000000000),     # Example 3: large single
        ([1], 1),                       # Single ball
        ([5, 5, 5], 3),                 # All equal
        ([10], 5),                      # Single color, partial
    ]

    for inv, orders in edge_cases:
        yield f'{json.dumps(inv, separators=(",", ":"))}\n{orders}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(1, 50)
        inventory = [random.randint(1, 1000) for _ in range(n)]
        max_orders = sum(inventory)
        orders = random.randint(1, min(max_orders, 10000))
        yield f'{json.dumps(inventory, separators=(",", ":"))}\n{orders}'


def generate_for_complexity(size: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    n = max(1, min(size, 500))

    inventory = [random.randint(1, 1000) for _ in range(n)]
    max_orders = sum(inventory)
    orders = random.randint(1, min(max_orders, 100000))

    return f'{json.dumps(inventory, separators=(",", ":"))}\n{orders}'

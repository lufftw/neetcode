"""
Generator for 2234 - Maximum Total Beauty of the Gardens

Generates test cases with:
- flowers array (current flower counts)
- newFlowers (budget for planting)
- target (threshold for complete garden)
- full, partial (beauty multipliers)
"""

import random
from typing import Iterator, Optional
import json


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Maximum Total Beauty of the Gardens."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # All already complete
        ([10, 10, 10], 5, 5, 3, 2),
        # None complete, high partial value
        ([1, 1, 1], 6, 10, 1, 100),
        # Single garden
        ([3], 5, 5, 10, 5),
        # All same value
        ([5, 5, 5, 5], 10, 8, 4, 3),
        # Mixed values
        ([1, 2, 3, 4, 5], 10, 6, 5, 2),
        # Large budget
        ([1, 1, 1], 1000, 5, 10, 5),
    ]

    yielded = 0
    for flowers, newFlowers, target, full, partial in edge_cases:
        if yielded >= count:
            return
        yield f"{json.dumps(flowers)}\n{newFlowers}\n{target}\n{full}\n{partial}"
        yielded += 1

    # Random cases
    while yielded < count:
        n = random.randint(1, 100)
        target = random.randint(5, 100)
        flowers = [random.randint(1, target + 5) for _ in range(n)]
        newFlowers = random.randint(0, n * target)
        full = random.randint(1, 100)
        partial = random.randint(1, 100)

        yield f"{json.dumps(flowers)}\n{newFlowers}\n{target}\n{full}\n{partial}"
        yielded += 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n gardens.

    Creates a balanced scenario where some gardens are near complete.
    """
    target = max(10, n // 10)
    flowers = [random.randint(1, target) for _ in range(n)]
    newFlowers = n * target // 2  # Enough for about half
    full = random.randint(1, 100)
    partial = random.randint(1, 100)

    return f"{json.dumps(flowers)}\n{newFlowers}\n{target}\n{full}\n{partial}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, case in enumerate(generate(3, seed=42)):
        print(f"Case {i+1}:")
        print(case)
        print()

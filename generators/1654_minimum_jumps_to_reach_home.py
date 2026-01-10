"""
Generator for 1654 - Minimum Jumps to Reach Home

Generates test cases with:
- Various forbidden positions
- Different a, b values
- Reachable and unreachable targets
"""

import random
from typing import Iterator, Optional
import json


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Minimum Jumps to Reach Home."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([], 1, 1, 0),             # Already home
        ([], 5, 3, 10),            # No forbidden, simple
        ([1], 2, 1, 4),            # One forbidden
        ([2, 4, 6], 3, 1, 9),      # Multiple forbidden
        (list(range(1, 100)), 100, 1, 0),  # Home is 0
    ]

    yielded = 0
    for forbidden, a, b, x in edge_cases:
        if yielded >= count:
            return
        yield f"{json.dumps(forbidden)}\n{a}\n{b}\n{x}"
        yielded += 1

    # Random cases
    while yielded < count:
        # Generate forbidden positions
        num_forbidden = random.randint(0, 100)
        forbidden = random.sample(range(1, 2001), min(num_forbidden, 2000))

        a = random.randint(1, 500)
        b = random.randint(1, 500)

        # Choose x not in forbidden
        x = random.randint(0, 500)
        while x in forbidden:
            x = random.randint(0, 500)

        yield f"{json.dumps(forbidden)}\n{a}\n{b}\n{x}"
        yielded += 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n forbidden positions.
    """
    n = min(n, 1000)
    forbidden = random.sample(range(1, 2001), n)
    a = random.randint(1, 500)
    b = random.randint(1, 500)
    x = random.randint(0, 500)
    while x in forbidden:
        x = random.randint(0, 500)
    return f"{json.dumps(forbidden)}\n{a}\n{b}\n{x}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, case in enumerate(generate(3, seed=42)):
        print(f"Case {i+1}:")
        print(case)
        print()

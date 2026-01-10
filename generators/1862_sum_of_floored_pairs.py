"""
Generator for 1862 - Sum of Floored Pairs

Generates test cases with various distributions:
- Uniform random
- Same value
- Powers of 2
- Small/large values
"""

import random
from typing import Iterator, Optional
import json


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Sum of Floored Pairs."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [1],                    # Single element
        [1, 1, 1],              # All ones (maximum quotients)
        [1, 2, 4, 8, 16],       # Powers of 2
        [100, 100, 100],        # Same large value
        [1, 10, 100, 1000],     # Different magnitudes
        [2, 3, 5, 7, 11],       # Primes
        [1, 2, 3, 4, 5, 6],     # Consecutive
    ]

    yielded = 0
    for nums in edge_cases:
        if yielded >= count:
            return
        yield json.dumps(nums)
        yielded += 1

    # Random cases
    while yielded < count:
        n = random.randint(1, 500)  # Keep small for brute-force verification
        case_type = random.choice(['uniform', 'same', 'small', 'mixed'])

        if case_type == 'uniform':
            max_val = random.randint(10, 1000)
            nums = [random.randint(1, max_val) for _ in range(n)]
        elif case_type == 'same':
            val = random.randint(1, 100)
            nums = [val] * n
        elif case_type == 'small':
            nums = [random.randint(1, 10) for _ in range(n)]
        else:  # mixed
            nums = [random.randint(1, 10000) for _ in range(n)]

        yield json.dumps(nums)
        yielded += 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n elements.

    Creates a mix of values to stress the algorithm.
    """
    max_val = min(n * 10, 100000)
    nums = [random.randint(1, max_val) for _ in range(n)]
    return json.dumps(nums)


if __name__ == "__main__":
    print("Sample test cases:")
    for i, case in enumerate(generate(3, seed=42)):
        print(f"Case {i+1}:")
        print(case)
        print()

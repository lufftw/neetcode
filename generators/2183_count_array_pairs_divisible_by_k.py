"""
Generator for 2183 - Count Array Pairs Divisible by K

Generates test cases with:
- Various k values (primes, composites, highly composite)
- Arrays with diverse gcd distributions
"""

import random
from typing import Iterator, Optional
import json


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for Count Array Pairs Divisible by K."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([1], 1),                    # Single element
        ([1, 1, 1], 1),              # k=1, all pairs valid
        ([2, 4, 6, 8], 2),           # All multiples of k
        ([1, 2, 3, 4, 5], 7),        # Prime k, few pairs
        ([6, 10, 15], 30),           # Composite k
        ([1, 2, 3], 100),            # Large k, no pairs
        ([5, 10, 15, 20], 5),        # Multiples of k
    ]

    yielded = 0
    for nums, k in edge_cases:
        if yielded >= count:
            return
        yield f"{json.dumps(nums)}\n{k}"
        yielded += 1

    # Random cases
    while yielded < count:
        n = random.randint(1, 500)  # Keep small for brute-force verification
        k = random.randint(1, 1000)

        case_type = random.choice(['multiples', 'mixed', 'coprime'])

        if case_type == 'multiples':
            # Many multiples of k's factors
            nums = [random.randint(1, 100) * random.choice([1, k, k // 2 if k > 1 else 1]) for _ in range(n)]
        elif case_type == 'coprime':
            # Values likely coprime to k
            nums = [random.randint(1, 100) for _ in range(n)]
        else:
            nums = [random.randint(1, 10000) for _ in range(n)]

        yield f"{json.dumps(nums)}\n{k}"
        yielded += 1


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n elements.

    Creates a mix of values with a moderately composite k.
    """
    k = random.choice([6, 12, 24, 30, 60, 120])  # Highly composite
    nums = [random.randint(1, 10000) for _ in range(n)]
    return f"{json.dumps(nums)}\n{k}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, case in enumerate(generate(3, seed=42)):
        print(f"Case {i+1}:")
        print(case)
        print()

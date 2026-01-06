"""
Test Generator for LeetCode 204: Count Primes
Pattern: Math / Number Theory - Prime Sieve
"""

import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test cases for Count Primes.

    Constraints:
    - 0 <= n <= 5 * 10^6
    """
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        10,        # 4 primes: 2,3,5,7
        0,         # 0 primes
        1,         # 0 primes
        2,         # 0 primes (primes < 2)
        3,         # 1 prime: 2
        100,       # 25 primes
        1000,      # 168 primes
        20,        # 8 primes: 2,3,5,7,11,13,17,19
    ]

    for n in edge_cases:
        if count <= 0:
            break
        yield json.dumps(n, separators=(",", ":"))
        count -= 1

    while count > 0:
        n = random.randint(0, 10000)
        yield json.dumps(n, separators=(",", ":"))
        count -= 1


def generate_for_complexity(n: int) -> str:
    return json.dumps(max(0, min(n, 5000000)), separators=(",", ":"))


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)

"""
Test Generator for LeetCode 168: Excel Sheet Column Title
Pattern: Math / Number Theory - Base Conversion
"""

import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test cases for Excel Sheet Column Title.

    Constraints:
    - 1 <= columnNumber <= 2^31 - 1
    """
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        1,         # A
        26,        # Z
        27,        # AA
        28,        # AB
        701,       # ZY
        702,       # ZZ
        703,       # AAA
        52,        # AZ
        2147483647 # Max int
    ]

    for n in edge_cases:
        if count <= 0:
            break
        yield json.dumps(n, separators=(",", ":"))
        count -= 1

    while count > 0:
        n = random.randint(1, 100000)
        yield json.dumps(n, separators=(",", ":"))
        count -= 1


def generate_for_complexity(n: int) -> str:
    return json.dumps(max(1, min(n, 2147483647)), separators=(",", ":"))


if __name__ == "__main__":
    for case in generate(5, seed=42):
        print(case)

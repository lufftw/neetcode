"""
Test Case Generator for Problem 1191 - K-Concatenation Maximum Sum

LeetCode Constraints:
- 1 <= arr.length <= 10^5
- 1 <= k <= 10^5
- -10^4 <= arr[i] <= 10^4
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([1, 2], 3),           # Example 1
        ([1, -2, 1], 5),       # Example 2
        ([-1, -2], 7),         # Example 3: all negative
        ([1], 1),              # Single element
        ([1], 10),             # Single positive repeated
        ([-1], 10),            # Single negative repeated
        ([1, -1], 100),        # Alternating
        ([3, -1, 2], 3),       # Mixed positive sum
    ]

    for arr, k in edge_cases:
        yield f"{json.dumps(arr, separators=(',', ':'))}\n{k}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(1, 50)
        arr = [random.randint(-100, 100) for _ in range(n)]
        k = random.randint(1, 100)
        yield f"{json.dumps(arr, separators=(',', ':'))}\n{k}"


def generate_for_complexity(n: int) -> str:
    n = max(1, min(n, 10000))
    arr = [random.randint(-100, 100) for _ in range(n)]
    k = random.randint(1, 1000)
    return f"{json.dumps(arr, separators=(',', ':'))}\n{k}"

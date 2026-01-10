# generators/0146_lru_cache.py
"""
Test Case Generator for Problem 0146 - LRU Cache

LeetCode Constraints:
- 1 <= capacity <= 3000
- 0 <= key <= 10^4
- 0 <= value <= 10^5
- At most 2 * 10^5 calls to get and put
"""
import json
import random
from typing import Iterator, Optional, List
from collections import OrderedDict


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases for LRU Cache."""
    if seed is not None:
        random.seed(seed)

    # Edge cases
    edge_cases = [
        # LeetCode example
        (
            ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"],
            [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]],
        ),
        # Capacity 1
        (
            ["LRUCache", "put", "get", "put", "get", "get"],
            [[1], [2, 1], [2], [3, 2], [2], [3]],
        ),
    ]

    for ops, args in edge_cases:
        yield f"{json.dumps(ops)}\n{json.dumps(args)}"
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random sequence of LRU cache operations."""
    capacity = random.randint(1, 10)
    num_ops = random.randint(10, 50)

    operations = ["LRUCache"]
    arguments = [[capacity]]

    for _ in range(num_ops):
        if random.random() < 0.6:
            # put operation
            key = random.randint(0, 20)
            value = random.randint(0, 100)
            operations.append("put")
            arguments.append([key, value])
        else:
            # get operation
            key = random.randint(0, 20)
            operations.append("get")
            arguments.append([key])

    return f"{json.dumps(operations)}\n{json.dumps(arguments)}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with approximately n operations for complexity estimation.
    """
    n = max(1, min(n, 200000))
    capacity = min(1000, max(1, n // 10))

    operations = ["LRUCache"]
    arguments = [[capacity]]

    for _ in range(n):
        if random.random() < 0.6:
            key = random.randint(0, capacity * 2)
            value = random.randint(0, 1000)
            operations.append("put")
            arguments.append([key, value])
        else:
            key = random.randint(0, capacity * 2)
            operations.append("get")
            arguments.append([key])

    return f"{json.dumps(operations)}\n{json.dumps(arguments)}"


if __name__ == "__main__":
    for i, test in enumerate(generate(3, seed=42), 1):
        lines = test.split("\n")
        ops = json.loads(lines[0])
        print(f"Test {i}: {len(ops)} operations")

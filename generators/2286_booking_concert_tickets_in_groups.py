"""
Test Case Generator for Problem 2286 - Booking Concert Tickets in Groups

LeetCode Constraints:
- 1 <= n <= 5 * 10^4
- 1 <= m, k <= 10^9
- 0 <= maxRow <= n - 1
- At most 5 * 10^4 calls
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs for BookMyShow."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Example from problem
        (
            ["BookMyShow", "gather", "gather", "scatter", "scatter"],
            [[2, 5], [4, 0], [2, 0], [5, 1], [5, 1]]
        ),
        # Single row
        (
            ["BookMyShow", "gather", "gather", "scatter"],
            [[1, 10], [5, 0], [5, 0], [1, 0]]
        ),
        # All gather
        (
            ["BookMyShow", "gather", "gather", "gather"],
            [[3, 3], [2, 0], [2, 1], [2, 2]]
        ),
        # All scatter
        (
            ["BookMyShow", "scatter", "scatter", "scatter"],
            [[3, 3], [3, 0], [3, 1], [3, 2]]
        ),
    ]

    for methods, args in edge_cases:
        yield _format_case(methods, args)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(methods: List[str], args: List[List[int]]) -> str:
    """Format a test case as input string."""
    return f"{json.dumps(methods, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


def _generate_random_case() -> str:
    """Generate a single random test case."""
    n = random.randint(2, 100)
    m = random.randint(2, 1000)

    methods = ["BookMyShow"]
    args = [[n, m]]

    num_ops = random.randint(5, 50)

    for _ in range(num_ops):
        op = random.choice(["gather", "scatter"])
        max_row = random.randint(0, n - 1)
        k = random.randint(1, m)

        methods.append(op)
        args.append([k, max_row])

    return _format_case(methods, args)


def generate_for_complexity(n: int) -> str:
    """Generate test case with n operations."""
    n = max(5, min(n, 1000))

    rows = random.randint(10, 100)
    seats = random.randint(100, 10000)

    methods = ["BookMyShow"]
    args = [[rows, seats]]

    for _ in range(n):
        op = random.choice(["gather", "scatter"])
        max_row = random.randint(0, rows - 1)
        k = random.randint(1, seats // 2)

        methods.append(op)
        args.append([k, max_row])

    return _format_case(methods, args)


if __name__ == "__main__":
    for i, test in enumerate(generate(3, seed=42), 1):
        print(f"--- Test {i} ---")
        print(test[:200] + "..." if len(test) > 200 else test)
        print()

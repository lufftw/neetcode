"""
Test Case Generator for Problem 2612 - Minimum Reverse Operations

LeetCode Constraints:
- 1 <= n <= 10^5
- 0 <= p <= n - 1
- 0 <= banned.length <= n - 1
- 0 <= banned[i] <= n - 1
- 1 <= k <= n
- banned[i] != p
- all values in banned are unique
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Minimum Reverse Operations.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (n, p, banned, k on separate lines)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Example cases
        (4, 0, [1, 2], 4),
        (5, 0, [2, 4], 3),
        (4, 2, [0, 1, 3], 1),

        # Minimal cases
        (1, 0, [], 1),
        (2, 0, [], 1),
        (2, 0, [], 2),
        (2, 1, [0], 2),

        # k=1: no movement possible
        (5, 2, [], 1),
        (5, 2, [0, 1, 3, 4], 1),

        # k=n: can only reverse entire array
        (5, 0, [], 5),
        (5, 2, [0, 4], 5),

        # No banned positions
        (10, 5, [], 3),
        (10, 0, [], 4),

        # Many banned positions
        (6, 3, [0, 1, 2, 4, 5], 2),
    ]

    for n, p, banned, k in edge_cases:
        yield _format_case(n, p, banned, k)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(n: int, p: int, banned: List[int], k: int) -> str:
    """Format a test case as input string."""
    return f"{n}\n{p}\n{json.dumps(banned, separators=(',', ':'))}\n{k}"


def _generate_random_case() -> str:
    """Generate a single random test case."""
    # Choose n with distribution favoring various sizes
    n = random.choice([
        random.randint(1, 10),
        random.randint(10, 100),
        random.randint(100, 1000),
        random.randint(1000, 10000),
    ])

    # Random starting position
    p = random.randint(0, n - 1)

    # Random k
    k = random.randint(1, n)

    # Random banned positions (not including p)
    max_banned = min(n - 1, random.randint(0, n // 2))
    available = [i for i in range(n) if i != p]
    banned = random.sample(available, min(max_banned, len(available)))

    return _format_case(n, p, banned, k)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Minimum Reverse Operations:
    - n is the array size
    - Time complexity is O(n log n) with SortedList

    Args:
        n: Target array size

    Returns:
        str: Test input
    """
    n = max(1, min(n, 100000))  # Clamp to valid range

    p = random.randint(0, n - 1)
    k = random.randint(2, n)  # k >= 2 for interesting cases

    # Create some banned positions (sparse)
    num_banned = min(n // 10, n - 1)
    available = [i for i in range(n) if i != p]
    banned = random.sample(available, min(num_banned, len(available)))

    return _format_case(n, p, banned, k)


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"--- Test {i} ---")
        print(test)
        print()

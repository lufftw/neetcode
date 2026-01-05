# generators/1109_corporate_flight_bookings.py
"""
Test Case Generator for Problem 1109 - Corporate Flight Bookings

LeetCode Constraints:
- 1 <= n <= 2 * 10^4
- 1 <= bookings.length <= 2 * 10^4
- bookings[i].length == 3
- 1 <= first_i <= last_i <= n
- 1 <= seats_i <= 10^4

Time Complexity: O(n + m) with difference array
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Corporate Flight Bookings.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in JSON format (bookings, n)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Classic example
        ([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5),
        # Single booking covering all
        ([[1, 5, 100]], 5),
        # Single flight
        ([[1, 1, 50]], 1),
        # Non-overlapping bookings
        ([[1, 2, 10], [3, 4, 20]], 4),
        # All flights have same booking
        ([[1, 3, 10], [1, 3, 20]], 3),
        # Boundary: first == last
        ([[2, 2, 100]], 3),
    ]

    for bookings, n in edge_cases:
        yield f"{json.dumps(bookings, separators=(',', ':'))}\n{n}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    n = random.randint(1, 500)
    num_bookings = random.randint(1, 200)
    bookings = []

    for _ in range(num_bookings):
        first = random.randint(1, n)
        last = random.randint(first, n)
        seats = random.randint(1, 1000)
        bookings.append([first, last, seats])

    return f"{json.dumps(bookings, separators=(',', ':'))}\n{n}"


def generate_for_complexity(n: int, m: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    bookings = []
    for _ in range(m):
        first = random.randint(1, n)
        last = random.randint(first, n)
        seats = random.randint(1, 1000)
        bookings.append([first, last, seats])
    return f"{json.dumps(bookings, separators=(',', ':'))}\n{n}"

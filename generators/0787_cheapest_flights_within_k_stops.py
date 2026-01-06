# generators/0787_cheapest_flights_within_k_stops.py
"""
Test Case Generator for Problem 0787 - Cheapest Flights Within K Stops

LeetCode Constraints:
- 1 <= n <= 100
- 0 <= flights.length <= (n * (n - 1) / 2)
- flights[i].length == 3
- 0 <= fromi, toi < n
- fromi != toi
- 1 <= pricei <= 10^4
- 0 <= src, dst, k < n
- src != dst
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Cheapest Flights Within K Stops.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: n, flights, src, dst, k in newline-separated format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        (4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1),  # Example 1
        (3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1),  # Example 2
        (3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0),  # Example 3
        (2, [[0, 1, 100]], 0, 1, 0),  # Direct flight
        (3, [[0, 1, 100]], 0, 2, 1),  # No path
        (4, [[0, 1, 1], [0, 2, 5], [1, 2, 1], [2, 3, 1]], 0, 3, 1),  # K limits shorter path
    ]

    for n, flights, src, dst, k in edge_cases:
        yield _format_case(n, flights, src, dst, k)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> str:
    """Format a test case as input string."""
    return (f"{n}\n{json.dumps(flights, separators=(',', ':'))}\n"
            f"{src}\n{dst}\n{k}")


def _generate_random_case() -> str:
    """Generate a single random test case."""
    n = random.randint(3, 30)
    src = random.randint(0, n - 1)
    dst = random.randint(0, n - 1)
    while dst == src:
        dst = random.randint(0, n - 1)

    k = random.randint(0, n - 2)

    # Generate flights
    num_flights = random.randint(n - 1, min(n * 2, 50))
    flight_set = set()

    # Ensure there's a path from src to dst (may or may not be within k stops)
    path_len = random.randint(1, min(k + 2, n - 1))
    path = [src]
    remaining = [i for i in range(n) if i != src]
    random.shuffle(remaining)

    for i in range(path_len):
        if i == path_len - 1:
            path.append(dst)
        else:
            if remaining:
                path.append(remaining.pop())
            else:
                break

    for i in range(len(path) - 1):
        price = random.randint(100, 1000)
        flight_set.add((path[i], path[i + 1], price))

    # Add random flights
    for _ in range(num_flights - len(flight_set)):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in {(f[0], f[1]) for f in flight_set}:
            price = random.randint(100, 1000)
            flight_set.add((u, v, price))

    flights = [list(f) for f in flight_set]
    return _format_case(n, flights, src, dst, k)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target number of cities

    Returns:
        str: Test case with approximately n cities
    """
    num_cities = max(3, n)
    src = 0
    dst = num_cities - 1
    k = num_cities // 2

    # Create a connected graph
    flights = []
    for i in range(num_cities - 1):
        flights.append([i, i + 1, random.randint(100, 1000)])

    # Add extra flights
    for _ in range(min(num_cities, 30)):
        u = random.randint(0, num_cities - 1)
        v = random.randint(0, num_cities - 1)
        if u != v:
            flights.append([u, v, random.randint(100, 1000)])

    return _format_case(num_cities, flights, src, dst, k)

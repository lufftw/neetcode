# generators/1094_car_pooling.py
"""
Test Case Generator for Problem 1094 - Car Pooling

LeetCode Constraints:
- 1 <= trips.length <= 1000
- trips[i].length == 3
- 1 <= numPassengers_i <= 100
- 0 <= from_i < to_i <= 1000
- 1 <= capacity <= 10^5

Time Complexity: O(n + m) with difference array (m = max location)
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Car Pooling.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in JSON format (trips, capacity)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([[2, 1, 5], [3, 3, 7]], 4),        # False - exceeds at location 3
        ([[2, 1, 5], [3, 3, 7]], 5),        # True - just enough
        ([[2, 1, 5], [3, 5, 7]], 3),        # True - no overlap
        ([[3, 2, 7], [3, 7, 9], [8, 3, 9]], 11),  # Complex overlaps
        ([[1, 0, 1]], 1),                    # Single trip
        ([[100, 0, 1000]], 100),             # Max passengers, full route
        ([[1, 0, 1], [1, 1, 2]], 1),         # Sequential, boundary
    ]

    for trips, capacity in edge_cases:
        yield f"{json.dumps(trips, separators=(',', ':'))}\n{capacity}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a single random test case."""
    num_trips = random.randint(1, 100)
    trips = []
    max_passengers_at_any_point = 0

    for _ in range(num_trips):
        passengers = random.randint(1, 50)
        from_loc = random.randint(0, 999)
        to_loc = random.randint(from_loc + 1, 1000)
        trips.append([passengers, from_loc, to_loc])

    # Calculate max overlapping passengers (for realistic capacity)
    diff = [0] * 1002
    for passengers, from_loc, to_loc in trips:
        diff[from_loc] += passengers
        diff[to_loc] -= passengers

    current = 0
    for d in diff:
        current += d
        max_passengers_at_any_point = max(max_passengers_at_any_point, current)

    # Random capacity - sometimes feasible, sometimes not
    if random.random() < 0.5:
        capacity = random.randint(max_passengers_at_any_point, max_passengers_at_any_point + 50)
    else:
        capacity = random.randint(max(1, max_passengers_at_any_point - 20), max_passengers_at_any_point)

    return f"{json.dumps(trips, separators=(',', ':'))}\n{capacity}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    trips = []
    for _ in range(n):
        passengers = random.randint(1, 50)
        from_loc = random.randint(0, 999)
        to_loc = random.randint(from_loc + 1, 1000)
        trips.append([passengers, from_loc, to_loc])
    capacity = random.randint(1, 10000)
    return f"{json.dumps(trips, separators=(',', ':'))}\n{capacity}"

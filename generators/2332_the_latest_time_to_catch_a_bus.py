"""
Test Case Generator for Problem 2332 - The Latest Time to Catch a Bus

LeetCode Constraints:
- 1 <= n, m, capacity <= 10^5
- 2 <= buses[i], passengers[i] <= 10^9
- All buses[i] and passengers[i] are unique
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        ([10, 20], [2, 17, 18, 19], 2),          # Example 1
        ([20, 30, 10], [19, 13, 26, 4, 25, 11, 21], 2),  # Example 2
        ([10], [10], 1),                          # Passenger at bus time
        ([10], [2], 1),                           # One passenger before bus
        ([10], [11], 1),                          # Passenger after bus
        ([5, 10], [3, 4, 5, 8, 9, 10], 2),        # Full buses with gaps
        ([10], [2, 3, 4, 5, 6, 7, 8, 9, 10], 100),  # Large capacity
    ]

    for buses, passengers, capacity in edge_cases:
        yield f'{json.dumps(buses, separators=(",", ":"))}\n{json.dumps(passengers, separators=(",", ":"))}\n{capacity}'
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(1, 20)
        m = random.randint(1, 50)
        capacity = random.randint(1, 20)

        # Generate unique times
        max_time = 1000
        all_times = random.sample(range(2, max_time), n + m)
        buses = all_times[:n]
        passengers = all_times[n:]

        yield f'{json.dumps(buses, separators=(",", ":"))}\n{json.dumps(passengers, separators=(",", ":"))}\n{capacity}'


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(1, min(n, 1000))
    m = n * 2

    max_time = n * 10
    all_times = random.sample(range(2, max_time + n + m), n + m)
    buses = sorted(all_times[:n])
    passengers = all_times[n:]
    capacity = max(1, n // 2)

    return f'{json.dumps(buses, separators=(",", ":"))}\n{json.dumps(passengers, separators=(",", ":"))}\n{capacity}'

# generators/0841_keys_and_rooms.py
"""
Test Case Generator for Problem 0841 - Keys and Rooms

LeetCode Constraints:
- n == rooms.length
- 2 <= n <= 1000
- 0 <= rooms[i].length <= 1000
- 1 <= sum(rooms[i].length) <= 3000
- 0 <= rooms[i][j] < n
- All values of rooms[i] are unique
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Keys and Rooms.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Rooms array in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[1], [2], [3], []],  # Can visit all (linear)
        [[1, 3], [3, 0, 1], [2], [0]],  # Cannot visit room 2
        [[1, 2, 3], [], [], []],  # Room 0 has all keys
        [[1], [0]],  # Two rooms with mutual keys
        [[1], [2], [0]],  # Cycle through all rooms
    ]

    for rooms in edge_cases:
        yield json.dumps(rooms, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    n = random.randint(2, 100)

    # Randomly decide if all rooms should be visitable
    all_visitable = random.random() < 0.5

    if all_visitable:
        return _generate_all_visitable(n)
    else:
        return _generate_random(n)


def _generate_all_visitable(n: int) -> str:
    """Generate a graph where all rooms are visitable from room 0."""
    rooms: List[List[int]] = [[] for _ in range(n)]

    # Build a spanning tree from room 0
    unvisited = list(range(1, n))
    random.shuffle(unvisited)

    visited = [0]
    for room in unvisited:
        # Pick a random visited room to hold the key
        source = random.choice(visited)
        rooms[source].append(room)
        visited.append(room)

    # Add some extra random keys
    num_extra = random.randint(0, n)
    for _ in range(num_extra):
        room = random.randint(0, n - 1)
        key = random.randint(0, n - 1)
        if key != room and key not in rooms[room]:
            rooms[room].append(key)

    return json.dumps(rooms, separators=(',', ':'))


def _generate_random(n: int) -> str:
    """Generate a random rooms configuration."""
    rooms: List[List[int]] = [[] for _ in range(n)]

    # Total keys constraint: sum <= 3000
    max_total_keys = min(3000, n * 10)
    total_keys = 0

    for i in range(n):
        num_keys = random.randint(0, min(n - 1, max_total_keys - total_keys))
        if num_keys > 0:
            available_keys = [k for k in range(n) if k != i]
            rooms[i] = random.sample(available_keys, min(num_keys, len(available_keys)))
            total_keys += len(rooms[i])

    return json.dumps(rooms, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size.

    Args:
        n: Number of rooms

    Returns:
        str: Rooms array with n rooms
    """
    return _generate_all_visitable(max(2, n))

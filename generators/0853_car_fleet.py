# generators/0853_car_fleet.py
"""
Test Case Generator for Problem 0853 - Car Fleet

LeetCode Constraints:
- n == position.length == speed.length
- 1 <= n <= 10^5
- 0 < target <= 10^6
- 0 <= position[i] < target
- All position values are unique
- 0 < speed[i] <= 10^6
"""
import json
import random
from typing import Iterator, Optional, List, Set


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Car Fleet.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (target, position, speed as JSON)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1
        (12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]),
        # LeetCode Example 2: single car
        (10, [3], [3]),
        # LeetCode Example 3: all merge into one fleet
        (100, [0, 2, 4], [4, 2, 1]),
        # All cars same speed (no merging possible by catch-up)
        (10, [0, 2, 4, 6], [1, 1, 1, 1]),
        # Two cars, will merge
        (10, [0, 5], [3, 1]),
        # Two cars, won't merge
        (10, [0, 5], [1, 3]),
    ]

    for target, position, speed in edge_cases:
        yield _format_case(target, position, speed)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(target: int, position: List[int], speed: List[int]) -> str:
    """Format a test case as input string."""
    return (
        f"{target}\n"
        f"{json.dumps(position, separators=(',', ':'))}\n"
        f"{json.dumps(speed, separators=(',', ':'))}"
    )


def _generate_random_case() -> str:
    """Generate a random car fleet test case."""
    n = random.randint(2, 50)
    target = random.randint(n + 10, 1000)

    # Generate unique positions
    positions: Set[int] = set()
    while len(positions) < n:
        positions.add(random.randint(0, target - 1))

    position = list(positions)
    speed = [random.randint(1, 100) for _ in range(n)]

    return _format_case(target, position, speed)


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Car Fleet:
    - n is the number of cars
    - Time complexity is O(n log n) for sorting

    Args:
        n: Number of cars (will be clamped to [1, 100000])

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 100000))

    target = n * 10 + 100

    # Generate unique positions
    position = random.sample(range(target), n)
    speed = [random.randint(1, 1000) for _ in range(n)]

    return _format_case(target, position, speed)


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        lines = test.split("\n")
        target = int(lines[0])
        position = json.loads(lines[1])
        print(f"Test {i}: target={target}, {len(position)} cars")
        if len(position) <= 10:
            print(f"  positions: {position}")
        print()

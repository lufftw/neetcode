# generators/1584_min_cost_to_connect_all_points.py
"""
Test Case Generator for Problem 1584 - Min Cost to Connect All Points

LeetCode Constraints:
- 1 <= points.length <= 1000
- -10^6 <= xi, yi <= 10^6
- All pairs (xi, yi) are distinct
"""
import json
import random
from typing import Iterator, Optional, List, Tuple, Set


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Min Cost to Connect All Points.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (points as JSON 2D array)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1
        [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]],
        # LeetCode Example 2
        [[3, 12], [-2, 5], [-4, 1]],
        # Single point
        [[0, 0]],
        # Two points
        [[0, 0], [1, 1]],
        # Collinear points
        [[0, 0], [1, 0], [2, 0], [3, 0]],
        # Square pattern
        [[0, 0], [0, 1], [1, 0], [1, 1]],
    ]

    for points in edge_cases:
        yield json.dumps(points, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random set of distinct points."""
    n = random.randint(5, 50)  # Moderate size for random tests
    return _generate_points(n)


def _generate_points(n: int) -> str:
    """Generate n distinct random points."""
    points: Set[Tuple[int, int]] = set()
    coord_range = 1000  # Keep reasonable for random tests

    while len(points) < n:
        x = random.randint(-coord_range, coord_range)
        y = random.randint(-coord_range, coord_range)
        points.add((x, y))

    return json.dumps([list(p) for p in points], separators=(",", ":"))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Min Cost to Connect All Points:
    - n is the number of points
    - Time complexity is O(n^2 log n) for heap-based Prim or O(n^2) for optimized
    - Generates n distinct points in a bounded region

    Args:
        n: Number of points (will be clamped to [1, 1000])

    Returns:
        str: Test input (points as JSON)
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 1000))

    # Generate n distinct points
    points: Set[Tuple[int, int]] = set()
    # Use larger range for more points to ensure distinctness
    coord_range = max(n * 10, 10000)

    while len(points) < n:
        x = random.randint(-coord_range, coord_range)
        y = random.randint(-coord_range, coord_range)
        points.add((x, y))

    return json.dumps([list(p) for p in points], separators=(",", ":"))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        points = json.loads(test)
        print(f"Test {i}: {len(points)} points")
        if len(points) <= 6:
            for p in points:
                print(f"  {p}")
        print()

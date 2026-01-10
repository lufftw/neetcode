# generators/2013_detect_squares.py
"""
Test Case Generator for Problem 2013 - Detect Squares

LeetCode Constraints:
- point.length == 2
- 0 <= x, y <= 1000
- At most 3000 calls in total will be made to add and count.
"""
import json
import random
from typing import Iterator, Optional, List, Tuple


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Detect Squares.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (operations and arguments as JSON)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1
        (
            ["DetectSquares", "add", "add", "add", "count", "count", "add", "count"],
            [[], [[3, 10]], [[11, 2]], [[3, 2]], [[11, 10]], [[14, 8]], [[11, 2]], [[11, 10]]]
        ),
        # Simple unit square
        (
            ["DetectSquares", "add", "add", "add", "add", "count"],
            [[], [[0, 0]], [[1, 1]], [[0, 1]], [[1, 0]], [[0, 0]]]
        ),
        # No square possible
        (
            ["DetectSquares", "add", "add", "count"],
            [[], [[0, 0]], [[5, 5]], [[0, 0]]]
        ),
        # Multiple squares from same query point
        (
            ["DetectSquares", "add", "add", "add", "add", "add", "add", "count"],
            [[], [[0, 0]], [[2, 2]], [[0, 2]], [[2, 0]], [[4, 4]], [[0, 4]], [[4, 0]], [[0, 0]]]
        ),
    ]

    for ops, args in edge_cases:
        yield f"{json.dumps(ops, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random sequence of operations."""
    num_ops = random.randint(10, 50)

    operations = ["DetectSquares"]
    args = [[]]

    # Add some initial points
    num_adds = random.randint(5, num_ops // 2)
    points_added = []

    for _ in range(num_adds):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        operations.append("add")
        args.append([[x, y]])
        points_added.append([x, y])

    # Mix of adds and counts
    remaining = num_ops - num_adds - 1
    for _ in range(remaining):
        if random.random() < 0.3 and points_added:
            # Count operation
            if random.random() < 0.7:
                # Query a point we've added (more likely to form squares)
                point = random.choice(points_added)
            else:
                # Query a random point
                point = [random.randint(0, 100), random.randint(0, 100)]
            operations.append("count")
            args.append([point])
        else:
            # Add operation
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            operations.append("add")
            args.append([[x, y]])
            points_added.append([x, y])

    return f"{json.dumps(operations, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Detect Squares:
    - n is the total number of operations
    - Count is O(unique_points) per call

    Args:
        n: Number of operations

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(2, min(n, 3000))

    operations = ["DetectSquares"]
    args = [[]]

    # Generate points that can form squares
    points = []
    grid_size = min(100, int(n ** 0.5))

    for i in range(grid_size):
        for j in range(grid_size):
            if len(points) < n // 2:
                points.append([i, j])

    # Add points
    for point in points:
        operations.append("add")
        args.append([point])

    # Add count operations
    remaining = n - len(operations)
    for i in range(remaining):
        operations.append("count")
        args.append([points[i % len(points)]])

    return f"{json.dumps(operations, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        lines = test.split('\n')
        ops = json.loads(lines[0])
        args = json.loads(lines[1])
        print(f"Test {i}:")
        print(f"  operations: {len(ops)} ops")
        print(f"  Sample ops: {ops[:5]}...")
        print()

"""
Test Case Generator for Problem 0149 - Max Points on a Line

LeetCode Constraints:
- 1 <= points.length <= 300
- points[i].length == 2
- -10^4 <= xi, yi <= 10^4
- All points are unique
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    edge_cases = [
        [[1, 1], [2, 2], [3, 3]],                    # All collinear
        [[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]],  # Mixed
        [[0, 0]],                                    # Single point
        [[0, 0], [1, 1]],                            # Two points
        [[0, 0], [0, 1], [0, 2]],                    # Vertical line
        [[0, 0], [1, 0], [2, 0]],                    # Horizontal line
    ]

    for points in edge_cases:
        yield json.dumps(points, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        n = random.randint(1, 30)
        used = set()
        points = []

        # Sometimes generate collinear points
        if random.random() < 0.3 and n >= 3:
            # Generate points on a line
            x0, y0 = random.randint(-100, 100), random.randint(-100, 100)
            dx, dy = random.randint(-5, 5), random.randint(-5, 5)
            if dx == 0 and dy == 0:
                dx = 1
            for i in range(min(n, 10)):
                x, y = x0 + i * dx, y0 + i * dy
                if (x, y) not in used:
                    points.append([x, y])
                    used.add((x, y))
            n = n - len(points)

        # Add random points
        while len(points) < n + len(used):
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            if (x, y) not in used:
                points.append([x, y])
                used.add((x, y))

        random.shuffle(points)
        yield json.dumps(points, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    n = max(1, min(n, 100))

    used = set()
    points = []

    while len(points) < n:
        x = random.randint(-1000, 1000)
        y = random.randint(-1000, 1000)
        if (x, y) not in used:
            points.append([x, y])
            used.add((x, y))

    return json.dumps(points, separators=(',', ':'))

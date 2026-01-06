"""
Test Generator for LeetCode 218: The Skyline Problem
https://leetcode.com/problems/the-skyline-problem/

Generates random building configurations for testing skyline algorithm.

Constraints:
- 1 <= buildings.length <= 10^4
- 0 <= lefti < righti <= 2^31 - 1
- 1 <= heighti <= 2^31 - 1
"""

import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test cases for The Skyline Problem.

    Each test case is a JSON array of buildings [[left, right, height], ...].
    """
    if seed is not None:
        random.seed(seed)

    for i in range(count):
        if i == 0:
            # Edge case: single building
            buildings = [[2, 9, 10]]
        elif i == 1:
            # Edge case: two non-overlapping buildings
            buildings = [[0, 2, 3], [5, 8, 4]]
        elif i == 2:
            # Edge case: two overlapping buildings
            buildings = [[2, 9, 10], [3, 7, 15]]
        elif i == 3:
            # Edge case: nested buildings
            buildings = [[1, 10, 5], [3, 7, 10]]
        elif i == 4:
            # Edge case: adjacent buildings (same height)
            buildings = [[0, 5, 10], [5, 10, 10]]
        elif i == 5:
            # Edge case: adjacent buildings (different heights)
            buildings = [[0, 5, 10], [5, 10, 15]]
        else:
            # Random case
            n = random.randint(3, 50)
            buildings = []
            for _ in range(n):
                left = random.randint(0, 1000)
                width = random.randint(1, 100)
                right = left + width
                height = random.randint(1, 100)
                buildings.append([left, right, height])
            # Sort by left coordinate (as per typical test expectations)
            buildings.sort(key=lambda x: x[0])

        yield json.dumps(buildings)


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with n buildings for complexity estimation.

    Creates buildings with varying overlap to stress-test the algorithm.
    """
    random.seed(42)
    buildings = []

    for i in range(n):
        left = random.randint(0, n * 10)
        width = random.randint(1, n // 2 + 1)
        right = left + width
        height = random.randint(1, 1000)
        buildings.append([left, right, height])

    buildings.sort(key=lambda x: x[0])
    return json.dumps(buildings)


if __name__ == "__main__":
    # Generate sample test cases
    for i, test_input in enumerate(generate(5, seed=42)):
        print(f"Test case {i + 1}:")
        print(test_input)
        print()

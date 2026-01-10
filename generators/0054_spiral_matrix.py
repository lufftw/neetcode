# generators/0054_spiral_matrix.py
"""
Test Case Generator for Problem 0054 - Spiral Matrix

LeetCode Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 10
- -100 <= matrix[i][j] <= 100
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Spiral Matrix.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (JSON 2D array)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[1]],                                      # Single element
        [[1, 2, 3]],                                # Single row
        [[1], [2], [3]],                            # Single column
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],          # LeetCode example 1 (3x3)
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],  # LeetCode example 2 (3x4)
        [[1, 2], [3, 4]],                           # 2x2
        [[1, 2, 3, 4]],                             # 1x4
        [[1], [2], [3], [4]],                       # 4x1
        [[1, 2], [3, 4], [5, 6]],                   # 3x2 (more rows than cols)
        [[1, 2, 3], [4, 5, 6]],                     # 2x3 (more cols than rows)
    ]

    for matrix in edge_cases:
        yield json.dumps(matrix, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Random dimensions
    m = random.randint(1, 10)
    n = random.randint(1, 10)

    # Generate matrix with random values
    matrix = [[random.randint(-100, 100) for _ in range(n)] for _ in range(m)]

    return json.dumps(matrix, separators=(',', ':'))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Spiral Matrix:
    - n is approximately sqrt(total elements)
    - We create an n x n matrix

    Args:
        n: Target dimension (will create n x n matrix)

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 10))

    matrix = [[random.randint(-100, 100) for _ in range(n)] for _ in range(n)]
    return json.dumps(matrix, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        matrix = json.loads(test)
        print(f"Test {i}: {len(matrix)}x{len(matrix[0])} matrix")
        for row in matrix[:3]:
            print(f"  {row}")
        if len(matrix) > 3:
            print("  ...")
        print()

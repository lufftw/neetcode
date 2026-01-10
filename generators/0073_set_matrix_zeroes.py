# generators/0073_set_matrix_zeroes.py
"""
Test Case Generator for Problem 0073 - Set Matrix Zeroes

LeetCode Constraints:
- m == matrix.length
- n == matrix[0].length
- 1 <= m, n <= 200
- -2^31 <= matrix[i][j] <= 2^31 - 1
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Set Matrix Zeroes.

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
        [[0]],                                      # Single zero
        [[1]],                                      # Single non-zero
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],          # LeetCode example 1
        [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]], # LeetCode example 2
        [[1, 0], [0, 1]],                           # Zeros on diagonal
        [[0, 0], [0, 0]],                           # All zeros
        [[1, 2, 3], [4, 5, 6]],                     # No zeros
        [[0]],                                      # 1x1 zero
        [[1, 0, 3]],                                # Single row with zero
        [[1], [0], [3]],                            # Single column with zero
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
    m = random.randint(1, 20)
    n = random.randint(1, 20)

    # Generate matrix
    matrix = [[random.randint(-100, 100) for _ in range(n)] for _ in range(m)]

    # Randomly add some zeros (10-30% of cells)
    num_zeros = random.randint(0, max(1, m * n // 5))
    for _ in range(num_zeros):
        i = random.randint(0, m - 1)
        j = random.randint(0, n - 1)
        matrix[i][j] = 0

    return json.dumps(matrix, separators=(',', ':'))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Set Matrix Zeroes:
    - n is approximately sqrt(total cells)
    - Creates n x n matrix

    Args:
        n: Target dimension

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 200))

    matrix = [[random.randint(-100, 100) for _ in range(n)] for _ in range(n)]

    # Add some zeros
    num_zeros = n // 3
    for _ in range(num_zeros):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        matrix[i][j] = 0

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

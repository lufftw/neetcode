# generators/0048_rotate_image.py
"""
Test Case Generator for Problem 0048 - Rotate Image

LeetCode Constraints:
- n == matrix.length == matrix[i].length
- 1 <= n <= 20
- -1000 <= matrix[i][j] <= 1000
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Rotate Image.

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
        [[1]],                                    # 1x1 matrix
        [[1, 2], [3, 4]],                         # 2x2 matrix
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],        # 3x3 matrix (LeetCode example)
        [[5, 1, 9, 11], [2, 4, 8, 10],            # 4x4 matrix (LeetCode example)
         [13, 3, 6, 7], [15, 14, 12, 16]],
        _generate_matrix(5),                      # 5x5 matrix
        _generate_matrix(20),                     # Maximum size
        _generate_matrix_sequential(3),           # Sequential values for easy verification
        _generate_matrix_sequential(4),
    ]

    for matrix in edge_cases:
        yield json.dumps(matrix, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_matrix(n: int) -> List[List[int]]:
    """Generate an n x n matrix with random values."""
    return [[random.randint(-1000, 1000) for _ in range(n)] for _ in range(n)]


def _generate_matrix_sequential(n: int) -> List[List[int]]:
    """Generate an n x n matrix with sequential values 1, 2, 3, ..."""
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]


def _generate_case() -> str:
    """Generate a single random test case."""
    # Weighted distribution: more medium-sized matrices
    n = random.choices(
        population=[1, 2, 3, 4, 5, 7, 10, 15, 20],
        weights=[1, 2, 3, 4, 4, 3, 2, 1, 1],
        k=1
    )[0]

    matrix = _generate_matrix(n)
    return json.dumps(matrix, separators=(',', ':'))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Rotate Image:
    - n is the matrix dimension
    - Complexity is O(n²) for both time and processing

    Args:
        n: Target matrix dimension

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 20))
    matrix = _generate_matrix(n)
    return json.dumps(matrix, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        matrix = json.loads(test)
        print(f"Test {i}: {len(matrix)}x{len(matrix)} matrix")
        for row in matrix:
            print(f"  {row}")
        print()

# generators/0542_01_matrix.py
"""
Random test generator for LC 542: 01 Matrix

Constraints:
- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 10^4
- 1 <= m * n <= 10^4
- mat[i][j] is either 0 or 1
- There is at least one 0 in mat
"""
import random
import json
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test cases for 01 Matrix.

    Each test case is a binary matrix with at least one 0.

    Strategy:
    - Generate random binary matrices
    - Ensure at least one 0 exists (constraint)
    - Vary density of 0s and 1s
    """
    if seed is not None:
        random.seed(seed)

    for i in range(count):
        if i == 0:
            # Edge case: single cell with 0
            yield json.dumps([[0]], separators=(',', ':'))
        elif i == 1:
            # Edge case: all zeros
            yield json.dumps([[0, 0], [0, 0]], separators=(',', ':'))
        elif i == 2:
            # Edge case: example from problem - surrounded by zeros
            yield json.dumps([[0, 0, 0], [0, 1, 0], [0, 0, 0]], separators=(',', ':'))
        elif i == 3:
            # Edge case: example from problem - chain of ones
            yield json.dumps([[0, 0, 0], [0, 1, 0], [1, 1, 1]], separators=(',', ':'))
        elif i == 4:
            # Edge case: single row
            yield json.dumps([[0, 1, 1, 1, 0]], separators=(',', ':'))
        elif i == 5:
            # Edge case: single column
            yield json.dumps([[0], [1], [1], [1], [0]], separators=(',', ':'))
        else:
            yield _generate_random_matrix()


def _generate_random_matrix() -> str:
    """Generate a random valid binary matrix."""
    # Keep size reasonable for testing (m * n <= 10^4)
    total_cells = random.randint(10, 100)
    rows = random.randint(2, min(20, total_cells))
    cols = max(2, total_cells // rows)

    # Probability of 0 (vary from sparse to dense)
    zero_prob = random.uniform(0.2, 0.8)

    mat = []
    has_zero = False

    for r in range(rows):
        row = []
        for c in range(cols):
            if random.random() < zero_prob:
                row.append(0)
                has_zero = True
            else:
                row.append(1)
        mat.append(row)

    # Ensure at least one 0 (constraint)
    if not has_zero:
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        mat[r][c] = 0

    return json.dumps(mat, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.

    Creates a sqrt(n) x sqrt(n) grid (approximately n cells).
    Places zeros at corners for maximum distance paths.
    """
    import math
    random.seed(42)  # Fixed seed for reproducibility

    # Create approximately n cells
    side = max(2, int(math.sqrt(n)))
    rows = cols = side

    # Initialize with all 1s
    mat = [[1] * cols for _ in range(rows)]

    # Place zeros at corners
    mat[0][0] = 0
    mat[0][cols - 1] = 0
    mat[rows - 1][0] = 0
    mat[rows - 1][cols - 1] = 0

    # Add some random zeros (20% of cells)
    zero_count = rows * cols // 5
    for _ in range(zero_count):
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        mat[r][c] = 0

    return json.dumps(mat, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases for 01 Matrix:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")

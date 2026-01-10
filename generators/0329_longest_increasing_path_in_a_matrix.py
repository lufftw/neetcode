# generators/0329_longest_increasing_path_in_a_matrix.py
"""
Test Case Generator for Problem 0329 - Longest Increasing Path in a Matrix

LeetCode Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 200
- 0 <= matrix[i][j] <= 2^31 - 1
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Longest Increasing Path in a Matrix.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (matrix as JSON 2D array)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1
        [[9, 9, 4], [6, 6, 8], [2, 1, 1]],
        # LeetCode Example 2
        [[3, 4, 5], [3, 2, 6], [2, 2, 1]],
        # LeetCode Example 3: single cell
        [[1]],
        # Single row
        [[1, 2, 3, 4, 5]],
        # Single column
        [[1], [2], [3], [4]],
        # All same values
        [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
        # Strictly increasing snake
        [[1, 2, 3], [6, 5, 4], [7, 8, 9]],
    ]

    for matrix in edge_cases:
        yield json.dumps(matrix, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random matrix."""
    m = random.randint(3, 20)
    n = random.randint(3, 20)

    matrix = [[random.randint(0, 100) for _ in range(n)] for _ in range(m)]

    return json.dumps(matrix, separators=(",", ":"))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Longest Increasing Path:
    - n is the total number of cells (m * n)
    - Time complexity is O(mn)

    Args:
        n: Total cells (will use sqrt(n) x sqrt(n) matrix, clamped)

    Returns:
        str: Test input (matrix as JSON)
    """
    # Determine dimensions
    side = max(1, min(int(n**0.5), 200))
    m, n = side, side

    # Clamp to constraints
    m = max(1, min(m, 200))
    n = max(1, min(n, 200))

    # Generate random matrix
    matrix = [[random.randint(0, 1000) for _ in range(n)] for _ in range(m)]

    return json.dumps(matrix, separators=(",", ":"))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        matrix = json.loads(test)
        m, n = len(matrix), len(matrix[0])
        print(f"Test {i}: {m}x{n} matrix")
        if m * n <= 25:
            for row in matrix:
                print(f"  {row}")
        print()

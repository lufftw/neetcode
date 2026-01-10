# generators/0074_search_a_2d_matrix.py
"""
Test Case Generator for Problem 0074 - Search a 2D Matrix

LeetCode Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 100
- -10^4 <= matrix[i][j], target <= 10^4
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Search a 2D Matrix.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (matrix JSON + target)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3),   # Example 1: found
        ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13),  # Example 2: not found
        ([[1]], 1),                                                # Single element found
        ([[1]], 0),                                                # Single element not found
        ([[1, 3]], 3),                                             # Single row found
        ([[1], [3]], 3),                                           # Single column found
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 5),                    # Middle element
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1),                    # First element
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 9),                    # Last element
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 10),                   # Greater than all
    ]

    for matrix, target in edge_cases:
        yield f"{json.dumps(matrix, separators=(',', ':'))}\n{target}"
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

    # Generate sorted matrix
    matrix = _generate_sorted_matrix(m, n)

    # Randomly choose target: 50% in matrix, 50% not in matrix
    if random.random() < 0.5:
        # Target in matrix
        row = random.randint(0, m - 1)
        col = random.randint(0, n - 1)
        target = matrix[row][col]
    else:
        # Target not in matrix
        all_values = set(val for row in matrix for val in row)
        target = random.randint(-10000, 10000)
        # Make sure it's not in matrix
        while target in all_values:
            target = random.randint(-10000, 10000)

    return f"{json.dumps(matrix, separators=(',', ':'))}\n{target}"


def _generate_sorted_matrix(m: int, n: int) -> List[List[int]]:
    """Generate a valid sorted matrix for this problem."""
    # Generate m*n unique sorted values
    total = m * n
    start = random.randint(-10000, 10000 - total * 2)
    values = []
    current = start
    for _ in range(total):
        current += random.randint(1, 3)  # Ensure strictly increasing
        values.append(current)

    # Split into rows
    matrix = []
    for i in range(m):
        row = values[i * n:(i + 1) * n]
        matrix.append(row)

    return matrix


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Search a 2D Matrix:
    - n is approximately sqrt(total elements)
    - Creates n x n matrix

    Args:
        n: Target dimension

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 100))

    matrix = _generate_sorted_matrix(n, n)
    # Choose target not in matrix for worst case
    target = matrix[0][0] - 1

    return f"{json.dumps(matrix, separators=(',', ':'))}\n{target}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        lines = test.split('\n')
        matrix = json.loads(lines[0])
        target = int(lines[1])
        print(f"Test {i}: {len(matrix)}x{len(matrix[0])} matrix, target={target}")
        for row in matrix[:3]:
            print(f"  {row}")
        if len(matrix) > 3:
            print("  ...")
        print()

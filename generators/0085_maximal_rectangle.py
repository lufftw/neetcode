# generators/0085_maximal_rectangle.py
"""
Test Case Generator for Problem 0085 - Maximal Rectangle

LeetCode Constraints:
- rows == matrix.length
- cols == matrix[i].length
- 1 <= rows, cols <= 200
- matrix[i][j] is '0' or '1'

Time Complexity: O(rows * cols) with histogram stack
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Maximal Rectangle.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in JSON format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"],
         ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]],  # Classic
        [["0"]],                    # Single zero
        [["1"]],                    # Single one
        [["0", "0"], ["0", "0"]],   # All zeros
        [["1", "1"], ["1", "1"]],   # All ones (2x2)
        [["1", "0", "1"]],          # Single row
        [["1"], ["0"], ["1"]],      # Single column
    ]

    for edge in edge_cases:
        yield json.dumps(edge, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        rows = random.randint(1, 100)
        cols = random.randint(1, 100)
        yield _generate_case(rows, cols)


def _generate_case(rows: int, cols: int) -> str:
    """Generate a single random test case."""
    matrix = [
        [random.choice(["0", "1"]) for _ in range(cols)]
        for _ in range(rows)
    ]
    return json.dumps(matrix, separators=(",", ":"))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size for complexity estimation."""
    # For n elements, create roughly sqrt(n) x sqrt(n) matrix
    import math
    side = max(1, int(math.sqrt(n)))
    return _generate_case(side, side)

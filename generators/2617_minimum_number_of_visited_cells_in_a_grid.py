"""
Test Case Generator for Problem 2617 - Minimum Number of Visited Cells in a Grid

LeetCode Constraints:
- 1 <= m, n <= 10^5
- 1 <= m * n <= 10^5
- 0 <= grid[i][j] < m * n
- grid[m-1][n-1] == 0
"""
import json
import random
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test case inputs."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [[3,4,2,1],[4,2,3,1],[2,1,0,0],[2,4,0,0]],  # Example 1
        [[3,4,2,1],[4,2,1,1],[2,1,1,0],[3,4,1,0]],  # Example 2
        [[2,1,0],[1,0,0]],                          # Example 3: no path
        [[0]],                                       # Single cell
        [[1,0]],                                     # 1x2
        [[1],[0]],                                   # 2x1
        [[1,1,0],[1,1,0],[1,1,0]],                  # 3x3
    ]

    for case in edge_cases:
        yield json.dumps(case, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        # Keep grid small for testing
        m = random.randint(2, 10)
        n = random.randint(2, 10)

        grid = []
        for i in range(m):
            row = []
            for j in range(n):
                if i == m - 1 and j == n - 1:
                    row.append(0)  # Bottom-right must be 0
                else:
                    max_val = max(m - i - 1, n - j - 1)
                    row.append(random.randint(0, max_val + 1))
            grid.append(row)

        yield json.dumps(grid, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific total cells n."""
    n = max(1, min(n, 1000))

    # Create roughly square grid
    m = int(n ** 0.5)
    cols = n // m

    grid = []
    for i in range(m):
        row = []
        for j in range(cols):
            if i == m - 1 and j == cols - 1:
                row.append(0)
            else:
                max_val = max(m - i - 1, cols - j - 1)
                row.append(random.randint(0, max_val + 1))
        grid.append(row)

    return json.dumps(grid, separators=(',', ':'))


if __name__ == "__main__":
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"--- Test {i} ---")
        print(test[:100] + "..." if len(test) > 100 else test)
        print()

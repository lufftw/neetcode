# generators/0286_walls_and_gates.py
"""
Random test generator for LC 286: Walls and Gates

Constraints:
- m == rooms.length
- n == rooms[i].length
- 1 <= m, n <= 250
- rooms[i][j] is -1 (wall), 0 (gate), or 2147483647 (INF/empty)
"""
import random
import json
from typing import Iterator, Optional


INF = 2147483647


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test cases for Walls and Gates.

    Each test case is a 2D grid with:
    - -1: walls (obstacles)
    - 0: gates (destinations)
    - INF: empty rooms (need distance calculation)

    Strategy:
    - Generate grid with random walls, gates, and empty rooms
    - Ensure at least one gate and one empty room for interesting cases
    """
    if seed is not None:
        random.seed(seed)

    for i in range(count):
        if i == 0:
            # Edge case: single cell gate
            yield json.dumps([[0]], separators=(',', ':'))
        elif i == 1:
            # Edge case: single cell wall
            yield json.dumps([[-1]], separators=(',', ':'))
        elif i == 2:
            # Edge case: single empty room (unreachable)
            yield json.dumps([[INF]], separators=(',', ':'))
        elif i == 3:
            # Edge case: example from problem description
            yield json.dumps([
                [INF, -1, 0, INF],
                [INF, INF, INF, -1],
                [INF, -1, INF, -1],
                [0, -1, INF, INF]
            ], separators=(',', ':'))
        else:
            yield _generate_random_grid()


def _generate_random_grid() -> str:
    """Generate a random valid grid."""
    rows = random.randint(2, 20)
    cols = random.randint(2, 20)

    # Probabilities for cell types
    # wall_prob: chance of -1
    # gate_prob: chance of 0
    # remaining: INF (empty room)
    wall_prob = random.uniform(0.1, 0.3)
    gate_prob = random.uniform(0.05, 0.15)

    grid = []
    has_gate = False
    has_empty = False

    for r in range(rows):
        row = []
        for c in range(cols):
            rand_val = random.random()
            if rand_val < wall_prob:
                row.append(-1)
            elif rand_val < wall_prob + gate_prob:
                row.append(0)
                has_gate = True
            else:
                row.append(INF)
                has_empty = True
        grid.append(row)

    # Ensure at least one gate
    if not has_gate:
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        grid[r][c] = 0

    # Ensure at least one empty room (for interesting test)
    if not has_empty:
        # Find a non-gate cell and make it empty
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 0:
                    grid[r][c] = INF
                    has_empty = True
                    break
            if has_empty:
                break

    return json.dumps(grid, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.

    Creates an n x n grid with scattered gates.
    """
    random.seed(42)  # Fixed seed for reproducibility

    # Create n x n grid
    grid = [[INF] * n for _ in range(n)]

    # Place gates at corners and center
    grid[0][0] = 0
    grid[0][n - 1] = 0
    grid[n - 1][0] = 0
    grid[n - 1][n - 1] = 0
    grid[n // 2][n // 2] = 0

    # Add some random walls (10% of cells)
    wall_count = n * n // 10
    for _ in range(wall_count):
        r, c = random.randint(0, n - 1), random.randint(0, n - 1)
        if grid[r][c] == INF:
            grid[r][c] = -1

    return json.dumps(grid, separators=(',', ':'))


if __name__ == "__main__":
    print("Sample test cases for Walls and Gates:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test[:80]}{'...' if len(test) > 80 else ''}")

## Variation: N-Queens (LeetCode 51/52)

> **Problem**: Place n queens on an n×n board so no two queens attack each other.  
> **Sub-Pattern**: Constraint satisfaction with row-by-row placement.  
> **Key Insight**: Track columns and diagonals as constraint sets.

### Implementation

```python
def solve_n_queens(n: int) -> list[list[str]]:
    """
    Find all solutions to the N-Queens puzzle.
    
    Algorithm:
    - Place queens row by row (one queen per row guaranteed)
    - Track three constraints:
      1. Columns: No two queens in same column
      2. Main diagonals (↘): row - col is constant
      3. Anti-diagonals (↙): row + col is constant
    - Use hash sets for O(1) constraint checking
    
    Key Insight:
    - Row-by-row placement eliminates row conflicts by construction
    - Only need to check column and diagonal conflicts
    
    Time Complexity: O(n!)
        - At row 0: n choices
        - At row 1: at most n-1 choices
        - ... and so on
    
    Space Complexity: O(n) for constraint sets and recursion
    
    Args:
        n: Board size
        
    Returns:
        All valid board configurations as string arrays
    """
    results: list[list[str]] = []
    
    # State: queen_cols[row] = column where queen is placed
    queen_cols: list[int] = [-1] * n
    
    # Constraint sets for O(1) conflict checking
    used_cols: set[int] = set()
    used_diag_main: set[int] = set()   # row - col
    used_diag_anti: set[int] = set()   # row + col
    
    def backtrack(row: int) -> None:
        # BASE CASE: All queens placed
        if row == n:
            results.append(build_board(queen_cols, n))
            return
        
        # Try each column in current row
        for col in range(n):
            # Calculate diagonal identifiers
            diag_main = row - col
            diag_anti = row + col
            
            # CONSTRAINT CHECK (pruning)
            if col in used_cols:
                continue
            if diag_main in used_diag_main:
                continue
            if diag_anti in used_diag_anti:
                continue
            
            # CHOOSE: Place queen
            queen_cols[row] = col
            used_cols.add(col)
            used_diag_main.add(diag_main)
            used_diag_anti.add(diag_anti)
            
            # EXPLORE: Move to next row
            backtrack(row + 1)
            
            # UNCHOOSE: Remove queen
            queen_cols[row] = -1
            used_cols.discard(col)
            used_diag_main.discard(diag_main)
            used_diag_anti.discard(diag_anti)
    
    backtrack(0)
    return results


def build_board(queen_cols: list[int], n: int) -> list[str]:
    """Convert queen positions to board representation."""
    board = []
    for col in queen_cols:
        row = '.' * col + 'Q' + '.' * (n - col - 1)
        board.append(row)
    return board
```

### Diagonal Identification

```
Main diagonal (↘): cells where row - col is constant
    (0,0) (1,1) (2,2) → row - col = 0
    (0,1) (1,2) (2,3) → row - col = -1
    (1,0) (2,1) (3,2) → row - col = 1

Anti-diagonal (↙): cells where row + col is constant
    (0,2) (1,1) (2,0) → row + col = 2
    (0,3) (1,2) (2,1) (3,0) → row + col = 3
```

### N-Queens II (Count Only)

```python
def total_n_queens(n: int) -> int:
    """Count solutions without building boards."""
    count = 0
    
    used_cols: set[int] = set()
    used_diag_main: set[int] = set()
    used_diag_anti: set[int] = set()
    
    def backtrack(row: int) -> None:
        nonlocal count
        if row == n:
            count += 1
            return
        
        for col in range(n):
            dm, da = row - col, row + col
            if col in used_cols or dm in used_diag_main or da in used_diag_anti:
                continue
            
            used_cols.add(col)
            used_diag_main.add(dm)
            used_diag_anti.add(da)
            
            backtrack(row + 1)
            
            used_cols.discard(col)
            used_diag_main.discard(dm)
            used_diag_anti.discard(da)
    
    backtrack(0)
    return count
```


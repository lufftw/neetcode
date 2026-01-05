## Range Sum Query 2D (LeetCode 304)

> **Problem**: Handle multiple rectangle sum queries on an immutable 2D matrix.
> **Invariant**: `prefix[i][j]` = sum of all elements in rectangle from (0,0) to (i-1, j-1).
> **Role**: 2D EXTENSION using inclusion-exclusion principle.

### 2D Prefix Sum Principle

For a 2D matrix, prefix sum extends naturally using inclusion-exclusion:

```
Building prefix[i][j]:
┌─────┬───────────┐
│  A  │     B     │
├─────┼───────────┤
│  C  │ (i-1,j-1) │
└─────┴───────────┘

prefix[i][j] = matrix[i-1][j-1] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]
             = current cell    + top          + left          - overlap (counted twice)
```

### Rectangle Sum Query

```
Querying region from (row1, col1) to (row2, col2):
┌─────────────────────────┐
│  A  │        B          │
├─────┼──────────┬────────┤
│     │ ████████ │        │
│  C  │ █TARGET█ │   D    │
│     │ ████████ │        │
├─────┴──────────┴────────┤
│           E             │
└─────────────────────────┘

TARGET = Total - B - C + A
       = prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]
```

### Implementation

```python
class NumMatrix:
    """
    2D range sum query with O(m*n) preprocessing and O(1) queries.

    Prefix Sum 2D:
    - Extra row and column of zeros simplify boundary handling
    - prefix[i][j] = sum of rectangle from (0,0) to (i-1, j-1)
    - Uses inclusion-exclusion principle for both building and querying

    Time: O(m*n) init, O(1) query | Space: O(m*n)
    """
    def __init__(self, matrix: List[List[int]]):
        if not matrix or not matrix[0]:
            self.prefix_sum = [[0]]
            return

        row_count, col_count = len(matrix), len(matrix[0])

        # Extra row and column of zeros for boundary handling
        self.prefix_sum = [[0] * (col_count + 1) for _ in range(row_count + 1)]

        # Build prefix sum using inclusion-exclusion
        for row in range(1, row_count + 1):
            for col in range(1, col_count + 1):
                self.prefix_sum[row][col] = (
                    matrix[row - 1][col - 1]
                    + self.prefix_sum[row - 1][col]      # Top rectangle
                    + self.prefix_sum[row][col - 1]      # Left rectangle
                    - self.prefix_sum[row - 1][col - 1]  # Subtract overlap
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self.prefix_sum[row2 + 1][col2 + 1]  # Total (origin to bottom-right)
            - self.prefix_sum[row1][col2 + 1]    # Subtract top strip
            - self.prefix_sum[row2 + 1][col1]    # Subtract left strip
            + self.prefix_sum[row1][col1]        # Add back top-left (subtracted twice)
        )
```

### Trace Example

```
matrix = [
  [3, 0, 1, 4, 2],
  [5, 6, 3, 2, 1],
  [1, 2, 0, 1, 5]
]

prefix (with boundary zeros):
[0,  0,  0,  0,  0,  0]
[0,  3,  3,  4,  8, 10]
[0,  8, 14, 18, 24, 27]
[0,  9, 17, 21, 28, 36]

Query sumRegion(1, 1, 2, 2):
= prefix[3][3] - prefix[1][3] - prefix[3][1] + prefix[1][1]
= 21 - 4 - 9 + 3
= 11

Verification: 6 + 3 + 2 + 0 = 11 ✓
```



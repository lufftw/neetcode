# 286. Walls and Gates

## Problem Link
https://leetcode.com/problems/walls-and-gates/

## Difficulty
Medium

## Tags
- Array
- Breadth-First Search
- Matrix

## Pattern
GridBFSMultiSource - Fill with Distance

## API Kernel
`GridBFSMultiSource`

## Problem Summary

Given an m × n grid where:
- `-1` = wall (obstacle)
- `0` = gate (destination)
- `INF` (2³¹ - 1) = empty room

Fill each empty room with the distance to its nearest gate. If impossible to reach a gate, leave as INF.

## Key Insight

**Reverse the perspective**: Instead of computing distance FROM each room TO gates, compute distance FROM gates TO rooms. Start BFS from all gates simultaneously - each room gets filled with the distance when first reached (which is guaranteed to be the minimum due to BFS properties).

```
Initial:              After BFS:
INF  -1   0  INF      3  -1   0   1
INF INF INF  -1   →   2   2   1  -1
INF  -1 INF  -1       1  -1   2  -1
  0  -1 INF INF       0  -1   3   4
```

## Delta from Base Template

| Aspect | Rotting Oranges | Walls and Gates |
|--------|-----------------|-----------------|
| Source | Rotten (2) | Gate (0) |
| Target | Fresh (1) | Empty (INF) |
| Marking | Change to 2 | Store distance |
| Result | Max time / -1 | Modified grid |

Key change: Instead of just marking visited, we **store the distance value** in each cell.

## Template Mapping

```python
from collections import deque
from typing import List

class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Modify rooms in-place to store distance to nearest gate.
        """
        if not rooms or not rooms[0]:
            return

        INF = 2147483647
        rows, cols = len(rooms), len(rooms[0])
        queue = deque()

        # Phase 1: Initialize - all gates are sources at distance 0
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:  # Gate found
                    queue.append((r, c))

        # Phase 2: BFS from all gates simultaneously
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            r, c = queue.popleft()

            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    # Only process empty rooms (INF)
                    # Rooms already filled have shorter distance
                    if rooms[nr][nc] == INF:
                        rooms[nr][nc] = rooms[r][c] + 1
                        queue.append((nr, nc))
```

## Complexity
- Time: O(m × n) - each cell visited at most once
- Space: O(m × n) - queue can hold all cells in worst case

## Why This Problem Second?

Walls and Gates introduces **distance storage** while maintaining the core multi-source BFS structure:

1. **Different source identification**: Gates (0) vs rotten oranges (2)
2. **Distance propagation**: `new_dist = current_dist + 1` pattern
3. **Natural visited check**: `INF` cells are unvisited, non-INF are visited
4. **In-place modification**: Common grid modification pattern

## Common Mistakes

1. **BFS from each empty room** - O(m²n²) vs O(mn) with multi-source from gates
2. **Using separate visited set** - The grid itself tracks visited status (INF → distance)
3. **Processing walls** - Must skip `-1` cells
4. **Re-processing already filled rooms** - Check `rooms[nr][nc] == INF` before updating

## Related Problems
- LC 994: Rotting Oranges (propagation timer)
- LC 542: 01 Matrix (similar distance field)
- LC 1162: As Far from Land as Possible (inverse: distance from land)



# 994. Rotting Oranges

## Problem Link
https://leetcode.com/problems/rotting-oranges/

## Difficulty
Medium

## Tags
- Array
- Breadth-First Search
- Matrix

## Pattern
GridBFSMultiSource - Propagation Timer

## API Kernel
`GridBFSMultiSource`

## Problem Summary

Given an m × n grid where:
- `0` = empty cell
- `1` = fresh orange
- `2` = rotten orange

Every minute, fresh oranges adjacent (4-directionally) to rotten oranges become rotten. Return the minimum minutes until no fresh oranges remain, or -1 if impossible.

## Key Insight

All rotten oranges spread infection **simultaneously** each minute. This is the textbook multi-source BFS scenario: initialize the queue with all rotten oranges (sources), then expand level-by-level. Each BFS level represents one minute of propagation.

```
Initial:          After 1 min:      After 2 min:
2 1 1             2 2 1             2 2 2
1 1 0      →      2 1 0      →      2 2 0
0 1 1             0 1 1             0 2 1

                  After 3 min:      After 4 min:
                  2 2 2             2 2 2
           →      2 2 0      →      2 2 0
                  0 2 2             0 2 2
```

## Template Mapping

```python
from collections import deque
from typing import List

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh_count = 0

        # Phase 1: Initialize sources and count targets
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:      # Source: rotten orange
                    queue.append((r, c))
                elif grid[r][c] == 1:    # Target: fresh orange
                    fresh_count += 1

        # Early exit: no fresh oranges
        if fresh_count == 0:
            return 0

        # Phase 2: Multi-source BFS expansion
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        minutes = 0

        while queue:
            # Process entire current level
            for _ in range(len(queue)):
                r, c = queue.popleft()

                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc

                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == 1:  # Fresh orange found
                            grid[nr][nc] = 2   # Mark as rotten (visited)
                            queue.append((nr, nc))
                            fresh_count -= 1

            minutes += 1

        # Phase 3: Check if all targets reached
        # Subtract 1 because we count one extra level after last infection
        return minutes - 1 if fresh_count == 0 else -1
```

## Complexity
- Time: O(m × n) - each cell visited at most once
- Space: O(m × n) - queue can hold all cells in worst case

## Why This Problem First?

Rotting Oranges is the **canonical multi-source BFS problem** because:

1. **Clear physical metaphor**: Infection spreading is intuitive
2. **Explicit simultaneity**: "Every minute" makes multi-source nature obvious
3. **Simple state space**: Only 3 cell values (0, 1, 2)
4. **Direct BFS level = time mapping**: Each level is exactly one minute

Once you understand this problem, the pattern transfers directly to other grid propagation scenarios.

## Common Mistakes

1. **Starting BFS from one rotten orange** - Must start from ALL rotten oranges simultaneously
2. **Forgetting the -1 adjustment** - The while loop counts one extra iteration after the last spread
3. **Not handling edge cases** - Empty grid, no fresh oranges, no rotten oranges
4. **Modifying grid before full level processing** - Must process entire level before incrementing time

## Related Problems
- LC 286: Walls and Gates (fill with distances)
- LC 542: 01 Matrix (distance to nearest 0)
- LC 1162: As Far from Land as Possible (max distance to land)



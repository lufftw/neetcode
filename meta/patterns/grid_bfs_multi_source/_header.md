# Multi-Source BFS on Grids: Complete Reference

> **API Kernel**: `GridBFSMultiSource`
> **Core Mechanism**: Simultaneous wavefront propagation from multiple source cells, computing minimum distances or spread times in a single BFS traversal.

This document presents the **canonical multi-source BFS templates** for grid-based propagation problems. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Core Concepts

### Why Multi-Source BFS?

Traditional single-source BFS starts from one cell and expands outward. Multi-source BFS starts from **all source cells simultaneously**, processing them as if they were a single "super-source" at distance 0.

This technique is essential when:
- Multiple origins propagate simultaneously (infections, fire spread)
- Computing distances to the **nearest** source among many
- Level-by-level expansion from a set of starting points

### The Key Insight

> **All sources start at the same "time" (distance 0).**

Instead of running BFS from each source separately (O(k * m * n) for k sources), we initialize the queue with all sources and run a single BFS (O(m * n)).

```
Single-Source BFS:           Multi-Source BFS:
    S                        S . . . S
    |                        |       |
  1 1 1                    0 1 1 1 0
  |   |                      | | | |
2 2 2 2 2                  1 1 1 1 1
```

### Universal Multi-Source BFS Template

```python
from collections import deque
from typing import List

def multi_source_bfs(grid: List[List[int]], is_source, is_valid_target) -> int:
    """
    Multi-source BFS template for grid problems.

    Core invariant:
    - All sources start at distance 0 (initialized in queue simultaneously)
    - BFS guarantees shortest distance property
    - Each cell is visited exactly once

    Args:
        grid: The 2D grid
        is_source: Function to identify source cells
        is_valid_target: Function to identify cells that can be reached/modified

    Returns:
        Maximum distance reached (or -1 if targets remain unreached)
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    queue = deque()

    # Phase 1: Initialize - collect all sources at distance 0
    target_count = 0
    for r in range(rows):
        for c in range(cols):
            if is_source(grid[r][c]):
                queue.append((r, c))
            elif is_valid_target(grid[r][c]):
                target_count += 1

    # Early termination: no targets to process
    if target_count == 0:
        return 0

    # Phase 2: BFS expansion
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    distance = 0

    while queue:
        # Process all cells at current distance level
        for _ in range(len(queue)):
            r, c = queue.popleft()

            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc

                # Boundary check and valid target check
                if 0 <= nr < rows and 0 <= nc < cols:
                    if is_valid_target(grid[nr][nc]):
                        # Mark as visited (convert to source state)
                        grid[nr][nc] = grid[r][c]  # Or mark with distance
                        queue.append((nr, nc))
                        target_count -= 1

        distance += 1

    # Phase 3: Return result based on problem type
    return distance - 1 if target_count == 0 else -1
```

### Pattern Variants

| Variant | State Tracking | Use Case | Example |
|---------|---------------|----------|---------|
| **Propagation Timer** | Count levels | "How long until all X?" | Rotting Oranges |
| **Fill/Replace** | Mark with source value | "Fill from boundaries" | Walls and Gates |
| **Distance Field** | Store min distance | "Distance to nearest X" | 01 Matrix |

### Grid Traversal Helpers

```python
# 4-directional movement (standard for most grid BFS)
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    """Check if coordinates are within grid boundaries."""
    return 0 <= r < rows and 0 <= c < cols

def get_neighbors(r: int, c: int, rows: int, cols: int):
    """Generate valid 4-directional neighbors."""
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc
```

### When to Use Multi-Source BFS

| Scenario | Single-Source | Multi-Source |
|----------|---------------|--------------|
| One starting point | ✅ | ❌ Overkill |
| Multiple starting points, need all distances | ✅ (run k times) | ✅ Better |
| Multiple starting points, need min distance | ❌ Inefficient | ✅ Perfect |
| Simultaneous propagation | ❌ Cannot model | ✅ Natural fit |

### Complexity Analysis

For an m × n grid with k source cells:

| Approach | Time | Space |
|----------|------|-------|
| Single-source BFS × k | O(k * m * n) | O(m * n) |
| Multi-source BFS | O(m * n) | O(m * n) |

The multi-source approach visits each cell exactly once regardless of source count.



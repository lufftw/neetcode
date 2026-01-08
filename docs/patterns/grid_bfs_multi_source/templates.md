# Multi-Source BFS on Grids: Complete Reference

> **API Kernel**: `GridBFSMultiSource`
> **Core Mechanism**: Simultaneous wavefront propagation from multiple source cells, computing minimum distances or spread times in a single BFS traversal.

This document presents the **canonical multi-source BFS templates** for grid-based propagation problems. Each implementation follows consistent naming conventions and includes detailed logic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Problem Link](#2-problem-link)
3. [Difficulty](#3-difficulty)
4. [Tags](#4-tags)
5. [Pattern](#5-pattern)
6. [API Kernel](#6-api-kernel)
7. [Problem Summary](#7-problem-summary)
8. [Key Insight](#8-key-insight)
9. [Template Mapping](#9-template-mapping)
10. [Complexity](#10-complexity)
11. [Why This Problem First?](#11-why-this-problem-first)
12. [Common Mistakes](#12-common-mistakes)
13. [Related Problems](#13-related-problems)
14. [Problem Link](#14-problem-link)
15. [Difficulty](#15-difficulty)
16. [Tags](#16-tags)
17. [Pattern](#17-pattern)
18. [API Kernel](#18-api-kernel)
19. [Problem Summary](#19-problem-summary)
20. [Key Insight](#20-key-insight)
21. [Delta from Base Template](#21-delta-from-base-template)
22. [Template Mapping](#22-template-mapping)
23. [Complexity](#23-complexity)
24. [Why This Problem Second?](#24-why-this-problem-second)
25. [Common Mistakes](#25-common-mistakes)
26. [Related Problems](#26-related-problems)
27. [Problem Link](#27-problem-link)
28. [Difficulty](#28-difficulty)
29. [Tags](#29-tags)
30. [Pattern](#30-pattern)
31. [API Kernel](#31-api-kernel)
32. [Problem Summary](#32-problem-summary)
33. [Key Insight](#33-key-insight)
34. [Delta from Base Template](#34-delta-from-base-template)
35. [Template Mapping](#35-template-mapping)
36. [Alternative: In-Place Modification](#36-alternative-in-place-modification)
37. [Complexity](#37-complexity)
38. [Why This Problem Third?](#38-why-this-problem-third)
39. [Common Mistakes](#39-common-mistakes)
40. [DP Alternative](#40-dp-alternative)
41. [Related Problems](#41-related-problems)
42. [Problem Comparison](#42-problem-comparison)
43. [State Tracking Comparison](#43-state-tracking-comparison)
44. [Pattern Evolution](#44-pattern-evolution)
45. [Code Structure Comparison](#45-code-structure-comparison)
46. [Decision Tree](#46-decision-tree)
47. [Pattern Selection Guide](#47-pattern-selection-guide)
48. [Problem Identification Checklist](#48-problem-identification-checklist)
49. [Quick Pattern Recognition](#49-quick-pattern-recognition)
50. [Universal Templates](#50-universal-templates)

---

## 1. Core Concepts

### 1.1 Why Multi-Source BFS?

Traditional single-source BFS starts from one cell and expands outward. Multi-source BFS starts from **all source cells simultaneously**, processing them as if they were a single "super-source" at distance 0.

This technique is essential when:
- Multiple origins propagate simultaneously (infections, fire spread)
- Computing distances to the **nearest** source among many
- Level-by-level expansion from a set of starting points

### 1.2 The Key Insight

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

### 1.3 Universal Multi-Source BFS Template

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

### 1.4 Pattern Variants

| Variant | State Tracking | Use Case | Example |
|---------|---------------|----------|---------|
| **Propagation Timer** | Count levels | "How long until all X?" | Rotting Oranges |
| **Fill/Replace** | Mark with source value | "Fill from boundaries" | Walls and Gates |
| **Distance Field** | Store min distance | "Distance to nearest X" | 01 Matrix |

### 1.5 Grid Traversal Helpers

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

### 1.6 When to Use Multi-Source BFS

| Scenario | Single-Source | Multi-Source |
|----------|---------------|--------------|
| One starting point | ✅ | ❌ Overkill |
| Multiple starting points, need all distances | ✅ (run k times) | ✅ Better |
| Multiple starting points, need min distance | ❌ Inefficient | ✅ Perfect |
| Simultaneous propagation | ❌ Cannot model | ✅ Natural fit |

### 1.7 Complexity Analysis

For an m × n grid with k source cells:

| Approach | Time | Space |
|----------|------|-------|
| Single-source BFS × k | O(k * m * n) | O(m * n) |
| Multi-source BFS | O(m * n) | O(m * n) |

The multi-source approach visits each cell exactly once regardless of source count.

---

# 994. Rotting Oranges

## 2. Problem Link
https://leetcode.com/problems/rotting-oranges/

## 3. Difficulty
Medium

## 4. Tags
- Array
- Breadth-First Search
- Matrix

## 5. Pattern
GridBFSMultiSource - Propagation Timer

## 6. API Kernel
`GridBFSMultiSource`

## 7. Problem Summary

Given an m × n grid where:
- `0` = empty cell
- `1` = fresh orange
- `2` = rotten orange

Every minute, fresh oranges adjacent (4-directionally) to rotten oranges become rotten. Return the minimum minutes until no fresh oranges remain, or -1 if impossible.

## 8. Key Insight

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

## 9. Template Mapping

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

## 10. Complexity
- Time: O(m × n) - each cell visited at most once
- Space: O(m × n) - queue can hold all cells in worst case

## 11. Why This Problem First?

Rotting Oranges is the **canonical multi-source BFS problem** because:

1. **Clear physical metaphor**: Infection spreading is intuitive
2. **Explicit simultaneity**: "Every minute" makes multi-source nature obvious
3. **Simple state space**: Only 3 cell values (0, 1, 2)
4. **Direct BFS level = time mapping**: Each level is exactly one minute

Once you understand this problem, the pattern transfers directly to other grid propagation scenarios.

## 12. Common Mistakes

1. **Starting BFS from one rotten orange** - Must start from ALL rotten oranges simultaneously
2. **Forgetting the -1 adjustment** - The while loop counts one extra iteration after the last spread
3. **Not handling edge cases** - Empty grid, no fresh oranges, no rotten oranges
4. **Modifying grid before full level processing** - Must process entire level before incrementing time

## 13. Related Problems
- LC 286: Walls and Gates (fill with distances)
- LC 542: 01 Matrix (distance to nearest 0)
- LC 1162: As Far from Land as Possible (max distance to land)

---

# 286. Walls and Gates

## 14. Problem Link
https://leetcode.com/problems/walls-and-gates/

## 15. Difficulty
Medium

## 16. Tags
- Array
- Breadth-First Search
- Matrix

## 17. Pattern
GridBFSMultiSource - Fill with Distance

## 18. API Kernel
`GridBFSMultiSource`

## 19. Problem Summary

Given an m × n grid where:
- `-1` = wall (obstacle)
- `0` = gate (destination)
- `INF` (2³¹ - 1) = empty room

Fill each empty room with the distance to its nearest gate. If impossible to reach a gate, leave as INF.

## 20. Key Insight

**Reverse the perspective**: Instead of computing distance FROM each room TO gates, compute distance FROM gates TO rooms. Start BFS from all gates simultaneously - each room gets filled with the distance when first reached (which is guaranteed to be the minimum due to BFS properties).

```
Initial:              After BFS:
INF  -1   0  INF      3  -1   0   1
INF INF INF  -1   →   2   2   1  -1
INF  -1 INF  -1       1  -1   2  -1
  0  -1 INF INF       0  -1   3   4
```

## 21. Delta from Base Template

| Aspect | Rotting Oranges | Walls and Gates |
|--------|-----------------|-----------------|
| Source | Rotten (2) | Gate (0) |
| Target | Fresh (1) | Empty (INF) |
| Marking | Change to 2 | Store distance |
| Result | Max time / -1 | Modified grid |

Key change: Instead of just marking visited, we **store the distance value** in each cell.

## 22. Template Mapping

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

## 23. Complexity
- Time: O(m × n) - each cell visited at most once
- Space: O(m × n) - queue can hold all cells in worst case

## 24. Why This Problem Second?

Walls and Gates introduces **distance storage** while maintaining the core multi-source BFS structure:

1. **Different source identification**: Gates (0) vs rotten oranges (2)
2. **Distance propagation**: `new_dist = current_dist + 1` pattern
3. **Natural visited check**: `INF` cells are unvisited, non-INF are visited
4. **In-place modification**: Common grid modification pattern

## 25. Common Mistakes

1. **BFS from each empty room** - O(m²n²) vs O(mn) with multi-source from gates
2. **Using separate visited set** - The grid itself tracks visited status (INF → distance)
3. **Processing walls** - Must skip `-1` cells
4. **Re-processing already filled rooms** - Check `rooms[nr][nc] == INF` before updating

## 26. Related Problems
- LC 994: Rotting Oranges (propagation timer)
- LC 542: 01 Matrix (similar distance field)
- LC 1162: As Far from Land as Possible (inverse: distance from land)

---

# 542. 01 Matrix

## 27. Problem Link
https://leetcode.com/problems/01-matrix/

## 28. Difficulty
Medium

## 29. Tags
- Array
- Breadth-First Search
- Matrix
- Dynamic Programming

## 30. Pattern
GridBFSMultiSource - Distance Field

## 31. API Kernel
`GridBFSMultiSource`

## 32. Problem Summary

Given an m × n binary matrix `mat`, return the distance of the nearest 0 for each cell. The distance between two adjacent cells is 1.

## 33. Key Insight

This is a **distance field computation** problem. For each cell, we want the shortest distance to ANY zero. Multi-source BFS from all zeros computes this optimally:

1. All zeros have distance 0 (they ARE zeros)
2. Start BFS from all zeros simultaneously
3. First time a cell is reached = its minimum distance to any zero

```
Input:         Output:
0 0 0          0 0 0
0 1 0    →     0 1 0
1 1 1          1 2 1
```

## 34. Delta from Base Template

| Aspect | Rotting Oranges | 01 Matrix |
|--------|-----------------|-----------|
| Source | Rotten (2) | Zero (0) |
| Target | Fresh (1) | One (1) |
| Output | Single value (time) | New matrix (distances) |
| Tracking | Count remaining | Distance matrix |

Key changes:
1. Create separate distance matrix (or modify in place)
2. Initialize zeros with distance 0
3. Initialize ones with infinity (or a sentinel like -1)

## 35. Template Mapping

```python
from collections import deque
from typing import List

class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        rows, cols = len(mat), len(mat[0])
        queue = deque()

        # Phase 1: Initialize distance matrix
        # Zeros have distance 0, ones start with infinity
        dist = [[0 if mat[r][c] == 0 else float('inf')
                 for c in range(cols)] for r in range(rows)]

        # Add all zeros to queue (sources at distance 0)
        for r in range(rows):
            for c in range(cols):
                if mat[r][c] == 0:
                    queue.append((r, c))

        # Phase 2: BFS from all zeros
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            r, c = queue.popleft()

            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    # Update if we found a shorter path
                    new_dist = dist[r][c] + 1
                    if new_dist < dist[nr][nc]:
                        dist[nr][nc] = new_dist
                        queue.append((nr, nc))

        return dist
```

## 36. Alternative: In-Place Modification

```python
class SolutionInPlace:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        """
        Modify matrix in-place using -1 as 'unvisited one' marker.
        """
        rows, cols = len(mat), len(mat[0])
        queue = deque()

        # Mark all ones as unvisited (-1), add zeros to queue
        for r in range(rows):
            for c in range(cols):
                if mat[r][c] == 0:
                    queue.append((r, c))
                else:
                    mat[r][c] = -1  # Unvisited marker

        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        distance = 0

        while queue:
            distance += 1
            for _ in range(len(queue)):
                r, c = queue.popleft()

                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc

                    if 0 <= nr < rows and 0 <= nc < cols:
                        if mat[nr][nc] == -1:  # Unvisited one
                            mat[nr][nc] = distance
                            queue.append((nr, nc))

        return mat
```

## 37. Complexity
- Time: O(m × n) - each cell visited at most once
- Space: O(m × n) - queue and distance matrix

## 38. Why This Problem Third?

01 Matrix consolidates the pattern with a clean output specification:

1. **Pure distance field**: Output is a matrix of distances
2. **No special states**: Just 0s and 1s (cleaner than walls/gates)
3. **Guaranteed solvability**: Every cell is reachable from some zero
4. **Flexible implementation**: Can modify in-place or create new matrix

## 39. Common Mistakes

1. **BFS from each one** - O(m²n²) vs O(mn) with multi-source from zeros
2. **Wrong initialization** - Ones must start as infinity/unvisited, not 1
3. **Confusing source vs target** - Sources are zeros (known distance), targets are ones
4. **Level counting off-by-one** - Zeros are at distance 0, not 1

## 40. DP Alternative

This problem can also be solved with DP (two passes), but BFS is more intuitive for grid distance problems:

```python
# DP approach (for reference):
# Pass 1: top-left to bottom-right (check top and left)
# Pass 2: bottom-right to top-left (check bottom and right)
```

## 41. Related Problems
- LC 994: Rotting Oranges (propagation timer)
- LC 286: Walls and Gates (similar fill pattern)
- LC 1162: As Far from Land as Possible (max min-distance)
- LC 934: Shortest Bridge (BFS between two islands)

---

## 42. Problem Comparison

| Problem | Source Cells | Target Cells | Output | BFS Termination |
|---------|-------------|--------------|--------|-----------------|
| **Rotting Oranges** | Rotten (2) | Fresh (1) | Max time or -1 | All fresh infected or queue empty |
| **Walls and Gates** | Gates (0) | Empty (INF) | Modified grid | Queue empty |
| **01 Matrix** | Zeros (0) | Ones (1) | Distance matrix | Queue empty |

## 43. State Tracking Comparison

| Problem | Visited Marker | Distance Storage | Remaining Count |
|---------|---------------|------------------|-----------------|
| **Rotting Oranges** | Change 1→2 | Implicit (levels) | Yes (fresh count) |
| **Walls and Gates** | Change INF→dist | In grid cell | No |
| **01 Matrix** | Change 1→dist or -1→dist | Separate matrix or in-place | No |

## 44. Pattern Evolution

```
┌──────────────────────────────────────────────────────────────────┐
│                    Multi-Source BFS Evolution                    │
└──────────────────────────────────────────────────────────────────┘

       Rotting Oranges (Base)
              │
              │ Core pattern:
              │ - Initialize queue with all sources
              │ - Process level by level
              │ - Track remaining targets
              │
              ▼
    ┌─────────────────────┐
    │ What changes for    │
    │ Walls and Gates?    │
    ├─────────────────────┤
    │ + Store distance    │
    │ + Different markers │
    │ - No count tracking │
    │ - No result check   │
    └─────────────────────┘
              │
              ▼
       Walls and Gates
              │
              │ Distance storage pattern:
              │ - dist[nr][nc] = dist[r][c] + 1
              │ - INF as unvisited marker
              │
              ▼
    ┌─────────────────────┐
    │ What changes for    │
    │ 01 Matrix?          │
    ├─────────────────────┤
    │ + Clean binary grid │
    │ + Return new matrix │
    │ - No obstacles      │
    └─────────────────────┘
              │
              ▼
         01 Matrix
```

## 45. Code Structure Comparison

```python
# ===== Rotting Oranges =====
# Sources: grid[r][c] == 2
# Targets: grid[r][c] == 1
# Update:  grid[nr][nc] = 2
# Result:  minutes - 1 if fresh == 0 else -1

# ===== Walls and Gates =====
# Sources: rooms[r][c] == 0
# Targets: rooms[r][c] == INF
# Update:  rooms[nr][nc] = rooms[r][c] + 1
# Result:  in-place modification (void)

# ===== 01 Matrix =====
# Sources: mat[r][c] == 0
# Targets: mat[r][c] == 1 (or dist[r][c] == inf)
# Update:  dist[nr][nc] = dist[r][c] + 1
# Result:  distance matrix
```

---

## 46. Decision Tree

```
Start: Grid problem involving distances or propagation?
                    │
                    ▼
        ┌───────────────────────┐
        │ Multiple starting     │
        │ points (sources)?     │
        └───────────────────────┘
                    │
            ┌───────┴───────┐
            ▼               ▼
           YES              NO
            │               │
            ▼               ▼
    ┌───────────────┐  Single-source BFS
    │ Need minimum  │  or other approach
    │ distance to   │
    │ ANY source?   │
    └───────────────┘
            │
            ▼
     Multi-Source BFS
            │
    ┌───────┴───────────┬────────────────┐
    ▼                   ▼                ▼
"Time until all?"  "Distance field?"  "Fill to nearest?"
    │                   │                │
    ▼                   ▼                ▼
Rotting Oranges    01 Matrix       Walls and Gates
 (count levels)    (store dist)    (store dist)
```

## 47. Pattern Selection Guide

### 47.1 Use Multi-Source BFS when:

- ✅ Multiple cells serve as starting points
- ✅ Need shortest distance to the **nearest** source
- ✅ Simultaneous propagation/spread semantics
- ✅ BFS level = distance relationship is needed
- ✅ Grid is unweighted (all edges have cost 1)

### 47.2 Use Single-Source BFS when:

- ✅ Only one starting point
- ✅ Need distance from a specific source to all targets
- ✅ Path finding from A to B

### 47.3 Use Dijkstra instead when:

- ✅ Weighted edges (different movement costs)
- ✅ Non-uniform grid (some cells cost more to traverse)

### 47.4 Use DP instead when:

- ✅ Only need to check reachability (no actual distances)
- ✅ Bounded directions (e.g., only down/right movement)
- ✅ Two-pass approach is simpler

## 48. Problem Identification Checklist

When you see a grid problem, ask:

1. **How many sources?** Single vs Multiple
2. **What's the question?** Time/count vs Distance vs Reachability
3. **Simultaneous or sequential?** Multi-source implies simultaneous
4. **Uniform cost?** BFS for uniform, Dijkstra for weighted

## 49. Quick Pattern Recognition

| Keyword in Problem | Likely Pattern |
|--------------------|----------------|
| "minimum time until all" | Multi-source BFS (timer) |
| "distance to nearest" | Multi-source BFS (distance field) |
| "fill from boundary" | Multi-source BFS from edges |
| "spread/propagate/infect" | Multi-source BFS (propagation) |
| "shortest path from A to B" | Single-source BFS |

---

## 50. Universal Templates

### 50.1 Template 1: Propagation Timer (Rotting Oranges Style)

```python
from collections import deque
from typing import List

def propagation_timer(grid: List[List[int]], SOURCE: int, TARGET: int) -> int:
    """
    Count levels until all targets are converted to sources.

    Returns: number of levels (time units), or -1 if impossible
    Use for: LC 994 (Rotting Oranges)
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    queue = deque()
    target_count = 0

    # Initialize: collect sources, count targets
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == SOURCE:
                queue.append((r, c))
            elif grid[r][c] == TARGET:
                target_count += 1

    if target_count == 0:
        return 0

    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    levels = 0

    while queue:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == TARGET:
                        grid[nr][nc] = SOURCE
                        queue.append((nr, nc))
                        target_count -= 1
        levels += 1

    return levels - 1 if target_count == 0 else -1
```

**Use for**: LC 994 (Rotting Oranges), similar "time to spread" problems

---

### 50.2 Template 2: Distance Fill (Walls and Gates Style)

```python
from collections import deque
from typing import List

def distance_fill(grid: List[List[int]], SOURCE: int, INF: int) -> None:
    """
    Fill each INF cell with distance to nearest SOURCE.
    Modifies grid in-place.

    Use for: LC 286 (Walls and Gates)
    """
    if not grid or not grid[0]:
        return

    rows, cols = len(grid), len(grid[0])
    queue = deque()

    # Initialize: all sources at distance 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == SOURCE:
                queue.append((r, c))

    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == INF:
                    grid[nr][nc] = grid[r][c] + 1
                    queue.append((nr, nc))
```

**Use for**: LC 286 (Walls and Gates), boundary fill problems

---

### 50.3 Template 3: Distance Matrix (01 Matrix Style)

```python
from collections import deque
from typing import List

def distance_matrix(mat: List[List[int]], SOURCE_VAL: int = 0) -> List[List[int]]:
    """
    Return new matrix where each cell contains distance to nearest source.

    Use for: LC 542 (01 Matrix)
    """
    rows, cols = len(mat), len(mat[0])
    queue = deque()

    # Initialize distance matrix
    dist = [[0 if mat[r][c] == SOURCE_VAL else float('inf')
             for c in range(cols)] for r in range(rows)]

    # Add all sources
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == SOURCE_VAL:
                queue.append((r, c))

    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_dist = dist[r][c] + 1
                if new_dist < dist[nr][nc]:
                    dist[nr][nc] = new_dist
                    queue.append((nr, nc))

    return dist
```

**Use for**: LC 542 (01 Matrix), distance field computations

---

### 50.4 Template 4: Generic Multi-Source BFS

```python
from collections import deque
from typing import List, Callable

def multi_source_bfs_generic(
    grid: List[List[int]],
    is_source: Callable[[int], bool],
    is_target: Callable[[int], bool],
    mark_visited: Callable[[List[List[int]], int, int, int], None],
    directions: List[tuple] = None
) -> int:
    """
    Generic multi-source BFS with customizable predicates.

    Args:
        is_source: lambda cell_value -> bool
        is_target: lambda cell_value -> bool
        mark_visited: function(grid, r, c, dist) to mark cell as visited

    Returns: max distance reached
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    queue = deque()
    directions = directions or [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialize
    for r in range(rows):
        for c in range(cols):
            if is_source(grid[r][c]):
                queue.append((r, c, 0))

    max_dist = 0

    while queue:
        r, c, dist = queue.popleft()
        max_dist = max(max_dist, dist)

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if is_target(grid[nr][nc]):
                    mark_visited(grid, nr, nc, dist + 1)
                    queue.append((nr, nc, dist + 1))

    return max_dist
```

**Use for**: Custom multi-source BFS scenarios



---



*Document generated for NeetCode Practice Framework — API Kernel: GridBFSMultiSource*

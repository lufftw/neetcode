## Problem Comparison

| Problem | Source Cells | Target Cells | Output | BFS Termination |
|---------|-------------|--------------|--------|-----------------|
| **Rotting Oranges** | Rotten (2) | Fresh (1) | Max time or -1 | All fresh infected or queue empty |
| **Walls and Gates** | Gates (0) | Empty (INF) | Modified grid | Queue empty |
| **01 Matrix** | Zeros (0) | Ones (1) | Distance matrix | Queue empty |

## State Tracking Comparison

| Problem | Visited Marker | Distance Storage | Remaining Count |
|---------|---------------|------------------|-----------------|
| **Rotting Oranges** | Change 1→2 | Implicit (levels) | Yes (fresh count) |
| **Walls and Gates** | Change INF→dist | In grid cell | No |
| **01 Matrix** | Change 1→dist or -1→dist | Separate matrix or in-place | No |

## Pattern Evolution

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

## Code Structure Comparison

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



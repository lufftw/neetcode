# Multi-Source BFS - Intuition Guide

## The Mental Model: Dropping Multiple Pebbles

Imagine dropping pebbles into a still pond. Each pebble creates ripples that expand outward. If you drop **one pebble**, you see one set of ripples expanding from that point. But what if you drop **multiple pebbles simultaneously**?

```
Single pebble:          Multiple pebbles:
      ●                    ●   ●
     /|\                  /|\ /|\
    / | \                / |X| \
   /  |  \              /  | |  \
```

When multiple ripples meet, they don't create new sources - they simply merge. The key insight: **every point in the pond reaches the nearest pebble first**.

Multi-source BFS works exactly like this:
- Each source cell is a "pebble dropped at time 0"
- The BFS wavefront expands like ripples
- Each cell is reached by the nearest source first

## Why Multi-Source BFS?

### The Naive Approach (Don't Do This)

For a problem like "find distance to nearest zero for each cell":

```python
# BAD: O(k * m * n) where k = number of zeros
for each zero in grid:
    run BFS from this zero
    update all cells with min distance
```

This runs BFS once per source - expensive and redundant.

### The Multi-Source Insight

```python
# GOOD: O(m * n) regardless of source count
add ALL zeros to queue at distance 0
run ONE BFS expanding from all sources simultaneously
```

The magic: BFS guarantees that **the first time we reach a cell, it's via the shortest path**. Since all sources start at distance 0, the first source to reach any cell must be the nearest one.

## Core Pattern Visualization

```
Step 0: Initialize all sources
┌─────────────────────────────────┐
│  S = source (in queue)          │
│  . = target (unvisited)         │
│  # = obstacle                   │
│                                 │
│    S  .  .  #  S                │
│    .  .  .  .  .                │
│    .  #  .  .  .                │
│    S  .  .  .  .                │
└─────────────────────────────────┘

Step 1: First BFS level (distance 1)
┌─────────────────────────────────┐
│    S  1  .  #  S                │
│    1  .  .  .  1                │
│    .  #  .  .  .                │
│    S  1  .  .  .                │
└─────────────────────────────────┘

Step 2: Second BFS level (distance 2)
┌─────────────────────────────────┐
│    S  1  2  #  S                │
│    1  2  .  2  1                │
│    2  #  .  .  2                │
│    S  1  2  .  .                │
└─────────────────────────────────┘

... and so on until all cells are reached
```

## The Three Variants

### Variant 1: Propagation Timer (Rotting Oranges)

**Question**: "How long until everything is infected?"

**Mental model**: Zombie infection spreading. All zombies move one step per minute. We want to know when the last survivor gets bitten.

```
┌────────────────────────────────────────┐
│  Minute 0: Initial state               │
│  🧟 😊 😊          (2 fresh, 1 zombie)  │
│                                        │
│  Minute 1:                             │
│  🧟 🧟 😊          (1 fresh, 2 zombies) │
│                                        │
│  Minute 2:                             │
│  🧟 🧟 🧟          (0 fresh, all zombies)│
│                                        │
│  Answer: 2 minutes                     │
└────────────────────────────────────────┘
```

**Key implementation detail**: Count BFS levels. Return `levels - 1` because we count one extra level after the last conversion.

### Variant 2: Distance Fill (Walls and Gates)

**Question**: "What's the distance from each room to the nearest exit?"

**Mental model**: Evacuation signs. Each room needs a sign showing distance to the nearest exit. Instead of measuring from each room (expensive), measure from each exit (cheap with multi-source BFS).

```
┌────────────────────────────────────────┐
│  Before:              After:           │
│  ∞  #  0  ∞          3  #  0  1        │
│  ∞  ∞  ∞  #    →     2  2  1  #        │
│  ∞  #  ∞  #          1  #  2  #        │
│  0  #  ∞  ∞          0  #  3  4        │
└────────────────────────────────────────┘
```

**Key implementation detail**: Store `distance[neighbor] = distance[current] + 1`. The grid cell itself becomes the distance tracker.

### Variant 3: Distance Field (01 Matrix)

**Question**: "For each cell, what's the distance to the nearest special cell?"

**Mental model**: Computing a "heat map" of distances. Every zero is a heat source at temperature 0. Heat radiates outward, increasing by 1 at each step.

```
┌────────────────────────────────────────┐
│  Input:               Output:          │
│  0  0  0              0  0  0          │
│  0  1  0      →       0  1  0          │
│  1  1  1              1  2  1          │
└────────────────────────────────────────┘
```

**Key implementation detail**: Can modify in-place or create separate distance matrix.

## Common Mistakes and Fixes

### Mistake 1: BFS from Each Source Separately

```python
# WRONG: O(k * m * n)
for source in sources:
    bfs_from(source)
    update_min_distances()

# RIGHT: O(m * n)
queue = deque(all_sources)
bfs_from_queue()
```

### Mistake 2: Wrong Initialization

```python
# WRONG: Adding sources with distance 1
for source in sources:
    queue.append((source, 1))  # Should be 0!

# RIGHT: Sources are at distance 0
for source in sources:
    queue.append((source, 0))  # Correct
    dist[source] = 0
```

### Mistake 3: Forgetting Level Counting Adjustment

```python
# For propagation timer problems:
while queue:
    for _ in range(len(queue)):  # Process whole level
        ...
    levels += 1

# The while loop runs one extra time after last conversion
return levels - 1  # Not levels!
```

### Mistake 4: Double-Counting Visits

```python
# WRONG: Mark visited after popping
while queue:
    cell = queue.popleft()
    if cell in visited:
        continue
    visited.add(cell)  # Too late! May have added duplicates

# RIGHT: Mark visited before adding
if neighbor not in visited:
    visited.add(neighbor)  # Mark immediately
    queue.append(neighbor)
```

## Quick Pattern Recognition

| Problem Statement Contains | Pattern |
|---------------------------|---------|
| "minimum time for all to become X" | Multi-source BFS (timer) |
| "distance to nearest X for each cell" | Multi-source BFS (distance field) |
| "fill each cell with distance to X" | Multi-source BFS (distance fill) |
| "spreading/infection/propagation" | Multi-source BFS (timer) |

## Visual Summary

```
┌──────────────────────────────────────────────────────────────────┐
│                    Multi-Source BFS Pipeline                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐                                             │
│  │  Initialize     │  For each source cell:                      │
│  │  Queue          │  - Add to queue                             │
│  │                 │  - Mark as distance 0 / visited             │
│  └────────┬────────┘                                             │
│           │                                                       │
│           ▼                                                       │
│  ┌─────────────────┐                                             │
│  │  BFS Loop       │  While queue not empty:                     │
│  │                 │  - Pop cell                                 │
│  │                 │  - For each neighbor:                       │
│  │                 │    - If valid target:                       │
│  │                 │      - Update distance/state                │
│  │                 │      - Add to queue                         │
│  └────────┬────────┘                                             │
│           │                                                       │
│           ▼                                                       │
│  ┌─────────────────┐                                             │
│  │  Return Result  │  Timer: max level (or -1 if unreachable)    │
│  │                 │  Distance: modified grid or new matrix      │
│  └─────────────────┘                                             │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```



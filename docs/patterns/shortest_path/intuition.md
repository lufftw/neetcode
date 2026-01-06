# Shortest Path Patterns: Mental Models & Intuition

> Build deep understanding of when and why different shortest path algorithms work.

## The Core Insight

**Shortest path finds the minimum-cost route between points in a weighted graph.**

The key is choosing the right algorithm based on:
- Edge weights (non-negative? binary? negative?)
- Constraints (limited steps? specific target?)
- Objective (minimize sum? minimize max?)

---

## Mental Model 1: Dijkstra as Greedy Expansion

Imagine flooding water from the source node:

```
Start:           After wave 1:       After wave 2:
    S                S                   S
   /|\              /|\                 /|\
  ? ? ?            2 3 ?               2 3 5
                   visited!               ↑
                   (closest)          next closest

Water flows to nearest unvisited node first.
Once water reaches a node, that's the shortest path!
```

**Key insight:** For non-negative weights, the first time we reach a node is optimal.

---

## Mental Model 2: 0-1 BFS with Deque

When edges cost only 0 or 1, we can use a faster approach:

```
Regular Dijkstra:          0-1 BFS with Deque:
┌───────────────┐          ┌───────────────┐
│   Min-Heap    │          │    Deque      │
│ [1,2,3,4,5]   │          │ [1,1,2,2,3]   │
│ O(log n) ops  │          │ O(1) ops      │
└───────────────┘          └───────────────┘

Cost-0 edges: add to FRONT (like staying in place)
Cost-1 edges: add to BACK (like normal BFS)
```

**Why it works:** The deque stays sorted because:
- Front elements have same or lower cost
- Back elements have cost + 1

---

## Mental Model 3: Bellman-Ford as Wave Propagation

Each iteration extends paths by one edge:

```
Iteration 0:    Iteration 1:    Iteration 2:    Iteration 3:
    0               0               0               0
    |               |               |               |
S - inf         S - 5           S - 5           S - 5
    |               |               |               |
   inf             inf              8               8
                                    |               |
                                   inf             12

After k iterations: know shortest paths using ≤ k edges
```

**Key insight:** K iterations = paths with at most K edges.

---

## Mental Model 4: Minimax Path

Instead of summing edge weights, track the maximum:

```
Path 1: 1 → 3 → 5 → 2    (max = 5)
Path 2: 1 → 8 → 2        (max = 8)

Minimax chooses Path 1 (smaller maximum)
```

**Dijkstra still works** because we want to minimize the max:
- Priority = max edge on path so far
- First arrival at target = minimum possible max

---

## Mental Model 5: State-Space Dijkstra

When you have constraints, expand the state:

```
Simple Dijkstra:           With K-stop constraint:
State = (node)             State = (node, stops_used)

Graph:                     State Graph:
    A                      (A,0) → (B,1) → (C,2)
   / \                         ↘ (C,1)
  B   C
                           Different stop counts = different states!
```

**Key insight:** Add dimensions to state for constraints.

---

## Algorithm Selection Guide

| Edge Weights | Algorithm | Time | Use Case |
|--------------|-----------|------|----------|
| All equal | BFS | O(V+E) | Unweighted graph |
| 0 or 1 | 0-1 BFS | O(V+E) | Binary cost grid |
| Non-negative | Dijkstra | O((V+E)log V) | General weighted |
| Any | Bellman-Ford | O(VE) | Negative edges |
| K edge limit | Bellman-Ford K | O(KE) | Limited steps |

---

## Common Pitfalls

### Pitfall 1: Using BFS for Weighted Graphs

```python
# WRONG: BFS finds shortest path by edge count, not weight
from collections import deque
def shortest_path(graph, start):
    queue = deque([start])  # BFS only works for unweighted!

# CORRECT: Use Dijkstra for weighted graphs
import heapq
def shortest_path(graph, start):
    pq = [(0, start)]  # Priority by distance
```

### Pitfall 2: Not Skipping Visited Nodes

```python
# WRONG: Process same node multiple times
while pq:
    dist, node = heappop(pq)
    for neighbor in graph[node]:  # Might add duplicates!
        heappush(pq, (dist + weight, neighbor))

# CORRECT: Skip if already processed
while pq:
    dist, node = heappop(pq)
    if dist > distances[node]:  # Already found better!
        continue
    # ... process neighbors
```

### Pitfall 3: Wrong Order in 0-1 BFS

```python
# WRONG: Adding to wrong end
if edge_cost == 0:
    dq.append((cost, node))    # Should be front!
else:
    dq.appendleft((cost, node))  # Should be back!

# CORRECT: 0-cost to front, 1-cost to back
if edge_cost == 0:
    dq.appendleft((new_cost, neighbor))  # Front
else:
    dq.append((new_cost, neighbor))      # Back
```

### Pitfall 4: Forgetting Path Length Limit

```python
# WRONG: Dijkstra doesn't track path length
# For "at most K stops", need state = (node, stops)

# CORRECT: Expand state space
visited = {}  # (node, stops) -> min_cost
pq = [(0, start, 0)]  # (cost, node, stops_used)
```

---

## Practice Progression

### Level 1: Basic Dijkstra
1. **LC 743 - Network Delay Time** (Find max of shortest paths)

### Level 2: Grid Variations
2. **LC 1631 - Path With Minimum Effort** (Minimax objective)

### Level 3: Constrained Paths
3. **LC 787 - Cheapest Flights Within K Stops** (Edge limit)

### Level 4: 0-1 BFS
4. **LC 1368 - Minimum Cost Valid Path** (Direction changes)
5. **LC 2290 - Minimum Obstacle Removal** (Remove obstacles)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                   SHORTEST PATH                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  DIJKSTRA:                 0-1 BFS:                     │
│  ─────────                 ────────                     │
│  pq = [(0, start)]         dq = deque([(0, start)])     │
│  heappop → closest         popleft → process            │
│  heappush neighbors        cost-0 → appendleft          │
│  Skip if already better    cost-1 → append              │
│                                                          │
│  BELLMAN-FORD:             MINIMAX:                     │
│  ────────────              ───────                      │
│  Relax all edges K times   new_dist = max(dist, edge)   │
│  new_dist[v] = dist[u]+w   Instead of sum               │
│  Use copy for each round   Still use Dijkstra           │
│                                                          │
│  COMPLEXITY:                                             │
│  ──────────                                              │
│  Dijkstra:     O((V+E) log V)                           │
│  0-1 BFS:      O(V + E)                                 │
│  Bellman-Ford: O(V × E) or O(K × E)                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

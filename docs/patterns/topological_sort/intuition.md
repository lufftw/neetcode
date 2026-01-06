# Topological Sort Patterns: Mental Models & Intuition

> Build deep understanding of when and why Topological Sort works.

## The Core Insight

**Topological Sort orders nodes so all dependencies come first.**

For a directed graph where edge A → B means "A must come before B":
- Find an ordering where every edge points forward
- If no such ordering exists, there's a cycle
- A DAG (Directed Acyclic Graph) always has at least one valid ordering

---

## Mental Model 1: The Dependency Chain

```
Prerequisites:         Valid Order:
  0 → 1                [0, 2, 1, 3]
  0 → 2                or [0, 1, 2, 3]
  1 → 3                or [0, 2, 1, 3]
  2 → 3

Think of it as: "What can I do with no blockers?"
```

**Key insight:** At any point, nodes with no remaining dependencies can be processed.

---

## Mental Model 2: Kahn's Algorithm (Peeling Layers)

Imagine removing nodes layer by layer:

```
Initial:           Layer 1:          Layer 2:          Layer 3:
  0 → 1 → 3        Remove 0          Remove 1, 2       Remove 3
  ↓                (in-degree 0)     (in-degree 0)     (in-degree 0)
  2 ───↗

In-degrees:        After removing 0:  After removing 1,2:
  0: 0 ←start      1: 0 ←start        3: 0 ←start
  1: 1             2: 0 ←start
  2: 1             3: 2
  3: 2

Order: [0, 1, 2, 3] or [0, 2, 1, 3]
```

**Key operations:**
- Track in-degree for each node
- Process nodes with in-degree 0
- Decrement neighbors' in-degrees

---

## Mental Model 3: DFS Postorder (Finish Last)

DFS explores deeply, adds nodes when "done" with them:

```
Start from 0:
  Visit 0
    Visit 1
      Visit 3 (no more neighbors)
        Done with 3, add to result: [3]
      Done with 1, add to result: [3, 1]
    Visit 2
      3 already done
      Done with 2, add to result: [3, 1, 2]
    Done with 0, add to result: [3, 1, 2, 0]

Reverse: [0, 2, 1, 3] ← Valid topological order!
```

**Why reverse?** We add nodes after processing all descendants, so they end up last. Reversing puts them first.

---

## Mental Model 4: Three-Color Cycle Detection

```
Colors:
  WHITE = unvisited
  GRAY  = currently in recursion stack (being explored)
  BLACK = fully processed (safe)

Cycle Detection:
  If we visit a GRAY node → We found a back edge → CYCLE!

  0 (GRAY) → 1 (GRAY) → 2 (GRAY) → 0 (GRAY!) ← CYCLE!
```

**Key insight:** A back edge (edge to ancestor in DFS tree) means a cycle.

---

## Mental Model 5: Safe States (Reverse Thinking)

For "eventual safe states" problems:

```
Original Graph:        Reverse Perspective:
  A → B → C (terminal)    Start from terminals
  A → D → E → A (cycle)   Propagate "safety" backwards

Safe: C, B, then A      Unsafe: E, D, anything reaching them
(if A only went to B)
```

**Key insight:** A node is safe iff ALL paths lead to terminals.

---

## Pattern Recognition Checklist

| Signal Words | Pattern | Key Insight |
|-------------|---------|-------------|
| "prerequisites", "dependencies" | Topological Sort | Order respecting edges |
| "can all be completed?" | Cycle Detection | len(result) == n |
| "valid ordering" | Return Order | Collect during traversal |
| "safe states" | Reverse Analysis | DFS three-color or reverse graph |
| "multi-level ordering" | Nested Topo Sort | Sort groups, then items |

---

## When to Use Kahn's vs DFS

| Use Kahn's (BFS) | Use DFS Postorder |
|------------------|-------------------|
| Need to process in levels/batches | Simpler implementation |
| Parallelization needed | Already doing DFS |
| Dynamic graph updates | Finding all orderings |
| Streaming/online processing | Stack depth not an issue |

---

## Common Pitfalls

### Pitfall 1: Wrong Edge Direction

```python
# WRONG: "A depends on B" doesn't mean A → B
# If A depends on B, B must come BEFORE A
# So the edge is B → A (or track in-degree[A]++)

# Course [1, 0] means "1 depends on 0" → edge: 0 → 1
graph[0].append(1)
in_degree[1] += 1
```

### Pitfall 2: Forgetting Disconnected Components

```python
# WRONG: Only start from one node
dfs(0)

# CORRECT: Start from ALL unvisited nodes
for node in range(n):
    if color[node] == WHITE:
        dfs(node)
```

### Pitfall 3: Self-Loops

```python
# A node depending on itself is a cycle!
if course == prereq:
    return False  # Impossible
```

### Pitfall 4: Forgetting to Reverse in DFS

```python
# DFS postorder gives reverse topological order
result.append(node)  # Add when done
...
return result[::-1]  # Don't forget to reverse!
```

---

## Practice Progression

### Level 1: Core Concept
1. **LC 207 - Course Schedule** (Detect if order exists)

### Level 2: Return Order
2. **LC 210 - Course Schedule II** (Return actual order)

### Level 3: Safe States
3. **LC 802 - Find Eventual Safe States** (Not in any cycle)

### Level 4: Advanced
4. **LC 1203 - Sort Items by Groups** (Two-level topo sort)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                 TOPOLOGICAL SORT                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  KAHN'S (BFS):                DFS POSTORDER:            │
│  ─────────────                ──────────────            │
│  in_degree[v]++               WHITE → GRAY → BLACK      │
│  queue: in_degree 0           Add node when BLACK       │
│  process, decrement           Reverse at end            │
│                                                          │
│  CYCLE DETECTION:                                        │
│  ─────────────────                                       │
│  Kahn's: len(result) < n                                │
│  DFS: GRAY → GRAY (back edge)                           │
│                                                          │
│  PATTERNS:                                               │
│  ─────────                                               │
│  Ordering:    Return result list                        │
│  Can finish:  len(result) == n                          │
│  Safe nodes:  Not reachable from any cycle              │
│  Two-level:   Sort groups, then items within groups     │
│                                                          │
│  COMPLEXITY:                                             │
│  ─────────                                               │
│  Time:  O(V + E)                                         │
│  Space: O(V + E) for graph + O(V) for state             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

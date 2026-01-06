# Union-Find Patterns: Mental Models & Intuition

> Build deep understanding of when and why Union-Find works.

## The Core Insight

**Union-Find answers one question efficiently: "Are X and Y connected?"**

It maintains a forest of trees where:
- Each tree represents a connected component
- The root identifies the component
- Two nodes are connected iff they have the same root

---

## Mental Model 1: The Forest View

```
Initially (n=6):        After unions:
  0   1   2   3   4   5     0       4
  │   │   │   │   │   │    /|\      |
  ↓   ↓   ↓   ↓   ↓   ↓   1 2 3    5

  6 separate trees        2 trees (components)
```

**Key operations:**
- `find(x)`: Walk up to root
- `union(x, y)`: Connect roots
- `connected(x, y)`: Same root?

---

## Mental Model 2: Path Compression

Without compression, trees can become chains:

```
Long chain:             After find(4):
    0                       0
    │                    /│ \ \
    1                   1 2  3 4
    │
    2                   All nodes now point
    │                   directly to root!
    3
    │
    4
```

**Path compression makes subsequent finds O(1).**

```python
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # ← Compress!
    return parent[x]
```

---

## Mental Model 3: Union by Rank

Attach smaller tree under larger tree:

```
Bad union:              Good union (by rank):
    0        1              0
   / \       │            / | \
  2   3      4           2  3  1
                              |
                              4

Height grows!           Height stays balanced
```

**Union by rank keeps tree height O(log n).**

---

## Mental Model 4: Cycle Detection

**If union(x, y) fails (same root), adding edge x-y creates a cycle.**

```
Tree so far:        Try to add edge 2-3:
    1               find(2) = 1
   / \              find(3) = 1
  2   3             Same root! → Cycle!

Adding 2-3 would create: 1-2-3-1 (cycle)
```

---

## Pattern Recognition Checklist

| Signal Words | Pattern | Key Insight |
|-------------|---------|-------------|
| "connected components" | Count components | Start n, subtract on each union |
| "same group/set" | Connectivity query | find(x) == find(y) |
| "creates cycle" | Cycle detection | union returns False |
| "merge by common" | Equivalence grouping | Map items → indices |
| "connect all" | Network connectivity | Need (components-1) edges |
| "equality/inequality" | Constraint satisfaction | == first, then check != |

---

## When to Use Union-Find vs DFS

| Use Union-Find | Use DFS |
|----------------|---------|
| Multiple connectivity queries | Single query |
| Dynamic edge additions | Static graph |
| Only need "connected?" | Need actual path |
| Cycle detection during build | Path exploration |
| Space-constrained | Need to visit all nodes |

---

## Common Pitfalls

### Pitfall 1: Not Using Path Compression

```python
# WRONG: O(n) per find
def find(x):
    while parent[x] != x:
        x = parent[x]
    return x

# CORRECT: O(α(n)) ≈ O(1) amortized
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # Path compression
    return parent[x]
```

### Pitfall 2: Wrong Index Range

```python
# 1-indexed nodes (like LC 684)
parent = list(range(n + 1))  # Need n+1 slots!

# 0-indexed nodes
parent = list(range(n))
```

### Pitfall 3: Processing Order (Constraints)

```python
# WRONG: Check both in one pass
for eq in equations:
    if eq[1] == '=':
        union(...)
    else:
        if find(x) == find(y):  # Too early!
            return False

# CORRECT: Two passes
for eq in equations:
    if eq[1] == '=':
        union(...)  # Build equalities first

for eq in equations:
    if eq[1] == '!':
        if find(x) == find(y):  # Now check
            return False
```

---

## Practice Progression

### Level 1: Core Concept
1. **LC 547 - Number of Provinces** (Basic connectivity)

### Level 2: Cycle Detection
2. **LC 684 - Redundant Connection** (Find cycle-forming edge)

### Level 3: Equivalence
3. **LC 721 - Accounts Merge** (Group by common elements)
4. **LC 990 - Equation Satisfaction** (Constraint checking)

### Level 4: Network Operations
5. **LC 1319 - Network Connected** (Count components + feasibility)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                    UNION-FIND                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  STRUCTURE:              OPERATIONS:                     │
│  parent[x] = root        find(x): path compression       │
│  rank[x] = depth bound   union(x,y): by rank            │
│                                                          │
│  PATTERNS:                                               │
│  ─────────                                               │
│  Components:  count -= 1 on each successful union        │
│  Cycle:       union returns False = cycle found          │
│  Grouping:    map items → indices, then union            │
│  Constraints: equalities first, then check inequalities  │
│                                                          │
│  COMPLEXITY:                                             │
│  ─────────                                               │
│  Time:  O(α(n)) ≈ O(1) per operation (amortized)        │
│  Space: O(n) for parent + rank arrays                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

# Bitmask DP - Intuition Guide

## The Mental Model: Binary Light Switches

Imagine a control panel with n light switches. Each switch can be ON (1) or OFF (0). The entire panel state is just a sequence of bits:

```
Panel with 4 switches: [OFF, ON, ON, OFF]
As a number:            0    1   1   0  = 6 in binary

Switch 0 → bit 0 (2^0 = 1)
Switch 1 → bit 1 (2^1 = 2)
Switch 2 → bit 2 (2^2 = 4)
Switch 3 → bit 3 (2^3 = 8)
```

This is the core of **Bitmask DP**: we represent "which items are selected" as an integer, and use bit operations to efficiently track and transition between states.

## Why Bitmasks?

The naive approach to tracking subsets would use sets or arrays:
```python
# Slow: set operations, hashing
visited = {0, 2, 5}
if 3 not in visited:
    visited.add(3)
```

With bitmasks, the same operations are O(1):
```python
# Fast: bit operations
visited = 0b100101  # {0, 2, 5}
if not (visited & (1 << 3)):
    visited |= (1 << 3)
```

## The Bit Operation Toolkit

Think of these as your "subset operations":

```
Operation        Code              Meaning
─────────────────────────────────────────────
Add i            mask | (1 << i)   Put i in the set
Remove i         mask & ~(1 << i)  Take i out
Check if i in    mask & (1 << i)   Is i present?
Toggle i         mask ^ (1 << i)   Flip i's membership
Full set         (1 << n) - 1      All n elements
Empty set        0                 Nothing selected
Count elements   bin(mask).count('1')  Set size
```

## Pattern 1: Subset Enumeration

**The insight**: Every integer from 0 to 2^n - 1 represents a unique subset.

```
n = 3, elements = [A, B, C]

mask=0 (000): {}        mask=4 (100): {C}
mask=1 (001): {A}       mask=5 (101): {A, C}
mask=2 (010): {B}       mask=6 (110): {B, C}
mask=3 (011): {A, B}    mask=7 (111): {A, B, C}
```

The code writes itself:
```python
for mask in range(1 << n):
    subset = [items[i] for i in range(n) if mask & (1 << i)]
```

## Pattern 2: BFS with Bitmask State (TSP-style)

**The problem**: Find the shortest path visiting ALL nodes in a graph.

**The insight**: State = (current_node, set_of_visited_nodes)

```
State (node=2, visited=0b101)
  = "I'm at node 2, having visited nodes 0 and 2"

From here, I can go to node 1:
  new_state = (node=1, visited=0b101 | 0b010)
            = (node=1, visited=0b111)
            = "Now at node 1, visited {0, 1, 2}"
```

Why BFS works: All edges have weight 1, so BFS finds shortest paths.

```python
# Start from EVERY node (we can start anywhere)
for i in range(n):
    queue.append((i, 1 << i, 0))  # (node, mask, distance)

while queue:
    node, mask, dist = queue.popleft()

    for neighbor in graph[node]:
        new_mask = mask | (1 << neighbor)

        if new_mask == (1 << n) - 1:  # All visited!
            return dist + 1

        if (neighbor, new_mask) not in seen:
            queue.append((neighbor, new_mask, dist + 1))
```

**Visual**:
```
Graph: 0 — 1 — 2

Start: (0, 001, 0), (1, 010, 0), (2, 100, 0)

BFS Level 1:
  From (0, 001): → (1, 011, 1)
  From (1, 010): → (0, 011, 1), (2, 110, 1)
  From (2, 100): → (1, 110, 1)

BFS Level 2:
  From (1, 011): → (2, 111, 2) ← DONE! Distance = 2
```

## Pattern 3: Set Cover DP

**The problem**: Cover all required skills using minimum people. Each person has some subset of skills.

**The insight**: dp[skill_mask] = minimum team to achieve those skills

```
Required skills: [Python, Java, SQL]
Person 0: [Python]       → mask = 001
Person 1: [Java, SQL]    → mask = 110
Person 2: [Python, Java] → mask = 011

dp[000] = []           # No skills, no team needed
dp[001] = [0]          # Just Python = Person 0
dp[011] = [2]          # Python+Java = Person 2 (better than [0] + someone)
dp[110] = [1]          # Java+SQL = Person 1
dp[111] = [1, 2] or [0, 1]  # All skills
```

The transition:
```python
for person_id, person_mask in enumerate(person_masks):
    for current_mask, team in list(dp.items()):
        new_mask = current_mask | person_mask

        if new_mask not in dp or len(team) + 1 < len(dp[new_mask]):
            dp[new_mask] = team + [person_id]
```

## The Constraint: Why n ≤ 20?

Bitmask DP has exponential complexity. Here's the reality:

```
n     2^n          Feasibility
──────────────────────────────
10    1,024        ✓ Fast
15    32,768       ✓ OK
18    262,144      ✓ Borderline
20    1,048,576    ⚠ Slow but doable
22    4,194,304    ✗ Too slow
25    33,554,432   ✗ Way too slow
```

When you see n ≤ 20 in constraints, think "bitmask DP is probably intended."

## Common Mistakes

### Mistake 1: Wrong bit check

```python
❌ if mask & i:          # WRONG: i is not a bit
✅ if mask & (1 << i):   # RIGHT: 1 << i is the bit
```

### Mistake 2: Forgetting node in TSP state

```python
❌ State = just the visited mask
   (Same mask can be reached from different nodes!)

✅ State = (current_node, visited_mask)
```

### Mistake 3: Single-source BFS for TSP

```python
❌ queue = [(0, 1, 0)]  # Start only from node 0

✅ # Start from ALL nodes
   for i in range(n):
       queue.append((i, 1 << i, 0))
```

### Mistake 4: Modifying dict during iteration

```python
❌ for mask, team in dp.items():
       dp[new_mask] = ...  # Modifying during iteration!

✅ for mask, team in list(dp.items()):  # Copy to list first
       dp[new_mask] = ...
```

## Quick Pattern Recognition

| Clue | Pattern |
|------|---------|
| "All subsets" or "power set" | Subset Enumeration |
| "Visit all nodes", n ≤ 12 | BFS + Bitmask |
| "Minimum team to cover all", m ≤ 16 | Set Cover DP |
| "Partition into k equal groups" | Bitmask + DP |
| "Assign n tasks to n workers" | Bitmask permutation |

## The State Transition Mental Model

Think of bitmask DP as navigating a hypercube:

```
n=3: 8 states (vertices of a cube)

     011 -------- 111
    / |          / |
  001 -------- 101 |
   |  |         |  |
   | 010 -------|- 110
   | /          | /
  000 -------- 100

Transitions: Add one element = move along an edge
Full mask (111) = goal state
```

Every problem is about finding the best path from some starting vertex to the target vertex.

## Visual Summary

```
BITMASK DP PATTERNS:

1. SUBSET ENUM         2. BFS + BITMASK        3. SET COVER DP

   mask=0 to 2^n-1        (node, mask)            dp[mask] = team
        ↓                      ↓                       ↓
   decode to subset       BFS layers             person by person
        ↓                      ↓                       ↓
   collect results        first full_mask        min team for full
```

Bitmask DP is about **encoding set membership as integers** for O(1) transitions. The key is recognizing when your state is "which items are selected" and n is small enough (≤ 20).

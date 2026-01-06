# Union-Find Patterns: Complete Reference

> **API Kernel**: `UnionFindConnectivity`
> **Core Mechanism**: Maintain disjoint sets with efficient union and find operations using path compression and union by rank.

This document presents the **canonical Union-Find templates** covering connectivity queries, cycle detection, component counting, and equivalence grouping. Each implementation includes path compression and union by rank for near-constant time operations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Number of Provinces (LeetCode 547)](#2-number-of-provinces-leetcode-547)
3. [Redundant Connection (LeetCode 684)](#3-redundant-connection-leetcode-684)
4. [Accounts Merge (LeetCode 721)](#4-accounts-merge-leetcode-721)
5. [Number of Operations to Make Network Connected (LeetCode 1319)](#5-number-of-operations-to-make-network-connected-leetcode-1319)
6. [Satisfiability of Equality Equations (LeetCode 990)](#6-satisfiability-of-equality-equations-leetcode-990)
7. [Pattern Comparison](#7-pattern-comparison)
8. [Decision Framework](#8-decision-framework)
9. [Code Templates Summary](#9-code-templates-summary)

---

## 1. Core Concepts

### 1.1 Union-Find Data Structure

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))  # Initially, each node is its own parent
        self.rank = [0] * n           # Rank (tree depth upper bound)

    def find(self, x: int) -> int:
        """Find with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union by rank. Returns True if union performed (different sets)."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already in same set

        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

### 1.2 Why Path Compression?

```python
# Without path compression:
#     1           After find(5): 1→2→3→4→5
#    /            Every find traverses full chain: O(n)
#   2
#  /
# 3
#  \
#   4
#    \
#     5

# With path compression:
#       1         After find(5): All nodes point to root
#    / | \ \      Subsequent finds: O(1)
#   2  3  4  5
```

### 1.3 Why Union by Rank?

```python
# Without rank: Tree can become a linked list (O(n) per operation)
# With rank: Tree height stays O(log n)

# Union by rank: Always attach shorter tree under taller tree
# This keeps tree balanced
```

### 1.4 Time Complexity Analysis

| Operation | Amortized Time |
|-----------|---------------|
| Find | O(α(n)) ≈ O(1) |
| Union | O(α(n)) ≈ O(1) |
| Connected | O(α(n)) ≈ O(1) |

Where α(n) is the inverse Ackermann function, which grows extremely slowly (α(n) ≤ 4 for any practical n).

### 1.5 Pattern Variants

| Variant | Use When | Key Insight |
|---------|----------|-------------|
| **Connected Components** | Count/query connectivity | Each union reduces component count by 1 |
| **Cycle Detection** | Find redundant edges | Union returns False = cycle found |
| **Equivalence Grouping** | Group equivalent items | Map items to indices, then union |
| **Network Operations** | Min operations to connect | Components - 1 unions needed |

### 1.6 Common Operations

```python
# Check if connected
def connected(self, x: int, y: int) -> bool:
    return self.find(x) == self.find(y)

# Count connected components
def count_components(self) -> int:
    return sum(1 for i, p in enumerate(self.parent) if self.find(i) == i)

# Get size of component (need to track sizes)
def __init__(self, n: int):
    self.parent = list(range(n))
    self.rank = [0] * n
    self.size = [1] * n  # Track component sizes

def union(self, x: int, y: int) -> bool:
    px, py = self.find(x), self.find(y)
    if px == py:
        return False
    if self.rank[px] < self.rank[py]:
        px, py = py, px
    self.parent[py] = px
    self.size[px] += self.size[py]  # Update size
    if self.rank[px] == self.rank[py]:
        self.rank[px] += 1
    return True
```

---

## 2. Number of Provinces (LeetCode 547)

> **Problem**: Count connected components in an adjacency matrix graph.
> **Invariant**: Each union reduces component count by 1.
> **Role**: BASE TEMPLATE for Union-Find connectivity.

### 2.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "connected components" | → Union-Find or DFS |
| "adjacency matrix" | → Symmetric edges, union both (i,j) |
| "count groups" | → Track components during unions |

### 2.2 Implementation

```python
# Pattern: union_find_connected_components
# See: docs/patterns/union_find/templates.md Section 1 (Base Template)

class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        """
        Count number of provinces (connected components).

        Key Insight:
        - Start with n components (each city is its own province)
        - Each successful union reduces count by 1
        - Final count = number of provinces

        Why Union-Find over DFS?
        - Same complexity O(n²) for this problem
        - Union-Find is more natural for connectivity queries
        - Easier to extend for dynamic edge additions
        """
        n = len(isConnected)
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> bool:
            px, py = find(x), find(y)
            if px == py:
                return False
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True

        components = n
        for i in range(n):
            for j in range(i + 1, n):  # Only upper triangle (symmetric)
                if isConnected[i][j] == 1:
                    if union(i, j):
                        components -= 1

        return components
```

### 2.3 Trace Example

```
Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]

Cities: 0, 1, 2
Initial: components = 3, parent = [0, 1, 2]

Process edges:
- isConnected[0][1] = 1: union(0, 1) → success
  parent = [0, 0, 2], components = 2
- isConnected[0][2] = 0: skip
- isConnected[1][2] = 0: skip

Output: 2 (provinces: {0,1} and {2})
```

### 2.4 Visual Representation

```
Adjacency Matrix:      Graph:
   0  1  2
0 [1, 1, 0]           0 --- 1
1 [1, 1, 0]
2 [0, 0, 1]           2 (isolated)

Union-Find Forest:
  0                   2
  |
  1

Result: 2 components
```

### 2.5 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n² × α(n)) ≈ O(n²) |
| Space | O(n) for parent/rank arrays |

### 2.6 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 200: Number of Islands | Grid-based components |
| LC 323: Number of Connected Components | Edge list input |
| LC 1319: Network Operations | Count components + edge requirement |

---

## 3. Redundant Connection (LeetCode 684)

> **Problem**: Find the edge that creates a cycle in an undirected graph.
> **Invariant**: Union returns False when connecting already-connected nodes.
> **Role**: BASE TEMPLATE for cycle detection.

### 3.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "creates cycle" | → Union-Find: union returns False |
| "redundant edge" | → Edge connecting same component |
| "remove one edge" | → First (or last) edge creating cycle |

### 3.2 Implementation

```python
# Pattern: union_find_cycle_detection
# See: docs/patterns/union_find/templates.md Section 2

class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        """
        Find the edge that creates a cycle.

        Key Insight:
        - Process edges in order
        - Union returns False if nodes already connected
        - That edge is redundant (creates a cycle)

        Why this works:
        - In a tree with n nodes, there are n-1 edges
        - Adding one more edge creates exactly one cycle
        - The edge connecting already-connected nodes is redundant
        """
        n = len(edges)
        parent = list(range(n + 1))  # 1-indexed
        rank = [0] * (n + 1)

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> bool:
            px, py = find(x), find(y)
            if px == py:
                return False  # Cycle detected!
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True

        for u, v in edges:
            if not union(u, v):
                return [u, v]

        return []  # Should never reach here
```

### 3.3 Trace Example

```
Input: edges = [[1,2],[1,3],[2,3]]

Process:
1. union(1, 2): success, parent = [0, 1, 1, 3]
2. union(1, 3): success, parent = [0, 1, 1, 1]
3. union(2, 3): find(2)=1, find(3)=1, SAME! Return [2,3]

Output: [2, 3]
```

### 3.4 Visual Representation

```
Building graph:
Step 1: 1 --- 2         (union succeeds)
Step 2: 1 --- 2         (union succeeds)
        |
        3
Step 3: 1 --- 2         (union fails - cycle!)
        | \ /
        3

Edge [2,3] creates the cycle.
```

### 3.5 Edge Case: Multiple Valid Answers

```
Problem says: Return the LAST edge that creates a cycle
(if multiple edges could be removed)

Input: [[1,2],[2,3],[3,4],[1,4],[1,5]]

Graph: 1-2-3-4-1 (cycle) + 1-5

Edge [1,4] creates the cycle.
If we check [3,4] first: no cycle yet
If we check [1,4] second: cycle detected!
```

### 3.6 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n × α(n)) ≈ O(n) |
| Space | O(n) for parent/rank arrays |

### 3.7 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 685: Redundant Connection II | Directed graph (harder) |
| LC 261: Graph Valid Tree | Check if exactly n-1 edges |
| LC 1319: Network Operations | Count extra edges |

---

## 4. Accounts Merge (LeetCode 721)

> **Problem**: Merge accounts that share common emails.
> **Invariant**: Same email in different accounts = same person.
> **Role**: VARIANT applying Union-Find to string grouping.

### 4.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "merge by common element" | → Union-Find with element mapping |
| "group equivalent items" | → Map items to indices |
| "transitive equivalence" | → If A~B and B~C, then A~C |

### 4.2 Implementation

```python
# Pattern: union_find_equivalence_grouping
# See: docs/patterns/union_find/templates.md Section 3

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        """
        Merge accounts sharing common emails.

        Key Insight:
        - Map each email to first account index that has it
        - If email seen before, union current account with previous account
        - Collect emails by component root

        Why Union-Find?
        - Handles transitive relationships naturally
        - A shares email with B, B shares with C → A, B, C all merge
        """
        from collections import defaultdict

        n = len(accounts)
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> None:
            px, py = find(x), find(y)
            if px == py:
                return
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1

        # Map email to first account index
        email_to_account: dict[str, int] = {}

        for i, account in enumerate(accounts):
            for email in account[1:]:  # Skip name
                if email in email_to_account:
                    # Union this account with account that has same email
                    union(i, email_to_account[email])
                else:
                    email_to_account[email] = i

        # Collect emails by root
        root_to_emails: dict[int, set[str]] = defaultdict(set)
        for email, account_idx in email_to_account.items():
            root = find(account_idx)
            root_to_emails[root].add(email)

        # Build result
        result: list[list[str]] = []
        for root, emails in root_to_emails.items():
            name = accounts[root][0]
            result.append([name] + sorted(emails))

        return result
```

### 4.3 Trace Example

```
Input: accounts = [
    ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
    ["John", "johnsmith@mail.com", "john00@mail.com"],
    ["Mary", "mary@mail.com"],
    ["John", "johnnybravo@mail.com"]
]

Process:
Account 0: emails = {johnsmith@mail.com, john_newyork@mail.com}
  email_to_account = {johnsmith: 0, john_newyork: 0}

Account 1: emails = {johnsmith@mail.com, john00@mail.com}
  johnsmith seen! union(1, 0)
  email_to_account = {..., john00: 1}

Account 2: emails = {mary@mail.com}
  email_to_account = {..., mary: 2}

Account 3: emails = {johnnybravo@mail.com}
  email_to_account = {..., johnnybravo: 3}

Roots: 0→{johnsmith, john_newyork, john00}, 2→{mary}, 3→{johnnybravo}

Output: [
    ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
    ["Mary", "mary@mail.com"],
    ["John", "johnnybravo@mail.com"]
]
```

### 4.4 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n × k × α(n)) where k = avg emails per account |
| Space | O(n × k) for email mapping |

### 4.5 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 990: Equation Satisfaction | Group by character equality |
| LC 839: Similar String Groups | Group by string similarity |
| LC 1202: Smallest String With Swaps | Group by swap indices |

---

## 5. Number of Operations to Make Network Connected (LeetCode 1319)

> **Problem**: Find minimum operations to connect all computers.
> **Invariant**: Need (components - 1) edges to connect all components.
> **Role**: VARIANT combining component counting with edge availability.

### 5.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "make all connected" | → Count components, need c-1 edges |
| "rearrange edges" | → Count redundant edges (extras) |
| "minimum operations" | → Move redundant edges to connect |

### 5.2 Implementation

```python
# Pattern: union_find_network_connectivity
# See: docs/patterns/union_find/templates.md Section 4

class Solution:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        """
        Minimum cables to move to connect all computers.

        Key Insight:
        - Need at least n-1 edges to connect n nodes
        - Redundant edges (forming cycles) can be moved
        - Count components and check if enough redundant edges

        Algorithm:
        1. If edges < n-1: impossible (-1)
        2. Count components using Union-Find
        3. Need (components - 1) moves to connect all
        """
        if len(connections) < n - 1:
            return -1  # Not enough cables

        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> bool:
            px, py = find(x), find(y)
            if px == py:
                return False  # Redundant edge
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True

        components = n
        for a, b in connections:
            if union(a, b):
                components -= 1

        return components - 1
```

### 5.3 Trace Example

```
Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]

Check: 5 edges >= 5 (n-1)? Yes, possible.

Process:
- union(0,1): success, components = 5
- union(0,2): success, components = 4
- union(0,3): success, components = 3
- union(1,2): find(1)=0, find(2)=0, SAME (redundant)
- union(1,3): find(1)=0, find(3)=0, SAME (redundant)

Components: {0,1,2,3}, {4}, {5}
Need: 3 - 1 = 2 operations

Output: 2
```

### 5.4 Visual Representation

```
Initial:
0 --- 1           4        5
| \ / |
2   3

Operations needed:
- Move one redundant edge to connect {4}
- Move another redundant edge to connect {5}

After:
0 --- 1 --- 4 --- 5
| \ /
2   3
```

### 5.5 Edge Cases

```python
# Not enough edges
n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]
# 4 edges < 5 needed → return -1

# Already connected
n = 4, connections = [[0,1],[0,2],[1,2],[1,3],[2,3]]
# 1 component → return 0

# Worst case: all isolated
n = 4, connections = []
# 0 edges < 3 needed → return -1
```

### 5.6 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(E × α(n)) ≈ O(E) |
| Space | O(n) for parent/rank arrays |

### 5.7 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 547: Number of Provinces | Just count components |
| LC 1579: Remove Max Edges | Count edges to keep |
| LC 1101: Earliest Moment Friends Connected | Process edges in order |

---

## 6. Satisfiability of Equality Equations (LeetCode 990)

> **Problem**: Check if equality/inequality equations are satisfiable.
> **Invariant**: Equal variables must be in same component; unequal must be in different.
> **Role**: VARIANT applying Union-Find to constraint satisfaction.

### 6.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "equality constraints" | → Union-Find: union equal variables |
| "inequality constraints" | → Check: must be in different components |
| "satisfiable" | → Process equalities first, then check inequalities |

### 6.2 Implementation

```python
# Pattern: union_find_constraint_satisfaction
# See: docs/patterns/union_find/templates.md Section 5

class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        """
        Check if all equations can be satisfied.

        Key Insight:
        - Process '==' first: union all equal variables
        - Then check '!=': must be in different components
        - If any '!=' has variables in same component → unsatisfiable

        Why two passes?
        - Equality is transitive (a==b, b==c → a==c)
        - Must build all equality relationships before checking inequality
        """
        parent = list(range(26))  # 26 lowercase letters
        rank = [0] * 26

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> None:
            px, py = find(x), find(y)
            if px == py:
                return
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1

        # Pass 1: Process all equalities
        for eq in equations:
            if eq[1] == '=':  # "a==b"
                x = ord(eq[0]) - ord('a')
                y = ord(eq[3]) - ord('a')
                union(x, y)

        # Pass 2: Check all inequalities
        for eq in equations:
            if eq[1] == '!':  # "a!=b"
                x = ord(eq[0]) - ord('a')
                y = ord(eq[3]) - ord('a')
                if find(x) == find(y):
                    return False  # Contradiction!

        return True
```

### 6.3 Trace Example

```
Input: equations = ["a==b", "b!=c", "c==a"]

Pass 1 (equalities):
- "a==b": union(0, 1) → parent[1] = 0
- "c==a": union(2, 0) → parent[2] = 0

Components: {a, b, c} all in same component

Pass 2 (inequalities):
- "b!=c": find(b)=0, find(c)=0, SAME! → return False

Output: False
```

### 6.4 Another Example

```
Input: equations = ["a==b", "b==c", "a==c"]

Pass 1:
- union(a, b): {a, b}
- union(b, c): {a, b, c}
- union(a, c): already same component

Pass 2: No inequalities

Output: True
```

### 6.5 Edge Cases

```python
# Self-inequality
equations = ["a!=a"]
# Pass 1: nothing
# Pass 2: find(a) == find(a) → False

# Self-equality (trivially true)
equations = ["a==a"]
# Pass 1: union(a, a) → no-op
# Pass 2: nothing
# Output: True

# Disjoint groups with inequality
equations = ["a==b", "c==d", "a!=d"]
# Pass 1: {a,b}, {c,d}
# Pass 2: find(a)≠find(d) → True
```

### 6.6 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n × α(26)) ≈ O(n) |
| Space | O(1) (fixed 26 characters) |

### 6.7 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 721: Accounts Merge | Group by common elements |
| LC 399: Evaluate Division | Weighted Union-Find |
| LC 1061: Lexicographically Smallest Equivalent String | Find smallest in component |

---

---

## 7. Pattern Comparison

### 7.1 Union-Find vs DFS/BFS for Connectivity

| Aspect | Union-Find | DFS/BFS |
|--------|------------|---------|
| Build time | O(E × α(n)) | O(V + E) |
| Query time | O(α(n)) | O(V + E) |
| Dynamic edges | ✓ Efficient | ✗ Rebuild needed |
| Path info | ✗ Just connectivity | ✓ Can find path |
| Memory | O(V) | O(V + E) for adj list |

### 7.2 When to Use Union-Find

```python
# ✓ USE Union-Find when:
# - Multiple connectivity queries after building
# - Dynamic edge additions (but not deletions!)
# - Only need "are X and Y connected?" not "what's the path?"
# - Detecting cycles during graph construction

# ✗ DON'T USE Union-Find when:
# - Need to find actual path between nodes
# - Need to handle edge deletions
# - Single connectivity query (DFS is simpler)
# - Need shortest path (BFS is better)
```

### 7.3 Problem Type Recognition

| Problem Type | Key Signal | Approach |
|--------------|------------|----------|
| **Count components** | "how many groups" | Track count during unions |
| **Cycle detection** | "redundant edge", "creates cycle" | Union returns False |
| **Equivalence grouping** | "same group if share X" | Map items → indices |
| **Network connectivity** | "connect all", "minimum operations" | Components - 1 edges needed |
| **Constraint satisfaction** | "a==b", "a!=b" | Equality first, then check inequality |

### 7.4 Code Pattern Comparison

```python
# BASIC UNION-FIND (most problems)
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x, y):
    px, py = find(x), find(y)
    if px == py: return False
    parent[py] = px
    return True

# WITH RANK (balanced trees)
def union_by_rank(x, y):
    px, py = find(x), find(y)
    if px == py: return False
    if rank[px] < rank[py]: px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]: rank[px] += 1
    return True

# WITH SIZE TRACKING
def union_with_size(x, y):
    px, py = find(x), find(y)
    if px == py: return False
    if size[px] < size[py]: px, py = py, px
    parent[py] = px
    size[px] += size[py]
    return True
```

### 7.5 Optimization Techniques

| Technique | Effect | When Needed |
|-----------|--------|-------------|
| Path compression | Find → O(α(n)) | Always use |
| Union by rank | Balanced trees | Competitive programming |
| Union by size | Track component sizes | Size-related queries |
| Weighted Union-Find | Handle weighted relationships | Division evaluation |

---

---

## 8. Decision Framework

### 8.1 Quick Reference Decision Tree

```
START: Given connectivity/grouping problem
│
├─ "Count connected components"?
│   └─ YES → Union-Find with component counter
│            (LC 547, 1319 pattern)
│
├─ "Find cycle" or "redundant edge"?
│   └─ YES → Union-Find: union returns False = cycle
│            (LC 684 pattern)
│
├─ "Merge/group by common element"?
│   └─ YES → Map elements to indices, union on match
│            (LC 721 pattern)
│
├─ "Equality + inequality constraints"?
│   └─ YES → Two-pass: equalities first, then check inequalities
│            (LC 990 pattern)
│
├─ "Connect all with minimum operations"?
│   └─ YES → Count components, need c-1 moves
│            Check if enough extra edges
│            (LC 1319 pattern)
│
└─ "Path between nodes" or "shortest path"?
    └─ NO → Union-Find can help
    └─ YES → Use DFS/BFS instead
```

### 8.2 Feature Selection Guide

```
Need to track component sizes?
  → Add size[] array, update in union()

Need weighted relationships (like a/b = 2)?
  → Use weighted Union-Find with ratio tracking

Need to handle string keys (not just indices)?
  → Use dict for parent instead of list
  → Or map strings to indices first

Need to count redundant edges?
  → Count when union() returns False
```

### 8.3 Common Mistakes to Avoid

| Mistake | Why Wrong | Correct Approach |
|---------|-----------|------------------|
| Not using path compression | O(n) per find | Always compress path |
| Forgetting to update rank/size | Unbalanced trees | Update after linking |
| Processing order wrong | Wrong answer | Equalities before inequalities |
| Using 0-indexed for 1-indexed input | Off-by-one | Match problem indexing |
| Not checking if enough edges | Wrong answer for impossible | Check edges >= n-1 |

### 8.4 Index Mapping Patterns

```python
# 1-indexed nodes (LC 684)
parent = list(range(n + 1))  # Extra slot for 1-indexing

# Character indices (LC 990)
x = ord(char) - ord('a')  # 'a'->0, 'b'->1, etc.

# String to index mapping (LC 721)
string_to_idx = {}
for i, s in enumerate(strings):
    if s not in string_to_idx:
        string_to_idx[s] = len(string_to_idx)

# Coordinate to index (grid problems)
idx = row * cols + col
```

### 8.5 Complexity Expectations

| Operation | Expected Complexity |
|-----------|-------------------|
| Initialize | O(n) |
| Find (with path compression) | O(α(n)) ≈ O(1) |
| Union (with rank) | O(α(n)) ≈ O(1) |
| Process all edges | O(E × α(n)) |
| Count components | O(n) |

---

---

## 9. Code Templates Summary

### 9.1 Template 1: Basic Union-Find Class

```python
class UnionFind:
    """Standard Union-Find with path compression and union by rank."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
```

### 9.2 Template 2: Inline Functions (Competitive)

```python
def solve(n: int, edges: List[List[int]]) -> int:
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    # Use find() and union() here
```

### 9.3 Template 3: With Size Tracking

```python
class UnionFindWithSize:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        # Union by size
        if self.size[px] < self.size[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        return True

    def get_size(self, x: int) -> int:
        return self.size[self.find(x)]
```

### 9.4 Template 4: Cycle Detection (LC 684)

```python
def find_redundant_edge(edges: List[List[int]]) -> List[int]:
    n = len(edges)
    parent = list(range(n + 1))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return [u, v]  # Cycle found!
        parent[pv] = pu

    return []
```

### 9.5 Template 5: Constraint Satisfaction (LC 990)

```python
def check_equations(equations: List[str]) -> bool:
    parent = list(range(26))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    # Pass 1: Union equals
    for eq in equations:
        if eq[1] == '=':
            x, y = ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a')
            parent[find(y)] = find(x)

    # Pass 2: Check not-equals
    for eq in equations:
        if eq[1] == '!':
            x, y = ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a')
            if find(x) == find(y):
                return False

    return True
```

### 9.6 Pattern Selection Cheat Sheet

| Problem Signal | Template | Key Modification |
|---------------|----------|-----------------|
| "count components" | Template 1 | Track component count |
| "find cycle" | Template 4 | Return edge when union fails |
| "group by common" | Template 1 | Map items to indices |
| "equality constraints" | Template 5 | Two-pass processing |
| "component sizes" | Template 3 | Use size instead of rank |



---



*Document generated for NeetCode Practice Framework — API Kernel: UnionFindConnectivity*

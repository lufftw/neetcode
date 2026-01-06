# Bitmask DP Pattern

## Table of Contents

1. [API Kernel: `BitmaskDP`](#1-api-kernel-bitmaskdp)
2. [Why Bitmask DP?](#2-why-bitmask-dp)
3. [Core Insight](#3-core-insight)
4. [Bit Manipulation Cheat Sheet](#4-bit-manipulation-cheat-sheet)
5. [Universal Template Structure](#5-universal-template-structure)
6. [Pattern Variants](#6-pattern-variants)
7. [State Space Analysis](#7-state-space-analysis)
8. [Common Patterns](#8-common-patterns)
9. [Problem Link](#9-problem-link)
10. [Difficulty](#10-difficulty)
11. [Tags](#11-tags)
12. [Pattern](#12-pattern)
13. [API Kernel](#13-api-kernel)
14. [Problem Summary](#14-problem-summary)
15. [Key Insight](#15-key-insight)
16. [Template Mapping](#16-template-mapping)
17. [Complexity](#17-complexity)
18. [Why This Problem First?](#18-why-this-problem-first)
19. [Common Mistakes](#19-common-mistakes)
20. [Related Problems](#20-related-problems)
21. [Problem Link](#21-problem-link)
22. [Difficulty](#22-difficulty)
23. [Tags](#23-tags)
24. [Pattern](#24-pattern)
25. [API Kernel](#25-api-kernel)
26. [Problem Summary](#26-problem-summary)
27. [Key Insight](#27-key-insight)
28. [Template Mapping](#28-template-mapping)
29. [Complexity](#29-complexity)
30. [Why This Problem Second?](#30-why-this-problem-second)
31. [Key Observations](#31-key-observations)
32. [Common Mistakes](#32-common-mistakes)
33. [Related Problems](#33-related-problems)
34. [Problem Link](#34-problem-link)
35. [Difficulty](#35-difficulty)
36. [Tags](#36-tags)
37. [Pattern](#37-pattern)
38. [API Kernel](#38-api-kernel)
39. [Problem Summary](#39-problem-summary)
40. [Key Insight](#40-key-insight)
41. [Template Mapping](#41-template-mapping)
42. [Complexity](#42-complexity)
43. [Why This Problem Third?](#43-why-this-problem-third)
44. [Key Observations](#44-key-observations)
45. [Optimization: Prune Dominated People](#45-optimization-prune-dominated-people)
46. [Common Mistakes](#46-common-mistakes)
47. [Related Problems](#47-related-problems)
48. [Problem Comparison](#48-problem-comparison)
49. [Pattern Evolution](#49-pattern-evolution)
50. [Key Differences](#50-key-differences)
51. [Common Bit Operations Across Problems](#51-common-bit-operations-across-problems)
52. [When to Use Each Pattern](#52-when-to-use-each-pattern)
53. [Decision Tree](#53-decision-tree)
54. [Pattern Selection Guide](#54-pattern-selection-guide)
55. [Red Flags - When NOT to Use Bitmask DP](#55-red-flags---when-not-to-use-bitmask-dp)
56. [Quick Pattern Identification](#56-quick-pattern-identification)
57. [Integration with Other Patterns](#57-integration-with-other-patterns)
58. [Universal Templates](#58-universal-templates)
59. [Bit Manipulation Utilities](#59-bit-manipulation-utilities)
60. [Complexity Reference](#60-complexity-reference)

---

## 1. API Kernel: `BitmaskDP`

> **Core Mechanism**: Represent set states using integers as bitmasks, enabling efficient DP over subsets with O(1) state transitions.

## 2. Why Bitmask DP?

Bitmask DP solves problems where:
- You need to track "which items are selected/visited"
- State space is over subsets of a small set (n ≤ 20)
- Standard DP would have exponential states

## 3. Core Insight

An integer's binary representation encodes a subset:
```
Set: {A, B, C, D}  (indices 0, 1, 2, 3)

Bitmask   Binary   Subset
0         0000     {}
5         0101     {A, C}
15        1111     {A, B, C, D}
```

## 4. Bit Manipulation Cheat Sheet

| Operation | Code | Example |
|-----------|------|---------|
| Set bit i | `mask | (1 << i)` | Add element i |
| Clear bit i | `mask & ~(1 << i)` | Remove element i |
| Check bit i | `(mask >> i) & 1` | Is i in set? |
| Toggle bit i | `mask ^ (1 << i)` | Flip membership |
| Count bits | `bin(mask).count('1')` | Set size |
| All bits set | `(1 << n) - 1` | Full set |

## 5. Universal Template Structure

```python
def bitmask_dp(n, items):
    # State: dp[mask] = value for subset represented by mask
    # Iterate over all 2^n subsets
    for mask in range(1 << n):
        for i in range(n):
            if mask & (1 << i):  # If i is in current subset
                prev_mask = mask ^ (1 << i)  # Subset without i
                dp[mask] = transition(dp[prev_mask], items[i])

    return dp[(1 << n) - 1]  # Full set
```

## 6. Pattern Variants

| Pattern | State | Transition | Example |
|---------|-------|------------|---------|
| **Subset Enumeration** | Generate all subsets | Bit operations | Subsets |
| **TSP-style** | dp[mask][last] | Visit new node | Shortest Path All Nodes |
| **Set Cover** | dp[mask] | Add person's skills | Smallest Sufficient Team |
| **Subset Sum** | dp[mask] | Include/exclude | Partition Equal Subset |

## 7. State Space Analysis

For n elements:
- Number of subsets: 2^n
- Memory: O(2^n) for bitmask states
- Practical limit: n ≤ 20 (2^20 ≈ 10^6)

## 8. Common Patterns

### 8.1 Pattern 1: Generate All Subsets
```python
def subsets(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result
```

### 8.2 Pattern 2: TSP / Hamiltonian Path
```python
# dp[mask][last] = min cost to visit nodes in mask, ending at last
for mask in range(1, 1 << n):
    for last in range(n):
        if not (mask & (1 << last)):
            continue
        prev_mask = mask ^ (1 << last)
        for prev in range(n):
            if prev_mask & (1 << prev):
                dp[mask][last] = min(dp[mask][last],
                                     dp[prev_mask][prev] + cost[prev][last])
```

### 8.3 Pattern 3: Set Cover
```python
# dp[mask] = min items to cover skills in mask
for i in range(num_people):
    skill_mask = encode_skills(people[i])
    for mask in range(1 << num_skills):
        new_mask = mask | skill_mask
        dp[new_mask] = min(dp[new_mask], dp[mask] + 1)
```

---

# 78. Subsets

## 9. Problem Link
https://leetcode.com/problems/subsets/

## 10. Difficulty
Medium

## 11. Tags
- Bitmask
- Subset Enumeration
- Bit Manipulation

## 12. Pattern
Bitmask DP - Subset Enumeration

## 13. API Kernel
`BitmaskDP`

## 14. Problem Summary
Given an integer array `nums` of unique elements, return all possible subsets (the power set).

## 15. Key Insight

Each subset corresponds to a unique bitmask from 0 to 2^n - 1:
- Bit i is set → include nums[i]
- Bit i is clear → exclude nums[i]

This gives O(2^n) subsets directly without recursion.

## 16. Template Mapping

```python
def subsets(nums):
    n = len(nums)
    result = []

    # Enumerate all 2^n bitmasks
    for mask in range(1 << n):
        # Build subset from mask
        subset = []
        for i in range(n):
            if mask & (1 << i):  # Check if bit i is set
                subset.append(nums[i])
        result.append(subset)

    return result
```

## 17. Complexity
- Time: O(n × 2^n) - iterate through all masks, each taking O(n) to decode
- Space: O(n × 2^n) - storing all subsets

## 18. Why This Problem First?

1. **Pure bitmask enumeration** - No DP, just understanding bitmask-to-subset mapping
2. **Foundation for all bitmask DP** - The enumeration loop `for mask in range(1 << n)` is universal
3. **Bit operation practice** - Check bit with `mask & (1 << i)`

## 19. Common Mistakes

1. **Off-by-one in range** - Should be `range(1 << n)`, not `range((1 << n) - 1)`
2. **Wrong bit check** - Use `mask & (1 << i)`, not `mask & i`
3. **Modifying mask during iteration** - Decode mask, don't modify it

## 20. Related Problems
- LC 90: Subsets II (with duplicates)
- LC 784: Letter Case Permutation
- LC 1286: Iterator for Combination

---

# 847. Shortest Path Visiting All Nodes

## 21. Problem Link
https://leetcode.com/problems/shortest-path-visiting-all-nodes/

## 22. Difficulty
Hard

## 23. Tags
- Bitmask DP
- BFS
- Graph
- State Compression

## 24. Pattern
Bitmask DP - TSP-style / BFS with Bitmask State

## 25. API Kernel
`BitmaskDP`

## 26. Problem Summary
Given an undirected graph with n nodes, find the length of the shortest path that visits every node. You may start and stop at any node, revisit nodes, and reuse edges.

## 27. Key Insight

State = (current_node, visited_mask):
- `visited_mask` tracks which nodes have been visited
- BFS explores all states level by level
- First state with `visited_mask == (1 << n) - 1` is the answer

Unlike classic TSP, we can revisit nodes, so BFS works (no need for DP minimum tracking).

## 28. Template Mapping

```python
from collections import deque

def shortestPathLength(graph):
    n = len(graph)
    if n == 1:
        return 0

    full_mask = (1 << n) - 1

    # State: (node, visited_mask)
    # Initialize: start from every node
    queue = deque()
    visited = set()

    for i in range(n):
        state = (i, 1 << i)
        queue.append((i, 1 << i, 0))  # (node, mask, distance)
        visited.add(state)

    while queue:
        node, mask, dist = queue.popleft()

        for neighbor in graph[node]:
            new_mask = mask | (1 << neighbor)

            if new_mask == full_mask:
                return dist + 1

            state = (neighbor, new_mask)
            if state not in visited:
                visited.add(state)
                queue.append((neighbor, new_mask, dist + 1))

    return -1  # Should never reach here for connected graph
```

## 29. Complexity
- Time: O(n × 2^n) - n nodes × 2^n possible masks
- Space: O(n × 2^n) - visited states

## 30. Why This Problem Second?

1. **Combines BFS with bitmask** - State includes both position and visited set
2. **TSP variant** - Classic interview pattern
3. **State space explosion** - Shows why n ≤ 12 constraint is critical

## 31. Key Observations

1. **Multi-source BFS** - Start from all nodes simultaneously
2. **State deduplication** - (node, mask) pair uniquely identifies state
3. **Early termination** - Return immediately when full_mask reached

## 32. Common Mistakes

1. **Single-source BFS** - Must try all starting nodes
2. **Forgetting node in state** - State is (node, mask), not just mask
3. **Not handling n=1** - Edge case returns 0

## 33. Related Problems
- LC 943: Find the Shortest Superstring
- LC 1494: Parallel Courses II
- LC 1066: Campus Bikes II

---

# 1125. Smallest Sufficient Team

## 34. Problem Link
https://leetcode.com/problems/smallest-sufficient-team/

## 35. Difficulty
Hard

## 36. Tags
- Bitmask DP
- Set Cover
- Dynamic Programming

## 37. Pattern
Bitmask DP - Set Cover

## 38. API Kernel
`BitmaskDP`

## 39. Problem Summary
Given a list of required skills and people with their skills, find the smallest team such that all required skills are covered.

## 40. Key Insight

Represent skill coverage as bitmask:
- `dp[mask]` = minimum team to cover skills in mask
- For each person, their skills form a bitmask
- Transition: `dp[mask | person_skills] = min(dp[mask | person_skills], dp[mask] + person)`

## 41. Template Mapping

```python
def smallestSufficientTeam(req_skills, people):
    n = len(req_skills)
    skill_to_idx = {s: i for i, s in enumerate(req_skills)}

    # Encode each person's skills as bitmask
    person_masks = []
    for skills in people:
        mask = 0
        for skill in skills:
            if skill in skill_to_idx:
                mask |= (1 << skill_to_idx[skill])
        person_masks.append(mask)

    full_mask = (1 << n) - 1

    # dp[mask] = smallest team to achieve skill mask
    dp = {0: []}

    for i, person_mask in enumerate(person_masks):
        # Iterate over copy of current states
        for mask, team in list(dp.items()):
            new_mask = mask | person_mask

            # Only update if this gives a smaller team
            if new_mask not in dp or len(dp[new_mask]) > len(team) + 1:
                dp[new_mask] = team + [i]

    return dp[full_mask]
```

## 42. Complexity
- Time: O(2^m × n) where m = number of skills, n = number of people
- Space: O(2^m) - storing teams for each skill mask

## 43. Why This Problem Third?

1. **Classic set cover** - NP-hard problem made tractable with bitmask DP
2. **Optimization DP** - Track minimum, not just reachability
3. **Team reconstruction** - Return actual indices, not just count

## 44. Key Observations

1. **Skill encoding** - Map skill names to bit positions
2. **Monotonic improvement** - Only update if strictly better team found
3. **State explosion control** - m ≤ 16 constraint makes bitmask feasible

## 45. Optimization: Prune Dominated People

```python
# Remove people whose skills are subset of another person
def prune_dominated(person_masks):
    n = len(person_masks)
    keep = [True] * n
    for i in range(n):
        for j in range(n):
            if i != j and (person_masks[i] | person_masks[j]) == person_masks[j]:
                # Person i is dominated by person j
                keep[i] = False
                break
    return [i for i in range(n) if keep[i]]
```

## 46. Common Mistakes

1. **Mutating dict during iteration** - Use `list(dp.items())`
2. **Wrong optimization direction** - Minimize team size, not maximize skills
3. **Forgetting skill mapping** - Skills are strings, need index mapping

## 47. Related Problems
- LC 1494: Parallel Courses II
- LC 1723: Find Minimum Time to Finish All Jobs
- LC 1986: Minimum Number of Work Sessions

---

## 48. Problem Comparison

| Problem | Core Pattern | State | Transition | Output |
|---------|-------------|-------|------------|--------|
| **78. Subsets** | Subset Enumeration | mask (visited) | Decode mask to subset | List of subsets |
| **847. Shortest Path** | BFS + Bitmask | (node, mask) | `mask | (1 << neighbor)` | Min path length |
| **1125. Smallest Team** | Set Cover DP | mask (skills) | `mask | person_skills` | Min team members |

## 49. Pattern Evolution

```
Subset Enumeration (LC 78)
        ↓
    Pure bitmask iteration
    No DP needed
        ↓
BFS + Bitmask (LC 847)
        ↓
    Add position to state
    BFS for shortest path
        ↓
Set Cover DP (LC 1125)
        ↓
    Optimization DP
    Track minimum team
```

## 50. Key Differences

### 50.1 1. State Complexity

| Problem | State Dimensions | State Space |
|---------|-----------------|-------------|
| LC 78 | 1D (mask only) | O(2^n) |
| LC 847 | 2D (node, mask) | O(n × 2^n) |
| LC 1125 | 1D (mask) + team | O(2^m) |

### 50.2 2. Traversal Strategy

| Problem | Strategy | Why |
|---------|----------|-----|
| LC 78 | Linear enumeration | Generate all subsets |
| LC 847 | BFS | Shortest path in unweighted graph |
| LC 1125 | DP with iteration | Minimize team size |

### 50.3 3. Constraint Limits

| Problem | n/m Limit | State Space | Why Limit |
|---------|-----------|-------------|-----------|
| LC 78 | n ≤ 10 | 2^10 = 1024 | Generate all subsets |
| LC 847 | n ≤ 12 | 12 × 2^12 ≈ 50K | BFS state space |
| LC 1125 | m ≤ 16 | 2^16 = 65K | DP state space |

## 51. Common Bit Operations Across Problems

```python
# All three problems use these operations:

# 1. Set bit i (add element)
mask | (1 << i)

# 2. Check bit i (is element present?)
mask & (1 << i)  # or (mask >> i) & 1

# 3. Full mask (all elements)
(1 << n) - 1

# 4. Iterate bits
for i in range(n):
    if mask & (1 << i):
        # Process element i
```

## 52. When to Use Each Pattern

| If you need to... | Use Pattern | Example |
|-------------------|-------------|---------|
| Generate all subsets | Enumeration (LC 78) | Subsets, Combinations |
| Find shortest path visiting all | BFS + Bitmask (LC 847) | TSP variants |
| Cover requirements with minimum | Set Cover DP (LC 1125) | Team building, task assignment |

---

## 53. Decision Tree

```
Start: Need to track "which elements are selected/visited"?
       AND set size ≤ 20?
                    │
                    ▼
              ┌─────────────────────────────────────────┐
              │   BITMASK DP is likely applicable       │
              └─────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │ What are you optimizing?  │
        └───────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
Generate all   Shortest path   Minimize count
  subsets      visiting all    to cover all
    │               │               │
    ▼               ▼               ▼
┌─────────┐   ┌───────────┐   ┌───────────┐
│ SUBSET  │   │ BFS +     │   │ SET COVER │
│ ENUM    │   │ BITMASK   │   │ DP        │
│ (LC 78) │   │ (LC 847)  │   │ (LC 1125) │
└─────────┘   └───────────┘   └───────────┘
```

## 54. Pattern Selection Guide

### 54.1 Use Subset Enumeration (LC 78) when:
- ✅ Need to generate all possible subsets
- ✅ No optimization objective
- ✅ Just enumerate possibilities
- ✅ n ≤ 15 (2^15 = 32K subsets)

### 54.2 Use BFS + Bitmask (LC 847) when:
- ✅ Need shortest path in state space
- ✅ State includes "which nodes visited"
- ✅ Can revisit nodes (BFS works)
- ✅ n ≤ 12-15 (state space n × 2^n)

### 54.3 Use Set Cover DP (LC 1125) when:
- ✅ Need minimum items to cover requirements
- ✅ Each item covers a subset of requirements
- ✅ Requirements can be encoded as bitmask
- ✅ m ≤ 16-20 requirements

## 55. Red Flags - When NOT to Use Bitmask DP

| Red Flag | Why | Alternative |
|----------|-----|-------------|
| n > 20 | 2^20 ≈ 10^6, too slow | Greedy/approximation |
| Order matters | Need permutation, not subset | Backtracking |
| Continuous values | Can't encode as bits | Standard DP |
| Duplicates in set | Bits can't handle multiplicity | HashMap DP |

## 56. Quick Pattern Identification

### 56.1 Keywords → Pattern

| Keywords | Pattern |
|----------|---------|
| "all subsets", "power set" | Subset Enumeration |
| "visit all nodes", "TSP" | BFS + Bitmask |
| "minimum team", "cover all" | Set Cover DP |
| "partition into groups" | Bitmask + DP |
| "assign tasks to workers" | Bitmask + DP |

### 56.2 Constraint → Pattern

| Constraint | Suggests |
|------------|----------|
| n ≤ 10 | Any bitmask pattern safe |
| n ≤ 12 | 2D bitmask (node, mask) ok |
| n ≤ 16 | 1D bitmask DP ok |
| n ≤ 20 | Tight, may need pruning |
| n > 20 | NOT bitmask DP |

## 57. Integration with Other Patterns

Bitmask DP often combines with:

1. **BFS** (LC 847) - For shortest path in bitmask state space
2. **Standard DP** - Bitmask as one dimension
3. **Backtracking** - Generate subsets recursively
4. **Greedy** - Prune dominated choices before DP

---

## 58. Universal Templates

### 58.1 Template 1: Subset Enumeration

```python
def enumerate_subsets(nums):
    """Generate all 2^n subsets using bitmask."""
    n = len(nums)
    result = []

    for mask in range(1 << n):
        # Decode bitmask to subset
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)

    return result
```

**Use for**: LC 78, 90, 784, 1286

---

### 58.2 Template 2: BFS + Bitmask State

```python
from collections import deque

def bfs_bitmask(graph):
    """BFS with (node, visited_mask) state."""
    n = len(graph)
    full_mask = (1 << n) - 1

    # Initialize: start from every node
    queue = deque()
    visited = set()

    for i in range(n):
        state = (i, 1 << i)
        queue.append((i, 1 << i, 0))  # (node, mask, dist)
        visited.add(state)

    while queue:
        node, mask, dist = queue.popleft()

        for neighbor in graph[node]:
            new_mask = mask | (1 << neighbor)

            # Early termination
            if new_mask == full_mask:
                return dist + 1

            state = (neighbor, new_mask)
            if state not in visited:
                visited.add(state)
                queue.append((neighbor, new_mask, dist + 1))

    return -1
```

**Use for**: LC 847, 943, 1494

---

### 58.3 Template 3: Set Cover DP

```python
def set_cover_dp(required_mask, item_masks):
    """
    Find minimum items to cover all requirements.

    Args:
        required_mask: Target mask to achieve
        item_masks: List of (item_id, mask) tuples

    Returns:
        List of item indices forming minimum cover
    """
    # dp[mask] = smallest set of items to achieve mask
    dp = {0: []}

    for item_id, item_mask in item_masks:
        # Iterate over copy of current states
        for mask, items in list(dp.items()):
            new_mask = mask | item_mask

            # Only update if strictly better
            if new_mask not in dp or len(dp[new_mask]) > len(items) + 1:
                dp[new_mask] = items + [item_id]

    return dp.get(required_mask, [])
```

**Use for**: LC 1125, 1723, 1986

---

### 58.4 Template 4: TSP-style DP

```python
def tsp_dp(dist):
    """
    Classic TSP: minimum cost to visit all nodes.

    Args:
        dist: n×n distance matrix

    Returns:
        Minimum cost to visit all nodes starting from node 0
    """
    n = len(dist)
    INF = float('inf')

    # dp[mask][last] = min cost to visit nodes in mask, ending at last
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Start at node 0

    for mask in range(1, 1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if dp[mask][last] == INF:
                continue

            for next_node in range(n):
                if mask & (1 << next_node):
                    continue

                new_mask = mask | (1 << next_node)
                dp[new_mask][next_node] = min(
                    dp[new_mask][next_node],
                    dp[mask][last] + dist[last][next_node]
                )

    full_mask = (1 << n) - 1
    return min(dp[full_mask])
```

**Use for**: TSP variants, Hamiltonian path problems

---

## 59. Bit Manipulation Utilities

```python
# Essential bit operations

def set_bit(mask, i):
    """Add element i to set."""
    return mask | (1 << i)

def clear_bit(mask, i):
    """Remove element i from set."""
    return mask & ~(1 << i)

def has_bit(mask, i):
    """Check if element i is in set."""
    return (mask >> i) & 1

def toggle_bit(mask, i):
    """Toggle element i membership."""
    return mask ^ (1 << i)

def count_bits(mask):
    """Count elements in set."""
    return bin(mask).count('1')

def full_mask(n):
    """Create mask with all n bits set."""
    return (1 << n) - 1

def iterate_bits(mask, n):
    """Yield indices of set bits."""
    for i in range(n):
        if mask & (1 << i):
            yield i

def submasks(mask):
    """Iterate all submasks of mask (excluding 0)."""
    sub = mask
    while sub:
        yield sub
        sub = (sub - 1) & mask
```

---

## 60. Complexity Reference

| Pattern | Time | Space | Practical n |
|---------|------|-------|-------------|
| Subset Enum | O(n × 2^n) | O(n × 2^n) | n ≤ 15 |
| BFS + Bitmask | O(n × 2^n) | O(n × 2^n) | n ≤ 12 |
| Set Cover DP | O(m × 2^m) | O(2^m) | m ≤ 16 |
| TSP DP | O(n^2 × 2^n) | O(n × 2^n) | n ≤ 18 |



---



*Document generated for NeetCode Practice Framework — API Kernel: bitmask_dp*

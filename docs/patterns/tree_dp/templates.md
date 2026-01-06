# Tree DP Pattern

## Table of Contents

1. [API Kernel: `TreeDP`](#1-api-kernel-treedp)
2. [Why Tree DP?](#2-why-tree-dp)
3. [Core Insight](#3-core-insight)
4. [Universal Template Structure](#4-universal-template-structure)
5. [State Design Strategies](#5-state-design-strategies)
6. [State Transition Patterns](#6-state-transition-patterns)
7. [Pattern Variants](#7-pattern-variants)
8. [Problem: House Robber III (LC 337)](#8-problem-house-robber-iii-lc-337)
9. [Problem: Binary Tree Maximum Path Sum (LC 124)](#9-problem-binary-tree-maximum-path-sum-lc-124)
10. [Problem: Binary Tree Cameras (LC 968)](#10-problem-binary-tree-cameras-lc-968)
11. [Pattern Comparison](#11-pattern-comparison)
12. [State Design Summary](#12-state-design-summary)
13. [Complexity Comparison](#13-complexity-comparison)
14. [Return Value vs Global State](#14-return-value-vs-global-state)
15. [When to Use Tree DP](#15-when-to-use-tree-dp)
16. [Quick Reference Templates](#16-quick-reference-templates)
17. [State Design Cheat Sheet](#17-state-design-cheat-sheet)

---

## 1. API Kernel: `TreeDP`

> **Core Mechanism**: Apply dynamic programming on tree structures by computing states bottom-up (post-order) where each node's state depends on its children's states.

## 2. Why Tree DP?

Tree DP solves optimization problems on trees where:
- You need to make decisions at each node (include/exclude, color, etc.)
- The optimal solution depends on subtree solutions
- Simple greedy doesn't work due to dependent choices

## 3. Core Insight

Trees have a natural recursive structure. Process children first (post-order DFS), then combine their states to compute the parent's state.

```
       1
      / \
     2   3
    / \
   4   5

Post-order: 4 → 5 → 2 → 3 → 1

At each node, compute:
dp[node] = f(dp[children], node_value)
```

## 4. Universal Template Structure

```python
def tree_dp(root):
    def dfs(node):
        if not node:
            return base_state

        # Process children first (post-order)
        left_state = dfs(node.left)
        right_state = dfs(node.right)

        # Compute current node's state from children
        current_state = combine(left_state, right_state, node.val)

        return current_state

    return extract_answer(dfs(root))
```

## 5. State Design Strategies

| Pattern | State Type | Example |
|---------|------------|---------|
| **Include/Exclude** | (with_node, without_node) | House Robber III |
| **Path Through Node** | max_path_ending_here | Max Path Sum |
| **Coverage States** | (covered, has_camera, not_covered) | Binary Tree Cameras |
| **Subtree Info** | (height, is_balanced) | Balanced Tree Check |

## 6. State Transition Patterns

### 6.1 Pattern 1: Include/Exclude (House Robber)
```python
def dfs(node):
    if not node:
        return (0, 0)  # (with, without)

    left = dfs(node.left)
    right = dfs(node.right)

    # Include current: can't include children
    with_current = node.val + left[1] + right[1]
    # Exclude current: take max of children
    without_current = max(left) + max(right)

    return (with_current, without_current)
```

### 6.2 Pattern 2: Path Contribution (Max Path Sum)
```python
def dfs(node):
    nonlocal max_sum

    if not node:
        return 0

    # Max contribution from each child (can't take negative)
    left = max(0, dfs(node.left))
    right = max(0, dfs(node.right))

    # Path through this node
    path_sum = node.val + left + right
    max_sum = max(max_sum, path_sum)

    # Return max single-branch contribution
    return node.val + max(left, right)
```

### 6.3 Pattern 3: Multi-State (Camera Coverage)
```python
# States: 0=not covered, 1=covered no camera, 2=has camera
def dfs(node):
    if not node:
        return 1  # null nodes are "covered"

    left = dfs(node.left)
    right = dfs(node.right)

    if left == 0 or right == 0:
        return 2  # Must place camera
    if left == 2 or right == 2:
        return 1  # Covered by child's camera
    return 0  # Not covered, needs parent
```

## 7. Pattern Variants

1. **Binary Choice**: Include/exclude node in solution
2. **Path Optimization**: Find optimal path through nodes
3. **State Machine**: Multiple states per node with transitions
4. **Aggregation**: Collect information from entire subtree

---

## 8. Problem: House Robber III (LC 337)

> **Base Template** for include/exclude tree DP.

### 8.1 Problem Statement

The thief has found a new place for thievery. Houses form a binary tree. If two directly-linked houses are broken into, they will alert the police. Maximize the total amount robbed.

### 8.2 Pattern: Include/Exclude DP

**Invariant**: For each node, track two states:
- Maximum if we **include** this node
- Maximum if we **exclude** this node

**Key Insight**: If we include parent, we can't include children. If we exclude parent, children are independent.

### 8.3 Algorithm

```
Tree:     3
         / \
        4   5
       / \   \
      1   3   1

Post-order computation:
  Node 1: include=1, exclude=0
  Node 3: include=3, exclude=0
  Node 4: include=4+0+0=4, exclude=max(1,0)+max(3,0)=4
  Node 5: include=5+0=5, exclude=max(1,0)=1
  Node 1: include=1, exclude=0
  Node 3: include=3+4+1=8, exclude=max(4,4)+max(5,1)=9

Answer: max(8, 9) = 9 (rob nodes 4, 5, and leaf 3)
```

### 8.4 Implementation

```python
def rob(root: TreeNode) -> int:
    def dfs(node):
        if not node:
            return (0, 0)  # (include, exclude)

        left = dfs(node.left)
        right = dfs(node.right)

        # Include this node: must exclude children
        include = node.val + left[1] + right[1]

        # Exclude this node: children are free choice
        exclude = max(left) + max(right)

        return (include, exclude)

    return max(dfs(root))
```

### 8.5 State Transition Diagram

```
        Parent
       /      \
    Child    Child

Include parent → must exclude both children
Exclude parent → each child can be included or excluded (independent)
```

### 8.6 Complexity

- **Time**: O(n) - visit each node once
- **Space**: O(h) - recursion stack depth (h = tree height)

### 8.7 Why Two States Work

The key constraint is "adjacent nodes can't both be selected." With two states per node, we capture all legal combinations:
- Parent included → children must be excluded
- Parent excluded → children independently optimal

---

## 9. Problem: Binary Tree Maximum Path Sum (LC 124)

> **Variant**: Path optimization tree DP.

### 9.1 Problem Statement

A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge. The path sum is the sum of node values. Find the maximum path sum.

### 9.2 Pattern: Path Contribution DP

**Invariant**: For each node, track the maximum contribution it can make to a path extending upward.

**Key Insight**: A path can:
1. Go through a node (left → node → right)
2. Extend from a node upward (can only use one branch)

**Delta from Base**: Track global maximum separately from returned value.

### 9.3 Algorithm

```
Tree:    -10
        /    \
       9      20
            /    \
           15     7

DFS returns (max contribution upward):
  Node 9:  return 9, global max = 9
  Node 15: return 15, global max = 15
  Node 7:  return 7, global max = 15
  Node 20: path=20+15+7=42, return 20+15=35, global=42
  Node -10: path=-10+9+35=34, return max(-10+9,-10+35)=25

Answer: 42 (path 15 → 20 → 7)
```

### 9.4 Implementation

```python
def maxPathSum(root: TreeNode) -> int:
    max_sum = float('-inf')

    def dfs(node):
        nonlocal max_sum

        if not node:
            return 0

        # Max contribution from children (ignore negative)
        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))

        # Path through this node (potential answer)
        path_through = node.val + left + right
        max_sum = max(max_sum, path_through)

        # Return max single-branch contribution
        # (path can only extend one way upward)
        return node.val + max(left, right)

    dfs(root)
    return max_sum
```

### 9.5 Why Return Only One Branch?

```
      A
     / \
    B   C

If we're building a path from A's parent:
- We can go Parent → A → B (one branch)
- We can go Parent → A → C (one branch)
- We CAN'T go B ← A → C then up to Parent (path would branch)

So we return the max single-branch contribution.
```

### 9.6 Key Differences from House Robber

| Aspect | House Robber | Max Path Sum |
|--------|--------------|--------------|
| State | (include, exclude) | single value |
| Return | both states | max contribution upward |
| Answer | max of root states | global max (any node) |
| Negative | keep if positive | clamp to 0 |

### 9.7 Complexity

- **Time**: O(n)
- **Space**: O(h)

### 9.8 Edge Cases

1. **Single node**: Answer is node.val
2. **All negative**: Must include at least one node
3. **Negative children**: Clamp contribution to 0 (don't use negative branches)

---

## 10. Problem: Binary Tree Cameras (LC 968)

> **Advanced Variant**: Multi-state tree DP.

### 10.1 Problem Statement

You are given the root of a binary tree. Install cameras on tree nodes such that every node is monitored. A camera can monitor its parent, itself, and immediate children. Return the minimum number of cameras needed.

### 10.2 Pattern: State Machine DP

**Invariant**: Each node is in one of three states:
- **State 0**: Not covered (needs parent's camera)
- **State 1**: Covered but no camera here
- **State 2**: Has camera (covers parent and children)

**Delta from Base**: Three states with coverage rules.

### 10.3 Algorithm

```
Tree:     0
         /
        0
       / \
      0   0

Post-order (leaves first):
  Leaf nodes: return 0 (not covered)
  Parent of leaves: child=0 → must place camera → return 2
  Root: child=2 → covered → return 1

Cameras placed: 1 (at the parent of leaves)
```

### 10.4 State Transition Rules

```python
def get_state(left, right):
    # If any child is not covered, must place camera
    if left == 0 or right == 0:
        return 2  # Place camera, count += 1

    # If any child has camera, this node is covered
    if left == 2 or right == 2:
        return 1  # Covered, no camera needed

    # Both children covered but no camera nearby
    return 0  # Not covered, needs parent
```

### 10.5 Implementation

```python
def minCameraCover(root: TreeNode) -> int:
    cameras = 0

    def dfs(node):
        nonlocal cameras

        if not node:
            return 1  # Null is "covered" (don't need camera for it)

        left = dfs(node.left)
        right = dfs(node.right)

        # Rule 1: Child not covered → place camera here
        if left == 0 or right == 0:
            cameras += 1
            return 2

        # Rule 2: Child has camera → we're covered
        if left == 2 or right == 2:
            return 1

        # Rule 3: Children covered, no camera nearby
        return 0

    # Handle root specially
    if dfs(root) == 0:
        cameras += 1  # Root not covered, needs camera

    return cameras
```

### 10.6 Why This Greedy Works

The strategy is **leaf-driven**:
1. Don't place cameras on leaves (wasteful)
2. Place cameras on parents of leaves (covers 3 nodes)
3. Propagate coverage upward

This greedy approach is optimal because:
- Each camera covers at most 3 levels
- Placing at parents of leaves maximizes coverage

### 10.7 State Transition Diagram

```
Child States    →    Parent State
─────────────────────────────────
Any child = 0  →    2 (place camera)
Both covered,
one has camera →    1 (covered)
Both = 1       →    0 (not covered)
```

### 10.8 Complexity

- **Time**: O(n)
- **Space**: O(h)

### 10.9 Why Three States?

Two states (has camera / no camera) aren't enough:
- "No camera" doesn't distinguish "covered by child" vs "needs coverage"
- We need to know if a node NEEDS a camera from its parent

### 10.10 Key Differences from Other Tree DP

| Aspect | House Robber | Max Path | Cameras |
|--------|--------------|----------|---------|
| States | 2 | 1 + global | 3 |
| Goal | Maximize sum | Max path | Minimize count |
| Constraint | No adjacent | Path structure | Full coverage |

---

## 11. Pattern Comparison

| Problem | States Per Node | Return Value | Global Tracking |
|---------|-----------------|--------------|-----------------|
| **House Robber III** | 2 (include, exclude) | Both states | No |
| **Max Path Sum** | 1 (contribution) | Max branch contribution | Yes (max path) |
| **Binary Tree Cameras** | 3 (coverage states) | Coverage state | Yes (camera count) |

## 12. State Design Summary

| Pattern Type | When to Use | State Example |
|--------------|-------------|---------------|
| **Include/Exclude** | Binary choice per node | `(with_node, without_node)` |
| **Path Contribution** | Optimize paths | `max_contribution_upward` |
| **Multi-State** | Complex constraints | `(not_covered, covered, has_camera)` |

## 13. Complexity Comparison

| Problem | Time | Space | Key Operation |
|---------|------|-------|---------------|
| House Robber III | O(n) | O(h) | Max of combinations |
| Max Path Sum | O(n) | O(h) | Sum with clamping |
| Binary Tree Cameras | O(n) | O(h) | State transition |

## 14. Return Value vs Global State

| Problem | Return to Parent | Global Update |
|---------|------------------|---------------|
| House Robber | Both states for parent's choice | None |
| Max Path | Single branch (path constraint) | Max of all paths |
| Cameras | Coverage state | Camera count |

---

## 15. When to Use Tree DP

### 15.1 Pattern Recognition Signals

Use tree DP when you see:

1. **Binary tree structure** with optimization requirement
2. **Node-level decisions** that affect neighbors (parent/children)
3. **Constraint propagation** through tree edges
4. **Optimal substructure** where subtree solutions combine for parent

### 15.2 Decision Flowchart

```
Problem on a tree?
├── No → Not tree DP
└── Yes → What's the constraint?
    ├── Node selection (include/exclude) → Include/Exclude DP
    │   └── Examples: House Robber III, Max Independent Set
    ├── Path optimization → Path Contribution DP
    │   └── Examples: Max Path Sum, Diameter
    └── Coverage/coloring → Multi-State DP
        └── Examples: Binary Tree Cameras, Vertex Cover
```

### 15.3 State Design Questions

1. **What information does a parent need from children?**
   - Binary choice → 2 states
   - Path contribution → 1 value
   - Multiple scenarios → 3+ states

2. **Is the answer at the root or anywhere?**
   - At root → return from DFS
   - Anywhere → track global max/min

3. **Can negative values be ignored?**
   - Yes → clamp contributions to 0
   - No → handle negative cases

### 15.4 Tree DP vs Other Patterns

| Alternative | When to Prefer |
|-------------|----------------|
| **BFS/DFS** | Just traversal, no optimization |
| **Greedy** | Local optimal = global optimal |
| **1D DP** | Tree degenerates to path |
| **Memoization** | Same subtree appears multiple times (rare in trees) |

### 15.5 Common Pitfalls

1. **Forgetting base case**: Handle null nodes properly
2. **Wrong state count**: More constraints need more states
3. **Confusing return vs global**: Know what to return vs track globally
4. **Off-by-one in coverage**: Careful with parent/child relationships

---

## 16. Quick Reference Templates

### 16.1 Template 1: Include/Exclude DP (House Robber III)

```python
def tree_dp_include_exclude(root: TreeNode) -> int:
    """
    Returns maximum value with constraint:
    adjacent nodes can't both be selected.
    """
    def dfs(node):
        if not node:
            return (0, 0)  # (include, exclude)

        left = dfs(node.left)
        right = dfs(node.right)

        # Include: must exclude children
        include = node.val + left[1] + right[1]
        # Exclude: children are free choice
        exclude = max(left) + max(right)

        return (include, exclude)

    return max(dfs(root))
```

### 16.2 Template 2: Path Contribution DP (Max Path Sum)

```python
def tree_dp_path_sum(root: TreeNode) -> int:
    """
    Find maximum path sum where path can start/end at any node.
    """
    max_sum = float('-inf')

    def dfs(node):
        nonlocal max_sum

        if not node:
            return 0

        # Get max contribution from each branch (clamp negative to 0)
        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))

        # Path through this node
        path_through = node.val + left + right
        max_sum = max(max_sum, path_through)

        # Return single-branch contribution for parent
        return node.val + max(left, right)

    dfs(root)
    return max_sum
```

### 16.3 Template 3: Multi-State DP (Camera Coverage)

```python
def tree_dp_coverage(root: TreeNode) -> int:
    """
    Minimum cameras to cover all nodes.
    States: 0=not covered, 1=covered, 2=has camera
    """
    cameras = 0

    def dfs(node):
        nonlocal cameras

        if not node:
            return 1  # Null is "covered"

        left = dfs(node.left)
        right = dfs(node.right)

        if left == 0 or right == 0:
            cameras += 1
            return 2  # Place camera

        if left == 2 or right == 2:
            return 1  # Covered by child

        return 0  # Not covered

    if dfs(root) == 0:
        cameras += 1  # Root needs camera

    return cameras
```

### 16.4 Template 4: Generic Tree DP Framework

```python
def tree_dp_generic(root: TreeNode) -> ResultType:
    """
    Generic framework for tree DP.
    """
    # Global state if answer can be at any node
    global_result = initial_value

    def dfs(node) -> StateType:
        nonlocal global_result

        if not node:
            return base_state

        # Post-order: process children first
        left_state = dfs(node.left)
        right_state = dfs(node.right)

        # Compute current node's state
        current_state = transition(left_state, right_state, node.val)

        # Update global result if needed
        global_result = update_global(global_result, current_state)

        return current_state

    root_state = dfs(root)
    return extract_answer(root_state, global_result)
```

### 16.5 Template 5: Tree Diameter (Bonus)

```python
def tree_diameter(root: TreeNode) -> int:
    """
    Find longest path between any two nodes.
    """
    diameter = 0

    def dfs(node):
        nonlocal diameter

        if not node:
            return 0

        left = dfs(node.left)
        right = dfs(node.right)

        # Diameter through this node
        diameter = max(diameter, left + right)

        # Return height (depth of deepest subtree)
        return 1 + max(left, right)

    dfs(root)
    return diameter
```

## 17. State Design Cheat Sheet

| Constraint | States | Return |
|------------|--------|--------|
| Include/exclude | (with, without) | Both |
| Path sum | contribution | Single + global |
| Coverage | (not_covered, covered, has_camera) | State + count |
| Height/depth | integer | Single value |
| Subtree property | (satisfies, info) | Tuple |



---



*Document generated for NeetCode Practice Framework — API Kernel: tree_dp*

## Problem: Binary Tree Cameras (LC 968)

> **Advanced Variant**: Multi-state tree DP.

### Problem Statement

You are given the root of a binary tree. Install cameras on tree nodes such that every node is monitored. A camera can monitor its parent, itself, and immediate children. Return the minimum number of cameras needed.

### Pattern: State Machine DP

**Invariant**: Each node is in one of three states:
- **State 0**: Not covered (needs parent's camera)
- **State 1**: Covered but no camera here
- **State 2**: Has camera (covers parent and children)

**Delta from Base**: Three states with coverage rules.

### Algorithm

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

### State Transition Rules

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

### Implementation

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

### Why This Greedy Works

The strategy is **leaf-driven**:
1. Don't place cameras on leaves (wasteful)
2. Place cameras on parents of leaves (covers 3 nodes)
3. Propagate coverage upward

This greedy approach is optimal because:
- Each camera covers at most 3 levels
- Placing at parents of leaves maximizes coverage

### State Transition Diagram

```
Child States    →    Parent State
─────────────────────────────────
Any child = 0  →    2 (place camera)
Both covered,
one has camera →    1 (covered)
Both = 1       →    0 (not covered)
```

### Complexity

- **Time**: O(n)
- **Space**: O(h)

### Why Three States?

Two states (has camera / no camera) aren't enough:
- "No camera" doesn't distinguish "covered by child" vs "needs coverage"
- We need to know if a node NEEDS a camera from its parent

### Key Differences from Other Tree DP

| Aspect | House Robber | Max Path | Cameras |
|--------|--------------|----------|---------|
| States | 2 | 1 + global | 3 |
| Goal | Maximize sum | Max path | Minimize count |
| Constraint | No adjacent | Path structure | Full coverage |

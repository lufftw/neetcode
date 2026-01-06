# Tree DP Pattern

## API Kernel: `TreeDP`

> **Core Mechanism**: Apply dynamic programming on tree structures by computing states bottom-up (post-order) where each node's state depends on its children's states.

## Why Tree DP?

Tree DP solves optimization problems on trees where:
- You need to make decisions at each node (include/exclude, color, etc.)
- The optimal solution depends on subtree solutions
- Simple greedy doesn't work due to dependent choices

## Core Insight

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

## Universal Template Structure

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

## State Design Strategies

| Pattern | State Type | Example |
|---------|------------|---------|
| **Include/Exclude** | (with_node, without_node) | House Robber III |
| **Path Through Node** | max_path_ending_here | Max Path Sum |
| **Coverage States** | (covered, has_camera, not_covered) | Binary Tree Cameras |
| **Subtree Info** | (height, is_balanced) | Balanced Tree Check |

## State Transition Patterns

### Pattern 1: Include/Exclude (House Robber)
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

### Pattern 2: Path Contribution (Max Path Sum)
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

### Pattern 3: Multi-State (Camera Coverage)
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

## Pattern Variants

1. **Binary Choice**: Include/exclude node in solution
2. **Path Optimization**: Find optimal path through nodes
3. **State Machine**: Multiple states per node with transitions
4. **Aggregation**: Collect information from entire subtree

## Quick Reference Templates

### Template 1: Include/Exclude DP (House Robber III)

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

### Template 2: Path Contribution DP (Max Path Sum)

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

### Template 3: Multi-State DP (Camera Coverage)

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

### Template 4: Generic Tree DP Framework

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

### Template 5: Tree Diameter (Bonus)

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

## State Design Cheat Sheet

| Constraint | States | Return |
|------------|--------|--------|
| Include/exclude | (with, without) | Both |
| Path sum | contribution | Single + global |
| Coverage | (not_covered, covered, has_camera) | State + count |
| Height/depth | integer | Single value |
| Subtree property | (satisfies, info) | Tuple |

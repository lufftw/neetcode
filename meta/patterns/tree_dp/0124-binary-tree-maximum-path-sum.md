## Problem: Binary Tree Maximum Path Sum (LC 124)

> **Variant**: Path optimization tree DP.

### Problem Statement

A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge. The path sum is the sum of node values. Find the maximum path sum.

### Pattern: Path Contribution DP

**Invariant**: For each node, track the maximum contribution it can make to a path extending upward.

**Key Insight**: A path can:
1. Go through a node (left → node → right)
2. Extend from a node upward (can only use one branch)

**Delta from Base**: Track global maximum separately from returned value.

### Algorithm

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

### Implementation

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

### Why Return Only One Branch?

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

### Key Differences from House Robber

| Aspect | House Robber | Max Path Sum |
|--------|--------------|--------------|
| State | (include, exclude) | single value |
| Return | both states | max contribution upward |
| Answer | max of root states | global max (any node) |
| Negative | keep if positive | clamp to 0 |

### Complexity

- **Time**: O(n)
- **Space**: O(h)

### Edge Cases

1. **Single node**: Answer is node.val
2. **All negative**: Must include at least one node
3. **Negative children**: Clamp contribution to 0 (don't use negative branches)

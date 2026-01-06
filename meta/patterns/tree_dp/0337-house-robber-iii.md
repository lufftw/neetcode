## Problem: House Robber III (LC 337)

> **Base Template** for include/exclude tree DP.

### Problem Statement

The thief has found a new place for thievery. Houses form a binary tree. If two directly-linked houses are broken into, they will alert the police. Maximize the total amount robbed.

### Pattern: Include/Exclude DP

**Invariant**: For each node, track two states:
- Maximum if we **include** this node
- Maximum if we **exclude** this node

**Key Insight**: If we include parent, we can't include children. If we exclude parent, children are independent.

### Algorithm

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

### Implementation

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

### State Transition Diagram

```
        Parent
       /      \
    Child    Child

Include parent → must exclude both children
Exclude parent → each child can be included or excluded (independent)
```

### Complexity

- **Time**: O(n) - visit each node once
- **Space**: O(h) - recursion stack depth (h = tree height)

### Why Two States Work

The key constraint is "adjacent nodes can't both be selected." With two states per node, we capture all legal combinations:
- Parent included → children must be excluded
- Parent excluded → children independently optimal

## Diameter of Binary Tree (LeetCode 543)

> **Problem**: Find the longest path between any two nodes.
> **Invariant**: Diameter through node = left_height + right_height.
> **Role**: VARIANT combining heights for path problems.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "diameter" | → Max(left_height + right_height) over all nodes |
| "longest path" | → Track max during height computation |
| "between any two nodes" | → Path can go through any node |

### Implementation

```python
# Pattern: tree_path_computation
# See: docs/patterns/tree/templates.md Section 5

class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        Longest path between any two nodes (in edges).

        Key Insight:
        - For each node, longest path through it = left_height + right_height
        - Track maximum during height computation
        - Return height for recursion, track diameter separately
        """
        self.diameter = 0

        def height(node: Optional[TreeNode]) -> int:
            if not node:
                return 0

            left_h = height(node.left)
            right_h = height(node.right)

            # Update diameter (path through this node)
            self.diameter = max(self.diameter, left_h + right_h)

            # Return height for parent's computation
            return 1 + max(left_h, right_h)

        height(root)
        return self.diameter
```

### Alternative (No Instance Variable)

```python
def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
    """Using nonlocal or list to track max."""
    result = [0]

    def height(node):
        if not node:
            return 0
        left = height(node.left)
        right = height(node.right)
        result[0] = max(result[0], left + right)
        return 1 + max(left, right)

    height(root)
    return result[0]
```

### Trace Example

```
Tree:       1
           / \
          2   3
         / \
        4   5

height(1):
  height(2):
    height(4) = 1, diameter = max(0, 0+0) = 0
    height(5) = 1, diameter = max(0, 0+0) = 0
    diameter = max(0, 1+1) = 2
    return 2
  height(3) = 1, diameter = max(2, 0+0) = 2
  diameter = max(2, 2+1) = 3
  return 3

Result: 3 (path: 4→2→1→3 or 5→2→1→3)
```

### Visual Representation

```
        1
       / \
      2   3
     / \
    4   5

Longest path: 4 → 2 → 1 → 3 (or 5 → 2 → 1 → 3)
Length: 3 edges

At node 2: left_h=1, right_h=1, diameter=2 (4→2→5)
At node 1: left_h=2, right_h=1, diameter=3 (4→2→1→3)
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - visit each node once |
| Space | O(h) - recursion stack depth |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 124: Max Path Sum | Add node values to path |
| LC 687: Longest Univalue Path | Path with same values |
| LC 1522: Diameter of N-Ary Tree | N children |



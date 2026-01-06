## Maximum Depth of Binary Tree (LeetCode 104)

> **Problem**: Find the maximum depth (height) of a binary tree.
> **Invariant**: Depth = 1 + max(left_depth, right_depth).
> **Role**: BASE TEMPLATE for tree property computation.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "depth" or "height" | → Recursive max of children + 1 |
| "longest path to leaf" | → DFS postorder style |
| "tree property" | → Bottom-up computation |

### Implementation

```python
# Pattern: tree_property_computation
# See: docs/patterns/tree/templates.md Section 3

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Maximum depth of binary tree.

        Key Insight:
        - Empty tree has depth 0
        - Leaf has depth 1
        - Internal node: 1 + max(left, right)
        """
        if not root:
            return 0

        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

### Iterative BFS Version

```python
def maxDepth(self, root: Optional[TreeNode]) -> int:
    """Maximum depth using BFS level counting."""
    if not root:
        return 0

    depth = 0
    queue = deque([root])

    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return depth
```

### Trace Example

```
Tree:       3
           / \
          9  20
            /  \
           15   7

Recursive calls:
maxDepth(3) = 1 + max(maxDepth(9), maxDepth(20))
maxDepth(9) = 1 + max(0, 0) = 1
maxDepth(20) = 1 + max(maxDepth(15), maxDepth(7))
maxDepth(15) = 1 + max(0, 0) = 1
maxDepth(7) = 1 + max(0, 0) = 1
maxDepth(20) = 1 + max(1, 1) = 2
maxDepth(3) = 1 + max(1, 2) = 3

Result: 3
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - visit each node once |
| Space | O(h) - recursion stack depth |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 111: Minimum Depth | Stop at first leaf |
| LC 110: Balanced Binary Tree | Compare left/right depths |
| LC 543: Diameter | Max left + right depths |



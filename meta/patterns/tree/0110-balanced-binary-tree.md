## Balanced Binary Tree (LeetCode 110)

> **Problem**: Check if tree is height-balanced.
> **Invariant**: |height(left) - height(right)| <= 1 for all nodes.
> **Role**: VARIANT with early termination.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "balanced" | → Check height difference at each node |
| "height-balanced" | → |left - right| <= 1 |
| "validate property" | → DFS with early termination |

### Implementation

```python
# Pattern: tree_property_validation
# See: docs/patterns/tree/templates.md Section 4

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        """
        Check if tree is height-balanced.

        Key Insight:
        - Compute height bottom-up
        - Return -1 to signal imbalance (early termination)
        - Avoid recomputing heights
        """
        def check(node: Optional[TreeNode]) -> int:
            """Return height if balanced, -1 if not."""
            if not node:
                return 0

            left = check(node.left)
            if left == -1:
                return -1  # Early termination

            right = check(node.right)
            if right == -1:
                return -1

            if abs(left - right) > 1:
                return -1

            return 1 + max(left, right)

        return check(root) != -1
```

### Naive O(n²) Version (for comparison)

```python
def isBalanced(self, root: Optional[TreeNode]) -> bool:
    """Naive: recomputes height at each level."""
    if not root:
        return True

    def height(node):
        if not node: return 0
        return 1 + max(height(node.left), height(node.right))

    # Check this node and recurse
    return (abs(height(root.left) - height(root.right)) <= 1 and
            self.isBalanced(root.left) and
            self.isBalanced(root.right))
```

### Trace Example

```
Balanced:       3
               / \
              9  20
                /  \
               15   7

check(3):
  check(9) = 1
  check(20):
    check(15) = 1
    check(7) = 1
    |1-1| = 0 <= 1, return 2
  |1-2| = 1 <= 1, return 3 ≠ -1

Result: True

Unbalanced:     1
               / \
              2   2
             / \
            3   3
           / \
          4   4

check(1):
  check(2, left):
    check(3):
      check(4) = 1
      check(4) = 1
      return 2
    check(3) = 1
    return 3
  check(2, right) = 1
  |3-1| = 2 > 1, return -1

Result: False
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - each node visited once |
| Space | O(h) - recursion stack depth |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 104: Maximum Depth | Base height computation |
| LC 543: Diameter | Use heights for path length |
| LC 222: Count Complete Tree Nodes | Special balanced check |



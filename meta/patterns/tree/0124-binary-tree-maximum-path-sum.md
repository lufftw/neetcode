## Binary Tree Maximum Path Sum (LeetCode 124)

> **Problem**: Find the maximum path sum where path visits each node at most once.
> **Invariant**: Max through node = node.val + max(0, left) + max(0, right).
> **Role**: HARD VARIANT of diameter pattern with values.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "maximum path sum" | → Track max during traversal |
| "path can start/end anywhere" | → Consider all nodes as path apex |
| "can include negatives" | → Use max(0, child) to skip negative paths |

### Implementation

```python
# Pattern: tree_path_sum
# See: docs/patterns/tree/templates.md Section 6

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        """
        Maximum path sum in binary tree.

        Key Insight:
        - At each node, consider it as path apex
        - Path sum through node = node.val + left_gain + right_gain
        - Gain from subtree = max(0, subtree_max) (can skip negative)
        - Return single branch max (can only go one direction to parent)
        """
        self.max_sum = float('-inf')

        def max_gain(node: Optional[TreeNode]) -> int:
            if not node:
                return 0

            # Max gain from left/right (ignore negative paths)
            left_gain = max(0, max_gain(node.left))
            right_gain = max(0, max_gain(node.right))

            # Path sum if this node is apex
            path_sum = node.val + left_gain + right_gain
            self.max_sum = max(self.max_sum, path_sum)

            # Return max single-branch gain for parent
            return node.val + max(left_gain, right_gain)

        max_gain(root)
        return self.max_sum
```

### Trace Example

```
Tree:       -10
           /   \
          9    20
              /  \
             15   7

max_gain(-10):
  max_gain(9) = max(0, 9 + max(0,0) + max(0,0)) → path=9, return 9
  max_gain(20):
    max_gain(15) = max(0, 15+0+0) → path=15, return 15
    max_gain(7) = max(0, 7+0+0) → path=7, return 7
    path = 20 + 15 + 7 = 42, max_sum = 42
    return 20 + max(15, 7) = 35
  path = -10 + 9 + 35 = 34 < 42, max_sum stays 42
  return -10 + max(9, 35) = 25

Result: 42 (path: 15→20→7)
```

### Why max(0, child)?

```python
# Consider tree with negative branch:
#       1
#      /
#    -5
#
# Without max(0, ...):
# path through 1 would be 1 + (-5) = -4
#
# With max(0, ...):
# left_gain = max(0, -5) = 0
# path through 1 = 1 + 0 = 1
# We "skip" the negative subtree
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - visit each node once |
| Space | O(h) - recursion stack depth |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 543: Diameter | Count edges, not sum values |
| LC 112: Path Sum | Root to leaf path |
| LC 437: Path Sum III | Any start/end, count paths |



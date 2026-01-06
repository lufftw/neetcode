## Binary Tree Level Order Traversal (LeetCode 102)

> **Problem**: Return level-order traversal as list of lists.
> **Invariant**: Process all nodes at depth d before depth d+1.
> **Role**: BASE TEMPLATE for BFS traversal.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "level order" | → BFS with queue |
| "by depth" | → Track level boundaries |
| "breadth-first" | → Queue-based traversal |

### Implementation

```python
# Pattern: tree_bfs_level_order
# See: docs/patterns/tree/templates.md Section 2

from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Level-order traversal using BFS.

        Key Insight:
        - Use queue for BFS
        - Process entire level at once using len(queue)
        - Add children to queue for next level
        """
        if not root:
            return []

        result: list[list[int]] = []
        queue: deque[TreeNode] = deque([root])

        while queue:
            level: list[int] = []
            level_size = len(queue)

            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level)

        return result
```

### Trace Example

```
Tree:       3
           / \
          9  20
            /  \
           15   7

Level 0: queue = [3]
  Process 3, add 9, 20
  level = [3]

Level 1: queue = [9, 20]
  Process 9 (no children)
  Process 20, add 15, 7
  level = [9, 20]

Level 2: queue = [15, 7]
  Process 15, 7 (no children)
  level = [15, 7]

Result: [[3], [9, 20], [15, 7]]
```

### DFS Alternative

```python
def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
    """Level-order using DFS with depth tracking."""
    result: list[list[int]] = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return
        if depth == len(result):
            result.append([])
        result[depth].append(node.val)
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return result
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - visit each node once |
| Space | O(w) - max width of tree (queue size) |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 103: Zigzag Level Order | Alternate left-right |
| LC 107: Level Order Bottom | Bottom to top |
| LC 199: Right Side View | Rightmost at each level |



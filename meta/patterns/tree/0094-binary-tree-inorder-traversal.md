## Binary Tree Inorder Traversal (LeetCode 94)

> **Problem**: Return inorder traversal of a binary tree.
> **Invariant**: Visit left subtree, node, right subtree.
> **Role**: BASE TEMPLATE for DFS traversal.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "inorder traversal" | → Left, Node, Right |
| "BST sorted order" | → Inorder gives sorted sequence |
| "visit all nodes" | → DFS traversal |

### Implementation

```python
# Pattern: tree_dfs_inorder
# See: docs/patterns/tree/templates.md Section 1

class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """
        Inorder traversal: Left → Node → Right.

        Key Insight:
        - Recursive: natural left-first, then visit, then right
        - Iterative: use stack, go left as far as possible
        """
        result: list[int] = []

        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            dfs(node.left)
            result.append(node.val)
            dfs(node.right)

        dfs(root)
        return result
```

### Iterative Version

```python
def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
    """Iterative inorder using explicit stack."""
    result: list[int] = []
    stack: list[TreeNode] = []
    curr = root

    while curr or stack:
        # Go left as far as possible
        while curr:
            stack.append(curr)
            curr = curr.left

        # Process node
        curr = stack.pop()
        result.append(curr.val)

        # Move to right subtree
        curr = curr.right

    return result
```

### Trace Example

```
Tree:       1
             \
              2
             /
            3

Recursive:
1. dfs(1): dfs(None), visit(1), dfs(2)
2. dfs(2): dfs(3), visit(2), dfs(None)
3. dfs(3): dfs(None), visit(3), dfs(None)

Order: 3 (left of 2), 2 (middle), 1 → wait, let me fix:

Actually: inorder visits nodes in order: left subtree, node, right subtree
1. At node 1: left is None, visit 1, go right to 2
2. At node 2: left is 3, so first visit 3
3. At node 3: left is None, visit 3, right is None
4. Back to 2: visit 2, right is None

Result: [1, 3, 2]
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - visit each node once |
| Space | O(h) - recursion stack depth (h = height) |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 144: Preorder Traversal | Node → Left → Right |
| LC 145: Postorder Traversal | Left → Right → Node |
| LC 173: BST Iterator | Inorder with lazy evaluation |



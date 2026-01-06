---

## Code Templates Summary

### Template 1: DFS Traversal (Inorder)

```python
def inorderTraversal(root: TreeNode) -> List[int]:
    result = []
    def dfs(node):
        if not node: return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)
    dfs(root)
    return result
```

### Template 2: BFS Level Order

```python
def levelOrder(root: TreeNode) -> List[List[int]]:
    if not root: return []
    result = []
    queue = deque([root])

    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)

    return result
```

### Template 3: Simple Property (Height)

```python
def maxDepth(root: TreeNode) -> int:
    if not root: return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

### Template 4: Validation with Early Termination

```python
def isBalanced(root: TreeNode) -> bool:
    def check(node):
        if not node: return 0
        left = check(node.left)
        if left == -1: return -1
        right = check(node.right)
        if right == -1: return -1
        if abs(left - right) > 1: return -1
        return 1 + max(left, right)
    return check(root) != -1
```

### Template 5: Path Problem (Diameter)

```python
def diameterOfBinaryTree(root: TreeNode) -> int:
    result = [0]
    def height(node):
        if not node: return 0
        left = height(node.left)
        right = height(node.right)
        result[0] = max(result[0], left + right)
        return 1 + max(left, right)
    height(root)
    return result[0]
```

### Template 6: Max Path Sum

```python
def maxPathSum(root: TreeNode) -> int:
    result = [float('-inf')]
    def dfs(node):
        if not node: return 0
        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))
        result[0] = max(result[0], left + node.val + right)
        return node.val + max(left, right)
    dfs(root)
    return result[0]
```

### Pattern Selection Cheat Sheet

| Problem Signal | Template | Key Technique |
|---------------|----------|---------------|
| "traversal order" | Template 1 | Change order of visit |
| "by level" | Template 2 | BFS with queue |
| "height/depth" | Template 3 | Recursive property |
| "balanced/valid" | Template 4 | Early termination |
| "diameter/longest path" | Template 5 | Track global max |
| "maximum path sum" | Template 6 | max(0, child) to skip |



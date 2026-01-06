# Tree Traversal Patterns: Complete Reference

> **API Kernels**: `TreeTraversalDFS`, `TreeTraversalBFS`
> **Core Mechanism**: Process tree nodes in specific orders using recursion (DFS) or queue (BFS).

This document presents the **canonical tree traversal templates** covering DFS (preorder, inorder, postorder), BFS (level-order), and tree property computation patterns. Each implementation includes both recursive and iterative approaches.

---

## Core Concepts

### Tree Node Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### DFS Traversal Orders

```python
# Preorder: Node → Left → Right (top-down)
def preorder(root):
    if not root: return
    visit(root)
    preorder(root.left)
    preorder(root.right)

# Inorder: Left → Node → Right (BST sorted order)
def inorder(root):
    if not root: return
    inorder(root.left)
    visit(root)
    inorder(root.right)

# Postorder: Left → Right → Node (bottom-up)
def postorder(root):
    if not root: return
    postorder(root.left)
    postorder(root.right)
    visit(root)
```

### BFS Level-Order Traversal

```python
from collections import deque

def level_order(root):
    if not root: return []
    result = []
    queue = deque([root])

    while queue:
        level = []
        for _ in range(len(queue)):  # Process entire level
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)

    return result
```

### Traversal Order Selection

| Order | Use When | Example Problems |
|-------|----------|------------------|
| **Preorder** | Process node before children (top-down) | Clone tree, serialize |
| **Inorder** | BST operations, sorted output | Validate BST, kth smallest |
| **Postorder** | Need children's results first (bottom-up) | Height, diameter, delete tree |
| **Level-order** | Process by depth, shortest path in tree | Level sums, zigzag |

### Pattern Variants

| Variant | API Kernel | Use When |
|---------|------------|----------|
| **Basic DFS** | `TreeTraversalDFS` | Simple traversal, collect values |
| **Property Computation** | `TreeTraversalDFS` | Height, depth, balance check |
| **Path Problems** | `TreeTraversalDFS` | Max path sum, diameter |
| **Level-Order** | `TreeTraversalBFS` | Process by depth levels |

### Common Recursive Patterns

```python
# Pattern 1: Return single value (e.g., height)
def height(root):
    if not root: return 0
    return 1 + max(height(root.left), height(root.right))

# Pattern 2: Return with early termination (e.g., is balanced)
def is_balanced(root):
    def check(node):
        if not node: return 0
        left = check(node.left)
        if left == -1: return -1  # Early termination
        right = check(node.right)
        if right == -1: return -1
        if abs(left - right) > 1: return -1
        return 1 + max(left, right)
    return check(root) != -1

# Pattern 3: Track path through recursion (e.g., max path sum)
def max_path(root):
    result = [float('-inf')]
    def dfs(node):
        if not node: return 0
        left = max(0, dfs(node.left))   # Can choose to not take path
        right = max(0, dfs(node.right))
        result[0] = max(result[0], left + node.val + right)  # Path through node
        return node.val + max(left, right)  # Return single branch
    dfs(root)
    return result[0]
```



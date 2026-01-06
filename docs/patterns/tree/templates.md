# Tree Traversal Patterns: Complete Reference

> **API Kernels**: `TreeTraversalDFS`, `TreeTraversalBFS`
> **Core Mechanism**: Process tree nodes in specific orders using recursion (DFS) or queue (BFS).

This document presents the **canonical tree traversal templates** covering DFS (preorder, inorder, postorder), BFS (level-order), and tree property computation patterns. Each implementation includes both recursive and iterative approaches.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Binary Tree Inorder Traversal (LeetCode 94)](#2-binary-tree-inorder-traversal-leetcode-94)
3. [Binary Tree Level Order Traversal (LeetCode 102)](#3-binary-tree-level-order-traversal-leetcode-102)
4. [Maximum Depth of Binary Tree (LeetCode 104)](#4-maximum-depth-of-binary-tree-leetcode-104)
5. [Balanced Binary Tree (LeetCode 110)](#5-balanced-binary-tree-leetcode-110)
6. [Diameter of Binary Tree (LeetCode 543)](#6-diameter-of-binary-tree-leetcode-543)
7. [Binary Tree Maximum Path Sum (LeetCode 124)](#7-binary-tree-maximum-path-sum-leetcode-124)
8. [Pattern Comparison](#8-pattern-comparison)
9. [Decision Framework](#9-decision-framework)
10. [Code Templates Summary](#10-code-templates-summary)

---

## 1. Core Concepts

### 1.1 Tree Node Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### 1.2 DFS Traversal Orders

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

### 1.3 BFS Level-Order Traversal

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

### 1.4 Traversal Order Selection

| Order | Use When | Example Problems |
|-------|----------|------------------|
| **Preorder** | Process node before children (top-down) | Clone tree, serialize |
| **Inorder** | BST operations, sorted output | Validate BST, kth smallest |
| **Postorder** | Need children's results first (bottom-up) | Height, diameter, delete tree |
| **Level-order** | Process by depth, shortest path in tree | Level sums, zigzag |

### 1.5 Pattern Variants

| Variant | API Kernel | Use When |
|---------|------------|----------|
| **Basic DFS** | `TreeTraversalDFS` | Simple traversal, collect values |
| **Property Computation** | `TreeTraversalDFS` | Height, depth, balance check |
| **Path Problems** | `TreeTraversalDFS` | Max path sum, diameter |
| **Level-Order** | `TreeTraversalBFS` | Process by depth levels |

### 1.6 Common Recursive Patterns

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

---

## 2. Binary Tree Inorder Traversal (LeetCode 94)

> **Problem**: Return inorder traversal of a binary tree.
> **Invariant**: Visit left subtree, node, right subtree.
> **Role**: BASE TEMPLATE for DFS traversal.

### 2.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "inorder traversal" | → Left, Node, Right |
| "BST sorted order" | → Inorder gives sorted sequence |
| "visit all nodes" | → DFS traversal |

### 2.2 Implementation

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

### 2.3 Iterative Version

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

### 2.4 Trace Example

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

### 2.5 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - visit each node once |
| Space | O(h) - recursion stack depth (h = height) |

### 2.6 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 144: Preorder Traversal | Node → Left → Right |
| LC 145: Postorder Traversal | Left → Right → Node |
| LC 173: BST Iterator | Inorder with lazy evaluation |

---

## 3. Binary Tree Level Order Traversal (LeetCode 102)

> **Problem**: Return level-order traversal as list of lists.
> **Invariant**: Process all nodes at depth d before depth d+1.
> **Role**: BASE TEMPLATE for BFS traversal.

### 3.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "level order" | → BFS with queue |
| "by depth" | → Track level boundaries |
| "breadth-first" | → Queue-based traversal |

### 3.2 Implementation

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

### 3.3 Trace Example

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

### 3.4 DFS Alternative

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

### 3.5 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - visit each node once |
| Space | O(w) - max width of tree (queue size) |

### 3.6 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 103: Zigzag Level Order | Alternate left-right |
| LC 107: Level Order Bottom | Bottom to top |
| LC 199: Right Side View | Rightmost at each level |

---

## 4. Maximum Depth of Binary Tree (LeetCode 104)

> **Problem**: Find the maximum depth (height) of a binary tree.
> **Invariant**: Depth = 1 + max(left_depth, right_depth).
> **Role**: BASE TEMPLATE for tree property computation.

### 4.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "depth" or "height" | → Recursive max of children + 1 |
| "longest path to leaf" | → DFS postorder style |
| "tree property" | → Bottom-up computation |

### 4.2 Implementation

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

### 4.3 Iterative BFS Version

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

### 4.4 Trace Example

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

### 4.5 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - visit each node once |
| Space | O(h) - recursion stack depth |

### 4.6 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 111: Minimum Depth | Stop at first leaf |
| LC 110: Balanced Binary Tree | Compare left/right depths |
| LC 543: Diameter | Max left + right depths |

---

## 5. Balanced Binary Tree (LeetCode 110)

> **Problem**: Check if tree is height-balanced.
> **Invariant**: |height(left) - height(right)| <= 1 for all nodes.
> **Role**: VARIANT with early termination.

### 5.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "balanced" | → Check height difference at each node |
| "height-balanced" | → |left - right| <= 1 |
| "validate property" | → DFS with early termination |

### 5.2 Implementation

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

### 5.3 Naive O(n²) Version (for comparison)

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

### 5.4 Trace Example

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

### 5.5 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - each node visited once |
| Space | O(h) - recursion stack depth |

### 5.6 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 104: Maximum Depth | Base height computation |
| LC 543: Diameter | Use heights for path length |
| LC 222: Count Complete Tree Nodes | Special balanced check |

---

## 6. Diameter of Binary Tree (LeetCode 543)

> **Problem**: Find the longest path between any two nodes.
> **Invariant**: Diameter through node = left_height + right_height.
> **Role**: VARIANT combining heights for path problems.

### 6.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "diameter" | → Max(left_height + right_height) over all nodes |
| "longest path" | → Track max during height computation |
| "between any two nodes" | → Path can go through any node |

### 6.2 Implementation

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

### 6.3 Alternative (No Instance Variable)

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

### 6.4 Trace Example

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

### 6.5 Visual Representation

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

### 6.6 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - visit each node once |
| Space | O(h) - recursion stack depth |

### 6.7 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 124: Max Path Sum | Add node values to path |
| LC 687: Longest Univalue Path | Path with same values |
| LC 1522: Diameter of N-Ary Tree | N children |

---

## 7. Binary Tree Maximum Path Sum (LeetCode 124)

> **Problem**: Find the maximum path sum where path visits each node at most once.
> **Invariant**: Max through node = node.val + max(0, left) + max(0, right).
> **Role**: HARD VARIANT of diameter pattern with values.

### 7.1 Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "maximum path sum" | → Track max during traversal |
| "path can start/end anywhere" | → Consider all nodes as path apex |
| "can include negatives" | → Use max(0, child) to skip negative paths |

### 7.2 Implementation

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

### 7.3 Trace Example

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

### 7.4 Why max(0, child)?

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

### 7.5 Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n) - visit each node once |
| Space | O(h) - recursion stack depth |

### 7.6 Related Problems

| Problem | Variation |
|---------|-----------|
| LC 543: Diameter | Count edges, not sum values |
| LC 112: Path Sum | Root to leaf path |
| LC 437: Path Sum III | Any start/end, count paths |

---

---

## 8. Pattern Comparison

### 8.1 DFS vs BFS for Trees

| Aspect | DFS | BFS |
|--------|-----|-----|
| Space | O(h) - height | O(w) - width |
| Use when | Path-based, properties | Level-based |
| Order | Preorder/Inorder/Postorder | Level-order |
| Implementation | Recursion or stack | Queue |

### 8.2 DFS Order Selection

| Order | When to Use | Code Pattern |
|-------|-------------|--------------|
| **Preorder** | Process parent first | visit → left → right |
| **Inorder** | BST sorted order | left → visit → right |
| **Postorder** | Need children's results | left → right → visit |

### 8.3 Common Tree Patterns

```python
# PATTERN 1: Simple property (height, count)
def property(node):
    if not node: return BASE_VALUE
    left = property(node.left)
    right = property(node.right)
    return COMBINE(node.val, left, right)

# PATTERN 2: Validation with early termination
def validate(node):
    if not node: return VALID_BASE
    left = validate(node.left)
    if not left: return INVALID  # Early termination
    right = validate(node.right)
    if not right: return INVALID
    return CHECK(node, left, right)

# PATTERN 3: Path tracking (diameter, max path sum)
def path_property(node):
    if not node: return BASE
    left = path_property(node.left)
    right = path_property(node.right)
    UPDATE_GLOBAL(node, left, right)  # Track max path
    return SINGLE_BRANCH(node, left, right)  # Return for parent
```

### 8.4 When to Use Each Pattern

| Problem Type | Pattern | Example |
|--------------|---------|---------|
| Count nodes | Simple property | Count, sum values |
| Height/depth | Simple property | Max depth, min depth |
| Validate structure | Early termination | Balanced, BST valid |
| Longest path | Path tracking | Diameter, max path sum |
| By level | BFS | Level order, zigzag |

---

---

## 9. Decision Framework

### 9.1 Quick Reference Decision Tree

```
START: Given tree problem
│
├─ Need to process by level/depth?
│   └─ YES → BFS with queue
│            (LC 102 pattern)
│
├─ Need BST sorted order?
│   └─ YES → Inorder traversal
│            (LC 94 pattern)
│
├─ Need to compute tree property?
│   ├─ Simple: height, count, sum?
│   │   └─ YES → Basic recursive property
│   │            (LC 104 pattern)
│   │
│   └─ Need early termination?
│       └─ YES → Return sentinel (-1, None)
│                (LC 110 pattern)
│
├─ Path problem (diameter, max sum)?
│   └─ YES → Track global max during DFS
│            Return single-branch for parent
│            (LC 543, 124 pattern)
│
└─ Need to process parent before children?
    └─ YES → Preorder traversal
```

### 9.2 Recursive Return Strategy

```
What should recursion return?

1. Single value (height, count)
   return 1 + max(left, right)

2. Boolean validation
   return left and right and CHECK

3. Sentinel for invalid
   if invalid: return -1
   return valid_value

4. Path contribution
   UPDATE_GLOBAL(left + right + node)
   return node + max(left, right)
```

### 9.3 Common Mistakes

| Mistake | Why Wrong | Correct Approach |
|---------|-----------|------------------|
| Forgetting base case | Infinite recursion | Check `if not node` first |
| Wrong order | Incorrect result | Match problem requirements |
| Recomputing values | O(n²) time | Compute bottom-up once |
| Not handling None | NullPointerException | Return base value for None |
| Path direction | Return wrong value | Single branch for parent |

### 9.4 Complexity Expectations

| Operation | Time | Space |
|-----------|------|-------|
| Any single traversal | O(n) | O(h) |
| BFS level order | O(n) | O(w) |
| Property computation | O(n) | O(h) |

---

---

## 10. Code Templates Summary

### 10.1 Template 1: DFS Traversal (Inorder)

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

### 10.2 Template 2: BFS Level Order

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

### 10.3 Template 3: Simple Property (Height)

```python
def maxDepth(root: TreeNode) -> int:
    if not root: return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

### 10.4 Template 4: Validation with Early Termination

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

### 10.5 Template 5: Path Problem (Diameter)

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

### 10.6 Template 6: Max Path Sum

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

### 10.7 Pattern Selection Cheat Sheet

| Problem Signal | Template | Key Technique |
|---------------|----------|---------------|
| "traversal order" | Template 1 | Change order of visit |
| "by level" | Template 2 | BFS with queue |
| "height/depth" | Template 3 | Recursive property |
| "balanced/valid" | Template 4 | Early termination |
| "diameter/longest path" | Template 5 | Track global max |
| "maximum path sum" | Template 6 | max(0, child) to skip |



---



*Document generated for NeetCode Practice Framework — API Kernel: tree*

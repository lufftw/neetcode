# Tree Traversal: Intuition Guide

## The Mental Model

A binary tree is a specialized graph where each node has at most two children (left and right). Unlike general graphs, trees have:

1. **No cycles** - You can never revisit a node by following edges
2. **Exactly one path** between any two nodes
3. **Natural hierarchy** - Parent/child relationships

The key insight: **Trees decompose recursively**. A tree is a root plus two smaller trees. This makes recursion the natural approach.

---

## Two Fundamental Traversal Strategies

### DFS (Depth-First Search)

Go as deep as possible before backtracking. Three flavors based on when you "process" the current node:

```
       1
      / \
     2   3
    / \
   4   5

Preorder  (Node → Left → Right): 1, 2, 4, 5, 3
Inorder   (Left → Node → Right): 4, 2, 5, 1, 3
Postorder (Left → Right → Node): 4, 5, 2, 3, 1
```

**When to use which order?**
- **Preorder**: Process node before children (e.g., copy/serialize tree)
- **Inorder**: BST gives sorted order; useful for BST operations
- **Postorder**: Process children before node (e.g., delete tree, compute subtree values)

### BFS (Breadth-First Search)

Process level by level, using a queue:

```
       1          Level 0: [1]
      / \
     2   3        Level 1: [2, 3]
    / \
   4   5          Level 2: [4, 5]
```

**When to use BFS?**
- Level-order output required
- Finding nodes at specific depth
- Zigzag or spiral traversal
- Right-side view / boundary traversal

---

## Pattern Recognition Signals

### Signal: "Traverse and collect values"

**Trigger phrases**: "inorder traversal", "preorder", "postorder", "level order"

**Mental model**: Just run the appropriate traversal, collecting values.

```python
# Inorder: Left → Node → Right
def inorder(node):
    if not node: return
    inorder(node.left)
    result.append(node.val)
    inorder(node.right)
```

### Signal: "Compute tree property from subtrees"

**Trigger phrases**: "height", "depth", "number of nodes", "sum of values"

**Mental model**: Postorder thinking. Compute for children, combine at node.

```
Computing height:
       1 (h=2)
      / \
(h=1) 2   3 (h=0)
     /
(h=0) 4

height(node) = 1 + max(height(left), height(right))
```

**Key insight**: Most tree properties follow this pattern:
```python
def compute(node):
    if not node: return BASE_CASE
    left_val = compute(node.left)
    right_val = compute(node.right)
    return COMBINE(node.val, left_val, right_val)
```

### Signal: "Path through node" or "max path"

**Trigger phrases**: "longest path", "maximum path sum", "diameter"

**Mental model**: At each node, consider paths that use this node as the "apex" (highest point). Track global max while returning single-branch contribution.

```
Maximum path sum through node:
       10          Best path through 10: 2 → 10 → 3 = 15
      /  \         Left gain: max(0, 2) = 2
     2    3        Right gain: max(0, 3) = 3
                   Return for parent: 10 + max(2, 3) = 13
```

**Key insight**: Return value ≠ answer. You return what a parent can use (one branch), but the answer might include both branches.

### Signal: "Check property holds for all nodes"

**Trigger phrases**: "is balanced", "is symmetric", "is valid BST"

**Mental model**: Early termination. Return False/sentinel as soon as property fails.

```python
# Balanced tree check
def check(node):
    if not node: return 0
    left = check(node.left)
    if left == -1: return -1      # Early terminate
    right = check(node.right)
    if right == -1: return -1     # Early terminate
    if abs(left - right) > 1:
        return -1                 # Failed here
    return 1 + max(left, right)
```

**Key insight**: Use sentinel values (-1) to propagate failure without extra state.

### Signal: "Process by level" or "zigzag"

**Trigger phrases**: "level order", "right side view", "zigzag", "average of levels"

**Mental model**: BFS with level-size batching.

```python
def level_order(root):
    queue = deque([root])
    while queue:
        level_size = len(queue)     # Snapshot current level size
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
```

---

## DFS vs BFS for Trees

| Use DFS when... | Use BFS when... |
|-----------------|-----------------|
| Computing recursive properties | Level-by-level processing needed |
| Path problems (root to leaf) | Finding nodes at specific depth |
| Backtracking on paths | Right-side view, boundary |
| Space: O(h) acceptable | Space: O(w) acceptable |
| Tree is balanced (h = log n) | Tree is deep/skewed (h = n) |

**Space comparison for trees**:
- DFS: O(h) where h = height. Best case O(log n), worst case O(n)
- BFS: O(w) where w = max width. Worst case O(n/2) = O(n) at bottom level

---

## The "Return vs Update" Pattern

Many tree problems require tracking two things:
1. **Return value**: What a parent node needs
2. **Global update**: The actual answer

```python
class Solution:
    def diameterOfBinaryTree(self, root):
        self.diameter = 0

        def height(node):
            if not node: return 0
            left = height(node.left)
            right = height(node.right)

            # Update global answer (path through this node)
            self.diameter = max(self.diameter, left + right)

            # Return value for parent (single branch)
            return 1 + max(left, right)

        height(root)
        return self.diameter
```

**Problems using this pattern**:
- Diameter of Binary Tree (LC 543)
- Binary Tree Maximum Path Sum (LC 124)
- Longest Univalue Path (LC 687)

---

## Common Pitfalls

### Pitfall 1: Confusing height vs depth

```
Height: Distance from node DOWN to farthest leaf
Depth:  Distance from root DOWN to node

       1 (depth=0, height=2)
      / \
     2   3 (depth=1, height=0)
    /
   4 (depth=2, height=0)
```

### Pitfall 2: Forgetting base cases

```python
# WRONG: Crashes on None
def height(node):
    return 1 + max(height(node.left), height(node.right))

# CORRECT: Handle None
def height(node):
    if not node: return 0  # or return -1 depending on definition
    return 1 + max(height(node.left), height(node.right))
```

### Pitfall 3: Not handling negative values in path sum

```python
# WRONG: Always include subtree
def max_gain(node):
    left = max_gain(node.left)
    right = max_gain(node.right)
    return node.val + left + right  # Might decrease sum!

# CORRECT: Can skip negative subtrees
def max_gain(node):
    left = max(0, max_gain(node.left))   # Skip if negative
    right = max(0, max_gain(node.right)) # Skip if negative
    return node.val + max(left, right)
```

### Pitfall 4: Stack overflow on deep trees

```python
# WRONG for deep trees (Python recursion limit ~1000)
def traverse(node):
    if node.left: traverse(node.left)
    if node.right: traverse(node.right)

# CORRECT: Iterative with explicit stack
def traverse_iterative(root):
    stack = [root]
    while stack:
        node = stack.pop()
        if node.right: stack.append(node.right)
        if node.left: stack.append(node.left)
```

---

## Practice Progression

### Level 1: Basic Traversals (Master First!)
1. **LC 94 - Binary Tree Inorder Traversal**: Core DFS pattern
2. **LC 102 - Binary Tree Level Order Traversal**: Core BFS pattern
3. **LC 104 - Maximum Depth of Binary Tree**: Basic recursion

### Level 2: Property Computation
4. **LC 110 - Balanced Binary Tree**: Early termination pattern
5. **LC 100 - Same Tree**: Parallel recursion
6. **LC 101 - Symmetric Tree**: Mirror comparison

### Level 3: Path Problems
7. **LC 543 - Diameter of Binary Tree**: Return vs update pattern
8. **LC 124 - Binary Tree Maximum Path Sum**: Complex path tracking
9. **LC 112 - Path Sum**: Root-to-leaf paths

### Level 4: Advanced Applications
10. **LC 236 - LCA of Binary Tree**: Ancestor finding
11. **LC 297 - Serialize/Deserialize Binary Tree**: Tree encoding
12. **LC 105 - Construct from Preorder/Inorder**: Tree building

---

## Quick Decision Tree

```
Problem type...
├── "Collect traversal values"
│   ├── Specific order (inorder/pre/post) → DFS with correct order
│   └── Level by level → BFS
├── "Compute property (height, sum, count)"
│   ├── Single value → Postorder recursion
│   └── Check validity → Early termination with sentinel
├── "Path problem"
│   ├── Root to leaf → Track path during DFS
│   ├── Any path (max sum, diameter) → Return + Update pattern
│   └── Path sum → DFS with target tracking
├── "Level-based"
│   ├── By-level output → BFS with size batching
│   ├── Right-side view → BFS, take last of each level
│   └── Zigzag → BFS, alternate direction
└── "Validate structure"
    ├── Balanced → Height with -1 sentinel
    ├── BST validity → Pass min/max bounds
    └── Symmetric → Two-pointer recursion
```

---

## Related Patterns

| If you see... | Consider also... |
|--------------|------------------|
| Find path in tree | Graph DFS (if multiple paths) |
| Shortest path in tree | BFS (unweighted), but tree has unique path |
| Binary Search Tree | Binary Search pattern for O(log n) |
| Tree serialization | String parsing / State machines |
| Lowest Common Ancestor | Union-Find (for queries) |
| Tree to graph conversion | General graph algorithms |

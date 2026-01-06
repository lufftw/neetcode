---

## Pattern Comparison

### DFS vs BFS for Trees

| Aspect | DFS | BFS |
|--------|-----|-----|
| Space | O(h) - height | O(w) - width |
| Use when | Path-based, properties | Level-based |
| Order | Preorder/Inorder/Postorder | Level-order |
| Implementation | Recursion or stack | Queue |

### DFS Order Selection

| Order | When to Use | Code Pattern |
|-------|-------------|--------------|
| **Preorder** | Process parent first | visit → left → right |
| **Inorder** | BST sorted order | left → visit → right |
| **Postorder** | Need children's results | left → right → visit |

### Common Tree Patterns

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

### When to Use Each Pattern

| Problem Type | Pattern | Example |
|--------------|---------|---------|
| Count nodes | Simple property | Count, sum values |
| Height/depth | Simple property | Max depth, min depth |
| Validate structure | Early termination | Balanced, BST valid |
| Longest path | Path tracking | Diameter, max path sum |
| By level | BFS | Level order, zigzag |



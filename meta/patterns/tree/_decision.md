---

## Decision Framework

### Quick Reference Decision Tree

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

### Recursive Return Strategy

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

### Common Mistakes

| Mistake | Why Wrong | Correct Approach |
|---------|-----------|------------------|
| Forgetting base case | Infinite recursion | Check `if not node` first |
| Wrong order | Incorrect result | Match problem requirements |
| Recomputing values | O(n²) time | Compute bottom-up once |
| Not handling None | NullPointerException | Return base value for None |
| Path direction | Return wrong value | Single branch for parent |

### Complexity Expectations

| Operation | Time | Space |
|-----------|------|-------|
| Any single traversal | O(n) | O(h) |
| BFS level order | O(n) | O(w) |
| Property computation | O(n) | O(h) |



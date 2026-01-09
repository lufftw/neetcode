# Missing Test Files

> **Status**: Backlog
> **Last Updated**: 2025-01-09
> **Total Items**: 13 solutions

This document tracks solutions that do not have corresponding `.in/.out` test files in `tests/`.

---

## Summary

These solutions pass syntax checks and have valid `JUDGE_FUNC` implementations, but cannot be verified through the test runner due to missing test cases.

| Pattern Category | Count |
|------------------|-------|
| Tree Traversal | 5 |
| Graph (DFS/BFS) | 3 |
| Topological Sort | 2 |
| Union Find | 2 |
| Shortest Path | 1 |

---

## Solutions Without Test Files

### Tree Traversal (5)

| Problem | Name | Reason |
|---------|------|--------|
| 0094 | Binary Tree Inorder Traversal | Requires tree serialization format |
| 0102 | Binary Tree Level Order Traversal | Requires tree serialization format |
| 0104 | Maximum Depth of Binary Tree | Requires tree serialization format |
| 0110 | Balanced Binary Tree | Requires tree serialization format |
| 0543 | Diameter of Binary Tree | Requires tree serialization format |

### Graph (DFS/BFS) (3)

| Problem | Name | Reason |
|---------|------|--------|
| 0133 | Clone Graph | Complex graph structure input |
| 0417 | Pacific Atlantic Water Flow | 2D grid with multiple valid outputs |
| 0787 | Cheapest Flights Within K Stops | Complex input format |

### Topological Sort (2)

| Problem | Name | Reason |
|---------|------|--------|
| 0207 | Course Schedule | Needs prerequisite edge list format |
| 0210 | Course Schedule II | Multiple valid outputs |

### Union Find (2)

| Problem | Name | Reason |
|---------|------|--------|
| 0684 | Redundant Connection | Needs edge list format |
| 0721 | Accounts Merge | Complex nested list input |

### Shortest Path (1)

| Problem | Name | Reason |
|---------|------|--------|
| 0743 | Network Delay Time | Needs weighted edge list format |

---

## Common Blockers

### 1. Tree Serialization

Many tree problems require a standardized tree serialization format. Options:

- LeetCode-style level-order with `null` markers: `[1,2,3,null,null,4,5]`
- Need to implement `build_tree()` helper in test infrastructure

### 2. Graph Input Format

Graph problems need a consistent edge list or adjacency list format:

- Edge list: `[[0,1],[1,2],[2,0]]`
- Adjacency list: `[[1,2],[0,2],[0,1]]`

### 3. Multiple Valid Outputs

Some problems have multiple correct answers (e.g., Course Schedule II). These already have `JUDGE_FUNC` implementations but need test cases to exercise them.

---

## Resolution Path

To resolve these items:

1. **Define input format** in `docs/contracts/test-file-format.md` for each problem type
2. **Create test files** following the defined format
3. **Verify** with `python runner/test_runner.py <problem_name>`
4. **Remove** from this backlog once tests pass

---

## Related

- [Test File Format](../contracts/test-file-format.md)
- [Generator Contract](../contracts/generator-contract.md)

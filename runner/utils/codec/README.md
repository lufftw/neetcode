# Codec Package

> Data structure I/O utilities for LeetCode problems

## Overview

This package provides codec functions to convert between simple `.in/.out` formats and LeetCode data structures (ListNode, TreeNode, etc.).

**Single Source of Truth** — Both runtime (`import` mode) and code generation (`inline` mode) use this package.

## Responsibility

### What this package does

- ✅ Define data structure classes (ListNode, TreeNode, Node, etc.)
- ✅ Convert Python lists ↔ linked data structures
- ✅ Handle semantic conversions (cycles, shared nodes, random pointers)

### What this package does NOT do

- ❌ Problem-specific logic (handled by `solve()`)
- ❌ Test comparison (handled by `runner/compare.py`)
- ❌ Code generation (handled by `packages/codegen/`)

## Public API

```python
from runner.utils.codec import (
    # Classes
    ListNode, TreeNode, Node, NodeGraph, NodeNary, DoublyListNode,
    
    # ListNode functions
    list_to_linkedlist, linkedlist_to_list,
    build_list_with_cycle, node_to_index, build_intersecting_lists,
    
    # TreeNode functions
    list_to_tree, tree_to_list,
    
    # Node functions (random pointer)
    build_random_pointer_list, encode_random_pointer_list, verify_deep_copy,
    
    # NodeGraph functions
    adjacency_to_graph, graph_to_adjacency,
    
    # NodeNary functions
    list_to_nary_tree, nary_tree_to_list,
    
    # DoublyListNode functions
    list_to_doubly_linked, doubly_linked_to_list,
)
```

## File Structure

```
codec/
├── __init__.py              # Re-export all (IDE entry point)
├── classes/                 # Data structure definitions
│   ├── list_node.py         # ListNode
│   ├── tree_node.py         # TreeNode
│   ├── node.py              # Node (random pointer)
│   ├── node_graph.py        # NodeGraph
│   ├── node_nary.py         # NodeNary
│   └── doubly_list_node.py  # DoublyListNode
└── functions/               # Conversion functions
    ├── list_node/           # Depends on ListNode
    │   ├── struct.py        # Tier-1 functions
    │   └── semantic.py      # Tier-1.5 functions
    ├── tree_node/
    ├── node/
    ├── node_graph/
    ├── node_nary/
    └── doubly_list_node/
```

## Tier Classification

| Directory | Tier | Description |
|-----------|------|-------------|
| `functions/*/struct.py` | 1 | Value-based conversion |
| `functions/*/semantic.py` | 1.5 | Requires problem knowledge |

## Dependencies

| Direction | Module | Purpose |
|-----------|--------|---------|
| Used by → | `solutions/*.py` | Runtime codec |
| Used by → | `packages/codegen/` | AST extraction for inline mode |

## Related Documentation

- **[Contract: Codec](../../../docs/contracts/codec.md)** — Architecture, conventions, full reference
- **[Problem Support Boundary](../../../docs/contracts/problem-support-boundary.md)** — Tier definitions, codec modes

---

## Documentation Maintenance

⚠️ **When modifying this package:**

1. Update this README (quick reference)
2. Update `docs/contracts/codec.md` (contract)
3. Update `packages/codegen/core/catalog/__init__.py` if adding new classes/functions


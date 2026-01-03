# Catalog Structure Contract

> **Status**: Active  
> **Created**: 2026-01-03  
> **Updated**: 2026-01-03  
> **Purpose**: Define the codec package structure and AST extraction conventions

---

## Overview

**Single Source of Truth**: All codec classes and functions live in `runner/utils/codec/`.

The `catalog` module uses **AST extraction** to read code from this package for inline mode.
No separate templates directory — DRY principle.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    runner/utils/codec/                       │
│                  (Single Source of Truth)                    │
├─────────────────────────────────────────────────────────────┤
│  classes/          functions/                                │
│  ├─ list_node.py   ├─ list_node/                            │
│  ├─ tree_node.py   │  ├─ struct.py    (Tier-1)              │
│  ├─ node.py        │  └─ semantic.py  (Tier-1.5)            │
│  ├─ node_graph.py  ├─ tree_node/                            │
│  ├─ node_nary.py   ├─ node/                                 │
│  └─ doubly_...py   ├─ node_graph/                           │
│                    ├─ node_nary/                             │
│                    └─ doubly_list_node/                      │
└─────────────────────────────────────────────────────────────┘
           │                           │
           ▼                           ▼
    Import Mode                  Inline Mode
    ───────────                  ───────────
    from runner.utils.codec      catalog.get_with_deps()
    import list_to_tree          → AST extraction
                                 → Embed in solution
```

---

## Helper Classes Reference

| Class | Description | Example Problems |
|-------|-------------|------------------|
| **ListNode** | Singly linked list | 2, 19, 21, 23, 24, 25, 61, 82, 83, 86, 92, 141, 142, 143, 160, 203, 206, 234, 328, 876 |
| **TreeNode** | Binary tree | 94, 98, 100, 101, 102, 104, 105, 108, 110, 111, 112, 144, 145, 199, 226, 543, 572 |
| **Node** | Random pointer list | 138 (Copy List with Random Pointer) |
| **NodeGraph** | Graph with neighbors | 133 (Clone Graph), 207, 210, 261, 323 |
| **NodeNary** | N-ary tree | 429, 559, 589, 590 |
| **DoublyListNode** | Doubly linked list | 430, 146 (LRU Cache internal) |

---

## Directory Structure

```
runner/utils/codec/
├── __init__.py                      # Re-export all (IDE entry point)
├── classes/                         # Data structure definitions
│   ├── __init__.py                  # Re-export classes
│   ├── list_node.py                 # class ListNode
│   ├── tree_node.py                 # class TreeNode
│   ├── node.py                      # class Node (random pointer)
│   ├── node_graph.py                # class NodeGraph
│   ├── node_nary.py                 # class NodeNary
│   └── doubly_list_node.py          # class DoublyListNode
└── functions/                       # Conversion functions
    ├── __init__.py                  # Re-export all functions
    ├── list_node/                   # Depends on ListNode
    │   ├── __init__.py
    │   ├── struct.py                # Tier-1: list_to_linkedlist, etc.
    │   └── semantic.py              # Tier-1.5: build_list_with_cycle, etc.
    ├── tree_node/                   # Depends on TreeNode
    │   ├── __init__.py
    │   └── struct.py                # Tier-1: list_to_tree, tree_to_list
    ├── node/                        # Depends on Node
    │   ├── __init__.py
    │   └── semantic.py              # Tier-1.5: build_random_pointer_list, etc.
    ├── node_graph/                  # Depends on NodeGraph
    │   ├── __init__.py
    │   └── struct.py                # Tier-1: adjacency_to_graph, etc.
    ├── node_nary/                   # Depends on NodeNary
    │   ├── __init__.py
    │   └── struct.py                # Tier-1: list_to_nary_tree, etc.
    └── doubly_list_node/            # Depends on DoublyListNode
        ├── __init__.py
        └── struct.py                # Tier-1: list_to_doubly_linked, etc.
```

---

## Helper Functions Reference

### ListNode Functions

| Function | Tier | Description |
|----------|------|-------------|
| `list_to_linkedlist` | 1 | `[1,2,3]` → LinkedList |
| `linkedlist_to_list` | 1 | LinkedList → `[1,2,3]` |
| `build_list_with_cycle` | 1.5 | Build list with cycle at pos |
| `node_to_index` | 1.5 | Find node's index in array |
| `build_intersecting_lists` | 1.5 | Build two intersecting lists |

### TreeNode Functions

| Function | Tier | Description |
|----------|------|-------------|
| `list_to_tree` | 1 | Level-order list → BinaryTree |
| `tree_to_list` | 1 | BinaryTree → level-order list |

### Node (Random Pointer) Functions

| Function | Tier | Description |
|----------|------|-------------|
| `build_random_pointer_list` | 1.5 | `[[val, idx], ...]` → list with random pointers |
| `encode_random_pointer_list` | 1.5 | List with random pointers → `[[val, idx], ...]` |
| `verify_deep_copy` | 1.5 | Verify deep copy has no shared nodes |

### NodeGraph Functions

| Function | Tier | Description |
|----------|------|-------------|
| `adjacency_to_graph` | 1 | Adjacency list → Graph nodes |
| `graph_to_adjacency` | 1 | Graph nodes → adjacency list |

### NodeNary Functions

| Function | Tier | Description |
|----------|------|-------------|
| `list_to_nary_tree` | 1 | Level-order with nulls → N-ary tree |
| `nary_tree_to_list` | 1 | N-ary tree → level-order with nulls |

### DoublyListNode Functions

| Function | Tier | Description |
|----------|------|-------------|
| `list_to_doubly_linked` | 1 | `[1,2,3]` → DoublyLinkedList |
| `doubly_linked_to_list` | 1 | DoublyLinkedList → `[1,2,3]` |

---

## Dependency Resolution

Dependencies are inferred from the **directory structure**:

| Path Pattern | Dependency |
|--------------|------------|
| `classes/*.py` | None |
| `functions/list_node/*.py` | `ListNode` |
| `functions/tree_node/*.py` | `TreeNode` |
| `functions/node/*.py` | `Node` |
| `functions/node_graph/*.py` | `NodeGraph` |
| `functions/node_nary/*.py` | `NodeNary` |
| `functions/doubly_list_node/*.py` | `DoublyListNode` |

---

## Tier Inference

| Path Pattern | Tier |
|--------------|------|
| `classes/*` | base |
| `functions/*/struct.py` | 1 |
| `functions/*/semantic.py` | 1.5 |

---

## Usage

### Import Mode (Runtime)

```python
# In solution files
from runner.utils.codec import list_to_tree, TreeNode

root = list_to_tree([1, 2, 3])
```

**IDE Support**: Go to Definition works — jumps directly to `tree_node.py`.

### Inline Mode (Codegen)

```python
# In packages/codegen
from packages.codegen.core.catalog import get, get_with_deps

# Get single definition
code = get("ListNode")

# Get with dependencies resolved
code = get_with_deps("build_list_with_cycle")
# Returns: ListNode class + build_list_with_cycle function
```

---

## Catalog API

```python
from packages.codegen.core.catalog import (
    get,            # Get single template code
    deps,           # Get dependency list
    get_with_deps,  # Get code with all dependencies
    list_all,       # List all available names
    list_classes,   # List all class names
    list_functions, # List all function names
    tier,           # Get tier for a name
)

# Examples
get("ListNode")  # Returns class definition
deps("list_to_tree")  # Returns ["TreeNode"]
get_with_deps("build_list_with_cycle")  # Returns ListNode + function
tier("list_to_tree")  # Returns "1"
tier("node_to_index")  # Returns "1.5"
```

---

## Config Integration

`config/problem-support.yaml` only needs function names:

```yaml
"0142":
  tier: "1.5"
  codec_mode: inline
  codec_hints:
    - build_list_with_cycle
    - node_to_index
```

**No need to list `ListNode`** — catalog resolves dependencies automatically via AST.

---

## Adding New Codec

### Add a new class

1. Create `runner/utils/codec/classes/new_class.py`
2. Add to `classes/__init__.py`
3. Add to `codec/__init__.py`
4. Done (catalog auto-discovers via AST)

### Add a function

1. Create directory `runner/utils/codec/functions/new_class/`
2. Create `struct.py` (Tier-1) or `semantic.py` (Tier-1.5)
3. Add to `functions/new_class/__init__.py`
4. Add to `functions/__init__.py`
5. Add to `codec/__init__.py`
6. Update `catalog/__init__.py` dependency mapping
7. Done

---

## Key Benefits

| Feature | Benefit |
|---------|---------|
| **Single Source** | No sync issues between runtime and inline |
| **AST Extraction** | Precise code extraction without imports |
| **Directory Structure** | Dependencies self-documenting |
| **IDE Support** | Full Go to Definition works |
| **DRY** | One copy of each function |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-03 | Initial contract |
| 2026-01-03 | Refactored: Single source with AST extraction |

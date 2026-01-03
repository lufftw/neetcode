# Catalog Structure Contract

> **Status**: Active  
> **Created**: 2026-01-03  
> **Purpose**: Define the directory structure and conventions for template catalog

---

## Overview

The catalog stores reusable code templates (classes and functions) for code generation.
Directory structure determines dependencies - no configuration needed.

---

## Directory Structure

```
packages/codegen/core/catalog/
├── __init__.py                      # API (~40 lines)
└── templates/
    ├── classes/                     # Base types (no dependencies)
    │   ├── ListNode.py
    │   ├── TreeNode.py
    │   └── Node.py
    └── functions/
        ├── ListNode/                # Depends on ListNode
        │   ├── struct/              # Tier-1 (value conversion)
        │   │   ├── list_to_linkedlist.py
        │   │   └── linkedlist_to_list.py
        │   └── semantic/            # Tier-1.5 (identity/semantic)
        │       ├── build_list_with_cycle.py
        │       ├── node_to_index.py
        │       └── build_intersecting_lists.py
        ├── TreeNode/
        │   └── struct/
        │       ├── list_to_tree.py
        │       └── tree_to_list.py
        └── Node/
            └── semantic/
                ├── build_random_pointer_list.py
                └── encode_random_pointer_list.py
```

---

## Conventions

### 1. Dependency Resolution (Priority Order)

| Priority | Condition | `depends_on` |
|----------|-----------|--------------|
| 1 | File has `TEMPLATE_META["depends_on"]` | Use specified value |
| 2 | Path is `functions/<ClassName>/...` | `[<ClassName>]` |
| 3 | Otherwise | `[]` |

### 2. Tier Inference

| Path Pattern | Tier |
|--------------|------|
| `classes/*` | base |
| `functions/*/struct/*` | 1 |
| `functions/*/semantic/*` | 1.5 |

### 3. Template File Format

Templates MUST be **pure definitions** with no imports:

```python
# ✅ CORRECT
class ListNode:
    """Singly linked list node."""
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next
```

```python
# ❌ WRONG (has import)
from typing import Optional

class ListNode:
    ...
```

**Reason**: Templates are pasted directly into generated files.

### 4. Exception Handling (Multi-Dependency)

For rare cases where a function depends on multiple classes, use `TEMPLATE_META`:

```python
# templates/functions/ListNode/semantic/some_multi_dep_func.py

TEMPLATE_META = {"depends_on": ["ListNode", "TreeNode"]}

def some_multi_dep_func(...):
    ...
```

---

## API

```python
from packages.codegen.core.catalog import get, deps, get_with_deps

# Get single template
code = get("ListNode")

# Get dependencies
deps("build_list_with_cycle")  # → ["ListNode"]

# Get template with all dependencies
code = get_with_deps("build_list_with_cycle")
# Returns: ListNode class + build_list_with_cycle function
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

**No need to list `ListNode`** - catalog resolves dependencies automatically.

---

## Adding New Templates

### Add a new class

1. Create `templates/classes/NewClass.py`
2. Done (auto-discovered)

### Add a function depending on existing class

1. Create `templates/functions/ListNode/struct/new_function.py`
2. Done (dependency inferred from path)

### Add a function with multiple dependencies

1. Create file in primary dependency folder
2. Add `TEMPLATE_META = {"depends_on": ["ClassA", "ClassB"]}`

---

## Validation Rules

1. **Unique names**: No two templates can have the same stem name
2. **Valid Python**: Templates must be syntactically valid
3. **No imports**: Templates cannot have import statements
4. **Dependency exists**: `depends_on` must reference existing classes

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-03 | Initial contract |


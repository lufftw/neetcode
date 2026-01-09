# Migration Plan: Tiered Problem Generation

> **Branch**: `feat/tiered-problem-generation`  
> **Created**: 2026-01-03  
> **Status**: In Progress

---

## Overview

This document outlines the implementation and migration plan for the Tiered Problem Generation framework.

---

## Phase 1: Infrastructure Setup ✅

### 1.1 Documentation (Complete)
- [x] `docs/contracts/problem-support-boundary.md` — Contract with Hard Rules
- [x] `config/problem-support.yaml` — Living registry
- [x] `docs/in-progress/tiered-problem-generation/specification.md` — Spec

### 1.2 Decisions Finalized
- [x] tier format: string `"1.5"`
- [x] import path: `runner/utils/codec.py`
- [x] inline_reason: required for inline mode
- [x] io_format naming: `_to_` pattern

---

## Phase 2: Codec Implementation ✅

### 2.1 Create `runner/utils/codec.py` ✅

**Purpose**: Runtime codec for `codec_mode: import`

```python
# Tier-1 functions (value-based I/O)
list_to_linkedlist(lst) -> ListNode
linkedlist_to_list(node) -> list
list_to_tree(lst) -> TreeNode
tree_to_list(root) -> list

# Tier-1.5 functions (semantic I/O)
build_list_with_cycle(values, pos) -> (head, nodes)
node_to_index(node, nodes) -> int
build_intersecting_lists(...) -> (headA, headB)
build_random_pointer_list(pairs) -> Node
encode_random_pointer_list(head) -> list
```

### 2.2 Refactor Catalog to Hybrid Structure ✅

**New Structure**:
```
src/codegen/core/catalog/
├── __init__.py              # Unified API
├── registry.py              # Metadata registry
└── templates/
    ├── classes/
    │   ├── ListNode.py
    │   ├── TreeNode.py
    │   └── Node.py
    └── functions/
        ├── struct/          # Tier-1
        │   ├── list_to_linkedlist.py
        │   └── ...
        └── semantic/        # Tier-1.5
            ├── build_list_with_cycle.py
            └── ...
```

**Benefits**:
- Templates are real Python files (testable, lintable)
- Can be imported for runtime use
- Can be read as strings for inline codegen
- Registry only manages metadata

---

## Phase 3: Config Reader ✅

### 3.1 Create config reader utility ✅

**Location**: `src/codegen/core/problem_support.py` (implemented)

All required functions are implemented:
- ✅ `load_problem_config(problem_id: str) -> ProblemConfig`
- ✅ `get_tier(problem_id: str) -> Tier`
- ✅ `get_codec_mode(problem_id: str) -> CodecMode`
- ✅ `get_codec_hints(problem_id: str) -> List[str]`
- ✅ `validate_config(problem_id: str) -> List[str]`

### 3.2 Integrate with codegen ✅

**Updated**: `src/codegen/reference/generator.py`
- ✅ Auto-detects tier from config
- ✅ Automatically uses tiered mode for Tier-1/1.5 problems
- ✅ Applies codec_mode logic (import vs inline)
- ✅ Uses codec_hints for function selection

---

## Phase 4: From-Scratch Generation Test Plan 🔜

### 4.1 Test Problems (No Existing Solution)

These problems will be used to test from-scratch generation:

#### Tier-1 ListNode (Value-based I/O)
| ID | Name | Codec | Status |
|----|------|-------|--------|
| 0019 | Remove Nth Node From End | `list_to_linkedlist` | Pending |
| 0024 | Swap Nodes in Pairs | `list_to_linkedlist` | Pending |
| 0061 | Rotate List | `list_to_linkedlist` | Pending |
| 0082 | Remove Duplicates II | `list_to_linkedlist` | Pending |
| 0083 | Remove Duplicates | `list_to_linkedlist` | Pending |
| 0203 | Remove List Elements | `list_to_linkedlist` | Pending |
| 0234 | Palindrome Linked List | `list_to_linkedlist` | Pending |
| 0328 | Odd Even Linked List | `list_to_linkedlist` | Pending |

#### Tier-1 TreeNode (Value-based I/O)
| ID | Name | Codec | Status |
|----|------|-------|--------|
| 0094 | Inorder Traversal | `list_to_tree` | Pending |
| 0100 | Same Tree | `list_to_tree` | Pending |
| 0101 | Symmetric Tree | `list_to_tree` | Pending |
| 0102 | Level Order Traversal | `list_to_tree` | Pending |
| 0104 | Maximum Depth | `list_to_tree` | Pending |
| 0110 | Balanced Binary Tree | `list_to_tree` | Pending |
| 0111 | Minimum Depth | `list_to_tree` | Pending |
| 0112 | Path Sum | `list_to_tree` | Pending |
| 0144 | Preorder Traversal | `list_to_tree` | Pending |
| 0145 | Postorder Traversal | `list_to_tree` | Pending |
| 0199 | Right Side View | `list_to_tree` | Pending |
| 0226 | Invert Binary Tree | `list_to_tree` | Pending |
| 0543 | Diameter of Binary Tree | `list_to_tree` | Pending |
| 0572 | Subtree of Another Tree | `list_to_tree` | Pending |

#### Tier-1 NodeNary (Value-based I/O)
| ID | Name | Codec | Status |
|----|------|-------|--------|
| 0559 | Max Depth N-ary Tree | `list_to_nary_tree` | Pending |
| 0589 | N-ary Preorder | `list_to_nary_tree` | Pending |
| 0590 | N-ary Postorder | `list_to_nary_tree` | Pending |

#### Tier-1.5 (Semantic I/O)
| ID | Name | Codec | Status |
|----|------|-------|--------|
| 0133 | Clone Graph | `adjacency_to_graph` | Pending |
| 0138 | Copy List Random Pointer | `build_random_pointer_list` | Pending |
| 0160 | Intersection of Two Lists | `build_intersecting_lists` | Pending |

### 4.2 Existing Solutions (Protected)

These have handwritten solutions - NO auto-overwrite:

| ID | Name | Status |
|----|------|--------|
| 0002 | Add Two Numbers | ✅ Protected |
| 0021 | Merge Two Sorted Lists | ✅ Protected |
| 0023 | Merge k Sorted Lists | ✅ Protected |
| 0025 | Reverse Nodes in k-Group | ✅ Protected |
| 0141 | Linked List Cycle | ✅ Protected |
| 0142 | Linked List Cycle II | ✅ Protected |
| 0206 | Reverse Linked List | ✅ Protected |
| 0876 | Middle of Linked List | ✅ Protected |

### 4.3 Test Execution Order

1. **Start with simplest**: 0094 (Inorder Traversal), 0104 (Max Depth)
2. **Progress to LinkedList**: 0083 (Remove Dups), 0206 (Reverse)
3. **Test semantic I/O**: 0160 (Intersection), 0133 (Clone Graph)
4. **Validate N-ary**: 0559 (Max Depth N-ary)

---

## Phase 5: Testing 🔜

### 5.1 Unit Tests

```
.dev/tests/
├── test_codec.py              # Test codec functions
├── test_config_reader.py      # Test config reading
└── test_solve_generator.py    # Test generation with tiers
```

### 5.2 Integration Tests

| Test Case | Description |
|-----------|-------------|
| Tier-0 new problem | `codegen new 1 --with-tests` |
| Tier-1 new problem | `codegen new 2 --with-tests` |
| Tier-1.5 new problem | `codegen new 142 --with-tests` (warning) |
| Practice from solution | `codegen practice 142` |
| Handwritten protection | Try overwrite without --force |

### 5.3 Validation

```bash
# All existing tests should pass
leetcode\Scripts\python.exe -m pytest .dev/tests -q

# Run all solutions
leetcode\Scripts\python.exe runner/test_runner.py --all
```

---

## Rollout Plan

### Stage 1: Internal (This Branch)
1. Implement codec.py
2. Update catalog.py
3. Create config reader
4. Test with existing solutions

### Stage 2: Integration
1. Update codegen to use config
2. Test new problem generation
3. Test practice generation

### Stage 3: Documentation
1. Update README
2. Update contributor guide
3. Add examples

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Break existing solutions | Handwritten protection rule |
| Config/code mismatch | Validation in config reader |
| Import path issues | Test on fresh environment |
| Performance regression | Benchmark before merge |

---

## Acceptance Criteria

### Must Have
- [x] `runner/utils/codec/` works with import mode (package structure)
- [x] `catalog.py` has all Tier-1.5 templates (AST-based extraction)
- [x] Config reader validates inline_reason
- [x] Handwritten solutions protected (via file existence check)
- [ ] All existing tests pass (needs verification)

### Should Have
- [x] codegen uses config for tier-aware generation (auto-detection implemented)
- [ ] Practice generation works (needs testing)

### Nice to Have
- [ ] Migration script for bulk updates
- [ ] Verbose mode for debugging

---

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Phase 1: Infrastructure | 1 day | ✅ Complete |
| Phase 2: Codec | 1 day | ✅ Complete |
| Phase 3: Config Reader | 0.5 day | ✅ Complete |
| Phase 4: Migration | 0.5 day | ✅ Complete (auto-detection) |
| Phase 5: Testing | 1 day | 🔜 In Progress |

**Total**: ~4 days

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-03 | Initial plan created |
| 2026-01-03 | Phase 2 & 3 completed: Codec module and config reader integrated |
| 2026-01-03 | Auto-detection implemented: Tier-1/1.5 problems automatically use tiered mode |
| 2026-01-03 | SolveMode type updated to include "tiered" |


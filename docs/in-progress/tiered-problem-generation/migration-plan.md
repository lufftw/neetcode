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

## Phase 2: Codec Implementation 🔜

### 2.1 Create `runner/utils/codec.py`

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

### 2.2 Update `packages/codegen/core/helpers/catalog.py`

**Purpose**: Templates for `codec_mode: inline`

Add to `HELPER_FUNCTIONS`:
- `build_list_with_cycle`
- `node_to_index`
- `build_intersecting_lists`
- `build_random_pointer_list`
- `encode_random_pointer_list`

---

## Phase 3: Config Reader 🔜

### 3.1 Create config reader utility

**Location**: `packages/codegen/config/problem_support.py`

```python
def load_problem_config(problem_id: str) -> dict:
    """Load problem configuration from problem-support.yaml"""
    
def get_tier(problem_id: str) -> str:
    """Get tier for a problem (default: "0")"""
    
def get_codec_mode(problem_id: str) -> str:
    """Get codec_mode for a problem (default: "import")"""
    
def get_codec_hints(problem_id: str) -> list:
    """Get codec_hints for a problem"""
    
def validate_config(problem_id: str) -> list[str]:
    """Validate config (e.g., inline_reason required for inline mode)"""
```

### 3.2 Integrate with codegen

Update `packages/codegen/core/solve_generator.py`:
- Read tier from config
- Apply codec_mode logic
- Use codec_hints for function selection

---

## Phase 4: Existing Solutions Migration 🔜

### 4.1 Inventory

| Problem | Current State | Target State | Action |
|---------|---------------|--------------|--------|
| 0002 | Inline codec | Keep inline (handwritten) | None |
| 0021 | Inline codec | Keep inline (handwritten) | None |
| 0023 | Inline codec | Keep inline (handwritten) | None |
| 0025 | Inline codec | Keep inline (handwritten) | None |
| 0141 | Inline codec | Keep inline (handwritten) | None |
| 0142 | Inline codec | Keep inline (handwritten) | None |
| 0206 | — | — | — |
| 0876 | Inline codec | Keep inline (handwritten) | None |

### 4.2 Migration Rules

1. **Handwritten solutions**: NO automatic changes
2. **Future generated solutions**: Follow config settings
3. **Practice generation**: Always use existing solution as source

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
- [ ] `runner/utils/codec.py` works with import mode
- [ ] `catalog.py` has all Tier-1.5 templates
- [ ] Config reader validates inline_reason
- [ ] Handwritten solutions protected
- [ ] All existing tests pass

### Should Have
- [ ] codegen uses config for tier-aware generation
- [ ] Practice generation works

### Nice to Have
- [ ] Migration script for bulk updates
- [ ] Verbose mode for debugging

---

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Phase 1: Infrastructure | 1 day | ✅ Complete |
| Phase 2: Codec | 1 day | 🔜 In Progress |
| Phase 3: Config Reader | 0.5 day | Pending |
| Phase 4: Migration | 0.5 day | Pending |
| Phase 5: Testing | 1 day | Pending |

**Total**: ~4 days

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-03 | Initial plan created |


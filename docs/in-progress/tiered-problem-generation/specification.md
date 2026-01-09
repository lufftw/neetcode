# Spec: Tiered Problem Generation & Codec Framework

> **Status**: 📝 Draft — Ready for Implementation  
> **Branch**: `feat/tiered-problem-generation`  
> **Created**: 2026-01-03  
> **Updated**: 2026-01-03  
> **Contract**: [problem-support-boundary.md](../../contracts/problem-support-boundary.md)

---

## Summary

This feature establishes:
1. **Tiered Problem Support** — Clear tier definitions with Practice-first priority
2. **Dual Codec Mode** — Support both Inline (Template) and Import (Runtime) approaches
3. **Mechanical Practice Generation** — Generate practice files by copying solution + clearing method body
4. **Hard Rules** — Protect handwritten solutions, require inline_reason for inline mode

---

## Goals

- Support **from-scratch generation** of complete practice scaffolds
- Generate: `solutions/{id}_{slug}.py`, `tests/*.in/*.out`, `generators/*.py`
- **Practice-first**: User only needs to fill `Solution.method()` to practice
- Keep `.in/.out` **simple and Example-friendly**
- Protect handwritten solutions from auto-overwrite

## Non-Goals (v1)

- ❌ Universal graph serialization system
- ❌ Hybrid inline/import (no `inline_overrides`)
- ❌ Automatic Tier-2 support
- ❌ Premature abstraction

---

## Finalized Decisions

| Item | Decision |
|------|----------|
| **tier format** | String `"1.5"` (not number) |
| **import path** | `runner/utils/codec/` (package) |
| **inline_reason** | Required when `codec_mode: inline` |
| **Tier-1.5 codec_mode** | Explicit `codec_mode: inline` (not inherited) |
| **Tier-1.5 generators** | Default `false` |
| **Handwritten protection** | MUST NOT overwrite without `--force` |

---

## Core Principles

### 1. Solution = Self-Contained Executable Environment

A solution file contains **everything needed** for practice generation:

| Component | Purpose | Practice Generation |
|-----------|---------|---------------------|
| `solve()` | I/O translation (codec) | ✅ Keep as-is |
| `JUDGE_FUNC` | Comparison semantics | ✅ Keep as-is |
| `ListNode` etc. | Data structures | ✅ Keep as-is |
| `Solution.method()` | Algorithm | ❌ Clear body → TODO |

> **Practice generation is mechanical**: copy + clear method body.

### 2. Judge is Semantic-Free

Judge MUST NOT contain problem-specific logic.

### 3. solve() is the Adapter

`solve()` adapts between simple `.in/.out` and LeetCode structures.

### 4. Anti-Overengineering

> **Extract patterns from working solutions, don't design universal systems upfront.**

---

## Tier Classification

| Tier | Definition | Scaffold | Practice | Generator |
|------|------------|----------|----------|-----------|
| **"0"** | Signature → I/O derivable | ✅ auto | ✅ | ✅ |
| **"1"** | Needs codec, value-based I/O | ✅ auto | ✅ | ✅ |
| **"1.5"** | I/O semantics need problem knowledge | ✅ scaffold | ✅ | ⚠️ manual |
| **"2"** | Complex structures (future) | ❌ | ❌ | ❌ |

### Key Insight

> **Tier "0"/"1"/"1.5": ALL can practice**
> Tier classification is about GENERATION capability, not practice capability.

---

## Dual Codec Mode

### Mode 1: Import (Default)

```python
from runner.utils.codec import list_to_linkedlist, linkedlist_to_list
```

- ✅ DRY, central maintenance
- ❌ Can't copy to LeetCode

### Mode 2: Inline

```python
def list_to_linkedlist(lst: list) -> 'ListNode':
    # ... full implementation ...
```

- ✅ Self-contained, LeetCode-copyable
- ❌ Code duplication

### When to Use Inline (Hard Rules)

| # | Condition | Example |
|---|-----------|---------|
| 1 | Custom adapter needed | 0142: `node_to_index` |
| 2 | Custom JUDGE_FUNC needed | 0138: deep copy verification |
| 3 | LeetCode copy-paste required | User request |

---

## Canonical Semantics

These are **non-negotiable**:

| Item | Canonical Value |
|------|-----------------|
| `node_to_index` | **0-based** |
| No-result | **-1** (integer) |
| Boolean | `true`/`false` (JSON) |

---

## Config Schema

```yaml
# config/problem-support.yaml

defaults:
  tier: "0"
  codec_mode: import
  generators:
    random: true
    complexity: true

problems:
  # Tier "1": Use default import
  "0002":
    tier: "1"
    io_format: list_to_list
    codec_hints: [list_to_linkedlist, linkedlist_to_list]

  # Tier "1.5": Explicit inline + reason
  "0142":
    tier: "1.5"
    codec_mode: inline
    inline_reason: "Output is node identity, needs node_to_index adapter"
    io_format: list_with_pos_to_node_index
    codec_hints: [build_list_with_cycle, node_to_index]
    generators:
      random: false
      complexity: false

tier2:
  - id: "0297"
    name: "Serialize and Deserialize Binary Tree"
  - id: "0430"
    name: "Flatten a Multilevel Doubly Linked List"
```

---

## Hard Rules

### Rule 1: Handwritten Solution Protection

```
IF solutions/{id}_{slug}.py EXISTS AND is_handwritten:
    codegen MUST NOT overwrite without --force flag
```

### Rule 2: inline_reason Required

```
IF codec_mode == "inline":
    inline_reason MUST be non-empty string
```

### Rule 3: Tier-1.5 Generators Default Off

```
IF tier == "1.5":
    generators.random DEFAULT false
    generators.complexity DEFAULT false
```

---

## File Structure

### New/Modified Files

| Path | Purpose |
|------|---------|
| `docs/contracts/problem-support-boundary.md` | Contract (stable rules) |
| `docs/contracts/codec.md` | Codec package contract |
| `config/problem-support.yaml` | Living registry |
| `runner/utils/codec/` | **Single Source**: Runtime + inline templates |
| `src/codegen/core/catalog/` | AST extraction from codec/ |
| `src/codegen/core/problem_support.py` | Config reader utility |
| `src/codegen/core/tiered_solve_generator.py` | Tiered solve() generation |

---

## Implementation Phases

### Phase 1: Framework Setup ✅
- [x] Create `docs/contracts/problem-support-boundary.md`
- [x] Create `docs/contracts/catalog-structure.md`
- [x] Create `config/problem-support.yaml`

### Phase 2: Codec Implementation ✅
- [x] Create `runner/utils/codec/` package (Single Source of Truth)
- [x] Implement all 6 classes: ListNode, TreeNode, Node, NodeGraph, NodeNary, DoublyListNode
- [x] Implement all Tier-1 and Tier-1.5 functions
- [x] Update `catalog/__init__.py` with AST extraction

### Phase 3: codegen Integration ✅
- [x] Create `src/codegen/core/problem_support.py` (config reader)
- [x] Create `src/codegen/core/tiered_solve_generator.py`
- [x] Implement `codec_mode` logic (import vs inline)
- [x] Add `--solve-mode=tiered` CLI option
- [x] Add `--codec-mode` CLI option (override config)
- [x] Auto-detect `has_solution` from filesystem

### Phase 4: Testing
- [x] Test Tier-1 generation (0104 Maximum Depth of Binary Tree)
- [ ] Test Tier-1.5 inline generation (0142)
- [ ] Test handwritten solution protection
- [ ] Test practice generation

---

## Acceptance Criteria

### Hard Rules
- [ ] Handwritten solutions are NOT overwritten without `--force`
- [ ] `inline_reason` validation fails if missing for inline mode
- [x] Tier-1.5 generators default to `false`

### Tier-1 Generation
- [x] `codegen new 104 --solve-mode=tiered` generates scaffold with import mode
- [x] Generated `solve()` uses `from runner.utils.codec import ...`
- [ ] Tests pass with generated scaffold + manual algorithm

### Tier-1.5 Generation
- [ ] `codegen new 142 --solve-mode=tiered` generates scaffold with inline mode
- [ ] Generated `solve()` contains inlined codec functions
- [ ] `inline_reason` is documented in generated file

### Practice Generation
- [ ] `codegen practice 142` works with existing solution
- [x] Mechanical copy: only `Solution.method()` body is cleared
- [x] All infrastructure (solve, judge, helpers) preserved

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [problem-support-boundary.md](../../contracts/problem-support-boundary.md) | Contract (Hard Rules, Semantics) |
| [test-file-format.md](../../contracts/test-file-format.md) | .in/.out format spec |
| `config/problem-support.yaml` | Living registry |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-03 | Initial draft |
| 2026-01-03 | Finalized: tier as string, inline_reason required, hard rules |

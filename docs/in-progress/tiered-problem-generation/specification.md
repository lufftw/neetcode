# Spec: Tiered Problem Generation & Codec Framework

> **Status**: 📝 Draft — Under Discussion  
> **Branch**: `feat/tiered-problem-generation`  
> **Created**: 2026-01-03  
> **Updated**: 2026-01-03  
> **Related**: [problem-support-boundary.md](../../contracts/problem-support-boundary.md) · [test-file-format.md](../../contracts/test-file-format.md)

## Summary

This feature establishes:
1. **Tiered Problem Support** — Clear tier definitions with Practice-first priority
2. **Dual Codec Mode** — Support both Inline (Template) and Import (Runtime) approaches
3. **Mechanical Practice Generation** — Generate practice files by copying solution + clearing method body

---

## Goals

- Define clear system boundaries for auto-generation capabilities
- Support ListNode/TreeNode problems with simple value-based I/O (Tier-1)
- Document problems that require manual `solve()` implementation (Tier-1.5)
- Provide codec utilities for common data structure operations
- Enable iterative expansion: manual solutions → pattern extraction → system support

## Non-Goals (v1)

- ❌ Universal graph serialization system
- ❌ Automatic handling of node identity comparison (0142, 0160)
- ❌ Random pointer support in core (0138)
- ❌ Complex structures: Graph clone, multi-level lists
- ❌ Premature abstraction before working solutions exist

---

## Core Principles

### 1. Judge is Semantic-Free

Judge MUST NOT contain problem-specific logic.

| ✅ Judge Does | ❌ Judge Does NOT |
|---------------|-------------------|
| Exact string comparison | Know about ListNode/TreeNode |
| Float tolerance | Have `if problem_id == X` branches |
| Order-independent comparison | Implement problem-specific logic |

### 2. solve() is the Adapter

For Tier-1.5 problems, `solve()` serves as the adapter between:
- Simple `.in/.out` format (human-friendly, Example-derivable)
- LeetCode's expected data structures and semantics

### 3. Anti-Overengineering

> **Extract patterns from working solutions, don't design universal systems upfront.**

```
Phase 1: Write working solve() for 0142, 0160, 0138
Phase 2: Identify common patterns
Phase 3: Extract into codec utilities
Phase 4: Update tier classification
```

### 4. Solution = Self-Contained Executable Environment

A solution file contains **everything needed** for practice generation:

| Component | Purpose | Practice Generation |
|-----------|---------|---------------------|
| `solve()` | I/O translation (codec) | ✅ Keep as-is |
| `JUDGE_FUNC` | Comparison semantics | ✅ Keep as-is |
| `ListNode` etc. | Data structures | ✅ Keep as-is |
| `Solution.method()` | Algorithm | ❌ Clear body → TODO |

> **Practice generation is mechanical**: copy + clear method body.
> No semantic understanding required.

---

## Dual Codec Mode

The system supports **two codec approaches** to balance flexibility and DRY:

### Mode 1: Inline (Template-based)

```python
# Generated file contains the codec code directly
def list_to_linkedlist(lst: list) -> 'ListNode':
    # ... full implementation inline ...
```

| Pros | Cons |
|------|------|
| ✅ Self-contained | ❌ Code duplication |
| ✅ Can customize per-problem | ❌ Template updates don't propagate |
| ✅ Copy-paste to LeetCode | |

### Mode 2: Import (Runtime codec)

```python
# Generated file imports from shared codec
from runner.utils.codec import list_to_linkedlist, linkedlist_to_list
```

| Pros | Cons |
|------|------|
| ✅ DRY (no duplication) | ❌ External dependency |
| ✅ Central updates apply everywhere | ❌ Can't customize per-problem |
| | ❌ Can't copy to LeetCode directly |

### Config Field: `codec_mode`

```yaml
"0002":
  tier: 1
  codec_mode: inline  # or "import"
  codec_hints: [list_to_linkedlist, linkedlist_to_list]
```

### Decision Guide

| Situation | Recommended Mode |
|-----------|------------------|
| Standard codec, no customization | `import` |
| Need per-problem customization | `inline` |
| Want LeetCode-copyable output | `inline` |
| Tier-1.5 with special semantics | `inline` |

---

## Tier Classification

| Tier | Definition | Auto solve()? | Auto tests? |
|------|------------|---------------|-------------|
| **Tier-0** | Signature → I/O fully derivable | ✅ | ✅ |
| **Tier-1** | Needs codec, value-based I/O | ✅ | ✅ |
| **Tier-1.5** | I/O semantics require problem knowledge | ❌ | ✅ |
| **Tier-2** | Complex structures (future) | ❌ | ❌ |

### Tier-1.5 Definition (Key Insight)

> **Tier-1.5 = 題目的 I/O 語義無法由 signature + value alone 決定**

This is NOT a system failure — it's an inherent property of the problem.

---

## Problem Classification

> **Key Insight**: Tier-1.5 is defined by **output semantic needing problem knowledge**,  
> NOT by "input needs special construction".

### Tier-1 Problems (Auto-generatable with Codec)

| Problem | io_format | Why Tier-1 |
|---------|-----------|------------|
| 0002 | `list_to_list` | Value-based I/O |
| 0021 | `two_lists_to_list` | Value-based I/O |
| 0023 | `list_of_lists_to_list` | Value-based I/O |
| 0025 | `list_int_to_list` | Value-based I/O |
| 0141 | `list_with_pos__out_bool` | Output is bool (value comparison) |
| 0206 | `list_to_list` | Value-based I/O |
| 0876 | `list_to_list` | Output is value array |

**Note on 0141**: Input needs cycle construction (`pos` parameter), but output is boolean. 
Value comparison is sufficient, so it's Tier-1.

**Note on 0876**: Output `[3,4,5]` is values from middle node. Value comparison works.

---

### Tier-1.5 Problems (Manual solve() Required)

These problems have **output semantics that need problem knowledge**.

#### 0142 — Linked List Cycle II

| Aspect | Detail |
|--------|--------|
| **io_format** | `list_with_pos__out_node_index` |
| **output_semantic** | `node_ref_index` |
| **Why Tier-1.5** | Output is node identity (which node is the cycle entry) |

**.in/.out**:
```
[3,2,0,-4]
1

# .out
1
```

#### 0160 — Intersection of Two Linked Lists

| Aspect | Detail |
|--------|--------|
| **io_format** | `two_lists_with_skips__out_node_value` |
| **output_semantic** | `node_ref_value` |
| **Why Tier-1.5** | Output is shared node identity |

**.in/.out** (matches LeetCode Example):
```
[4,1,8,4,5]
[5,6,1,8,4,5]
2
3

# .out
8
```

#### 0138 — Copy List with Random Pointer

| Aspect | Detail |
|--------|--------|
| **io_format** | `random_pointer_list` |
| **Why Tier-1.5** | Multi-pointer structure (next + random) |

**.in/.out**:
```
[[7,null],[13,0],[11,4],[10,2],[1,0]]

# .out
[[7,null],[13,0],[11,4],[10,2],[1,0]]
```

---

## File Structure

### New Files

| Path | Purpose |
|------|---------|
| `docs/contracts/problem-support-boundary.md` | System capability boundaries |
| `config/problem-support.yaml` | Per-problem tier configuration |
| `runner/utils/codec.py` | Data structure codec utilities |

### Modified Files

| Path | Change |
|------|--------|
| `packages/codegen/cli.py` | Read problem-support.yaml |
| `packages/codegen/core/solve_generator.py` | Tier-aware generation |

---

## Config Schema: `config/problem-support.yaml`

```yaml
# Default: Tier-0 (fully auto-generated)
defaults:
  tier: 0
  auto_solve: true
  auto_tests: true

# Tier-1: Needs codec, auto-generatable
tier1:
  - "0002"  # Add Two Numbers
  - "0021"  # Merge Two Sorted Lists
  - "0206"  # Reverse Linked List
  - "0094"  # Binary Tree Inorder Traversal

# Tier-1.5: Manual solve() required
tier1_5:
  "0142":
    reason: "Output is node identity (cycle entry point)"
    input_format: |
      Line 1: values array
      Line 2: pos (cycle position, -1 if none)
    output_format: "Node index or null"
    codec_hints:
      - build_list_with_cycle

  "0160":
    reason: "Output is shared node identity"
    codec_hints:
      - build_intersecting_lists

  "0138":
    reason: "Random pointer structure"
    codec_hints:
      - build_random_pointer_list

  "0876":
    reason: "Output is sublist from middle node"
    codec_hints:
      - list_to_values

# Tier-2: Future work
tier2:
  - "0133"  # Clone Graph
  - "0297"  # Serialize/Deserialize Binary Tree
```

---

## Codec Utilities: `runner/utils/codec.py`

### Tier-1 (Implement Now)

```python
def build_list(values: List[int]) -> Optional[ListNode]:
    """[1,2,3] → ListNode chain"""

def list_to_values(head: Optional[ListNode]) -> List[int]:
    """ListNode chain → [1,2,3]"""

def build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """[1,null,2,3] → TreeNode (level-order)"""

def tree_to_values(root: Optional[TreeNode]) -> List[Optional[int]]:
    """TreeNode → [1,null,2,3]"""
```

### Tier-1.5 (Extract After Manual Solutions)

```python
def build_list_with_cycle(values: List[int], pos: int) -> Tuple[ListNode, List[ListNode]]:
    """Build cyclic list, return (head, nodes_array)"""

def build_intersecting_lists(...) -> Tuple[ListNode, ListNode]:
    """Build two lists sharing nodes"""

def build_random_pointer_list(pairs: List[List]) -> Optional[Node]:
    """Build list with random pointers"""
```

---

## codegen Behavior

### Tier-0 / Tier-1: Auto-generate

```
✅ Created: solutions/0002_add_two_numbers.py (solve() auto-generated)
✅ Created: tests/0002_add_two_numbers_1.in
✅ Created: tests/0002_add_two_numbers_1.out
```

### Tier-1.5: TODO Template

```
⚠️  Problem 0142 requires manual solve() implementation

Reason: Output is node identity (cycle entry point)

✅ Created: solutions/0142_linked_list_cycle_ii.py
   └─ Contains TODO template for solve()
✅ Created: tests/0142_linked_list_cycle_ii_1.in
✅ Created: tests/0142_linked_list_cycle_ii_1.out

Codec hints: build_list_with_cycle
Reference: docs/contracts/problem-support-boundary.md#tier-15
```

### solve() TODO Template

```python
def solve():
    """
    TODO: Manual implementation required
    
    Reason: Output is node identity (cycle entry point)
    
    Steps:
    1. Parse input
    2. Build structure using codec
    3. Run Solution()
    4. Encode and print result
    
    Codec hints: build_list_with_cycle
    Reference: docs/contracts/problem-support-boundary.md
    """
    raise NotImplementedError("Manual solve() required")
```

---

## Implementation Phases

### Phase 1: Framework Setup
- [ ] Create `docs/contracts/problem-support-boundary.md`
- [ ] Create `config/problem-support.yaml`
- [ ] Update codegen to read config

### Phase 2: Tier-1 Codec
- [ ] Implement `runner/utils/codec.py` (build_list, build_tree, etc.)
- [ ] Update solve_generator for Tier-1 problems
- [ ] Test with 0002, 0021, 0206

### Phase 3: Tier-1.5 Documentation
- [ ] Document all Tier-1.5 problems in config
- [ ] Implement TODO template generation
- [ ] Test codegen output for 0142, 0160

### Phase 4: Manual Solutions (Post-merge)
- [ ] Write solve() for 0142
- [ ] Write solve() for 0160
- [ ] Write solve() for 0138
- [ ] Write solve() for 0876

### Phase 5: Pattern Extraction (Future)
- [ ] Extract common patterns from Phase 4
- [ ] Add to codec.py
- [ ] Update tier classifications

---

## Acceptance Criteria

### Framework
- [ ] `config/problem-support.yaml` exists and is parseable
- [ ] `docs/contracts/problem-support-boundary.md` documents all tiers
- [ ] codegen reads tier from config before generation

### Tier-1
- [ ] `codegen new 2 --with-tests` auto-generates solve() with ListNode codec
- [ ] solve() correctly builds/encodes ListNode
- [ ] All Tier-1 tests pass

### Tier-1.5
- [ ] `codegen new 142 --with-tests` shows warning message
- [ ] Generated solve() contains TODO template
- [ ] .in/.out files are generated (tests can be created)
- [ ] Exit code is 0 (not a failure, just needs manual work)

### Documentation
- [ ] Tier classification is clear and documented
- [ ] Upgrade path (Tier-1.5 → Tier-1) is documented
- [ ] Anti-overengineering principle is stated

---

## Open Questions

1. **0876 classification**: Is it really Tier-1.5, or can value comparison work?
   - LeetCode displays `[3,4,5]` which is value-based
   - Might be Tier-1 if we just compare output values

2. **Config location**: `config/` at repo root, or inside a package?

3. **Codec location**: `runner/utils/codec.py` or separate `packages/codec/`?

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [problem-support-boundary.md](../../contracts/problem-support-boundary.md) | Canonical boundary reference |
| [test-file-format.md](../../contracts/test-file-format.md) | .in/.out format spec |
| [solution-contract.md](../../contracts/solution-contract.md) | solve() requirements |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-03 | Initial draft created from discussion |


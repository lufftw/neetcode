# Problem Support Boundary

> **Status**: Contract (Stable)  
> **Scope**: Defines system capabilities, boundaries, and hard rules for problem generation  
> **Philosophy**: Anti-overengineering — extract patterns from working solutions

This document is a **Contract**: it defines rules that MUST be followed. Changes require review.

For the living registry of per-problem configurations, see `config/problem-support.yaml`.

---

## Table of Contents

1. [Hard Rules](#1-hard-rules)
2. [Core Principles](#2-core-principles)
3. [Tier Classification](#3-tier-classification)
4. [Codec Mode Policy](#4-codec-mode-policy)
5. [Canonical Semantics](#5-canonical-semantics)
6. [I/O Format Registry](#6-io-format-registry)
7. [Representative Examples](#7-representative-examples)
8. [FAQ](#8-faq)

---

## 1. Hard Rules

These rules MUST NOT be violated.

### Rule 1: Handwritten Solution Protection

```
IF solutions/{id}_{slug}.py EXISTS AND is_handwritten:
    codegen MUST NOT overwrite without explicit --force flag
    codegen MUST warn user before any modification
```

**Rationale**: Protect human effort. Auto-generation should never destroy manual work.

### Rule 2: inline_reason Required for Inline Mode

```
IF codec_mode == "inline":
    inline_reason MUST be non-empty string
```

**Rationale**: Force documentation of why inline is needed. Prevents accidental inline.

### Rule 3: Tier-1.5 Generators Default Off

```
IF tier == "1.5":
    generators.random DEFAULT false
    generators.complexity DEFAULT false
```

**Rationale**: Tier-1.5 problems have complex semantics; random generation is risky.

### Rule 4: Canonical Semantics (see Section 5)

All codec implementations MUST follow canonical semantics. No exceptions.

---

## 2. Core Principles

### 2.1 Judge is Semantic-Free

Judge MUST NOT contain problem-specific logic.

| ✅ Judge Responsibilities | ❌ Judge MUST NOT |
|---------------------------|-------------------|
| Exact string comparison | Know about ListNode/TreeNode |
| Float tolerance (configurable) | Have `if problem_id == X` branches |
| Order-independent comparison (flagged) | Implement problem-specific comparison |

### 2.2 solve() is the Adapter

The `solve()` function adapts between:
- **Simple `.in/.out`** — Human-friendly, Example-derivable
- **LeetCode structures** — ListNode, TreeNode, cycles, shared nodes

```
.in/.out (simple)  ──→  solve()  ──→  Solution.method()
                         ↓
                    codec utilities
```

### 2.3 Solution = Self-Contained Executable Environment

A solution file contains everything needed for practice generation:

| Component | Purpose | Practice Generation |
|-----------|---------|---------------------|
| `solve()` | I/O translation | ✅ Keep as-is |
| `JUDGE_FUNC` | Comparison semantics | ✅ Keep as-is |
| `ListNode` etc. | Data structures | ✅ Keep as-is |
| `Solution.method()` | Algorithm | ❌ Clear body → TODO |

> **Practice generation is mechanical**: copy + clear method body.

### 2.4 Anti-Overengineering

> **Extract patterns from working solutions. Don't design universal systems upfront.**

Evolution path:
1. Write working `solve()` for complex problems
2. Identify common patterns
3. Extract into codec utilities
4. Update tier classification

---

## 3. Tier Classification

**Tier = Overall support level (not just generation)**

| Tier | Definition | Scaffold | Practice | Generator |
|------|------------|----------|----------|-----------|
| **"0"** | Signature → I/O derivable | ✅ auto | ✅ | ✅ |
| **"1"** | Needs codec, value-based I/O | ✅ auto | ✅ | ✅ |
| **"1.5"** | I/O semantics need problem knowledge | ✅ scaffold | ✅ | ⚠️ manual |
| **"2"** | Complex structures (future) | ❌ | ❌ | ❌ |

### Key Insights

- **Tier "0"/"1"/"1.5"**: ALL can practice (scaffold always generated)
- **Tier classification**: About GENERATION capability, not practice capability
- **Solution file is scaffold**: Does not mean "already solved"
- **Practice does not depend on existing solutions**

### Tier Format in Config

Use **string** format for tier values:

```yaml
tier: "1.5"  # Correct
tier: 1.5    # Avoid (YAML float parsing issues)
```

---

## 4. Codec Mode Policy

### 4.1 Two Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `import` | Import from `runner/utils/codec.py` | Standard codec, DRY |
| `inline` | Inline template into solution | Custom adapter, LeetCode-copyable |

### 4.2 Default

```yaml
defaults:
  codec_mode: import
```

### 4.3 When to Use Inline (Hard Rules)

`codec_mode: inline` is REQUIRED when:

| # | Condition | Example |
|---|-----------|---------|
| 1 | **Custom adapter needed** (semantic translation) | 0142: `node_to_index` |
| 2 | **Custom JUDGE_FUNC needed** | 0138: deep copy verification |
| 3 | **LeetCode copy-paste required** | User request |

### 4.4 Config Schema

```yaml
"0142":
  tier: "1.5"
  codec_mode: inline                    # Explicit (not inherited)
  inline_reason: "Output is node identity, needs node_to_index adapter"
  codec_hints: [build_list_with_cycle, node_to_index]
```

### 4.5 Import Path

When `codec_mode: import`:

```python
from runner.utils.codec import list_to_linkedlist, linkedlist_to_list
```

---

## 5. Canonical Semantics

These semantics are **non-negotiable**. All implementations MUST follow.

### 5.1 Index Base

| Item | Canonical Value |
|------|-----------------|
| `node_to_index` | **0-based** |
| `pos` (cycle position) | **0-based** |
| Array indices | **0-based** |

### 5.2 No-Result Representation

| Situation | Canonical Value | Type |
|-----------|-----------------|------|
| No cycle found | `-1` | `int` |
| No intersection | `-1` | `int` |
| Null node | `-1` or `null` (context-dependent) | `int` or `null` |

### 5.3 Boolean Output

| Value | Canonical Format |
|-------|------------------|
| True | `true` (JSON lowercase) |
| False | `false` (JSON lowercase) |

---

## 6. I/O Format Registry

Config uses `io_format` keys to reference these definitions.

### 6.1 Tier-1 Formats (Value-Based)

| io_format | Input | Output |
|-----------|-------|--------|
| `list_to_list` | `[values]` | `[values]` |
| `two_lists_to_list` | `[list1]` `[list2]` | `[values]` |
| `list_of_lists_to_list` | `[[l1],[l2],...]` | `[values]` |
| `list_int_to_list` | `[values]` `int` | `[values]` |
| `list_with_pos_to_bool` | `[values]` `pos` | `true/false` |

### 6.2 Tier-1.5 Formats (Semantic)

| io_format | Input | Output | Semantic |
|-----------|-------|--------|----------|
| `list_with_pos_to_node_index` | `[values]` `pos` | `index` or `-1` | Node identity |
| `two_lists_with_skips_to_node_value` | `[listA]` `[listB]` `skipA` `skipB` | `value` or `-1` | Shared node |
| `random_pointer_list` | `[[val,rand],...]` | `[[val,rand],...]` | Deep copy |

---

## 7. Representative Examples

These examples illustrate how the rules apply. For the complete registry, see `config/problem-support.yaml`.

### 7.1 Tier-1.5 Example: 0142 Linked List Cycle II

| Aspect | Detail |
|--------|--------|
| **Tier** | `"1.5"` |
| **codec_mode** | `inline` |
| **inline_reason** | Output is node identity (cycle entry), needs `node_to_index` |
| **io_format** | `list_with_pos_to_node_index` |

**.in/.out**:
```
[3,2,0,-4]
1

# .out
1
```

### 7.2 Tier-1.5 Example: 0138 Copy List with Random Pointer

| Aspect | Detail |
|--------|--------|
| **Tier** | `"1.5"` |
| **codec_mode** | `inline` |
| **inline_reason** | Multi-pointer structure + deep copy verification |
| **io_format** | `random_pointer_list` |

**.in/.out**:
```
[[7,null],[13,0],[11,4],[10,2],[1,0]]

# .out
[[7,null],[13,0],[11,4],[10,2],[1,0]]
```

---

## 8. FAQ

### Q: Why not use a universal graph format?

**A**: Premature abstraction. We extract patterns from working solutions, not design upfront.

### Q: Can I write custom solve() for a Tier-0 problem?

**A**: Yes. Tier defines what the system CAN auto-generate, not what you MUST use.

### Q: How do I know if a problem is Tier-1.5?

**A**: Ask: "Can the I/O format be derived from signature and values alone?"
- Yes → Tier-0 or Tier-1
- No (needs problem knowledge) → Tier-1.5

### Q: What if codec_mode is not specified for Tier-1.5?

**A**: Config validation SHOULD warn. Tier-1.5 typically needs `inline`, and `inline_reason` is required.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `config/problem-support.yaml` | Living registry of per-problem config |
| [test-file-format.md](./test-file-format.md) | .in/.out format specification |
| [solution-contract.md](./solution-contract.md) | solve() function requirements |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-03 | Initial version |
| 2026-01-03 | Refactored as Contract; added Hard Rules, Canonical Semantics |

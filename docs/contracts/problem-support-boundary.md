# Problem Support Boundary

> **Status**: Canonical Reference  
> **Scope**: Defines system capabilities and boundaries for auto-generation  
> **Philosophy**: Anti-overengineering — extract patterns from working solutions

This document defines what the system can and cannot auto-generate, and provides clear guidance for problems that require manual implementation.

---

## Table of Contents

1. [Core Principles](#1-core-principles)
2. [Tier Classification](#2-tier-classification)
3. [I/O Format Registry](#3-io-format-registry)
4. [Tier-1.5 Problem Registry](#4-tier-15-problem-registry)
5. [Tier-1 Problem Notes](#5-tier-1-problem-notes)
6. [Codec Utilities](#6-codec-utilities)
7. [Evolution Strategy](#7-evolution-strategy)
8. [FAQ](#8-faq)

---

## 1. Core Principles

### 1.1 Judge is Semantic-Free

Judge MUST NOT contain problem-specific logic.

| ✅ Judge Responsibilities | ❌ Judge MUST NOT |
|---------------------------|-------------------|
| Exact string comparison | Know about ListNode/TreeNode |
| Float tolerance (configurable) | Have `if problem_id == X` branches |
| Order-independent comparison (flagged) | Implement problem-specific comparison |

**Rationale**: If judge knows problem semantics, it becomes unmaintainable:
```python
# ❌ This is the path to madness
if problem_id == 142:
    compare_cycle_entry()
elif problem_id == 160:
    compare_shared_node()
```

### 1.2 solve() is the Adapter

For problems where I/O semantics cannot be derived from signature alone, the `solve()` function serves as the **adapter** between:

- **Simple `.in/.out` format** — Human-friendly, Example-derivable
- **LeetCode structures** — ListNode, TreeNode, cycles, shared nodes

```
.in/.out (simple)  ──→  solve()  ──→  Solution class
                         ↓
                    codec utilities
```

### 1.3 Anti-Overengineering

> **Extract patterns from working solutions. Don't design universal systems upfront.**

The evolution path:
1. Write working `solve()` for complex problems
2. Identify common patterns across solutions
3. Extract patterns into codec utilities
4. Update tier classification

---

## 2. Tier Classification

| Tier | Definition | Auto solve()? | Auto tests? | Example |
|------|------------|---------------|-------------|---------|
| **Tier-0** | Signature → I/O fully derivable | ✅ | ✅ | Two Sum |
| **Tier-1** | Needs codec, value-based I/O | ✅ | ✅ | Add Two Numbers |
| **Tier-1.5** | I/O semantics require problem knowledge | ❌ | ✅ | Cycle II |
| **Tier-2** | Complex structures (future) | ❌ | ❌ | Clone Graph |

### 2.1 Tier-0: Fully Derivable

The I/O format can be completely derived from the method signature.

**Supported types**:
- Scalars: `int`, `float`, `bool`, `str`
- Arrays: `List[int]`, `List[str]`, `List[List[int]]`
- No pointer structures

**Example**: Two Sum
```python
def twoSum(nums: List[int], target: int) -> List[int]:
```
→ Input: array + int, Output: array

### 2.2 Tier-1: Value-Based I/O

Requires codec to build/serialize structures, but I/O is purely value-based.

**Supported types**:
- `ListNode` (no cycles, value comparison)
- `TreeNode` (level-order, value comparison)

**Example**: Add Two Numbers
```python
def addTwoNumbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
```
→ Input: two value arrays, Output: value array

### 2.3 Tier-1.5: Problem-Specific Semantics

> **Tier-1.5 = I/O 語義無法由 signature + value alone 決定**

This is NOT a system failure — it's an inherent property of the problem.

**Characteristics**:
- Output is node **identity** (not value)
- Input requires auxiliary construction parameters
- Comparison requires problem knowledge

**Examples**: 0142, 0160, 0138, 0876

### 2.4 Tier-2: Future Work

Complex structures not yet planned for support.

**Examples**: Graph clone, serialize/deserialize, multi-level lists

---

## 3. I/O Format Registry

Config uses `io_format` keys to reference these canonical definitions.
This prevents config drift and keeps format rules in one place.

### 3.1 Tier-1 Formats (Value-Based I/O)

| io_format | Input | Output | Example Problem |
|-----------|-------|--------|-----------------|
| `list_to_list` | `[values]` | `[values]` | 0002, 0206, 0876 |
| `two_lists_to_list` | `[list1]` `[list2]` | `[values]` | 0021 |
| `list_of_lists_to_list` | `[[l1],[l2],...]` | `[values]` | 0023 |
| `list_int_to_list` | `[values]` `int` | `[values]` | 0025 |
| `list_with_pos__out_bool` | `[values]` `pos` | `true/false` | 0141 |

### 3.2 Tier-1.5 Formats (Semantic I/O)

| io_format | Input | Output | Semantic |
|-----------|-------|--------|----------|
| `list_with_pos__out_node_index` | `[values]` `pos` | `index` or `null` | Node identity |
| `two_lists_with_skips__out_node_value` | `[listA]` `[listB]` `skipA` `skipB` | `value` or `null` | Shared node |
| `random_pointer_list` | `[[val,rand],...]` | `[[val,rand],...]` | Deep copy |

---

## 4. Tier-1.5 Problem Registry

> **Key Insight**: Tier-1.5 is defined by **output semantic needing problem knowledge**,  
> NOT by "input needs special construction".

### 0142 — Linked List Cycle II

| Aspect | Detail |
|--------|--------|
| **Reason** | Output is node identity (cycle entry point) |
| **io_format** | `list_with_pos__out_node_index` |
| **output_semantic** | `node_ref_index` |

**.in/.out**:
```
[3,2,0,-4]
1

# .out
1
```

**Comparison**: Check if returned node index matches expected.

---

### 0160 — Intersection of Two Linked Lists

| Aspect | Detail |
|--------|--------|
| **Reason** | Output is shared node identity |
| **io_format** | `two_lists_with_skips__out_node_value` |
| **output_semantic** | `node_ref_value` |

**.in/.out** (matches LeetCode Example format):
```
[4,1,8,4,5]
[5,6,1,8,4,5]
2
3

# .out
8
```

**Comparison**: Check if returned node's value matches, or `null`.

---

### 0138 — Copy List with Random Pointer

| Aspect | Detail |
|--------|--------|
| **Reason** | Multi-pointer structure (next + random) |
| **io_format** | `random_pointer_list` |

**.in/.out**:
```
[[7,null],[13,0],[11,4],[10,2],[1,0]]

# .out
[[7,null],[13,0],[11,4],[10,2],[1,0]]
```

**Comparison**: Deep copy structure matches.

---

## 5. Tier-1 Problem Notes

These problems are **fully auto-generatable** with codec support.

### 0141 — Linked List Cycle (Tier-1, NOT Tier-1.5)

| Aspect | Detail |
|--------|--------|
| **io_format** | `list_with_pos__out_bool` |
| **Why Tier-1** | Output is `bool` (value-based comparison) |

Input needs cycle construction, but output comparison is trivial.

### 0876 — Middle of the Linked List (Tier-1)

| Aspect | Detail |
|--------|--------|
| **io_format** | `list_to_list` |
| **Why Tier-1** | Output is value array, not node identity |

LeetCode displays `[3,4,5]` which is the values from middle node onward.
Value comparison is sufficient.

---

## 6. Codec Utilities

### 4.1 Available (Tier-1)

| Function | Signature | Purpose |
|----------|-----------|---------|
| `build_list` | `(List[int]) → ListNode` | Array to linked list |
| `list_to_values` | `(ListNode) → List[int]` | Linked list to array |
| `build_tree` | `(List[Optional[int]]) → TreeNode` | Level-order to tree |
| `tree_to_values` | `(TreeNode) → List[Optional[int]]` | Tree to level-order |

### 4.2 To Be Extracted (Tier-1.5)

These will be added as manual solutions are written:

| Function | Source Problem | Status |
|----------|----------------|--------|
| `build_list_with_cycle` | 0141, 0142 | 🔜 Planned |
| `build_intersecting_lists` | 0160 | 🔜 Planned |
| `build_random_pointer_list` | 0138 | 🔜 Planned |
| `encode_random_pointer_list` | 0138 | 🔜 Planned |

---

## 7. Evolution Strategy

### 5.1 Adding New Problem Support

```
Step 1: Classify the problem (Tier-0/1/1.5/2)
Step 2: If Tier-1.5, add to config/problem-support.yaml
Step 3: Write manual solve() with appropriate codec
Step 4: After pattern emerges, extract to codec utilities
Step 5: Update tier classification if now auto-generatable
```

### 5.2 Promoting Tier-1.5 → Tier-1

When a pattern becomes common enough:

1. Ensure codec utility exists and is tested
2. Update `solve_generator.py` to use the codec
3. Move problem from `tier1_5` to `tier1` in config
4. Update this document

### 5.3 Config File: `config/problem-support.yaml`

```yaml
tier1:
  - "0002"
  - "0021"

tier1_5:
  "0142":
    reason: "Output is node identity"
    codec_hints: ["build_list_with_cycle"]
```

---

## 8. FAQ

### Q: Why not use a universal graph format for everything?

**A**: Premature abstraction. We don't know what patterns will emerge until we write real solutions. A universal format adds complexity without proven benefit.

### Q: Can I write my own solve() for a Tier-0 problem?

**A**: Yes. The tier system defines what the system **can** auto-generate, not what you **must** use. Custom `solve()` always takes precedence.

### Q: How do I know if a problem is Tier-1.5?

**A**: Ask: "Can the I/O format be derived from the signature and values alone?"
- If yes → Tier-0 or Tier-1
- If no (needs problem-specific knowledge) → Tier-1.5

### Q: What if my solve() pattern is useful for other problems?

**A**: Great! Extract it to `runner/utils/codec.py` and update this document.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [test-file-format.md](./test-file-format.md) | .in/.out format specification |
| [solution-contract.md](./solution-contract.md) | solve() function requirements |
| [generator-contract.md](./generator-contract.md) | Generator requirements |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-03 | Initial version |


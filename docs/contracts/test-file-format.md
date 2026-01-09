# Test File Format Specification

> **Status**: Canonical Reference  
> **Created**: 2026-01-02  
> **Related**: [migration-plan.md](../in-progress/new-problem-tests-autogen/migration-plan.md)

This document defines the **data contract** for `.in` and `.out` test files.

---

## Design Principles

1. **Human-readable first**: Files should be reviewable without running code
2. **Signature-aligned**: Input mirrors function parameters
3. **Self-contained**: Output contains all verification data
4. **Runner-agnostic**: Format doesn't dictate validation logic

---

## Input Format (`.in` files)

### Rule

```
One line per parameter, following function signature order.
Each line contains a JSON-serializable value.
```

### Example

```python
def removeElement(self, nums: List[int], val: int) -> int:
```

```
# 001.in
[3,2,2,3]    ← nums (param 1)
3            ← val (param 2)
```

### Why This Format

| Benefit | Explanation |
|---------|-------------|
| Decoupled from names | Runner uses positional args, doesn't parse `nums = ...` |
| Diff-friendly | One parameter per line = easy to spot changes |
| Scalable | Works for any number of parameters |
| Simple | `lines[i]` → `json.loads()` → argument |

### Non-examples

❌ **Single JSON object**
```
{"nums": [3,2,2,3], "val": 3}
```
*Reason: Couples format to parameter names*

❌ **Concatenated line**
```
[3,2,2,3] 3
```
*Reason: Loses structural clarity, ambiguous parsing*

❌ **Variable assignment**
```
nums = [3,2,2,3]
val = 3
```
*Reason: Requires parsing variable names*

---

## Output Format (`.out` files)

### Rule

```
One line per validation value, in verification order.
First line is always the return value (if any).
Subsequent lines represent modified state (if needed).
```

### Category A: Simple Return Value

For problems that only return a value without side effects.

```python
def twoSum(self, nums: List[int], target: int) -> List[int]:
```

```
# .out
[0,1]
```

### Category B: Multi-output Validation

For problems with **in-place modification + return value**.

LeetCode validates both:
1. The return value is correct
2. The modified array is correct

Both must be specified for human review.

```python
def removeElement(self, nums: List[int], val: int) -> int:
```

LeetCode shows: `Output: 2, nums = [2,2,_,_]`

```
# .out
2          # return value (k)
[2,2]      # nums[:k] for verification
```

### Category C: Custom Judge Required

Same format as A or B, but runner uses `JUDGE_FUNC` for semantic comparison.

**When to use:**
- Order-independent results (e.g., permutations)
- Floating-point comparison with tolerance
- Multiple valid answers

```python
def threeSum(self, nums: List[int]) -> List[List[int]]:
```

```
# .out (any permutation is valid)
[[-1,-1,2],[-1,0,1]]
```

---

## Problem Classification

| Category | Description | Output Lines | Example |
|----------|-------------|--------------|---------|
| A | Simple return value | 1 | Two Sum |
| B | In-place + return value | 2+ | Remove Element |
| C | Custom judge needed | 1 or 2+ | 3Sum |

### Category B Problems (Multi-output)

| Problem | Return | Verification |
|---------|--------|--------------|
| 0026_remove_duplicates | k | nums[:k] |
| 0027_remove_element | k | nums[:k] |
| 0080_remove_duplicates_ii | k | nums[:k] |

### Category A Problems (Single-output, in-place no return)

| Problem | Output |
|---------|--------|
| 0075_sort_colors | nums |
| 0088_merge_sorted_array | nums1 |
| 0283_move_zeroes | nums |

---

## Canonical Format Rules

### JSON Literal Requirements

| Type | Format | Example |
|------|--------|---------|
| Integer | JSON number | `42` |
| Float | JSON number | `3.14159` |
| Boolean | JSON lowercase | `true`, `false` |
| String | JSON double-quoted | `"abc"` |
| Array (1D) | JSON array, no spaces | `[2,7,11,15]` |
| Array (2D) | JSON array, single line | `[[1,2],[3,4]]` |
| Null | JSON null | `null` |

### Normalization

| Rule | Specification |
|------|---------------|
| Quotes | Always `"`, never `'` |
| Spaces | No spaces after `:` or `,` |
| Booleans | `true`/`false` (not `True`/`False`) |
| Line endings | `\n` (parser tolerates `\r\n`) |
| Trailing newline | Optional |
| Empty files | Not allowed |

---

## Anti-patterns

### ❌ Don't merge return + side effects into JSON

```
# Bad
[2,[2,2]]
```

**Reason:** Invents a new format per problem. Not human-readable.

### ❌ Don't omit validation data

```
# Bad (for Category B problems)
2
```

**Reason:** Cannot verify correctness without running code.

### ❌ Don't use comments for data

```
# Bad
2  # k=2, array=[2,2]
```

**Reason:** Comments aren't machine-parseable.

### ❌ Don't use Python format

```
# Bad
[0, 1]     ← has spaces
True       ← Python boolean
'abc'      ← single quotes
```

---

## Edge Cases

### Empty Arrays

```
# .in
[]
2

# .out (Category B)
0
[]
```

### Single Element

```
# .in
[1]
1

# .out (Category B)
0
[]
```

### Empty String

```
# .in
""
"a"

# .out
false
```

---

## Validation

### Gate 0: Format Validation

All test files must pass:

```bash
python -m codegen check --all
```

Checks:
- Each line is valid JSON
- No empty files
- No BOM
- Correct line endings

### Gate 1: Behavioral Validation

All tests must pass with handwritten `solve()`:

```bash
python runner/test_runner.py --all
```

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [specification.md](../in-progress/new-problem-tests-autogen/specification.md) | Feature specification |
| [migration-plan.md](../in-progress/new-problem-tests-autogen/migration-plan.md) | Migration execution guide |
| [solution-contract.md](./solution-contract.md) | solve() function requirements |
| [generator-contract.md](./generator-contract.md) | Generator output requirements |


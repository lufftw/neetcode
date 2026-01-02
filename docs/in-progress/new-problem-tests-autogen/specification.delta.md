# Specification Delta: Migration Plan Alignment

> This document records the deltas between the current `specification.md`
> and the intended updates required for the migration.
> All changes described here are expected to be merged back into
> `specification.md` after implementation is completed.

**Created**: 2026-01-02  
**Status**: 📋 Pending merge to specification.md

---

## Delta 1: Tier Classification Update

### Current (specification.md)

```
Tier 0: int, str, List[int], List[str]
Tier 1: List[List[int]] (2D array)
Tier 2: LinkedList, TreeNode
```

### Updated

```
Tier-0 (Blocking):    int, bool, str, List[int], List[str], List[List[int]], List[List[str]]
Tier-1 (Non-blocking): ListNode, TreeNode
```

### Rationale

- 2D Array (`List[List[T]]`) moved to Tier-0 because:
  - LeetCode extensively uses 2D arrays (matrix / board problems)
  - Canonical format already supports single-line JSON `[[1,2],[3,4]]`
  - Parser/codec complexity is low
  - If left in Tier-1, Gate 2 loses practical value
- Tier-2 removed to avoid tier inflation

### Affected Sections

- `## IO Schema` → Supported Types table
- `## Future Discussion Topics` → solve() 自動生成範圍

---

## Delta 2: String Format Clarification

### Current (specification.md)

```
字串：`"abc"` 或直接 `abc`（視題目而定）
```

### Updated

```
字串：一律使用 JSON double-quoted `"abc"`
Unquoted strings are not supported in canonical format.
```

### Rationale

- `abc` is not valid JSON
- Requires context to determine if value is a string
- Breaks "machine-first" canonical principle
- LeetCode examples already use `"abc"` visually

### Affected Sections

- `## Canonical Format Decision` → Canonical 格式規範 → Input (.in)

---

## Delta 3: Exit Code 2 Clarification

### Current (specification.md)

```
| 2 | `--strict-tests` enabled + 0 tests generated |
```

### Updated

```
| 2 | Strict-mode semantic failure |

Exit code 2 indicates the command completed execution, but a required 
condition was not met. This may occur in multiple scenarios:
- `--strict-tests` enabled and 0 tests generated
- Type unsupported for solve() generation (when using `--solve-mode infer`)

The specific reason is always reported in stderr.
```

### Rationale

- Both scenarios represent "semantic failure" (command ran, but strict condition failed)
- Avoids exit code explosion
- CI/script handling remains simple
- stderr message provides detailed distinction

### Affected Sections

- `## Python CLI (Source of Truth)` → Exit codes table

---

## Delta 4: Add Missing CLI Flags Documentation

### Current (specification.md)

Flags `--tests-only` and `--strict-tests` are mentioned but marked as "Pending".

### Updated

Add to `## Python CLI (Source of Truth)`:

```markdown
| `--tests-only`    | Skip solution, generate tests only |
| `--strict-tests`  | Exit code 2 if 0 tests generated |
| `--format`        | Test format (default: `raw`, reserved for future) |
```

Add note:

```markdown
**Note on `--format raw`:**
This flag is reserved for future format variations. 
Currently only `raw` is supported and is the default.
```

### Affected Sections

- `## Python CLI (Source of Truth)` → Arguments table
- `## Implementation Progress` → Pending section (remove these items)

---

## Delta 5: CLI Command Path Standardization

### Current (specification.md)

Already correct:
```bash
python -m codegen new <id>
```

### Verification

`migration-plan.md` incorrectly used `python -m packages.codegen`.
This delta confirms specification.md is the source of truth.

No changes needed to specification.md.

---

## Summary Table

| Item | specification.md Change Required |
|------|----------------------------------|
| Tier classification | ✅ Update Tier-0/1 definition |
| String format | ✅ Clarify always double-quoted |
| Exit code 2 | ✅ Expand definition |
| CLI flags | ✅ Document --tests-only, --strict-tests |
| CLI command path | ❌ Already correct |

---

## Merge Checklist

When merging back to specification.md:

- [ ] Update `## IO Schema` → move 2D array to Tier-0
- [ ] Update `## Canonical Format Decision` → string always quoted
- [ ] Update `## Python CLI` → exit code 2 expanded meaning
- [ ] Update `## Python CLI` → add flag documentation
- [ ] Update `## Implementation Progress` → mark flags as complete
- [ ] Remove `## Future Discussion Topics` → Tier-2 references
- [ ] Add cross-reference to `migration-plan.md`

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `specification.md` | Source of truth (to be updated) |
| `migration-plan.md` | Execution guide (aligned with this delta) |


# Migration Plan: Canonical Format Upgrade

> **Status**: 📝 Draft  
> **Branch**: `feat/new-problem-tests-autogen`  
> **Created**: 2026-01-02  
> **Last Updated**: 2026-01-02

## Overview

[To be written - 為什麼要遷移、目標、範圍]

---

## Canonical Format Specification

[To be written - 標準格式定義]

---

## Verification Gates

Migration success is defined by passing **Gate 0 + Gate 1 + Gate 3**.  
Gate 2 is tracked separately for coverage expansion.

### Quick Reference

| Gate | Name | Type | Purpose |
|------|------|------|---------|
| **Gate 0** | Format & Integrity | 🔴 Blocking | Test files parse correctly under canonical format |
| **Gate 1** | Regression | 🔴 Blocking | Handwritten `solve()` all pass on canonical tests |
| **Gate 2** | Coverage | 🟡 Non-blocking | Generated `solve()` matches handwritten oracle |
| **Gate 3** | E2E Workflow | 🔴 Blocking | `codegen new --with-tests` outputs are runnable |

### Gate Dependencies

```
Gate 0 ──→ Gate 1 ──→ Gate 3
              │
              └── Gate 2 (independent, non-blocking)
```

- Gates must be re-run if any upstream gate inputs change.
- Downstream gates are invalidated by upstream failures.

### Execution Rules

| Situation | Required Action |
|-----------|-----------------|
| Gate 0 rerun with changes | Re-run Gate 1 and Gate 3 |
| Gate 1 fails after passing Gate 0 | Do not proceed to Gate 3 |
| Gate 2 updates | No gate invalidation |

**Principles:**
- Each gate assumes a stable input scope. Unrelated changes should not be mixed during gate execution.
- When a gate fails, fixes should be minimal and scoped to the failure cause.

### Responsibility

| Gate | Executor |
|------|----------|
| Gate 0–1 | Migration executor |
| Gate 2 | Migration executor / contributor |
| Gate 3 | Migration executor |

CI automation (when enabled) does not replace manual responsibility.

---

### Gate 0: Format & Integrity

**Goal:** All test files can be parsed by the canonical parser.

**Principle:** Block only issues that affect the parser. Style issues do not block.

#### Checks

| Check | Condition | Severity |
|-------|-----------|----------|
| Empty file | File has 0 bytes | ❌ Hard fail |
| BOM | File contains BOM header | ❌ Hard fail |
| Line endings | `\r\n` found | ⚠️ Auto-convert to `\n` |
| Parse error | Cannot parse as canonical format | ❌ Hard fail |
| Trailing whitespace | Lines end with spaces | ✅ Ignored (style) |

#### Command

```bash
python -m packages.codegen validate-tests --all
```

#### Pass Condition

- Exit code 0
- All `.in` / `.out` files parse without error

#### Failure Handling

**Stop immediately.** Fix format/integrity issues before proceeding.

Example error output:
```
❌ tests/0001_two_sum_1.in: Parse error at line 1: unexpected character
❌ tests/0015_3sum_2.out: Empty file
```

---

### Gate 1: Regression

**Goal:** Migration does not break existing behavior.

**Principle:** This is behavioral regression, not a test framework upgrade. Only run handwritten `solve()`.

#### Command

```bash
python runner/test_runner.py --all
```

#### Pass Condition

- Exit code 0
- All problems with handwritten `solve()` pass on canonical tests

#### Cross-Platform Notes

- Line endings are normalized to `\n` during parsing (tolerates `\r\n` input)
- Handled by `.gitattributes` and parser normalization

#### Failure Handling

**Block migration.** Regression must be resolved before proceeding to Gate 3.

---

### Gate 2: solve_generator Coverage

**Goal:** Validate that `solve_generator` can produce correct `solve()` functions by comparing against handwritten oracles.

**Principle:** This gate expands coverage incrementally. It does not block the migration mainline.

#### Type Tiers

| Tier | Types | Target | Status |
|------|-------|--------|--------|
| **Tier-0** | `int`, `str`, `bool`, `List[int]`, `List[str]`, `List[List[int]]` | 100% | 🔴 Blocking |
| **Tier-1** | `ListNode`, `TreeNode` | 0% initial | 🟡 Non-blocking |

#### Oracle Verification Flow

```
For each problem:
  1. Run handwritten solve() → expected output
  2. Run generated solve()  → actual output
  3. Compare: exact match OR semantic equivalence (with comparator)
  4. Record result in capability report
```

#### Coverage Reporting

The capability report should include:

| Field | Description |
|-------|-------------|
| `problem_id` | e.g., `0001_two_sum` |
| `tier` | Tier-0 / Tier-1 |
| `status` | `pass` / `fail` / `unsupported` |
| `reason` | If failed: `type_unsupported`, `comparator_missing`, `parse_mismatch`, `value_diff` |

Example report:
```json
{
  "summary": { "pass": 38, "fail": 0, "unsupported": 7 },
  "details": [
    { "problem_id": "0001_two_sum", "tier": "tier0", "status": "pass" },
    { "problem_id": "0002_add_two_numbers", "tier": "tier1", "status": "unsupported", "reason": "type_unsupported: ListNode" }
  ]
}
```

#### Failure Handling

**Record and continue.** Generate capability report, do not block migration.

---

### Gate 3: E2E New Workflow

**Goal:** The new problem workflow produces runnable outputs out-of-the-box.

**Principle:** This is new feature acceptance. No sampling — test all supported types.

#### Validation Flow

```bash
# For each supported problem type:
python -m packages.codegen new <id> --with-tests
python runner/test_runner.py <id>
```

#### Exit Code Specification

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success: solution and tests created, runnable |
| 1 | Hard failure: metadata fetch failed |
| 2 | Partial: tests generated but type unsupported for solve() |

For unsupported types, `codegen` must:
- Exit with non-zero code
- Print explicit error message
- **Never** produce silent broken output

#### Example Output

**Success:**
```
✅ Created: solutions/0001_two_sum.py
✅ Created: tests/0001_two_sum_1.in
✅ Created: tests/0001_two_sum_1.out
✅ Tests runnable: python runner/test_runner.py 0001_two_sum
```

**Unsupported type:**
```
⚠️  Created: solutions/0002_add_two_numbers.py
⚠️  Type unsupported for auto-generated solve(): ListNode
⚠️  Manual solve() implementation required.
Exit code: 2
```

#### Failure Handling

**Block release of new workflow.** Existing system may continue operating.

---

### Automation Strategy

**Phase 1: Manual Execution**
- Gate 0, Gate 1, Gate 3 run manually by migration executor
- Gate 2 run on-demand for coverage expansion

**Phase 2: CI Integration (after stabilization)**
- Gate 0 + Gate 1 + Gate 3: CI runs on PR, blocks merge on failure
- Gate 2: CI generates report only, does not fail build

---

## Execution Phases

[To be written - 按順序的執行步驟]

---

## Per-Folder Migration Guide

### tests/ Migration

[To be written]

### solutions/ Migration

[To be written]

### generators/ Migration

[To be written]

---

## Tools & Commands

[To be written - 可用的工具和指令]

---

## Rollback & Recovery

[To be written - 備份和回滾策略]

---

## Open Questions / Future Work

[To be written - 待解決問題]

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-02 | Initial draft created |


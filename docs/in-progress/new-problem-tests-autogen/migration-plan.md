# Migration Plan: Canonical Format Upgrade

> **Status**: ✅ Gate 1 + Phase 5 Passed  
> **Branch**: `feat/new-problem-tests-autogen`  
> **Created**: 2026-01-02  
> **Last Updated**: 2026-01-02  
> **Related**: [specification.md](./specification.md) · [specification.delta.md](./specification.delta.md)

## Gate 1 Completion Summary

**Date**: 2026-01-02

| Metric | Result |
|--------|--------|
| Problems Passing | 40/45 |
| LinkedList (OUT_OF_SCOPE) | 5 |
| Gate 0 | ✅ All test files parse |
| Gate 1 | ✅ All in-scope solve() pass |

## Phase 5 Completion Summary

**Date**: 2026-01-02

| Test Type | Result | Notes |
|-----------|--------|-------|
| Static tests | 40/45 ✅ | 5 LinkedList OUT_OF_SCOPE |
| Generated tests | 38/45 ✅ | 5 skipped + 2 LinkedList failures |
| Combined | 118/135 ✅ | All in-scope passing |

### Generator Updates

All 38 in-scope generators converted to canonical JSON format:

**Pattern Applied:**
```python
# Before (old format)
edge_cases = [
    "3 2 2 3\n3",        # Space-separated string
]
for edge in edge_cases:
    yield json.dumps(edge)  # Wrong: json.dumps on string

# After (canonical JSON)
edge_cases = [
    ([3, 2, 2, 3], 3),   # Data structure tuple
]
for nums, val in edge_cases:
    yield f"{json.dumps(nums, separators=(',', ':'))}\n{val}"
```

### Key Changes
- Converted all `edge_cases` from hardcoded strings to data structures
- Used `json.dumps(separators=(',', ':'))` for array serialization
- Fixed `import json` placement (moved outside docstrings)
- Ensured 1 line = 1 parameter following function signature

### OUT_OF_SCOPE Problems (Tier-1 Future Work)

These LinkedList problems require special serialization support and are deferred:

| Problem | Reason |
|---------|--------|
| 0002_add_two_numbers | ListNode I/O |
| 0021_merge_two_sorted_lists | ListNode I/O |
| 0023_merge_k_sorted_lists | ListNode I/O |
| 0141_linked_list_cycle | ListNode I/O |
| 0142_linked_list_cycle_ii | ListNode I/O |

### Post-Gate 1 Format Review (需檢查)

以下問題需要確認 `.in/.out` 格式符合新規則：

#### Input Format: 1 line = 1 parameter (signature order)
```
def removeElement(self, nums: List[int], val: int) -> int:

# .in
[3,2,2,3]  ← nums (param 1)
3          ← val (param 2)
```

#### Output Format: Multi-output validation problems
```
# .out (for in-place with return value)
2          ← return value (k)
[2,2]      ← nums[:k] for verification
```

| Problem | Category | Status |
|---------|----------|--------|
| 0026_remove_duplicates | Multi-output | ✅ 已更新 |
| 0027_remove_element | Multi-output | ✅ 已更新 |
| 0080_remove_duplicates_ii | Multi-output | ✅ 已更新 |
| 0075_sort_colors | Single-output (no return) | ✅ OK |
| 0088_merge_sorted_array | Single-output (no return) | ✅ OK |
| 0283_move_zeroes | Single-output (no return) | ✅ OK |

---

## Overview

### Why This Migration?

| Driver | Problem | Solution |
|--------|---------|----------|
| **Technical Debt** | Test files use inconsistent formats (comma-separated, space-separated, mixed) | Canonical JSON literal format |
| **New Feature** | `codegen new --with-tests` needs predictable I/O | Unified format specification |
| **Maintainability** | Each generator/solve() invents its own format | Single source of truth |

### Goals

1. **Canonical Format** — All `.in/.out` files use JSON literal
2. **Regression Safety** — Existing handwritten `solve()` continues to work
3. **New Workflow** — `codegen new --with-tests` produces runnable tests
4. **Extensibility** — Foundation for LinkedList/TreeNode support (future)

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| 45 existing problems | New problem additions |
| tests/, solutions/, generators/ | runner/ internal refactoring |
| Tier-0 types (int, str, List) | Tier-1 types (ListNode, TreeNode) |
| Format migration | Algorithm changes |

### Success Definition

Migration is complete when:

- ✅ **Gate 0**: All test files parse under canonical format
- ✅ **Gate 1**: All handwritten `solve()` pass on canonical tests
- ✅ **Gate 3**: `codegen new --with-tests` outputs are runnable
- 🟡 **Gate 2**: Coverage tracked, Tier-0 at 100% (non-blocking for mainline)

### Execution Summary

```
Phase 1: tests/ canonicalization     → Gate 0
Phase 2: Infrastructure update       → Gate 1
Phase 3: solutions/ compatibility    → Gate 1
Phase 4: codegen E2E workflow        → Gate 3
Phase 5: generators/ update          → (validation)
Phase 6: solve_generator expansion   → Gate 2
```

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Format | JSON literal | 100% parseable, no custom rules |
| 2D Arrays | Single line `[[1,2],[3,4]]` | JSON-native, diff-stable |
| solve() strategy | Keep handwritten as Oracle | Validate generator against known-good |
| LinkedList/TreeNode | Future work | Avoid scope explosion |
| Backup | .bak files + Git | Belt and suspenders |

---

## Canonical Format Specification

This section defines the **data contract** for `.in` and `.out` files.

> **Canonical ≠ Human Pretty**  
> Canonical is a machine-first format for stable parsing, not for display.

### Design Principles

1. **100% JSON Literal** — Every line is valid JSON
2. **One value per line** — Parameters separated by newlines
3. **No variable names** — Strip `nums = `, keep only values
4. **No invented formats** — Match LeetCode's visual representation

### Quick Reference

| Type | Canonical Format | Example |
|------|------------------|---------|
| Integer | JSON number | `42` |
| Float | JSON number | `3.14159` |
| Boolean | JSON lowercase | `true`, `false` |
| String | JSON double-quoted (always) | `"abcabcbb"` |
| Array (1D) | JSON array, no spaces | `[2,7,11,15]` |
| Array (2D) | JSON array, single line | `[[1,2],[3,4]]` |
| Null | JSON null | `null` |
| LinkedList | ⚠️ Future work | — |
| TreeNode | ⚠️ Future work | — |

---

### Input Format (`.in`)

Each parameter occupies **one line**, in the order defined by the LeetCode method signature.

#### Example: Two Sum

LeetCode Example:
```
Input: nums = [2,7,11,15], target = 9
```

Canonical `.in`:
```
[2,7,11,15]
9
```

#### Example: Permutation in String

LeetCode Example:
```
Input: s1 = "ab", s2 = "eidbaooo"
```

Canonical `.in`:
```
"ab"
"eidbaooo"
```

#### Example: Word Search (2D Array)

LeetCode Example:
```
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
```

Canonical `.in`:
```
[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
"ABCCED"
```

---

### Output Format (`.out`)

Output format depends on the problem category.

#### Category A: Simple Return Value

Single line JSON literal matching the method return type.

| Return Type | Canonical `.out` |
|-------------|------------------|
| `int` | `3` |
| `bool` | `true` |
| `str` | `"abc"` |
| `List[int]` | `[0,1]` |
| `List[List[str]]` | `[[".Q..","...Q"],["..Q.","Q..."]]` |

#### Category B: Multi-output Validation

For problems with **in-place modification + return value**, each validation value occupies one line:

- **Line 1**: Return value
- **Line 2+**: Modified state for verification

**Example: 0027 Remove Element**

```python
def removeElement(self, nums: List[int], val: int) -> int:
```

LeetCode Output: `Output: 2, nums = [2,2,_,_]`

Canonical `.out`:
```
2          # return value (k)
[2,2]      # nums[:k] for verification
```

**Rationale:**
- Mirrors LeetCode's dual validation (return value + modified array)
- Human-readable without running code
- Consistent with "1 line = 1 value" philosophy

#### Category C: Custom Judge Required

Same format as A or B, but runner uses `JUDGE_FUNC` for semantic comparison (e.g., order-independent results).

---

### Normalization Rules

| Rule | Specification |
|------|---------------|
| **Quotes** | Always double quotes `"`, never single `'`. Unquoted strings not supported. |
| **Spaces** | No spaces after `:` or `,` in arrays |
| **Booleans** | Lowercase `true`/`false` (JSON style, not Python) |
| **Line endings** | Always `\n` (parser tolerates `\r\n`, formatter converts) |
| **Trailing newline** | Optional (parser tolerates, formatter adds) |
| **BOM** | Not allowed |
| **Empty files** | Not allowed |

---

### Type Mapping: LeetCode → Canonical

| LeetCode Type | Python Type | Canonical |
|---------------|-------------|-----------|
| `int` | `int` | `42` |
| `float` | `float` | `2.5` |
| `boolean` | `bool` | `true` / `false` |
| `string` | `str` | `"abc"` |
| `integer[]` | `List[int]` | `[1,2,3]` |
| `string[]` | `List[str]` | `["a","b"]` |
| `integer[][]` | `List[List[int]]` | `[[1,2],[3,4]]` |
| `character[][]` | `List[List[str]]` | `[["a","b"],["c","d"]]` |
| `ListNode` | `Optional[ListNode]` | ⚠️ Future work |
| `TreeNode` | `Optional[TreeNode]` | ⚠️ Future work |

---

### Future Work: LinkedList & TreeNode

These types are **explicitly out of scope** for this migration:

| Type | Status | Reason |
|------|--------|--------|
| `ListNode` | 🚧 Future | Requires serialization format design |
| `TreeNode` | 🚧 Future | Requires serialization + null representation |
| Cycle detection | 🚧 Future | Requires special notation (e.g., `pos` parameter) |

**Current behavior:**
- Gate 2 detects these types and marks as `unsupported`
- `codegen new` exits with code 2 for these types
- Existing handwritten `solve()` continues to work

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
python -m codegen validate-tests --all
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
python -m codegen new <id> --with-tests
python runner/test_runner.py <id>
```

#### Exit Code Specification

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success: solution and tests created, runnable |
| 1 | Hard failure: metadata fetch failed |
| 2 | Strict-mode semantic failure |

**Exit code 2** indicates the command completed, but a required condition was not met:
- `--strict-tests` enabled and 0 tests generated
- Type unsupported for solve() generation (with `--solve-mode infer`)

The specific reason is always reported in stderr.

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

Migration follows a strict order to maintain safety nets at each step.

```
Phase 1: tests/ ──→ Phase 2: Infrastructure ──→ Phase 3: solutions/
                                                      │
                                                      ▼
Phase 6: solve_generator ◀── Phase 5: generators/ ◀── Phase 4: codegen E2E
```

---

### Phase 1: tests/ Canonicalization

**Goal:** Convert all test files to canonical format.

**Prerequisites:** None

**Steps:**

1. **Backup existing tests**
   ```bash
   # migrator.py creates .bak files automatically
   python -m codegen migrate --all --dry-run  # Preview
   python -m codegen migrate --all            # Execute
   ```

2. **Run Gate 0 validation**
   ```bash
   python -m codegen validate-tests --all
   ```

3. **Review and commit**
   ```bash
   git add tests/
   git commit -m "chore(tests): migrate to canonical JSON literal format"
   ```

**Exit Criteria:** Gate 0 passes (all files parse without error)

**Rollback:** Restore from `.bak` files or `git checkout`

---

### Phase 2: Infrastructure Update

**Goal:** Ensure parser and comparator handle canonical format.

**Prerequisites:** Phase 1 complete

**Steps:**

1. **Update test runner parser**
   - Ensure `runner/` can parse canonical JSON literal
   - Normalize `\r\n` to `\n` during read

2. **Update comparators (if needed)**
   - Boolean: compare `true`/`false` correctly
   - Arrays: handle no-space format `[1,2,3]`

3. **Verify with existing tests**
   ```bash
   python runner/test_runner.py --all
   ```

**Exit Criteria:** Gate 1 passes (all handwritten solve() pass)

**Rollback:** Revert parser changes, tests remain canonical

---

### Phase 3: solutions/ Compatibility

**Goal:** Ensure handwritten `solve()` functions work with canonical tests.

**Prerequisites:** Phase 2 complete

**Steps:**

1. **Run full regression**
   ```bash
   python runner/test_runner.py --all
   ```

2. **Fix any solve() that fails**
   - Update input parsing to handle JSON literal
   - Update output formatting to match canonical

3. **Document changes per problem**
   - Track which problems required solve() updates

**Exit Criteria:** Gate 1 passes (100% regression)

**Rollback:** Revert solve() changes individually

---

### Phase 4: codegen E2E Workflow

**Goal:** `codegen new --with-tests` produces runnable outputs.

**Prerequisites:** Phase 3 complete

**Steps:**

1. **Test codegen on Tier-0 problems**
   ```bash
   # Pick a known Tier-0 problem
   python -m codegen new 1 --with-tests --force
   python runner/test_runner.py 0001_two_sum
   ```

2. **Validate all Tier-0 problems**
   ```bash
   # Run E2E validation script (to be created)
   python -m codegen validate-e2e --tier 0
   ```

3. **Verify unsupported types fail gracefully**
   ```bash
   python -m codegen new 2 --with-tests  # ListNode problem
   # Should exit with code 2 and clear message
   ```

**Exit Criteria:** Gate 3 passes

**Rollback:** N/A (codegen is additive, doesn't modify existing files without --force)

---

### Phase 5: generators/ Update ✅ COMPLETE

**Goal:** All generators output canonical format.

**Status:** ✅ Complete (2026-01-02)

**Results:**
- 38/40 in-scope generators updated
- 7 LinkedList generators (OUT_OF_SCOPE)
- All generated tests passing

**Changes Applied:**

1. ✅ Converted `edge_cases` from strings to data structures
2. ✅ Used `json.dumps(separators=(',', ':'))` for arrays
3. ✅ Fixed `import json` placement
4. ✅ Multi-parameter problems: `(nums, target)` tuples → formatted output

**Verification:**
```bash
pytest .dev/tests_solutions/test_all_solutions.py::TestAllSolutions::test_generated_tests
# Result: 38 passed, 5 skipped, 2 failed (LinkedList)
```

**Rollback:** Git revert on `generators/` directory

---

### Phase 6: solve_generator Coverage Expansion

**Goal:** Expand solve_generator to cover more types.

**Prerequisites:** Phase 5 complete

**Steps:**

1. **Run Oracle verification for Tier-0**
   ```bash
   python -m codegen check --all --tier 0
   ```

2. **Generate capability report**
   ```bash
   python -m codegen check --all --report json > coverage-report.json
   ```

3. **Identify gaps and fix**
   - Review `parse_mismatch` errors
   - Add missing codecs to `solve_generator`

4. **Track coverage over time**
   - Commit coverage reports
   - Set up dashboard (optional)

**Exit Criteria:** Gate 2 Tier-0 at 100%

**Rollback:** N/A (coverage expansion is additive)

---

### Phase Summary

| Phase | Folder | Gate | Blocking |
|-------|--------|------|----------|
| 1 | tests/ | Gate 0 | ✅ Yes |
| 2 | runner/ | Gate 1 | ✅ Yes |
| 3 | solutions/ | Gate 1 | ✅ Yes |
| 4 | codegen | Gate 3 | ✅ Yes |
| 5 | generators/ | — | ✅ Yes |
| 6 | solve_generator | Gate 2 | 🟡 Coverage-based |

---

## Per-Folder Migration Guide

### tests/ Migration

**Scope:** 45 problems × ~3 test cases each ≈ 135+ files

#### Before vs After

| Before (Mixed) | After (Canonical) |
|----------------|-------------------|
| `2,7,11,15` | `[2,7,11,15]` |
| `[0, 1]` | `[0,1]` |
| `True` | `true` |
| `'abc'` | `"abc"` |

#### Migration Commands

```bash
# Step 1: Preview changes
python -m codegen migrate --all --dry-run

# Step 2: Execute migration (creates .bak files)
python -m codegen migrate --all

# Step 3: Validate
python -m codegen validate-tests --all

# Step 4: Run regression to ensure nothing broke
python runner/test_runner.py --all
```

#### Handling Edge Cases

| Issue | Resolution |
|-------|------------|
| Empty file | Delete and regenerate with `codegen new <id> --with-tests` |
| Parse error | Manual review, fix format, or regenerate |
| Encoding issue (BOM) | Re-save as UTF-8 without BOM |

#### Cleanup

After migration verified:
```bash
# Remove backup files (optional, after Gate 1 passes)
del tests\*.bak  # Windows
rm tests/*.bak   # Unix
```

---

### solutions/ Migration

**Scope:** 45 solution files, each with `solve()` function

#### What Needs to Change

The `solve()` function must:
1. **Parse** canonical JSON literal input
2. **Output** canonical JSON literal

#### Pattern: Before vs After

**Before (comma-separated):**
```python
def solve():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    nums = list(map(int, lines[0].split(',')))  # ❌ Old format
    target = int(lines[1])
    ...
    print(result)  # ❌ Python repr
```

**After (canonical JSON):**
```python
def solve():
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')
    nums = json.loads(lines[0])  # ✅ JSON literal
    target = json.loads(lines[1])
    ...
    print(json.dumps(result, separators=(',', ':')))  # ✅ Canonical output
```

#### Migration Strategy

Since we chose **Option A** (keep handwritten solve() as Oracle):

1. **Don't rewrite** — Only fix if Gate 1 fails
2. **Minimal changes** — Update parsing/output, not logic
3. **Document** — Track which files were modified

#### Verification

```bash
# After each solve() change
python runner/test_runner.py <problem_id>

# Full regression
python runner/test_runner.py --all
```

---

### generators/ Migration

**Scope:** 44 generator files

#### What Needs to Change

Generator `generate()` must output canonical format.

#### Pattern: Before vs After

**Before:**
```python
def _generate_case(size: int) -> str:
    nums = [random.randint(-10**6, 10**6) for _ in range(size)]
    nums_str = ','.join(map(str, nums))  # ❌ Comma-separated
    return f"{nums_str}\n{target}"
```

**After:**
```python
import json

def _generate_case(size: int) -> str:
    nums = [random.randint(-10**6, 10**6) for _ in range(size)]
    return f"{json.dumps(nums, separators=(',', ':'))}\n{target}"  # ✅ JSON
```

#### Generator Audit Checklist

For each generator, verify:

- [ ] Output uses `json.dumps()` for arrays
- [ ] Strings are double-quoted
- [ ] Booleans are lowercase (`true`/`false`)
- [ ] No trailing spaces or inconsistent line endings

#### Bulk Update Pattern

Many generators follow similar patterns. Consider:

```python
# Shared utility (optional)
def canonical_array(arr: list) -> str:
    import json
    return json.dumps(arr, separators=(',', ':'))
```

#### Verification

```bash
# Test generator output is parseable
python -c "
from generators import 0001_two_sum as gen
import json
for case in gen.generate(count=5, seed=42):
    lines = case.strip().split('\n')
    json.loads(lines[0])  # Should not raise
    print('✓', lines[0][:50])
"

# Run stress test
python runner/test_runner.py 0001_two_sum --generate 10 --seed 42
```

#### Generator Migration Order

Prioritize by complexity:

| Priority | Generators | Reason |
|----------|------------|--------|
| 1 | Simple arrays (Two Sum, etc.) | Easy, high confidence |
| 2 | 2D arrays (Word Search, etc.) | Need `[[]]` format |
| 3 | String problems | Already close to canonical |
| 4 | LinkedList/TreeNode | Skip (future work) |

---

## Tools & Commands

### Quick Reference

| Task | Command |
|------|---------|
| Migrate tests | `python -m codegen migrate --all` |
| Validate tests | `python -m codegen validate-tests --all` |
| Run regression | `python runner/test_runner.py --all` |
| New problem + tests | `python -m codegen new <id> --with-tests` |
| Check consistency | `python -m codegen check <id>` |
| Check all | `python -m codegen check --all` |

---

### codegen CLI

#### `codegen new`

Create solution and optionally test files.

```bash
python -m codegen new <id> [options]

Options:
  --with-tests      Generate test files from LeetCode examples
  --tests-only      Skip solution, generate tests only
  --force           Overwrite existing files
  --strict-tests    Exit code 2 if 0 tests generated
  --solve-mode      solve() generation: "infer" (auto) or "skip"
  --format          Test format (default: "raw", reserved for future)
```

**Exit Codes:**
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Metadata fetch failed |
| 2 | Strict-mode semantic failure (0 tests with --strict-tests, or unsupported type) |

**Examples:**
```bash
# Solution only
python -m codegen new 1

# Solution + tests
python -m codegen new 1 --with-tests

# Regenerate tests (overwrite)
python -m codegen new 1 --with-tests --force
```

#### `codegen migrate`

Convert test files to canonical format.

```bash
python -m codegen migrate [problem_id] [options]

Options:
  --all             Migrate all problems
  --dry-run         Preview changes without writing
  --no-backup       Don't create .bak files
  --limit N         Process only first N problems
```

**Examples:**
```bash
# Preview all
python -m codegen migrate --all --dry-run

# Migrate single problem
python -m codegen migrate 0001_two_sum

# Migrate all without backup
python -m codegen migrate --all --no-backup
```

#### `codegen validate-tests`

Validate test files against canonical format (Gate 0).

```bash
python -m codegen validate-tests [options]

Options:
  --all             Validate all test files
  --verbose         Show detailed output
```

#### `codegen check`

Check consistency between LeetCode examples and test files.

```bash
python -m codegen check <id> [options]
python -m codegen check --all [options]

Options:
  -v, --verbose     Detailed output
  --report FORMAT   Output format: "text" or "json"
  --generatable     Only check if examples can be parsed
  --limit N         Process only first N problems
```

---

### test_runner CLI

#### Run Tests

```bash
python runner/test_runner.py <problem_id> [options]
python runner/test_runner.py --all [options]

Options:
  --generate N      Run N additional generated test cases
  --generate-only N Skip .in/.out files, only use generated
  --seed S          Random seed for reproducibility
  --solution NAME   Use specific solution (default: "default")
```

**Examples:**
```bash
# Run single problem
python runner/test_runner.py 0001_two_sum

# Run all problems
python runner/test_runner.py --all

# With generated tests
python runner/test_runner.py 0001_two_sum --generate 10 --seed 42
```

---

### Windows Batch Scripts

Located in `scripts/`:

| Script | Purpose |
|--------|---------|
| `new_problem.bat` | Wrapper for `codegen new` |
| `run_tests.bat` | Wrapper for `test_runner.py` |

**Usage:**
```batch
scripts\new_problem.bat 1 --with-tests
scripts\run_tests.bat 0001_two_sum
```

---

## Rollback & Recovery

### Backup Strategy

| Phase | Backup Method | Location |
|-------|---------------|----------|
| tests/ | `.bak` files (automatic) | `tests/*.bak` |
| solutions/ | Git history | `git log solutions/` |
| generators/ | Git history | `git log generators/` |

#### .bak File Lifecycle

```
Migration starts
    │
    ▼
┌─────────────────────────┐
│ .bak files created      │
│ (tests/0001_two_sum.bak)│
└─────────────────────────┘
    │
    ▼
Gate 0 passes?
    │
    ├─ No  → Restore from .bak
    │
    ▼ Yes
Gate 1 passes?
    │
    ├─ No  → Investigate, possibly restore
    │
    ▼ Yes
Keep .bak for 1 week
    │
    ▼
Delete .bak files
```

---

### Rollback Procedures

#### Rollback tests/ (from .bak)

```bash
# Single file
copy tests\0001_two_sum_1.in.bak tests\0001_two_sum_1.in

# All files (PowerShell)
Get-ChildItem tests\*.bak | ForEach-Object {
    $newName = $_.FullName -replace '\.bak$', ''
    Copy-Item $_.FullName $newName -Force
}

# All files (Bash)
for f in tests/*.bak; do cp "$f" "${f%.bak}"; done
```

#### Rollback tests/ (from Git)

```bash
# Single file
git checkout HEAD~1 -- tests/0001_two_sum_1.in

# All test files
git checkout HEAD~1 -- tests/

# To specific commit
git checkout <commit-hash> -- tests/
```

#### Rollback solutions/

```bash
# Single file
git checkout HEAD~1 -- solutions/0001_two_sum.py

# All solutions
git checkout HEAD~1 -- solutions/
```

#### Rollback generators/

```bash
# Single file
git checkout HEAD~1 -- generators/0001_two_sum.py

# All generators
git checkout HEAD~1 -- generators/
```

---

### Recovery Scenarios

#### Scenario 1: Gate 0 fails after migration

**Symptom:** `validate-tests` reports parse errors

**Recovery:**
1. Identify failing files from error output
2. Restore from `.bak` or regenerate with `codegen new --with-tests --force`
3. Re-run Gate 0

#### Scenario 2: Gate 1 fails (regression)

**Symptom:** `test_runner.py --all` has failures

**Recovery:**
1. Identify which problems fail
2. Check if it's a test file issue → restore test `.bak`
3. Check if it's a solve() issue → revert solve() changes
4. Re-run Gate 1

#### Scenario 3: codegen produces invalid output

**Symptom:** Gate 3 fails, generated files don't work

**Recovery:**
1. This doesn't affect existing files (codegen is additive)
2. Fix codegen code
3. Re-run `codegen new --with-tests --force` for affected problems

---

### Cleanup After Success

After migration verified and stable (1 week):

```bash
# Remove .bak files
del tests\*.bak        # Windows
rm tests/*.bak         # Unix

# Verify no orphaned files
git status
```

### Emergency Rollback (Full)

If everything goes wrong:

```bash
# Reset to before migration
git checkout <pre-migration-commit> -- tests/ solutions/ generators/

# Or reset entire branch
git reset --hard <pre-migration-commit>
```

---

## Open Questions / Future Work

### Deferred to Future Phases

| Topic | Status | Notes |
|-------|--------|-------|
| **LinkedList serialization** | 🚧 Future | Need to define `[2,4,3]` → ListNode format |
| **TreeNode serialization** | 🚧 Future | Level-order with nulls: `[1,null,2,3]` |
| **Cycle representation** | 🚧 Future | How to express `pos` for cycle problems |
| **Graph problems** | 🚧 Future | Adjacency list format |
| **Custom comparators** | 🚧 Future | Unordered arrays, float tolerance |

---

### Open Technical Questions

#### 1. Float Precision in Output

**Issue:** LeetCode shows `2.00000` but JSON produces `2.0` or `2`

**Options:**
- A. Accept both formats in comparator
- B. Normalize to fixed decimal places
- C. Define precision per problem in metadata

**Current decision:** Defer until we hit a real problem

#### 2. Multi-Value Output

**Issue:** Some problems return multiple values, e.g.:
```
Output: 2, nums = [1,2,_,_]
```

**Options:**
- A. Multiple lines in `.out` ✅
- B. JSON array `[2, [1,2]]` ❌
- C. Per-problem custom format ❌

**Decision (2026-01-02):** Option A — Multiple lines in `.out`

Each line represents one validation value:
- Line 1: Return value
- Line 2+: Modified state

**Rationale:**
- Human-readable without running code
- Consistent with "1 line = 1 value" philosophy
- Avoids inventing per-problem JSON structures (Option B creates technical debt)
- Self-contained specification (Option C lacks standardization)

**Example (0027 Remove Element):**
```
# .out
2          ← k (return value)
[2,2]      ← nums[:k] (verification)
```

See also: §Output Format → Category B

#### 3. Order-Independent Comparison

**Issue:** Some problems accept answers in any order

**Options:**
- A. Sort before comparison
- B. Define `JUDGE_FUNC` per problem
- C. Add metadata flag `order_independent: true`

**Current decision:** Use existing `JUDGE_FUNC` mechanism

---

### Future Enhancements

| Enhancement | Priority | Description |
|-------------|----------|-------------|
| **CI Integration** | Medium | Auto-run Gates on PR |
| **Coverage Dashboard** | Low | Visualize Gate 2 progress |
| **Auto-fix Mode** | Low | `migrator.py --auto-fix` for common issues |
| **Batch Validation** | Medium | Validate entire LeetCode problem set |

---

### Known Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| LinkedList/TreeNode unsupported | 7 problems | Manual solve() |
| No cycle detection support | 2 problems | Manual solve() |
| No interactive problems | 0 problems | N/A |
| No design problems | 0 problems | N/A |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-02 | Initial draft created |
| 2026-01-02 | Added Verification Gates (Gate 0-3) |
| 2026-01-02 | Added Canonical Format Specification |
| 2026-01-02 | Added Execution Phases (6 phases) |
| 2026-01-02 | Added Per-Folder Migration Guide |
| 2026-01-02 | Added Tools & Commands reference |
| 2026-01-02 | Added Rollback & Recovery procedures |
| 2026-01-02 | Added Open Questions / Future Work |
| 2026-01-02 | Added Overview (document complete) |
| 2026-01-02 | Synced with specification.md (CLI path, exit codes, flags) |


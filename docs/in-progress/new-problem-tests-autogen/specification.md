# Spec: Integrate `new problem` scaffolding with auto-generated example tests

> **Status**: ✅ Implementation Complete  
> **Branch**: `feat/new-problem-tests-autogen`  
> **Created**: 2025-12-31  
> **Completed**: 2026-01-02  
> **Related**: [migration-plan.md](./migration-plan.md) · [test-file-format.md](../../contracts/test-file-format.md)

## Implementation Summary

This feature has been fully implemented with the following capabilities:

| Feature | Command | Status |
|---------|---------|--------|
| Test file generation | `codegen new <id> --with-tests` | ✅ Complete |
| solve() auto-generation (Tier 0) | `codegen new <id> --solve-mode infer` | ✅ Complete |
| Consistency checker | `codegen check <id>` | ✅ Complete |
| Format migration | `codegen migrate --all` | ✅ Complete |
| Windows wrapper | `scripts/new_problem.bat` | ✅ Complete |

For complete documentation, see:
- [CodeGen Package Docs](../../packages/codegen/README.md)
- [Package README](../../../src/codegen/README.md)

---

## Goals

- Provide a single, consistent entrypoint for creating a new problem scaffold:
  - Generate the solution file under `solutions/`
  - Optionally generate example-based tests under `tests/`
- Preserve the existing Windows workflow via `scripts/new_problem.bat`, while keeping all business logic in `codegen` for cross-platform use
- Support problem ID inputs `3` and `0003` (auto-pad to 4 digits)
- Auto-resolve the LeetCode slug/title for filename generation (no slug input required)
- Default-safe behavior:
  - Skip existing files by default
  - Overwrite only when `--force` is provided

---

## Non-Goals (v0)

- Normalizing example I/O into a standardized stdin/JSON format
- Supporting slug-based inputs (e.g., `longest-substring-without-repeating-characters`)
- Generating non-example tests (randomized/fuzz) or validating correctness
- Full coverage of all LeetCode HTML edge cases (handled iteratively)

---

## User Interfaces

### Windows Wrapper

`scripts/new_problem.bat` MUST forward arguments to codegen:

```batch
@echo off
setlocal EnableExtensions

REM Pass-through wrapper: all logic lives in src/codegen
python -m codegen new %*
exit /b %ERRORLEVEL%
```

**Usage examples:**

| Command | Behavior |
|---------|----------|
| `new_problem.bat 3` | Create solution only |
| `new_problem.bat 3 --with-tests` | Create solution + tests |
| `new_problem.bat 3 --tests-only` | Create tests only (skip solution) |
| `new_problem.bat 3 --with-tests --force` | Overwrite existing files |
| `new_problem.bat 3 --with-tests --strict-tests` | Fail if 0 tests generated |

### Python CLI (Source of Truth)

```bash
python -m codegen new <id> [--with-tests] [--tests-only] [--force] [--strict-tests] [--format raw]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `<id>` | Problem ID: `3` or `0003` (auto-padded to 4 digits) |
| `--with-tests` | Generate example tests under `tests/` |
| `--tests-only` | Skip solution, generate tests only |
| `--force` | Overwrite existing files |
| `--strict-tests` | Exit code 2 if 0 tests generated |
| `--format` | Test format (default: `raw`, reserved for future) |

**Exit codes:**

| Code | Condition |
|------|-----------|
| `0` | Solution OK; tests success/partial/none (warning shown) |
| `1` | Metadata fetch failed (hard fail) |
| `2` | Strict-mode semantic failure |

**Exit code 2 details:**

Exit code 2 indicates the command completed execution, but a required condition was not met:
- `--strict-tests` enabled and 0 tests generated
- Type unsupported for solve() generation (when using `--solve-mode infer`)

The specific reason is always reported in stderr.

---

## File Naming & Layout

Given:
- `id4 = zero_pad_4(id)` (e.g., `0003`)
- `snake_slug = to_snake_case(leetcode_title_slug)`
  - Example: `longest-substring-without-repeating-characters` → `longest_substring_without_repeating_characters`

### Solution

```
solutions/{id4}_{snake_slug}.py
```

### Tests (Example-based)

For each parsed example `i` in `1..N`:

```
tests/{id4}_{snake_slug}_{i}.in
tests/{id4}_{snake_slug}_{i}.out
```

Indexing MUST be **1-based**.

---

## Data Sources

### Problem Metadata

Codegen MUST resolve `leetcode_title_slug` for the given ID using `leetcode_datasource`:

```python
from leetcode_datasource import LeetCodeDataSource

ds = LeetCodeDataSource()
question = ds.get_by_frontend_id(problem_id)
slug = question.titleSlug  # e.g., "longest-substring-without-repeating-characters"
```

**Slug source priority:** LeetCode `titleSlug` only (no fallback).

### Example Extraction

Examples MUST be extracted from `Question.Body` (HTML).

Each example includes:
- Input block
- Output block

**v0 format (`raw`):**
- `.in` = Example input section (raw text)
- `.out` = Example output section (raw text)

---

## Expected HTML Patterns

**Common LeetCode Example HTML structure:**

```html
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = "abcabcbb"
<strong>Output:</strong> 3
<strong>Explanation:</strong> The answer is "abc", with the length of 3.
</pre>
```

**Parsing rules:**

- Only `Input:` and `Output:` are extracted
- `Explanation:` is ignored
- Parser should be resilient to:
  - Missing `<p>` wrapper (example label may be inside `<pre>` only)
  - Line breaks / extra whitespace inside `<pre>`
  - Multiple `<pre>` blocks (rare but possible)

---

## Parsing Rules (v0, `raw` format)

### Extraction Logic

1. Detect examples in order: Example 1, Example 2, ...
2. For each example:
   - Extract `Input:` text
   - Extract `Output:` text

### `.in` File Content

- Everything **after `Input:`** until **`Output:`**
- Leading/trailing whitespace trimmed

### `.out` File Content

- Everything **after `Output:`** until **`Explanation:`** or end of block
- Leading/trailing whitespace trimmed

### Normalization (Minimal, Safe)

- Convert HTML entities/tags to plain text:
  - Strip `<strong>`, `<code>`, `<span>`, etc.
  - Keep text content only
- Collapse Windows newlines to `\n` when writing files (repository standard)
- Do **not** attempt to re-serialize into JSON/stdin DSL in v0

### Whitespace Handling

- Trim surrounding whitespace
- Preserve internal line breaks

---

## Soft Fail Strategy

### Per-Example Failure

If `Input:` or `Output:` markers are not found for an example:
- Skip that example
- Log a warning

### Overall Failure

- If **at least 1 example** was parsed successfully → generate tests for those examples and succeed
- If **0 examples** parsed successfully → still succeed (solution created) but emit warning summary

---

## Overwrite Policy

| Target File | Default | With `--force` |
|-------------|---------|----------------|
| Solution exists | SKIP | OVERWRITE |
| Test file exists | SKIP | OVERWRITE |

**Per-file policy:** Each file is checked independently.

---

## Logging / UX

### Success Output

```
✅ Created: solutions/0003_longest_substring_without_repeating_characters.py
✅ Created: tests/0003_longest_substring_without_repeating_characters_1.in
✅ Created: tests/0003_longest_substring_without_repeating_characters_1.out
✅ Created: tests/0003_longest_substring_without_repeating_characters_2.in
✅ Created: tests/0003_longest_substring_without_repeating_characters_2.out
✅ Created: tests/0003_longest_substring_without_repeating_characters_3.in
✅ Created: tests/0003_longest_substring_without_repeating_characters_3.out

Summary: 1 solution, 3 test cases created
```

### Skip Output

```
⏭️  SKIP: solutions/0003_longest_substring_without_repeating_characters.py (exists)
✅ Created: tests/0003_longest_substring_without_repeating_characters_1.in
...
```

### Parse Failure Warning

```
✅ Created: solutions/0003_longest_substring_without_repeating_characters.py
⚠️  WARNING: Example 2 parse failed: Output marker not found
✅ Created: tests/0003_longest_substring_without_repeating_characters_1.in
✅ Created: tests/0003_longest_substring_without_repeating_characters_1.out

Summary: 1 solution, 1 test case created (2 examples skipped)
```

### Zero Tests Warning

```
✅ Created: solutions/0003_longest_substring_without_repeating_characters.py
⚠️  WARNING: 0/3 examples parsed successfully; no tests generated.
   Hint: Check HTML structure or add tests manually.

Summary: 1 solution, 0 test cases created
```

---

## Acceptance Criteria

### Basic Functionality

- [ ] `new_problem.bat 3 --with-tests` creates:
  - `solutions/0003_<slug>.py`
  - `tests/0003_<slug>_1.in`, `tests/0003_<slug>_1.out`, ... for all examples
- [ ] Running twice without `--force` does not modify existing files
- [ ] Running with `--force` overwrites existing files
- [ ] `python -m codegen new 0003 --with-tests` behaves identically to ID `3`

### Edge Cases

- [ ] `--tests-only` skips solution creation
- [ ] `--strict-tests` returns exit code 2 when 0 tests generated
- [ ] Parse failures are logged but don't stop execution

### Validation (Future)

- [ ] Batch test against all problems in `leetcode_datasource` database
  - Tool: `tools/review-code/compare_html_parsers.py`
  - TODO: Extend to iterate over all cached problems

---

## Implementation Notes

### HTML Parsing Method

**Decision:** Use regex/string-based approach (Method A)

**Rationale:**
- Already implemented in `tools/docstring/formatter.py::_extract_examples()`
- No additional dependencies
- ~80x faster than BeautifulSoup
- Battle-tested in existing codebase

**Reference implementation:** `tools/docstring/formatter.py`

### Code Location

| Component | Location |
|-----------|----------|
| CLI entry point | `src/codegen/cli.py` |
| IO Schema inference | `src/codegen/core/io_schema.py` |
| Example parser | `src/codegen/core/example_parser.py` |
| Stub parser | `src/codegen/core/stub_parser.py` |
| solve() generator | `src/codegen/core/solve_generator.py` |
| Test generator | `src/codegen/core/test_generator.py` |
| Consistency checker | `src/codegen/checker.py` |
| Format migrator | `src/codegen/migrator.py` |
| Windows wrapper | `scripts/new_problem.bat` |

---

## Test Consistency Checker (Implemented)

### Purpose

Check whether LeetCode examples can be parsed and whether existing test files match.

### CLI Usage

```bash
# Check single problem
python -m codegen check 1
python -m codegen check 1 -v          # Verbose

# Check all problems
python -m codegen check --all
python -m codegen check --all --limit 10

# Generatability only (skip consistency check)
python -m codegen check 1 --generatable

# Output formats
python -m codegen check --all --report json
```

### Check Results

| Status | Meaning |
|--------|---------|
| `match` | Test files match examples (may have whitespace differences) |
| `mismatch` | Test files differ from parsed examples |
| `missing_tests` | No test files exist for parsed examples |
| `parse_error` | Could not parse examples from HTML |
| `fetch_error` | Could not fetch question data |

### Full Analysis Report (2025-12-31)

**45 題完整分析結果：**

| 指標 | 數量 | 百分比 |
|------|------|--------|
| Total problems | 45 | 100% |
| With existing tests | 40 | 89% |
| Can parse examples | 44 | 98% |
| Has LinkedList | 7 | 15.6% |
| Has Tree | 0 | 0% |

**Mismatch Type 分布：**

| 類型 | 數量 | 百分比 | 說明 |
|------|------|--------|------|
| `separator_diff` | 19 | 42.2% | 逗號 vs 空格 |
| `normalization_only` | 12 | 26.7% | 僅空白差異 |
| `output_format` | 12 | 26.7% | `[0,1]` vs `0 1` |
| `serialization_diff` | 11 | 24.4% | `[0,1]` vs `[0, 1]` |
| `type_unsupported` | 7 | 15.6% | LinkedList 題目 |
| `value_diff` | 6 | 13.3% | 真的值不同 |
| `quote_style` | 3 | 6.7% | `"` vs `'` |
| `boolean_case` | 1 | 2.2% | `true` vs `True` |

**建議修復分布：**

| 修復類型 | 數量 | 說明 |
|----------|------|------|
| `format_migration` | 15 | 需遷移到 JSON literal canonical |
| `auto_normalize` | 11 | 可自動正規化（空白、引號） |
| `none` | 8 | 無需修復 |
| `parser_fix` | 7 | LinkedList 等特殊類型 |
| `manual_review` | 3 | 需人工確認 |

**詳細報告位置：** `docs/in-progress/new-problem-tests-autogen/mismatch-report.json`

---

## IO Schema (Implemented)

### Purpose

Infer input/output format rules from LeetCode method signatures.

### Data Flow

```
Question.Code (stub) 
  → parse_code_stub() → StubInfo 
  → infer_io_schema() → IOSchema
```

### IOSchema Structure

```python
@dataclass
class IOSchema:
    method_name: str
    params: List[ParamSchema]  # [(name, type, format, separators)]
    return_type: str
    return_format: ParamFormat  # SCALAR, ARRAY_1D, ARRAY_2D, etc.
    needs_helpers: Set[str]     # {"ListNode", "TreeNode"}
```

### Supported Types

#### Tier Classification

| Tier | Types | Status |
|------|-------|--------|
| **Tier-0** (Blocking) | `int`, `bool`, `str`, `List[int]`, `List[str]`, `List[List[int]]`, `List[List[str]]` | ✅ Complete |
| **Tier-1** (Future) | `ListNode`, `TreeNode` | 📋 Planned |

#### Type Format Mapping

| Type | Format | Separator Priority |
|------|--------|-------------------|
| `int`, `float`, `bool` | SCALAR | - |
| `str` | STRING | - |
| `List[int]`, `List[str]` | ARRAY_1D | `,` |
| `List[List[int]]`, `List[List[str]]` | ARRAY_2D | `,` |
| `Optional[ListNode]` | LINKED_LIST | `,` (Tier-1) |
| `Optional[TreeNode]` | TREE | `,` (Tier-1) |

---

## Canonical Format Decision (2025-12-31)

### 已確認決策

| 決策項目 | 選擇 | 說明 |
|----------|------|------|
| **Literal 格式** | JSON literal | `true/false`, `null`, strings 用 `"` |
| **2D array 格式** | Canonical literal | `[[1,2],[3,4]]` (不用 rows/cols 前綴) |
| **現有測試遷移** | 逐步遷移 | 建立轉換工具，逐題遷移 |
| **solve() 權威** | 維持現狀 | 每題 solve() 自己定義 IO 格式 |

### Canonical 格式規範

**Input (.in)：**
- 每行一個參數，使用 JSON literal
- 陣列：`[1,2,3]` (JSON literal, no spaces)
- 字串：一律使用 JSON double-quoted `"abc"` (不支援 unquoted)
- 數字：`42`
- Boolean：`true` / `false` (JSON 風格，小寫)
- 2D 陣列：`[[1,2],[3,4]]` (單行 literal)

**Output (.out)：**

Output format depends on problem category:

| Category | Description | Output Lines |
|----------|-------------|--------------|
| **A** (Simple) | Single return value | 1 line |
| **B** (Multi-output) | Return + modified state | 2+ lines |
| **C** (Custom Judge) | Same as A or B | Uses `JUDGE_FUNC` |

**Category A Example (Two Sum):**
```
# .out
[0,1]
```

**Category B Example (Remove Element):**
```python
def removeElement(self, nums: List[int], val: int) -> int:
```
LeetCode shows: `Output: 2, nums = [2,2,_,_]`

```
# .out
2         ← return value (k)
[2,2]     ← nums[:k] for verification
```

**Category B Problems:**

| Problem | Output Lines |
|---------|--------------|
| 0026_remove_duplicates | k, nums[:k] |
| 0027_remove_element | k, nums[:k] |
| 0080_remove_duplicates_ii | k, nums[:k] |

**Category A (in-place, no return):**

| Problem | Output |
|---------|--------|
| 0075_sort_colors | nums |
| 0088_merge_sorted_array | nums |
| 0283_move_zeroes | nums |

**標準範例：**
```
# .in
[2,7,11,15]
9

# .out
[0,1]
```

### 分隔符優先順序

當自動判斷分隔符時：
1. 優先使用逗號 `,`
2. 若值內含逗號 → 使用空格 ` `
3. 若值內含空格和逗號 → 使用 JSON literal 格式

---

## Mismatch Analyzer (Implemented)

### Purpose

分析所有題目的 mismatch 原因，分類並建議修復方式。

### CLI Usage

```bash
python -m codegen.analyzer
```

### Code Location

| Component | Location |
|-----------|----------|
| Analyzer | `src/codegen/analyzer.py` |
| Report output | `docs/in-progress/new-problem-tests-autogen/mismatch-report.json` |

---

## Implementation Progress

### Completed ✅

- [x] `io_schema.py` - 從 LeetCode signature 推導 IO 規則
- [x] `example_parser.py` - 從 Question.Body 解析 Example
- [x] `checker.py` - 可生成性 + 一致性檢查
- [x] CLI: `python -m codegen check`
- [x] `analyzer.py` - 全量 mismatch 分類報告
- [x] 修正 `stub_parser.py` LinkedList 解析問題
- [x] **Step 3: 建立格式遷移工具** `migrator.py`
- [x] **Step 4: solve() 自動生成** (`--solve-mode infer` for Tier 0)
- [x] **整合 `--with-tests` 到 `codegen new`**
- [x] **更新 `scripts/new_problem.bat`** (pass-through wrapper)

### New Features Added

| Feature | CLI | Description |
|---------|-----|-------------|
| Test generation | `codegen new <id> --with-tests` | Generate .in/.out from LeetCode examples |
| solve() inference | `codegen new <id> --solve-mode infer` | Auto-generate solve() for Tier 0 types |
| Format migration | `codegen migrate --all --dry-run` | Migrate tests to canonical JSON literal |
| Force overwrite | `codegen new <id> --with-tests --force` | Overwrite existing test files |

### Pending 📋 (Future)

- [ ] Tier-1: LinkedList/TreeNode solve() generation
- [ ] TreeNode support

### Recently Completed (2026-01-02)

- [x] Full migration of existing tests to canonical format
- [x] `--tests-only` flag (generate tests without solution)
- [x] `--strict-tests` flag (exit code 2 if 0 tests generated)
- [x] Multi-output validation format (Category A/B/C)

---

## Future Work (Tier-1)

### LinkedList/TreeNode Support

**Status:** 📋 Planned (see [migration-plan.md](./migration-plan.md#tier-1-future-work-linkedlist-support))

**問題：**
- LinkedList: `[2,4,3]` 轉成 nodes，cycle 如何表示？
- TreeNode: level-order `[1,null,2,3]`

**Blocked Problems (7):**
- 0002, 0021, 0023, 0025, 0141, 0142, 0876

**Implementation Plan:**
1. Define canonical serialization format
2. Implement codec in runner/utils/
3. Update solve() templates
4. Update generators

### Resolved Topics

The following topics have been resolved during migration:

| Topic | Resolution |
|-------|------------|
| 格式遷移工具 | ✅ `codegen migrate --all` implemented |
| solve() 自動生成範圍 | ✅ Tier-0 complete (97.8% coverage) |
| Output 特殊案例 | ✅ Category A/B/C defined |
| 多值輸出 | ✅ Multi-line output format |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [migration-plan.md](./migration-plan.md) | Migration execution guide |
| [test-file-format.md](../../contracts/test-file-format.md) | Canonical format specification |
| [CodeGen Package README](../../packages/codegen/README.md) | Package specification |
| [Solution Contract](../../contracts/solution-contract.md) | Solution file format |
| [compare_html_parsers.py](../../../tools/review-code/compare_html_parsers.py) | Parser comparison tool |
| [mismatch-report.json](./mismatch-report.json) | Full analysis report |
| [coverage-report.json](../../../coverage-report.json) | Gate 2 coverage report |

---

## Changelog

| Date | Change |
|------|--------|
| 2025-12-31 | Initial specification created |
| 2025-12-31 | Added IO Schema and Consistency Checker implementation |
| 2025-12-31 | Added Canonical Format Decision |
| 2025-12-31 | Completed full 45-problem analysis |
| 2025-12-31 | Fixed stub_parser.py LinkedList parsing |
| 2025-12-31 | Added Future Discussion Topics |
| 2026-01-02 | **Implemented: migrator.py** - Format migration tool |
| 2026-01-02 | **Implemented: solve_generator.py** - Tier 0 solve() auto-gen |
| 2026-01-02 | **Implemented: test_generator.py** - Test file generation |
| 2026-01-02 | **Integrated: --with-tests** flag in `codegen new` |
| 2026-01-02 | **Updated: scripts/new_problem.bat** to pass-through wrapper |
| 2026-01-02 | **Migration Complete** - All Gates passed |
| 2026-01-02 | **Merged: specification.delta.md** - Tier classification, string format, exit codes, multi-output format |
| 2026-01-02 | **Updated: Tier-0** now includes 2D arrays |
| 2026-01-02 | **Added: Category A/B/C** output format specification |


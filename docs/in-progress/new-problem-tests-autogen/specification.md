# Spec: Integrate `new problem` scaffolding with auto-generated example tests

> **Status**: In Progress  
> **Branch**: `feat/new-problem-tests-autogen`  
> **Created**: 2025-12-31

---

## Goals

- Provide a single, consistent entrypoint for creating a new problem scaffold:
  - Generate the solution file under `solutions/`
  - Optionally generate example-based tests under `tests/`
- Preserve the existing Windows workflow via `scripts/new_problem.bat`, while keeping all business logic in `packages/codegen` for cross-platform use
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

REM Pass-through wrapper: all logic lives in packages/codegen
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
| `2` | `--strict-tests` enabled + 0 tests generated |

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

Codegen MUST resolve `leetcode_title_slug` for the given ID using `packages/leetcode_datasource`:

```python
from packages.leetcode_datasource import LeetCodeDataSource

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
| CLI entry point | `packages/codegen/cli.py` |
| Test generation logic | `packages/codegen/core/testgen.py` (new) |
| Example parser | Adapt from `tools/docstring/formatter.py::_extract_examples()` |
| Windows wrapper | `scripts/new_problem.bat` |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [CodeGen Package README](../../packages/codegen/README.md) | Package specification |
| [Solution Contract](../../contracts/solution-contract.md) | Solution file format |
| [compare_html_parsers.py](../../../tools/review-code/compare_html_parsers.py) | Parser comparison tool |

---

## Changelog

| Date | Change |
|------|--------|
| 2024-12-31 | Initial specification created |


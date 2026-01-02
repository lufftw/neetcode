# CodeGen

> **Status**: Canonical Reference  
> **Scope**: `packages/codegen/` - Solution skeleton generation with test extraction  
> **Related**: [Package README](https://github.com/lufftw/neetcode/blob/main/packages/codegen/README.md)

CodeGen generates solution and practice skeleton files for LeetCode problems, providing the infrastructure needed for a LeetCode-like practice experience. It also extracts example test cases from problem descriptions and validates test file consistency.

---

## Table of Contents

1. [Overview](#overview)
2. [Scope](#scope)
3. [Interfaces](#interfaces)
4. [CLI Reference](#cli-reference)
5. [How It Fits in the System](#how-it-fits-in-the-system)
6. [Typical Workflows](#typical-workflows)
7. [Test Generation](#test-generation)
8. [IO Schema Inference](#io-schema-inference)
9. [Format Migration](#format-migration)
10. [Key Design Decisions](#key-design-decisions)
11. [Configuration](#configuration)
12. [Failure Modes and Constraints](#failure-modes-and-constraints)
13. [Related Documentation](#related-documentation)

---

## Overview

CodeGen serves as the **code generation engine** for the NeetCode practice framework. Its primary purpose is to:

- Generate reference skeleton files to `solutions/`
- Generate practice skeleton files to `practices/`
- Extract example test cases from LeetCode problem descriptions
- Provide a consistent structure that integrates with `runner/` for testing

The module is designed as a **stateless** generator - it produces output based on input without maintaining internal state.

### Goals

| Goal | Description |
|------|-------------|
| **Reference Generation** | Generate solution skeletons conforming to [Solution Contract](../../contracts/solution-contract.md) |
| **Practice Generation** | Generate practice skeletons that reuse reference infrastructure |
| **Test Extraction** | Extract example input/output from LeetCode HTML |
| **solve() Inference** | Auto-generate `solve()` based on method signature |
| **Focus on Solution** | Users only write `class Solution`; infrastructure is provided |
| **Reusable Components** | `solution_header`, Helper Catalog available for other modules |

### Non-Goals

| Non-Goal | Reason |
|----------|--------|
| ❌ Auto-generate complete solutions | Only generates skeleton; users implement solutions |
| ❌ Execute tests | Handled by `runner/` |
| ❌ Manage practice history | Handled by `practice_workspace` |
| ❌ Fetch problem data | Uses `leetcode_datasource` |

---

## Scope

### What this module handles

- ✅ Rendering file-level docstrings (`solution_header`)
- ✅ Parsing LeetCode code stubs
- ✅ Detecting and emitting helper classes (ListNode, TreeNode, etc.)
- ✅ Assembling complete module files
- ✅ Generating SOLUTIONS dict structure
- ✅ Creating solve() interface (placeholder or inferred)
- ✅ **Extracting examples from HTML** (`example_parser`)
- ✅ **Inferring IO schema from signatures** (`io_schema`)
- ✅ **Generating test files** (`test_generator`)
- ✅ **Checking test consistency** (`checker`)
- ✅ **Migrating test formats** (`migrator`)

### What this module explicitly avoids

- ❌ Test execution (handled by `runner/`)
- ❌ Practice file versioning (handled by `practice_workspace`)
- ❌ Network requests for problem data (handled by `leetcode_datasource`)
- ❌ CLI argument parsing for tools (handled by `tools/`)

---

## Interfaces

High-level summary of public APIs. For complete API reference, see [Package README](https://github.com/lufftw/neetcode/blob/main/packages/codegen/README.md).

### Core Generation

| Interface | Purpose |
|-----------|---------|
| `generate_reference_skeleton()` | Generate skeleton to `solutions/` |
| `generate_practice_skeleton()` | Generate skeleton to `practices/` |
| `render_solution_header()` | Render file-level docstring |
| `parse_code_stub()` | Parse LeetCode code stub |
| `assemble_module()` | Assemble complete file from parts |
| `detect_required_helpers()` | Detect needed helper classes |

### Test Generation

| Interface | Purpose |
|-----------|---------|
| `generate_tests_from_datasource()` | Generate `.in`/`.out` files from examples |
| `parse_examples()` | Extract examples from HTML |
| `infer_io_schema()` | Infer IO format from signature |
| `generate_solve_function()` | Auto-generate solve() code |

### Validation & Migration

| Interface | Purpose |
|-----------|---------|
| `TestChecker` | Check test consistency |
| `migrate_problem()` | Migrate single problem's tests |
| `migrate_all()` | Migrate all tests |

---

## CLI Reference

### Generate Reference Skeleton

```bash
# Basic generation
python -m packages.codegen new <problem_id>

# With test files from examples
python -m packages.codegen new <problem_id> --with-tests

# With auto-generated solve()
python -m packages.codegen new <problem_id> --solve-mode infer

# Combined
python -m packages.codegen new <problem_id> --with-tests --solve-mode infer --force

# Preview without writing
python -m packages.codegen new <problem_id> --dry-run
```

| Flag | Description |
|------|-------------|
| `--with-tests` | Generate `.in`/`.out` files from LeetCode examples |
| `--solve-mode` | `placeholder` (default) or `infer` (auto-generate) |
| `--force` | Overwrite existing test files |
| `--dry-run` | Preview without writing files |
| `--header-level` | `minimal`, `standard`, or `full` |

### Generate Practice Skeleton

```bash
python -m packages.codegen practice <problem_id>
python -m packages.codegen practice <problem_id> --all-solutions
```

### Check Test Consistency

```bash
# Check single problem
python -m packages.codegen check <problem_id>
python -m packages.codegen check <problem_id> -v

# Check all problems
python -m packages.codegen check --all
python -m packages.codegen check --all --limit 10

# JSON output
python -m packages.codegen check --all --report json
```

| Status | Meaning |
|--------|---------|
| `match` | Test files match examples |
| `mismatch` | Test files differ from parsed examples |
| `missing_tests` | No test files exist |
| `parse_error` | Could not parse examples from HTML |

### Migrate Test Format

```bash
# Preview migration
python -m packages.codegen migrate <problem_id> --dry-run -v

# Migrate single problem
python -m packages.codegen migrate <problem_id>

# Migrate all problems
python -m packages.codegen migrate --all --dry-run

# Migrate without backup
python -m packages.codegen migrate --all --no-backup
```

---

## How It Fits in the System

```
┌────────────────────────┐
│  leetcode_datasource   │  ← Problem metadata + HTML
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐     ┌───────────────────────┐
│       codegen          │ ──► │   practice_workspace  │
│                        │     └───────────────────────┘
│  ┌──────────────────┐  │              │
│  │ test_generator   │  │              │ manages history
│  │ solve_generator  │  │              ▼
│  │ checker          │  │         practices/_history/
│  │ migrator         │  │
│  └──────────────────┘  │
└───────────┬────────────┘
            │ generates
            ▼
       solutions/
       practices/
       tests/
            │
            ▼
┌────────────────────────┐
│        runner          │  ← Executes tests
└────────────────────────┘
```

### Module Relationships

| Module | Relationship |
|--------|--------------|
| `leetcode_datasource` | **Uses** - Fetches problem metadata and HTML |
| `practice_workspace` | **Uses** - Calls `save_to_history()` when practice exists |
| `runner` | **Used by** - Runs generated files and tests |
| `tools/` | **Used by** - CLI wrappers invoke codegen |

---

## Typical Workflows

### Workflow: Generate Reference with Tests

When `codegen new <problem_id> --with-tests` is invoked:

1. **Check existence** - If `solutions/<id>_<slug>.py` exists, stop
2. **Fetch metadata** - Get problem info and HTML from `leetcode_datasource`
3. **Parse stub** - Extract method signature, parameters, return type
4. **Detect helpers** - Determine if ListNode, TreeNode, etc. are needed
5. **Infer IO schema** - Map parameter types to input formats
6. **Generate solve()** - Based on `--solve-mode` (placeholder or infer)
7. **Assemble module** - Combine header, imports, helpers, SOLUTIONS, Solution, solve()
8. **Write solution** - Output to `solutions/<id>_<slug>.py`
9. **Parse examples** - Extract examples from HTML
10. **Generate tests** - Create `.in`/`.out` files for each example

### Workflow: Check and Migrate

```bash
# 1. Check current state
python -m packages.codegen check --all

# 2. Preview migration
python -m packages.codegen migrate --all --dry-run

# 3. Migrate with backup
python -m packages.codegen migrate --all

# 4. Verify
python -m packages.codegen check --all
```

---

## Test Generation

### Canonical Test Format

All generated test files use the **JSON literal** format:

**Input File (`.in`):**
```
[2,7,11,15]
9
```

**Output File (`.out`):**
```
[0,1]
```

### Format Rules

| Type | Format | Example |
|------|--------|---------|
| Integer | Plain number | `42` |
| Float | Plain number | `3.14` |
| Boolean | Lowercase | `true`, `false` |
| String | Quoted | `"hello"` |
| Array | JSON literal | `[1,2,3]` |
| 2D Array | JSON literal | `[[1,2],[3,4]]` |

### Type Support Tiers

| Tier | Types | solve() Generation |
|------|-------|-------------------|
| **Tier 0** | `int`, `str`, `List[int]`, `List[str]` | ✅ Fully auto-generated |
| **Tier 1** | `List[List[int]]`, `float` | ✅ Fully auto-generated |
| **Tier 2** | `ListNode`, `TreeNode` | ⚠️ Placeholder with TODOs |

---

## IO Schema Inference

### Data Flow

```
Question.Code (stub) 
  → parse_code_stub() → StubInfo 
  → infer_io_schema() → IOSchema
  → generate_solve_function() → solve() code
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

### ParamFormat Types

| Format | Type Hints | Description |
|--------|------------|-------------|
| `SCALAR` | `int`, `float`, `bool` | Single value |
| `STRING` | `str` | String value |
| `ARRAY_1D` | `List[int]`, `List[str]` | 1D array |
| `ARRAY_2D` | `List[List[int]]` | 2D matrix |
| `LINKED_LIST` | `Optional[ListNode]` | Linked list |
| `TREE` | `Optional[TreeNode]` | Binary tree |

---

## Format Migration

### Purpose

The migrator converts existing test files from legacy formats (space-separated, comma-separated) to the canonical JSON literal format.

### Detected Formats

| Format | Example | Converted To |
|--------|---------|--------------|
| `space_sep` | `1 2 3 4` | `[1,2,3,4]` |
| `comma_sep` | `1,2,3,4` | `[1,2,3,4]` |
| `canonical` | `[1,2,3,4]` | (no change) |

### Migration Report

```
============================================================
MIGRATION REPORT
============================================================
Problems processed: 45
Total files: 218
  Migrated: 93
  Skipped (already canonical): 125
  Errors: 0
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Stateless design** | CodeGen has no internal state; outputs depend purely on inputs |
| **Parser doesn't guess** | `stub_parser.py` only parses; detection logic is separate |
| **Centralized assembly** | `assemble.py` handles file composition to avoid duplication |
| **Inline helpers by default** | Helper classes embedded in file for portability |
| **No template engine** | Pure Python string composition; no Jinja2 dependency |
| **Reuse over regenerate** | Practice skeletons reuse reference infrastructure when available |
| **JSON literal format** | Unambiguous, parseable, compatible with LeetCode examples |
| **Tiered type support** | Start with simple types, add complex types incrementally |

### Design Philosophy

```
┌─────────────────────────────────────────────────────────┐
│  codegen = stateless      → Only generates, no state    │
│  workspace = stateful     → Manages history/restore     │
│  runner = execution       → Runs tests, no generation   │
│                                                         │
│  stub_parser: parse only  → Separation of concerns      │
│  io_schema: infer format  → Type-driven generation      │
│  helpers: centralized     → Single source of truth      │
│  assemble.py: unified     → Avoid duplication           │
└─────────────────────────────────────────────────────────┘
```

---

## Configuration

### Config File Location

```
.neetcode/codegen.toml
```

### Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `header.level` | `"full"` | Header detail: `minimal`, `standard`, `full` |
| `helpers.mode` | `"inline"` | Helper emit: `inline`, `import`, `none` |
| `skeleton.solve_mode` | `"placeholder"` | solve() mode: `placeholder`, `infer` |
| `practice.multi_solution_mode` | `"single"` | Practice mode: `single`, `all` |

### Priority Order

```
CLI flag > .neetcode/codegen.toml > package defaults
```

---

## Failure Modes and Constraints

| Constraint | Behavior |
|------------|----------|
| Problem not found | Raises exception from `leetcode_datasource` |
| Reference already exists | Returns early with message (for `codegen new`) |
| Invalid code stub | Raises `ParseError` with details |
| Missing TOML config | Uses defaults |
| Example parse failure | Skips example, logs warning, continues |
| Test file exists | Skips (unless `--force` specified) |
| Unsupported type | Generates placeholder solve() with TODOs |

### Exit Codes

| Code | Condition |
|------|-----------|
| `0` | Success |
| `1` | Metadata fetch failed or validation error |
| `2` | `--strict-tests` enabled + 0 tests generated (reserved) |

---

## Related Documentation

| Document | Content |
|----------|---------|
| [Package README](https://github.com/lufftw/neetcode/blob/main/packages/codegen/README.md) | Quick reference, API details |
| [Solution Contract](../../contracts/solution-contract.md) | Output file requirements |
| [LeetCode DataSource](../leetcode_datasource/README.md) | Problem data source |
| [Practice Workspace](../practice_workspace/README.md) | History management |
| [Test Generation Spec](../../in-progress/new-problem-tests-autogen/specification.md) | Feature specification |

---

## Appendix: Output File Structure

Reference skeleton output follows the [Solution Contract](../../contracts/solution-contract.md):

```python
"""
Problem: Two Sum
Link: https://leetcode.com/problems/two-sum/
...
"""
from typing import List, Optional
from _runner import get_solver

# Helper classes (if detected)
class ListNode:
    ...

# SOLUTIONS dict
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "twoSum",
        "complexity": "TODO: O(?)",
        "description": "TODO: describe your approach",
    },
}

# Solution class
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # TODO: Implement your solution
        pass

# solve() interface (auto-generated with --solve-mode infer)
def solve():
    """
    Input format (JSON literal, one per line):
        nums: List[int]
        target: int

    Output: List[int]
    """
    import sys
    import json

    data = sys.stdin.read().strip().split('\n')

    nums = json.loads(data[0].strip())
    target = int(data[1].strip())

    solver = get_solver(SOLUTIONS)
    result = solver.twoSum(nums, target)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
```

---

## Appendix: Module Structure

```
codegen/
├── __init__.py              # Public API re-exports
├── __main__.py              # python -m packages.codegen
├── cli.py                   # CLI: new / practice / check / migrate
├── checker.py               # Test consistency checker
├── analyzer.py              # Mismatch analysis and reporting
├── migrator.py              # Format migration tool
├── core/
│   ├── __init__.py
│   ├── solution_header.py   # Header rendering
│   ├── stub_parser.py       # LeetCode stub parsing
│   ├── assemble.py          # Module assembly
│   ├── config.py            # Configuration management
│   ├── io_schema.py         # IO format inference
│   ├── example_parser.py    # HTML example extraction
│   ├── solve_generator.py   # solve() auto-generation
│   ├── test_generator.py    # Test file generation
│   └── helpers/
│       ├── __init__.py
│       ├── catalog.py       # Canonical helper definitions
│       ├── detect.py        # Helper detection logic
│       └── emit.py          # Helper code emission
├── reference/
│   ├── __init__.py
│   └── generator.py         # Reference skeleton generation
└── practice/
    ├── __init__.py
    ├── generator.py         # Practice skeleton generation
    └── reuse.py             # Reuse from reference
```

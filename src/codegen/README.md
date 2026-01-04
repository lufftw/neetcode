# CodeGen

LeetCode solution skeleton generator with automatic test case extraction.

## Overview

Generates reference (`solutions/`) and practice (`practices/`) skeleton files for LeetCode problems with proper infrastructure (helpers, solve(), SOLUTIONS dict). Optionally extracts example test cases from LeetCode problem descriptions.

## Responsibility

### What this package does

- ✅ Generates reference skeleton files to `solutions/`
- ✅ Generates practice skeleton files to `practices/`
- ✅ Renders solution file headers (problem description docstrings)
- ✅ Parses LeetCode code stubs
- ✅ Detects and emits required helper classes (ListNode, TreeNode, etc.)
- ✅ Assembles complete module files
- ✅ **Extracts example test cases** from LeetCode HTML
- ✅ **Auto-generates solve() functions** based on method signatures
- ✅ **Migrates test files** to canonical format
- ✅ **Validates consistency** between tests and LeetCode examples

### What this package does NOT do

- ❌ Execute tests (handled by `runner/`)
- ❌ Manage practice history (handled by `practice_workspace`)
- ❌ Fetch problem data directly (uses `leetcode_datasource`)

## CLI Commands

```bash
# Generate reference skeleton
python -m codegen new <problem_id>

# Generate with automatic test files
python -m codegen new <problem_id> --with-tests

# Generate with auto-inferred solve()
python -m codegen new <problem_id> --solve-mode infer

# Generate practice skeleton
python -m codegen practice <problem_id>

# Check test consistency
python -m codegen check <problem_id>
python -m codegen check --all

# Migrate tests to canonical format
python -m codegen migrate <problem_id>
python -m codegen migrate --all --dry-run
```

## Public API

| Export | Description |
|--------|-------------|
| `generate_reference_skeleton()` | Generate skeleton to `solutions/` |
| `generate_practice_skeleton()` | Generate skeleton to `practices/` |
| `render_solution_header()` | Render file-level docstring |
| `parse_code_stub()` | Parse LeetCode code stub |
| `StubInfo` | Parsed stub information |
| `assemble_module()` | Assemble complete file |
| `CodeGenConfig` | Configuration class |
| `load_config()` | Load config from TOML |
| `detect_required_helpers()` | Detect needed helpers |
| `emit_helpers()` | Emit helper code |
| `HELPER_CATALOG` | Canonical helper definitions |
| `infer_io_schema()` | Infer IO format from signature |
| `generate_solve_function()` | Auto-generate solve() |
| `generate_tests_from_datasource()` | Generate test files |
| `TestChecker` | Check test consistency |
| `migrate_problem()` | Migrate test format |

## File Structure

```
codegen/
├── __init__.py              # Public API re-exports
├── cli.py                   # CLI: new / practice / check / migrate
├── checker.py               # Test consistency checker
├── analyzer.py              # Mismatch analysis
├── migrator.py              # Format migration tool
├── core/                    # Core logic
│   ├── __init__.py
│   ├── solution_header.py   # Header rendering
│   ├── stub_parser.py       # Stub parsing
│   ├── assemble.py          # Module assembly
│   ├── config.py            # Configuration
│   ├── io_schema.py         # IO format inference
│   ├── example_parser.py    # HTML example extraction
│   ├── solve_generator.py   # solve() auto-generation
│   ├── test_generator.py    # Test file generation
│   └── helpers/             # Helper utilities
│       ├── __init__.py
│       ├── catalog.py       # Canonical definitions
│       ├── detect.py        # Detection logic
│       └── emit.py          # Emit strategies
├── reference/               # Reference generation
│   ├── __init__.py
│   └── generator.py
└── practice/                # Practice generation
    ├── __init__.py
    ├── generator.py
    └── reuse.py             # Reuse from reference
```

## Dependencies

| Direction | Package | Purpose |
|-----------|---------|---------|
| Uses → | `leetcode_datasource` | Problem metadata |
| Uses → | `practice_workspace` | History management (save_to_history) |

> ❗ **Do NOT list tools here.** Tools depend on packages, not vice versa.

## Usage

```python
from codegen import (
    generate_reference_skeleton,
    generate_practice_skeleton,
    render_solution_header,
)

# Generate reference skeleton
generate_reference_skeleton(1)  # Two Sum

# Generate reference with test files
from codegen.core.test_generator import generate_tests_from_datasource
generate_tests_from_datasource(1, force=True)

# Generate practice skeleton
generate_practice_skeleton(1)

# Check test consistency
from codegen.checker import TestChecker
checker = TestChecker()
result = checker.check_problem(1)
print(result.summary())
```

## Canonical Test Format

Test files use JSON literal format:

**Input (`.in`):**
```
[2,7,11,15]
9
```

**Output (`.out`):**
```
[0,1]
```

- One parameter per line as JSON literal
- Boolean: `true`/`false` (lowercase)
- Arrays: `[1,2,3]` (no spaces)
- 2D arrays: `[[1,2],[3,4]]` (single line)

## Related Documentation

- **[Complete Specification](../../docs/packages/codegen/README.md)** - System-level documentation
- **[Feature Spec](../../docs/in-progress/new-problem-tests-autogen/specification.md)** - Test generation specification

---

## Documentation Maintenance

⚠️ **When modifying this package:**

1. Update this README (quick reference)
2. Update `docs/packages/codegen/README.md` (complete specification)

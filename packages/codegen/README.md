# CodeGen

LeetCode solution skeleton generator.

## Overview

Generates reference (`solutions/`) and practice (`practices/`) skeleton files for LeetCode problems with proper infrastructure (helpers, solve(), SOLUTIONS dict).

## Responsibility

### What this package does

- ✅ Generates reference skeleton files to `solutions/`
- ✅ Generates practice skeleton files to `practices/`
- ✅ Renders solution file headers (problem description docstrings)
- ✅ Parses LeetCode code stubs
- ✅ Detects and emits required helper classes (ListNode, TreeNode, etc.)
- ✅ Assembles complete module files

### What this package does NOT do

- ❌ Execute tests (handled by `runner/`)
- ❌ Manage practice history (handled by `practice_workspace`)
- ❌ Fetch problem data directly (uses `leetcode_datasource`)

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

## File Structure

```
codegen/
├── __init__.py              # Public API re-exports
├── cli.py                   # CLI: codegen new / practice
├── core/                    # Core logic
│   ├── __init__.py
│   ├── solution_header.py   # Header rendering
│   ├── stub_parser.py       # Stub parsing
│   ├── assemble.py          # Module assembly
│   ├── config.py            # Configuration
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
from packages.codegen import (
    generate_reference_skeleton,
    generate_practice_skeleton,
    render_solution_header,
)

# Generate reference skeleton
generate_reference_skeleton(1)  # Two Sum

# Generate practice skeleton
generate_practice_skeleton(1)

# Render header only
from packages.leetcode_datasource import LeetCodeDataSource
ds = LeetCodeDataSource()
meta = ds.get_by_frontend_id(1)
header = render_solution_header(meta)
```

## Related Documentation

- **[Complete Specification](../../docs/packages/codegen/README.md)** - System-level documentation

---

## Documentation Maintenance

⚠️ **When modifying this package:**

1. Update this README (quick reference)
2. Update `docs/packages/codegen/README.md` (complete specification)


# CodeGen

> **Status**: Canonical Reference  
> **Scope**: `packages/codegen/` - Solution skeleton generation  
> **Related**: [Package README](https://github.com/lufftw/neetcode/blob/main/packages/codegen/README.md)

CodeGen generates solution and practice skeleton files for LeetCode problems, providing the infrastructure needed for a LeetCode-like practice experience.

---

## Table of Contents

1. [Overview](#overview)
2. [Scope](#scope)
3. [Interfaces](#interfaces)
4. [How It Fits in the System](#how-it-fits-in-the-system)
5. [Typical Workflows](#typical-workflows)
6. [Key Design Decisions](#key-design-decisions)
7. [Configuration](#configuration)
8. [Failure Modes and Constraints](#failure-modes-and-constraints)
9. [Related Documentation](#related-documentation)

---

## Overview

CodeGen serves as the **code generation engine** for the NeetCode practice framework. Its primary purpose is to:

- Generate reference skeleton files to `solutions/`
- Generate practice skeleton files to `practices/`
- Provide a consistent structure that integrates with `runner/` for testing

The module is designed as a **stateless** generator - it produces output based on input without maintaining internal state.

### Goals

| Goal | Description |
|------|-------------|
| **Reference Generation** | Generate solution skeletons conforming to [Solution Contract](../../contracts/solution-contract.md) |
| **Practice Generation** | Generate practice skeletons that reuse reference infrastructure |
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
- ✅ Creating solve() interface placeholders

### What this module explicitly avoids

- ❌ Test execution (handled by `runner/`)
- ❌ Practice file versioning (handled by `practice_workspace`)
- ❌ Network requests for problem data (handled by `leetcode_datasource`)
- ❌ CLI argument parsing for tools (handled by `tools/`)

---

## Interfaces

High-level summary of public APIs. For complete API reference, see [Package README](../../../packages/codegen/README.md).

| Interface | Purpose |
|-----------|---------|
| `generate_reference_skeleton()` | Generate skeleton to `solutions/` |
| `generate_practice_skeleton()` | Generate skeleton to `practices/` |
| `render_solution_header()` | Render file-level docstring |
| `parse_code_stub()` | Parse LeetCode code stub |
| `assemble_module()` | Assemble complete file from parts |
| `detect_required_helpers()` | Detect needed helper classes |

---

## How It Fits in the System

```
┌────────────────────────┐
│  leetcode_datasource   │  ← Problem metadata
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐     ┌───────────────────────┐
│       codegen          │ ──► │   practice_workspace  │
└───────────┬────────────┘     └───────────────────────┘
            │                          │
            │ generates                │ manages history
            ▼                          ▼
       solutions/                 practices/_history/
       practices/
            │
            │
            ▼
┌────────────────────────┐
│        runner          │  ← Executes tests
└────────────────────────┘
```

### Module Relationships

| Module | Relationship |
|--------|--------------|
| `leetcode_datasource` | **Uses** - Fetches problem metadata |
| `practice_workspace` | **Uses** - Calls `save_to_history()` when practice exists |
| `runner` | **Used by** - Runs generated files |
| `tools/` | **Used by** - CLI wrappers invoke codegen |

### Dependency Direction

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   ✅ codegen → leetcode_datasource                       │
│   ✅ codegen → practice_workspace (for history only)     │
│   ❌ codegen → runner (FORBIDDEN)                        │
│   ❌ codegen → tools  (FORBIDDEN)                        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Typical Workflows

### Workflow: Generate Reference Skeleton

When `codegen new <problem_id>` is invoked:

1. **Check existence** - If `solutions/<id>_<slug>.py` exists, stop (suggest using `codegen practice`)
2. **Fetch metadata** - Get problem info from `leetcode_datasource`
3. **Parse stub** - Extract method signature, parameters, return type
4. **Detect helpers** - Determine if ListNode, TreeNode, etc. are needed
5. **Assemble module** - Combine header, imports, helpers, SOLUTIONS, Solution class, solve()
6. **Write file** - Output to `solutions/<id>_<slug>.py`

### Workflow: Generate Practice Skeleton

When `codegen practice <problem_id>` is invoked:

1. **Check practice existence** - If `practices/<id>_<slug>.py` exists, save to `_history/`
2. **Check reference existence** - If `solutions/<id>_<slug>.py` exists, use **Reuse Strategy**
3. **Generate skeleton**:
   - **With reference**: Copy infrastructure, clear Solution class body
   - **Without reference**: Use same flow as reference generation
4. **Write file** - Output to `practices/<id>_<slug>.py`

### Reuse Strategy

When a reference solution exists, the practice skeleton reuses infrastructure:

| Component | Treatment |
|-----------|-----------|
| `solution_header` | ✅ Fully preserved |
| imports | ✅ Fully preserved |
| Helper classes | ✅ Fully preserved |
| JUDGE_FUNC | ✅ Fully preserved |
| SOLUTIONS dict | ⚠️ Structure kept, complexity/description cleared |
| Solution class(es) | ⚠️ Signature kept, body cleared |
| Helper functions | ✅ Fully preserved |
| solve() | ✅ Fully preserved |

> **Design Rationale**: Users focus only on implementing `class Solution`; all infrastructure is ready.

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

### Design Philosophy

```
┌─────────────────────────────────────────────────────────┐
│  codegen = stateless      → Only generates, no state    │
│  workspace = stateful     → Manages history/restore     │
│  runner = execution       → Runs tests, no generation   │
│                                                         │
│  stub_parser: parse only  → Separation of concerns      │
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

---

## Related Documentation

| Document | Content |
|----------|---------|
| [Package README](../../../packages/codegen/README.md) | Quick reference, API details |
| [Solution Contract](../../contracts/solution-contract.md) | Output file requirements |
| [LeetCode DataSource](../leetcode_datasource/README.md) | Problem data source |
| [Practice Workspace](../practice_workspace/README.md) | History management |

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

# solve() interface
def solve():
    ...

if __name__ == "__main__":
    solve()
```

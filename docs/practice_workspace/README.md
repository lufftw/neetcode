# Practice Workspace Specification

> **Status**: Draft  
> **Scope**: `packages/practice_workspace/` - Practice file management  
> **Related**: [Package README](https://github.com/lufftw/neetcode/blob/main/packages/practice_workspace/README.md)

Practice Workspace is a **stateful** package that manages practice file history and restore operations.

---

## Overview

This module handles:

- Saving practice files to history (`_history/` directory)
- Listing historical versions
- Restoring previous versions

## Scope

### What this module handles

- Practice file versioning
- Timestamp-based history management
- Restore operations

### What this module explicitly avoids

- File content generation (handled by `codegen`)
- Test execution (handled by `runner`)
- Network operations

## Interfaces

| Interface | Purpose |
|-----------|---------|
| `save_to_history()` | Save current practice to history |
| `list_history()` | List all history versions |
| `restore_from_history()` | Restore a specific version |
| `restore_latest()` | Restore the most recent version |

## How It Fits in the System

```
┌──────────────┐     ┌────────────────────────┐
│   codegen    │ ──► │   practice_workspace   │
└──────────────┘     └────────────────────────┘
        │                      │
        │ generates            │ manages history
        ▼                      ▼
    practices/             practices/_history/
```

When `codegen practice` runs:
1. CodeGen checks if practice file exists
2. If exists, calls `save_to_history()` from practice_workspace
3. CodeGen generates new skeleton
4. CodeGen writes to `practices/`

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Stateful design | History requires persistent state |
| Filesystem-only | No external dependencies |
| Timestamp-based naming | Simple, sortable, unique |

## Related Documentation

| Document | Content |
|----------|---------|
| [Package README](../../packages/practice_workspace/README.md) | Quick reference, API |
| [CodeGen Spec](../codegen/README.md) | How codegen uses workspace |

---

> **TODO**: Expand this specification with detailed workflow examples and edge cases.


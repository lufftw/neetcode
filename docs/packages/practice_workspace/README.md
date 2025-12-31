# Practice Workspace

> **Status**: Canonical Reference  
> **Scope**: `packages/practice_workspace/` - Practice file history management  
> **Related**: [Package README](https://github.com/lufftw/neetcode/blob/main/packages/practice_workspace/README.md)

Practice Workspace provides **stateful** management of practice file history and restore operations, enabling users to track their practice attempts over time.

---

## Table of Contents

1. [Overview](#overview)
2. [Scope](#scope)
3. [Interfaces](#interfaces)
4. [How It Fits in the System](#how-it-fits-in-the-system)
5. [Typical Workflows](#typical-workflows)
6. [Key Design Decisions](#key-design-decisions)
7. [File Naming Convention](#file-naming-convention)
8. [Failure Modes and Constraints](#failure-modes-and-constraints)
9. [Related Documentation](#related-documentation)

---

## Overview

Practice Workspace is the **state management layer** for practice files. Unlike `codegen` (stateless generation), this module:

- Tracks practice file versions over time
- Provides history listing with relative timestamps
- Enables restore to any previous version

### Goals

| Goal | Description |
|------|-------------|
| **Version Tracking** | Save practice files to `_history/` directory |
| **History Browsing** | List versions with timestamps and relative time |
| **Easy Restore** | Restore specific or latest version |
| **Minimal Footprint** | Filesystem-only, no external dependencies |

### Non-Goals

| Non-Goal | Reason |
|----------|--------|
| ❌ Generate file content | Handled by `codegen` |
| ❌ Execute tests | Handled by `runner/` |
| ❌ Complex version control | Simple timestamp-based backup |
| ❌ Diff/merge functionality | Out of scope |

---

## Scope

### What this module handles

- ✅ Saving practice files to `_history/` directory
- ✅ Listing historical versions with timestamps
- ✅ Formatting relative time display ("2 hours ago")
- ✅ Restoring specific or latest version
- ✅ Path utilities for practice files

### What this module explicitly avoids

- ❌ File content generation (handled by `codegen`)
- ❌ Test execution (handled by `runner/`)
- ❌ Network operations (filesystem-only)
- ❌ Problem data fetching (handled by `leetcode_datasource`)

---

## Interfaces

High-level summary of public APIs. For complete API reference, see [Package README](https://github.com/lufftw/neetcode/blob/main/packages/practice_workspace/README.md).

| Interface | Purpose |
|-----------|---------|
| `save_to_history()` | Save current practice to history |
| `list_history()` | List all history versions (formatted output) |
| `get_history_entries()` | Get history entries as objects |
| `restore_from_history()` | Restore specific version |
| `restore_latest()` | Restore most recent version |
| `HistoryEntry` | History entry data class |

---

## How It Fits in the System

```
┌────────────────────────────────────────────────────────────┐
│                      Workflow                               │
│                                                             │
│   codegen practice <id>                                     │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────────────────────────────────────────────┐  │
│   │  1. Check if practices/<id>.py exists               │  │
│   │     └── If yes, call practice_workspace.save_to_history │
│   │                                                      │  │
│   │  2. Generate new skeleton                           │  │
│   │                                                      │  │
│   │  3. Write to practices/<id>.py                      │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   User commands: practice history / practice restore        │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────────────────────────────────────────────┐  │
│   │  practice_workspace handles listing/restore         │  │
│   └─────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
practices/
├── 0001_two_sum.py                    # Active practice file
├── 0003_longest_substring.py          # Active practice file
│
└── _history/                          # Version history
    ├── 0001_two_sum.py.20251225_200000.bak
    ├── 0001_two_sum.py.20251230_091500.bak
    ├── 0001_two_sum.py.20251231_143022.bak
    └── 0003_longest_substring.py.20251231_100000.bak
```

### Module Relationships

| Module | Relationship |
|--------|--------------|
| `codegen` | **Used by** - Calls `save_to_history()` before regenerating |
| `runner` | No direct dependency |
| `leetcode_datasource` | No direct dependency |

### Dependency Direction

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   ✅ codegen → practice_workspace                        │
│   ❌ practice_workspace → codegen (FORBIDDEN)            │
│   ❌ practice_workspace → runner  (FORBIDDEN)            │
│                                                          │
│   practice_workspace is filesystem-only                  │
│   (stdlib dependencies only)                             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Typical Workflows

### Workflow: Save to History

When `codegen practice <id>` finds an existing practice file:

```
save_to_history(Path("practices/0001_two_sum.py"))
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  1. Read current practice file content                  │
│  2. Generate timestamp: 20251231_143022                 │
│  3. Create backup filename: 0001_two_sum.py.20251231_143022.bak │
│  4. Write to practices/_history/                        │
│  5. Return backup path                                  │
└─────────────────────────────────────────────────────────┘
```

### Workflow: List History

```
list_history(problem_id=1)
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  1. Find all .bak files for problem 1 in _history/      │
│  2. Parse timestamps from filenames                     │
│  3. Sort by timestamp (oldest first)                    │
│  4. Format relative times ("2 hours ago")               │
│  5. Print formatted list with index numbers             │
└─────────────────────────────────────────────────────────┘
```

**Output Example:**

```
Practice history for 0001_two_sum:

  [1] 20251225_200000  (6 days ago)
  [2] 20251230_091500  (1 day ago)
  [3] 20251231_143022  (2 hours ago)   ← latest

Total: 3 versions
```

### Workflow: Restore Version

```
restore_from_history(problem_id=1, timestamp="20251230_091500")
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  1. Find backup file matching timestamp                 │
│  2. Read backup content                                 │
│  3. Write to practices/0001_two_sum.py                  │
│  4. Return success message                              │
└─────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Stateful design** | History requires persistent state by nature |
| **Filesystem-only** | No database needed; simple backup files |
| **Timestamp-based naming** | Simple, sortable, unique identifiers |
| **Oldest-first display** | Natural chronological order; latest at bottom |
| **No automatic cleanup** | User controls when to delete old versions |
| **Separate from codegen** | Clear responsibility separation |

### Design Philosophy

```
┌─────────────────────────────────────────────────────────┐
│  codegen = stateless                                     │
│  practice_workspace = stateful                           │
│                                                          │
│  This separation allows:                                 │
│  - codegen to focus purely on generation                │
│  - workspace to manage state independently              │
│  - Clear boundaries and testability                     │
└─────────────────────────────────────────────────────────┘
```

---

## File Naming Convention

### Backup Filename Format

```
<original_filename>.<timestamp>.bak
```

### Timestamp Format

```
YYYYMMDD_HHMMSS
```

**Examples:**

| Original | Timestamp | Backup |
|----------|-----------|--------|
| `0001_two_sum.py` | `20251231_143022` | `0001_two_sum.py.20251231_143022.bak` |
| `0003_longest_substring.py` | `20251225_200000` | `0003_longest_substring.py.20251225_200000.bak` |

---

## Failure Modes and Constraints

| Constraint | Behavior |
|------------|----------|
| Practice file not found | Returns error message |
| No history exists | Returns "No history found" |
| Invalid timestamp | Returns "Version not found" |
| `_history/` doesn't exist | Creates directory automatically |
| File permission error | Raises standard Python exception |

---

## Related Documentation

| Document | Content |
|----------|---------|
| [Package README](https://github.com/lufftw/neetcode/blob/main/packages/practice_workspace/README.md) | Quick reference, API details |
| [CodeGen Spec](../codegen/README.md) | How codegen integrates with workspace |
| [Solution Contract](../../contracts/solution-contract.md) | File format requirements |

---

## Appendix: CLI Commands

### practice history

List practice history versions:

```bash
practice history <problem_id>
```

**Output:**

```
Practice history for 0001_two_sum:

  [1] 20251225_200000  (6 days ago)
  [2] 20251230_091500  (1 day ago)
  [3] 20251231_143022  (2 hours ago)   ← latest

Total: 3 versions
```

### practice restore

Restore a specific version:

```bash
# Interactive mode (default)
practice restore <problem_id>

# Restore latest
practice restore <problem_id> --latest

# Restore specific timestamp
practice restore <problem_id> --at 20251230_091500
```

**Interactive Example:**

```
Available versions for 0001_two_sum:

  [1] 20251225_200000  (6 days ago)
  [2] 20251230_091500  (1 day ago)
  [3] 20251231_143022  (2 hours ago)   ← latest

Select version to restore [3]: 2

✅ Restored: practices/0001_two_sum.py
   (from: 20251230_091500)
```

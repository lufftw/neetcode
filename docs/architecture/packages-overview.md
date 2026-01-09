# Packages Architecture Overview

> **Status**: Canonical Reference
> **Scope**: `src/` directory architecture

This document provides an overview of the `src/` directory structure and the relationships between packages.

---

## Directory Structure

```
src/
├── codegen/                    # Solution skeleton generator (Stateless)
│   ├── core/                   # Shared core components
│   ├── reference/              # Reference skeleton generation
│   └── practice/               # Practice skeleton generation
│
├── leetcode_datasource/        # LeetCode data layer
│   ├── models/                 # Data models (Question, ProblemInfo)
│   ├── storage/                # Cache and persistent storage
│   ├── serialization/          # Data serialization
│   └── fetchers/               # Network layer (pluggable)
│
└── practice_workspace/         # Practice file management (Stateful)
    ├── history.py              # History listing
    └── restore.py              # Version restore
```

## Package Responsibilities

| Package | Role | Stateful? |
|---------|------|-----------|
| `codegen` | Generate solution/practice skeletons | No (Stateless) |
| `leetcode_datasource` | Fetch and cache LeetCode data | Yes (Cache + Store) |
| `practice_workspace` | Manage practice history | Yes (Filesystem) |

## Inter-Package Dependencies

```
┌──────────────────┐
│     codegen      │
└────────┬─────────┘
         │ uses
         ▼
┌────────────────────────────┐
│   leetcode_datasource      │
└────────────────────────────┘

┌──────────────────────────┐
│   practice_workspace     │  (independent, filesystem only)
└──────────────────────────┘
```

## Detailed Specifications

For detailed specifications of each package, see:

| Package | Specification |
|---------|---------------|
| codegen | [docs/packages/codegen/README.md](../packages/codegen/README.md) |
| leetcode_datasource | [docs/packages/leetcode_datasource/README.md](../packages/leetcode_datasource/README.md) |
| practice_workspace | [docs/packages/practice_workspace/README.md](../packages/practice_workspace/README.md) |

---

## Related

- [Package Documentation Strategy](../contributors/package-documentation-strategy.md)


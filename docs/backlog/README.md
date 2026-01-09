# Backlog

> **Status**: Persistent Reference
> **Purpose**: Track technical debt, known issues, and items pending resolution
> **Lifecycle**: Items are updated or removed as they are addressed (history preserved in Git)

This directory contains documentation for known gaps, issues, and items that need attention but are not actively being developed.

---

## Purpose

The `docs/backlog/` directory serves as a **persistent tracking area** for:

- **Coverage gaps** — Missing test files, incomplete pattern coverage
- **Known issues** — Environment problems, workarounds needed
- **Technical debt** — Items to clean up or improve
- **Future improvements** — Ideas that aren't prioritized yet

---

## Difference from `in-progress/`

| Aspect | `in-progress/` | `backlog/` |
|--------|----------------|------------|
| **Content** | Features under active development | Issues/gaps pending resolution |
| **Lifecycle** | Removed after completion | Persists until resolved |
| **Structure** | Feature directories with specs | Topic-based documents |
| **Priority** | Active work | Not actively being worked on |

---

## Directory Structure

```
docs/backlog/
├── README.md                      # This file
├── missing-test-files.md          # Solutions without test files
└── environment-issues.md          # Environment setup problems
```

---

## Current Backlog Items

| Document | Description | Items |
|----------|-------------|-------|
| [Missing Test Files](missing-test-files.md) | Solutions that lack `.in/.out` test files | 13 |
| [Environment Issues](environment-issues.md) | Known environment setup problems | 1 |

---

## Workflow

### Adding Items

When you encounter an issue that can't be immediately resolved:

1. Identify the appropriate document (or create a new one)
2. Add the item with context and any relevant details
3. Commit the change

### Resolving Items

When an item is resolved:

1. Remove the item from the document
2. If the document becomes empty, consider removing it
3. Commit with a message referencing the resolution

---

## Notes

- **Persistent**: Unlike `in-progress/`, these documents are not removed after resolution
- **Version Controlled**: All changes are tracked in Git
- **Reference**: Use this for planning and prioritization
- **Low Priority**: Items here are acknowledged but not actively being worked on

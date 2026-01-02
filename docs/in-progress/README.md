# Development in Progress

> **Status**: Temporary Documentation  
> **Purpose**: Track feature specifications and design documents for ongoing development  
> **Lifecycle**: Documents are removed after feature completion and acceptance (history preserved in Git)

This directory contains feature specifications, design documents, and acceptance checklists for features currently under development.

---

## Purpose

The `docs/in-progress/` directory serves as a **temporary staging area** for development documentation:

- ✅ **Track development progress** — Requirements, design decisions, and acceptance criteria
- ✅ **Version control history** — All documents are tracked in Git for future reference
- ✅ **Clear separation** — Keeps development docs separate from canonical documentation
- ✅ **Cleanup workflow** — Removed after completion, but history remains in Git

---

## Directory Structure

Each feature should have its own subdirectory following this structure:

```
docs/in-progress/
├── README.md                    # This file
└── <feature-name>/              # Feature directory (kebab-case)
    ├── specification.md         # Feature requirements and specification (required)
    ├── design.md                # Technical design (optional)
    └── checklist.md             # Acceptance checklist and verification steps (optional)
```

**Note:** Only `specification.md` is required. `design.md` and `checklist.md` are optional and may be omitted if the specification already contains design details and acceptance criteria.

### Naming Convention

- **Feature directories**: Use `kebab-case` (e.g., `new-problem-tests-autogen`)
- **File names**: Use `kebab-case.md` (e.g., `specification.md`, `design.md`, `checklist.md`)

---

## Workflow

### 1. Create Feature Directory

When starting a new feature:

```bash
mkdir -p docs/in-progress/<feature-name>
```

### 2. Add Documentation

Create the necessary documents:

- **`specification.md`** — Feature requirements, scope, and acceptance criteria (required)
- **`design.md`** — Technical design, architecture decisions, API contracts (optional)
- **`checklist.md`** — Acceptance checklist with verification steps (optional)

**Note:** If acceptance criteria are embedded within `specification.md`, a separate `checklist.md` is not required.

### 3. Update During Development

- Update documents as design evolves
- Track implementation progress
- Document decisions and trade-offs

### 4. Complete Acceptance Checklist

Before marking as complete:

- ✅ Verify all acceptance criteria met
- ✅ Run all verification steps (from `checklist.md` if present, or from `specification.md`)
- ✅ Ensure documentation is complete

### 5. Remove After Acceptance

After feature is accepted and merged:

```bash
# Remove the feature directory (Git history is preserved)
rm -rf docs/in-progress/<feature-name>
```

The development history will remain accessible in Git:

```bash
git log --all --full-history -- docs/in-progress/<feature-name>/
```

---

## Example

```
docs/in-progress/new-problem-tests-autogen/
├── specification.md    # Requirements: new problem creation + test autogen
                        # (includes acceptance criteria embedded in spec)
```

**Note:** This feature currently uses a single `specification.md` file that contains both requirements and acceptance criteria. Separate `design.md` and `checklist.md` files are optional and can be added if needed.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [Docs Directory Organization](../contributors/docs-directory-organization.md) | Overall docs structure and organization |
| [Package Documentation Strategy](../contributors/package-documentation-strategy.md) | Package-level documentation standards |

---

## Notes

- ⚠️ **Temporary**: These documents are removed after completion
- 📝 **Version Controlled**: All changes are tracked in Git
- 🔍 **Reference**: Use Git history to reference past development decisions
- 📋 **Complete**: Ensure all acceptance criteria are met before removal


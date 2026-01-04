# Architecture Documentation

> **Status**: Overview  
> **Scope**: System architecture and package relationships

This section documents the overall architecture of the NeetCode Practice Framework.

---

## Package Architecture

The project follows a clean dependency hierarchy:

```
┌─────────────────────────────────────────────────────────────┐
│                    Dependency Direction                      │
│                                                              │
│   ┌──────────┐         ┌──────────────┐                     │
│   │  tools/  │ ──────► │    src/      │                     │
│   └──────────┘         └──────────────┘                     │
│        │                      │                              │
│        │                      ▼                              │
│        │               ┌──────────────┐                     │
│        └─────────────► │   runner/    │                     │
│                        └──────────────┘                     │
│                                                              │
│   ✅ tools → packages                                        │
│   ✅ tools → runner                                          │
│   ❌ packages → tools  (FORBIDDEN)                           │
│   ❌ packages → runner (FORBIDDEN)                           │
└─────────────────────────────────────────────────────────────┘
```

## Core Modules

| Module | Location | Role | Documentation |
|--------|----------|------|---------------|
| **runner** | `runner/` | Test execution engine | [Runner Spec](../runner/README.md) |
| **codegen** | `packages/codegen/` | Solution skeleton generator | [CodeGen Spec](../packages/codegen/README.md) |
| **leetcode_datasource** | `packages/leetcode_datasource/` | LeetCode data layer | [DataSource Spec](../packages/leetcode_datasource/README.md) |
| **practice_workspace** | `packages/practice_workspace/` | Practice file management | [Workspace Spec](../packages/practice_workspace/README.md) |

## Design Principles

| Principle | Description |
|-----------|-------------|
| **Packages are source of truth** | Tools adapt to packages, never the reverse |
| **One-way dependencies** | `tools → packages → (nothing)` |
| **Stateless codegen** | Generation is pure function, no side effects |
| **Stateful workspace** | History and restore managed separately |

## Documentation

| Document | Content |
|----------|---------|
| [packages-overview.md](./packages-overview.md) | Detailed packages architecture |
| [architecture-migration.md](./architecture-migration.md) | Migration history and plans |

---

## Related

- [Package Documentation Strategy](../contributors/package-documentation-strategy.md)
- [Docs Directory Organization](../contributors/docs-directory-organization.md)


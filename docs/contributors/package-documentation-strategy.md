# Package-level Documentation Strategy

> **Status**: Canonical Reference  
> **Scope**: Documentation standards for `packages/` and `runner/`  
> **Audience**: Maintainers, Contributors

This document defines the documentation strategy for core modules in this project. It establishes a dual-layer README approach that separates engineering context from system-level documentation.

---

## Table of Contents

1. [Core Principle](#1-core-principle)
2. [Why Dual-layer READMEs](#2-why-dual-layer-readmes)
3. [Package README Specification](#3-package-readme-specification)
4. [Docs README Specification](#4-docs-readme-specification)
5. [Relationship with runner/](#5-relationship-with-runner)
6. [Anti-patterns](#6-anti-patterns)

---

## 1. Core Principle

> **Packages are the source of truth.**  
> **Tools adapt to packages, never the other way around.**

### Dependency Direction (One-way Only)

```
┌──────────────────────────────────────────────────────────────┐
│                    Allowed Dependencies                       │
│                                                               │
│   ┌──────────┐         ┌──────────────┐                      │
│   │  tools/  │ ──────► │  packages/   │                      │
│   └──────────┘         └──────────────┘                      │
│        │                      │                               │
│        │                      ▼                               │
│        │               ┌──────────────┐                      │
│        └─────────────► │   runner/    │                      │
│                        └──────────────┘                      │
│                                                               │
│   ✅ tools → packages                                         │
│   ✅ tools → runner                                           │
│   ❌ packages → tools  (FORBIDDEN)                            │
│   ❌ packages → runner (FORBIDDEN)                            │
│   ❌ runner → packages (FORBIDDEN)                            │
└──────────────────────────────────────────────────────────────┘
```

### Documentation Implication

| Layer | Can mention tools? | Can mention packages? |
|-------|-------------------|----------------------|
| `packages/<pkg>/README.md` | ❌ **NO** | ✅ Yes (dependencies only) |
| `docs/packages/<pkg>/README.md` | ❌ **NO** | ✅ Yes (system interactions) |
| `tools/<tool>/README.md` | ✅ Yes | ✅ Yes (what it uses) |
| `docs/tools/<tool>/README.md` | ✅ Yes | ✅ Yes |

---

## 2. Why Dual-layer READMEs

The goal is **not** to write more documentation, but to establish a **maintainable documentation system**.

| Layer | Location | Role | Audience |
|-------|----------|------|----------|
| **Package README** | `packages/<pkg>/README.md` | Local quick reference | Engineers reading code directly |
| **Docs README** | `docs/packages/<pkg>/README.md` | System-level specification | People understanding the overall system |

> ⚠️ **Important**: Docs must be under `docs/packages/<pkg>/`, not `docs/<pkg>/`.
> Scattered files like `docs/codegen.md` are NOT allowed.

### Key Distinction

These two layers are **not mirrors**. They are **two perspectives of the same module**:

| Aspect | Package README | Docs README |
|--------|---------------|-------------|
| Perspective | Engineering / Local | Architecture / System |
| Syncs with | Code changes | Design changes |
| Contains | API, file structure, dependencies | Why it exists, system fit, workflows |
| Does NOT contain | System diagrams, workflows | API signatures, implementation details |

---

## 3. Package README Specification

**Location**: `packages/<pkg>/README.md` (or `runner/README.md`)

### 3.1 Role

- Engineering-oriented
- Quick reference
- Syncs with code
- Does NOT describe system flow
- Does NOT describe tools
- Does NOT describe UX

### 3.2 Language

**English only** (全英文)

### 3.3 Required Structure

Every package MUST have these sections:

```markdown
# <Package Name>

## Overview

One or two sentences describing what this package provides.

## Responsibility

### What this package does

- ✅ Explicit responsibility 1
- ✅ Explicit responsibility 2

### What this package does NOT do

- ❌ Explicit non-responsibility 1 (handled by `<other module>`)
- ❌ Explicit non-responsibility 2

## Public API

| Export | Description |
|--------|-------------|
| `function_or_class` | Purpose |
| `AnotherExport` | Purpose |

## File Structure

```
<pkg>/
├── __init__.py          # Public API re-exports
├── core/                # Core logic
│   └── ...
└── utils/               # Utilities
```

## Dependencies

| Direction | Package | Purpose |
|-----------|---------|---------|
| Uses → | `leetcode_datasource` | Problem metadata |
| Uses → | `<other package>` | Reason |

> ❗ **Do NOT list tools here.** Tools depend on packages, not vice versa.

## Related Documentation

- **[Complete Specification](../../docs/packages/<pkg>/README.md)** - System-level documentation

---

## Documentation Maintenance

⚠️ **When modifying this package:**

1. Update this README (quick reference)
2. Update `docs/packages/<pkg>/README.md` (complete specification)
```

### 3.4 Explicitly Forbidden Content

The following MUST NOT appear in Package README:

| ❌ Forbidden | Reason |
|--------------|--------|
| `tools/` references | Violates dependency direction |
| CLI commands | That's tool-level concern |
| User workflows | That's UX-level concern |
| System diagrams | That belongs in Docs README |
| UX / interaction patterns | Not package responsibility |

---

## 4. Docs README Specification

**Location**: `docs/packages/<pkg>/README.md` (or `docs/runner/README.md`)

> ℹ️ **Why `docs/runner/` NOT `docs/packages/runner/`?**
> - `runner/` is at repo root, not under `packages/`
> - Docs structure mirrors code structure
> - Only `packages/<pkg>/` → `docs/packages/<pkg>/`

### 4.1 Role

- System-oriented
- Architecture documentation
- Explains "why this exists"
- Describes interactions with other modules
- Documents design decisions and boundaries

### 4.2 Language

**English primarily** (英文為主)

May include Traditional Chinese notes in specific sections (e.g., Design Notes, Pitfalls) following the runner/ style.

### 4.3 Recommended Structure

```markdown
# <Package Name>

> **Status**: Canonical Reference  
> **Scope**: `<pkg>/` - <one-line description>  
> **Related**: [Package README](https://github.com/lufftw/neetcode/blob/main/packages/<pkg>/README.md)

<Overview paragraph: why this module exists and what problem it solves>

---

## Overview

Expanded description of the module's purpose and place in the system.

## Scope

### What this module handles

- Responsibility 1
- Responsibility 2

### What this module explicitly avoids

- Non-responsibility 1 (handled by `<other>`)

## Interfaces

High-level summary of public APIs. Do NOT duplicate full API docs here.

| Interface | Purpose |
|-----------|---------|
| `main_function()` | Primary entry point |
| `HelperClass` | Supporting functionality |

## How It Fits in the System

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ datasource   │ ──► │   codegen    │ ──► │  workspace   │
└──────────────┘     └──────────────┘     └──────────────┘
```

| Module | Relationship |
|--------|--------------|
| `leetcode_datasource` | Provides problem metadata |
| `runner` | Executes generated solutions |

## Typical Workflows

### Workflow: <Name>

1. Step 1 description
2. Step 2 description
3. Step 3 description

> **Note:** Describe internal/system workflows, not user CLI flows.

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Stateless design | Enables parallel execution |
| Single Source of Truth | `solutions/` as canonical location |

## Failure Modes and Constraints

| Constraint | Behavior |
|------------|----------|
| Missing dependency | Raises `ConfigError` |
| Invalid input | Returns empty result |

## Related Documentation

| Document | Content |
|----------|---------|
| [Package README](../../packages/<pkg>/README.md) | Quick reference, API |
| [Solution Contract](../contracts/solution-contract.md) | File format requirements |
```

### 4.4 Explicitly Forbidden Content

| ❌ Forbidden | Reason |
|--------------|--------|
| Full API reference | Belongs in Package README or docstrings |
| Duplicating Package README | Different perspectives, not mirrors |
| Tool usage details | Tools reference packages, not vice versa |
| CLI flags | Unless the module itself is a CLI |

---

## 5. Relationship with runner/

The `runner/` module is the **reference implementation** for this documentation strategy:

| Aspect | runner/ Example |
|--------|-----------------|
| Package README | `runner/README.md` - Quick Start, Commands, File Structure |
| Docs README | `docs/runner/README.md` - Specification, Architecture, Workflows |

### What "Reference runner/" Means

✅ **Style reference:**
- Clear responsibility definition
- Clear non-responsibility statements
- README not polluted by tools

❌ **NOT a structural reference:**
- Does not mean packages should mirror runner's directory structure
- Does not imply dependency inversion

---

## 6. Anti-patterns

### ❌ Anti-pattern 1: Mentioning tools in package docs

```markdown
<!-- BAD -->
## Used By
- `tools/codegen-cli` calls this package

<!-- GOOD -->
## Dependencies
| Direction | Package | Purpose |
|-----------|---------|---------|
| Uses → | `leetcode_datasource` | Problem data |
```

### ❌ Anti-pattern 2: Duplicating content between layers

```markdown
<!-- BAD: Same content in both files -->
packages/codegen/README.md: "## How It Works: Step 1, Step 2..."
docs/packages/codegen/README.md: "## How It Works: Step 1, Step 2..."

<!-- GOOD: Different perspectives -->
packages/codegen/README.md: "## Public API" (what to call)
docs/packages/codegen/README.md: "## Typical Workflows" (system-level flow)
```

### ❌ Anti-pattern 3: Scattered package docs at docs root

```markdown
<!-- BAD: Package docs at docs/ root -->
docs/codegen.md
docs/leetcode_datasource.md

<!-- GOOD: Package docs under docs/packages/ -->
docs/packages/codegen/README.md
docs/packages/leetcode_datasource/README.md
```

### ❌ Anti-pattern 4: Writing CLI docs in package README

```markdown
<!-- BAD -->
## Usage
```bash
python -m tools.codegen --problem 1
```

<!-- GOOD -->
## Public API
```python
from codegen import generate_reference_skeleton
generate_reference_skeleton(problem_id=1)
```
```

---

## Summary

| Principle | Description |
|-----------|-------------|
| **Packages are source of truth** | Tools adapt to packages |
| **One-way dependency** | `tools → packages`, never reverse |
| **Dual-layer, not duplicate** | Different perspectives, not mirrors |
| **Package README = Engineering** | API, structure, local context |
| **Docs README = Architecture** | System fit, workflows, design decisions |

---

## Related Documents

| Document | Content |
|----------|---------|
| [Docs Directory Organization](./docs-directory-organization.md) | `docs/` folder structure and migration |
| [Documentation Architecture](./documentation-architecture.md) | Overall documentation principles |

---

## Appendix: Migration Notes

When migrating existing documentation to this dual-layer structure:

1. **Identify API-heavy content** → Move to Package README (`packages/<pkg>/README.md`)
2. **Identify system context** → Keep/move to Docs README (`docs/packages/<pkg>/README.md`)
3. **Chinese content** → Gradually convert to English primarily; Chinese notes acceptable in specific sections
4. **Avoid duplication** → Each layer serves a different audience and purpose


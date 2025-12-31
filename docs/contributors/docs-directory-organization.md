# Docs Directory Organization

> **Status**: Canonical Reference  
> **Scope**: `docs/` folder structure and organization  
> **Audience**: Maintainers, Contributors

This document defines the organization of the `docs/` directory, including folder purposes, naming conventions, and the target structure for documentation.

---

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Target Directory Structure](#2-target-directory-structure)
3. [Folder Purposes](#3-folder-purposes)
4. [File Placement Guidelines](#4-file-placement-guidelines)
5. [MkDocs Infrastructure](#5-mkdocs-infrastructure)
6. [Migration Plan](#6-migration-plan) *(Remove after completion)*
7. [Migration Checklist](#7-migration-checklist) *(Remove after completion)*

---

## 1. Design Principles

### 1.1 Separation of Concerns

| Category | Location | Purpose |
|----------|----------|---------|
| **MkDocs Infrastructure** | `docs/.mkdocs/` | Theme, styles, assets, config |
| **Package Documentation** | `docs/packages/<pkg>/` | System-level specs for core modules |
| **Contracts & Standards** | `docs/contracts/` | Cross-cutting specifications |
| **How-to Guides** | `docs/guides/` | Step-by-step tutorials |
| **Contributor Docs** | `docs/contributors/` | Development guidelines |
| **Content** | `docs/patterns/`, `docs/mindmaps/` | User-facing educational content |
| **Tools Documentation** | `docs/tools/` | Tool-specific documentation |

### 1.2 Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Folders | `snake_case` or `kebab-case` | `leetcode_datasource/`, `two_pointers/` |
| Files | `kebab-case.md` | `solution-contract.md` |
| Package folders | Match package name exactly | `docs/packages/codegen/` matches `packages/codegen/` |

### 1.3 Root-level Files

Only these files should remain at `docs/` root:

| File | Purpose | Reason |
|------|---------|--------|
| `index.md` | MkDocs landing page | Required by MkDocs |
| `index_zh-TW.md` | Chinese landing page | Localization |
| `authors.yml` | Author definitions | Required by document-dates plugin |
| `robots.txt` | SEO | Must be served at site root |
| `BingSiteAuth.xml` | Bing verification | Must be served at site root |
| `google*.html` | Google verification | Must be served at site root |

Additionally, `pages/` must remain at `docs/pages/` (generated mindmap HTML output).

All other `.md` files MUST be placed in appropriate subdirectories.

---

## 2. Target Directory Structure

```
docs/
├── index.md                              # MkDocs landing page
├── index_zh-TW.md                        # Chinese landing page
├── robots.txt                            # SEO (must be at root)
├── BingSiteAuth.xml                      # Bing verification
├── google8e4b975a9b708272.html           # Google verification
│
├── .mkdocs/                              # ═══ MkDocs Infrastructure ═══
│   ├── assets/                           # Static assets
│   │   ├── avatar/                       # Author avatars
│   │   └── document_dates/               # Plugin config
│   ├── overrides/                        # Theme overrides
│   └── stylesheets/                      # Custom CSS
│
├── authors.yml                           # Author definitions (plugin requires root)
├── pages/                                # Generated HTML (mindmaps) - DO NOT MOVE
│
├── contracts/                            # ═══ Cross-cutting Contracts ═══
│   ├── solution-contract.md              # Solution file requirements
│   ├── generator-contract.md             # Generator file requirements
│   └── documentation-header-spec.md      # Doc header standards
│
├── guides/                               # ═══ How-to Guides ═══
│   ├── act-local-github-actions.md       # Run GitHub Actions locally
│   ├── build-docs-manual.md              # Build docs manually
│   ├── github-pages-setup.md             # GitHub Pages setup
│   ├── local-docs-build.md               # Local docs build options
│   └── mkdocs-content-guide.md           # MkDocs content authoring
│
├── contributors/                         # ═══ Contributor Documentation ═══
│   ├── README.md                         # Contributor overview
│   ├── testing.md                        # Testing documentation
│   ├── vscode-setup.md                   # VSCode configuration
│   ├── virtual-env-setup.md              # Virtual environment setup
│   ├── documentation-architecture.md     # Doc architecture principles
│   ├── documentation-naming.md           # Naming conventions
│   ├── package-documentation-strategy.md # Package doc strategy (NEW)
│   └── docs-directory-organization.md    # This file (NEW)
│
├── architecture/                         # ═══ Architecture Documentation ═══
│   ├── README.md                         # Architecture overview
│   ├── packages-overview.md              # Packages architecture summary
│   └── architecture-migration.md         # Migration documentation
│
├── runner/                               # ═══ Runner Module ═══
│   ├── README.md                         # Runner specification
│   ├── cli-output-contract.md            # CLI output format
│   ├── benchmarking/                     # Benchmarking docs
│   │   └── memory-metrics.md
│   └── profiling/                        # Profiling docs
│       ├── cli-output-memory.md
│       └── input-scale-metrics.md
│
├── packages/                             # ═══ Package Documentation ═══
│   ├── codegen/                          # CodeGen specification
│   │   └── README.md
│   ├── leetcode_datasource/              # DataSource specification
│   │   └── README.md
│   └── practice_workspace/               # Workspace specification
│       └── README.md
│
├── patterns/                             # ═══ Algorithm Patterns ═══
│   ├── README.md                         # Patterns overview
│   ├── sliding_window/
│   ├── two_pointers/
│   └── backtracking_exploration/
│
├── mindmaps/                             # ═══ Mind Maps ═══
│   ├── index.md                          # Mindmaps landing page
│   └── *.md                              # Individual mindmaps
│
├── tools/                                # ═══ Tools Documentation ═══
│   ├── README.md                         # Tools overview
│   ├── leetcode-api/
│   ├── mindmaps/
│   ├── patterndocs/
│   ├── review-code/
│   ├── docstring/
│   └── maintenance/
│
└── reference/                            # ═══ Reference Documents ═══ (NEW)
    └── ontology-design.md                # Ontology design reference
```

---

## 3. Folder Purposes

### 3.1 `.mkdocs/` — MkDocs Infrastructure

Contains all MkDocs-related configuration and assets that are NOT documentation content.

| Subfolder | Purpose |
|-----------|---------|
| `assets/` | Static files (avatars, images, plugin configs) |
| `overrides/` | MkDocs Material theme customizations |
| `stylesheets/` | Custom CSS files |
| `pages/` | Generated HTML output (mindmaps) |
| `authors.yml` | Author definitions for document-dates plugin |

**Why `.mkdocs/`?**
- Prefix `.` indicates infrastructure, not content
- Many MkDocs plugins cannot access repo root
- Keeps content docs clean from infrastructure files

### 3.2 `contracts/` — Cross-cutting Contracts

Specifications that apply across multiple modules.

| File | Scope |
|------|-------|
| `solution-contract.md` | Solution file format (affects `solutions/`, `runner/`) |
| `generator-contract.md` | Generator file format (affects `generators/`, `runner/`) |
| `documentation-header-spec.md` | Document header format (affects all docs) |

### 3.3 `guides/` — How-to Guides

Step-by-step tutorials for specific tasks. NOT specifications or contracts.

| Characteristic | Description |
|----------------|-------------|
| Verb-oriented | "How to do X" |
| Task-focused | Single goal per guide |
| Not normative | Doesn't define standards |

### 3.4 `contributors/` — Contributor Documentation

Documentation for project maintainers and contributors.

| Focus | Examples |
|-------|----------|
| Development setup | `vscode-setup.md`, `virtual-env-setup.md` |
| Testing | `testing.md` |
| Documentation standards | `package-documentation-strategy.md`, this file |

### 3.5 `architecture/` — Architecture Documentation

High-level architecture documentation that spans multiple modules.

| File | Purpose |
|------|---------|
| `README.md` | Architecture overview |
| `packages-overview.md` | Summary of packages architecture |
| `architecture-migration.md` | Migration plans and history |

### 3.6 Package Folders (`docs/packages/<pkg>/`, `docs/runner/`)

System-level documentation for core modules. See [Package Documentation Strategy](./package-documentation-strategy.md).

| Folder | Corresponds to |
|--------|----------------|
| `docs/runner/` | `runner/` |
| `docs/packages/codegen/` | `packages/codegen/` |
| `docs/packages/leetcode_datasource/` | `packages/leetcode_datasource/` |
| `docs/packages/practice_workspace/` | `packages/practice_workspace/` |

> ⚠️ **Important**: Package docs must be under `docs/packages/<pkg>/`, not `docs/<pkg>/`.
> Scattered files like `docs/codegen.md` are NOT allowed.

> ℹ️ **Why `docs/runner/` stays at `docs/runner/` (NOT `docs/packages/runner/`)?**
> - `runner/` is at repo root, not under `packages/`
> - Docs structure mirrors code structure: `runner/` → `docs/runner/`
> - Only modules under `packages/` go to `docs/packages/`

---

## 4. File Placement Guidelines

### Decision Tree

```
Is it MkDocs infrastructure (styles, assets, config)?
├── YES → docs/.mkdocs/
└── NO ↓

Is it a cross-cutting specification/contract?
├── YES → docs/contracts/
└── NO ↓

Is it a how-to guide (step-by-step tutorial)?
├── YES → docs/guides/
└── NO ↓

Is it for contributors/maintainers only?
├── YES → docs/contributors/
└── NO ↓

Is it architecture-level (spans multiple modules)?
├── YES → docs/architecture/
└── NO ↓

Is it about a specific package/module?
├── YES → docs/packages/<pkg>/
└── NO ↓

Is it educational content (patterns, mindmaps)?
├── YES → docs/patterns/ or docs/mindmaps/
└── NO ↓

Is it about a tool?
├── YES → docs/tools/<tool>/
└── NO → Discuss with maintainers
```

### Common Mistakes

| ❌ Wrong | ✅ Correct | Reason |
|----------|-----------|--------|
| `docs/codegen-spec.md` | `docs/packages/codegen/README.md` | Package docs go in package folder |
| `docs/solution-contract.md` | `docs/contracts/solution-contract.md` | Contracts go in contracts/ |
| `docs/act-local-github-actions.md` | `docs/guides/act-local-github-actions.md` | How-to guides go in guides/ |
| `docs/stylesheets/` | `docs/.mkdocs/stylesheets/` | Infrastructure goes in .mkdocs/ |

---

## 5. MkDocs Infrastructure

### 5.1 Configuration Updates

When moving infrastructure to `docs/.mkdocs/`, update `mkdocs.yml`:

```yaml
# Before
theme:
  custom_dir: docs/overrides

extra_css:
  - stylesheets/extra.css

# After
theme:
  custom_dir: docs/.mkdocs/overrides

extra_css:
  - .mkdocs/stylesheets/extra.css
```

### 5.2 Plugin Configuration

Update any plugins that reference infrastructure paths:

| Plugin | Config Key | New Path |
|--------|------------|----------|
| `document-dates` | (internal) | `docs/.mkdocs/authors.yml` |
| `theme` | `custom_dir` | `docs/.mkdocs/overrides` |

---

## 6. Migration Plan

> ⚠️ **REMOVE THIS SECTION AFTER MIGRATION IS COMPLETE**

### 6.1 Phase 1: Create New Structure

Create new directories:

```bash
# MkDocs infrastructure
mkdir -p docs/.mkdocs/assets
mkdir -p docs/.mkdocs/overrides
mkdir -p docs/.mkdocs/stylesheets
mkdir -p docs/.mkdocs/pages

# Documentation folders
mkdir -p docs/contracts
mkdir -p docs/guides
mkdir -p docs/architecture
mkdir -p docs/packages/codegen
mkdir -p docs/packages/leetcode_datasource
mkdir -p docs/packages/practice_workspace
mkdir -p docs/reference
```

### 6.2 Phase 2: Move MkDocs Infrastructure

| From | To | Note |
|------|-----|------|
| `docs/assets/` | `docs/.mkdocs/assets/` | |
| `docs/overrides/` | `docs/.mkdocs/overrides/` | |
| `docs/stylesheets/` | `docs/.mkdocs/stylesheets/` | |
| `docs/pages/` | **DO NOT MOVE** | Generated output, stays in place |
| `docs/authors.yml` | **DO NOT MOVE** | Plugin requires root location |

### 6.3 Phase 3: Move Contracts

| From | To |
|------|-----|
| `docs/solution-contract.md` | `docs/contracts/solution-contract.md` |
| `docs/generator-contract.md` | `docs/contracts/generator-contract.md` |
| `docs/documentation-header-spec.md` | `docs/contracts/documentation-header-spec.md` |

### 6.4 Phase 4: Move Guides

| From | To |
|------|-----|
| `docs/act-local-github-actions.md` | `docs/guides/act-local-github-actions.md` |
| `docs/build-docs-manual.md` | `docs/guides/build-docs-manual.md` |
| `docs/github-pages-setup.md` | `docs/guides/github-pages-setup.md` |
| `docs/local-docs-build.md` | `docs/guides/local-docs-build.md` |
| `docs/mkdocs-content-guide.md` | `docs/guides/mkdocs-content-guide.md` |

### 6.5 Phase 5: Move Architecture Docs

| From | To |
|------|-----|
| `docs/architecture-migration.md` | `docs/architecture/architecture-migration.md` |
| `docs/packages-architecture-spec.md` | Split: overview → `docs/architecture/packages-overview.md`, details → `docs/packages/leetcode_datasource/README.md` |

### 6.6 Phase 6: Move Reference Docs

| From | To |
|------|-----|
| `docs/ontology-design.md` | `docs/reference/ontology-design.md` |

### 6.7 Phase 7: Create Package Docs

Create placeholder README.md files:

| File | Source |
|------|--------|
| `docs/packages/codegen/README.md` | New (merge content from `docs/codegen-spec.md`) |
| `docs/packages/leetcode_datasource/README.md` | New (extract from `packages-architecture-spec.md`) |
| `docs/packages/practice_workspace/README.md` | New |
| `docs/architecture/README.md` | New |

### 6.8 Phase 8: Update mkdocs.yml

Update all path references in `mkdocs.yml`:

1. `theme.custom_dir`
2. `extra_css`
3. `nav` section (all moved files)

### 6.9 Phase 9: Delete Old Files

After verifying everything works:

1. Delete `docs/codegen-spec.md` (merged into `docs/packages/codegen/README.md`)
2. Delete moved files from original locations
3. Verify no broken links

### 6.10 Phase 10: Cleanup

1. Remove this Migration Plan section from this document
2. Remove the Migration Checklist section
3. Update `mkdocs.yml` nav if needed

---

## 7. Migration Checklist

> ⚠️ **REMOVE THIS SECTION AFTER MIGRATION IS COMPLETE**

### Phase 1: Create Structure

- [x] Create `docs/.mkdocs/assets/`
- [x] Create `docs/.mkdocs/overrides/`
- [x] Create `docs/.mkdocs/stylesheets/`
- [x] ~~Create `docs/.mkdocs/pages/`~~ (not needed, stays in docs/)
- [x] Create `docs/contracts/`
- [x] Create `docs/guides/`
- [x] Create `docs/architecture/`
- [x] Create `docs/packages/codegen/`
- [x] Create `docs/packages/leetcode_datasource/`
- [x] Create `docs/packages/practice_workspace/`
- [x] Create `docs/reference/`

### Phase 2: Move MkDocs Infrastructure

- [x] Move `docs/assets/` → `docs/.mkdocs/assets/`
- [x] Move `docs/overrides/` → `docs/.mkdocs/overrides/`
- [x] Move `docs/stylesheets/` → `docs/.mkdocs/stylesheets/`
- [x] Keep `docs/pages/` in place (DO NOT MOVE - generated output)
- [x] Keep `docs/authors.yml` in place (plugin requires root)

### Phase 3: Move Contracts

- [x] Move `docs/solution-contract.md` → `docs/contracts/`
- [x] Move `docs/generator-contract.md` → `docs/contracts/`
- [x] Move `docs/documentation-header-spec.md` → `docs/contracts/`

### Phase 4: Move Guides

- [x] Move `docs/act-local-github-actions.md` → `docs/guides/`
- [x] Move `docs/build-docs-manual.md` → `docs/guides/`
- [x] Move `docs/github-pages-setup.md` → `docs/guides/`
- [x] Move `docs/local-docs-build.md` → `docs/guides/`
- [x] Move `docs/mkdocs-content-guide.md` → `docs/guides/`

### Phase 5: Move Architecture Docs

- [x] Move `docs/architecture-migration.md` → `docs/architecture/`
- [x] Handle `docs/packages-architecture-spec.md`:
  - [x] Create `docs/architecture/packages-overview.md` (summary)
  - [x] Move to `docs/packages/leetcode_datasource/README.md` (detailed spec)

### Phase 6: Move Reference Docs

- [x] Move `docs/ontology-design.md` → `docs/reference/`

### Phase 7: Create Package Docs

- [x] Create `docs/packages/codegen/README.md` (from `codegen-spec.md`)
- [x] Create `docs/packages/leetcode_datasource/README.md` (from `packages-architecture-spec.md`)
- [x] Create `docs/packages/practice_workspace/README.md` (placeholder)
- [x] Create `docs/architecture/README.md`

### Phase 8: Update mkdocs.yml

- [x] Update `theme.custom_dir` path
- [x] Update `extra_css` path
- [x] Update all `nav` entries for moved files
- [x] Add new sections (Architecture, Packages)

### Phase 9: Verify & Delete

- [ ] Build docs locally: `mkdocs serve`
- [ ] Verify all links work
- [x] Delete `docs/codegen-spec.md` (moved to codegen/README.md)
- [x] Delete old infrastructure directories (assets, overrides, stylesheets)

### Phase 10: Cleanup

- [ ] Remove Section 6 (Migration Plan) from this document
- [ ] Remove Section 7 (Migration Checklist) from this document
- [ ] Commit with message: `docs: complete docs/ directory reorganization`

---

## Related Documents

| Document | Content |
|----------|---------|
| [Package Documentation Strategy](./package-documentation-strategy.md) | Package-level documentation standards |
| [Documentation Architecture](./documentation-architecture.md) | Overall documentation principles |


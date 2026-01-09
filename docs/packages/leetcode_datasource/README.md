# LeetCode DataSource

> **Status**: Canonical Reference  
> **Scope**: `src/leetcode_datasource/` - LeetCode problem data layer  
> **Related**: [Package README](https://github.com/lufftw/neetcode/blob/main/src/leetcode_datasource/README.md)

LeetCode DataSource provides a unified data layer for accessing LeetCode problem metadata with caching, persistent storage, and pluggable network fetching.

---

## Table of Contents

1. [Overview](#overview)
2. [Scope](#scope)
3. [Interfaces](#interfaces)
4. [How It Fits in the System](#how-it-fits-in-the-system)
5. [Architecture](#architecture)
6. [Typical Workflows](#typical-workflows)
7. [Key Design Decisions](#key-design-decisions)
8. [Data Directory Strategy](#data-directory-strategy)
9. [Configuration](#configuration)
10. [Failure Modes and Constraints](#failure-modes-and-constraints)
11. [Related Documentation](#related-documentation)

---

## Overview

LeetCode DataSource is the **data foundation** for the NeetCode practice framework. It provides:

- Clean API for accessing LeetCode problem data
- Multi-layer caching (memory → SQLite → network)
- Problem index for ID resolution (frontend_id ↔ slug)
- Structured data models for consistent access

### Goals

| Goal | Description |
|------|-------------|
| **Unified Access** | Single API for all problem data needs |
| **Global Importability** | `from leetcode_datasource import ...` anywhere in repo |
| **No sys.path Hacks** | Proper package setup via pyproject.toml |
| **Clear Dependencies** | `tools/ → packages/` only, never reverse |
| **Incremental Migration** | Works alongside existing tools |

### Non-Goals

| Non-Goal | Reason |
|----------|--------|
| ❌ Replace `tools/leetcode-api/` immediately | Gradual migration planned |
| ❌ Generate solution files | Handled by `codegen` |
| ❌ Execute tests | Handled by `runner/` |
| ❌ Implement `testgen` | Future work |

---

## Scope

### What this module handles

- ✅ Fetching LeetCode question metadata (title, description, examples)
- ✅ Caching for fast repeated access
- ✅ SQLite storage for persistence
- ✅ ID resolution (frontend_id ↔ slug)
- ✅ Problem index synchronization
- ✅ Structured data models

### What this module explicitly avoids

- ❌ Solution generation (handled by `codegen`)
- ❌ Test execution (handled by `runner/`)
- ❌ History management (handled by `practice_workspace`)
- ❌ CLI interfaces (handled by `tools/`)

---

## Interfaces

High-level summary of public APIs. For complete API reference, see [Package README](https://github.com/lufftw/neetcode/blob/main/src/leetcode_datasource/README.md).

| Interface | Purpose |
|-----------|---------|
| `LeetCodeDataSource` | Main data source class |
| `get_by_slug()` | Get question by URL slug |
| `get_by_frontend_id()` | Get question by problem number |
| `sync_problem_list()` | Sync problem index from LeetCode API |
| `get_slug()` / `get_frontend_id()` | Quick ID lookups |
| `Question` | Question data model |
| `ProblemInfo` | Minimal problem metadata |

---

## How It Fits in the System

```
┌─────────────────────────────────────────────────────────────┐
│                    Dependency Direction                      │
│                                                              │
│   ┌──────────┐         ┌──────────────────────────┐         │
│   │  tools/  │ ──────► │       src/               │         │
│   └──────────┘         │  └─ leetcode_datasource  │         │
│        │               └──────────────────────────┘         │
│        │                      │                              │
│        │                      ▼                              │
│        │               ┌──────────────┐                     │
│        └─────────────► │   runner/    │                     │
│                        └──────────────┘                     │
│                                                              │
│   ✅ tools → leetcode_datasource                            │
│   ✅ codegen → leetcode_datasource                          │
│   ❌ leetcode_datasource → tools  (FORBIDDEN)               │
│   ❌ leetcode_datasource → runner (FORBIDDEN)               │
└─────────────────────────────────────────────────────────────┘
```

### Module Relationships

| Module | Relationship |
|--------|--------------|
| `codegen` | **Used by** - Fetches problem metadata for generation |
| `practice_workspace` | No direct dependency |
| `runner` | No direct dependency |

### Related Tools

| Tool | Relationship |
|------|--------------|
| `tools/leetcode-api/` | Legacy API layer (uses SQLite cache) |
| `tools/docstring/` | HTML parser for docstrings (consumes this package) |
| `tools/review-code/` | Docstring fixer (consumes this package) |

---

## Architecture

### Module Structure

```
src/leetcode_datasource/
├── __init__.py              # Public API exports
├── datasource.py            # LeetCodeDataSource main class
├── config.py                # DataSourceConfig
├── exceptions.py            # Custom exceptions
│
├── models/                  # Data models
│   ├── question.py          # Question dataclass
│   ├── problem_info.py      # ProblemInfo dataclass
│   └── schema.py            # Schema versioning
│
├── storage/                 # Storage layer
│   ├── cache.py             # Memory/JSON cache
│   └── store.py             # SQLite persistent store
│
├── serialization/           # Serialization
│   └── question_serializer.py
│
└── fetchers/                # Network layer (pluggable)
    └── leetscrape_fetcher.py
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    LeetCodeDataSource                        │
│                                                              │
│   get_by_slug("two-sum")                                    │
│         │                                                    │
│         ▼                                                    │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│   │   Cache     │ ──► │   Store     │ ──► │   Fetcher   │   │
│   │  (memory)   │     │  (SQLite)   │     │  (network)  │   │
│   └─────────────┘     └─────────────┘     └─────────────┘   │
│         │                   │                   │            │
│         └───────────────────┴───────────────────┘            │
│                             │                                │
│                             ▼                                │
│                      Question object                         │
└─────────────────────────────────────────────────────────────┘
```

### Database Schema

```
leetcode.sqlite3
├── questions          # Full question data (~2224 rows)
│   ├── id (PK)
│   ├── qid            # frontend_question_id
│   ├── titleSlug
│   ├── title
│   ├── Body, Code, Hints...
│   └── ...
│
└── problem_index      # ID mappings (~3778 rows)
    ├── frontend_question_id (PK)
    ├── title_slug (UNIQUE)
    ├── title
    ├── difficulty
    ├── paid_only
    └── ...
```

> **Note**: `problem_index` contains minimal metadata for all problems; `questions` contains full details for fetched problems only.

---

## Typical Workflows

### Workflow: Fetch Question by Slug

```
ds.get_by_slug("two-sum")
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  1. Check cache (memory)                                │
│     └── Hit? Return cached Question                     │
│                                                         │
│  2. Check store (SQLite)                                │
│     └── Hit? Cache it, return Question                  │
│                                                         │
│  3. Fetch from network (LeetScrape)                     │
│     └── Store to SQLite, cache it, return Question      │
└─────────────────────────────────────────────────────────┘
```

### Workflow: Resolve Frontend ID

```
ds.get_slug(frontend_id=1)
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  1. Query problem_index table by frontend_question_id   │
│     └── Return title_slug                               │
└─────────────────────────────────────────────────────────┘
```

### Workflow: Sync Problem Index

```
ds.sync_problem_list()
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  1. Fetch from https://leetcode.com/api/problems/all/   │
│  2. UPSERT all problems to problem_index table          │
│  3. Update cache/problem_list.json (fallback)           │
│  4. Return count of problems synced                     │
└─────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **SQLite as canonical store** | Single source of truth, indexed, transactional |
| **No standalone mapping files** | All ID resolution through Store API |
| **Pluggable fetcher design** | Allow future replacement without core changes |
| **LeetScrape field names** | Compatibility with existing data |
| **Schema versioning** | Forward/backward compatible data evolution |
| **Lazy loading for Body** | Large fields loaded on access only |

### Problem Index Design

> **No standalone mapping files are considered canonical.**  
> **All identifier resolution must go through the Store-backed `problem_index`.**

| Decision | Rationale |
|----------|-----------|
| ❌ No standalone JSON mapping | Avoid bypassing, hard to maintain consistency |
| ✅ Unified in SQLite | Single source of truth, indexable |
| ✅ Consistent API | All ID resolution through Store |

---

## Data Directory Strategy

### Principle

> **Runtime data stays outside repo and package directories**

| Data Type | Location | Git Status | Can Delete? |
|-----------|----------|------------|-------------|
| Cache | `.neetcode/leetcode_datasource/cache/` | gitignored | ✅ Yes |
| Store | `.neetcode/leetcode_datasource/store/` | optional | ⚠️ Careful |

### Directory Structure

```
.neetcode/
└── leetcode_datasource/
    ├── cache/                        # Ephemeral, rebuildable
    │   ├── problem_list.json         # Internal-only (sync fallback)
    │   └── leetcode_cache_meta.json
    │
    └── store/                        # Persistent (canonical)
        └── leetcode.sqlite3
```

---

## Configuration

### DataSourceConfig Options

| Option | Default | Description |
|--------|---------|-------------|
| `data_dir` | Auto-detected | Root directory for data storage |
| `cache_enabled` | `True` | Enable memory/file cache |
| `cache_ttl_hours` | `168` (1 week) | Cache time-to-live |
| `fetch_timeout` | `30` | Network timeout in seconds |
| `rate_limit_delay` | `0.5` | Delay between requests |

### Data Directory Resolution Priority

1. **Explicit**: `DataSourceConfig(data_dir=Path("/custom"))`
2. **Environment**: `NEETCODE_DATA_DIR=/path/to/data`
3. **Repo Local**: `.neetcode/` in repo root
4. **platformdirs**: `~/.local/share/neetcode/` (Linux)

---

## Failure Modes and Constraints

| Constraint | Behavior |
|------------|----------|
| Question not found (cache + network) | Raises `QuestionNotFoundError` |
| Network failure | Raises `NetworkError` |
| Data parsing failure | Raises `ParseError` |
| Configuration error | Raises `ConfigError` |
| Cache error | Non-fatal (logged, not raised) |

### Exception Hierarchy

```
LeetCodeDataSourceError (base)
├── QuestionNotFoundError
├── NetworkError
├── ParseError
└── ConfigError
```

---

## Related Documentation

| Document | Content |
|----------|---------|
| [Package README](https://github.com/lufftw/neetcode/blob/main/src/leetcode_datasource/README.md) | Quick reference, API details |
| [CodeGen Spec](../codegen/README.md) | Consumer of this data |
| [Architecture Overview](../../architecture/packages-overview.md) | System architecture |

---

## Appendix: Data Model

### Question Fields

| Field | Type | Description |
|-------|------|-------------|
| `frontend_question_id` | `int` | Problem number (1, 2, 922...) |
| `titleSlug` | `str` | URL slug ("two-sum") |
| `title` | `str` | Display title ("Two Sum") |
| `difficulty` | `str` | "Easy", "Medium", "Hard" |
| `Body` | `str` | HTML problem description |
| `Code` | `str` | Code template/stubs |
| `Hints` | `List[str]` | Hint strings |
| `topicTags` | `str` | Comma-separated tags |

### ProblemInfo Fields

| Field | Type | Description |
|-------|------|-------------|
| `frontend_question_id` | `int` | Problem number |
| `title_slug` | `str` | URL slug |
| `title` | `str` | Display title |
| `difficulty` | `str` | Difficulty level |
| `paid_only` | `bool` | Premium flag |

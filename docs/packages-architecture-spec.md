# Packages Architecture Specification

> **Status**: Draft  
> **Branch**: `refactor/monorepo-packages`  
> **Scope**: `packages/` 架構 + `leetcode_datasource` 模組  
> **Last Updated**: 2025-12-31

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Package Design: leetcode_datasource](#3-package-design-leetcode_datasource)
4. [Data Model](#4-data-model)
5. [Data Directory Strategy](#5-data-directory-strategy)
6. [Configuration](#6-configuration)
7. [Migration Plan](#7-migration-plan)
8. [Future Work](#8-future-work)

---

## 1. Overview

### 1.1 Goals

本次重構的目標：

| Goal | Description |
|------|-------------|
| **建立 `packages/` 目錄** | 作為「可重用核心模組」的容器 |
| **全局可 import** | 在 repo 任意地方 `from leetcode_datasource import ...` |
| **消除 sys.path hack** | 不再需要 `sys.path.insert(...)` |
| **清楚的依賴方向** | `tools/ → packages/` ✅，反向 ❌ |
| **漸進式遷移** | 先建立 packages，後續再讓 tools 依賴它 |

### 1.2 Non-Goals (Out of Scope)

本次**不做**的事項：

| Non-Goal | Reason |
|----------|--------|
| 修改 `tools/leetcode-api/` | 先分離，後續再整合 |
| 遷移 `runner/` 到 packages | runner 是框架核心，保持獨立 |
| 實作 `packages/testgen/` | 僅保留 placeholder，後續討論 |
| 讓 tools 使用 packages | 分離完成後再進行 |

### 1.3 Success Criteria

重構完成的驗收標準：

```python
# ✅ 在 repo 任意地方都能執行
from leetcode_datasource import LeetCodeDataSource

ds = LeetCodeDataSource()
q = ds.get_by_slug("two-sum")
print(q.title)  # "Two Sum"

# ✅ 不需要任何 sys.path.insert(...)
```

### 1.4 Terminology

| Term | Definition |
|------|------------|
| `packages/` | 可重用核心模組目錄，乾淨 API，可被 import |
| `tools/` | CLI / wrapper / glue code，不承諾被 import |
| `frontend_question_id` | 使用者在 LeetCode 網站看到的題號（如 1, 922） |
| `title_slug` | URL slug（如 `"two-sum"`, `"sort-array-by-parity-ii"`） |
| `DataSource` | 資料來源的抽象概念（cache + store + fetcher） |

---

## 2. Architecture

### 2.1 Directory Structure (Target State)

```
neetcode/
├── .neetcode/                          # Runtime data (gitignored selectively)
│   ├── leetcode_datasource/
│   │   ├── cache/                      # Ephemeral (can be deleted)
│   │   │   ├── leetcode_problems.json
│   │   │   └── leetcode_cache_meta.json
│   │   └── store/                      # Persistent
│   │       └── leetcode.sqlite3
│   └── README.md                       # Explain this directory
│
├── packages/                           # ✨ NEW: Reusable core modules
│   ├── __init__.py
│   └── leetcode_datasource/            # LeetCode data layer
│       ├── __init__.py
│       ├── datasource.py
│       ├── config.py
│       ├── exceptions.py
│       ├── models/
│       ├── storage/
│       ├── serialization/
│       └── fetchers/
│
├── runner/                             # Core test runner (unchanged)
├── tools/                              # CLI / wrappers
│   └── leetcode-api/                   # Kept as CLI wrapper (not imported)
├── solutions/
├── generators/
├── tests/
└── pyproject.toml                      # Updated to include packages/*
```

### 2.2 Dependency Direction

```
┌─────────────────────────────────────────────────────────────┐
│                    Allowed Dependencies                      │
│                                                              │
│   ┌──────────┐         ┌──────────────┐                     │
│   │  tools/  │ ──────► │  packages/   │                     │
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
│   ❌ tools ↔ tools     (AVOID)                               │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Role Separation

| Directory | Role | Can be Imported? | Naming Convention |
|-----------|------|------------------|-------------------|
| `packages/` | Reusable core, clean API | ✅ Yes | `snake_case` |
| `tools/` | CLI, wrapper, glue code | ❌ No (not promised) | `kebab-case` OK |
| `runner/` | Framework core | ✅ Yes | `snake_case` |

### 2.4 pyproject.toml Changes

```toml
[tool.setuptools.packages.find]
include = ["generators*", "mkdocs_plugins*", "runner*", "packages*"]
#                                                        ^^^^^^^^^ NEW
exclude = ["leetcode*", "site*", "docs*", "tests*", "tools*", "scripts*"]
```

After this change:
```bash
pip install -e .  # Editable install

# Now works anywhere in the repo:
from leetcode_datasource import LeetCodeDataSource
```

---

## 3. Package Design: leetcode_datasource

### 3.1 Module Structure

```
packages/leetcode_datasource/
├── __init__.py                         # Public API exports
├── datasource.py                       # LeetCodeDataSource main class
├── config.py                           # DataSourceConfig
├── exceptions.py                       # Custom exceptions
│
├── models/                             # ─── Data Model ───
│   ├── __init__.py
│   ├── question.py                     # Question dataclass
│   └── schema.py                       # Schema version definitions
│
├── storage/                            # ─── Storage Layer ───
│   ├── __init__.py
│   ├── cache.py                        # Cache layer (ephemeral)
│   └── store.py                        # Persistent layer (SQLite)
│
├── serialization/                      # ─── Serialization ───
│   ├── __init__.py
│   └── question_serializer.py          # Question ↔ dict/JSON
│
└── fetchers/                           # ─── Network Layer (Pluggable) ───
    ├── __init__.py                     # Fetcher interface
    └── leetscrape_fetcher.py           # Default: LeetScrape implementation
```

### 3.2 Public API

#### LeetCodeDataSource (Primary Interface)

```python
from leetcode_datasource import LeetCodeDataSource

ds = LeetCodeDataSource()  # or LeetCodeDataSource(config=DataSourceConfig(...))
```

| Method | Signature | Description |
|--------|-----------|-------------|
| `get_by_slug` | `(slug: str, *, refresh: bool = False) -> Question` | Get question by URL slug |
| `get_by_frontend_id` | `(id: int, *, refresh: bool = False) -> Question` | Get question by problem number |
| `exists` | `(slug: str) -> bool` | Check if question exists in cache/store |
| `invalidate` | `(slug: str) -> bool` | Remove specific question from cache |
| `clear_cache` | `() -> None` | Clear all cached data |
| `stats` | `() -> dict` | Get statistics (count, cache hits, etc.) |

**Parameters:**
- `refresh=False`: Use cached data if available
- `refresh=True`: Bypass cache, fetch fresh data from network

**Example:**

```python
from leetcode_datasource import LeetCodeDataSource

ds = LeetCodeDataSource()

# Get by slug
q = ds.get_by_slug("two-sum")
print(q.title)        # "Two Sum"
print(q.difficulty)   # "Easy"

# Get by problem number
q = ds.get_by_frontend_id(1)
print(q.titleSlug)    # "two-sum"

# Force refresh from network
q = ds.get_by_slug("two-sum", refresh=True)

# Check existence
if ds.exists("two-sum"):
    print("Cached!")

# Get stats
print(ds.stats())
# {'total_questions': 2890, 'cache_hits': 42, 'cache_misses': 3}
```

#### Store (Direct Access)

For advanced use cases, direct store access is available:

```python
ds = LeetCodeDataSource()
store = ds.store
```

| Method | Signature | Description |
|--------|-----------|-------------|
| `put` | `(question: Question) -> None` | Save question to store |
| `get_by_slug` | `(slug: str) -> Question \| None` | Read from store |
| `get_by_frontend_id` | `(id: int) -> Question \| None` | Read from store |
| `count` | `() -> int` | Total questions in store |

### 3.3 Exception Hierarchy

```python
from leetcode_datasource.exceptions import (
    LeetCodeDataSourceError,  # Base exception
    QuestionNotFoundError,    # Question not found (cache miss + network fail)
    NetworkError,             # Network/fetch failure
    ParseError,               # Data parsing failure
    ConfigError,              # Configuration error
)
```

```
LeetCodeDataSourceError (base)
├── QuestionNotFoundError
├── NetworkError
├── ParseError
└── ConfigError
```

**Design Note:** Cache errors are non-fatal and only reflected in logs/stats, not as public exceptions.

### 3.4 Pluggable Fetcher Design

The network layer is designed to be replaceable:

```python
# Default: LeetScrape
ds = LeetCodeDataSource()  # Uses LeetscrapeFecher internally

# Custom fetcher (future)
from leetcode_datasource.fetchers import BaseFetcher

class MyCustomFetcher(BaseFetcher):
    def fetch(self, slug: str) -> dict:
        # Custom implementation
        ...

ds = LeetCodeDataSource(config=DataSourceConfig(fetcher=MyCustomFetcher()))
```

**Current Implementation:**
- Only `LeetscrapeFecher` is implemented
- Abstract base class (`BaseFetcher`) is intentionally NOT created yet (avoid premature abstraction)
- The interface is documented but code remains simple until a second fetcher is needed

### 3.5 Schema Versioning Strategy

To handle future field changes without breaking existing data:

```python
# models/schema.py
SCHEMA_VERSION = "1.0"

SCHEMA_CHANGELOG = {
    "1.0": "Initial schema with LeetScrape-compatible fields",
    # "1.1": "Added new_field",  # Future
}
```

**Migration Strategy:**
1. Schema version stored with each serialized Question
2. On deserialize, check version and apply migrations if needed
3. Backward-compatible: old data readable by new code
4. Forward-compatible: new fields have defaults

### 3.6 Performance Considerations

| Aspect | Strategy |
|--------|----------|
| **Cache Hit** | Memory-first, then SQLite, then network |
| **Lazy Loading** | `Question.Body` (large field) loaded on access |
| **Batch Operations** | `store.put()` uses transactions for bulk inserts |
| **ID Lookup** | SQLite index on `qid` provides fast frontend_id → slug lookup |
| **Rate Limiting** | Fetcher respects LeetCode rate limits (configurable delay) |

---

## 4. Data Model

### 4.1 Question Dataclass

```python
# packages/leetcode_datasource/models/question.py
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Question:
    """LeetCode question data model.
    
    Field names follow LeetScrape convention for compatibility.
    """
    # === Required Fields ===
    QID: int                              # Internal question ID (for reference only)
    frontend_question_id: int             # Problem number shown on website (1, 2, 922...)
    title: str                            # "Two Sum"
    titleSlug: str                        # "two-sum"
    difficulty: str                       # "Easy", "Medium", "Hard"
    
    # === Content Fields ===
    Body: str = ""                        # HTML problem description
    Code: str = ""                        # Code template/stubs
    Hints: List[str] = field(default_factory=list)
    
    # === Metadata Fields ===
    acceptanceRate: float = 0.0
    topicTags: str = ""                   # Comma-separated: "array,hash-table"
    categorySlug: str = ""                # "algorithms", "database", etc.
    isPaidOnly: bool = False
    
    # === Relationship Fields ===
    SimilarQuestions: List[int] = field(default_factory=list)
    Companies: Optional[List[str]] = None
    
    # === Cache Metadata (Internal) ===
    _schema_version: str = "1.0"
    _cached_at: Optional[str] = None
    _from_cache: bool = False
```

### 4.2 Field Reference

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `QID` | `int` | LeetScrape | Internal ID (not used for lookup) |
| `frontend_question_id` | `int` | LeetCode API | **Primary lookup key** by number |
| `title` | `str` | LeetScrape | Display title |
| `titleSlug` | `str` | LeetScrape | **Primary lookup key** by slug |
| `difficulty` | `str` | LeetScrape | Enum: Easy/Medium/Hard |
| `Body` | `str` | LeetScrape | HTML problem statement |
| `Code` | `str` | LeetScrape | Code template |
| `Hints` | `List[str]` | LeetScrape | Hint strings |
| `acceptanceRate` | `float` | LeetScrape | Percentage (0-100) |
| `topicTags` | `str` | LeetScrape | Comma-separated tags |
| `categorySlug` | `str` | LeetScrape | Category |
| `isPaidOnly` | `bool` | LeetScrape | Premium flag |
| `SimilarQuestions` | `List[int]` | LeetScrape | Related problem IDs |
| `Companies` | `List[str]` | LeetScrape | Company tags |

### 4.3 Schema Versioning

```python
# packages/leetcode_datasource/models/schema.py
SCHEMA_VERSION = "1.0"

SCHEMA_MIGRATIONS = {
    # "1.0 -> 1.1": lambda q: {...},  # Future migrations
}

def migrate_question(data: dict, from_version: str) -> dict:
    """Apply migrations to upgrade data to current schema."""
    # Implementation when needed
    pass
```

**Versioning Rules:**
1. `_schema_version` stored with every serialized Question
2. Deserialize checks version, applies migrations if needed
3. New fields always have defaults (backward compatible)
4. Breaking changes increment major version

---

## 5. Data Directory Strategy

### 5.1 Principle

> **Runtime data 不放 repo、不放 package 內**

| Data Type | Location | Can Delete? | Git Status |
|-----------|----------|-------------|------------|
| Cache | `.neetcode/leetcode_datasource/cache/` | ✅ Yes | gitignored |
| Store | `.neetcode/leetcode_datasource/store/` | ⚠️ Careful | optional gitignore |

### 5.2 Directory Structure

```
.neetcode/
├── leetcode_datasource/
│   ├── cache/                          # Ephemeral, rebuildable
│   │   ├── leetcode_problems.json      # Cached problem list
│   │   └── leetcode_cache_meta.json    # Cache metadata
│   │
│   └── store/                          # Persistent storage
│       └── leetcode.sqlite3            # SQLite database (indexed on qid)
│
└── README.md                           # Explain this directory
```

### 5.3 File Descriptions

| File | Purpose | Rebuild Strategy |
|------|---------|------------------|
| `cache/*.json` | Speed up repeated lookups | Re-fetch from LeetCode |
| `store/leetcode.sqlite3` | Offline access, persistence | Re-import from LeetScrape data |

### 5.4 .gitignore Strategy

```gitignore
# .neetcode runtime data
.neetcode/leetcode_datasource/cache/    # Always ignored
# .neetcode/leetcode_datasource/store/  # Optional: keep for sharing
```

**Decision Point:** Store 和 Meta 是否 commit 到 repo？

| Option | Pros | Cons |
|--------|------|------|
| **Commit** | 團隊共享、離線可用 | Repo 變大、需要更新維護 |
| **Gitignore** | Repo 乾淨 | 每人需要自己 import |

**建議：** 初期 commit 以方便使用，未來可改為 gitignore + download script。

---

## 6. Configuration

### 6.1 DataSourceConfig

```python
# packages/leetcode_datasource/config.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import os

@dataclass
class DataSourceConfig:
    """Configuration for LeetCodeDataSource."""
    
    # Data directory (where .neetcode/ lives)
    data_dir: Optional[Path] = None
    
    # Cache settings
    cache_enabled: bool = True
    cache_ttl_hours: int = 24 * 7  # 1 week default
    
    # Network settings
    fetch_timeout: int = 30  # seconds
    rate_limit_delay: float = 0.5  # seconds between requests
    
    # Fetcher (pluggable)
    fetcher: Optional["BaseFetcher"] = None  # None = use default LeetscrapeFecher
    
    def __post_init__(self):
        if self.data_dir is None:
            self.data_dir = self._resolve_data_dir()
    
    def _resolve_data_dir(self) -> Path:
        """Resolve data directory with priority order."""
        # Priority 1: Environment variable
        env_dir = os.environ.get("NEETCODE_DATA_DIR")
        if env_dir:
            return Path(env_dir)
        
        # Priority 2: Repo local .neetcode/
        repo_local = self._find_repo_root() / ".neetcode"
        if repo_local.parent.exists():
            return repo_local
        
        # Priority 3: platformdirs (fallback)
        try:
            import platformdirs
            return Path(platformdirs.user_data_dir("neetcode"))
        except ImportError:
            # Priority 4: Home directory fallback
            return Path.home() / ".neetcode"
    
    def _find_repo_root(self) -> Path:
        """Find repo root by looking for pyproject.toml."""
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / "pyproject.toml").exists():
                return parent
        return current
```

### 6.2 Configuration Priority

| Priority | Source | Example |
|----------|--------|---------|
| 1 (Highest) | **Explicit** | `DataSourceConfig(data_dir=Path("/custom"))` |
| 2 | **Environment** | `NEETCODE_DATA_DIR=/path/to/data` |
| 3 | **Repo Local** | `.neetcode/` in repo root |
| 4 (Lowest) | **platformdirs** | `~/.local/share/neetcode/` (Linux) |

### 6.3 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEETCODE_DATA_DIR` | Override data directory | (repo local) |
| `NEETCODE_CACHE_DISABLED` | Disable cache | `false` |
| `NEETCODE_FETCH_TIMEOUT` | Network timeout (seconds) | `30` |

### 6.4 Usage Examples

```python
from leetcode_datasource import LeetCodeDataSource, DataSourceConfig

# Default config (repo local .neetcode/)
ds = LeetCodeDataSource()

# Custom data directory
config = DataSourceConfig(data_dir=Path("/my/custom/path"))
ds = LeetCodeDataSource(config=config)

# Disable cache
config = DataSourceConfig(cache_enabled=False)
ds = LeetCodeDataSource(config=config)

# Custom fetcher (future)
config = DataSourceConfig(fetcher=MyCustomFetcher())
ds = LeetCodeDataSource(config=config)
```

---

## 7. Migration Plan

### 7.1 Overview

採用**漸進式遷移**，分階段完成：

```
Phase 1: 建立骨架 ──► Phase 2: 實作核心 ──► Phase 3: 資料遷移 ──► Phase 4: 驗證
```

### 7.2 Phase 1: Establish Structure

**目標：** 建立 `packages/` 目錄結構和 pyproject.toml 配置

| Task | Description | Status |
|------|-------------|--------|
| 1.1 | Create `packages/` directory | ⬜ |
| 1.2 | Create `packages/__init__.py` | ⬜ |
| 1.3 | Create `packages/leetcode_datasource/` structure | ⬜ |
| 1.4 | Update `pyproject.toml` to include `packages*` | ⬜ |
| 1.5 | Create `.neetcode/` directory with README | ⬜ |
| 1.6 | Update `.gitignore` for `.neetcode/cache/` | ⬜ |

**Deliverable:** Empty package structure, `pip install -e .` works

### 7.3 Phase 2: Implement Core

**目標：** 實作 `leetcode_datasource` 核心功能

| Task | Description | Dependency |
|------|-------------|------------|
| 2.1 | Implement `models/question.py` | - |
| 2.2 | Implement `models/schema.py` | - |
| 2.3 | Implement `exceptions.py` | - |
| 2.4 | Implement `config.py` | - |
| 2.5 | Implement `serialization/question_serializer.py` | 2.1, 2.2 |
| 2.6 | Implement `storage/store.py` (SQLite) | 2.1, 2.5 |
| 2.7 | Implement `storage/cache.py` | 2.1, 2.5 |
| 2.8 | Implement `fetchers/leetscrape_fetcher.py` | 2.1 |
| 2.9 | Implement `datasource.py` (main class) | 2.4-2.8 |
| 2.10 | Implement `__init__.py` (public exports) | 2.9 |

**Deliverable:** Working package, can fetch/store questions

### 7.4 Phase 3: Data Migration

**目標：** 從 `tools/leetcode-api/` 遷移資料

| Task | Description |
|------|-------------|
| 3.1 | Migrate `db/leetcode.db` → `.neetcode/leetcode_datasource/store/` |
| 3.2 | Migrate cache files → `.neetcode/leetcode_datasource/cache/` |

**Note:** `tools/leetcode-api/` 保持不變，只複製資料

### 7.5 Phase 4: Validation

**目標：** 驗證功能正確性

| Task | Description |
|------|-------------|
| 4.1 | Unit tests for all modules |
| 4.2 | Integration test: fetch → cache → store cycle |
| 4.3 | Verify import works from different locations |
| 4.4 | Compare output with existing `tools/leetcode-api/` |

**Acceptance Criteria:**

```python
# Must work from any directory in repo
from leetcode_datasource import LeetCodeDataSource

ds = LeetCodeDataSource()
q = ds.get_by_slug("two-sum")
assert q.title == "Two Sum"
assert q.frontend_question_id == 1

q = ds.get_by_frontend_id(1)
assert q.titleSlug == "two-sum"
```

### 7.6 Branch Strategy

```
main
  └── refactor/monorepo-packages
        ├── Phase 1 commits
        ├── Phase 2 commits
        ├── Phase 3 commits
        └── Phase 4 commits → PR to main
```

---

## 8. Future Work

### 8.1 Not In Scope (Deferred)

以下項目**不在本次重構範圍**，記錄為未來工作：

| Item | Description | Priority |
|------|-------------|----------|
| **tools 遷移** | 讓 `tools/leetcode-api/` 改用 `packages/leetcode_datasource` | High |
| **testgen 模組** | `packages/testgen/` 自動產生測資 | Medium |
| **CLI wrapper** | `python -m leetcode_datasource` CLI 介面 | Low |
| **Async support** | 非同步 fetch 支援 | Low |

### 8.2 tools/leetcode-api Integration (Next Phase)

完成本次重構後，下一步是讓 `tools/` 使用 `packages/`：

```python
# Before (tools/leetcode-api/question_api.py)
from question_store import QuestionStore
from question_serializer import Question

# After
from leetcode_datasource import LeetCodeDataSource, Question

ds = LeetCodeDataSource()
q = ds.get_by_slug("two-sum")
```

**Migration Path:**
1. Keep `tools/leetcode-api/` as CLI wrapper
2. Replace internal imports with `leetcode_datasource`
3. Remove duplicated code

### 8.3 packages/testgen Placeholder

```
packages/
├── leetcode_datasource/     # ✅ This PR
└── testgen/                 # 🔜 Future
    └── __init__.py          # Placeholder only
```

**testgen 模組規劃：**
- 自動產生測資
- 依賴 `leetcode_datasource` 取得題目資訊
- 輸出符合 `tests/*.in`, `tests/*.out` 格式

### 8.4 Dependency Enforcement (Future)

未來可加入自動化檢查確保依賴方向：

```yaml
# .github/workflows/lint.yml (future)
- name: Check dependency direction
  run: |
    # Ensure packages/ does not import from tools/
    ! grep -r "from tools" packages/
    ! grep -r "import tools" packages/
```

---

## Appendix

### A. Glossary

| Term | Definition |
|------|------------|
| **packages/** | 可重用核心模組目錄，提供乾淨 API，設計為可被 import |
| **tools/** | CLI / wrapper / glue code，不承諾被 import |
| **runner/** | 測試框架核心，獨立於 packages |
| **frontend_question_id** | 使用者在 LeetCode 網站看到的題號（1, 2, 922...） |
| **question_id** | LeetCode 內部資料庫 ID（不對外暴露） |
| **title_slug** | URL slug（如 `"two-sum"`） |
| **DataSource** | 資料來源抽象（整合 cache + store + fetcher） |
| **Store** | 持久化儲存層（SQLite） |
| **Cache** | 快取層（ephemeral，可丟棄重建） |
| **Fetcher** | 網路抓取層（可插拔，預設 LeetScrape） |

### B. References

| Document | Description |
|----------|-------------|
| [tools/reorganization-plan.md](../tools/reorganization-plan.md) | Tools 目錄整理規劃 |
| [docs/architecture-migration.md](./architecture-migration.md) | Solution 架構遷移文件 |
| [docs/tools/leetcode-api/README.md](./tools/leetcode-api/README.md) | 現有 leetcode-api 文件 |
| [LeetScrape Docs](https://nikhil-ravi.github.io/LeetScrape/question/) | LeetScrape 官方文件 |

### C. Related PRs / Issues

| PR/Issue | Description | Status |
|----------|-------------|--------|
| Branch: `refactor/monorepo-packages` | 本次重構 | 🔜 Planned |

### D. Changelog

| Date | Change |
|------|--------|
| 2025-12-31 | Initial draft |


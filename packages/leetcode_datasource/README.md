# LeetCode DataSource

Unified data layer for LeetCode question metadata.

## Overview

Provides a clean API to access LeetCode problem data with caching, persistent storage, and pluggable network fetcher.

## Responsibility

### What this package does

- ✅ Fetches LeetCode question metadata (title, description, examples, etc.)
- ✅ Provides cache layer for fast repeated access
- ✅ Stores question data in SQLite for persistence
- ✅ Supports lookup by frontend ID or title slug
- ✅ Provides structured data models

### What this package does NOT do

- ❌ Generate solution files (handled by `codegen`)
- ❌ Execute tests (handled by `runner/`)
- ❌ Manage practice history (handled by `practice_workspace`)

## Public API

| Export | Description |
|--------|-------------|
| `LeetCodeDataSource` | Main data source class |
| `DataSourceConfig` | Configuration class |
| `Question` | Question data model |
| `ProblemInfo` | Minimal problem info model |
| `LeetCodeDataSourceError` | Base exception |
| `QuestionNotFoundError` | Question not found |
| `NetworkError` | Network request failed |
| `ParseError` | Data parsing failed |
| `ConfigError` | Configuration error |

## File Structure

```
leetcode_datasource/
├── __init__.py              # Public API re-exports
├── datasource.py            # Main LeetCodeDataSource class
├── config.py                # Configuration
├── exceptions.py            # Exception classes
├── models/                  # Data models
│   ├── __init__.py
│   ├── question.py          # Question model
│   ├── problem_info.py      # ProblemInfo model
│   └── schema.py            # Schema definitions
├── storage/                 # Storage layer
│   ├── __init__.py
│   ├── cache.py             # JSON cache
│   └── store.py             # SQLite store
├── serialization/           # Serialization
│   ├── __init__.py
│   └── question_serializer.py
└── fetchers/                # Network fetchers
    ├── __init__.py
    └── leetscrape_fetcher.py
```

## Dependencies

| Direction | Package | Purpose |
|-----------|---------|---------|
| Uses → | (stdlib only) | No package dependencies |

> ❗ **Do NOT list tools here.** Tools depend on packages, not vice versa.

## Usage

```python
from leetcode_datasource import LeetCodeDataSource

ds = LeetCodeDataSource()

# Get by title slug
q = ds.get_by_slug("two-sum")
print(q.title)       # "Two Sum"
print(q.difficulty)  # "Easy"

# Get by frontend ID
q = ds.get_by_frontend_id(1)
print(q.titleSlug)   # "two-sum"

# Access question data
print(q.description)
print(q.examples)
print(q.constraints)
print(q.hints)
```

## Related Documentation

- **[Complete Specification](../../docs/packages/leetcode_datasource/README.md)** - System-level documentation

---

## Documentation Maintenance

⚠️ **When modifying this package:**

1. Update this README (quick reference)
2. Update `docs/packages/leetcode_datasource/README.md` (complete specification)


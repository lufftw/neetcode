# LeetCode API

> **Purpose**: SQLite-backed cache and unified API for LeetCode question data  
> **Location**: `tools/leetcode-api/`  
> **Last Updated**: {{ git_revision_date_localized }}

This module provides a local cache and unified API for accessing LeetCode question data, reducing network requests and improving performance for tools that need problem metadata.

---

## Features

- **SQLite Cache**: Persistent local storage for question data
- **LeetScrape Integration**: Automatic fallback to network fetch when not cached
- **Transparent API**: Same `Question` interface whether from cache or network
- **Bulk Import**: Import all questions from LeetScrape JSON dump

---

## Quick Start

### Using the API

```python
from tools.leetcode_api import get_question

# Get question (from cache or network)
q = get_question("two-sum")

# Access question data (LeetScrape-compatible interface)
print(q.title)           # "Two Sum"
print(q.QID)             # 1
print(q.difficulty)      # "Easy"
print(q.topicTags)       # "array,hash-table"
print(q.Body)            # HTML problem description
print(q.Hints)           # ["hint1", "hint2", ...]
print(q.SimilarQuestions)  # [15, 18, 167, ...]
```

### Bulk Import from LeetScrape Data

```bash
# Import all questions from data/all.json
python tools/leetcode-api/import_all_json.py

# Dry run (preview without saving)
python tools/leetcode-api/import_all_json.py --dry-run

# Include paid-only questions
python tools/leetcode-api/import_all_json.py --include-paid
```

---

## Architecture

```
tools/leetcode-api/
├── __init__.py            # Package exports
├── question_api.py        # Unified public API
├── question_serializer.py # LeetScrape ↔ SQLite conversion
├── question_store.py      # SQLite storage layer
├── import_all_json.py     # Bulk import script
└── data/
    └── all.json           # LeetScrape data dump
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    get_question(slug)                       │
│                           │                                 │
│         ┌─────────────────┴─────────────────┐               │
│         ▼                                   ▼               │
│   [Cache Hit]                        [Cache Miss]           │
│   SQLite 讀取                        LeetScrape 抓取         │
│         │                                   │               │
│         ▼                                   ▼               │
│   deserialize()                     serialize() + save()    │
│         │                                   │               │
│         └─────────────────┬─────────────────┘               │
│                           ▼                                 │
│                     Question 物件                            │
│               (與 LeetScrape 完全相容)                        │
└─────────────────────────────────────────────────────────────┘
```

---

## API Reference

### `get_question(slug, force_refresh=False)`

Get a LeetCode question by slug.

```python
from tools.leetcode_api import get_question

q = get_question("two-sum")
q = get_question("two-sum", force_refresh=True)  # Bypass cache
```

**Parameters:**
- `slug` (str): Question slug (e.g., "two-sum")
- `force_refresh` (bool): If True, bypass cache and fetch from network

**Returns:** `Question` object or `None` if not found

### `get_question_by_id(qid)`

Get a question by LeetCode QID (cache only).

```python
from tools.leetcode_api import get_question_by_id

q = get_question_by_id(1)      # By int
q = get_question_by_id("0001") # By string (padded)
```

**Parameters:**
- `qid` (int | str): Question ID

**Returns:** `Question` object or `None` if not in cache

### `Question` Object

The `Question` dataclass matches [LeetScrape JSON format](https://raw.githubusercontent.com/nikhil-ravi/LeetScrape/refs/heads/main/example/data/all.json):

| Attribute | Type | Description |
|-----------|------|-------------|
| `QID` | `int` | Question ID (e.g., 1) |
| `title` | `str` | Problem title |
| `titleSlug` | `str` | URL slug (e.g., "two-sum") |
| `difficulty` | `str` | "Easy", "Medium", "Hard" |
| `acceptanceRate` | `float` | Acceptance rate percentage |
| `topicTags` | `str` | Comma-separated tags (e.g., "array,hash-table") |
| `categorySlug` | `str` | Category (e.g., "algorithms") |
| `Hints` | `List[str]` | List of hint strings |
| `Companies` | `List[str]` or `None` | Company tags |
| `SimilarQuestions` | `List[int]` | List of related QIDs |
| `Code` | `str` | Code template string |
| `Body` | `str` | HTML problem description |
| `isPaidOnly` | `bool` | Premium-only flag |
| `paidOnly` | `bool` | Same as isPaidOnly |

**Cache metadata:**
- `_from_cache` (bool): True if loaded from SQLite
- `_cached_at` (str): Timestamp when cached

---

## SQLite Schema

Database location: `tools/.cache/leetcode_questions.db`

```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    qid INTEGER NOT NULL,
    title TEXT NOT NULL,
    title_slug TEXT NOT NULL UNIQUE,
    difficulty TEXT,
    acceptance_rate REAL,
    paid_only INTEGER DEFAULT 0,
    topic_tags TEXT,
    category_slug TEXT,
    hints TEXT,              -- JSON array
    companies TEXT,          -- JSON array or null
    similar_questions TEXT,  -- JSON array of QIDs
    code TEXT,
    body TEXT,
    is_paid_only INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

## CLI Tools

### `import_all_json.py`

Bulk import questions from LeetScrape JSON dump.

```bash
# Basic usage
python tools/leetcode-api/import_all_json.py

# Options
python tools/leetcode-api/import_all_json.py --help
```

| Option | Description |
|--------|-------------|
| `--json-path PATH` | Path to all.json file |
| `--dry-run` | Parse JSON without saving |
| `--include-paid` | Include paid-only questions |
| `--include-empty` | Include questions with empty Body |

**Example output:**

```
Reading: tools/leetcode-api/data/all.json
Found 3245 questions
  Progress: 100/3245 (3%)
  Progress: 200/3245 (6%)
  ...

==================================================
Import Summary
==================================================
  Total in JSON:    3245
  Imported:         2890
  Skipped (paid):   312
  Skipped (empty):  43
  Errors:           0
==================================================

Database now has: 2890 questions
```

---

## Integration with review-code

The `review-code` tool uses this API for fetching question data:

```python
# tools/review-code/leetscrape_fetcher.py
from question_api import get_question

def get_full_docstring_data(slug: str) -> dict:
    q = get_question(slug)
    # ... extract description, examples, constraints
```

This enables:
- **Caching**: Avoid repeated LeetCode API calls
- **Offline support**: Work with cached data without network
- **Faster processing**: Batch operations use local cache

---

## Data Source

Question data schema follows [LeetScrape](https://github.com/nikhil-ravi/LeetScrape):

- **JSON Format**: [all.json](https://raw.githubusercontent.com/nikhil-ravi/LeetScrape/refs/heads/main/example/data/all.json)
- **Documentation**: [LeetScrape Docs](https://nikhil-ravi.github.io/LeetScrape/question/)

---

## Related Documentation

- [Review Code Tool](../README.md) - File-Level Docstring generator
- [review-code.md](../../review-code.md) - Docstring format specification


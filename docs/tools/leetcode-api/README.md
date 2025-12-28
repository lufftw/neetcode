# LeetCode API

> **Status**: Canonical Reference  
> **Scope**: LeetCode API cache module in tools/leetcode-api/  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}  
> **Purpose**: SQLite-backed cache and unified API for LeetCode question data  
> **Location**: `tools/leetcode-api/`

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
# Import all questions (auto-detect source: json or csv)
python tools/leetcode-api/import_all_question.py

# Explicitly use all.json
python tools/leetcode-api/import_all_question.py --source json

# Use CSV files (questions.csv + questionBody.pickle + questionTopics.csv)
python tools/leetcode-api/import_all_question.py --source csv

# Dry run (preview without saving)
python tools/leetcode-api/import_all_question.py --dry-run

# Include paid-only questions
python tools/leetcode-api/import_all_question.py --include-paid
```

---

## Architecture

```
tools/leetcode-api/
├── __init__.py              # Package exports
├── question_api.py          # Unified public API
├── question_serializer.py   # LeetScrape ↔ SQLite conversion
├── question_store.py        # SQLite storage layer
├── import_all_question.py   # Bulk import script
├── db/
│   └── leetcode.db          # SQLite database
└── data/
    ├── all.json             # Complete question data (primary)
    ├── questions.csv        # Basic metadata
    ├── questionBody.pickle  # Problem statements
    ├── questionTopics.csv   # QID to topic mapping
    ├── topicTags.csv        # Topic tag details
    └── companies.csv        # Company information
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

Database location: `tools/leetcode-api/db/leetcode.db`

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

### `import_all_question.py`

Bulk import questions from LeetScrape data files.

```bash
# Basic usage (auto-detect source)
python tools/leetcode-api/import_all_question.py

# Options
python tools/leetcode-api/import_all_question.py --help
```

| Option | Description |
|--------|-------------|
| `--source {json,csv,auto}` | Data source: json (all.json), csv (combine CSVs), auto (default) |
| `--data-dir PATH` | Path to data directory |
| `--dry-run` | Parse data without saving |
| `--include-paid` | Include paid-only questions |
| `--include-empty` | Include questions with empty Body |

**Data Sources:**
- `json`: Uses `all.json` which contains complete question data
- `csv`: Combines `questions.csv`, `questionBody.pickle`, and `questionTopics.csv`
- `auto`: Tries json first, falls back to csv

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

## Integration with docstring module

The `docstring` domain module uses this API for fetching question data:

```python
# tools/docstring/formatter.py
from question_api import get_question

def get_full_docstring_data(slug: str) -> dict:
    q = get_question(slug)
    # ... extract description, examples, constraints
```

This enables:
- **Caching**: Avoid repeated LeetCode API calls
- **Offline support**: Work with cached data without network
- **Faster processing**: Batch operations use local cache

See [Docstring Formatter](../docstring/README.md) for the design and API details.

---

## Important: LeetCode Problem ID Types

LeetCode uses **two different ID systems** which can cause confusion when looking up problems:

| Field | Description | Example |
|-------|-------------|---------|
| `question_id` | Internal database ID | 958 |
| `frontend_question_id` | Problem number displayed on website | 922 |

### Why This Matters

Solution filenames in this project use the **frontend_question_id** (the number shown on LeetCode's website):

```
0922_sort_array_by_parity_ii.py  → frontend_question_id = 922
```

However, the same problem has `question_id = 958` internally.

### Cache Lookup

The `fix_docstring.py` tool uses `tools/leetcode-api/crawler/.cache/leetcode_problems.json` which contains both IDs:

```json
{
  "0958": {
    "question_id": 958,
    "frontend_question_id": 922,
    "title": "Sort Array By Parity II",
    "slug": "sort-array-by-parity-ii"
  }
}
```

When looking up by problem number (from filename), always use `frontend_question_id`, not `question_id`:

```python
# ✅ Correct: Use frontend_question_id
for key, value in cache.items():
    if value.get('frontend_question_id') == problem_id:
        return value['slug']

# ❌ Wrong: Using question_id would return wrong problem!
for key, value in cache.items():
    if value.get('question_id') == problem_id:
        return value['slug']  # May return wrong slug!
```

### Quick Reference

| Filename | frontend_question_id | question_id | Correct Slug |
|----------|---------------------|-------------|--------------|
| `0001_two_sum.py` | 1 | 1 | `two-sum` |
| `0922_sort_array_by_parity_ii.py` | 922 | 958 | `sort-array-by-parity-ii` |
| `0886_possible_bipartition.py` | 886 | 922 | `possible-bipartition` |

---

## Data Source

Question data schema follows [LeetScrape](https://github.com/nikhil-ravi/LeetScrape):

- **JSON Format**: [all.json](https://raw.githubusercontent.com/nikhil-ravi/LeetScrape/refs/heads/main/example/data/all.json)
- **Documentation**: [LeetScrape Docs](https://nikhil-ravi.github.io/LeetScrape/question/)

---

## Related Documentation

- [Review Code Tool](../review-code/README.md) - File-Level Docstring generator
- [Docstring Formatter](../docstring/README.md) - Docstring formatting module
- [Main Tools README](../README.md) - Tools overview


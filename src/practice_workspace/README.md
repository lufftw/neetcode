# Practice Workspace

Stateful management of practice file history and restore operations.

## Overview

Manages practice file versioning in the `_history/` directory, enabling save, list, and restore operations for practice sessions.

## Responsibility

### What this package does

- ✅ Saves practice files to `_history/` directory
- ✅ Lists historical versions with timestamps
- ✅ Restores specific or latest version
- ✅ Formats relative time display

### What this package does NOT do

- ❌ Generate file content (handled by `codegen`)
- ❌ Execute tests (handled by `runner/`)
- ❌ Fetch problem data (handled by `leetcode_datasource`)

## Public API

| Export | Description |
|--------|-------------|
| `save_to_history()` | Save current practice to history |
| `list_history()` | List all history versions (formatted) |
| `get_history_entries()` | Get history entries as objects |
| `HistoryEntry` | History entry data class |
| `restore_from_history()` | Restore specific version |
| `restore_latest()` | Restore most recent version |
| `get_practice_path()` | Get practice file path |
| `get_history_dir()` | Get history directory path |
| `parse_timestamp()` | Parse timestamp string |
| `format_relative_time()` | Format relative time display |

## File Structure

```
practice_workspace/
├── __init__.py              # Public API re-exports
├── history.py               # History operations
├── restore.py               # Restore operations
├── utils.py                 # Utilities (paths, timestamps)
└── cli.py                   # CLI: practice history/restore
```

## Dependencies

| Direction | Package | Purpose |
|-----------|---------|---------|
| Uses → | (stdlib only) | No package dependencies |

> ❗ **Do NOT list tools here.** Tools depend on packages, not vice versa.

## Related Packages

| Package | Relationship |
|---------|--------------|
| `codegen` | Generates practice skeletons, calls `save_to_history()` |
| `leetcode_datasource` | No direct dependency |

## Usage

```python
from practice_workspace import (
    save_to_history,
    list_history,
    restore_from_history,
    restore_latest,
)
from pathlib import Path

# Save current practice to history
practice_path = Path("practices/0001_two_sum.py")
history_path = save_to_history(practice_path)
# -> practices/_history/0001_two_sum.py.20251231_143022.bak

# List all history versions
versions = list_history(1)
# Output:
# Practice history for 0001_two_sum:
#   [1] 20251225_200000  (6 days ago)
#   [2] 20251230_091500  (1 day ago)
#   [3] 20251231_143022  (2 hours ago)   ← latest

# Restore specific version
restore_from_history(1, timestamp="20251230_091500")

# Restore latest version
restore_latest(1)
```

## Related Documentation

- **[Complete Specification](../../docs/packages/practice_workspace/README.md)** - System-level documentation

---

## Documentation Maintenance

⚠️ **When modifying this package:**

1. Update this README (quick reference)
2. Update `docs/packages/practice_workspace/README.md` (complete specification)


# .neetcode Runtime Data Directory

This directory contains runtime data for the NeetCode project.

## Structure

```
.neetcode/
├── leetcode_datasource/
│   ├── cache/          # Ephemeral cache (safe to delete)
│   └── store/          # Persistent SQLite storage
└── README.md           # This file
```

## Data Types

| Directory | Purpose | Safe to Delete? |
|-----------|---------|-----------------|
| `cache/` | Speed up repeated lookups | ✅ Yes - will be rebuilt |
| `store/` | Offline access, persistence | ⚠️ Careful - contains imported data |

## Git Status

- `cache/` is gitignored (ephemeral data)
- `store/` may be committed for sharing (optional)

## Rebuilding Data

If you need to rebuild the data:

```bash
# Re-import from LeetScrape data
python -c "from leetcode_datasource import LeetCodeDataSource; print('OK')"
```

## Configuration

The data directory location can be overridden:

1. **Environment variable**: `NEETCODE_DATA_DIR=/custom/path`
2. **Code**: `DataSourceConfig(data_dir=Path("/custom/path"))`

See `docs/packages-architecture-spec.md` for full documentation.

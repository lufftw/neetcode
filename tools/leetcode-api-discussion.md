# LeetCode API Integration

## API Overview

### Endpoint
```
https://leetcode.com/api/problems/all/
```

### Key Fields

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `question_id` | int | `11` | Problem ID (backend) |
| `question__title` | str | `"Container With Most Water"` | Full problem title |
| `question__title_slug` | str | `"container-with-most-water"` | URL slug for links |
| `frontend_question_id` | int/str | `11` | Frontend display ID |

### Format Mapping

**File naming:**
- Format: `{question_id:04d}_{slug}.py`
- Example: `0011_container_with_most_water.py`

**URL format:**
- `https://leetcode.com/problems/{slug}/description/`

**Slug conversion:**
- File: `0011_container_with_most_water` (underscores)
- URL: `container-with-most-water` (hyphens)
- Conversion handled in post-processing

## Implementation

### Data Sync Tool (`sync_leetcode_data.py`)

**Usage:**
```bash
# Update cache (if expired)
python tools/sync_leetcode_data.py

# Check cache status
python tools/sync_leetcode_data.py --check

# Force update
python tools/sync_leetcode_data.py --force
```

**Cache:**
- Location: `tools/.cache/leetcode_problems.json`
- Expiry: 7 days (auto-checked)

### Integration

**PostProcessor** automatically:
1. Loads LeetCode API cache data
2. Merges with local TOML data
3. Generates correct URLs for problems
4. No code changes required

**Link format:**
```
[LeetCode 11](url) | [Solution](github_url)
```

## References

- [Data sync tool](tools/sync_leetcode_data.py)
- [API integration module](tools/ai-markmap-agent/src/leetcode_api.py)
- [Post-processing module](tools/ai-markmap-agent/src/post_processing.py)
- [Post-processing docs](tools/ai-markmap-agent/docs/post-processing-links.md)

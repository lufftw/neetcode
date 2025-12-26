# Review Code Tool

Auto-fix File-Level Docstring for solution files to comply with `docs/review-code.md` specification.

## Features

- Automatically remove decorative separators (`===`, `---`)
- Check and ensure Problem and Link fields exist
- Check and add missing Constraints section
- Format docstring to comply with standard format
- Support range selection and single file processing
- Support dry-run mode (preview changes without modifying files)
- Fetch missing Problem and Link from LeetCode API cache

## Usage

### Interactive mode (prompts for range)

When run without arguments, the tool will prompt you to enter min and max range:

```bash
python tools/review-code/fix_docstring.py
# Will prompt:
# Min (inclusive): 77
# Max (inclusive): 142
```

**Note:** In interactive mode and range mode, all File-Level Docstrings will be **completely replaced** with program-generated content.

### Fix files in a range

```bash
# Fix files from 0077 to 0142 (completely replaces docstrings)
python tools/review-code/fix_docstring.py --range 77 142
```

### Fix a single file

```bash
python tools/review-code/fix_docstring.py --file 0077_combinations.py
```

### Preview mode (no actual file modification)

```bash
python tools/review-code/fix_docstring.py --dry-run
```

### Fetch missing info from LeetCode API

```bash
# Automatically fetch Problem and Link from LeetCode API cache
python tools/review-code/fix_docstring.py --fetch-online

# Combine: preview and fetch from online
python tools/review-code/fix_docstring.py --range 0077 0142 --fetch-online --dry-run
```

## Examples

```bash
# Preview changes for range 0077-0142
python tools/review-code/fix_docstring.py --range 0077 0142 --dry-run

# Actually fix a single file
python tools/review-code/fix_docstring.py --file 0080_remove_duplicates_from_sorted_array_ii.py

# Fix with online data fetching
python tools/review-code/fix_docstring.py --range 0077 0142 --fetch-online
```

## Notes

### Replacement Mode

- **Interactive mode and range mode**: All File-Level Docstrings are **completely replaced** with program-generated content
- The tool fetches Problem and Link from LeetCode API cache automatically (enabled by default)
- Existing optional fields (Sub-Pattern, Key Insight, etc.) are **not preserved** in replacement mode
- Description is preserved if it exists, but Problem and Link are always replaced with LeetCode data

### Online Fetching

- When using `--fetch-online` (default), the tool automatically fills Problem and Link from LeetCode API cache
- If LeetCode API cache doesn't exist, run `python tools/sync_leetcode_data.py` first to create the cache
- Use `--no-fetch` to disable online fetching

### Constraints

- If Constraints section is missing, a placeholder will be added for manual filling (currently cannot be auto-fetched from web)
- Existing constraints are preserved if they exist

### Best Practices

- It's recommended to use `--dry-run` first to preview changes before actually modifying files
- Make sure LeetCode API cache is up-to-date: `python tools/sync_leetcode_data.py`

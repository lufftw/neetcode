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
- Configurable random delays between requests to avoid anti-crawling (default: 1.0-3.0 seconds)

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

### Anti-Crawling Delay Configuration

To avoid being blocked by anti-crawling mechanisms, the tool includes random delays between requests:

```bash
# Use default delay (1.0-3.0 seconds)
python tools/review-code/fix_docstring.py --range 0077 0142

# Custom delay range (2.0-5.0 seconds)
python tools/review-code/fix_docstring.py --range 0077 0142 --delay-min 2.0 --delay-max 5.0

# Longer delay for safer crawling (3.0-8.0 seconds)
python tools/review-code/fix_docstring.py --range 0077 0142 --delay-min 3.0 --delay-max 8.0
```

**Parameters:**
- `--delay-min`: Minimum delay in seconds between requests (default: 1.0)
- `--delay-max`: Maximum delay in seconds between requests (default: 3.0)

**Note:** The tool will randomly wait between `delay-min` and `delay-max` seconds before each online request to avoid triggering anti-crawling mechanisms.

## Examples

```bash
# Preview changes for range 0077-0142
python tools/review-code/fix_docstring.py --range 0077 0142 --dry-run

# Actually fix a single file
python tools/review-code/fix_docstring.py --file 0080_remove_duplicates_from_sorted_array_ii.py

# Fix with online data fetching
python tools/review-code/fix_docstring.py --range 0077 0142 --fetch-online

# Fix with custom delay to avoid anti-crawling (recommended for large batches)
python tools/review-code/fix_docstring.py --range 0077 0142 --fetch-online --delay-min 2.0 --delay-max 5.0

# Preview with longer delay for safety
python tools/review-code/fix_docstring.py --range 0077 0142 --dry-run --delay-min 3.0 --delay-max 8.0

python tools/review-code/fix_docstring.py --range 200 300 --fetch-online --delay-min 30.0 --delay-max 60.0
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
- Use `--no-web-fetch` to disable web fetching for Description and Constraints (only use cache for Problem/Link)

### Anti-Bot Protection

The tool includes several anti-bot countermeasures:
- **Random delays between requests**: Configurable delay range (default: 1.0-3.0 seconds)
  - Use `--delay-min` and `--delay-max` to customize the delay range
  - Each request waits a random duration within the specified range
- Random User-Agent rotation (mimics different browsers)
- Automatic retry mechanism (up to 2 retries)
- Comprehensive browser headers (Referer, DNT, etc.)
- Special handling for 403 and 429 errors

**Delay Configuration:**
- Default: 1.0-3.0 seconds (balanced speed and safety)
- Recommended for large batches: 2.0-5.0 seconds
- For maximum safety: 3.0-8.0 seconds

If you encounter frequent 403 errors, consider:
- Increasing delay range: `--delay-min 3.0 --delay-max 8.0`
- Using `--no-fetch` to skip web fetching and manually fill Description/Constraints
- Processing files in smaller batches
- Waiting a few minutes between large batch runs

### Constraints

- When using `--fetch-online`, the tool will automatically fetch Description and Constraints from LeetCode web pages
- If fetching fails or fields are missing, placeholders will be added for manual filling
- Existing constraints are preserved if they exist

### Best Practices

- It's recommended to use `--dry-run` first to preview changes before actually modifying files
- Make sure LeetCode API cache is up-to-date: `python tools/sync_leetcode_data.py`

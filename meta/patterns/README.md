# Pattern Source Files Organization

This directory contains source files for generating pattern documentation. Each pattern has its own subdirectory with markdown files that are composed into the final documentation.

## Directory Structure

```
meta/patterns/
└── <pattern_name>/
    ├── _config.toml          # File ordering configuration (optional)
    ├── _header.md            # Core concepts and pattern overview (required)
    ├── _comparison.md        # Pattern comparison table (optional)
    ├── _decision.md          # When to use this pattern (optional)
    ├── _templates.md          # Quick reference templates (optional)
    └── XXXX_<name>.md        # Per-problem markdown files
```

## File Ordering Configuration

Each pattern directory can optionally include a `_config.toml` file to control the order of files when composing the final document.

### Configuration Format

```toml
# Header files (appear first, typically only _header.md)
header_files = [
    "_header.md"
]

# Problem files (appear in middle, ordered by LeetCode number or custom order)
problem_files = [
    "0003-base.md",
    "76-min-window.md",
    "09-min-subarray.md"
]

# Footer files (appear last, typically comparison, decision, templates)
footer_files = [
    "_comparison.md",
    "_decision.md",
    "_templates.md"
]
```

### Behavior

- **If `_config.toml` exists**: Files are ordered exactly as specified in the config
- **If `_config.toml` doesn't exist**: Falls back to default ordering:
  - Header files: `_header.md` first
  - Footer files: `_comparison.md`, `_decision.md`, `_templates.md` (in that order)
  - Problem files: Sorted alphabetically by filename

### Notes

- Files listed in config but not found in directory are silently skipped
- Files found in directory but not listed in config are appended at the end (for problem files) or placed after configured files (for header/footer files)
- The `_config.toml` file itself is excluded from the final document

## Example: Sliding Window

```
meta/patterns/sliding_window/
├── _config.toml
├── _header.md
├── _comparison.md
├── _decision.md
├── _templates.md
├──@03-base.md
├──@76-min-window.md
├──B09-min-subarray.md
├──C40-k-distinct.md
├──D38-anagrams.md
└──E67-permutation.md
```

The `_config.toml` ensures that problems appear in LeetCode number order (0003, 0076, 0209, etc.) rather than alphabetical order.

## Generating Documentation

After creating or updating source files, regenerate the documentation:

```bash
# Generate specific pattern
python tools/patterndocs/generate_pattern_docs.py --pattern <pattern_name>

# Generate all patterns
python tools/patterndocs/generate_pattern_docs.py --all
```


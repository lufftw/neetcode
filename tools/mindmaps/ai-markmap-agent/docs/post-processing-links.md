# Post-Processing Link Handling

## Overview

The post-processing module (`post_processing.py`) handles two key functions:

1. **Input Preprocessing**: Simplifies links before sending to LLM to reduce tokens
2. **Output Post-processing**: Converts plain text references back to full links

## Input Preprocessing (Token Reduction)

Before content is sent to the LLM, links are simplified while preserving titles:

```
[LeetCode 79 – Word Search](url) · [Solution](github_url)
→ LeetCode 79 – Word Search
```

This significantly reduces input tokens while keeping the problem title for LLM context. The full links are restored by post-processing.

---

## Output Post-Processing

The post-processing module converts LeetCode problem references in AI-generated mindmap content into standardized link formats.

## Target Format

```
[LeetCode 11 - Container With Most Water](leetcode_url) · [Solution](github_url)
```

**Features:**
- Includes problem number and title for clarity
- Title sourced from `tools/_staging/.cache/leetcode_problems.json` for consistency
- Automatically adds GitHub solution links (if available)

## Input Formats Handled

Post-processing handles various formats that AI may generate:

1. **Plain Text Format**
   - `LeetCode 11`
   - `LeetCode 11 - Container With Most Water`
   - `LC 11`

2. **Markdown Link Format**
   - `[LeetCode 11](url)`
   - `[LeetCode 11 - Title](url)`
   - `[LeetCode 11](url) · [Solution](url)` (existing Solution replaced)

3. **Incorrect URLs**
   - `[LeetCode 11](wrong_url)` → Automatically corrected

## Processing Steps (3 Steps)

### Step 1: Text Replacement

- `LC 11` → `LeetCode 11`
- `LC-11` → `LeetCode 11`
- `LeetCode11` → `LeetCode 11`

### Step 2: Remove Solution Artifacts

Remove plain text "· Solution" that LLM may have output (from learning the preprocessing pattern):

- `LeetCode 11 · Solution` → `LeetCode 11`

### Step 3: Convert to Complete Links

Convert all LeetCode references to complete links with Solution in one step:

**Input:**
```
LeetCode 11
```

**Output:**
```
[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
```

This step handles:
- Plain text → complete link with Solution
- Existing links → replace with correct URL and add Solution
- Existing links with Solution → regenerate complete link

## Processing Flow

### Overall Flow

1. **Writer Phase**: Produces raw markdown (**no post-processing**)
   - Saved to debug output
   - Used for translation phase

2. **Translation Phase**: Translates raw markdown (**no post-processing**)
   - Saved to debug output
   - Produces translated raw markdown

3. **Post-Processing Phase**: Processes links for English and Chinese
   - Simultaneously processes `writer_outputs` (English) and `translated_outputs` (Chinese)
   - Generates standardized links for all languages

## Data Sources

### Local TOML Files

Load problem metadata from `meta/problems/` directory:
- Problem titles
- Solution file paths

### LeetCode API Cache

Load from `tools/_staging/.cache/leetcode_problems.json`:
- LeetCode URLs
- Slugs
- Problem titles

**Priority:**
1. Local TOML data with solution files (priority)
2. API cache data (supplement)

## Examples

### Example 1: Plain Text Conversion

**Before:**
```markdown
- LeetCode 11
- LeetCode 3 - Longest Substring
```

**After:**
```markdown
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
```

### Example 2: Existing Links with Solution

**Before:**
```markdown
- [LeetCode 11](url) · [Solution](old_github_url)
- [LeetCode 11](url)[Solution](old_github_url)
```

**After:**
```markdown
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
```

### Example 3: Mixed Formats

**Before:**
```markdown
- LC 11
- LeetCode 11 · Solution
- [LeetCode 11](wrong_url)
```

**After:**
```markdown
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](...)
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](...)
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) · [Solution](...)
```

## Configuration

Post-processing behavior is controlled by `workflow.post_processing` in `config/config.yaml`:

```yaml
workflow:
  post_processing:
    text_replacements:
      - pattern: "\\bLC[-\\s]?(\\d+)"
        replacement: "LeetCode \\1"
```

## Related Files

- `src/post_processing.py` - Post-processing main module (280 lines)
- `src/leetcode_api.py` - LeetCode API data loading
- `src/graph.py` - Workflow integration
- `../../tests/test_post_processing.py` - Unit tests (24 tests)

## Testing

Run unit tests:
```bash
python -m pytest tools/tests/test_post_processing.py -v
```

Test coverage:
- Input preprocessing (simplify links for LLM)
- Solution artifact removal
- Link pattern matching (all formats)
- Duplicate prevention

## Notes

1. **One-Step Conversion**: All LeetCode references are converted to complete links with Solution in a single step
2. **Pattern Matching**: Regex matches entire link including existing Solution to avoid duplicates
3. **Data Normalization**: Solution file paths are normalized from both `solution_file` and `files.solution` formats
4. **Stats Output**: Single summary line shows conversion count (e.g., "✓ Converted 15 LeetCode references, 12 with Solution links")

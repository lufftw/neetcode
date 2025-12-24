# Post-Processing Link Handling

## Overview

The post-processing module (`post_processing.py`) is responsible for converting LeetCode problem references in AI-generated mindmap content into standardized link formats.

## Link Format

### Target Format

```
[LeetCode 11 - Container With Most Water](leetcode_url) | [Solution](github_url)
```

**Features:**
- Includes problem number and title for clarity
- Title sourced from `tools/.cache/leetcode_problems.json` for consistency
- Automatically adds GitHub solution links (if available)

### Input Formats Handled

Post-processing handles the following various formats that AI may generate:

1. **Plain Text Format**
   - `LeetCode 11`
   - `LeetCode 11 - Container With Most Water`
   - `LC 11`

2. **Markdown Link Format**
   - `[LeetCode 11](url)`
   - `[LeetCode 11 - Container With Most Water](url)`
   - `[LC 11](url)`

3. **Incorrect URLs**
   - `[LeetCode 11](wrong_url)` → Automatically corrected to the correct URL

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

### Post-Processing Steps

### Step 1: Text Replacement

- `LC 11` → `LeetCode 11`
- `LC-11` → `LeetCode 11`
- `LeetCode11` → `LeetCode 11`

### Step 2: Link Conversion

Convert plain text or existing links to standard format with title:

**Input:**
```
LeetCode 11 - Container With Most Water
```

**Output:**
```
[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/)
```

Note: Title is sourced from `tools/.cache/leetcode_problems.json` (using `frontend_question_id` for lookup).

### Step 3: URL Normalization

Ensure all LeetCode URLs use the correct format:
- Remove file name format slugs (e.g., `0011_container_with_most_water`)
- Convert to standard slugs (e.g., `container-with-most-water`)
- Ensure ending with `/description/`

### Step 4: Add GitHub Solution Links

If a problem has a corresponding solution file, automatically add GitHub link:

**Input:**
```
[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/)
```

**Output:**
```
[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
```

## Data Sources

### Local TOML Files

Load problem metadata from `meta/problems/` directory, including:
- Problem titles
- Solution file paths
- Other metadata

### LeetCode API Cache

Load from `tools/.cache/leetcode_problems.json`:
- LeetCode URLs
- Slugs
- Problem titles (as supplement)

**Priority:**
1. Local TOML data (priority)
2. API cache data (supplement)

## Comparison Files

After each post-processing execution, a comparison file is automatically generated:

**Location:** `outputs/final/post_processing_comparison_{timestamp}.md`

**Content:**
- Before/After comparison for each language (English, Chinese, etc.)
- Before: Original content (Writer/Translation output, unprocessed)
- After: Post-processed content (links standardized)

**Purpose:**
- Check post-processing effectiveness
- Verify links are correctly generated (English and Chinese)
- Compare differences before and after processing

## Flow Confirmation

### Writer Phase Output

**Output:** Raw markdown (no post-processing)
```
- LeetCode 11 - Container With Most Water
- LeetCode 3 - Longest Substring
```

**Debug Output:** `llm_output_writer_write.md` (original content)

### Translation Phase Output

**Input:** Writer's raw markdown (no post-processing)

**Output:** Translated raw markdown (no post-processing)
```
- LeetCode 11 - 盛最多水的容器
- LeetCode 3 - 無重複字符的最長子串
```

**Debug Output:** 
- `translation_before_general_en_general_zh-TW.md` (before translation)
- `translation_after_general_en_general_zh-TW.md` (after translation)

### Post-Processing Phase Output

**Input:** 
- Writer raw markdown (English)
- Translated raw markdown (Chinese)

**Output:** Post-processed markdown (English and Chinese)

**English:**
```
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](...)
- [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](...)
```

**Chinese:**
```
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](...)
- [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](...)
```

**Debug Output:**
- `post_processing_before_general_en.md` (English before processing)
- `post_processing_after_general_en.md` (English after processing)
- `post_processing_before_general_zh-TW.md` (Chinese before processing)
- `post_processing_after_general_zh-TW.md` (Chinese after processing)

**Comparison File:** `post_processing_comparison_{timestamp}.md` (contains comparisons for all languages)

## Examples

### Example 1: Plain Text Conversion

**Before:**
```markdown
- LeetCode 11 - Container With Most Water
- LeetCode 3 - Longest Substring
```

**After:**
```markdown
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [LeetCode 3 - Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
```

### Example 2: Correcting Incorrect URLs

**Before:**
```markdown
- [LeetCode 11](https://leetcode.com/problems/0011_container_with_most_water/)
```

**After:**
```markdown
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
```

### Example 3: Handling Multiple Formats

**Before:**
```markdown
- LC 11
- LeetCode 11 - Container With Most Water
- [LeetCode 11](wrong_url)
```

**After:**
```markdown
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
```

## Configuration

Post-processing behavior is controlled by the `workflow.post_processing` configuration in `config/config.yaml`:

```yaml
workflow:
  post_processing:
    text_replacements:
      - pattern: "\\bLC[-\\s]?(\\d+)"
        replacement: "LeetCode \\1"
```

## Related Files

- `src/post_processing.py` - Post-processing main module
- `src/leetcode_api.py` - LeetCode API data loading
- `src/graph.py` - Workflow integration
- `tools/sync_leetcode_data.py` - API data synchronization tool

## Notes

1. **Complete Format**: Includes problem number and title (e.g., `LeetCode 11 - Container With Most Water`)
2. **Consistent Data Source**: Title sourced from `tools/.cache/leetcode_problems.json` using `frontend_question_id`
3. **Automatic Supplementation**: If local data lacks URLs, automatically supplements from API cache
4. **Comparison Files**: Comparison files are generated after each execution for easy effect checking
5. **Backward Compatibility**: Does not affect existing functionality, only supplements and standardizes

# Workflow Processing Order

## Processing Flow Confirmation

### Phase 4: Writer

**Output:**
- Raw markdown (**no post-processing**)
- Saved to `writer_outputs["general_en"]`

**Debug Output:**
- `llm_input_writer_write.md` - Writer input
- `llm_output_writer_write.md` - Writer output (raw markdown)

**Purpose:**
- Used as input for translation phase
- Save original AI output for inspection

---

### Phase 5: Translation

**Input:**
- `writer_outputs` (raw markdown, unprocessed)

**Output:**
- Translated raw markdown (**no post-processing**)
- Saved to `translated_outputs["general_zh-TW"]` etc.

**Debug Output:**
- `translation_before_{source}_{target}.md` - Content before translation
- `translation_after_{source}_{target}.md` - Content after translation (raw markdown)

**Purpose:**
- Save translation results for inspection
- Used as input for post-processing phase

---

### Phase 6: Post-Processing

**Input:**
- `writer_outputs` (English raw markdown)
- `translated_outputs` (Chinese raw markdown)

**Processing:**
- Simultaneously processes **all languages** raw markdown
- Generates standardized links for both English and Chinese

**Output:**
- Post-processed markdown (English and Chinese)
- Saved to `final_outputs`

**Debug Output:**
- `post_processing_before_{key}.md` - Content before post-processing (each language)
- `post_processing_after_{key}.md` - Content after post-processing (each language)

**Comparison File:**
- `post_processing_comparison_{timestamp}.md` - Contains Before/After comparison for all languages

---

## Flow Diagram

```
Writer Phase
    ↓
[Raw Markdown (EN)] → Debug: llm_output_writer_write.md
    ↓
Translation Phase
    ↓
[Raw Markdown (EN)] → [Raw Markdown (ZH-TW)] → Debug: translation_*.md
    ↓
Post-Processing Phase
    ↓
[Raw Markdown (EN)] ──┐
                      ├─→ Post-Processing → [Processed Markdown (EN)]
[Raw Markdown (ZH-TW)] ┘                    [Processed Markdown (ZH-TW)]
                      ↓
                  Debug: post_processing_*.md
                  Comparison: post_processing_comparison_*.md
```

---

## Important Principles

1. **Writer Output Not Post-Processed**: Keeps original AI output for easy inspection and debugging
2. **Translation Based on Original Content**: Translation phase uses unprocessed markdown to ensure translation accuracy
3. **Unified Post-Processing**: Final phase uniformly processes links for all languages to ensure consistency
4. **Debug Recording Throughout**: Each phase saves debug output for easy problem tracking

---

## Examples

### Writer Output (Raw)

```markdown
- LeetCode 11 - Container With Most Water
- LeetCode 3 - Longest Substring
```

### Translation Output (Raw)

```markdown
- LeetCode 11 - 盛最多水的容器
- LeetCode 3 - 無重複字符的最長子串
```

### Post-Processing Output (English)

```markdown
- [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](...)
- [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](...)
```

### Post-Processing Output (Chinese)

```markdown
- [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](...)
- [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](...)
```

---

## Related Documents

- [Post-Processing Link Handling](POST_PROCESSING_LINKS.md)
- [Main README](../README.md)

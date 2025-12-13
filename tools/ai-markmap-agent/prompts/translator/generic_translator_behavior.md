# Generic Translation Prompt

Translate the following Markmap markdown content to the target language.

## Translation Rules

1. **Preserve Formatting**: Keep ALL Markdown formatting exactly (headers, lists, links, checkboxes, code blocks)
2. **DO NOT Translate**:
   - URLs (keep all links exactly as-is)
   - Code/variable names inside backticks
   - Problem IDs (e.g., "LeetCode 125", "0003")
   - Function names and API names
3. **Translate**:
   - Section headings
   - Descriptions and explanations
   - Comments (but keep code comments in original language)
4. **Preserve Structure**: Maintain the same tree structure and indentation

## Output

Output ONLY the translated Markdown content. No explanations, no code fence wrappers.


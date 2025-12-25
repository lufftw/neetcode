# Post-Processing Solution Links - Technical Reference

## Overview

This document describes the technical implementation of Solution link generation in the post-processing module.

## Processing Flow (3 Steps)

```python
def process(self, content: str) -> str:
    # Step 1: Text replacements (LC → LeetCode)
    result = self._apply_text_replacements(content)
    
    # Step 2: Remove "· Solution" artifacts
    result = self._remove_solution_artifacts(result)
    
    # Step 3: Convert all LeetCode references to complete links
    result = self._convert_to_complete_links(result)
    
    return result
```

## Key Method: `_convert_to_complete_links`

This method handles all LeetCode reference conversions in one pass:

### First Pass: Handle Existing Links

```python
# Pattern matches [LeetCode...](url) with optional Solution link
pattern = r'\[(LeetCode\s+\d+[^\]]*)\]\(([^)]+)\)(\s*(?:·|\xb7|\|)?\s*\[Solution\]\([^)]+\))?'
```

**Key Feature**: The pattern captures existing Solution links (group 3) so the entire match is replaced, preventing duplicate Solution links.

### Second Pass: Handle Plain Text

```python
# Pattern matches plain text LeetCode references
pattern = r'(?<!\[)LeetCode\s+(\d+)(\s*[-–—:]\s*[^\[\]\n(]+)?(?!\]\()'
```

## Solution File Lookup

### Data Normalization

The `_normalize_problem_data` method handles both data formats:

```python
def _normalize_problem_data(self, data: dict) -> dict:
    normalized = {
        "url": data.get("url", ""),
        "title": data.get("title", ""),
        "solution_file": None,
    }
    
    # Get solution file from either format
    if data.get("solution_file"):
        normalized["solution_file"] = data["solution_file"]
    elif data.get("files", {}).get("solution"):
        normalized["solution_file"] = data["files"]["solution"]
    
    return normalized
```

This ensures compatibility with:
- Direct format: `{"solution_file": "path"}`
- Nested format: `{"files": {"solution": "path"}}`

### Problem ID Lookup

Problems are stored with multiple key formats:

```python
# For problem ID "79":
lookup["0079"] = normalized_data  # 4-digit padded
lookup["79"] = normalized_data    # Integer string
```

## Complete Link Generation

### `_build_complete_link` Method

```python
def _build_complete_link(self, problem_id: str) -> str:
    problem = self.problems_lookup.get(problem_id.zfill(4)) or \
              self.problems_lookup.get(problem_id)
    
    if not problem:
        return f"LeetCode {problem_id}"
    
    # Build LeetCode link with title
    url = problem.get("url", "")
    title = problem.get("title", "")
    link_text = f"LeetCode {problem_id} - {title}" if title else f"LeetCode {problem_id}"
    leetcode_link = f"[{link_text}]({url})"
    
    # Add Solution link if available
    solution_file = problem.get("solution_file")
    if solution_file:
        github_url = self.github_template.format(solution_file=solution_file)
        return f"{leetcode_link} · [Solution]({github_url})"
    
    return leetcode_link
```

## Data Flow

```
meta/problems/*.toml + tools/.cache/leetcode_problems.json
    ↓
merge_leetcode_api_data()
    ↓
_build_problems_lookup() → _normalize_problem_data()
    ↓
problems_lookup = {"0079": {url, title, solution_file}, ...}
    ↓
_convert_to_complete_links() → _build_complete_link()
    ↓
[LeetCode 79 - Word Search](url) · [Solution](github_url)
```

## Example Transformation

### Input
```markdown
[LeetCode 79](https://leetcode.com/problems/word-search/) · [Solution](old_url)
```

### Processing
1. **Regex Match**: Captures entire string including existing Solution
   - Group 1: `LeetCode 79`
   - Group 2: `https://leetcode.com/problems/word-search/`
   - Group 3: ` · [Solution](old_url)` (captured but ignored)

2. **Problem Lookup**: Find ID "79" → normalized data with title and solution_file

3. **Build Complete Link**: Generate new link with correct URL and fresh Solution link

### Output
```markdown
[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) · [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)
```

## Troubleshooting

### Solution Links Not Added

1. **Check problem data**: Ensure `solution_file` exists in normalized data
2. **Check lookup**: Verify problem ID format matches lookup keys
3. **Check stats output**: Look for "✓ Converted X LeetCode references, Y with Solution links"

### Duplicate Solution Links

This should not happen with the new implementation. The regex pattern captures existing Solution links:

```python
r'...\)(\s*(?:·|\xb7|\|)?\s*\[Solution\]\([^)]+\))?'
#      ↑ Captures existing Solution link
```

The entire match (including existing Solution) is replaced with the new complete link.

## Stats Output

The module outputs a single summary line:

```
✓ Converted 15 LeetCode references, 12 with Solution links
```

This shows:
- Total LeetCode references converted
- How many had solution files available

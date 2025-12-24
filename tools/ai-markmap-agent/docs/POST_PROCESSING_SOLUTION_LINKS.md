# Post-Processing Solution Links Check Report

## Processing Flow

Post-processing is executed in the following order (`PostProcessor.process()` method):

### Step 1: Text Replacement
- `LC 11` → `LeetCode 11`
- `LC-11` → `LeetCode 11`

### Step 2: Convert Plain Text to Links (`_convert_plain_leetcode_to_links`)
- Process existing links: `[LeetCode 79 - Word Search](wrong_url)` → `[LeetCode 79 - Word Search](correct_url)`
- Process plain text: `LeetCode 79` → `[LeetCode 79 - Word Search](url)`
- Uses URL and title data from `tools/.cache/leetcode_problems.json` (lookup by `frontend_question_id`)

### Step 3: Normalize LeetCode Links (`_normalize_leetcode_links`)
- Fix URL format to ensure it ends with `/description/`
- Example: `https://leetcode.com/problems/word-search/` → `https://leetcode.com/problems/word-search/description/`

### Step 4: Add Solution Links (`_add_github_solution_links`)
- Find all links in the format `[LeetCode {id} - {title}](url)`
- If the problem has a `[files].solution` field in `meta/problems/*.toml`
- Add Solution link: `[LeetCode 79 - Word Search](url) | [Solution](github_url)`

## Solution Link Processing Logic

### 1. Problem Lookup (`_add_github_solution_links`)

```python
# Extract problem ID from link text
id_match = re.search(r'LeetCode\s+(\d+)', link_text)
problem_id = id_match.group(1)  # Example: "79"

# Try multiple ID formats for lookup
lookup_keys = [
    problem_id.zfill(4),      # "0079"
    problem_id,              # "79"
    str(int(problem_id)).zfill(4),  # "0079" (normalized)
    str(int(problem_id))     # "79" (normalized)
]

for key in lookup_keys:
    problem = self.problems_lookup.get(key)
    if problem:
        break
```

### 2. Solution File Check

```python
# Check if solution file exists
files = problem.get("files", {})
solution_file = files.get("solution", "")

if solution_file:
    # Generate GitHub URL
    github_url = self.github_template.format(solution_file=solution_file)
    # Add link
    return f"{full_text} | [Solution]({github_url})"
```

### 3. Problem Data Lookup Table Construction (`_build_problems_lookup`)

Load data from `meta/problems/*.toml` files:

```toml
# 0079_word_search.toml
id = "0079"
leetcode_id = 79
[files]
solution = "solutions/0079_word_search.py"
```

The lookup table stores multiple key formats:
- `"0079"` → problem data
- `"79"` → problem data
- `str(int("0079"))` → problem data (if different)

## Data Flow

```
state.get("problems", {})  # Loaded from DataSourcesLoader
    ↓
PostProcessor(config, problems=problems)
    ↓
merge_leetcode_api_data(problems)  # Merge API cache data
    ↓
_build_problems_lookup(problems)  # Build ID lookup table
    ↓
_add_github_solution_links(content)  # Add Solution links
```

## Verification Checkpoints

### ✅ Checked Items

1. **Problems Data Passing**
   - `graph.py:1053`: `PostProcessor(config, problems=state.get("problems", {}))`
   - ✅ Correctly passed

2. **Lookup Table Construction**
   - `_build_problems_lookup`: Supports multiple ID formats
   - ✅ Logic is correct

3. **Solution Link Addition**
   - `_add_github_solution_links`: Checks `files.solution` field
   - ✅ Logic is correct

4. **Regular Expression Matching**
   - Pattern: `r'\[(LeetCode\s+\d+[^\]]*)\]\(([^)]+)\)'`
   - ✅ Can match `[LeetCode 79](url)` and `[LeetCode 79 - Title](url)`

### 🔍 Items to Verify

1. **Whether Problems Data is Correctly Loaded to State**
   - Check `graph.py:1188`: `"problems": data.get("problems", {})`
   - Check `main.py:293`: `data = loader.load_all()`

2. **Files Field Format in TOML Files**
   - Confirm format is: `[files] solution = "solutions/0079_word_search.py"`
   - Not: `files.solution` or `files["solution"]`

3. **Data Flow at Runtime**
   - May need to add debug output for verification

## Example

### Input
```markdown
[LeetCode 79](https://leetcode.com/problems/word-search/)
```

### Processing Steps
1. Step 2: Convert to link with title → `[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/)`
   - Title "Word Search" sourced from `tools/.cache/leetcode_problems.json`
2. Step 3: Normalize URL → ensure ends with `/description/`
3. Step 4: Lookup problem ID "79" → Found in cache and TOML
4. Step 4: Check `files.solution` → Found `"solutions/0079_word_search.py"`
5. Step 4: Generate GitHub URL → `https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py`

### Output
```markdown
[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)
```

## Potential Issues

1. **If Solution links are not added, possible reasons:**
   - Problems data not correctly loaded to state
   - Missing `[files].solution` field in TOML files
   - Problem ID matching failed (lookup logic has been improved)
   - Regular expression matching failed (verified should be able to match)

2. **Debugging Suggestions:**
   - Add debug output in `_add_github_solution_links`
   - Check contents of `self.problems_lookup`
   - Verify structure of `problem.get("files", {})`

## Improvement Suggestions

1. ✅ Improved: Problem ID lookup logic, supports multiple formats
2. ✅ Improved: Clearer lookup key list
3. ✅ Improved: Links now include full title (e.g., `[LeetCode 79 - Word Search](url)`)
4. ✅ Improved: Title sourced from `tools/.cache/leetcode_problems.json` using `frontend_question_id`
5. 🔄 Optional: Add debug mode to output lookup process

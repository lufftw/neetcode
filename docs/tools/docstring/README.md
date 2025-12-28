# Docstring Formatter

> **Purpose**: Transform LeetCode Question objects into structured docstring specifications  
> **Location**: `tools/docstring/formatter.py`  
> **Last Updated**: {{ git_revision_date_localized }}

This module extracts and normalizes docstring-relevant content from LeetCode problems, including descriptions, examples, constraints, topics, hints, and follow-up questions. It provides a unified API for generating file-level docstrings according to the project specification.

---

## Features

- **HTML Parsing**: Extracts structured content from LeetCode HTML problem descriptions
- **Multiple Formats**: Handles both new and legacy LeetCode HTML formats
- **Complete Data**: Extracts all docstring components (description, examples, constraints, topics, hints, follow-ups, notes)
- **Normalized Output**: Produces spec-aligned, consistent format for docstring generation
- **Cache Integration**: Uses SQLite-backed cache from `tools/leetcode-api` for performance
- **Backward Compatible**: Maintains legacy API for existing code

---

## Quick Start

### Basic Usage

```python
from tools.docstring.formatter import get_full_docstring_data

# Get all docstring data for a problem
data = get_full_docstring_data("two-sum")

# Access structured components
print(data['title'])        # "Two Sum"
print(data['description'])  # List of description lines
print(data['examples'])     # List of example dicts
print(data['constraints'])  # List of constraint lines
print(data['topics'])       # "Array, Hash Table"
print(data['hints'])        # ["Hint 1: ...", "Hint 2: ..."]
print(data['follow_ups'])   # ["Follow-up question text"]
print(data['note'])         # Optional note string or None
```

### Legacy API (Backward Compatible)

```python
from tools.docstring.formatter import get_description_and_constraints

# Get only description and constraints
desc, constraints = get_description_and_constraints("two-sum")
```

### Direct Question Access

```python
from tools.docstring.formatter import get_question_data

# Get complete Question object
question = get_question_data("two-sum")
print(question.title)
print(question.difficulty)
print(question.Body)  # Raw HTML
```

---

## API Reference

### `get_full_docstring_data(slug: str) -> dict`

Get all data needed for generating a complete file-level docstring.

**Parameters:**
- `slug` (str): LeetCode problem slug (e.g., "two-sum")

**Returns:** Dictionary with the following structure:

```python
{
    'title': str,              # Problem title (e.g., "Two Sum")
    'url': str,                # LeetCode problem URL
    'description': List[str],  # List of description lines (plain text)
    'examples': List[dict],    # List of example dictionaries
    'constraints': List[str],  # List of constraint lines (each starts with "- ")
    'topics': str,             # Formatted topics (e.g., "Array, Hash Table")
    'hints': List[str],        # Formatted hints (e.g., ["Hint 1: ...", "Hint 2: ..."])
    'follow_ups': List[str],   # List of follow-up question strings
    'note': Optional[str],     # Note text or None
}
```

**Example:**

```python
data = get_full_docstring_data("two-sum")

# Example structure
example = data['examples'][0]
# {
#     'number': 1,
#     'img': None or '<img src="...">',
#     'input': 'nums = [2,7,11,15], target = 9',
#     'output': '[0,1]',
#     'explanation': 'Because nums[0] + nums[1] == 9, we return [0, 1].'
# }
```

**Returns empty structure if question not found:**

```python
{
    'title': '',
    'url': '',
    'description': [],
    'examples': [],
    'constraints': [],
    'topics': '',
    'hints': [],
    'follow_ups': [],
    'note': None,
}
```

---

### `get_description_and_constraints(slug: str) -> Tuple[List[str], List[str]]`

Legacy backward-compatible API for fetching description and constraints only.

**Parameters:**
- `slug` (str): LeetCode problem slug (e.g., "combinations")

**Returns:** Tuple of `(description_lines, constraint_lines)` where:
- `description_lines`: List of description strings (plain text, no examples/constraints)
- `constraint_lines`: List of constraint strings (each starts with "- ")

**Example:**

```python
desc, constraints = get_description_and_constraints("two-sum")

# desc: ["Given an array of integers nums...", "You may assume that..."]
# constraints: ["- 2 <= nums.length <= 10^4", "- -10^9 <= nums[i] <= 10^9", ...]
```

**Returns:** `([], [])` if question not found or has no Body

---

### `get_question_data(slug: str, force_refresh: bool = False) -> Optional[Question]`

Get complete Question object for direct access to all question data.

**Parameters:**
- `slug` (str): LeetCode problem slug (e.g., "two-sum")
- `force_refresh` (bool): If True, bypass cache and fetch fresh data from network

**Returns:** `Question` object or `None` if not found

**Question Object Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `QID` | `int` | Question ID |
| `title` | `str` | Problem title |
| `titleSlug` | `str` | URL slug |
| `difficulty` | `str` | "Easy", "Medium", or "Hard" |
| `topicTags` | `str` | Comma-separated tags (e.g., "array,hash-table") |
| `Body` | `str` | HTML problem description |
| `Hints` | `List[str]` | List of hint strings |
| `Code` | `str` | Code template |
| `SimilarQuestions` | `List[int]` | Related question IDs |

**Example:**

```python
q = get_question_data("two-sum")
if q:
    print(q.title)           # "Two Sum"
    print(q.difficulty)      # "Easy"
    print(q.topicTags)       # "array,hash-table"
    print(q.Body)            # HTML content
    print(q.Hints)           # ["hint1", "hint2"]
```

---

## Data Format Details

### Description

- **Format**: List of plain text lines
- **Content**: Problem statement only (excludes Examples, Constraints, Follow-up, Note sections)
- **Stops at**: First occurrence of "Example", "Constraints", "Follow-up", "Note", or "Custom Judge"

### Examples

- **Format**: List of dictionaries with keys: `number`, `img`, `input`, `output`, `explanation`
- **Number**: Example number (1, 2, 3, ...)
- **Image**: Preserved `<img>` tag string or `None`
- **Input/Output**: Plain text (HTML tags removed)
- **Explanation**: Plain text, may span multiple lines
- **Supports**: Both new format (`<pre>` blocks) and old format (separate `<p>` elements)

### Constraints

- **Format**: List of strings, each starting with "- "
- **Source**: Extracted from `<ul><li>` tags in HTML
- **Superscript**: `<sup>n</sup>` converted to `^n` notation
- **Example**: `["- 2 <= nums.length <= 10^4", "- -10^9 <= nums[i] <= 10^9"]`

### Topics

- **Format**: Comma-separated string with capitalized words
- **Input**: `"array,hash-table"` (from `Question.topicTags`)
- **Output**: `"Array, Hash Table"`
- **Transformation**: Hyphens removed, words capitalized

### Hints

- **Format**: List of strings with numbered format
- **Input**: `["Try a hash table", "A really brute force way..."]`
- **Output**: `["Hint 1: Try a hash table", "Hint 2: A really brute force way..."]`

### Follow-ups

- **Format**: List of plain text strings
- **Handles**: Multiple HTML formats (with/without `<p>` tags, with `&nbsp;`)
- **Content**: Full follow-up question text (HTML tags removed)

### Note

- **Format**: Optional string or `None`
- **Content**: Note section text (if present in problem)

---

## Architecture

```
tools/docstring/
└── formatter.py              # Main module
    ├── Public API
    │   ├── get_full_docstring_data()      # Complete docstring data
    │   ├── get_description_and_constraints()  # Legacy API
    │   └── get_question_data()            # Direct Question access
    │
    └── Internal Extractors
        ├── _extract_brief_description()   # Description only
        ├── _extract_examples()            # All examples
        ├── _extract_constraints()         # Constraints list
        ├── _extract_follow_up()           # Follow-up questions
        ├── _extract_note()                # Note section
        ├── _format_topics()               # Topic formatting
        ├── _format_hints()                # Hint formatting
        └── _extract_text_from_html()      # HTML → text utility
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│              get_full_docstring_data(slug)                  │
│                           │                                 │
│                           ▼                                 │
│              get_question(slug) [from leetcode-api]        │
│                           │                                 │
│                           ▼                                 │
│                    Question Object                          │
│         (with Body, Hints, topicTags, etc.)                │
│                           │                                 │
│         ┌─────────────────┼─────────────────┐               │
│         ▼                 ▼                 ▼               │
│   _extract_*()      _format_topics()  _format_hints()      │
│         │                 │                 │               │
│         └─────────────────┼─────────────────┘               │
│                           ▼                                 │
│              Structured Dictionary                          │
│    {title, url, description, examples, constraints, ...}    │
└─────────────────────────────────────────────────────────────┘
```

### Dependencies

- **`tools/leetcode-api`**: Provides `get_question()` and `Question` object
- **Standard Library**: `re`, `html`, `typing`, `pathlib`

---

## Usage Examples

### Generate Complete Docstring Data

```python
from tools.docstring.formatter import get_full_docstring_data

data = get_full_docstring_data("two-sum")

# Build docstring from components
docstring = f"""
{data['title']}

{chr(10).join(data['description'])}

Examples:
"""
for ex in data['examples']:
    docstring += f"""
    Example {ex['number']}:
        Input: {ex['input']}
        Output: {ex['output']}
        Explanation: {ex['explanation']}
"""

docstring += f"""
Constraints:
{chr(10).join(data['constraints'])}

Topics: {data['topics']}
"""
```

### Extract Only Description and Constraints

```python
from tools.docstring.formatter import get_description_and_constraints

desc, constraints = get_description_and_constraints("two-sum")

print("Description:")
for line in desc:
    print(f"  {line}")

print("\nConstraints:")
for constraint in constraints:
    print(f"  {constraint}")
```

### Access Raw Question Data

```python
from tools.docstring.formatter import get_question_data

# Get from cache (default)
q = get_question_data("two-sum")

# Force refresh from network
q = get_question_data("two-sum", force_refresh=True)

if q:
    # Access raw HTML
    print(q.Body)
    
    # Access all metadata
    print(f"ID: {q.QID}")
    print(f"Difficulty: {q.difficulty}")
    print(f"Acceptance: {q.acceptanceRate}%")
    print(f"Similar: {q.SimilarQuestions}")
```

### Interactive Testing

Run the module directly for interactive testing:

```bash
python tools/docstring/formatter.py
```

Enter a problem slug when prompted to see both API outputs.

---

## HTML Parsing Details

### Supported Formats

The module handles multiple LeetCode HTML formats:

1. **New Format** (Example in `<pre>` block):
   ```html
   <p><strong class="example">Example 1:</strong></p>
   <pre>
   <strong>Input:</strong> nums = [2,7,11,15], target = 9
   <strong>Output:</strong> [0,1]
   <strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1].
   </pre>
   ```

2. **Old Format** (Separate elements):
   ```html
   <p><strong>Example 1:</strong></p>
   <p><strong>Input:</strong> nums = [2,7,11,15], target = 9</p>
   <p><strong>Output:</strong> [0,1]</p>
   ```

### HTML Cleaning

- **Removes**: `<script>`, `<style>`, all HTML tags
- **Preserves**: Text content, `<img>` tags (in examples)
- **Converts**: `<sup>n</sup>` → `^n` (for constraints)
- **Normalizes**: Multiple spaces/newlines → single space/double newline

### Stop Keywords

Description extraction stops at:
- `"example"` (case-insensitive)
- `"constraints:"`
- `"follow-up:"` or `"follow-up"`
- `"note:"`
- `"custom judge"`

---

## Integration with Other Tools

### `fix_docstring.py`

The `tools/review-code/fix_docstring.py` tool uses this module to generate docstrings:

```python
from tools.docstring.formatter import get_full_docstring_data

data = get_full_docstring_data(slug)
# ... format into docstring and write to file
```

### `leetcode-api` Module

This module depends on `tools/leetcode-api` for:
- **Caching**: SQLite-backed cache reduces network requests
- **Unified API**: Same `Question` interface whether from cache or network
- **Performance**: Fast batch operations using local cache

See [leetcode-api README](../leetcode-api/README.md) for details.

---

## Error Handling

### Question Not Found

All functions handle missing questions gracefully:

```python
# Returns empty structure
data = get_full_docstring_data("non-existent-slug")
# data = {'title': '', 'url': '', 'description': [], ...}

# Returns empty tuple
desc, constraints = get_description_and_constraints("non-existent-slug")
# desc = [], constraints = []

# Returns None
q = get_question_data("non-existent-slug")
# q = None
```

### Missing Data

- **Empty Body**: Returns empty lists/None for all components
- **No Examples**: `examples = []`
- **No Constraints**: `constraints = []`
- **No Hints**: `hints = []`
- **No Follow-ups**: `follow_ups = []`
- **No Note**: `note = None`

---

## Related Documentation

- [LeetCode API](../leetcode-api/README.md) - SQLite cache and Question API
- [Review Code Tool](../../README.md) - File-level docstring generator
- [review-code README](../../../tools/review-code/README.md) - Docstring format specification

---

## Module Structure

```
tools/docstring/
├── formatter.py              # Main module (503 lines)
│   ├── Public Functions
│   │   ├── get_full_docstring_data()
│   │   ├── get_description_and_constraints()
│   │   └── get_question_data()
│   │
│   └── Internal Functions
│       ├── _extract_text_from_html()
│       ├── _extract_brief_description()
│       ├── _extract_constraints()
│       ├── _extract_examples()
│       ├── _extract_follow_up()
│       ├── _extract_note()
│       ├── _format_topics()
│       └── _format_hints()
│
└── README.md                 # This file
```

---

## Testing

Run the module interactively:

```bash
python tools/docstring/formatter.py
```

Enter a problem slug to test extraction:

```
Enter LeetCode problem slug (e.g. two-sum): two-sum

=== Using get_description_and_constraints (backward-compatible) ===
Description:
Given an array of integers nums and an integer target...
...

=== Using get_full_docstring_data (new API) ===
Title: Two Sum
URL: https://leetcode.com/problems/two-sum/
Examples: 2
  Example 1:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
...
```

---

## Notes

- **HTML Format Changes**: LeetCode occasionally updates HTML structure; the module handles both old and new formats
- **Performance**: Uses SQLite cache from `leetcode-api` for fast repeated access
- **Offline Support**: Works with cached data without network connection
- **Backward Compatibility**: `get_description_and_constraints()` maintained for legacy code


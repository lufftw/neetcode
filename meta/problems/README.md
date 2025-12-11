# Problem Metadata Files

This directory contains TOML metadata files for LeetCode problems. Each problem has one TOML file that describes its properties, relationships, and file locations.

## File Naming Convention

Files are named using the format: `{problem_id}_{slug}.toml`

Examples:
- `0001_two_sum.toml`
- `0003_longest_substring_without_repeating_characters.toml`
- `0011_container_with_most_water.toml`

## Required Fields

Every problem TOML file must include the following sections:

### 1. Problem Info

Basic problem identification:

```toml
# ===== Problem Info =====
id = "0001"                    # Problem ID (4-digit zero-padded)
slug = "0001_two_sum"          # File slug (usually id_title_snake_case)
title = "Two Sum"              # Problem title
leetcode_id = 1                # LeetCode problem number
url = "https://leetcode.com/problems/two-sum/"  # LeetCode problem URL
```

**Required fields:**
- `id`: 4-digit zero-padded string (e.g., "0001", "0023")
- `slug`: Snake-case identifier matching filename (without .toml)
- `title`: Problem title as shown on LeetCode
- `leetcode_id`: Integer LeetCode problem number
- `url`: Full LeetCode problem URL

### 2. LeetCode Official Metadata

Standard LeetCode categorization:

```toml
# ===== LeetCode Official Metadata =====
difficulty = "easy"            # "easy", "medium", or "hard"
topics = ["array", "hash_table"]  # Array of LeetCode topic tags
companies = ["google", "amazon", "meta"]  # Array of company IDs
```

**Required fields:**
- `difficulty`: One of `"easy"`, `"medium"`, `"hard"`
- `topics`: Array of topic strings (see `ontology/topics.toml` for valid values)
- `companies`: Array of company IDs (see `ontology/companies.toml` for valid values)

### 3. Roadmaps

Learning path associations:

```toml
# ===== Roadmaps =====
roadmaps = ["neetcode_150", "blind_75", "leetcode_top_100"]
```

**Required fields:**
- `roadmaps`: Array of roadmap IDs (see `ontology/roadmaps.toml` for valid values)
- Can be empty array `[]` if not part of any roadmap

### 4. Ontology Tags (Problem Level)

Knowledge graph relationships at the problem level:

```toml
# ===== Ontology Tags (Problem Level) =====
api_kernels      = ["SubstringSlidingWindow"]  # Array of API kernel IDs
patterns         = ["sliding_window_unique"]   # Array of pattern IDs
families         = ["substring_window"]        # Array of family IDs
data_structures  = ["string", "hash_map"]      # Array of data structure IDs
algorithms       = ["sliding_window"]          # Array of algorithm IDs
related_problems = ["0159", "0340"]            # Array of related problem IDs
```

**Required fields (can be empty arrays):**
- `api_kernels`: Array of API kernel IDs (see `ontology/api_kernels.toml`)
- `patterns`: Array of pattern IDs (see `ontology/patterns.toml`)
- `families`: Array of family IDs (see `ontology/families.toml`)
- `data_structures`: Array of data structure IDs (see `ontology/data_structures.toml`)
- `algorithms`: Array of algorithm IDs (see `ontology/algorithms.toml`)
- `related_problems`: Array of related problem IDs (4-digit format, e.g., "0159")

### 5. File Locations

**CRITICAL**: This section determines whether AI mind maps link to your GitHub solution or LeetCode.

```toml
# ===== File Locations =====
[files]
solution  = "solutions/0001_two_sum.py"              # Path to solution file (relative to repo root)
generator = "generators/0001_two_sum.py"            # Path to generator file (optional)
tests_dir = "tests/0001_two_sum/"                    # Path to tests directory (optional)
```

**Required fields:**
- `solution`: **MUST be set** if you have a solution file. This is used by AI mind map generator to create GitHub links.
  - Format: `"solutions/{problem_slug}.py"`
  - If empty or missing, AI will link to LeetCode instead of GitHub
  - Example: `solution = "solutions/0011_container_with_most_water.py"`

**Optional fields:**
- `generator`: Path to test case generator file
- `tests_dir`: Path to test cases directory

### 6. Solutions (Optional)

If the problem has multiple solution approaches, document them:

```toml
# ===== Solutions =====
[[solutions]]
key    = "default"              # Solution key (used in test_runner)
class  = "Solution"              # Class name in solution file
method = "twoSum"                # Method name

api_kernels      = []            # Solution-specific API kernels
patterns         = []            # Solution-specific patterns
families         = ["two_sum_variants"]
data_structures  = ["array", "hash_map"]
algorithms       = []
related_problems = ["0167"]

role       = "base"              # "base" or "variant"
variant    = ""                   # Variant name if role is "variant"
based_on   = []                   # Array of solution references (e.g., ["0003#default"])
delta      = ""                   # Description of differences from base
complexity = "O(n) time, O(n) space"  # Time and space complexity
notes      = "Single pass with hash map to find complement."  # Additional notes
```

**Fields:**
- `key`: Unique identifier for this solution (used by test runner)
- `class`: Class name containing the solution
- `method`: Method name implementing the solution
- `role`: `"base"` for primary solution, `"variant"` for alternative approaches
- `variant`: Name describing the variant (e.g., "dictionary", "set_while_loop")
- `based_on`: Array of references to other solutions (format: `"{problem_id}#{key}"`)
- `delta`: Brief description of how this differs from the base solution
- `complexity`: Time and space complexity notation
- `notes`: Additional implementation notes

### 7. Pattern Role (Optional)

If this problem serves as a base template for a pattern:

```toml
# ===== Pattern Role =====
[pattern_role]
is_base_template = true                    # Whether this is a base template
base_for_kernel = "SubstringSlidingWindow" # API kernel this problem demonstrates
derived_problems = ["0076", "0159"]        # Problems derived from this template
```

**Fields:**
- `is_base_template`: Boolean indicating if this is a canonical template
- `base_for_kernel`: API kernel ID this problem demonstrates
- `derived_problems`: Array of problem IDs that build upon this template

## Complete Example

See `0003_longest_substring_without_repeating_characters.toml` for a complete example with all sections.

## Minimal Example

For a simple problem with one solution:

```toml
# Problem: Two Sum
# https://leetcode.com/problems/two-sum/

# ===== Problem Info =====
id = "0001"
slug = "0001_two_sum"
title = "Two Sum"
leetcode_id = 1
url = "https://leetcode.com/problems/two-sum/"

# ===== LeetCode Official Metadata =====
difficulty = "easy"
topics = ["array", "hash_table"]
companies = ["google", "amazon", "meta", "microsoft"]

# ===== Roadmaps =====
roadmaps = ["neetcode_150", "blind_75"]

# ===== Ontology Tags (Problem Level) =====
api_kernels      = []
patterns         = []
families         = ["two_sum_variants"]
data_structures  = ["array", "hash_map"]
algorithms       = []
related_problems = []

# ===== File Locations =====
[files]
solution  = "solutions/0001_two_sum.py"
generator = "generators/0001_two_sum.py"
tests_dir = "tests/0001_two_sum/"

# ===== Solutions =====
[[solutions]]
key    = "default"
class  = "Solution"
method = "twoSum"

api_kernels      = []
patterns         = []
families         = ["two_sum_variants"]
data_structures  = ["array", "hash_map"]
algorithms       = []
related_problems = []

role       = "base"
variant    = ""
based_on   = []
delta      = ""
complexity = "O(n) time, O(n) space"
notes      = "Single pass with hash map to find complement."
```

## Important Notes

### Solution File Linking

**The `[files].solution` field is critical for AI mind map generation:**

- ✅ **If set**: AI generates links to your GitHub solution
  - Example: `[LeetCode 11 - Container With Most Water](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)`

- ❌ **If empty or missing**: AI generates links to LeetCode problem page
  - Example: `[LeetCode 11 - Container With Most Water](https://leetcode.com/problems/container-with-most-water/)`

**Always set `solution` field if you have a solution file!**

### ID Format

- Problem IDs must be 4-digit zero-padded strings: `"0001"`, `"0023"`, `"0011"`
- Related problems use the same format: `["0159", "0340"]`

### Valid Values

Check these files for valid IDs:
- `ontology/topics.toml` - Valid topic IDs
- `ontology/companies.toml` - Valid company IDs
- `ontology/roadmaps.toml` - Valid roadmap IDs
- `ontology/api_kernels.toml` - Valid API kernel IDs
- `ontology/patterns.toml` - Valid pattern IDs
- `ontology/families.toml` - Valid family IDs
- `ontology/data_structures.toml` - Valid data structure IDs
- `ontology/algorithms.toml` - Valid algorithm IDs

## Usage

After creating or updating a problem TOML file:

1. **For AI Mind Maps**: The file is automatically loaded when generating mind maps
2. **For Pattern Documentation**: Referenced in pattern documentation generation
3. **For Test Runner**: Used to locate solution and generator files

## See Also

- [`meta/patterns/README.md`](../patterns/README.md) - Pattern source files documentation
- [`ontology/`](../../ontology/) - Ontology definitions (for valid IDs)
- [`tools/generate_mindmaps_ai.py`](../../tools/generate_mindmaps_ai.py) - AI mind map generator


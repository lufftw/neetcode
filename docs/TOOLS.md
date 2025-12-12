# Solution Tools

Tools for checking and validating solution files against the Pure Polymorphic Architecture standards.

## Quick Start

```bash
# Run format checker (quick check)
python tools/check_solutions.py

# Run format unit tests
python tools/run_format_tests.py

# Run full format check (checker + tests)
tools\run_format_tests.bat     # Windows
tools/run_format_tests.sh      # Linux/Mac

# Run ALL tests (format + component + correctness)
.dev\run_all_tests.bat         # Windows
.dev/run_all_tests.sh          # Linux/Mac
```

---

## Tools Overview

### `check_solutions.py`

Command-line tool to check all solution files for compliance. Provides a detailed report of issues grouped by type.

**Usage:**

```bash
python tools/check_solutions.py           # Standard check
python tools/check_solutions.py --verbose # Show suggestions
```

**Checks performed:**

1. **Architecture Compliance**
   - `SOLUTIONS` dictionary exists
   - `SOLUTIONS` contains `'class'` field
   - No wrapper functions (`solve_*`)
   - `solve()` uses `get_solver()`
   - Proper import: `from _runner import get_solver`

2. **Code Format**
   - Solution comments use "Solution 1:" format (not "Solution:" or "Solution -")
   - Solution comments are BEFORE class definitions (not inside)

3. **Complexity Comments**
   - Each solution has `# Time: O(...)` comment
   - Each solution has `# Space: O(...)` comment

**Output:**

- Summary statistics (total files, OK count, error count, warning count)
- Grouped issues by type (Architecture, Format, Complexity)
- Detailed error messages with file names and line numbers
- Suggestions for fixes (with `--verbose`)

### `run_format_tests.py`

Standalone script to run unit tests for format checking.

**Usage:**

```bash
python tools/run_format_tests.py           # Standard
python tools/run_format_tests.py --verbose # Verbose output
python tools/run_format_tests.py --quiet   # Quiet mode
```

### `run_format_tests.bat` / `run_format_tests.sh`

Shell scripts that run both the format checker and unit tests.

```bash
# Windows
tools\run_format_tests.bat

# Linux/Mac
tools/run_format_tests.sh
```

---

## Unit Tests

### `tools/tests/test_solution_format.py`

Comprehensive unit tests for solution file format validation. Tests are separated from:

- Component tests (`.dev/tests/`) - Runner module functionality
- Solution correctness tests (`.dev/tests_solutions/`) - Test case validation

**Test Methods:**

| Test | Description |
|------|-------------|
| `test_solution_comment_format` | Validates "Solution 1:" format |
| `test_complexity_comments` | Checks Time/Space complexity presence |
| `test_solutions_dictionary_exists` | Validates SOLUTIONS dictionary exists |
| `test_solutions_dictionary_structure` | Validates SOLUTIONS has 'class' field |
| `test_no_wrapper_functions` | Ensures no `solve_*` wrapper functions |
| `test_uses_get_solver` | Verifies `get_solver()` usage |
| `test_solution_comment_before_class` | Checks comment placement |
| `test_all_solution_classes_have_comments` | All Solution* classes have comments |

**Running Tests:**

```bash
# Via pytest
pytest tools/tests/test_solution_format.py -v

# Via unittest
python -m unittest tools.tests.test_solution_format

# Via standalone script
python tools/run_format_tests.py
```

---

## Architecture Requirements

All solution files must follow the Pure Polymorphic Architecture:

### 1. SOLUTIONS Dictionary (required)

```python
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",  # Required
        "method": "methodName",
        "complexity": "O(n) time, O(1) space",
        "description": "Solution description",
    },
    "alternative": {
        "class": "SolutionHashMap",
        "method": "methodName",
        "complexity": "O(n) time, O(n) space",
        "description": "Alternative approach",
    },
}
```

### 2. Solution Classes (polymorphic)

```python
class SolutionTwoPointers:
    def removeElement(self, nums: List[int], val: int) -> int:
        ...
```

### 3. Solution Comments (format)

```python
# ============================================
# Solution 1: Two Pointers
# Time: O(n), Space: O(1)
#   - Explanation of algorithm
#   - Key insights
# ============================================
class SolutionTwoPointers:
    ...
```

**Valid formats:**

- `# Solution 1: Two Pointers`
- `# Solution 2: Hash Map Approach`

**Invalid formats:**

- `# Solution: Two Pointers` (missing number)
- `# Solution - Two Pointers` (wrong separator)
- Inside class definition (wrong placement)

### 4. solve() Function

```python
from _runner import get_solver

def solve():
    solver = get_solver(SOLUTIONS)
    result = solver.methodName(...)
    return result
```

---

## Test Structure

The project has three separate test categories:

```
neetcode/
├── .dev/
│   ├── tests/                    # Component tests (runner modules)
│   │   ├── test_integration.py
│   │   ├── test_test_runner.py
│   │   └── ...
│   ├── tests_solutions/          # Solution correctness tests
│   │   └── test_all_solutions.py
│   ├── run_tests.bat/sh          # Run component tests only
│   ├── run_tests_solutions.bat/sh # Run correctness tests only
│   └── run_all_tests.bat/sh      # Run ALL tests
│
└── tools/
    ├── tests/                    # Format compliance tests
    │   └── test_solution_format.py
    ├── check_solutions.py        # Format checker tool
    ├── run_format_tests.py       # Format test runner
    └── run_format_tests.bat/sh   # Format test scripts
```

---

## Running All Tests

To run the complete test suite:

```bash
# Windows
.dev\run_all_tests.bat

# Linux/Mac
.dev/run_all_tests.sh
```

This runs:

1. **Solution Format Tests** - Architecture compliance
2. **Component Tests** - Runner module functionality
3. **Solution Correctness Tests** - Test case validation

---

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install pytest
      - run: python tools/check_solutions.py
      - run: pytest tools/tests/ -v
      - run: pytest .dev/tests/ -v
      - run: pytest .dev/tests_solutions/ -v
```

**Exit Codes:**

| Code | Meaning |
|------|---------|
| `0` | All checks/tests passed |
| `1` | Errors found / Tests failed |

---

## Common Issues and Fixes

### Missing Solution Comment

**Issue:**

```
0001_two_sum.py:30 - Class Solution missing Solution comment before definition
```

**Fix:** Add comment before class:

```python
# ============================================
# Solution 1: Hash Map
# Time: O(n), Space: O(n)
# ============================================
class Solution:
    ...
```

### Wrong Comment Format

**Issue:**

```
0001_two_sum.py:25 - Use 'Solution 1:' format (not 'Solution:')
```

**Fix:** Change `# Solution:` to `# Solution 1:`

### Missing Complexity

**Issue:**

```
0001_two_sum.py:25 - Missing Time and Space complexity
```

**Fix:** Add complexity comments:

```python
# Solution 1: Hash Map
# Time: O(n)
# Space: O(n)
```

### Comment Inside Class

**Issue:**

```
0001_two_sum.py:30 - Class Solution has Solution comment inside class
```

**Fix:** Move comment from inside class to before class definition.

---

## Related Documentation

- [Solution Contract](SOLUTION_CONTRACT.md) - Full solution file specification
- [Generator Contract](GENERATOR_CONTRACT.md) - Test generator specification
- [Architecture Migration](ARCHITECTURE_MIGRATION.md) - Migration guide to Pure Polymorphic Architecture

## Deprecated Tools

The following tools have been removed or consolidated:

- `auto_migrate.py` - Migration completed, no longer needed
- `batch_migrate_remaining.py` - Migration completed, no longer needed
- `check_migration.py` - Replaced by `check_solutions.py`
- `check_solution_format.py` - Merged into `check_solutions.py`

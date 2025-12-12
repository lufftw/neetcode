# Solution Format Checking Tools

This directory contains tools for validating solution files against the Pure Polymorphic Architecture standards.

## Tools Overview

### `check_solutions.py`
Command-line tool to check all solution files for compliance. Provides a detailed report of issues grouped by type.

**Usage:**
```bash
python tools/check_solutions.py
```

**Checks performed:**
1. **Architecture Compliance**
   - SOLUTIONS dictionary exists
   - SOLUTIONS contains 'class' field
   - No wrapper functions (`solve_*`)
   - `solve()` uses `get_solver()`
   - Proper import: `from _runner import get_solver`

2. **Code Format**
   - Solution comments use "Solution 1:" format (not "Solution:" or "Solution -")
   - Each solution has Time and Space complexity comments

**Output:**
- Summary statistics (total files, OK count, error count)
- Grouped issues by type (Architecture, Format, Complexity)
- Detailed error messages with file names and line numbers

### `run_format_tests.py`
Standalone script to run unit tests for format checking. Can be executed directly or via shell scripts.

**Usage:**
```bash
# Direct execution
python tools/run_format_tests.py

# With verbose output
python tools/run_format_tests.py --verbose

# Quiet mode
python tools/run_format_tests.py --quiet

# Using shell scripts (recommended)
# Windows
tools\run_format_tests.bat

# Linux/Mac
tools/run_format_tests.sh
```

**Test Coverage:**
- `test_solution_comment_format`: Validates comment format
- `test_complexity_comments`: Checks for Time/Space complexity
- `test_solutions_dictionary_structure`: Validates SOLUTIONS structure
- `test_no_wrapper_functions`: Ensures no wrapper functions exist
- `test_uses_get_solver`: Verifies get_solver() usage

## Unit Tests

### `tests/test_solution_format.py`
Comprehensive unit tests for solution file format validation. These tests can be run independently or as part of the test suite.

**Test Methods:**
1. `test_solution_comment_format()` - Validates Solution comment format
2. `test_complexity_comments()` - Checks Time/Space complexity presence
3. `test_solutions_dictionary_structure()` - Validates SOLUTIONS dictionary
4. `test_no_wrapper_functions()` - Ensures no wrapper functions
5. `test_uses_get_solver()` - Verifies get_solver() usage

**Running Tests:**
```bash
# Via pytest
pytest tools/tests/test_solution_format.py -v

# Via unittest
python -m unittest tools.tests.test_solution_format

# Via standalone script
python tools/run_format_tests.py
```

## Expected Format

### Solution Comment Format
```python
# Solution 1: Two Pointers
# Time: O(n)
# Space: O(1)
class Solution:
    ...
```

**Invalid formats:**
- `# Solution: Two Pointers` (missing number)
- `# Solution - Two Pointers` (wrong separator)

### SOLUTIONS Dictionary
```python
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "methodName",
        "complexity": "O(n) time, O(1) space",
        "description": "Solution description",
    },
}
```

### solve() Function
```python
from _runner import get_solver

def solve():
    solver = get_solver(SOLUTIONS)
    result = solver.methodName(...)
    return result
```

## Integration

These tools are designed to:
- Run in CI/CD pipelines
- Be executed manually during development
- Provide clear feedback for fixing issues
- Support both Windows and Unix-like systems

## Exit Codes

- `0`: All checks passed / All tests passed
- `1`: Errors found / Tests failed

This allows easy integration with build scripts and CI systems.


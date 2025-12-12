# Solution Tools

Tools for checking and validating solution files.

## Tools

### `check_solutions.py`

Main checker for solution file compliance with Pure Polymorphic Architecture.

**Checks:**

1. SOLUTIONS dictionary exists
2. SOLUTIONS contains 'class' field
3. No wrapper functions (solve_*)
4. solve() uses get_solver()
5. Imports _runner.get_solver
6. Solution comment format: "Solution 1:" not "Solution:" or "Solution -"
7. Solution classes have Time and Space complexity comments

**Usage:**

```bash
python tools/check_solutions.py
```

### `run_format_tests.py`

Standalone script to run format checking unit tests.

**Usage:**

```bash
# Direct execution
python tools/run_format_tests.py

# With verbose output
python tools/run_format_tests.py --verbose

# Using shell scripts (recommended)
# Windows
tools\run_format_tests.bat

# Linux/Mac
tools/run_format_tests.sh
```

## Tests

### `tests/test_solution_format.py`

Unit tests for solution file format:

- `test_solution_comment_format()` - Validates Solution comment format
- `test_complexity_comments()` - Checks Time/Space complexity presence
- `test_solutions_dictionary_structure()` - Validates SOLUTIONS structure
- `test_no_wrapper_functions()` - Ensures no wrapper functions exist
- `test_uses_get_solver()` - Verifies get_solver() usage

## Architecture Requirements

All solution files must follow the Pure Polymorphic Architecture:

### 1. SOLUTIONS Dictionary (required)

```python
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",
        "method": "removeElement",
        "complexity": "O(n) time, O(1) space",
        "description": "Reader/writer pointer pattern",
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
# Solution 1: Description
# Time: O(n), Space: O(1)
#   - Additional details
# ============================================
```

### 4. solve() Function

```python
def solve():
    solver = get_solver(SOLUTIONS)
    result = solver.methodName(args)
```

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


# Review Code Tools

> **Status**: Canonical Reference  
> **Scope**: Code review and validation tools in tools/review-code/  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

Code review and validation tools for the NeetCode Practice Framework.

## Overview

The review-code module provides tools for:
- Code format validation
- Solution file compliance checking
- Docstring auto-fixing
- Test format checking

## Module Structure

```
tools/review-code/
├── __init__.py
├── fix_docstring.py           # Auto-fix file-level docstrings
├── test_fetcher.py            # LeetCode data fetching
├── test_leetscrape.py         # Leetscrape testing
├── NAMING_ANALYSIS.md         # Naming convention analysis
├── README.md                  # Module documentation
│
└── validation/                # Validation tools
    ├── check_solutions.py     # Solution file checker
    ├── check_test_files.py    # Test file format checker
    ├── check_solution_contract.py  # Solution contract checker
    ├── run_format_tests.py    # Format test runner
    ├── run_format_tests.bat   # Windows batch script
    ├── run_format_tests.sh    # Unix shell script
    └── tests/                 # Validation tests
        └── test_solution_format.py
```

## Validation Tools

### `check_solutions.py`

Validates solution files for Pure Polymorphic Architecture compliance.

```bash
python tools/review-code/validation/check_solutions.py              # Standard check
python tools/review-code/validation/check_solutions.py --verbose    # Show fix suggestions
python tools/review-code/validation/check_solutions.py --list-warnings  # List warnings only
python tools/review-code/validation/check_solutions.py --show-warnings  # Show warnings with suggestions
```

**Checks Performed:**

| Category | What It Checks |
|----------|----------------|
| **Architecture** | `SOLUTIONS` dictionary exists with `class` field |
| | No wrapper functions (`solve_*`) |
| | `solve()` uses `get_solver()` |
| | Correct import: `from _runner import get_solver` |
| **Format** | Comments use `Solution 1:` format |
| | Comments placed BEFORE class definition |
| **Complexity** | Each solution has `# Time: O(...)` |
| | Each solution has `# Space: O(...)` |

### `check_test_files.py`

Checks and fixes double newline ending errors in test files.

```bash
python tools/review-code/validation/check_test_files.py              # List issues
python tools/review-code/validation/check_test_files.py --fix        # Auto-fix
python tools/review-code/validation/check_test_files.py --verbose    # Detailed info
```

### `run_format_tests.py`

Runs format compliance unit tests.

```bash
python tools/review-code/validation/run_format_tests.py           # Standard run
python tools/review-code/validation/run_format_tests.py --verbose # Verbose output
```

## Code Review Tools

### `fix_docstring.py`

Auto-fixes file-level docstrings by fetching data from LeetCode.

```bash
# Fix files in range
python tools/review-code/fix_docstring.py --range 77 142

# Fix single file
python tools/review-code/fix_docstring.py --range 202 202

# Custom delay
python tools/review-code/fix_docstring.py --range 77 142 --delay-min 3.0 --delay-max 8.0
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--range START END` | Required | Problem number range |
| `--delay-min` | 3.0 | Minimum delay between requests |
| `--delay-max` | 8.0 | Maximum delay between requests |

## Testing

```bash
# Run validation tests
python -m pytest tools/review-code/validation/tests -v

# Run format check
python tools/review-code/validation/check_solutions.py
```

## See Also

- [Main Tools README](../README.md) - Overview of all tools
- [Solution Contract](../../contracts/solution-contract.md) - Solution file specification
- [Testing Documentation](../../contributors/testing.md) - Testing guide (if exists)


# Solution Correctness Tests

This directory contains correctness tests for all **Solution files**.

## Test Categories

This project's tests are divided into three main categories:

| Category | Directory | Purpose |
|----------|-----------|---------|
| **Format Compliance Tests** | `tools/tests/` | Solution format standards |
| **Component Tests** | `.dev/tests/` | Runner module functionality |
| **Solution Correctness Tests** | `.dev/tests_solutions/` ← This directory | Solution execution results |

---

## Overview

`test_all_solutions.py` provides comprehensive test coverage for all Solution files.

**Note**: This is different from `.dev/tests/`:
- `.dev/tests/` tests **Runner system functionality** (whether the testing framework works properly)
- `.dev/tests_solutions/` tests **Solution execution results** (whether solutions are correct)

---

## Test Types

### 1. Static Tests (`test_static_tests`)

- Uses static test data from `tests/` directory
- Skips Solutions without test data
- Supports legacy and polymorphic modes

### 2. Generated Tests (`test_generated_tests`)

- Uses generators to produce test data
- **Requires**: Generator module (`generators/{problem}.py`) AND `JUDGE_FUNC`
- Auto-skips when generator or JUDGE_FUNC is missing
- Uses fixed seed (42) for reproducibility

### 3. Combined Tests (`test_combined_static_and_generated`)

- Uses both static and generated test data
- Provides best coverage when both are available

---

## How to Run Tests

### Quick Start (Recommended)

```bash
# Windows
.dev\run_tests_solutions.bat

# Linux/Mac
.dev/run_tests_solutions.sh
```

The script will automatically:
- Check virtual environment
- Check pytest installation
- Run all Solution tests
- Display clear success/failure messages

### Using pytest

```bash
# Run all Solution tests
python -m pytest .dev/tests_solutions -v

# Run specific test type
python -m pytest .dev/tests_solutions/test_all_solutions.py::TestAllSolutions::test_static_tests -v
python -m pytest .dev/tests_solutions/test_all_solutions.py::TestAllSolutions::test_generated_tests -v

# Test specific problem
python -m pytest .dev/tests_solutions -v -k "0023"
python -m pytest .dev/tests_solutions -v -k "0023 or 0027"
```

---

## Test Behavior

### Skip Conditions

Tests will automatically skip:
- Solution modules that cannot be loaded
- Problems without static test data (static tests)
- Problems without generators (generated tests)
- Problems without JUDGE_FUNC (required for generated tests)
- Problems without any available tests (combined tests)

### Failure Reporting

When tests fail, displays:
- Problem name and method (for multiple solutions)
- Test case name
- Expected vs actual output (truncated)
- For generated tests: input data that caused failure

---

## Example Output

```
test_static_tests[0023_merge_k_sorted_lists] PASSED
test_static_tests[0027_remove_element] FAILED
  AssertionError: 0027_remove_element (default): 2/3 static tests passed

test_generated_tests[0023_merge_k_sorted_lists] PASSED
test_generated_tests[0027_remove_element] FAILED
  Failed: 0027_remove_element (default): Generated case 3 failed
```

---

## Comparison with Other Tests

| Test Suite | Location | Purpose | Test Count |
|------------|----------|---------|------------|
| **Format Tests** | `tools/tests/` | Test Solution format standards | ~10 |
| **Component Tests** | `.dev/tests/` | Test Runner system functionality | ~273 |
| **Solution Tests** | `.dev/tests_solutions/` | Test Solution execution results | ~99 |

Run separately:
```bash
# Format tests
python -m pytest tools/tests -v

# Component tests
python -m pytest .dev/tests -v

# Solution tests
python -m pytest .dev/tests_solutions -v

# All tests
.dev\run_all_tests.bat  # Windows
.dev/run_all_tests.sh   # Linux/Mac
```

---

## Notes

- Generated tests use a small number of cases (5) to speed up CI
- Fixed seed (42) ensures failures are reproducible
- Supports both legacy and polymorphic Solution modes
- Multiple solution problems only test "default" method

---

## Related Links

- [../testing.md](../testing.md) - Complete testing documentation
- [../tests/README.md](../tests/README.md) - Component tests

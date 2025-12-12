# Solutions Test Suite

## Overview

This directory contains tests for **all solution files** in the `solutions/` directory.

**Note**: This is separate from `.dev/tests/` which tests the **runner system functionality**.
The runner tests verify that the testing framework works correctly, while these tests verify
that the actual solutions work correctly.

`test_all_solutions.py` provides comprehensive test coverage for all solution files.

## Test Types

### 1. Static Tests (`test_static_tests`)
- Tests all solutions with static test cases from `tests/` directory
- Skips solutions without static test files
- Supports both legacy and polymorphic solution patterns

### 2. Generated Tests (`test_generated_tests`)
- Tests solutions with generated test cases (if generator available)
- **Requires**: Generator module (`generators/{problem}.py`) AND `JUDGE_FUNC` in solution
- Skips gracefully if generator or JUDGE_FUNC missing
- Uses fixed seed (42) for reproducibility

### 3. Combined Tests (`test_combined_static_and_generated`)
- Tests solutions with both static and generated test cases
- Best coverage when both are available
- Skips if no tests available at all

## Usage

### Quick Start (Recommended)

**Windows:**
```batch
# Double-click or run from command prompt
.dev\run_tests_solutions.bat
```

**Linux/Mac:**
```bash
# First time: make script executable
chmod +x .dev/run_tests_solutions.sh

# Run the script
.dev/run_tests_solutions.sh
```

The batch files automatically:
- Check for virtual environment
- Check for pytest installation
- Run all solution tests with verbose output
- Show clear success/failure messages

### Run All Tests (Manual)
```bash
python -m pytest .dev/tests_solutions/ -v
```

### Run Specific Test Type
```bash
# Static tests only
python -m pytest .dev/tests_solutions/test_all_solutions.py::TestAllSolutions::test_static_tests -v

# Generated tests only
python -m pytest .dev/tests_solutions/test_all_solutions.py::TestAllSolutions::test_generated_tests -v

# Combined tests
python -m pytest .dev/tests_solutions/test_all_solutions.py::TestAllSolutions::test_combined_static_and_generated -v
```

### Run Tests for Specific Problem
```bash
# Test specific problem
python -m pytest .dev/tests_solutions/ -v -k "0023"

# Test multiple problems
python -m pytest .dev/tests_solutions/ -v -k "0023 or 0027"
```

### Run Tests for All Solutions (CI Mode)
```bash
# Quick check (static tests only, no generated)
python -m pytest .dev/tests_solutions/test_all_solutions.py::TestAllSolutions::test_static_tests -v --tb=short
```

## Separation from Runner Tests

| Test Suite | Location | Purpose | Test Count |
|-----------|----------|---------|------------|
| **Runner Tests** | `.dev/tests/` | Test the runner system functionality (test_runner, executor, etc.) | ~273 tests |
| **Solutions Tests** | `.dev/tests_solutions/` | Test all solution files work correctly | ~99 tests |

Run them separately:
```bash
# Test runner system
# Windows: .dev\run_tests.bat
# Linux/Mac: .dev/run_tests.sh
python -m pytest .dev/tests/ -v

# Test all solutions
# Windows: .dev\run_tests_solutions.bat
# Linux/Mac: .dev/run_tests_solutions.sh
python -m pytest .dev/tests_solutions/ -v

# Test both
python -m pytest .dev/tests/ .dev/tests_solutions/ -v
```

## Test Behavior

### Skipping Logic

Tests automatically skip when:
- Solution module cannot be loaded
- No static test files found (for static tests)
- No generator found (for generated tests)
- No JUDGE_FUNC (for generated tests - required for validation)
- No tests available at all (for combined tests)

### Failure Reporting

When a test fails, it shows:
- Problem name and method (if multi-solution)
- Test case name
- Expected vs actual output (truncated)
- For generated tests: input data that caused failure

## Example Output

```
test_static_tests[0023_merge_k_sorted_lists] PASSED
test_static_tests[0027_remove_element] FAILED
  AssertionError: 0027_remove_element (default): 2/3 static tests passed

test_generated_tests[0023_merge_k_sorted_lists] PASSED
test_generated_tests[0027_remove_element] FAILED
  Failed: 0027_remove_element (default): Generated case 3 failed
```

## Notes

- Generated tests use a small number of cases (5 for `test_generated_tests`, 3 for combined) for CI speed
- Fixed seed (42) ensures reproducible failures
- Tests support both legacy solutions (no SOLUTIONS dict) and polymorphic solutions
- Multi-solution problems test the "default" method only in these tests

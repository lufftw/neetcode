# Testing Documentation - NeetCode Practice Framework

> **Status**: Informational  
> **Scope**: Testing documentation and test files in `.dev/`  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

## Overview

This project has established a comprehensive test suite, divided into **three main categories**:

| Category | Directory | Purpose | Test Count |
|----------|-----------|---------|------------|
| **1. Component Tests** | `.dev/tests/` | Test Runner module functionality | ~273 |
| **2. Solution Correctness Tests** | `.dev/tests_solutions/` | Test Solution execution results | ~99 |
| **3. Format Compliance Tests** | `tools/review-code/validation/tests/` | Test Solution format standards | ~10 |

## Test Lead

**luffdev** - Unit Test Lead

## Core Objective

> Use tests to lock down "behavior", helping to ensure refactoring doesn't break things

---

## Quick Start

### Install Dependencies

```bash
python -m pip install pytest pytest-cov
```

### Run All Tests (Recommended)

```bash
# Windows
.dev\run_all_tests.bat

# Linux/Mac
.dev/run_all_tests.sh
```

### Run Tests Separately

```bash
# 1. Format Compliance Tests
tools\review-code\validation\run_format_tests.bat      # Windows
tools/review-code/validation/run_format_tests.sh       # Linux/Mac

# 2. Component Tests
.dev\run_tests.bat              # Windows
.dev/run_tests.sh               # Linux/Mac

# 3. Solution Correctness Tests
.dev\run_tests_solutions.bat    # Windows
.dev/run_tests_solutions.sh     # Linux/Mac
```

---

## Test Categories Explained

### 1. Format Compliance Tests (Solution Format Tests)

**Location**: `tools/review-code/validation/tests/`

Tests whether Solution files comply with Pure Polymorphic Architecture standards.

#### Test Items

| Test | Description |
|------|-------------|
| `test_solution_comment_format` | Solution comments use "Solution 1:" format |
| `test_complexity_comments` | Has Time/Space complexity comments |
| `test_solutions_dictionary_exists` | SOLUTIONS dictionary exists |
| `test_solutions_dictionary_structure` | SOLUTIONS has 'class' field |
| `test_no_wrapper_functions` | No solve_* wrapper functions |
| `test_uses_get_solver` | Uses get_solver() pattern |
| `test_solution_comment_before_class` | Comments are before class |
| `test_all_solution_classes_have_comments` | All Solution classes have comments |

#### How to Run

```bash
# Quick check
python tools/review-code/validation/check_solutions.py
python tools/review-code/validation/check_solutions.py --verbose  # Show fix suggestions

# Unit tests
python -m pytest tools/review-code/validation/tests/test_solution_format.py -v
```

---

### 2. Component Tests

**Location**: `.dev/tests/`

Tests the core functionality of the Runner system, ensuring refactoring doesn't break existing behavior.

#### Test Files

| File | Test Target | Test Count |
|------|-------------|------------|
| `test_util.py` | runner/util.py | 40+ |
| `test_case_runner.py` | runner/case_runner.py | 15+ |
| `test_test_runner.py` | runner/test_runner.py | 30+ |
| `test_complexity_estimator.py` | runner/complexity_estimator.py | 25+ |
| `test_edge_cases.py` | Edge cases | 40+ |
| `test_integration.py` | Integration tests | 20+ |
| `test_generate_mindmaps.py` | tools/mindmaps/generate_mindmaps.py | 50+ |
| `test_generate_pattern_docs.py` | tools/pattern-docs/generate_pattern_docs.py | 50+ |

#### Test Coverage

##### runner/util.py
- ✅ `normalize_output()` - Output normalization
- ✅ `compare_outputs()` - Three comparison modes (exact/sorted/set)
- ✅ `compare_result()` - JUDGE_FUNC support
- ✅ Path helper functions
- ✅ File operation functions

##### runner/case_runner.py
- ✅ Command line argument parsing and validation
- ✅ File existence checking
- ✅ Single test case execution flow

##### runner/test_runner.py
- ✅ `load_solution_module()` - Solution module loading
- ✅ `load_generator_module()` - Generator module loading
- ✅ `run_one_case()` - Single case execution
- ✅ Multiple solution support (SOLUTIONS metadata)
- ✅ Comparison modes (exact/sorted/set)
- ✅ JUDGE_FUNC support

##### runner/complexity_estimator.py
- ✅ Availability checking
- ✅ Complexity estimation
- ✅ Mock stdin mechanism
- ✅ Result formatting

#### How to Run

```bash
# All component tests
python -m pytest .dev/tests -v

# Run by marker
python -m pytest .dev/tests -v -m unit
python -m pytest .dev/tests -v -m integration
python -m pytest .dev/tests -v -m edge_case

# Specific file
python -m pytest .dev/tests/test_util.py -v
```

---

### 3. Solution Correctness Tests

**Location**: `.dev/tests_solutions/`

Tests the execution results of all Solution files.

#### Test Types

| Test | Description |
|------|-------------|
| `test_static_tests` | Uses static test data from tests/ directory |
| `test_generated_tests` | Uses generator to produce test data (requires JUDGE_FUNC) |
| `test_combined_static_and_generated` | Combines both |

#### Skip Conditions

Tests will automatically skip:
- Solution modules that cannot be loaded
- Problems without static test data
- Problems without generators
- Problems without JUDGE_FUNC (required for generated tests)

#### How to Run

```bash
# All Solution tests
python -m pytest .dev/tests_solutions -v

# Specific problem
python -m pytest .dev/tests_solutions -v -k "0023"

# Static tests only
python -m pytest .dev/tests_solutions/test_all_solutions.py::TestAllSolutions::test_static_tests -v
```

---

## Testing Principles

### 1. Behavior First
Test "what it does" not "how it does it". Refactoring can change implementation, but cannot change behavior.

### 2. Input/Output Verification
Given the same input, must get the same output.

### 3. Edge Case Coverage
Test extreme situations: empty input, min/max values, invalid formats, large data, special characters.

### 4. Independence
Each test runs independently, not depending on execution order or state of other tests.

### 5. Reproducibility
Test results must be deterministic, unaffected by time, environment, or other factors.

---

## Test Markers

```python
@pytest.mark.unit          # Unit tests
@pytest.mark.integration   # Integration tests
@pytest.mark.edge_case     # Edge case tests
@pytest.mark.slow          # Slow tests
@pytest.mark.requires_big_o # Requires big-O package
```

---

## Test Directory Structure

```
neetcode/
├── .dev/
│   ├── tests/                          # Component tests
│   │   ├── test_util.py
│   │   ├── test_case_runner.py
│   │   ├── test_test_runner.py
│   │   ├── test_complexity_estimator.py
│   │   ├── test_edge_cases.py
│   │   ├── test_integration.py
│   │   ├── test_generate_mindmaps.py
│   │   ├── test_generate_pattern_docs.py
│   │   └── README.md
│   │
│   ├── tests_solutions/                # Solution correctness tests
│   │   ├── test_all_solutions.py
│   │   └── README.md
│   │
│   ├── run_tests.bat/sh                # Component test scripts
│   ├── run_tests_solutions.bat/sh      # Solution test scripts
│   ├── run_all_tests.bat/sh            # ★ Full project test scripts
│   │
│   ├── testing.md                      # This file
│   ├── virtual-env-setup.md
│   └── README.md
│
└── tools/
    └── review-code/
        └── validation/                     # Format compliance tests
            ├── tests/
            │   └── test_solution_format.py
            ├── check_solutions.py          # Format checking tool
            ├── run_format_tests.py
            └── run_format_tests.bat/sh     # Format test scripts
```

---

## Scripts Overview

| Script | Purpose | Location |
|--------|---------|----------|
| `run_all_tests.bat/sh` | ★ Run all three test categories | `.dev/` |
| `run_tests.bat/sh` | Run component tests | `.dev/` |
| `run_tests_solutions.bat/sh` | Run solution correctness tests | `.dev/` |
| `run_format_tests.bat/sh` | Run format compliance tests | `tools/review-code/validation/` |

---

## Development Workflow

### Adding New Features

1. Write tests first (TDD)
2. Implement feature
3. Run tests to ensure passing
4. Commit code

### Fixing Bugs

1. Write test to reproduce bug
2. Fix bug
3. Ensure tests pass
4. Commit code

### Refactoring Code

1. Ensure all existing tests pass
2. Perform refactoring
3. Run tests again
4. If tests fail, fix code or update tests
5. Commit code

### Adding New Solutions

1. Ensure compliance with format standards (run `python tools/review-code/validation/check_solutions.py`)
2. Add test cases to `tests/` directory
3. Run `python -m pytest .dev/tests_solutions -v -k "problem_number"`
4. Commit code

---

## CI/CD Integration

### GitHub Actions Example

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
      
      - name: Install dependencies
        run: pip install pytest pytest-cov
      
      - name: Format Tests
        run: |
          python tools/review-code/validation/check_solutions.py
          pytest tools/review-code/validation/tests/ -v
      
      - name: Component Tests
        run: pytest .dev/tests/ -v
      
      - name: Solution Tests
        run: pytest .dev/tests_solutions/ -v
```

---

## Command Reference

```bash
# === Full Project Tests ===
.dev\run_all_tests.bat                          # Windows
.dev/run_all_tests.sh                           # Linux/Mac

# === Format Tests ===
python tools/review-code/validation/check_solutions.py                 # Quick check
python tools/review-code/validation/check_solutions.py --verbose       # Show suggestions
python -m pytest tools/review-code/validation/tests -v                 # Unit tests

# === Component Tests ===
python -m pytest .dev/tests -v                  # All
python -m pytest .dev/tests -v -m unit          # Unit tests
python -m pytest .dev/tests -v -m integration   # Integration tests
python -m pytest .dev/tests -v -m edge_case     # Edge case tests

# === Solution Tests ===
python -m pytest .dev/tests_solutions -v        # All
python -m pytest .dev/tests_solutions -v -k "0023"  # Specific problem

# === Coverage ===
python -m pytest .dev/tests --cov=runner --cov-report=html

# === Other Options ===
python -m pytest ... -x                         # Stop on first failure
python -m pytest ... --lf                       # Run only failed tests
python -m pytest ... --tb=short                 # Short error messages
```

---

## Contact Information

**Test Lead**: luffdev  
**Created**: 2025-12-08  
**Last Updated**: 2025-12-12

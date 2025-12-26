# Component Tests

This directory contains **characterization tests** for the NeetCode **Runner system**.

## Test Categories

This project's tests are divided into three main categories:

| Category | Directory | Purpose |
|----------|-----------|---------|
| **Format Compliance Tests** | `tools/tests/` | Solution format standards |
| **Component Tests** | `.dev/tests/` ← This directory | Runner module functionality |
| **Solution Correctness Tests** | `.dev/tests_solutions/` | Solution execution results |

---

## Purpose

The main purposes of these tests are:

1. **Lock down existing behavior** - Ensure refactoring doesn't change existing functionality
2. **Edge case validation** - Test empty input, invalid input, large data, and other edge cases
3. **Integration testing** - Verify that components work correctly together
4. **Regression testing** - Prevent future changes from breaking existing functionality

---

## Test Structure

```
.dev/tests/
├── __init__.py
│
│   # === Runner System Tests ===
├── test_util.py                     # util.py tests (40+ tests)
├── test_case_runner.py              # case_runner.py tests (15+ tests)
├── test_test_runner.py              # test_runner.py tests (30+ tests)
├── test_complexity_estimator.py     # complexity_estimator.py tests (25+ tests)
├── test_edge_cases.py               # Edge case tests (40+ tests)
├── test_integration.py              # Integration tests (20+ tests)
│
│   # === Tool Tests ===
├── test_generate_mindmaps.py        # generate_mindmaps.py tests (50+ tests)
├── test_generate_pattern_docs.py    # generate_pattern_docs.py tests (50+ tests)
│
└── README.md                        # This file
```

---

## How to Run Tests

### Quick Start

```bash
# Windows
.dev\run_tests.bat

# Linux/Mac
.dev/run_tests.sh
```

### Using pytest

```bash
# Run all component tests
python -m pytest .dev/tests -v

# Run by marker
python -m pytest .dev/tests -v -m unit
python -m pytest .dev/tests -v -m integration
python -m pytest .dev/tests -v -m edge_case

# Run specific file
python -m pytest .dev/tests/test_util.py -v

# Run specific test class
python -m pytest .dev/tests/test_util.py::TestNormalizeOutput -v

# Generate coverage report
python -m pytest .dev/tests --cov=runner --cov-report=html
```

---

## Test Coverage

### runner/util.py

- ✅ `normalize_output()` - Output normalization
- ✅ `compare_outputs()` - Three comparison modes (exact/sorted/set)
- ✅ `compare_result()` - JUDGE_FUNC support
- ✅ `_compare_sorted()` - Sorted comparison
- ✅ `_compare_set()` - Set comparison
- ✅ Path helper functions
- ✅ File operation functions

### runner/case_runner.py

- ✅ Command line argument handling
- ✅ File path validation
- ✅ Single test case execution
- ✅ Error handling

### runner/test_runner.py

- ✅ Module loading (solution/generator)
- ✅ Test case execution
- ✅ Multiple solution support
- ✅ Comparison modes (exact/sorted/set)
- ✅ JUDGE_FUNC support
- ✅ Failed case saving

### runner/complexity_estimator.py

- ✅ Availability checking
- ✅ Complexity estimation
- ✅ Mock stdin mechanism
- ✅ Result formatting

### Edge Case Tests

- ✅ Empty input
- ✅ Invalid input
- ✅ Large data
- ✅ Special characters (Unicode, emoji, CJK)
- ✅ Malformed data

### Integration Tests

- ✅ End-to-end workflow
- ✅ Multiple solution integration
- ✅ Comparison mode integration
- ✅ JUDGE_FUNC integration

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

## Testing Principles

1. **Behavior testing first** - Test "what it does" not "how it does it"
2. **Input/output verification** - Given the same input, ensure the same output
3. **Edge case coverage** - Test extreme cases and error handling
4. **Independence** - Each test should run independently
5. **Reproducibility** - Test results should be deterministic

---

## Refactoring Guide

When refactoring the Runner system:

1. **Run all tests first** - Ensure all tests pass in current state
2. **Perform refactoring** - Modify implementation details
3. **Run tests again** - Ensure behavior hasn't changed
4. **If tests fail**:
   - If behavior change is expected, update tests
   - If it's unexpected breakage, fix code

---

## Known Limitations

- Some tests require the `big-O` package (marked with `@pytest.mark.requires_big_o`)
- Integration tests create temporary files and directories
- Some tests may have subtle differences across operating systems

---

## Related Links

- [../testing.md](../testing.md) - Complete testing documentation
- [../tests_solutions/README.md](../tests_solutions/README.md) - Solution correctness tests

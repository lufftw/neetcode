# Developer & Maintainer Area

> ⚠️ **Note**: This folder is for project maintainers only, containing unit tests, development documentation, and maintenance tools.  
> For general users, please refer to the root [README.md](../README.md)

---

## 📁 Folder Structure

```
.dev/
├── tests/                          # Component tests (Runner modules)
│   ├── test_util.py                # util.py tests (40+ tests)
│   ├── test_case_runner.py         # case_runner.py tests (15+ tests)
│   ├── test_test_runner.py         # test_runner.py tests (30+ tests)
│   ├── test_complexity_estimator.py # complexity_estimator.py tests (25+ tests)
│   ├── test_edge_cases.py          # Edge case tests (40+ tests)
│   ├── test_integration.py         # Integration tests (20+ tests)
│   ├── test_generate_mindmaps.py   # mindmap generator tests (50+ tests)
│   ├── test_generate_pattern_docs.py # pattern doc generator tests (50+ tests)
│   └── README.md
│
├── tests_solutions/                # Solution correctness tests
│   ├── test_all_solutions.py       # All Solution tests (~99 tests)
│   └── README.md
│
├── run_tests.bat                   # Windows - Component tests
├── run_tests.sh                    # Linux/Mac - Component tests
├── run_tests_solutions.bat         # Windows - Solution tests
├── run_tests_solutions.sh          # Linux/Mac - Solution tests
├── run_all_tests.bat               # ★ Windows - Full project tests
├── run_all_tests.sh                # ★ Linux/Mac - Full project tests
│
├── TESTING.md                      # Complete testing documentation
├── VIRTUAL_ENV_SETUP.md            # Virtual environment setup guide
└── README.md                       # This file
```

---

## 🎯 Test Categories

This project's tests are divided into **three main categories**:

| Category | Directory | Purpose | Count |
|----------|-----------|---------|-------|
| **Format Compliance Tests** | `tools/tests/` | Solution format standards | ~10 |
| **Component Tests** | `.dev/tests/` | Runner module functionality | ~273 |
| **Solution Correctness Tests** | `.dev/tests_solutions/` | Solution execution results | ~99 |

---

## 🚀 Quick Start

### 1. Ensure Virtual Environment is Set Up

```bash
# Windows
python -m venv leetcode
leetcode\Scripts\activate

# Linux/Mac
python -m venv leetcode
source leetcode/bin/activate
```

### 2. Install Test Dependencies

```bash
pip install pytest pytest-cov
```

### 3. Run All Tests (Recommended)

```bash
# Windows
.dev\run_all_tests.bat

# Linux/Mac
.dev/run_all_tests.sh
```

This will execute in order:
1. ✅ Solution format compliance tests
2. ✅ Runner component tests
3. ✅ Solution correctness tests

### 4. Run Tests Separately

```bash
# === Format Compliance Tests ===
# Windows
tools\run_format_tests.bat
# Linux/Mac
tools/run_format_tests.sh

# === Component Tests ===
# Windows
.dev\run_tests.bat
# Linux/Mac
.dev/run_tests.sh

# === Solution Correctness Tests ===
# Windows
.dev\run_tests_solutions.bat
# Linux/Mac
.dev/run_tests_solutions.sh
```

---

## 📊 Test Statistics

| Item | Count |
|------|-------|
| Test Files | 10 |
| Test Classes | 70+ |
| Test Cases | 380+ |
| Code Coverage | 80-100% |

### Test Coverage

- ✅ `runner/util.py` - 100% coverage
- ✅ `runner/case_runner.py` - 90% coverage
- ✅ `runner/test_runner.py` - 85% coverage
- ✅ `runner/complexity_estimator.py` - 80% coverage
- ✅ `solutions/*.py` - Format compliance validation

---

## 📚 Documentation Index

### Core Documentation

| Document | Description |
|----------|-------------|
| [TESTING.md](TESTING.md) | Complete testing documentation (strategy, principles, workflow) |
| [VIRTUAL_ENV_SETUP.md](VIRTUAL_ENV_SETUP.md) | Virtual environment setup guide |
| [tests/README.md](tests/README.md) | Component tests detailed description |
| [tests_solutions/README.md](tests_solutions/README.md) | Solution tests detailed description |
| [../tools/FORMAT_CHECKING.md](../tools/FORMAT_CHECKING.md) | Format checking tools description |

---

## 🔧 Development Workflow

### Adding New Solutions

1. Ensure compliance with format standards
   ```bash
   python tools/check_solutions.py --verbose
   ```
2. Add test cases to `tests/` directory
3. Run tests to verify
   ```bash
   python -m pytest .dev/tests_solutions -v -k "problem_number"
   ```
4. Commit code

### Modifying Runner Modules

1. Run existing tests to ensure they pass
2. Make modifications
3. Run tests again
   ```bash
   python -m pytest .dev/tests -v
   ```
4. Commit code

### Refactoring Code

1. Run all tests to establish baseline
   ```bash
   .dev\run_all_tests.bat
   ```
2. Perform refactoring
3. Run all tests again to ensure consistent behavior
4. Commit code

---

## 📈 Test Command Reference

```bash
# === Full Project Tests ===
.dev\run_all_tests.bat                    # Windows
.dev/run_all_tests.sh                     # Linux/Mac

# === Format Tests ===
python tools/check_solutions.py           # Quick check
python tools/check_solutions.py --verbose # Show suggestions
python -m pytest tools/tests -v           # Unit tests

# === Component Tests ===
python -m pytest .dev/tests -v            # All
python -m pytest .dev/tests -v -m unit    # By marker

# === Solution Tests ===
python -m pytest .dev/tests_solutions -v  # All
python -m pytest .dev/tests_solutions -v -k "0023"  # Specific problem

# === Coverage Report ===
python -m pytest .dev/tests --cov=runner --cov-report=html
```

---

## 🎓 Testing Principles

1. **Behavior Testing First** - Test "what it does" not "how it does it"
2. **Independence** - Each test runs independently, not relying on other tests
3. **Reproducibility** - Test results are deterministic
4. **Clarity** - Tests are easy to understand and maintain
5. **Completeness** - Cover normal cases and edge cases

---

## 📞 Contact Information

**Test Lead**: luffdev  
**Created**: 2025-12-08  
**Last Updated**: 2025-12-12

---

## 🔗 Related Links

- [Project Main README](../README.md) - Project overview
- [Root pytest.ini](../pytest.ini) - pytest configuration file
- [requirements.txt](../requirements.txt) - Project dependencies
- [tools/FORMAT_CHECKING.md](../tools/FORMAT_CHECKING.md) - Format checking description

---

**Note**: This folder's contents are for maintainers only; general users need not be concerned.

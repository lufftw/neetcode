# Developer & Maintainer Area

> **Status**: Informational  
> **Scope**: `.dev/` directory  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

> ⚠️ **Note**: This folder is for project maintainers only, containing unit tests, development documentation, and maintenance tools.  
> For general users, please refer to the root [README.md](../README.md)

---

## 📁 Quick Overview

This directory contains:
- **Component Tests** (`.dev/tests/`) - Runner module functionality tests (~273 tests)
- **Solution Correctness Tests** (`.dev/tests_solutions/`) - Solution execution tests (~99 tests)
- **Test Scripts** - Helper scripts to run tests (`.bat` for Windows, `.sh` for Linux/Mac)

---

## 🚀 Quick Start

### Run All Tests

```bash
# Windows
.dev\run_all_tests.bat

# Linux/Mac
.dev/run_all_tests.sh
```

### Run Tests Separately

```bash
# Component tests
python -m pytest .dev/tests -v

# Solution tests
python -m pytest .dev/tests_solutions -v
```

---

## 📚 Full Documentation

For complete documentation, please see:

- **[Contributors Overview](../docs/contributors/README.md)** - Complete maintainer guide
- **[Testing Documentation](../docs/contributors/TESTING.md)** - Comprehensive testing guide
- **[Documentation Architecture](../docs/contributors/DOCUMENTATION_ARCHITECTURE.md)** - Documentation structure
- **[Virtual Environment Setup](../docs/contributors/VIRTUAL_ENV_SETUP.md)** - Environment setup guide

---

**Note**: This folder's contents are for maintainers only; general users need not be concerned.

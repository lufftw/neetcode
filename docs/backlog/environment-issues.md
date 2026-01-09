# Environment Issues

> **Status**: Backlog
> **Last Updated**: 2025-01-09
> **Total Items**: 1 issue

This document tracks known environment setup issues and their workarounds.

---

## Active Issues

### 1. `leetcode_datasource` Module Not Found

**Symptom**:
```
ModuleNotFoundError: No module named 'leetcode_datasource'
```

**Impact**:
- 11 unit tests in `.dev/tests/test_leetcode_datasource_validation.py` fail
- `test_generate_mindmaps.py` cannot be collected

**Affected Tests**:
```
FAILED test_leetcode_datasource_validation.py::TestLeetCodeDataSource*
```

**Cause**:
The `leetcode_datasource` package in `src/` is not installed in editable mode.

**Workaround**:
```bash
# Install local packages in editable mode
pip install -e src/leetcode_datasource
```

**Proper Fix**:
Add to `requirements.txt` or setup instructions:
```
-e src/leetcode_datasource
-e src/codegen
-e src/practice_workspace
```

**Status**: Not blocking solution development or testing. Only affects internal tooling tests.

---

## Resolved Issues

*None yet*

---

## Related

- [Virtual Environment Setup](../contributors/virtual-env-setup.md)
- [Testing Guide](../contributors/testing.md)

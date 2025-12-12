# Migration Guide: Pure Polymorphic Architecture

## Migration Steps

For each file that needs migration, follow these steps:

### 1. Add Import Statement

Add at the top of the file:
```python
from _runner import get_solver
```

### 2. Update SOLUTIONS Dictionary

#### Case A: File Missing SOLUTIONS Dictionary

Add SOLUTIONS dictionary (before the first Solution class):

```python
# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",  # Class name
        "method": "methodName",  # LeetCode method name
        "complexity": "O(n) time, O(1) space",
        "description": "Solution description",
    },
}
```

#### Case B: SOLUTIONS Dictionary Missing "class" Field

Update each entry to add the "class" field, and change "method" from wrapper function name to the actual LeetCode method name:

**Before:**
```python
SOLUTIONS = {
    "default": {
        "method": "solve_two_pointers",  # wrapper function
        ...
    },
}
```

**After:**
```python
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",  # Class name
        "method": "removeDuplicates",  # LeetCode method name
        ...
    },
}
```

### 3. Remove Wrapper Functions

Delete all `solve_*` wrapper functions:

```python
# Delete these functions
def solve_two_pointers(...):
    """Wrapper for SolutionTwoPointers."""
    return SolutionTwoPointers().methodName(...)
```

### 4. Update solve() Function

**Before:**
```python
def solve():
    ...
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    method_info = SOLUTIONS.get(method_name, SOLUTIONS['default'])
    method_func_name = method_info['method']
    method_func = globals()[method_func_name]
    result = method_func(...)
```

**After:**
```python
def solve():
    ...
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.methodName(...)  # Use actual LeetCode method name
```

### 5. Remove Unused Imports

If `os.environ` is no longer used, remove:
```python
import os  # Remove if no longer needed
```

## Migration Checklist

- [ ] Add `from _runner import get_solver`
- [ ] SOLUTIONS dictionary contains "class" field
- [ ] SOLUTIONS dictionary "method" field uses LeetCode method name (not wrapper function name)
- [ ] Remove all wrapper functions (`solve_*`)
- [ ] solve() function uses `get_solver(SOLUTIONS)`
- [ ] Remove unused `import os` (if no longer needed)

## Example: Complete Migration

### Before Migration

```python
from typing import List
import os

SOLUTIONS = {
    "default": {
        "method": "solve_two_pointers",
        "complexity": "O(n) time, O(1) space",
    },
}

class SolutionTwoPointers:
    def removeDuplicates(self, nums: List[int]) -> int:
        ...

def solve_two_pointers(nums: List[int]) -> int:
    return SolutionTwoPointers().removeDuplicates(nums)

def solve():
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    method_info = SOLUTIONS.get(method_name, SOLUTIONS['default'])
    method_func_name = method_info['method']
    method_func = globals()[method_func_name]
    result = method_func(nums)
```

### After Migration

```python
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",
        "method": "removeDuplicates",
        "complexity": "O(n) time, O(1) space",
    },
}

class SolutionTwoPointers:
    def removeDuplicates(self, nums: List[int]) -> int:
        ...

def solve():
    solver = get_solver(SOLUTIONS)
    result = solver.removeDuplicates(nums)
```

## Checking Migration Status

Run `python tools/check_solutions.py` to see which files need migration.

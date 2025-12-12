# Architecture Migration: Polymorphic Solution Pattern

## Overview

This document describes the migration from wrapper-based and single-class patterns to a unified **Pure Polymorphic Architecture** for all solution files.

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| `SOLUTIONS` dictionary | **Required** | Explicit metadata over auto-detection |
| Wrapper functions | **Deprecated** | Redundant indirection layer |
| Single-class multiple methods | **Deprecated** | Unclear semantics for AI analysis |
| Auto-detection of classes | **Not supported** | Too many edge cases, hard to debug |

---

## Current State (Before Migration)

### Pattern 1: Wrapper Functions
Used in: `0025_reverse_nodes_in_k_group.py`, `0027_remove_element.py`

```python
SOLUTIONS = {
    "default": {"method": "solve_two_pointers", ...},
    "two_ends": {"method": "solve_two_ends", ...},
}

class SolutionTwoPointers:
    def removeElement(self, nums, val): ...

class SolutionTwoEnds:
    def removeElement(self, nums, val): ...

# Wrapper functions (redundant layer)
def solve_two_pointers(nums, val):
    return SolutionTwoPointers().removeElement(nums, val)

def solve_two_ends(nums, val):
    return SolutionTwoEnds().removeElement(nums, val)

def solve():
    method_func = globals()[method_func_name]  # Calls wrapper
    result = method_func(nums, val)
```

### Pattern 2: Single-Class Multiple Methods
Used in: `0023_merge_k_sorted_lists.py`

```python
SOLUTIONS = {
    "default": {"method": "mergeKListsPriorityQueue", ...},
    "divide": {"method": "mergeKListsDivideAndConquer", ...},
}

class Solution:
    def mergeKListsPriorityQueue(self, lists): ...
    def mergeKListsDivideAndConquer(self, lists): ...

def solve():
    sol = Solution()
    method_func = getattr(sol, method_func_name)  # Same instance
    result = method_func(lists)
```

---

## Target State (After Migration)

### Pure Polymorphic Pattern

All solutions use **multiple classes implementing the same method name**.

```python
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",   # Required: class name
        "method": "removeElement",         # Required: LeetCode method name
        "complexity": "O(n) time, O(1) space",
        "description": "Reader/writer pointer pattern",
    },
    "two_ends": {
        "class": "SolutionTwoEnds",
        "method": "removeElement",         # Same method name (polymorphism)
        "complexity": "O(n) time, O(1) space",
        "description": "Opposite pointers approach",
    },
}

class SolutionTwoPointers:
    def removeElement(self, nums: List[int], val: int) -> int:
        ...

class SolutionTwoEnds:
    def removeElement(self, nums: List[int], val: int) -> int:
        ...

# No wrapper functions

def solve():
    nums = [...]
    val = ...
    
    # Clean polymorphic invocation (like LeetCode style)
    solver = get_solver(SOLUTIONS)
    k = solver.removeElement(nums, val)
    
    print(k)
```

---

## Runtime Helper: `get_solver()`

### Why `get_solver()` Instead of Direct Dispatch?

| Pattern | Code | Readability |
|---------|------|-------------|
| ❌ Direct dispatch | `getattr(globals()[info['class']](), info['method'])(nums, val)` | Poor |
| ❌ `invoke_solution` | `invoke_solution(SOLUTIONS, globals(), nums, val)` | Medium |
| ✅ `get_solver` | `solver.removeElement(nums, val)` | **Excellent** |

The `get_solver()` pattern:
1. Returns the correct class instance based on `SOLUTION_METHOD` env var
2. User calls method naturally (like LeetCode)
3. No need to pass `globals()` (uses `inspect` internally)

### Usage

```python
from _runner import get_solver

def solve():
    # Parse input
    nums = list(map(int, input().split()))
    val = int(input())
    
    # Get solver instance (auto-selects based on SOLUTION_METHOD)
    solver = get_solver(SOLUTIONS)
    
    # Call method naturally - exactly like LeetCode!
    k = solver.removeElement(nums, val)
    
    print(k)
```

### Implementation

Located in `solutions/_runner.py`:

```python
import inspect
import os

def get_solver(solutions_meta):
    """
    Get the solver instance for the currently selected solution method.
    
    Returns:
        An instance of the selected solution class.
    
    Example:
        solver = get_solver(SOLUTIONS)
        result = solver.twoSum(nums, target)  # Natural method call
    """
    # Auto-capture caller's globals (no need to pass explicitly)
    caller_globals = inspect.currentframe().f_back.f_globals
    
    method_key = os.environ.get('SOLUTION_METHOD', 'default')
    info = solutions_meta.get(method_key, solutions_meta['default'])
    
    return caller_globals[info['class']]()
```

### Benefits

1. **LeetCode-style calls** - `solver.methodName(args)` is natural
2. **No `globals()` pollution** - Framework handles it via `inspect`
3. **IDE autocomplete works** - After `solver = get_solver(...)`, IDE can suggest methods
4. **Explicit method call** - User sees which method is being called

---

## Deprecated Patterns

| Pattern | Status | Reason |
|---------|--------|--------|
| No `SOLUTIONS` dictionary | **DEPRECATED** | Explicit metadata required |
| Wrapper functions | **DEPRECATED** | Redundant indirection layer |
| One class with multiple differently-named methods | **DEPRECATED** | Unclear semantics for AI analysis |
| `globals()[method_name]` for wrappers | **DEPRECATED** | Use `class` + `method` fields |
| `SOLUTIONS` without `class` field | **DEPRECATED** | Must specify class explicitly |
| `invoke_solution(SOLUTIONS, globals(), ...)` | **DEPRECATED** | Poor readability, use `get_solver()` |

### Clarification: Single Solution Problems

A problem with only **one solution class** is perfectly valid:

```python
# ✅ Valid: Single solution problem
SOLUTIONS = {
    "default": {"class": "Solution", "method": "twoSum", ...},
}

class Solution:
    def twoSum(self, nums, target): ...
```

What's deprecated is **one class containing multiple differently-named methods**:

```python
# ❌ Deprecated: Multiple methods in one class
class Solution:
    def mergeKListsPriorityQueue(self, lists): ...   # Method A
    def mergeKListsDivideAndConquer(self, lists): ... # Method B (different name)
```

The correct pattern for multiple solutions is **polymorphism** (multiple classes, same method name).

---

## SOLUTIONS Format Specification

### Why SOLUTIONS is Required (Not Auto-Detected)

We explicitly require a `SOLUTIONS` dictionary instead of auto-detecting solution classes. Rationale:

| Concern | Why Auto-Detection Fails |
|---------|-------------------------|
| **Helper classes** | `SolutionHelper`, `SolutionBase` would be misidentified as solutions |
| **Method detection** | Which method is the main entry point? `twoSum`? `solve`? |
| **Complexity info** | Where does `O(n)` come from? Docstrings? Decorators? |
| **Inheritance** | Should base classes count as solutions? |
| **Debugging** | Users can't tell which classes were detected |
| **Testing** | Mocking becomes complex with reflection |

**Explicit is better than implicit.** The `SOLUTIONS` dictionary provides:
- Clear metadata (complexity, description)
- Predictable behavior
- Easy validation
- AI-friendly structured data

### Required Fields

```python
SOLUTIONS = {
    "key": {
        "class": str,        # Required: Class name (e.g., "SolutionHeap")
        "method": str,       # Required: Method name (LeetCode original)
        "complexity": str,   # Recommended: Time/space complexity
        "description": str,  # Recommended: Brief description
    },
}
```

### Rules

1. **`SOLUTIONS` dictionary is required** - Every solution file must define it
2. **`default` key is required** - Used when no `SOLUTION_METHOD` is specified
3. **`class` field is required** - No fallback to wrapper functions
4. **`method` field is required** - Must be the LeetCode original method name
5. **All classes must implement the same method name** - Polymorphism requirement
6. **Class names should reflect the algorithm** - e.g., `SolutionHeap`, `SolutionTwoPointers`

### Minimal Example (Single Solution)

```python
# For problems with only one solution approach
SOLUTIONS = {
    "default": {"class": "Solution", "method": "twoSum"},
}

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        ...
```

---

## Test Runner Behavior

### `--all` Flag

The `--all` flag runs all solutions defined in `SOLUTIONS`:

| Scenario | Solutions Count | `--all` Behavior |
|----------|-----------------|------------------|
| Single solution problem | 1 | Runs 1 solution (normal) |
| Multiple solutions (polymorphic) | N | Runs N solutions (benchmark) |
| Missing `SOLUTIONS` | - | ❌ Validation error |
| Missing `class` field | - | ❌ Validation error |

**Note**: A problem with only one solution is perfectly valid. The `SOLUTIONS` dictionary is still required, even for single-solution problems.

### Validation Logic

```python
def validate_solutions_meta(solutions_meta: dict) -> bool:
    """Validate SOLUTIONS format. SOLUTIONS is required."""
    if not solutions_meta:
        print("❌ SOLUTIONS dictionary is required")
        print("   Example:")
        print("   SOLUTIONS = {")
        print('       "default": {"class": "Solution", "method": "twoSum"},')
        print("   }")
        return False
    
    if 'default' not in solutions_meta:
        print("❌ SOLUTIONS must have 'default' key")
        return False
    
    for key, info in solutions_meta.items():
        if 'class' not in info:
            print(f"❌ SOLUTIONS['{key}'] missing 'class' field")
            return False
        if 'method' not in info:
            print(f"❌ SOLUTIONS['{key}'] missing 'method' field")
            return False
    
    return True
```

---

## Migration Steps

### Phase 1: Update Runner Infrastructure

1. Update `runner/executor.py` - Remove wrapper function support
2. Update `runner/test_runner.py` - Add polymorphic mode validation
3. Update `runner/module_loader.py` - Validate `class` field presence
4. Add unit tests for new invocation pattern

### Phase 2: Migrate Example Solutions

1. `0027_remove_element.py` - Reference implementation
2. `0025_reverse_nodes_in_k_group.py` - Remove wrapper functions
3. `0023_merge_k_sorted_lists.py` - Split into multiple classes

### Phase 3: Migrate All Solutions

1. Identify all solutions with wrapper functions
2. Identify all solutions with single-class pattern
3. Migrate each solution to polymorphic pattern
4. Remove deprecated wrapper functions

### Phase 4: Update Templates and Documentation

1. Update `template_solution_multi.py`
2. Update pattern documentation
3. Update README files

---

## Example Migration

### Before (0023_merge_k_sorted_lists.py)

```python
class Solution:
    def mergeKListsPriorityQueue(self, lists): ...
    def mergeKListsDivideAndConquer(self, lists): ...
    def mergeKListsGreedy(self, lists): ...

SOLUTIONS = {
    "default": {"method": "mergeKListsPriorityQueue", ...},
    "divide": {"method": "mergeKListsDivideAndConquer", ...},
    "greedy": {"method": "mergeKListsGreedy", ...},
}
```

### After

```python
class SolutionHeap:
    def mergeKLists(self, lists): ...

class SolutionDivideConquer:
    def mergeKLists(self, lists): ...

class SolutionGreedy:
    def mergeKLists(self, lists): ...

SOLUTIONS = {
    "default": {"class": "SolutionHeap", "method": "mergeKLists", ...},
    "divide": {"class": "SolutionDivideConquer", "method": "mergeKLists", ...},
    "greedy": {"class": "SolutionGreedy", "method": "mergeKLists", ...},
}
```

---

## Benefits

1. **Cleaner architecture** - No wrapper function indirection
2. **Clear semantics** - Class name conveys algorithm intent
3. **AI-friendly** - Each class is an independent, analyzable unit
4. **Consistent with TOML** - Python `SOLUTIONS` aligns with TOML metadata
5. **Fair benchmarking** - `--all` compares independent class instances
6. **Reduced bugs** - Single invocation pattern, no fallback chains

---

## Timeline

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Runner infrastructure | ✅ Completed |
| Phase 2 | Example migrations | ✅ Completed |
| Phase 3 | Full migration | Pending (scan remaining solutions) |
| Phase 4 | Documentation & Templates | ✅ Completed |

### Completed Items

- **Phase 1**: Added `validate_solutions_meta()` to `runner/module_loader.py`
- **Phase 2**: Migrated example solutions:
  - `0027_remove_element.py` - Polymorphic pattern with `SolutionTwoPointers`, `SolutionTwoEnds`
  - `0025_reverse_nodes_in_k_group.py` - Polymorphic pattern with `SolutionIterative`, `SolutionRecursive`
  - `0023_merge_k_sorted_lists.py` - Split into `SolutionHeap`, `SolutionDivideConquer`, `SolutionGreedy`
- **Phase 4**: 
  - Updated test fixtures in `.dev/tests/` to use polymorphic format
  - Updated `template_solution.py` to use `SOLUTIONS` + `get_solver()`
  - Updated `template_solution_multi.py` to use polymorphic pattern
  - Deleted deprecated `template_solution_wrapper.py`
  - Updated `scripts/new_problem.bat` and `scripts/new_problem.sh` (removed `--wrapper` option)
  - Updated `scripts/run_tests.bat` to pass all arguments
  - Created `docs/SOLUTION_CONTRACT.md` as canonical specification


# Solution Contract Specification

> **Status**: Canonical Reference  
> **Scope**: All solution files in `solutions/`  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

This document defines the **contract** for solution files in this repository. All solution files MUST conform to this specification. The test runner, generators, and tooling depend on this contract.

---

## A. Solution File Structure

### A.1 File Naming Convention

```
solutions/{problem_id}_{slug}.py
```

| Component | Format | Example |
|-----------|--------|---------|
| `problem_id` | 4-digit zero-padded LeetCode ID | `0001`, `0023`, `0994` |
| `slug` | snake_case problem name | `two_sum`, `merge_k_sorted_lists` |

**Examples:**
- `solutions/0001_two_sum.py`
- `solutions/0023_merge_k_sorted_lists.py`
- `solutions/0051_n_queens.py`

### A.2 Required Elements

Every solution file MUST contain:

| Element | Required | Description |
|---------|----------|-------------|
| `SOLUTIONS` dict | ✅ | Metadata for all solution variants |
| Solution class(es) | ✅ | One or more classes implementing the solution |
| `solve()` function | ✅ | Entry point for stdin/stdout execution |
| `_runner` import | ✅ | For polymorphic dispatch |

### A.3 Minimal Solution File

```python
# solutions/0001_two_sum.py
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "twoSum",
        "complexity": "O(n) time, O(n) space",
        "description": "Single pass with hash map",
    },
}

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []

def solve():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    nums = list(map(int, lines[0].split(',')))
    target = int(lines[1])
    
    solver = get_solver(SOLUTIONS)
    result = solver.twoSum(nums, target)
    print(result)

if __name__ == "__main__":
    solve()
```

### A.4 Multi-Solution File (Polymorphic Pattern)

When a problem has multiple solution approaches, use **separate classes with the same method name**:

```python
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionHeap",
        "method": "mergeKLists",
        "complexity": "O(N log k)",
        "description": "Min-heap approach",
    },
    "divide": {
        "class": "SolutionDivideConquer",
        "method": "mergeKLists",
        "complexity": "O(N log k)",
        "description": "Divide and conquer",
    },
    "greedy": {
        "class": "SolutionGreedy",
        "method": "mergeKLists",
        "complexity": "O(N * k)",
        "description": "Sequential merge",
    },
}

class SolutionHeap:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        ...

class SolutionDivideConquer:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        ...

class SolutionGreedy:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        ...

def solve():
    # ... parse input ...
    solver = get_solver(SOLUTIONS)
    result = solver.mergeKLists(lists)
    print(result)
```

**Key Polymorphism Rule**: All solution classes MUST implement the **same method name** (the LeetCode original method name). The runner selects the class via `SOLUTION_METHOD` environment variable.

### A.5 Runner Method Selection

The test runner selects solutions via the `SOLUTION_METHOD` environment variable:

```bash
# Run default solution
python runner/test_runner.py 0023

# Run specific solution
python runner/test_runner.py 0023 --method divide

# Run all solutions
python runner/test_runner.py 0023 --all
```

The `solve()` function uses `get_solver()` to dispatch:

```python
from _runner import get_solver

def solve():
    solver = get_solver(SOLUTIONS)  # Returns correct class instance
    result = solver.methodName(args)  # Natural LeetCode-style call
```

### A.6 Deprecated Patterns

The following patterns are **DEPRECATED** and should not be used in new code:

| Pattern | Status | Migration |
|---------|--------|-----------|
| No `SOLUTIONS` dictionary | ❌ DEPRECATED | Add `SOLUTIONS` with `class` + `method` |
| Wrapper functions | ❌ DEPRECATED | Use polymorphic classes directly |
| Single class with multiple methods | ❌ DEPRECATED | Split into separate classes |
| `SOLUTIONS` without `class` field | ❌ DEPRECATED | Add `class` field to each entry |
| `invoke_solution()` helper | ❌ DEPRECATED | Use `get_solver()` instead |
| `globals()[method_name]` dispatch | ❌ DEPRECATED | Use `get_solver()` instead |

**Deprecated wrapper pattern (DO NOT USE):**
```python
# ❌ DEPRECATED
def solve_a(nums, val):
    return SolutionA().removeElement(nums, val)

SOLUTIONS = {
    "default": {"method": "solve_a", ...},  # Missing 'class' field
}
```

### A.7 Solution Comment Format

Solutions SHOULD include structured comments to explain the algorithm, approach, and key insights. This section defines the standard comment format.

#### A.7.1 File-Level Docstring

Every solution file SHOULD start with a docstring describing the problem:

```python
"""
Problem: Two Sum
Link: https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, return indices 
of the two numbers such that they add up to target.

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.
"""
```

| Field | Required | Description |
|-------|----------|-------------|
| `Problem` | ✅ | Problem title |
| `Link` | ✅ | LeetCode URL |
| Description | Recommended | Brief problem statement |
| `Constraints` | Recommended | Key constraints affecting algorithm choice |

#### A.7.2 Solution Block Comments

Each solution class SHOULD be preceded by a block comment explaining the approach.

**No blank line** between the comment block and the class definition:

```python
# ============================================================================
# Solution 1: Sliding Window (Optimized with Jump)
# Time: O(n), Space: O(min(n, σ))
#   - Each character visited at most twice
#   - Uses last-seen-index array for O(1) duplicate detection
#   - Direct position jumping instead of incremental contraction
# ============================================================================
class SolutionSlidingWindow:   # ← 緊接著，無空行
    ...
```

**Format:**

```
# ============================================
# Solution {N}: {Approach Name}
# Time: O(?), Space: O(?)
#   - {Key insight or implementation detail}
#   - {Additional notes}
# ============================================
class ClassName:   # ← No blank line before class/function
```

| Component | Required | Description |
|-----------|----------|-------------|
| Solution number & name | ✅ | e.g., `Solution 1: Sliding Window` |
| Time/Space complexity | ✅ | e.g., `Time: O(n), Space: O(n)` |
| Bullet points | Recommended | Key insights, implementation details |
| **No blank line** | ✅ | Comment block directly followed by class/function |

**More examples:**

```python
# ============================================
# Solution 1: Single Pass
# Time: O(max(m,n)), Space: O(max(m,n))
#   - Single pass through both lists
#   - Result list has at most max(m,n) + 1 nodes
# ============================================
class Solution:
    ...
```

```python
# ============================================================================
# Solution 2: Using Dictionary (More Flexible for Unicode)
# Time: O(n), Space: O(min(n, σ))
#   - Same sliding window approach with dictionary instead of array
#   - More flexible for Unicode strings but slightly slower
# ============================================================================
class SolutionDict:
    ...
```

```python
# ============================================================================
# Solution 3: Using Set (Standard While-Loop Pattern)
# Time: O(n), Space: O(min(n, σ))
#   - Uses set to track current window characters
#   - Demonstrates standard while-loop contraction pattern
# ============================================================================
class SolutionSet:
    ...
```

#### A.7.3 JUDGE_FUNC Comments (Optional)

When defining a `JUDGE_FUNC`, you MAY include a block comment explaining its purpose and complexity.

Same rule: **no blank line** between comment and function:

```python
# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
# Uses brute force O(m+n) merge to compute the correct answer,
# then compares with the solution output.
# ============================================
def judge(actual, expected, input_data: str) -> bool:   # ← 無空行
    ...

JUDGE_FUNC = judge
```

This is optional but recommended when:
- The judge uses a different algorithm than the solution
- The judge has notable complexity characteristics
- Generator support requires custom validation

---

## B. SOLUTIONS Metadata Schema

### B.1 Required Schema

```python
SOLUTIONS = {
    "key": {
        "class": str,        # REQUIRED: Class name
        "method": str,       # REQUIRED: Method name (LeetCode original)
        "complexity": str,   # RECOMMENDED: Time/space complexity
        "description": str,  # RECOMMENDED: Brief description
    },
}
```

### B.2 Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `class` | `str` | ✅ | Python class name that implements the solution |
| `method` | `str` | ✅ | Method name to invoke (must match LeetCode signature) |
| `complexity` | `str` | Recommended | Time and/or space complexity (e.g., `"O(n) time, O(1) space"`) |
| `description` | `str` | Recommended | Brief description of the approach |

### B.3 Required Keys

- **`"default"`** key is REQUIRED. This is used when no `--method` flag is specified.
- Additional keys are optional and represent alternative solution approaches.

### B.4 Validation Rules

The runner validates `SOLUTIONS` at load time:

1. `SOLUTIONS` dictionary MUST exist
2. `"default"` key MUST be present
3. Each entry MUST have `"class"` field
4. Each entry MUST have `"method"` field
5. The class specified in `"class"` MUST exist in the module
6. The method specified in `"method"` MUST exist on the class

**Validation error example:**
```
❌ [0023] Invalid SOLUTIONS format:
   - SOLUTIONS['heap'] missing 'class' field
   
   Expected format:
   SOLUTIONS = {
       "default": {"class": "Solution", "method": "twoSum", ...},
   }
```

### B.5 Complete Example

```python
SOLUTIONS = {
    "default": {
        "class": "SolutionBacktrackSets",
        "method": "solveNQueens",
        "complexity": "O(N!) time, O(N) space",
        "description": "Backtracking with hash sets for O(1) conflict detection",
    },
    "sets": {
        "class": "SolutionBacktrackSets",
        "method": "solveNQueens",
        "complexity": "O(N!) time, O(N) space",
        "description": "Backtracking with hash sets for O(1) conflict detection",
    },
    "bitmask": {
        "class": "SolutionBacktrackBitmask",
        "method": "solveNQueens",
        "complexity": "O(N!) time, O(N) space",
        "description": "Backtracking with bitmask for ultra-fast conflict detection",
    },
}
```

### B.6 Optional Extended Fields

For integration with the ontology system, these optional fields may be included:

| Field | Type | Description |
|-------|------|-------------|
| `api_kernels` | `list[str]` | API Kernels used (e.g., `["SubstringSlidingWindow"]`) |
| `patterns` | `list[str]` | Patterns applied (e.g., `["sliding_window_unique"]`) |
| `families` | `list[str]` | Problem families (e.g., `["substring_search"]`) |
| `data_structures` | `list[str]` | Data structures used (e.g., `["hash_map", "deque"]`) |
| `algorithms` | `list[str]` | Algorithms/techniques (e.g., `["two_pointers"]`) |
| `tags` | `list[str]` | Custom tags for categorization |

---

## C. Judge / Validation Contract

### C.1 Validation Priority Order

The runner validates solution output in this priority order:

| Priority | Mode | Trigger | Description |
|----------|------|---------|-------------|
| 1 | `JUDGE_FUNC` | `JUDGE_FUNC` defined in module | Custom validation function |
| 2 | `COMPARE_MODE` | `COMPARE_MODE` defined in module | Framework-provided comparators |
| 3 | Exact | Default | String equality comparison |

### C.2 JUDGE_FUNC Specification

#### Definition

```python
JUDGE_FUNC = judge  # Module-level assignment
```

#### Signature

```python
def judge(actual, expected, input_data: str) -> bool:
    """
    Custom validation function.
    
    Args:
        actual: Program output (parsed if possible, else raw string)
        expected: Expected output (parsed if possible, else raw string, or None)
        input_data: Raw input string
    
    Returns:
        bool: True if answer is correct, False otherwise
    """
```

#### Argument Parsing Rules

| Argument | Parsing Behavior |
|----------|------------------|
| `actual` | Parsed via `ast.literal_eval()` if valid Python literal; otherwise raw string |
| `expected` | Parsed via `ast.literal_eval()` if valid Python literal; otherwise raw string; `None` if `.out` file missing |
| `input_data` | Always raw string (no parsing) |

#### Return Types

| Return Value | Meaning |
|--------------|---------|
| `True` | Test passed |
| `False` | Test failed |

#### Judge-Only Mode

When `.out` file is missing:
- `expected` is `None`
- `JUDGE_FUNC` MUST validate using only `actual` and `input_data`
- This enables validation without precomputed expected outputs

**Example (N-Queens with judge-only support):**

```python
def judge(actual: list, expected, input_data: str) -> bool:
    """Validate N-Queens solution."""
    n = int(input_data.strip())
    
    # Known solution counts for N-Queens
    KNOWN_COUNTS = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352}
    
    # 1. Verify each board is valid
    for board in actual:
        if not _is_valid_board(board, n):
            return False
    
    # 2. Check no duplicates
    unique = set(tuple(row for row in board) for board in actual)
    if len(unique) != len(actual):
        return False
    
    # 3. Check count
    if expected is not None:
        return len(actual) == len(expected)
    else:
        # Judge-only: use known counts
        expected_count = KNOWN_COUNTS.get(n)
        if expected_count is not None:
            return len(actual) == expected_count
        return True  # Accept if count unknown

JUDGE_FUNC = judge
```

### C.3 COMPARE_MODE Specification

#### Definition

```python
COMPARE_MODE = "sorted"  # Module-level assignment
```

#### Supported Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `"exact"` | String equality after normalization | Default; exact answer required |
| `"sorted"` | Sort lists before comparison | "Return in any order" problems |
| `"set"` | Set comparison (ignores order and duplicates) | Unique elements, order doesn't matter |

#### Normalization

Before comparison, outputs are normalized:
1. Strip leading/trailing whitespace
2. Remove trailing whitespace from each line
3. Normalize line endings

#### Sorted Mode Details

For nested lists (e.g., `List[List[str]]`):
- Convert inner lists to tuples
- Sort outer list
- Compare sorted results

```python
# Example: N-Queens output
actual   = [[".Q..", "...Q"], ["..Q.", "Q..."]]
expected = [["..Q.", "Q..."], [".Q..", "...Q"]]
# After sorting: both become the same → PASS
```

### C.4 Validation Mode Reporting

The runner reports validation mode for each test case:

```
0051_n_queens_1: ✅ PASS [judge]
0051_n_queens_2: ✅ PASS [judge-only]
0001_two_sum_1: ✅ PASS [exact]
0015_3sum_1: ✅ PASS [sorted]
```

| Label | Meaning |
|-------|---------|
| `[judge]` | `JUDGE_FUNC` used with `.out` file present |
| `[judge-only]` | `JUDGE_FUNC` used without `.out` file |
| `[exact]` | Exact string comparison |
| `[sorted]` | Sorted comparison |
| `[set]` | Set comparison |
| `[skip]` | Skipped (no `.out` and no `JUDGE_FUNC`) |

---

## D. Test Files Contract

### D.1 Directory Conventions

```
neetcode/
├── tests/                          # Static test cases
│   ├── {problem_id}_{slug}_{n}.in  # Input file
│   └── {problem_id}_{slug}_{n}.out # Expected output file (optional if JUDGE_FUNC)
│
├── generators/                     # Dynamic test generators
│   └── {problem_id}_{slug}.py      # Generator module
```

### D.2 Static Test Files

#### Naming Convention

```
tests/{problem_id}_{slug}_{case_number}.{in|out}
```

**Examples:**
- `tests/0001_two_sum_1.in`
- `tests/0001_two_sum_1.out`
- `tests/0051_n_queens_2.in`
- `tests/0051_n_queens_2.out`

#### Input File Format (`.in`)

- Plain text, parsed by `solve()` function
- Format is problem-specific
- Line endings: LF or CRLF (both accepted)

**Example (`0001_two_sum_1.in`):**
```
2,7,11,15
9
```

#### Output File Format (`.out`)

- Plain text matching `print()` output from `solve()`
- MUST match exactly (after normalization) unless `COMPARE_MODE` or `JUDGE_FUNC` specified

**Example (`0001_two_sum_1.out`):**
```
[0, 1]
```

#### Optional `.out` Files

`.out` files are optional when:
- `JUDGE_FUNC` is defined (judge-only mode)

### D.3 Generator Requirements

> 📖 **Full Specification**: See [`GENERATOR_CONTRACT.md`](GENERATOR_CONTRACT.md) for complete generator documentation.

#### Overview

Generators enable dynamic test case generation for stress testing and edge case discovery.

| Requirement | Description |
|-------------|-------------|
| File location | `generators/{problem_id}_{slug}.py` |
| Required function | `generate(count: int, seed: Optional[int]) -> Iterator[str]` |
| JUDGE_FUNC | Solutions using generators MUST define `JUDGE_FUNC` |

#### Key Rules

1. Generator output MUST match `.in` file format
2. Same `seed` MUST produce identical output (reproducibility)
3. Edge cases should be yielded before random cases

### D.4 Running Tests

#### Static Tests

```bash
python runner/test_runner.py 0001_two_sum
```

#### With Generated Tests

> 📖 **Full CLI Reference**: See [`GENERATOR_CONTRACT.md`](GENERATOR_CONTRACT.md#g-running-generated-tests) for all generator options.

```bash
# Static + N generated tests
python runner/test_runner.py 0001_two_sum --generate 10

# Reproducible with seed
python runner/test_runner.py 0001_two_sum --generate 10 --seed 12345
```

---

## E. Required Metadata Layers

### E.1 Metadata Hierarchy

| Layer | Location | Scope | Change Frequency |
|-------|----------|-------|------------------|
| **Solution-level** | `solutions/{problem}.py` | Per-solution variant | Often |
| **Problem-level** | `meta/problems/{problem}.toml` | Per-problem | Moderate |
| **Ontology-level** | `ontology/*.toml` | Global definitions | Rarely |

### E.2 Solution-Level Metadata (Required)

Located in the solution file itself:

```python
SOLUTIONS = {
    "default": {
        "class": "Solution",           # REQUIRED
        "method": "twoSum",            # REQUIRED
        "complexity": "O(n)",          # RECOMMENDED
        "description": "Hash map",     # RECOMMENDED
    },
}

# Optional validation
JUDGE_FUNC = judge        # Custom validation
COMPARE_MODE = "sorted"   # Comparison mode
```

### E.3 Problem-Level Metadata (Optional)

Located in `meta/problems/{problem_id}_{slug}.toml`:

```toml
[problem]
id = "0001"
title = "Two Sum"
difficulty = "easy"
url = "https://leetcode.com/problems/two-sum/"

topics = ["array", "hash_table"]
companies = ["google", "amazon", "facebook"]

[[solutions]]
key = "default"
class = "Solution"
method = "twoSum"
complexity = "O(n) time"
api_kernels = []
patterns = ["hash_lookup"]
```

### E.4 Ontology-Level Metadata

Located in `ontology/` directory:

| File | Content |
|------|---------|
| `api_kernels.toml` | Reusable algorithmic cores |
| `patterns.toml` | Problem-solving patterns |
| `families.toml` | Problem family definitions |
| `algorithms.toml` | Algorithm taxonomy |
| `data_structures.toml` | Data structure taxonomy |
| `topics.toml` | LeetCode topics |
| `difficulties.toml` | Difficulty levels |
| `companies.toml` | Company tags |
| `roadmaps.toml` | Learning path metadata |

### E.5 Consistency Checklist

When adding or modifying a solution, verify:

#### Solution File Consistency

- [ ] `SOLUTIONS` dictionary exists with `"default"` key
- [ ] Each entry has `"class"` and `"method"` fields
- [ ] Class names match actual classes in file
- [ ] Method names match actual methods on classes
- [ ] All solution classes implement the same method name

#### Test Consistency

- [ ] At least one `.in` file exists in `tests/`
- [ ] `.out` files exist OR `JUDGE_FUNC` is defined
- [ ] Input format in `.in` matches `solve()` parsing logic
- [ ] Output format in `.out` matches `print()` output

#### Generator Consistency (if applicable)

- [ ] Generator file exists in `generators/`
- [ ] `generate()` function yields correct format
- [ ] `JUDGE_FUNC` is defined in solution (required for generators)
- [ ] Edge cases are included in generator

#### Ontology Consistency (if applicable)

- [ ] Referenced `api_kernels` exist in `ontology/api_kernels.toml`
- [ ] Referenced `patterns` exist in `ontology/patterns.toml`
- [ ] Referenced `families` exist in `ontology/families.toml`
- [ ] Problem metadata in `meta/problems/` aligns with solution file

---

## Appendix: Quick Reference

### File Structure Template

```python
# solutions/{problem_id}_{slug}.py
"""
Problem: {Problem Title}
Link: https://leetcode.com/problems/{slug}/

{Brief problem description}

Constraints:
- {constraint 1}
- {constraint 2}
"""
from typing import List
from _runner import get_solver

# ============================================
# Optional: Custom validation
# ============================================
# JUDGE_FUNC = judge        # For "any order" or complex validation
# COMPARE_MODE = "sorted"   # For simple "any order" problems

# ============================================
# SOLUTIONS metadata (REQUIRED)
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "methodName",
        "complexity": "O(?)",
        "description": "Brief description",
    },
}

# ============================================
# Solution 1: {Approach Name}
# Time: O(?), Space: O(?)
#   - {Key insight or implementation detail}
#   - {Additional notes}
# ============================================
class Solution:   # ← No blank line after comment block
    def methodName(self, ...):
        ...

# ============================================
# Entry point
# ============================================
def solve():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    # Parse input...
    
    solver = get_solver(SOLUTIONS)
    result = solver.methodName(...)
    
    print(result)

if __name__ == "__main__":
    solve()
```

### CLI Reference

```bash
# Run tests
python runner/test_runner.py {problem}              # Default solution
python runner/test_runner.py {problem} --method X   # Specific solution
python runner/test_runner.py {problem} --all        # All solutions
python runner/test_runner.py {problem} --benchmark  # With timing

# Generator (see GENERATOR_CONTRACT.md for full options)
python runner/test_runner.py {problem} --generate N          # Static + N generated
python runner/test_runner.py {problem} --generate N --seed S # Reproducible
```

### Related Documentation

- [`GENERATOR_CONTRACT.md`](GENERATOR_CONTRACT.md) — Generator file specification
  - Full `generate()` function spec
  - Generator design patterns
  - Complexity estimation
  - Running generated tests CLI

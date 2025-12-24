# Generator Contract Specification

> **Status**: Canonical Reference  
> **Scope**: All generator files in `generators/`  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

This document defines the **contract** for test case generator files. Generators enable stress testing, edge case discovery, and reproducible test generation.

---

## Table of Contents

- [File Structure](#file-structure)
- [generate() Function](#generate-function)
- [Generator Design Patterns](#generator-design-patterns)
- [Complexity Estimation Generator](#complexity-estimation-generator)
- [Input Format Specifications](#input-format-specifications)
- [JUDGE_FUNC Requirement](#judge_func-requirement)
- [Running Generated Tests](#running-generated-tests)
- [Best Practices](#best-practices)
- [Quick Reference](#quick-reference)

---

## File Structure

### Naming Convention

```
generators/{problem_id}_{slug}.py
```

| Component | Format | Example |
|-----------|--------|---------|
| `problem_id` | 4-digit zero-padded LeetCode ID | `0001`, `0004`, `0051` |
| `slug` | snake_case problem name | `two_sum`, `median_of_two_sorted_arrays` |

**Examples:**
- `generators/0001_two_sum.py`
- `generators/0004_median_of_two_sorted_arrays.py`
- `generators/0051_n_queens.py`

### Required Elements

Every generator file MUST contain:

| Element | Required | Description |
|---------|----------|-------------|
| `generate()` function | ✅ | Main entry point for test generation |
| Docstring with constraints | ✅ | LeetCode constraints documentation |
| Edge cases | ✅ | Known edge cases yielded first |

### Optional Elements

| Element | Optional | Description |
|---------|----------|-------------|
| `generate_for_complexity()` | ⭕ | For time complexity estimation |
| Helper functions | ⭕ | Internal `_generate_case()` etc. |
| Custom generators | ⭕ | `generate_all_sizes()` etc. |

---

## generate() Function

### Function Signature

```python
def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input in the same format as .in files
    """
```

### Contract Rules

| Rule | Requirement | Rationale |
|------|-------------|-----------|
| **Yield format** | Must match `.in` file format | Runner passes to `solve()` via stdin |
| **Reproducibility** | Same seed → same output | Enables failure reproduction |
| **Edge cases first** | Yield known edge cases before random | Catch corner-case bugs early |
| **Constraint compliance** | Respect LeetCode constraints | Ensure valid test cases |
| **JUDGE_FUNC required** | Solution must have `JUDGE_FUNC` | No `.out` file for generated cases |

> 📖 See [JUDGE_FUNC Specification](SOLUTION_CONTRACT.md#judge_func-specification) for validation details.

### Minimal Example

```python
# generators/0001_two_sum.py
import random
from typing import Iterator, Optional

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate test cases for Two Sum."""
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        "2,7,11,15\n9",   # Classic example
        "3,2,4\n6",       # Answer not first element
        "3,3\n6",         # Duplicate values
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()

def _generate_case() -> str:
    size = random.randint(2, 5000)
    nums = [random.randint(-10**6, 10**6) for _ in range(size)]
    i, j = random.sample(range(size), 2)
    target = nums[i] + nums[j]
    return f"{','.join(map(str, nums))}\n{target}"
```

---

## Generator Design Patterns

### Standard Template

```python
# generators/{problem_id}_{slug}.py
"""
Test Case Generator for Problem {ID} - {Title}

LeetCode Constraints:
- {constraint_1}
- {constraint_2}
- ...

Time Complexity: O(?)
"""
import random
from typing import Iterator, Optional


# ============================================
# Random Test Generation (for functional testing)
# ============================================

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input in the same format as .in files
    """
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    edge_cases = [
        # Known important test cases
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single random test case."""
    # Implementation here
    pass


# ============================================
# Complexity Estimation (controlled size)
# ============================================

def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Target input size
    
    Returns:
        str: Test input with size approximately n
    """
    pass
```

### Edge Case Design

Edge cases should cover:

| Category | Examples |
|----------|----------|
| **Boundary values** | Min/max constraints, empty inputs |
| **Special cases** | Single element, all same values |
| **Negative cases** | Negative numbers, zero |
| **Classic examples** | LeetCode example inputs |

**Example (Median of Two Sorted Arrays):**

```python
edge_cases = [
    "[]\n[1]",                    # nums1 is empty
    "[1]\n[]",                    # nums2 is empty
    "[1,3]\n[2]",                 # Classic odd total length
    "[1,2]\n[3,4]",               # Classic even total length
    "[-5,-3,-1]\n[2,4,6]",        # Negative and positive
    "[1]\n[1]",                   # Same single element
]
```

### Guaranteed Valid Input

For problems requiring valid solutions exist, ensure generated inputs are solvable:

```python
def _generate_case(size: int) -> str:
    """
    Generate a Two Sum case with guaranteed solution.
    
    Strategy:
    1. Generate random array
    2. Pick two random indices
    3. Set target = nums[i] + nums[j]
    """
    nums = [random.randint(-10**6, 10**6) for _ in range(size)]
    i, j = random.sample(range(size), 2)
    target = nums[i] + nums[j]  # Guaranteed to have solution
    
    return f"{','.join(map(str, nums))}\n{target}"
```

### Weighted Random Distribution

For more thorough testing, weight towards challenging cases:

```python
def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    # ...
    
    for _ in range(count):
        # Weight towards larger n (more thorough testing)
        n = random.choices(
            population=range(1, 10),
            weights=[1, 1, 2, 3, 4, 5, 6, 7, 8],  # Higher weight for larger
            k=1
        )[0]
        yield str(n)
```

---

## Complexity Estimation Generator

### Function Signature

```python
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.
    
    Args:
        n: Target input size
    
    Returns:
        str: Test input with size approximately n
    """
```

### Purpose

The `--estimate` flag uses this function to:
1. Generate test cases of increasing sizes
2. Measure execution time for each size
3. Fit curve to estimate Big-O complexity

> 📖 See [Test Runner § Complexity Estimation](runner/README.md#complexity-estimation) for usage.

### Example

```python
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size.
    
    For Two Sum:
    - n is the length of nums array
    - Expected complexity: O(n) with hash map
    """
    n = max(2, n)  # Ensure minimum valid size
    return _generate_case(n)
```

### Size Semantics

Define what "n" means for your problem:

| Problem Type | n Meaning |
|--------------|-----------|
| Array problems | Array length |
| String problems | String length |
| Two-array problems | Total elements (m + n) |
| Matrix problems | Total cells (rows × cols) |
| Graph problems | Number of nodes or edges |

---

## Input Format Specifications

### Format Rules

| Rule | Requirement |
|------|-------------|
| Match `.in` format | Output must be parseable by `solve()` |
| No trailing spaces | Strip whitespace from each line |
| Consistent separators | Use `,` or `\n` consistently |
| No Python repr spaces | `[1,2,3]` not `[1, 2, 3]` |

### Common Formats

**Single array:**
```python
# Format: comma-separated values
"2,7,11,15"
```

**Array + target:**
```python
# Format: array on line 1, target on line 2
"2,7,11,15\n9"
```

**Two arrays:**
```python
# Format: Python list repr without spaces
"[1,3]\n[2]"
# Or: two comma-separated lines
"1,3\n2"
```

**Matrix (grid):**
```python
# Format: Python 2D list repr
"[[1,2,3],[4,5,6],[7,8,9]]"
```

**Single value:**
```python
# Format: just the value
"4"
```

### Removing Spaces from Lists

```python
# Wrong: has spaces
f"{nums1}\n{nums2}"  # -> "[1, 2, 3]\n[4, 5, 6]"

# Correct: no spaces
f"{nums1}\n{nums2}".replace(' ', '')  # -> "[1,2,3]\n[4,5,6]"
```

---

## JUDGE_FUNC Requirement

### Why JUDGE_FUNC is Required

Generated test cases have **no expected output** (`.out` file). The solution MUST validate correctness using `JUDGE_FUNC`:

```
Generator → Input only → Solution → Output → JUDGE_FUNC validates
```

> 📖 See [JUDGE_FUNC Specification](SOLUTION_CONTRACT.md#judge_func-specification) for complete documentation.

### Generator-Specific Considerations

When `JUDGE_FUNC` is used with generators (judge-only mode):

| Parameter | Value | Implication |
|-----------|-------|-------------|
| `actual` | Solution output | Parsed via `ast.literal_eval()` if valid |
| `expected` | `None` | No `.out` file exists |
| `input_data` | Raw input string | Use to validate correctness |

The `JUDGE_FUNC` MUST be able to validate using **only** `actual` and `input_data` when `expected` is `None`.

### Example Pattern

```python
def judge(actual, expected, input_data: str) -> bool:
    # Parse input to understand problem constraints
    n = int(input_data.strip())
    
    # Validate actual output against problem requirements
    if not _is_valid_output(actual, n):
        return False
    
    # For judge-only mode: use known answers or algorithmic validation
    if expected is None:
        return _validate_without_expected(actual, n)
    
    # For static tests: compare with expected
    return actual == expected

JUDGE_FUNC = judge
```

---

## Running Generated Tests

### Command Line Usage

```bash
# Static tests + N generated tests
python runner/test_runner.py {problem} --generate N

# Only generated tests (skip static tests)
python runner/test_runner.py {problem} --generate-only N

# Reproducible with seed
python runner/test_runner.py {problem} --generate N --seed 12345

# Save failing cases to tests/
python runner/test_runner.py {problem} --generate N --save-failed

# Complexity estimation
python runner/test_runner.py {problem} --estimate
```

> 📖 See [Test Runner Specification](runner/README.md) for full CLI reference.

### Output Format

```
============================================================
🧪 Test Results: 0001_two_sum
============================================================

📁 Static Tests:
0001_two_sum_1: ✅ PASS [judge]          0.12ms
0001_two_sum_2: ✅ PASS [judge]          0.08ms

🎲 Generated Tests (seed=12345):
gen_1: ✅ PASS [judge-only]              0.45ms
gen_2: ✅ PASS [judge-only]              0.52ms
gen_3: ❌ FAIL [judge-only]              0.38ms
   ┌─ Input ─────────────────────────────────
   │ 5,3,8,1,2
   │ 11
   └─────────────────────────────────────────

💡 To reproduce: python runner/test_runner.py 0001 --generate 3 --seed 12345
============================================================
```

### Failure Reproduction

When a generated test fails:

1. **Re-run with same seed:**
   ```bash
   python runner/test_runner.py 0001 --generate 10 --seed 12345
   ```

2. **Save failed case:**
   ```bash
   python runner/test_runner.py 0001 --generate 10 --save-failed
   # Creates: tests/0001_failed_1.in
   ```

3. **Debug specific case:**
   ```bash
   python runner/case_runner.py 0001 failed_1
   ```

---

## Best Practices

### Generator Checklist

- [ ] Docstring with LeetCode constraints
- [ ] `seed` parameter for reproducibility
- [ ] Edge cases yielded first
- [ ] Random cases respect constraints
- [ ] Input format matches `.in` files
- [ ] Solution has `JUDGE_FUNC` defined
- [ ] `generate_for_complexity()` if using `--estimate`

### Performance Considerations

| Consideration | Recommendation |
|---------------|----------------|
| Generation speed | Keep generators fast (< 1ms per case) |
| Constraint limits | Use LeetCode max constraints for stress tests |
| Practical limits | Don't exceed O(N!) or exponential complexity bounds |

### Testing Your Generator

```python
# Manual test
from generators.{problem} import generate

for i, test_input in enumerate(generate(count=5, seed=42)):
    print(f"--- Case {i+1} ---")
    print(test_input)
    print()
```

---

## Quick Reference

### Generator Template

```python
# generators/{problem_id}_{slug}.py
"""
Test Case Generator for Problem {ID} - {Title}

LeetCode Constraints:
- {constraints}
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    if seed is not None:
        random.seed(seed)
    
    # Edge cases
    edge_cases = ["..."]
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    # Generate valid input
    pass


def generate_for_complexity(n: int) -> str:
    return _generate_case_with_size(n)
```

### CLI Reference

```bash
# Run with generation
python runner/test_runner.py {problem} --generate N
python runner/test_runner.py {problem} --generate-only N
python runner/test_runner.py {problem} --generate N --seed S
python runner/test_runner.py {problem} --generate N --save-failed

# Complexity estimation
python runner/test_runner.py {problem} --estimate
```

> 📖 See [Test Runner Specification](runner/README.md) for full CLI reference.

### Related Documentation

| Document | Content |
|----------|---------|
| [Solution Contract](SOLUTION_CONTRACT.md) | `SOLUTIONS`, `JUDGE_FUNC`, `COMPARE_MODE`, file structure |
| [Test Runner Specification](runner/README.md) | CLI options, output format, troubleshooting |
| [Architecture Migration](ARCHITECTURE_MIGRATION.md) | Polymorphic pattern migration guide |

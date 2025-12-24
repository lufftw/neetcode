# Test Runner Specification

> **Status**: Canonical Reference  
> **Scope**: `runner/test_runner.py` - Main test execution engine  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}  
> **Related**: [Runner README](../../runner/README.md) (Quick Reference)

The Test Runner is the core testing engine for executing solutions against test cases. It supports multi-solution benchmarking, random test generation, and complexity estimation.

---

## Quick Start

```bash
# Run default solution
python runner/test_runner.py 0001_two_sum

# Run specific solution method
python runner/test_runner.py 0023_merge_k_sorted_lists --method heap

# Compare all solutions with timing
python runner/test_runner.py 0023 --all --benchmark
```

---

## Common Use Cases

### Testing a Single Solution

```bash
# Default solution against static tests
python runner/test_runner.py 0001_two_sum

# Specific method
python runner/test_runner.py 0023_merge_k_sorted_lists --method heap

# With execution timing
python runner/test_runner.py 0001_two_sum --benchmark
```

### Comparing Multiple Solutions

```bash
# Test all solutions in SOLUTIONS dict
python runner/test_runner.py 0023 --all

# All solutions with performance comparison
python runner/test_runner.py 0023 --all --benchmark
```

**Output:**
```
============================================================
📊 Performance Comparison
============================================================
Method               Avg Time    Complexity      Static    Generated
------------------------------------------------------------
heap                 12.34ms     O(N log k)      5/5       5/5
divide               15.67ms     O(N log k)      5/5       5/5
============================================================
```

### Random Test Generation

Requires a generator file at `generators/{problem}.py` and `JUDGE_FUNC` in solution.

```bash
# Generate 10 cases (runs together with static tests)
python runner/test_runner.py 0004 --generate 10

# Generate only (skip static tests)
python runner/test_runner.py 0004 --generate-only 20

# Reproducible generation with seed
python runner/test_runner.py 0004 --generate 10 --seed 12345

# Save failed cases for debugging
python runner/test_runner.py 0004 --generate 10 --save-failed
```

### Complexity Estimation

Requires `generate_for_complexity(n)` in generator and `big-O` package.

```bash
pip install big-O

# Estimate time complexity
python runner/test_runner.py 0004 --estimate

# Estimate for specific method
python runner/test_runner.py 0004 --method binary --estimate

# Estimate all methods
python runner/test_runner.py 0004 --all --estimate
```

**Output:**
```
📌 Estimating: heap

   ✅ Estimated: O(n log n)
      Confidence: 0.95
      Details: Best fit: O(n log n), R² = 0.98
```

---

## Command Reference

### Basic Syntax

```bash
python runner/test_runner.py <problem> [OPTIONS]
```

| Argument | Format | Example |
|----------|--------|---------|
| `problem` | `{id}_{slug}` or `{id}` | `0001_two_sum` or `0001` |

### All Options

| Option | Short | Description |
|--------|-------|-------------|
| `--method NAME` | `-m` | Test specific solution method |
| `--all` | `-a` | Test all solutions in SOLUTIONS |
| `--tests-dir DIR` | `-t` | Custom tests directory (default: `tests`) |
| `--generate N` | `-g` | Generate N random cases (with static tests) |
| `--generate-only N` | | Generate N cases only (skip static tests) |
| `--seed N` | `-s` | Random seed for reproducibility |
| `--save-failed` | | Save failed generated cases to `tests/` |
| `--benchmark` | `-b` | Show execution time for each case |
| `--estimate` | `-e` | Estimate time complexity |

---

## Understanding Output

### Test Case Results

| Symbol | Meaning |
|--------|---------|
| ✅ PASS | Test passed |
| ❌ FAIL | Test failed (shows expected vs actual) |
| ⚠️ SKIP | Cannot validate (missing `.out` and no JUDGE_FUNC) |

**Pass:**
```
   case_1: ✅ PASS [exact]
   case_1: ✅ PASS (12.34ms) [judge]
```

**Fail:**
```
   case_2: ❌ FAIL [exact]
      Expected: [0, 1]...
      Actual:   [1, 0]...
```

**Generated Test Fail:**
```
   gen_5: ❌ FAIL [generated]
      ┌─ Input ─────────────────────────────────
      │ 2,7,11,15
      │ 9
      ├─ Actual ────────────────────────────────
      │ [1, 0]
      └─────────────────────────────────────────
      💾 Saved to: tests/0001_two_sum_failed_1.in
```

### Summary

**Single Solution:**
```
Summary: 8 / 10 cases passed.
   ├─ Static (tests/): 5/5
   └─ Generated: 3/5
Average Time: 15.23ms
```

**Multi-Solution:**
```
   Result: 10 / 10 cases passed.
      ├─ Static: 5/5
      └─ Generated: 5/5
```

---

## Validation Modes

The runner validates output in different ways depending on what's defined:

| Mode | When Used | Description |
|------|-----------|-------------|
| `judge` | JUDGE_FUNC + `.out` exists | Custom validation + expected output |
| `judge-only` | JUDGE_FUNC, no `.out` | Custom validation only |
| `exact` | COMPARE_MODE="exact" | Exact string match |
| `sorted` | COMPARE_MODE="sorted" | Sort before comparison |
| `set` | COMPARE_MODE="set" | Set comparison (ignore order/duplicates) |
| `skip` | No `.out`, no JUDGE_FUNC | Cannot validate |

**Priority:** JUDGE_FUNC → COMPARE_MODE → Skip

---

## Required File Structure

### Solution File

Location: `solutions/{problem}.py`

```python
SOLUTIONS = {
    "default": {"class": "Solution", "method": "solve"},
    "heap": {"class": "SolutionHeap", "method": "solve"},
}

# Optional: for multiple correct answers
COMPARE_MODE = "sorted"  # or "exact", "set"

# Optional: custom validation
def JUDGE_FUNC(input_str, expected, actual):
    return validate(input_str, actual)

def solve():
    # Entry point
    ...
```

### Generator File

Location: `generators/{problem}.py`

```python
def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Required: Generate random test cases."""
    if seed is not None:
        random.seed(seed)
    for _ in range(count):
        yield create_test_input()

def generate_for_complexity(n: int) -> str:
    """Optional: For --estimate. Generate test of size n."""
    return create_test_input(size=n)
```

### Test Files

Location: `tests/`

```
tests/
├── 0001_two_sum_1.in       # Input file
├── 0001_two_sum_1.out      # Expected output (optional if JUDGE_FUNC)
├── 0001_two_sum_2.in
├── 0001_two_sum_2.out
└── 0001_two_sum_failed_1.in  # Saved failed case (excluded from normal runs)
```

---

## Troubleshooting

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `No test input files found` | No `tests/{problem}_*.in` files | Add test files or use `--generate` |
| `Solution method 'X' not found` | Method not in SOLUTIONS | Check SOLUTIONS dict keys |
| `Generator requires JUDGE_FUNC` | Using `--generate` without JUDGE_FUNC | Add JUDGE_FUNC to solution |
| `No generator found` | No `generators/{problem}.py` | Create generator file |
| `big-O package not installed` | Using `--estimate` | Run `pip install big-O` |

### Common Issues

**Tests pass locally but fail in runner**
- Check output format (whitespace, newlines)
- Use COMPARE_MODE or normalize output

**"SKIP" cases appearing**
- Add `.out` files or implement JUDGE_FUNC

**Reproduce a failed generated test**
- Use `--seed` with same value
- Check `--save-failed` output files

---

## Architecture

```
test_runner.py (CLI entry point)
├── module_loader.py      # Load solution/generator modules
├── executor.py           # Execute individual test cases
├── reporter.py           # Format and display results
├── compare.py            # Output validation logic
└── complexity_estimator.py  # Big-O estimation
```

### Execution Flow

1. **Load** solution module from `solutions/{problem}.py`
2. **Find** test files from `tests/{problem}_*.in`
3. **Execute** each test case via subprocess
4. **Validate** output (JUDGE_FUNC or COMPARE_MODE)
5. **Report** results (PASS/FAIL/SKIP)

For generated tests:
1. Load generator from `generators/{problem}.py`
2. Check JUDGE_FUNC exists (required for generated tests)
3. Generate test cases
4. Execute and validate via JUDGE_FUNC

---

## Best Practices

1. **Start with static tests** → Create `tests/{problem}_*.in` files first
2. **Add JUDGE_FUNC** → When problems have multiple correct answers
3. **Create generator** → For stress testing and edge case discovery
4. **Use `--seed`** → For reproducible debugging
5. **Use `--save-failed`** → Capture problematic inputs automatically
6. **Use `--all --benchmark`** → Compare solution approaches

---

## Related Documentation

- **[Solution Contract](../SOLUTION_CONTRACT.md)** - Solution file specification
- **[Generator Contract](../GENERATOR_CONTRACT.md)** - Generator file specification
- **[Runner README](../../runner/README.md)** - Quick reference guide

---

## Documentation Maintenance

⚠️ **When modifying `test_runner.py`:**

1. Update this document (`docs/runner/README.md`)
2. Update quick reference (`runner/README.md`)
3. Update docstring (`runner/test_runner.py`)

---

**Maintainer:** See [Contributors](../contributors/README.md)


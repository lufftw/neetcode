# Test Runner Specification

> **Status**: Canonical Reference  
> **Scope**: `runner/test_runner.py` - Main test execution engine  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}  
> **Related**: [Runner README](../../runner/README.md) (Quick Reference)

This document defines the **complete specification** for the Test Runner (`test_runner.py`), the core testing engine that executes solutions against test cases, supports multi-solution benchmarking, random test generation, and complexity estimation.

---

## A. Overview

### A.1 Purpose

The Test Runner is the primary interface for:
- Running solutions against static test cases from `tests/`
- Generating random test cases via generators
- Comparing multiple solution approaches with performance benchmarks
- Estimating time complexity empirically
- Validating solutions using custom judge functions or comparison modes

### A.2 Key Features

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Multi-Solution Testing** | Test all solution variants in one run | Compare different approaches |
| **Performance Benchmarking** | Measure and compare execution times | Identify fastest solution |
| **Random Test Generation** | Generate test cases with seed support | Stress testing, edge case discovery |
| **Custom Validation** | JUDGE_FUNC or COMPARE_MODE | Handle multiple correct answers |
| **Complexity Estimation** | Empirical Big-O analysis | Verify theoretical claims |
| **Reproducible Testing** | Seed-based generation | Debug failures reliably |

### A.3 Architecture

```
test_runner.py (CLI entry point)
├── module_loader.py      # Load solution/generator modules
├── executor.py           # Execute individual test cases
├── reporter.py           # Format and display results
├── compare.py            # Output validation logic
└── complexity_estimator.py  # Big-O estimation
```

---

## B. Command-Line Interface

### B.1 Basic Syntax

```bash
python runner/test_runner.py <problem> [OPTIONS]
```

### B.2 Required Arguments

| Argument | Format | Example | Description |
|----------|--------|---------|-------------|
| `problem` | `{id}_{slug}` | `0001_two_sum` | Problem identifier (4-digit ID + snake_case name) |

### B.3 Solution Selection Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--method` | `-m` | Test specific solution method | `--method heap` |
| `--all` | `-a` | Test all solutions in SOLUTIONS | `--all` |
| *(none)* | | Test default solution | *(default behavior)* |

**Solution Selection Logic:**
1. If `--all` → test all methods in `SOLUTIONS`
2. If `--method X` → test only method `X`
3. If no flag → test `"default"` method (or legacy mode if no SOLUTIONS)

### B.4 Test Source Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--tests-dir` | `-t` | Tests directory (default: `tests`) | `--tests-dir custom_tests` |
| `--generate` | `-g` | Generate N cases (runs with `tests/`) | `--generate 10` |
| `--generate-only` | | Generate N cases (skip `tests/`) | `--generate-only 20` |
| `--seed` | `-s` | Random seed for reproducibility | `--seed 12345` |
| `--save-failed` | | Save failed generated cases to `tests/` | `--save-failed` |

**Test Source Priority:**
- Static tests from `tests/{problem}_*.in` (excludes `*_failed_*.in`)
- Generated tests from `generators/{problem}.py` (if `--generate` specified)
- Both can run together (static + generated)

### B.5 Output Options

| Option | Short | Description |
|--------|-------|-------------|
| `--benchmark` | `-b` | Show execution time for each case |
| `--estimate` | `-e` | Estimate time complexity (requires `generate_for_complexity`) |

---

## C. Usage Examples

### C.1 Basic Testing

```bash
# Run default solution against static tests
python runner/test_runner.py 0001_two_sum

# Run specific solution method
python runner/test_runner.py 0023_merge_k_sorted_lists --method heap

# Test all solutions
python runner/test_runner.py 0023_merge_k_sorted_lists --all

# With performance timing
python runner/test_runner.py 0023 --all --benchmark
```

### C.2 Random Test Generation

```bash
# Generate 10 cases (runs with static tests)
python runner/test_runner.py 0004_median_of_two_sorted_arrays --generate 10

# Generate only (skip static tests)
python runner/test_runner.py 0004 --generate-only 20

# Reproducible generation
python runner/test_runner.py 0004 --generate 10 --seed 12345

# Save failed cases for debugging
python runner/test_runner.py 0004 --generate 10 --save-failed
```

### C.3 Complexity Estimation

```bash
# Estimate time complexity
python runner/test_runner.py 0004 --estimate

# Estimate for specific method
python runner/test_runner.py 0004 --method binary --estimate

# Estimate all methods
python runner/test_runner.py 0004 --all --estimate
```

**Requirements:**
- Generator must implement `generate_for_complexity(n: int) -> str`
- `big-O` package must be installed: `pip install big-O`

### C.4 Combined Usage

```bash
# All solutions + generated tests + benchmark
python runner/test_runner.py 0023 --all --generate 50 --benchmark

# Specific method + generated + save failed
python runner/test_runner.py 0004 --method binary --generate 100 --save-failed
```

---

## D. Test Execution Flow

### D.1 Static Test Execution

1. **Find Test Files**: `tests/{problem}_*.in` (excludes `*_failed_*.in`)
2. **Load Solution Module**: `solutions/{problem}.py`
3. **For Each Test Case**:
   - Read input: `{problem}_{n}.in`
   - Read expected output: `{problem}_{n}.out` (if exists)
   - Execute solution via subprocess
   - Validate output (JUDGE_FUNC or COMPARE_MODE)
   - Report result (PASS/FAIL/SKIP)

### D.2 Generated Test Execution

1. **Load Generator Module**: `generators/{problem}.py`
2. **Check JUDGE_FUNC**: Required for generated tests (no `.out` files)
3. **Generate Test Cases**: Call `generate(count, seed)`
4. **For Each Generated Case**:
   - Execute solution with generated input
   - Validate via JUDGE_FUNC only
   - Report result
   - Save failed cases if `--save-failed` specified

### D.3 Validation Modes

| Mode | Trigger | Description |
|------|---------|-------------|
| `judge` | JUDGE_FUNC + `.out` exists | Custom validation + expected output check |
| `judge-only` | JUDGE_FUNC, no `.out` | Custom validation only (generated tests) |
| `exact` | COMPARE_MODE="exact" | Exact string match |
| `sorted` | COMPARE_MODE="sorted" | Sort before comparison |
| `set` | COMPARE_MODE="set" | Set comparison (ignore order/duplicates) |
| `skip` | No `.out`, no JUDGE_FUNC | Cannot validate, skipped |

**Priority:**
1. JUDGE_FUNC (if defined) → always used
2. COMPARE_MODE (if `.out` exists) → fallback
3. Skip (if neither available)

---

## E. Output Format

### E.1 Test Case Results

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

**Skip:**
```
   case_3: ⚠️ SKIP (missing .out, no JUDGE_FUNC)
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

### E.2 Summary

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

============================================================
📊 Performance Comparison
============================================================
Method               Avg Time    Complexity      Static    Generated
------------------------------------------------------------
heap                 12.34ms     O(N log k)      5/5       5/5
divide               15.67ms     O(N log k)      5/5       5/5
============================================================
```

### E.3 Complexity Estimation Output

```
============================================================
📈 Complexity Estimation
============================================================

📌 Estimating: heap

   ✅ Estimated: O(n log n)
      Confidence: 0.95
      Details: Best fit: O(n log n), R² = 0.98
```

---

## F. Integration with Solution Files

### F.1 Solution Module Requirements

The runner expects solutions to follow the [Solution Contract](../SOLUTION_CONTRACT.md):

| Element | Required | Purpose |
|---------|----------|---------|
| `SOLUTIONS` dict | ✅ | Metadata for multi-solution support |
| `solve()` function | ✅ | Entry point for execution |
| `COMPARE_MODE` | ⭕ | Output comparison mode |
| `JUDGE_FUNC` | ⭕ | Custom validation function |

### F.2 Method Selection

**Environment Variable:**
- `SOLUTION_METHOD` is set by the runner to select which solution class/method to use

**Example:**
```python
# solutions/0023_merge_k_sorted_lists.py
SOLUTIONS = {
    "heap": {"class": "SolutionHeap", "method": "mergeKLists"},
    "divide": {"class": "SolutionDivide", "method": "mergeKLists"},
}

# Runner sets: env['SOLUTION_METHOD'] = "heap"
# _runner.get_solver() uses this to instantiate SolutionHeap
```

---

## G. Integration with Generator Files

### G.1 Generator Module Requirements

The runner expects generators to follow the [Generator Contract](../GENERATOR_CONTRACT.md):

| Element | Required | Purpose |
|---------|----------|---------|
| `generate(count, seed)` | ✅ | Main test generation function |
| `generate_for_complexity(n)` | ⭕ | For complexity estimation |

### G.2 Generator Usage

**For Random Testing:**
```python
# generators/0001_two_sum.py
def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    if seed is not None:
        random.seed(seed)
    # ... yield test inputs ...
```

**For Complexity Estimation:**
```python
def generate_for_complexity(n: int) -> str:
    """Generate test case with input size = n."""
    # Return test input string for size n
    ...
```

**JUDGE_FUNC Requirement:**
- Generated tests require `JUDGE_FUNC` in solution file (no `.out` files)
- Runner will error if generator is used without JUDGE_FUNC

---

## H. Error Handling

### H.1 Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `No test input files found` | No `tests/{problem}_*.in` and no `--generate` | Add test files or use `--generate` |
| `Solution method 'X' not found` | `--method X` but X not in SOLUTIONS | Check available methods |
| `Generator requires JUDGE_FUNC` | Using `--generate` but no JUDGE_FUNC | Add JUDGE_FUNC to solution |
| `No generator found` | `--generate` but no `generators/{problem}.py` | Create generator file |
| `big-O package not installed` | `--estimate` without big-O | `pip install big-O` |

### H.2 Validation Failures

**Missing `.out` File:**
- If no JUDGE_FUNC → case is skipped
- If JUDGE_FUNC exists → validated via judge-only mode

**Failed Generated Cases:**
- Display input and actual output
- If `--save-failed` → saved to `tests/{problem}_failed_{n}.in`
- Reproduction hint shown if `--seed` was used

---

## I. Advanced Features

### I.1 Multi-Solution Benchmarking

When `--all --benchmark` is used:
- All solutions run against same test cases
- Execution times collected per method
- Summary table shows performance comparison
- Includes complexity metadata from SOLUTIONS

**Use Case:** Compare heap vs divide-and-conquer approaches

### I.2 Reproducible Testing

**Seed-Based Generation:**
```bash
# First run
python runner/test_runner.py 0004 --generate 10 --seed 12345

# Reproduce exact same cases
python runner/test_runner.py 0004 --generate 10 --seed 12345
```

**Failed Case Reproduction:**
- Failed cases saved with `--save-failed`
- Can be re-run with `case_runner.py` for debugging

### I.3 Complexity Estimation

**How It Works:**
1. Generator provides `generate_for_complexity(n)` for different input sizes
2. Runner executes solution with increasing sizes: n=10, 20, 40, 80, ...
3. Measures execution time for each size
4. Fits curve to determine Big-O complexity
5. Reports estimated complexity with confidence score

**Requirements:**
- `big-O` package installed
- Generator implements `generate_for_complexity(n: int) -> str`
- Solution must be deterministic

---

## J. Module Dependencies

### J.1 Internal Modules

| Module | Purpose | Used By |
|--------|---------|---------|
| `module_loader.py` | Load solution/generator modules | test_runner |
| `executor.py` | Execute individual test cases | test_runner, reporter |
| `reporter.py` | Format and display results | test_runner |
| `compare.py` | Output validation logic | executor |
| `complexity_estimator.py` | Big-O estimation | test_runner |

### J.2 External Dependencies

| Package | Required For | Installation |
|---------|--------------|--------------|
| `big-O` | Complexity estimation | `pip install big-O` |

---

## K. File Structure

### K.1 Test Files

```
tests/
├── {problem}_1.in          # Static test input
├── {problem}_1.out         # Expected output (optional)
├── {problem}_2.in
├── {problem}_2.out
└── {problem}_failed_1.in    # Saved failed case (excluded from normal runs)
```

### K.2 Solution Files

```
solutions/
└── {problem}.py            # Solution module with SOLUTIONS dict
```

### K.3 Generator Files

```
generators/
└── {problem}.py            # Generator module with generate() function
```

---

## L. Best Practices

### L.1 Testing Workflow

1. **Start with Static Tests**: Create `tests/{problem}_*.in` files
2. **Add JUDGE_FUNC**: For problems with multiple correct answers
3. **Create Generator**: For stress testing and edge case discovery
4. **Run with Seed**: Use `--seed` for reproducible debugging
5. **Save Failed Cases**: Use `--save-failed` to capture problematic inputs
6. **Benchmark Solutions**: Use `--all --benchmark` to compare approaches

### L.2 Debugging Failed Tests

1. **Check Output**: Compare actual vs expected in failure message
2. **Reproduce**: Use saved failed case or `--seed` to reproduce
3. **Run Single Case**: Use `case_runner.py` for detailed debugging
4. **Validate Input**: Check if input format matches solution expectations

### L.3 Performance Optimization

1. **Benchmark First**: Identify slow solutions with `--benchmark`
2. **Compare Approaches**: Use `--all` to see relative performance
3. **Estimate Complexity**: Verify theoretical claims with `--estimate`
4. **Profile Large Cases**: Use `--generate-only` with large N for profiling

---

## M. Troubleshooting

### M.1 Test Runner Issues

**Problem:** "No test input files found"
- **Check:** `tests/{problem}_*.in` files exist
- **Solution:** Create test files or use `--generate`

**Problem:** "Solution method 'X' not found"
- **Check:** `SOLUTIONS` dict in solution file
- **Solution:** Verify method name matches SOLUTIONS key

**Problem:** "Generator requires JUDGE_FUNC"
- **Check:** Solution file has `JUDGE_FUNC` defined
- **Solution:** Add JUDGE_FUNC or use static tests only

### M.2 Validation Issues

**Problem:** Tests pass locally but fail in runner
- **Check:** Output format (whitespace, newlines)
- **Solution:** Use `normalize_output()` or adjust COMPARE_MODE

**Problem:** "SKIP" cases appearing
- **Check:** `.out` files exist or JUDGE_FUNC defined
- **Solution:** Add expected outputs or implement JUDGE_FUNC

---

## N. Related Documentation

- **[Solution Contract](../SOLUTION_CONTRACT.md)**: Solution file specification
- **[Generator Contract](../GENERATOR_CONTRACT.md)**: Generator file specification
- **[Runner README](../../runner/README.md)**: Quick reference guide
- **[Architecture Migration](../ARCHITECTURE_MIGRATION.md)**: Migration guide for multi-solution support

---

## O. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Initial | Basic test execution |
| 2.0 | Multi-solution | Added `--method`, `--all`, SOLUTIONS support |
| 2.1 | Generator | Added `--generate`, `--seed`, `--save-failed` |
| 2.2 | Complexity | Added `--estimate` for Big-O estimation |
| 2.3 | Benchmark | Enhanced `--benchmark` with comparison table |

---

## Documentation Maintenance

⚠️ **Important:** When modifying `test_runner.py` or its behavior:

1. **Update this document** (`docs/runner/README.md`) - Complete specification
2. **Update quick reference** (`runner/README.md`) - Quick start guide
3. **Update docstring** (`runner/test_runner.py`) - Inline documentation

These three files must stay in sync. For quick reference, see [Runner README](../../runner/README.md).

---

**Last Updated:** {{ git_revision_date_localized }}  
**Maintainer:** See [Contributors](../contributors/README.md)


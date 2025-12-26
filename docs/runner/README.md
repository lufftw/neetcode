# Test Runner Specification

> **Status**: Canonical Reference  
> **Scope**: `runner/test_runner.py` - Main test execution engine  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}  
> **Related**: [Runner README](https://github.com/lufftw/neetcode/blob/main/runner/README.md) (Quick Reference)

The Test Runner is the core testing engine for executing solutions against test cases. It supports multi-solution benchmarking, random test generation, and complexity estimation.

---

## Quick Start

```bash
# Run default solution
python runner/test_runner.py 0001_two_sum

# Run specific solution method
python runner/test_runner.py 0023 --method heap

# Compare all solutions with timing
python runner/test_runner.py 0023 --all --benchmark
```

---

## Command Reference

```bash
python runner/test_runner.py <problem> [OPTIONS]
```

### Solution Selection

| Option | Description |
|--------|-------------|
| *(none)* | Run `"default"` solution |
| `--method NAME` | Run specific solution |
| `--all` | Run all solutions in `SOLUTIONS` |

### Test Generation

| Option | Description |
|--------|-------------|
| `--generate N` | Static tests + N generated cases |
| `--generate-only N` | Skip static, generate N cases only |
| `--seed N` | Reproducible generation |
| `--save-failed` | Save failed cases to `tests/` |

> 📖 Requires generator file. See [Generator Contract](../GENERATOR_CONTRACT.md).

### Analysis

| Option | Description |
|--------|-------------|
| `--benchmark` | Show execution time per case (includes memory metrics if psutil installed) |
| `--estimate` | Estimate time complexity |

> 📖 `--estimate` requires `generate_for_complexity(n)` and `pip install big-O`.

### Memory Profiling

| Option | Description |
|--------|-------------|
| `--memory-trace` | Show run-level memory traces (sparklines) per method |
| `--trace-compare` | Multi-method memory comparison with ranking table |
| `--memory-per-case` | Debug: Top-K cases by peak RSS |

> 📖 Memory profiling requires `pip install psutil`. Without it, memory columns show "Unavailable".

### Other

| Option | Description |
|--------|-------------|
| `--tests-dir DIR` | Custom tests directory (default: `tests`) |

---

## Usage Examples

### Basic Testing

```bash
python runner/test_runner.py 0001_two_sum
python runner/test_runner.py 0023 --method heap
python runner/test_runner.py 0023 --all --benchmark
```

### Random Testing

```bash
python runner/test_runner.py 0004 --generate 10
python runner/test_runner.py 0004 --generate 10 --seed 12345
python runner/test_runner.py 0004 --generate 100 --save-failed
```

### Complexity Estimation

```bash
python runner/test_runner.py 0004 --estimate
python runner/test_runner.py 0004 --all --estimate
```

---

## Output Format

### Test Results

```
   case_1: ✅ PASS [exact]
   case_2: ✅ PASS (12.34ms) [judge]
   case_3: ❌ FAIL [exact]
      Expected: [0, 1]...
      Actual:   [1, 0]...
   case_4: ⚠️ SKIP (missing .out, no JUDGE_FUNC)
```

### Multi-Solution Comparison

When running `--all --benchmark`, the test runner displays a **visual bar chart** followed by a detailed comparison table:

**Visual Bar Chart with Approach Legend:**

```
   ╔═══════════════════════════════════════════════════════════════════════════════╗
   ║                  0131_palindrome_partitioning - Performance                   ║
   ╠═══════════════════════════════════════════════════════════════════════════════╣
   ║ default: ████████████████████  158ms                                          ║
   ║ naive:   ███████████████████░  152ms                                          ║
   ╚═══════════════════════════════════════════════════════════════════════════════╝

   default  → Backtracking with DP-Precomputed Palindrome Table
   naive    → Backtracking with On-the-Fly Checking
```

The bar length is proportional to execution time (longest time = full bar). The approach descriptions are shown in a legend below the chart, parsed from class header comments.

**Enhanced Method Header:**

```
──────────────────────────────────────────────────
📌 Shorthand: default
   Approach: Backtracking with DP-Precomputed Palindrome Table
   Complexity: O(n × 2^n) time, O(n^2) space
──────────────────────────────────────────────────
```

> **Note:** On terminals that don't support Unicode, ASCII fallback characters are used.

**Detailed Table:**

```
======================================================================
Performance Comparison (Details)
======================================================================

Method         Avg Time   Pass Rate  Complexity
-----------  ----------  ----------  --------------------
default        158.17ms         2/2  O(n × 2^n) time, O(n^2) space
naive          152.00ms         2/2  O(n × 2^n × n) time, O(n) space

default      → Backtracking with DP-Precomputed Palindrome Table
naive        → Backtracking with On-the-Fly Checking

======================================================================
```

The approach descriptions are shown in a legend below the table, matching the format used in the visual bar chart.

### Complexity Estimation with Visual Charts

Use `--all --benchmark --estimate` to integrate complexity estimation into the visual performance comparison:

```bash
python runner/test_runner.py 0215 --all --benchmark --estimate
```

This displays:

1. **Visual bar chart** with execution times
2. **Approach legend** (method → approach name)
3. **Estimated complexity section** with confidence scores
4. **Detailed table** showing both declared and estimated complexity

**Example Output:**

```
   ╔════════════════════════════════════════════════════╗
   ║ 0215_kth_largest_element_in_an_array - Performance ║
   ╠════════════════════════════════════════════════════╣
   ║ default:     █████████████████░░░  170ms           ║
   ║ quickselect: ███████████████████░  191ms           ║
   ║ heap:        ████████████████████  199ms           ║
   ╚════════════════════════════════════════════════════╝

   default      → Quickselect Algorithm
   quickselect  → Quickselect Algorithm
   heap         → Heap-Based Solution

   📈 Estimated Complexity:
   default    : O(n)        [confidence: 1.00]
   quickselect: O(n log n)  [confidence: 1.00]
   heap       : O(n log n)  [confidence: 1.00]

======================================================================
Performance Comparison (Details)
======================================================================

Method         Avg Time   Pass Rate      Declared     Estimated
-----------  ----------  ----------  ------------  ------------
default        169.59ms         3/3  O(n) average          O(n)
quickselect    190.74ms         3/3  O(n) average    O(n log n)
heap           198.63ms         3/3  O(n log k)      O(n log n)

default      → Quickselect Algorithm
quickselect  → Quickselect Algorithm
heap         → Heap-Based Solution

======================================================================
```

**Requirements for Complexity Estimation:**

- Generator must provide `generate_for_complexity(n)` function
- Install `pip install big-O` package

### Standalone Complexity Estimation

For complexity estimation without benchmark comparison:

```bash
python runner/test_runner.py 0004 --estimate
```

```
📌 Estimating: heap

   ✅ Estimated: O(n log n)
      Confidence: 0.95
```

---

## Validation Modes

| Mode | When Used |
|------|-----------|
| `[judge]` | `JUDGE_FUNC` + `.out` exists |
| `[judge-only]` | `JUDGE_FUNC`, no `.out` (generated tests) |
| `[exact]` | Default string comparison |
| `[sorted]` | `COMPARE_MODE="sorted"` |
| `[set]` | `COMPARE_MODE="set"` |
| `[skip]` | No `.out`, no `JUDGE_FUNC` |

> 📖 See [Solution Contract § Validation](../SOLUTION_CONTRACT.md#validation-judge_func--compare_mode) for `JUDGE_FUNC` and `COMPARE_MODE` details.

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `No test input files found` | Add `tests/{problem}_*.in` or use `--generate` |
| `Solution method 'X' not found` | Check `SOLUTIONS` dict in solution file |
| `Generator requires JUDGE_FUNC` | Add `JUDGE_FUNC` to solution |
| `No generator found` | Create `generators/{problem}.py` |
| `big-O package not installed` | `pip install big-O` |

---

## Complete Reference

### All Options

| Option | Short | Description |
|--------|-------|-------------|
| `--method NAME` | `-m` | Run specific solution |
| `--all` | `-a` | Run all solutions in `SOLUTIONS` |
| `--benchmark` | `-b` | Show execution time per case |
| `--tests-dir DIR` | `-t` | Custom tests directory (default: `tests`) |
| `--generate N` | `-g` | Static tests + N generated cases |
| `--generate-only N` | — | Skip static, generate N cases only |
| `--seed N` | `-s` | Reproducible generation |
| `--save-failed` | — | Save failed cases to `tests/` |
| `--estimate` | `-e` | Estimate time complexity |

### Advanced Combinations

```bash
# Full comparison: all methods, benchmarked, with generated tests
python runner/test_runner.py 0023 -a -b -g 50 -s 12345

# Stress test only (skip static tests)
python runner/test_runner.py 0023 --generate-only 100 --all

# Estimate complexity for all solutions
python runner/test_runner.py 0023 --all --estimate

# Full benchmark with complexity estimation (visual charts)
python runner/test_runner.py 0215 --all --benchmark --estimate

# Debug failed case with saved input
python runner/test_runner.py 0023 --generate 100 --save-failed
```

### Output Details

**Failed Generated Case Box:**

```
   gen_3: ❌ FAIL [generated]
      ┌─ Input ─────────────────────────────────
      │ [1,3,5,7]
      │ [2,4,6,8]
      ├─ Actual ────────────────────────────────
      │ 4.5
      └─────────────────────────────────────────
      💾 Saved to: tests/0004_failed_1.in
```

**Reproduction Hint (when using `--seed`):**

```
💡 To reproduce: python runner/test_runner.py 0004 --generate 10 --seed 12345
```

**Summary Breakdown (static + generated):**

```
Summary: 15 / 15 cases passed.
   ├─ Static (tests/): 5/5
   └─ Generated: 10/10
```

### Internal Behaviors

| Behavior | Description |
|----------|-------------|
| Failed file exclusion | Files matching `*_failed_*.in` are excluded from normal test runs |
| Legacy mode | When no `SOLUTIONS` dict exists, runs single default solution |
| Exit codes | Exits with code `1` on missing tests, invalid method, or missing generator |

---

## Case Runner

`case_runner.py` runs a **single test case** without comparison — ideal for debugging.

```bash
python runner/case_runner.py <problem> <case_number>
```

**Example:**

```bash
python runner/case_runner.py 0001_two_sum 1
```

This runs `solutions/0001_two_sum.py` with input from `tests/0001_two_sum_1.in` and displays output directly (no pass/fail comparison).

---

## VSCode Integration

Pre-configured tasks and debug configurations are provided in `.vscode/`.

- **Ctrl+Shift+B**: Run all tests for current problem (default build task)
- **F5**: Debug with breakpoints

> 📖 See [VSCode Setup Guide](../contributors/VSCODE_SETUP.md) for complete task/debug configuration reference.

---

## Architecture

```
test_runner.py (CLI)
├── module_loader.py      # Load solution/generator modules
├── executor.py           # Execute test cases
├── reporter.py           # Format results
├── compare.py            # Output validation
└── complexity_estimator.py  # Big-O estimation
```

---

## Execution Methods

The test runner supports two execution methods:

### Method 1: Virtual Environment (Recommended)

Use the project's virtual environment for isolated dependencies:

```bash
# Windows (PowerShell/CMD)
leetcode\Scripts\python.exe runner/test_runner.py 0023 --all --benchmark

# Linux/macOS
./leetcode/bin/python runner/test_runner.py 0023 --all --benchmark
```

### Method 2: System Python

Use system Python directly (requires dependencies installed globally):

```bash
python runner/test_runner.py 0023 --all --benchmark
```

---

## Dependencies

### Required

- Python 3.10+
- Solution files in `solutions/`
- Test files in `tests/` (or use generators)

### Optional Packages

| Package | Feature | Install |
|---------|---------|---------|
| `big-O` | Complexity estimation (`--estimate`) | `pip install big-O` |
| `psutil` | RSS memory profiling (`--memory-trace`, `--trace-compare`, `--memory-per-case`) | `pip install psutil` |
| `sparklines` | Memory trace visualization (sparkline charts) | `pip install sparklines` |
| `tabulate` | CLI table formatting | `pip install tabulate` |

**Install all optional packages:**

```bash
pip install big-O psutil sparklines tabulate
```

### Memory Measurement Types

| Type | Source | Method | Description |
|------|--------|--------|-------------|
| **RSS** | Static/Generated tests | `psutil` (subprocess) | Full process memory including interpreter |
| **Alloc** | `--estimate` runs | `tracemalloc` (in-process) | Python allocations only |

> **Note:** RSS and Alloc metrics are displayed separately in `--memory-per-case`
> output because they measure different things and are not directly comparable.

### Graceful Degradation

| Missing Package | Behavior |
|-----------------|----------|
| `big-O` | `--estimate` ignored, complexity shown as "Unknown" |
| `psutil` | RSS memory columns show "Unavailable", warning displayed |
| `sparklines` | Falls back to simple ASCII visualization |
| `tabulate` | Falls back to manual column formatting |

---

## Related Documentation

| Document | Content |
|----------|---------|
| [Solution Contract](../SOLUTION_CONTRACT.md) | `SOLUTIONS`, `JUDGE_FUNC`, `COMPARE_MODE`, file structure |
| [Generator Contract](../GENERATOR_CONTRACT.md) | `generate()`, `generate_for_complexity()`, edge cases |
| [Runner README](https://github.com/lufftw/neetcode/blob/main/runner/README.md) | Quick reference (in-module) |
| [VSCode Setup Guide](../contributors/VSCODE_SETUP.md) | Tasks, debug configurations, workflow examples |

---

## Documentation Maintenance

When modifying `test_runner.py`:

1. Update this spec (`docs/runner/README.md`)
2. Update quick reference ([runner/README.md](https://github.com/lufftw/neetcode/blob/main/runner/README.md))
3. Update docstring (`runner/test_runner.py`)

---

**Maintainer:** See [Contributors](../contributors/README.md)

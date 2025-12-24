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
| `--benchmark` | Show execution time per case |
| `--estimate` | Estimate time complexity |

> 📖 `--estimate` requires `generate_for_complexity(n)` and `pip install big-O`.

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

### Complexity Estimation

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

> 📖 See [Solution Contract § Validation](../SOLUTION_CONTRACT.md#c-judge--validation-contract) for `JUDGE_FUNC` and `COMPARE_MODE` details.

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

## Related Documentation

| Document | Content |
|----------|---------|
| [Solution Contract](../SOLUTION_CONTRACT.md) | `SOLUTIONS`, `JUDGE_FUNC`, `COMPARE_MODE`, file structure |
| [Generator Contract](../GENERATOR_CONTRACT.md) | `generate()`, `generate_for_complexity()`, edge cases |
| [Runner README](../../runner/README.md) | Quick reference (in-module) |
| [VSCode Setup Guide](../contributors/VSCODE_SETUP.md) | Tasks, debug configurations, workflow examples |

---

## Documentation Maintenance

When modifying `test_runner.py`:

1. Update this spec (`docs/runner/README.md`)
2. Update quick reference (`runner/README.md`)
3. Update docstring (`runner/test_runner.py`)

---

**Maintainer:** See [Contributors](../contributors/README.md)

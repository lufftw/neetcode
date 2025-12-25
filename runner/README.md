# Test Runner - Quick Reference

> **Quick Start Guide**  
> For complete documentation, see [docs/runner/README.md](../docs/runner/README.md)

## Overview

`test_runner.py` is the main test execution engine for running solutions against test cases, comparing multiple solution approaches, and generating random test cases.

## Quick Start

```bash
# Run default solution
python runner/test_runner.py 0001_two_sum

# Run specific solution method
python runner/test_runner.py 0023 --method heap

# Test all solutions with benchmark
python runner/test_runner.py 0023 --all --benchmark

# Generate random test cases
python runner/test_runner.py 0004 --generate 10 --seed 12345
```

## Common Commands

| Command | Description |
|---------|-------------|
| `python runner/test_runner.py <problem>` | Run default solution |
| `python runner/test_runner.py <problem> --method <name>` | Run specific method |
| `python runner/test_runner.py <problem> --all` | Test all solutions |
| `python runner/test_runner.py <problem> --all --benchmark` | Compare performance |
| `python runner/test_runner.py <problem> --all --benchmark --estimate` | Compare with complexity estimation |
| `python runner/test_runner.py <problem> --generate N` | Generate N test cases |
| `python runner/test_runner.py <problem> --generate N --seed S` | Reproducible generation |
| `python runner/test_runner.py <problem> --estimate` | Estimate complexity |
| `python runner/test_runner.py <problem> --all --memory-trace` | Show memory traces |
| `python runner/test_runner.py <problem> --all --trace-compare` | Compare memory usage |
| `python runner/test_runner.py <problem> --memory-per-case` | Debug: Top-K cases by RSS |

## Key Features

- ✅ **Multi-Solution Testing**: Test all solution variants in one run
- ✅ **Performance Benchmarking**: Compare execution times with visual bar chart
- ✅ **Random Test Generation**: Stress testing with seed support
- ✅ **Custom Validation**: JUDGE_FUNC or COMPARE_MODE
- ✅ **Complexity Estimation**: Empirical Big-O analysis
- ✅ **Memory Profiling**: RSS measurement and comparison (requires `psutil`)

## Visual Performance Comparison

When running multiple solutions with `--all --benchmark`, the test runner displays a visual bar chart with approach names extracted from class comments:

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

### Integrated Complexity Estimation

Use `--all --benchmark --estimate` to include estimated complexity in the visual charts:

```bash
python runner/test_runner.py 0215 --all --benchmark --estimate
```

Output includes estimated complexity alongside approach descriptions:

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
```

The detailed table also shows both declared and estimated complexity:

```
======================================================================
Performance Comparison (Details)
======================================================================

Method         Avg Time   Pass Rate      Declared     Estimated
-----------  ----------  ----------  ------------  ------------
default        169.59ms         3/3  O(n) average          O(n)
quickselect    190.74ms         3/3  O(n) average    O(n log n)
heap           198.63ms         3/3  O(n log k)      O(n log n)
======================================================================
```

> **Note:** Complexity estimation requires `generate_for_complexity(n)` function in the generator and `pip install big-O`.

## Memory Profiling

The `--benchmark` flag automatically includes memory metrics (Peak RSS, P95 RSS) in the comparison table when `psutil` is installed.

```bash
# Memory metrics in benchmark table
python runner/test_runner.py 0023 --all --benchmark

# Run-level memory traces
python runner/test_runner.py 0023 --all --memory-trace

# Multi-method memory comparison with ranking
python runner/test_runner.py 0023 --all --trace-compare

# Debug: Top 5 cases by peak RSS
python runner/test_runner.py 0023 --memory-per-case
```

**Benchmark Table with Memory Columns:**

```
Method     Avg Time   Pass Rate  Aux Space  Peak RSS   P95 RSS
default      83.2ms     50/50     O(N)       25.4MB     23.1MB
native      120.5ms     50/50     O(1)       21.1MB     20.8MB
```

**Memory Trace Output:**

```
Memory Trace (Run-level RSS)

default:
▁▂▃▅▇▆▅▃▂▁
Peak 25.4MB | P95 23.1MB
```

> **Note:** Memory profiling requires `pip install psutil`. The system gracefully degrades without it.

**Enhanced Method Display:**

Each method also shows detailed information when running:

```
──────────────────────────────────────────────────
📌 Shorthand: default
   Approach: Backtracking with DP-Precomputed Palindrome Table
   Complexity: O(n × 2^n) time, O(n^2) space
──────────────────────────────────────────────────
```

The approach names are automatically parsed from the class header comments in the solution file:

```python
# ============================================================================
# Solution 1: Backtracking with DP-Precomputed Palindrome Table
# Time: O(n × 2^n), Space: O(n^2)
#   - Key insight or implementation detail
# ============================================================================
class SolutionDP:
    ...
```

**Usage:**
```bash
python runner/test_runner.py 0131 --all --benchmark
python runner/test_runner.py 0215 --all --benchmark --estimate
```

> **Note:** On terminals that don't support Unicode (e.g., some Windows terminals), ASCII fallback characters are used automatically.

## File Structure

```
runner/
├── test_runner.py          # Main CLI entry point (~380 lines)
├── module_loader.py         # Load solution/generator modules (~120 lines)
├── executor.py              # Execute test cases (~240 lines)
├── method_runner.py         # Run tests per method (~410 lines)
├── reporter.py              # Format results (~440 lines)
├── compare.py               # Output validation (~190 lines)
├── complexity_estimator.py  # Big-O estimation (~290 lines)
├── memory_profiler.py       # RSS measurement and metrics (~340 lines)
└── solution_parser.py       # Parse solution class comments (~250 lines)
```

## Requirements

- Solution files in `solutions/` (see [Solution Contract](../docs/SOLUTION_CONTRACT.md))
- Test files in `tests/` (optional, can use generators)
- Generator files in `generators/` (optional, for random testing)
- `big-O` package (optional, for complexity estimation): `pip install big-O`
- `psutil` package (optional, for memory profiling): `pip install psutil`

## Validation Modes

| Mode | When Used |
|------|-----------|
| `judge` | JUDGE_FUNC + `.out` exists |
| `judge-only` | JUDGE_FUNC, no `.out` (generated tests) |
| `exact` | COMPARE_MODE="exact" |
| `sorted` | COMPARE_MODE="sorted" |
| `set` | COMPARE_MODE="set" |
| `skip` | No `.out`, no JUDGE_FUNC |

## Troubleshooting

**No test files found?**
- Create `tests/{problem}_*.in` files, or
- Use `--generate N` to generate test cases

**Generator requires JUDGE_FUNC?**
- Add `JUDGE_FUNC` to solution file, or
- Use static tests only (without `--generate`)

**Method not found?**
- Check `SOLUTIONS` dict in solution file
- List available methods: run without `--method` to see error

## Related Documentation

- **[Complete Documentation](../docs/runner/README.md)**: Full specification and examples
- **[Solution Contract](../docs/SOLUTION_CONTRACT.md)**: Solution file requirements
- **[Generator Contract](../docs/GENERATOR_CONTRACT.md)**: Generator file requirements

---

## Documentation Maintenance

⚠️ **Important:** When modifying `test_runner.py` or its behavior:

1. **Update this README** (`runner/README.md`) - Quick reference changes
2. **Update detailed docs** (`docs/runner/README.md`) - Complete specification
3. **Update docstring** (`test_runner.py`) - Inline documentation

These three files must stay in sync. See [Complete Documentation](../docs/runner/README.md) for the full specification.


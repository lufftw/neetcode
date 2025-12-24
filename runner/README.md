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
| `python runner/test_runner.py <problem> --generate N` | Generate N test cases |
| `python runner/test_runner.py <problem> --generate N --seed S` | Reproducible generation |
| `python runner/test_runner.py <problem> --estimate` | Estimate complexity |

## Key Features

- ✅ **Multi-Solution Testing**: Test all solution variants in one run
- ✅ **Performance Benchmarking**: Compare execution times
- ✅ **Random Test Generation**: Stress testing with seed support
- ✅ **Custom Validation**: JUDGE_FUNC or COMPARE_MODE
- ✅ **Complexity Estimation**: Empirical Big-O analysis

## File Structure

```
runner/
├── test_runner.py          # Main CLI entry point
├── module_loader.py         # Load solution/generator modules
├── executor.py              # Execute test cases
├── reporter.py              # Format results
├── compare.py               # Output validation
└── complexity_estimator.py  # Big-O estimation
```

## Requirements

- Solution files in `solutions/` (see [Solution Contract](../docs/SOLUTION_CONTRACT.md))
- Test files in `tests/` (optional, can use generators)
- Generator files in `generators/` (optional, for random testing)
- `big-O` package (optional, for complexity estimation): `pip install big-O`

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


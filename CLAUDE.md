# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NeetCode is a scalable Python practice framework for algorithm learning and interview preparation. It provides:
- Knowledge graph-driven learning with interconnected patterns and API kernels
- Industrial-strength testing infrastructure (random test generation, custom judges, benchmarking)
- AI-powered mind maps for pattern discovery
- VS Code integration for one-click testing and debugging

## Key Commands

### Creating New Problems
```bash
# Windows
scripts\new_problem.bat <leetcode_id>
scripts\new_problem.bat <leetcode_id> --with-tests

# Linux/macOS
./scripts/new_problem.sh <leetcode_id>
./scripts/new_problem.sh <leetcode_id> --with-tests

# Advanced options
scripts\new_problem.bat 104 --solve-mode tiered  # For tree/linked list problems
```

### Running Tests
```bash
# Run all tests for a problem
python runner/test_runner.py <problem_name>

# Run specific test case
python runner/case_runner.py <problem_name> <case_number>

# Benchmark
python runner/test_runner.py <problem_name> --benchmark

# Compare all solutions
python runner/test_runner.py <problem_name> --all --benchmark

# Generate random tests
python runner/test_runner.py <problem_name> --generate 10
python runner/test_runner.py <problem_name> --generate 10 --seed 42

# Estimate complexity
python runner/test_runner.py <problem_name> --estimate
```

### Running Unit Tests
```bash
# Activate virtual environment first
leetcode\Scripts\activate  # Windows
source leetcode/bin/activate  # Linux/macOS

# Run all unit tests
python -m pytest .dev/tests -v
```

## Code Architecture

### Directory Structure
- `solutions/` - Solution files (one per LeetCode problem)
- `tests/` - Test cases (.in/.out files)
- `generators/` - Random test generators (optional)
- `runner/` - Test execution engine
- `src/` - Core packages (see below)
- `tools/` - Standalone tools (mindmaps, patterndocs, review-code)
- `ontology/` - Algorithm ontology (TOML files)
- `meta/` - Problem and pattern metadata
- `docs/` - MkDocs documentation

### Core Packages (`src/`)

```
leetcode_datasource ←── codegen ──→ practice_workspace
```

| Package | Purpose |
|---------|---------|
| `leetcode_datasource` | LeetCode API + SQLite cache, problem metadata |
| `codegen` | Solution/practice skeleton generation, test extraction |
| `practice_workspace` | Practice file history and restore |

Dependency rule: `tools/ → src/` only, never reverse.

### Solution File Format

Solutions follow a standardized polymorphic pattern:

```python
# solutions/XXXX_problem_name.py
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "methodName",
        "complexity": "O(n) time, O(n) space",
        "description": "Brief description",
    },
}

class Solution:
    def methodName(self, ...):
        # Implementation
        pass

def solve():
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    # Parse input (canonical JSON format)
    param1 = json.loads(lines[0])
    param2 = json.loads(lines[1])

    # Get solver and call method
    solver = get_solver(SOLUTIONS)
    result = solver.methodName(param1, param2)

    # Output canonical JSON
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    solve()
```

### Test File Format

Test files use canonical JSON literal format (one value per line):

**Input file** (`tests/XXXX_problem_name_N.in`):
```
[2,7,11,15]
9
```

**Output file** (`tests/XXXX_problem_name_N.out`):
```
[0,1]
```

Requirements:
- Line ending: LF (Unix format)
- Encoding: UTF-8
- Single newline at end of file

### Multi-Solution Pattern

For problems with multiple approaches:

```python
SOLUTIONS = {
    "default": {...},
    "approach1": {
        "class": "SolutionApproach1",
        "method": "solve",
        ...
    },
    "approach2": {
        "class": "SolutionApproach2",
        "method": "solve",
        ...
    },
}
```

Run with `--method approach1` or `--all` to compare.

### Custom Judge Functions

For problems with multiple valid answers:

```python
def judge(actual, expected, input_data: str) -> bool:
    """Custom validation logic."""
    # Return True if actual is valid
    return is_valid(actual)

JUDGE_FUNC = judge
```

Or use simple comparison modes:
```python
COMPARE_MODE = "sorted"  # Options: "exact" | "sorted" | "set"
```

### Random Test Generator

Create `generators/XXXX_problem_name.py`:

```python
import random
from typing import Iterator, Optional

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    if seed is not None:
        random.seed(seed)

    for _ in range(count):
        # Generate test case
        yield f"{json.dumps(param1)}\n{json.dumps(param2)}"

def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n for complexity estimation."""
    return generate_case_of_size(n)
```

## VS Code Integration

- `Ctrl+Shift+B` - Run all tests for current file
- `F5` - Debug with test case #1
- Tasks available via `Ctrl+Shift+P` → "Tasks: Run Task"

## Documentation

Key documentation files:
- `docs/contracts/solution-contract.md` - Solution file specification
- `docs/contracts/test-file-format.md` - Test file format
- `docs/contracts/generator-contract.md` - Generator specification
- `docs/runner/README.md` - Test runner reference
- `docs/packages/codegen/README.md` - CodeGen reference

## Python Environment

- Python 3.11 (matching LeetCode official environment)
- Virtual environment: `leetcode/`
- Activate: `leetcode\Scripts\activate` (Windows) or `source leetcode/bin/activate` (Linux/macOS)

## Naming Conventions

- Problem files: `XXXX_problem_name.py` (4-digit zero-padded LeetCode ID)
- Test files: `XXXX_problem_name_N.in/.out` (N = case number starting from 1)
- Documentation: kebab-case for markdown files

## Important Notes

1. Always use `json.dumps(result, separators=(',', ':'))` for output (no spaces)
2. Test files must end with a single newline
3. Use LF line endings, not CRLF
4. The `_runner.py` module provides `get_solver()` for polymorphic dispatch
5. Complexity in SOLUTIONS is declared metadata; use `--estimate` for empirical verification

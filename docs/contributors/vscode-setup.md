# VSCode Setup Guide

> **Status**: Informational  
> **Scope**: VSCode tasks and debug configurations  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

This guide covers the pre-configured VSCode tasks and debug configurations for running and debugging LeetCode solutions.

---

## Prerequisites

1. **Virtual environment**: `leetcode/` must exist (see [Virtual Environment Setup](virtual-env-setup.md))
2. **Python extension**: Install [Python extension for VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
3. **debugpy**: Install via `pip install debugpy`

---

## Quick Start

1. Open a solution file (e.g., `solutions/0001_two_sum.py`)
2. Press `Ctrl+Shift+B` to run all tests
3. Press `F5` to debug with breakpoints

> 💡 Tasks and debug configs auto-detect problem name from the current file.

---

## Tasks (Ctrl+Shift+B)

Run via **Terminal → Run Build Task** or `Ctrl+Shift+B`.

### How to Run Tasks

1. Press `Ctrl+Shift+B` (runs default task), or
2. Press `Ctrl+Shift+P` → type "Run Task" → select a task

### Available Tasks

#### Basic Testing

| Task | Description | CLI Equivalent |
|------|-------------|----------------|
| ⭐ **Run all tests for current problem** | Default build task | `python runner/test_runner.py {problem}` |
| Run case #1 for current problem | Run first test case only | `python runner/case_runner.py {problem} 1` |
| Run case #2 for current problem | Run second test case only | `python runner/case_runner.py {problem} 2` |
| Run case (prompt for number) | Prompts for case number | `python runner/case_runner.py {problem} {N}` |

#### Benchmarking

| Task | Description | CLI Equivalent |
|------|-------------|----------------|
| Benchmark current problem | Show timing for each case | `--benchmark` |
| Run all solutions with benchmark | Compare all solution methods | `--all --benchmark` |

#### Test Generation

| Task | Description | CLI Equivalent |
|------|-------------|----------------|
| Run with generated cases (10) | Static + 10 generated | `--generate 10 --benchmark` |
| Run generated only (prompt for count) | Skip static, generate N | `--generate-only {N} --benchmark` |
| Run generated with seed (reproducible) | Reproducible generation | `--generate {N} --seed {S} --benchmark` |
| Run generated + save failed | Save failing inputs | `--generate {N} --save-failed --benchmark` |

#### Combined Operations

| Task | Description | CLI Equivalent |
|------|-------------|----------------|
| Run all solutions + generated | All methods with generation | `--all --benchmark --generate {N}` |
| Run all solutions + generated only | All methods, skip static | `--all --benchmark --generate-only {N}` |

#### Complexity Estimation

| Task | Description | CLI Equivalent |
|------|-------------|----------------|
| Estimate complexity | Estimate Big-O | `--estimate` |
| Run all + benchmark + estimate | Full analysis | `--all --benchmark --estimate` |

### Input Prompts

Some tasks prompt for input:

| Prompt | Description | Default |
|--------|-------------|---------|
| Case number | Test case number (1, 2, 3...) | `1` |
| Generate count | Number of cases to generate | `10` |
| Seed number | Random seed for reproducibility | `12345` |

---

## Debug Configurations (F5)

Run via **Run and Debug** panel (`Ctrl+Shift+D`) or press `F5`.

### How to Debug

1. Open a solution file
2. Set breakpoints (click left of line numbers)
3. Press `F5` or select a configuration from the dropdown
4. Use debug controls: Step Over (F10), Step Into (F11), Continue (F5)

### Available Configurations

#### Single Case Debugging

| Configuration | Description | Use Case |
|---------------|-------------|----------|
| Debug current problem (case #1) | Debug with first test case | Quick debugging |
| Debug current problem (case #2) | Debug with second test case | Test edge cases |
| Debug current problem (case #3) | Debug with third test case | Additional cases |
| Debug solution directly (no stdin) | Run current file directly | Manual testing |

#### Full Test Suite Debugging

| Configuration | Description | Use Case |
|---------------|-------------|----------|
| Debug all tests | Debug all static tests | Find failing case |
| Benchmark current problem | Debug with timing | Performance issues |
| Benchmark current problem all solutions | Debug all methods | Compare implementations |

#### Generated Test Debugging

| Configuration | Description | Use Case |
|---------------|-------------|----------|
| Debug with generated cases (10) | Static + 10 generated | Stress testing |
| Debug generated only (10) | 10 generated only | Random testing |
| Debug generated with seed | Reproducible (seed: 12345) | Reproduce failures |
| Debug all solutions + generated (10) | All methods + generated | Full comparison |

---

## Workflow Examples

### Example 1: Basic Development Cycle

```
1. Open solutions/0001_two_sum.py
2. Press Ctrl+Shift+B → runs all tests
3. If test fails:
   - Set breakpoint in solution
   - Press F5 → select "Debug current problem (case #1)"
   - Step through code to find bug
```

### Example 2: Multi-Solution Comparison

```
1. Open solutions/0023_merge_k_sorted_lists.py
2. Ctrl+Shift+P → "Run Task" → "Run all solutions with benchmark"
3. Compare timing across heap, divide, greedy methods
```

### Example 3: Stress Testing

```
1. Open solution file
2. Ctrl+Shift+P → "Run Task" → "Run generated + save failed"
3. Enter count: 100
4. If failure found:
   - Check tests/{problem}_failed_1.in
   - Debug with that specific input
```

### Example 4: Reproduce a Failure

```
1. Note the seed from failure output
2. Ctrl+Shift+P → "Run Task" → "Run generated with seed"
3. Enter count and seed
4. Set breakpoints and debug
```

---

## Customization

### Adding Custom Tasks

Edit `.vscode/tasks.json`:

```json
{
    "label": "My custom task",
    "type": "shell",
    "command": "${workspaceFolder}/leetcode/Scripts/python.exe",
    "args": [
        "runner/test_runner.py",
        "${fileBasenameNoExtension}",
        "--method",
        "heap"
    ],
    "options": {
        "cwd": "${workspaceFolder}"
    }
}
```

### Adding Custom Debug Configurations

Edit `.vscode/launch.json`:

```json
{
    "name": "Debug specific method",
    "type": "debugpy",
    "request": "launch",
    "program": "${workspaceFolder}/runner/test_runner.py",
    "args": [
        "${fileBasenameNoExtension}",
        "--method",
        "heap"
    ],
    "python": "${workspaceFolder}/leetcode/Scripts/python.exe",
    "console": "integratedTerminal",
    "cwd": "${workspaceFolder}"
}
```

### VSCode Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `${fileBasenameNoExtension}` | Current file name without extension | `0001_two_sum` |
| `${file}` | Full path to current file | `C:\...\solutions\0001_two_sum.py` |
| `${workspaceFolder}` | Workspace root | `C:\Developer\...\neetcode` |

---

## Troubleshooting

### Task Not Running

**Symptom**: Task fails with Python not found

**Fix**: Ensure virtual environment exists:
```bash
python -m venv leetcode
```

### Debug Not Starting

**Symptom**: F5 does nothing or shows error

**Fix**: 
1. Install debugpy: `pip install debugpy`
2. Ensure Python extension is installed
3. Check `.vscode/launch.json` Python path

### Wrong Problem Detected

**Symptom**: Task runs wrong problem

**Fix**: Ensure the solution file is the active editor tab (not a test file or other file).

### Path Issues on Linux/macOS

**Symptom**: Python path not found

**Fix**: The configs include platform-specific paths:
- Windows: `leetcode/Scripts/python.exe`
- Linux/macOS: `leetcode/bin/python`

---

## Related Documentation

| Document | Content |
|----------|---------|
| [Virtual Environment Setup](virtual-env-setup.md) | Python environment setup |
| [Test Runner Specification](https://github.com/lufftw/neetcode/blob/main/runner/README.md) | CLI options and usage |
| [Testing Guide](testing.md) | Unit testing framework |

---

**Maintainer**: See [Contributors](README.md)


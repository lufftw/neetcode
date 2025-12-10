# 🧩 NeetCode / LeetCode Practice Framework

**Language / 語言**: [English](README.md) | [繁體中文](README_zh-TW.md)

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![VS Code](https://img.shields.io/badge/VS%20Code-Integration-007ACC.svg)](https://code.visualstudio.com/)

A **high-performance Python LeetCode / algorithm practice framework** with reproducible random test generation, automated validation via custom `JUDGE_FUNC`, multi-solution benchmarking, and full VS Code debugging workflow integration. Designed for **competitive programming**, **algorithm engineering**, and **large-scale stress testing**.

> 🚀 **Key Features**: Automated test runner for algorithms | Reproducible random test generator | Judge-function validation (Codeforces/ICPC style) | Multi-solution benchmarking | VS Code debugger integration | Stress testing toolkit | Interactive mind maps for pattern visualization

---

## ⭐ Why This Framework is Different

Most LeetCode repos are just solution collections. **This framework is a complete testing infrastructure**:

| Feature | This Framework | Typical LeetCode Repos |
|---------|---------------|----------------------|
| **Reproducible Random Tests** | ✅ Seeded generators | ❌ Manual test cases only |
| **Custom Judge Function** | ✅ Codeforces/ICPC style validation | ❌ Exact string match only |
| **Multi-Solution Benchmarking** | ✅ Compare N solutions automatically | ❌ One solution per file |
| **VS Code Integration** | ✅ Tasks, debugging, shortcuts | ❌ Command line only |
| **Stress Testing** | ✅ Generate 1000+ test cases | ❌ Limited to manual cases |
| **Time Complexity Estimation** | ✅ Automatic Big-O analysis | ❌ Not available |

---

## ❓ Frequently Asked Questions

### What problems does this framework solve?

- Running multiple algorithm implementations automatically
- Generating large-scale reproducible test data for stress testing
- Benchmarking solutions to identify performance differences
- Debugging LeetCode-style problems with VS Code integration
- Validating outputs using custom logic beyond simple `.out` file comparison

### Who is this framework for?

- **Competitive programmers** preparing for contests (Codeforces, ICPC, etc.)
- **Software engineers** preparing for coding interviews (FAANG, etc.)
- **Students** taking data structures and algorithms courses
- **Researchers** needing large-scale algorithm stress tests

### How is this different from just copying LeetCode solutions?

This is not a solution collection — it's a **testing infrastructure**. You write solutions, and the framework:

1. Runs them against static test cases
2. Generates random test cases automatically
3. Validates correctness using custom judge functions
4. Benchmarks multiple solutions against each other
5. Estimates time complexity empirically

### Can I use this for interview preparation?

Yes! The framework is perfect for interview prep because:

- You can practice writing solutions in **real LeetCode format**
- The random test generator helps you find **edge cases you might miss**
- Multi-solution benchmarking shows which approach is **actually faster**
- VS Code integration makes **debugging easy**

---

## 🧠 Interactive Mind Maps

Visualize algorithm patterns, problem relationships, and learning paths with interactive mind maps powered by [Markmap](https://markmap.js.org/).

Explore our algorithm patterns visually:

| Mind Map | Description | Links |
|----------|-------------|-------|
| 📐 Pattern Hierarchy | API Kernels → Patterns → Problems hierarchy | [Static](docs/mindmaps/pattern_hierarchy.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#pattern-hierarchy) |
| 👨‍👩‍👧‍👦 Family Derivation | Base templates and derived problem variants | [Static](docs/mindmaps/family_derivation.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#family-derivation) |
| ⚡ Algorithm Usage | Problems organized by algorithms they use | [Static](docs/mindmaps/algorithm_usage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#algorithm-usage) |
| 🏗️ Data Structure Usage | Problems organized by data structures | [Static](docs/mindmaps/data_structure.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#data-structure-usage) |
| 🏢 Company Coverage | Problems frequently asked by companies | [Static](docs/mindmaps/company_coverage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#company-coverage) |
| 🗺️ Learning Roadmaps | Curated problem sequences (NeetCode 150, Blind 75, etc.) | [Static](docs/mindmaps/roadmap_paths.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#learning-roadmaps) |
| 🔗 Problem Relations | Related problems network | [Static](docs/mindmaps/problem_relations.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#problem-relations) |
| 🔀 Solution Variants | Problems with multiple solution approaches | [Static](docs/mindmaps/solution_variants.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#solution-variants) |
| 📊 Difficulty × Topics | Topics organized by difficulty level | [Static](docs/mindmaps/difficulty_topics.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#difficulty-topics) |

👉 **[View All Interactive Mind Maps](https://lufftw.github.io/neetcode/mindmaps/)**

---

## 📑 Table of Contents

- [Why This Framework is Different](#-why-this-framework-is-different)

- [Frequently Asked Questions](#-frequently-asked-questions)

- [Interactive Mind Maps](#-interactive-mind-maps)

- [Project Structure](#-project-structure)

- [Quick Start](#-quick-start)
  - [Environment Setup](#1-environment-setup-first-time)
  - [Daily Usage](#2-daily-usage-activate-environment)
  - [Create New Problem](#3-create-new-problem)
  - [Run Tests](#4-run-tests)

- [VS Code Integration](#️-vs-code-integration)
  - [Quick Shortcuts](#quick-shortcuts)
  - [Tasks](#tasks-ctrlshiftp--tasks-run-task)
  - [Debug Configurations](#debug-configurations-f5--select)

- [Solution File Format](#-solution-file-format)

- [Test File Format](#-test-file-format)

- [Command Line Usage](#-command-line-usage)

- [Multi-Solution Testing](#-multi-solution-testing--performance-comparison)
  - [Command Line Parameters](#command-line-parameters)
  - [Define Multiple Solutions](#how-to-define-multiple-solutions)
  - [SOLUTIONS Field Description](#solutions-field-description)
  - [Custom Short Names](#custom-short-names)
  - [Wrapper-Based Pattern](#advanced-wrapper-based-pattern-for-multiple-solution-classes)

- [Flexible Output Comparison](#-flexible-output-comparison)
  - [Validation Modes](#validation-modes)
  - [JUDGE_FUNC](#approach-1-judge_func-recommended-for-complex-cases)
  - [COMPARE_MODE](#approach-2-compare_mode-simple-cases)
  - [JUDGE_FUNC Examples](#judge_func-examples)
  - [Applicable Problems](#applicable-problems)

- [Test Case Generator](#-test-case-generator)

- [Time Complexity Estimation](#-time-complexity-estimation)

- [Test Result Example](#-test-result-example)

- [Python Environment](#-python-environment)

- [Tips](#-tips)

- [Generate Mind Maps Locally](#️-generate-mind-maps-locally)

- [Maintainer Zone](#-maintainer-zone-unit-tests)

- [Runner Module Architecture](#️-runner-module-architecture-for-developers)

- [License](#-license)

---

## 📁 Project Structure

```
neetcode/
│
├── .vscode/                 ← VS Code integration
│   ├── settings.json        ← Python environment settings
│   ├── tasks.json           ← Ctrl+Shift+B shortcuts
│   └── launch.json          ← F5 Debug configuration
│
├── runner/                  ← Test runner modules
│   ├── test_runner.py       ← CLI entry point
│   ├── module_loader.py     ← Load solution/generator modules
│   ├── executor.py          ← Run test cases
│   ├── reporter.py          ← Format and display results
│   ├── compare.py           ← Output comparison logic
│   ├── paths.py             ← Path utilities
│   ├── io_utils.py          ← File I/O operations
│   ├── util.py              ← Re-exports (backward compatible)
│   ├── complexity_estimator.py  ← Time complexity estimation
│   └── case_runner.py       ← Run single case (debugging)
│
├── solutions/               ← Solution files for each problem
│   └── 0001_two_sum.py
│
├── tests/                   ← All test cases
│   ├── 0001_two_sum_1.in
│   ├── 0001_two_sum_1.out
│   ├── *_failed_*.in        ← Auto-saved failed generated cases (with --save-failed)
│   └── ...
│
├── generators/              ← Test case generators (optional)
│   └── 0001_two_sum.py      ← Generate random test cases
│
├── templates/               ← Templates for new problems
│   ├── template_solution.py         ← Single solution template
│   ├── template_solution_multi.py   ← Multi-solution (one class)
│   ├── template_solution_wrapper.py ← Multi-solution (wrapper pattern)
│   └── template_test.txt
│
├── .dev/                    ⚠️ Maintainer Zone - Unit tests and dev docs
│   ├── tests/               ← Unit test suite (150+ test cases)
│   │   ├── test_util.py            ← Tests for runner/util.py
│   │   ├── test_case_runner.py     ← Tests for runner/case_runner.py
│   │   ├── test_test_runner.py     ← Tests for runner/test_runner.py
│   │   ├── test_complexity_estimator.py  ← Complexity estimator tests
│   │   ├── test_edge_cases.py      ← Edge case tests
│   │   ├── test_integration.py     ← End-to-end integration tests
│   │   └── README.md               ← Test documentation
│   │
│   ├── run_tests.bat        ← Windows: Run unit tests
│   ├── run_tests.sh         ← Linux/macOS: Run unit tests
│   │
│   ├── TESTING.md           ← Complete testing documentation
│   ├── TEST_SUMMARY.md      ← Test suite summary
│   └── README.md            ← Maintainer guide
│
├── tools/                   ← Documentation and generation tools
│   ├── generate_mindmaps.py  ← Generate interactive mind maps
│   ├── generate_mindmaps.toml ← Mind maps configuration
│   ├── generate_pattern_docs.py ← Generate pattern documentation
│   ├── text_to_mindmap.py   ← Convert text to mind maps (LLM)
│   └── README.md            ← Tools documentation
│
├── docs/                    ← Documentation (MkDocs)
│   ├── mindmaps/            ← Generated mind map markdown files
│   │   ├── pattern_hierarchy.md
│   │   ├── algorithm_usage.md
│   │   └── ...
│   ├── patterns/            ← Generated pattern documentation
│   │   └── sliding_window.md
│   ├── pages/               ← Generated HTML for GitHub Pages (gitignored)
│   │   └── mindmaps/        ← Interactive HTML mind maps
│   ├── stylesheets/         ← Custom CSS
│   ├── index.md             ← Homepage (English)
│   ├── index_zh-TW.md       ← Homepage (Traditional Chinese)
│   └── GITHUB_PAGES_SETUP.md ← GitHub Pages setup guide
│
├── ontology/                ← Algorithm ontology definitions
│   ├── api_kernels.toml     ← API kernel definitions
│   ├── patterns.toml         ← Pattern definitions
│   ├── algorithms.toml      ← Algorithm definitions
│   ├── data_structures.toml ← Data structure definitions
│   ├── companies.toml       ← Company definitions
│   ├── topics.toml          ← Topic definitions
│   ├── difficulties.toml    ← Difficulty definitions
│   ├── families.toml        ← Problem family definitions
│   └── roadmaps.toml         ← Roadmap definitions
│
├── meta/                    ← Problem and pattern metadata
│   ├── problems/            ← Problem metadata (TOML)
│   │   └── *.toml           ← One file per problem
│   └── patterns/            ← Pattern documentation sources
│       └── <pattern_name>/  ← Pattern-specific markdown files
│           ├── _header.md   ← Core concepts
│           ├── _comparison.md ← Pattern comparison
│           ├── _decision.md ← When to use
│           ├── _templates.md ← Quick reference
│           └── *.md         ← Problem-specific content
│
├── roadmaps/                ← Learning roadmap definitions
│   ├── neetcode_150.toml
│   ├── blind_75.toml
│   └── sliding_window_path.toml
│
├── .github/                 ← GitHub configuration
│   └── workflows/
│       └── deploy-pages.yml ← GitHub Pages deployment
│
├── leetcode/                ← Python virtual environment (Python 3.11)
│
├── mkdocs.yml               ← MkDocs configuration
├── pytest.ini               ← pytest configuration (for unit tests)
│
├── run_tests.bat            ← Windows: Run all tests
├── run_case.bat             ← Windows: Run single test
├── new_problem.bat          ← Windows: Create new problem
│
├── run_tests.sh             ← Linux/macOS: Run all tests
├── run_case.sh              ← Linux/macOS: Run single test
├── new_problem.sh           ← Linux/macOS: Create new problem
│
├── requirements.txt         ← Python dependencies
├── README.md                ← Main documentation (English)
└── README_zh-TW.md          ← Main documentation (Traditional Chinese)
```

> **📝 Note**: 
> - **End users**: Focus on `solutions/`, `tests/`, `runner/` and root-level scripts
> - **Maintainers**: `.dev/` folder contains unit tests and maintenance docs to ensure refactoring doesn't break existing functionality
> - **Documentation**: 
>   - `docs/mindmaps/*.md` - Auto-generated by `tools/generate_mindmaps.py`
>   - `docs/patterns/*.md` - Auto-generated by `tools/generate_pattern_docs.py`
>   - `docs/pages/` - Generated HTML files (gitignored, regenerated on deploy)
>   - `ontology/` and `meta/` - Source data for documentation generation

---

## 🚀 Quick Start

### 1. Environment Setup (First Time)

> Reference: [LeetCode Official Environment](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages)

#### Windows (PowerShell)

> **Prerequisite**: To use `py install` command, you need to install **Python Install Manager** from the [Python official website](https://www.python.org/downloads/) first.

```powershell
# Navigate to project directory
cd /d "D:\Developer\program\python\neetcode"

# Install Python 3.11 (if not already installed)
# Note: Requires Python Install Manager from https://www.python.org/downloads/
py install 3.11

# Create virtual environment
py -3.11 -m venv leetcode

# Activate virtual environment
leetcode\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Linux / macOS (Using pyenv - Recommended)

> **Why pyenv?** Installs Python in user directory without affecting system Python. Supports multiple versions.

```bash
# ============================================
# Step 1: Install pyenv (one-time setup)
# ============================================

# --- macOS ---
brew install pyenv

# --- Linux (Ubuntu/Debian/Fedora/etc.) ---
# Install dependencies first:
sudo apt update && sudo apt install -y build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev curl \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Install pyenv:
curl https://pyenv.run | bash

# ============================================
# Step 2: Configure shell (add to ~/.bashrc or ~/.zshrc)
# ============================================
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Reload shell
source ~/.bashrc   # or: source ~/.zshrc

# ============================================
# Step 3: Install Python 3.11 and setup project
# ============================================
# Navigate to project directory
cd ~/path/to/neetcode

# Install Python 3.11 (doesn't affect system Python)
pyenv install 3.11

# Set Python 3.11 for this project only
pyenv local 3.11

# Create virtual environment
python -m venv leetcode

# Activate virtual environment
source leetcode/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make shell scripts executable (first time only)
chmod +x run_tests.sh run_case.sh new_problem.sh
```

<details>
<summary>📋 Alternative: Direct system install (may affect existing Python)</summary>

```bash
# Ubuntu/Debian:
sudo apt update && sudo apt install python3.11 python3.11-venv

# macOS (Homebrew):
brew install python@3.11

# Then create venv:
python3.11 -m venv leetcode
```

</details>

### 2. Daily Usage (Activate Environment)

#### Windows

```powershell
cd /d "D:\Developer\program\python\neetcode"
leetcode\Scripts\activate
```

#### Linux / macOS

```bash
cd ~/path/to/neetcode
source leetcode/bin/activate
```

### 3. Create New Problem

#### Windows

```batch
# Single solution template
new_problem.bat 0007_reverse_integer

# Multi-solution template (one class, multiple methods)
new_problem.bat 0023_merge_k_lists --multi

# Wrapper-based template (multiple classes, preserves LeetCode method names)
new_problem.bat 0025_reverse_nodes --wrapper
```

#### Linux / macOS

```bash
# Single solution template
./new_problem.sh 0007_reverse_integer

# Multi-solution template (one class, multiple methods)
./new_problem.sh 0023_merge_k_lists --multi

# Wrapper-based template (multiple classes, preserves LeetCode method names)
./new_problem.sh 0025_reverse_nodes --wrapper
```

This will create:
- `solutions/0007_reverse_integer.py`
- `tests/0007_reverse_integer_1.in`
- `tests/0007_reverse_integer_1.out`

### 4. Run Tests

#### Windows

```batch
# Run all test cases
run_tests.bat 0001_two_sum

# Run single test case
run_case.bat 0001_two_sum 1
```

#### Linux / macOS

```bash
# Run all test cases
./run_tests.sh 0001_two_sum

# Run single test case
./run_case.sh 0001_two_sum 1
```

---

## ⌨️ VS Code Integration

### Quick Shortcuts

| Shortcut | Function |
|----------|----------|
| `Ctrl+Shift+B` | Run all tests for current file |
| `F5` | Debug current file with case #1 |

> **Note**: Open a solution file in `solutions/` before using shortcuts.

### Tasks (Ctrl+Shift+P → "Tasks: Run Task")

| Task | Description |
|------|-------------|
| Run all tests for current problem | Basic test run |
| Run case #1 / #2 | Run specific test case |
| Benchmark current problem | Show execution time |
| Run all solutions with benchmark | Compare all solutions |
| Run with generated cases (10) | Static + 10 generated |
| Run generated only | Skip static tests |
| Run generated with seed | Reproducible generation |
| Run generated + save failed | Save failed inputs |
| Run all solutions + generated | All solutions with generator |

### Debug Configurations (F5 → Select)

| Configuration | Description |
|---------------|-------------|
| Debug current problem (case #1/2/3) | Debug specific test case |
| Debug all tests | Debug full test suite |
| Benchmark current problem | Run with timing |
| Debug with generated cases | Static + generated |
| Debug generated only | Only generated cases |
| Debug generated with seed | Reproducible debug |
| Debug all solutions + generated | Compare all with generator |

> 💡 **Tip**: These tasks/configs run the same commands documented in [Command Line Usage](#-command-line-usage) and [Test Case Generator](#-test-case-generator).
> 
> Example: "Benchmark current problem" runs `python runner/test_runner.py {problem} --benchmark`

---

## 📝 Solution File Format

```python
# solutions/0001_two_sum.py
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Your solution
        pass

def solve():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    # Parse input
    nums = list(map(int, lines[0].split(',')))
    target = int(lines[1])
    
    sol = Solution()
    result = sol.twoSum(nums, target)
    
    # Print result
    print(result)

if __name__ == "__main__":
    solve()
```

---

## 📋 Test File Format

### Specifications

| Item | Requirement |
|------|-------------|
| Line Ending | **LF** (Unix/Linux format, `\n`) |
| Encoding | UTF-8 |
| File Ending | Must end with single newline |
| Naming | `{problem_number}_{problem_name}_{case_number}.in/.out` |

### Input File (`.in`)
```
2,7,11,15
9

```

### Output File (`.out`)
```
[0, 1]

```

---

## 🔧 Command Line Usage

```bash
# Run all test cases
python runner/test_runner.py <problem_name>

# Run single test case
python runner/case_runner.py <problem_name> <case_index>
```

### Examples

```bash
python runner/test_runner.py 0001_two_sum
python runner/case_runner.py 0001_two_sum 1
```

---

## 🚀 Multi-Solution Testing & Performance Comparison

Test multiple solutions and compare performance for the same problem.

### Command Line Parameters

```bash
# Run default solution
python runner/test_runner.py 0023_merge_k_sorted_lists

# Run specific solution
python runner/test_runner.py 0023_merge_k_sorted_lists --method heap
python runner/test_runner.py 0023_merge_k_sorted_lists --method greedy

# Run all solutions
python runner/test_runner.py 0023_merge_k_sorted_lists --all

# Run all solutions + performance comparison
python runner/test_runner.py 0023_merge_k_sorted_lists --all --benchmark
```

### How to Define Multiple Solutions

Add a `SOLUTIONS` dictionary in your solution file:

```python
# solutions/0023_merge_k_sorted_lists.py

SOLUTIONS = {
    "default": {
        "method": "mergeKListsPriorityQueue",   # Name of the method in Solution class
        "complexity": "O(N log k)",             # Time complexity
        "description": "Priority Queue approach"
    },
    "heap": {
        "method": "mergeKListsPriorityQueue",
        "complexity": "O(N log k)",
        "description": "Priority Queue (Min Heap)"
    },
    "divide": {
        "method": "mergeKListsDivideConquer",
        "complexity": "O(N log k)",
        "description": "Divide and Conquer"
    },
    "greedy": {
        "method": "mergeKListsGreedy",
        "complexity": "O(kN)",
        "description": "Greedy comparison"
    },
}

class Solution:
    def mergeKListsPriorityQueue(self, lists):
        # Heap solution...
        pass

    def mergeKListsDivideConquer(self, lists):
        # Divide & Conquer solution...
        pass

    def mergeKListsGreedy(self, lists):
        # Greedy solution...
        pass

def solve():
    import os
    # Get solution method from environment variable
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    method_info = SOLUTIONS.get(method_name, SOLUTIONS['default'])
    method_func_name = method_info['method']
    
    sol = Solution()
    method_func = getattr(sol, method_func_name)
    result = method_func(...)
    print(result)
```

### SOLUTIONS Field Description

| Field | Description | Required |
|-------|-------------|----------|
| `method` | Method name in Solution class | ✅ |
| `complexity` | Time complexity (for display) | ❌ |
| `description` | Solution description | ❌ |

### Custom Short Names

The **key** in `SOLUTIONS` is the short name used in command line:

```python
SOLUTIONS = {
    "default": {"method": "solve_optimal", ...},     # Default solution
    "heap": {"method": "solve_heap", ...},           # --method heap
    "h": {"method": "solve_heap", ...},              # --method h (alias)
    "pq": {"method": "solve_priority_queue", ...},   # --method pq
    "bf": {"method": "solve_bruteforce", ...},       # --method bf
}
```

> **Note**: 
> - `default` is used when `--method` is not specified
> - Time complexity must be annotated by user; system only measures actual execution time

### Advanced: Wrapper-Based Pattern for Multiple Solution Classes

When implementing multiple approaches (e.g., recursive vs iterative), you may encounter:
- Method name conflicts inside one class
- Having to rename methods away from their original LeetCode signatures

**Solution**: Use separate Solution classes with wrapper functions.

```python
# solutions/0025_reverse_nodes_in_k_group.py

# ============================================
# Solution 1: Recursive approach
# ============================================
class SolutionRecursive:
    def reverseKGroup(self, head, k):
        # Recursive implementation...
        pass

# ============================================
# Solution 2: Iterative approach  
# ============================================
class SolutionIterative:
    def reverseKGroup(self, head, k):
        # Iterative implementation...
        pass

# ============================================
# Wrapper functions for test_runner integration
# ============================================
def solve_recursive(head, k):
    """Wrapper for SolutionRecursive."""
    return SolutionRecursive().reverseKGroup(head, k)

def solve_iterative(head, k):
    """Wrapper for SolutionIterative."""
    return SolutionIterative().reverseKGroup(head, k)

# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "method": "solve_iterative",
        "complexity": "O(N) time, O(1) space",
        "description": "Iterative in-place reversal"
    },
    "recursive": {
        "method": "solve_recursive",
        "complexity": "O(N) time, O(N) space",
        "description": "Recursive reversal with stack"
    },
    "iterative": {
        "method": "solve_iterative",
        "complexity": "O(N) time, O(1) space",
        "description": "Iterative in-place reversal"
    },
}

def solve():
    import os
    import sys
    
    # Get solution method from environment variable
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    method_info = SOLUTIONS.get(method_name, SOLUTIONS['default'])
    method_func_name = method_info['method']
    
    # Parse input
    lines = sys.stdin.read().strip().split('\n')
    # ... parse your input ...
    
    # Call wrapper function directly (not via class)
    method_func = globals()[method_func_name]
    result = method_func(head, k)
    
    print(result)
```

**Benefits of this pattern:**
- Each solution stays in its own class (`SolutionRecursive`, `SolutionIterative`)
- Preserve original LeetCode method names (e.g., `reverseKGroup`, `mergeKLists`)
- No method name collisions inside a single class
- Scales nicely when a problem has more than two approaches

> **Tip**: Use `new_problem.bat <name> --wrapper` (Windows) or `./new_problem.sh <name> --wrapper` (Linux/macOS) to create a template with this pattern.

---

## 🔀 Flexible Output Comparison

Some LeetCode problems state **"You may return the answer in any order"** or have multiple valid answers. The test runner supports flexible validation with clear output labels.

### Validation Modes

| Label | Description | Requires `.out` |
|-------|-------------|-----------------|
| `[judge]` | JUDGE_FUNC with `.out` reference | ✅ |
| `[judge-only]` | JUDGE_FUNC without `.out` (pure validation) | ❌ |
| `[exact]` | Exact string match | ✅ |
| `[sorted]` | Sort lists before comparison | ✅ |
| `[set]` | Set comparison | ✅ |

### Priority

```
1. JUDGE_FUNC (custom validation) - highest priority
2. COMPARE_MODE (sorted/set comparison)
3. Exact string match (default)
```

### Test Output Example

```
============================================================
🧪 Testing: 0051_n_queens
⚖️  Judge: JUDGE_FUNC
============================================================

📌 Method: default

   0051_n_queens_1: ✅ PASS (88.33ms) [judge]
   0051_n_queens_2: ✅ PASS (92.15ms) [judge]
   0051_n_queens_3: ✅ PASS (156.20ms) [judge-only]

   Result: 3 / 3 cases passed.
```

---

### Approach 1: JUDGE_FUNC (Recommended for Complex Cases)

Use **Decision Problem** approach: verify the answer is **valid**, not just **identical**.

**Key Feature**: `.out` file is **optional** when `JUDGE_FUNC` is defined!

```python
# solutions/0051_n_queens.py

def judge(actual: list, expected, input_data: str) -> bool:
    """
    Custom validation function.
    
    Args:
        actual: Program output (parsed as Python object if possible)
        expected: Expected output, or None if .out file doesn't exist
        input_data: Input data (raw string)
    
    Returns:
        bool: Whether the answer is correct
    """
    n = int(input_data.strip())
    
    # Validate solution regardless of expected
    for board in actual:
        if not is_valid_n_queens(board, n):
            return False
    
    # Check count only if expected is provided
    if expected is not None:
        if len(actual) != len(expected):
            return False
    
    # Check no duplicates
    return len(set(tuple(b) for b in actual)) == len(actual)

JUDGE_FUNC = judge  # Tell test_runner to use this function
```

**Benefits:**
- Validates correctness, not just string equality
- Handles multiple valid answers
- **`.out` file optional** - supports judge-only mode for custom test cases
- Works with any output format (strings, objects, custom formats)

**Use Cases for Judge-Only Mode (no `.out`):**
- Custom large test cases you generate
- Stress testing with random inputs
- Cases where computing expected output is complex

---

### Approach 2: COMPARE_MODE (Simple Cases)

For simple order-independent comparisons (requires `.out` file):

```python
# solutions/0046_permutations.py

COMPARE_MODE = "sorted"  # Options: "exact" | "sorted" | "set"
```

| Mode | Description | Use Case |
|------|-------------|----------|
| `"exact"` | Exact string match (default) | Most problems |
| `"sorted"` | Sort lists before comparison | Permutations, Combinations |
| `"set"` | Set comparison (ignores duplicates) | Unique elements |

---

### JUDGE_FUNC Examples

#### Example 1: N-Queens (with optional `.out`)

```python
def judge(actual: list, expected, input_data: str) -> bool:
    n = int(input_data.strip())
    
    # Always validate board correctness
    if not all(is_valid_board(b, n) for b in actual):
        return False
    
    # If .out exists, also check count
    if expected is not None:
        return len(actual) == len(expected)
    
    return True  # Judge-only mode: just validate

JUDGE_FUNC = judge
```

#### Example 2: LinkedList (String Mode)

```python
def judge(actual: str, expected: str, input_data: str) -> bool:
    # Parse "1->2->3" format
    def parse(s):
        return s.strip().split("->") if s.strip() else []
    return parse(actual) == parse(expected)

JUDGE_FUNC = judge
```

#### Example 3: Floating Point Tolerance

```python
def judge(actual: float, expected: float, input_data: str) -> bool:
    return abs(actual - expected) < 1e-5

JUDGE_FUNC = judge
```

#### Example 4: Pure Validation (Judge-Only)

```python
def judge(actual: list, expected, input_data: str) -> bool:
    """Validate without expected output."""
    # expected is None when .out doesn't exist
    params = parse_input(input_data)
    return is_valid_solution(actual, params)

JUDGE_FUNC = judge
```

---

### Applicable Problems

| Problem | Recommended Approach | `.out` Required |
|---------|---------------------|-----------------|
| N-Queens | `JUDGE_FUNC` (validate board) | Optional |
| Permutations | `COMPARE_MODE = "sorted"` | ✅ |
| Subsets | `COMPARE_MODE = "sorted"` | ✅ |
| Shortest Path (multiple) | `JUDGE_FUNC` (validate path) | Optional |
| Floating point | `JUDGE_FUNC` (tolerance) | ✅ |
| LinkedList/Tree | `JUDGE_FUNC` (parse format) | ✅ |
| Custom stress tests | `JUDGE_FUNC` (judge-only) | ❌ |

---

## 🎲 Test Case Generator

Automatically generate test cases to stress-test your solutions.

### Setup

Create a generator file in `generators/` with the same name as your solution:

```
generators/
└── 0004_median_of_two_sorted_arrays.py
```

### Generator Template

```python
# generators/0004_median_of_two_sorted_arrays.py
"""
LeetCode Constraints:
- 0 <= m, n <= 1000
- 1 <= m + n <= 2000
- -10^6 <= nums1[i], nums2[i] <= 10^6
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
    
    Yields:
        str: Test input (same format as .in files)
    """
    # Constraints
    min_m, max_m = 0, 1000
    min_n, max_n = 0, 1000
    min_val, max_val = -10**6, 10**6
    
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    yield "[]\n[1]"
    yield "[1]\n[]"
    count -= 2
    
    # Random cases
    for _ in range(count):
        m = random.randint(min_m, max_m)
        n = random.randint(min_n, max_n)
        nums1 = sorted([random.randint(min_val, max_val) for _ in range(m)])
        nums2 = sorted([random.randint(min_val, max_val) for _ in range(n)])
        yield f"{nums1}\n{nums2}".replace(' ', '')
```

### Usage

```bash
# Run tests/ + 10 generated cases
python runner/test_runner.py 0004_median --generate 10

# Only run generated cases (skip tests/)
python runner/test_runner.py 0004_median --generate-only 10

# Use seed for reproducibility
python runner/test_runner.py 0004_median --generate 10 --seed 12345

# Save failed cases for debugging
# Failed cases will be saved to tests/ as {problem}_failed_{n}.in
python runner/test_runner.py 0004_median --generate 10 --save-failed
```

### Output Example

```
============================================================
🧪 Testing: 0004_median_of_two_sorted_arrays
⚖️  Judge: JUDGE_FUNC
🎲 Generator: 10 cases, seed: 12345
============================================================

📌 Running default solution...

   --- tests/ (static) ---
   0004_median_1: ✅ PASS (12.33ms) [judge]
   0004_median_2: ✅ PASS (11.15ms) [judge]

   --- generators/ (10 cases, seed: 12345) ---
   gen_1: ✅ PASS (8.20ms) [generated]
   gen_2: ✅ PASS (7.15ms) [generated]
   gen_3: ❌ FAIL [generated]
      ┌─ Input ─────────────────────────────────
      │ [1,3,5,7,9]
      │ [2,4,6,8,10]
      ├─ Actual ────────────────────────────────
      │ 5.0
      └─────────────────────────────────────────
      💾 Saved to: tests/0004_median_failed_1.in
   ...

Summary: 11 / 12 cases passed.
   ├─ Static (tests/): 2/2
   └─ Generated: 9/10

💡 To reproduce: python runner/test_runner.py 0004_median --generate 10 --seed 12345
```

### Requirements

| Component | Required | Description |
|-----------|----------|-------------|
| `generators/{problem}.py` | Generator file | Must have `generate(count, seed)` function |
| `JUDGE_FUNC` in solution | ✅ | Generator cases have no `.out`, need judge |
| `tests/*.in` | Optional | Static tests run before generated |
| `tests/*_failed_*.in` | Auto-generated | Failed cases saved with `--save-failed` flag |

---

## 📈 Time Complexity Estimation

Automatically estimate algorithm time complexity using the big_O library approach.

### Design Philosophy

**Simple and generic** - Only requires one additional function in your generator:

| Function | Purpose | Required |
|----------|---------|----------|
| `generate(count, seed)` | Random test cases for functional testing | ✅ Required |
| `generate_for_complexity(n)` | Controlled size cases for complexity estimation | Optional |

The estimator uses **Mock stdin** approach internally:
- ✅ Generic - works with any solution that has `solve()` function
- ✅ No subprocess overhead
- ✅ Maintains stdin abstraction design

### Usage

```bash
# Estimate complexity (requires generate_for_complexity in generator)
python runner/test_runner.py 0004_median_of_two_sorted_arrays --estimate

# Combine with other flags
python runner/test_runner.py 0004 --all --benchmark --estimate
```

### Generator Example

```python
# generators/0004_median_of_two_sorted_arrays.py

# Required: Random test generation
def generate(count: int, seed: Optional[int] = None) -> Iterator[str]:
    """Random sizes - tests functional correctness"""
    for _ in range(count):
        m = random.randint(0, 1000)
        n = random.randint(0, 1000)
        yield _generate_case(m, n)


# Optional: Enable complexity estimation
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size.
    
    For this problem, n = total elements (m + n)
    """
    m = random.randint(0, n)
    return _generate_case(m, n - m)
```

### Output Example

```
📈 Running complexity estimation...
   Mode: Direct call (Mock stdin, no subprocess overhead)
   Sizes: [10, 20, 50, 100, 200, 500, 1000, 2000]
   n=   10: 0.0040ms (avg of 3 runs)
   n=  100: 0.0082ms (avg of 3 runs)
   n= 1000: 0.0685ms (avg of 3 runs)
   n= 2000: 0.1796ms (avg of 3 runs)

✅ Estimated: O(n log n)
   Confidence: 1.00
```

### Requirements

| Component | Required | Description |
|-----------|----------|-------------|
| `big-O` package | ✅ | `pip install big-O` |
| `generate_for_complexity(n)` | ✅ | Function that takes size `n` and returns test input |

### Suitable Problem Types

Not all problems are suitable for time complexity estimation. The estimation works best when:

| ✅ Suitable | ❌ Not Suitable |
|-------------|-----------------|
| Input size `n` can vary continuously (10, 100, 1000...) | Input size has hard constraints (e.g., n ≤ 9) |
| Execution time scales with input size | Execution time is dominated by fixed overhead |
| Linear, logarithmic, polynomial complexity | Factorial/exponential with small n limit |

**Examples:**

| Problem | Suitable? | Reason |
|---------|-----------|--------|
| Two Sum | ✅ | n can be 10 ~ 10000, O(n) scales clearly |
| Longest Substring | ✅ | String length can vary widely |
| Merge k Sorted Lists | ✅ | Total elements N can scale |
| N-Queens (0051) | ❌ | n ≤ 9 (factorial explosion), can't vary size meaningfully |
| Rotting Oranges (0994) | ❌ | Grid size limited, BFS time dominated by grid structure |
| Sudoku Solver | ❌ | Fixed 9x9 grid, backtracking complexity |

> **Tip**: Only add `generate_for_complexity(n)` to generators where `n` can meaningfully vary from small (10) to large (1000+).

### Backward Compatibility

- **Solution files**: No changes required (must have `solve()` function)
- **Existing generators**: Continue to work without changes
- **New feature**: Add `generate_for_complexity(n)` to enable estimation

---

## 📊 Test Result Example

```
============================================================
🧪 Testing: 0023_merge_k_sorted_lists
============================================================

📌 Method: default
   Complexity: O(N log k)
   Description: Priority Queue (Min Heap) approach

   0023_merge_k_sorted_lists_1: ✅ PASS (53.04ms)
   0023_merge_k_sorted_lists_2: ✅ PASS (43.11ms)
   0023_merge_k_sorted_lists_3: ✅ PASS (44.50ms)

   Result: 3 / 3 cases passed.

📌 Method: heap
   Complexity: O(N log k)
   Description: Priority Queue (Min Heap) approach

   0023_merge_k_sorted_lists_1: ✅ PASS (44.40ms)
   0023_merge_k_sorted_lists_2: ✅ PASS (43.89ms)
   0023_merge_k_sorted_lists_3: ✅ PASS (44.79ms)

   Result: 3 / 3 cases passed.

📌 Method: divide
   Complexity: O(N log k)
   Description: Divide and Conquer approach

   0023_merge_k_sorted_lists_1: ✅ PASS (44.02ms)
   0023_merge_k_sorted_lists_2: ✅ PASS (44.32ms)
   0023_merge_k_sorted_lists_3: ✅ PASS (45.11ms)

   Result: 3 / 3 cases passed.

📌 Method: greedy
   Complexity: O(kN)
   Description: Greedy comparison - compare all k heads each time

   0023_merge_k_sorted_lists_1: ✅ PASS (44.68ms)
   0023_merge_k_sorted_lists_2: ✅ PASS (45.00ms)
   0023_merge_k_sorted_lists_3: ✅ PASS (44.78ms)

   Result: 3 / 3 cases passed.

============================================================
📊 Performance Comparison
============================================================
Method               Avg Time     Complexity      Pass Rate
------------------------------------------------------------
default                 46.88ms   O(N log k)      3/3
heap                    44.36ms   O(N log k)      3/3
divide                  44.48ms   O(N log k)      3/3
greedy                  44.82ms   O(kN)           3/3
============================================================
```

---

## 🐍 Python Environment

- **Python Version**: 3.11 (matches [LeetCode Official Environment](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages))
- **Virtual Environment**: `leetcode/` (inside project)
- **Dependencies**: See `requirements.txt`

### Install Dependencies

```bash
# Activate virtual environment first, then:
pip install -r requirements.txt
```

| Package | Required | Description |
|---------|----------|-------------|
| `debugpy` | ✅ | Debug support for VS Code |
| `big-O` | Optional | Time complexity estimation |

### Activate Virtual Environment

#### Windows

```powershell
# PowerShell
.\leetcode\Scripts\Activate.ps1

# CMD
leetcode\Scripts\activate.bat
```

#### Linux / macOS

```bash
source leetcode/bin/activate
```

### Install New Packages

#### Windows

```powershell
# Activate virtual environment first, then install
leetcode\Scripts\activate
pip install <package_name>
```

#### Linux / macOS

```bash
# Activate virtual environment first, then install
source leetcode/bin/activate
pip install <package_name>
```

---

## 🔧 Maintainer Zone (Unit Tests)

> ⚠️ **For project maintainers and contributors** - End users can skip this section

The `.dev/` folder contains a complete **unit test suite** and maintenance documentation to ensure code refactoring doesn't break existing functionality.

### Test Statistics

- **Test Cases**: 150+
- **Test Coverage**: 80-100%
- **Test Types**: Unit tests, edge case tests, integration tests

### Quick Usage

```bash
# 1. Activate virtual environment
# Windows
leetcode\Scripts\activate

# Linux/Mac
source leetcode/bin/activate

# 2. Install test dependencies
pip install pytest pytest-cov

# 3. Run all unit tests
cd .dev
run_tests.bat          # Windows
./run_tests.sh         # Linux/Mac

# 4. Generate coverage report
cd ..
leetcode\Scripts\python.exe -m pytest .dev/tests --cov=runner --cov-report=html  # Windows
leetcode/bin/python -m pytest .dev/tests --cov=runner --cov-report=html  # Linux/Mac
```

### Documentation

- **[.dev/README.md](.dev/README.md)** - Maintainer guide
- **[.dev/TESTING.md](.dev/TESTING.md)** - Complete testing documentation
- **[.dev/TEST_SUMMARY.md](.dev/TEST_SUMMARY.md)** - Test suite summary

### Test Purpose

These tests ensure:
- ✅ Refactoring doesn't break existing functionality
- ✅ Given same input → always same output
- ✅ Edge cases (empty input, error input, large data) are covered

**Test Maintainer**: luffdev

---

## 💡 Tips

1. **Add more test cases**: Copy `.in/.out` files and change the number
   ```
   0001_two_sum_1.in → 0001_two_sum_2.in
   0001_two_sum_1.out → 0001_two_sum_2.out
   ```

2. **Debug specific test case**: Modify case number in `launch.json`

3. **Custom input format**: Define parsing logic in `solve()` function

---

## 🏗️ Runner Module Architecture (For Developers)

> ⚠️ **For contributors and maintainers** - End users can skip this section

The `runner/` directory contains modular components for test execution:

### Module Overview

```
runner/
├── test_runner.py         # CLI entry point and main orchestration
├── module_loader.py       # Dynamic loading of solution/generator modules
├── executor.py            # Test case execution (subprocess management)
├── reporter.py            # Result formatting and benchmark display
├── compare.py             # Output comparison logic (exact/sorted/set/judge)
├── paths.py               # Path helper utilities
├── io_utils.py            # File I/O operations
├── util.py                # Re-exports for backward compatibility
├── complexity_estimator.py # Time complexity estimation (big_O integration)
└── case_runner.py         # Single case runner for debugging
```

### Module Responsibilities

| Module | Lines | Responsibility |
|--------|-------|----------------|
| `compare.py` | ~190 | Output comparison: `normalize_output`, `compare_outputs`, `compare_result`, `_compare_sorted`, `_compare_set` |
| `paths.py` | ~30 | Path construction: `get_solution_path`, `get_test_input_path`, `get_test_output_path` |
| `io_utils.py` | ~45 | File operations: `read_file`, `write_file`, `file_exists`, `print_diff` |
| `module_loader.py` | ~65 | Dynamic import: `load_solution_module`, `load_generator_module` |
| `executor.py` | ~120 | Test execution: `run_one_case`, `run_generated_case` |
| `reporter.py` | ~160 | Output formatting: `truncate_input`, `format_validation_label`, `save_failed_case`, `print_benchmark_summary`, `run_method_tests` |
| `test_runner.py` | ~310 | CLI and orchestration: argument parsing, main flow |
| `complexity_estimator.py` | ~300 | Complexity estimation: `ComplexityEstimator`, Mock stdin approach |
| `case_runner.py` | ~60 | Single case debugging |

### Backward Compatibility

The refactored modules maintain full backward compatibility:

```python
# Old imports still work:
from runner.util import normalize_output, compare_result
from runner.test_runner import run_one_case, load_solution_module

# New direct imports (recommended for new code):
from runner.compare import normalize_output, compare_result
from runner.executor import run_one_case
from runner.module_loader import load_solution_module
```

### Dependency Graph

```
test_runner.py (CLI entry)
    ├── module_loader.py
    ├── executor.py ──────────┐
    ├── reporter.py ──────────┼──→ compare.py
    └── complexity_estimator.py

util.py (re-exports)
    ├── compare.py
    ├── paths.py
    └── io_utils.py
```

### Unit Tests

All modules are covered by characterization tests in `.dev/tests/`:

```bash
# Run all unit tests
leetcode\Scripts\python.exe -m pytest .dev/tests -v  # Windows
leetcode/bin/python -m pytest .dev/tests -v          # Linux/macOS
```

---

## 📜 License

MIT License - Free for personal learning


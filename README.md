# 🧩 NeetCode Practice Framework

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/lufftw/neetcode?style=for-the-badge&logo=github&color=gold)](https://github.com/lufftw/neetcode/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/lufftw/neetcode?style=for-the-badge&logo=github&color=silver)](https://github.com/lufftw/neetcode/network)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![VS Code](https://img.shields.io/badge/VS%20Code-Ready-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
[![Tests](https://img.shields.io/badge/Unit%20Tests-150+-success?style=flat-square&logo=pytest&logoColor=white)](.dev/tests/)
[![Mind Maps](https://img.shields.io/badge/Mind%20Maps-9%20Types-ff69b4?style=flat-square&logo=markmap&logoColor=white)](https://lufftw.github.io/neetcode/mindmaps/)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square&logo=git&logoColor=white)](https://github.com/lufftw/neetcode/pulls)

### 🎯 Stop Memorizing. Start Engineering.

*The algorithm practice framework that treats your code like production software.*

[📚 Documentation](https://lufftw.github.io/neetcode/) &nbsp;•&nbsp; [🧠 Interactive Mind Maps](https://lufftw.github.io/neetcode/mindmaps/) &nbsp;•&nbsp; [🚀 Quick Start](#-quick-start)

**Language / 語言**: [English](README.md) | [繁體中文](README_zh-TW.md)

</div>

---

## 🌟 What Sets Us Apart

> 💡 **"The difference between a good programmer and a great one isn't the algorithm they choose — it's how they prove it works."**

<table>
<tr>
<td width="60%">

### 📦 Other LeetCode Repos
❌ Copy solutions, hope they work  
❌ Manual test cases only  
❌ No way to compare approaches  
❌ Memorize patterns blindly  
❌ No systematic learning path  

</td>
<td width="40%">

### 🚀 This Framework
✅ **Prove** your solution is correct  
✅ Auto-generate 1000+ test cases  
✅ Benchmark N solutions side-by-side  
✅ **Visualize** patterns with mind maps  
✅ Structured roadmaps (NeetCode 150, Blind 75)  

</td>
</tr>
</table>

### 🧠 The Knowledge Graph Advantage

Most people practice algorithms in isolation. We built an **interconnected knowledge system**:

```
📐 Pattern Hierarchy    →  See how API kernels become patterns become solutions
👨‍👩‍👧‍👦 Family Derivation    →  Understand how problems evolve from base templates  
⚡ Algorithm Usage      →  Know which algorithm applies where
🏢 Company Coverage     →  Target your preparation for specific companies
🗺️ Learning Roadmaps    →  Follow proven paths (NeetCode 150, Blind 75, etc.)
```

**[→ Explore 9 Interactive Mind Maps](https://lufftw.github.io/neetcode/mindmaps/)**

### ⚙️ Industrial-Strength Testing

Built on principles from **Codeforces, ICPC, and Google's engineering practices**:

| Capability | What It Does | Why It Matters |
|:-----------|:-------------|:---------------|
| 🎲 **Random Test Generation** | Seeded generators for reproducibility | Find edge cases you never imagined |
| ⚖️ **Custom Judge Functions** | ICPC-style validation logic | Multiple correct answers? No problem |
| 📊 **Multi-Solution Benchmark** | Compare N approaches automatically | Know which is *actually* faster |
| 📈 **Complexity Estimation** | Empirical Big-O analysis | Verify your theoretical claims |
| 🔧 **VS Code Integration** | One-click debug, tasks, shortcuts | Debug algorithms like real software |

---

## 📑 Table of Contents

- [Why This Framework?](#-why-this-framework)
- [Quick Start](#-quick-start)
- [Key Features](#-key-features)
- [Interactive Mind Maps](#-interactive-mind-maps)
- [Usage Guide](#-usage-guide)
- [Advanced Features](#-advanced-features)
- [Project Architecture](#-project-architecture)
- [FAQ](#-frequently-asked-questions)
- [For Contributors](#-for-contributors)
- [License](#-license)

---

## ⭐ Why This Framework?

### The Problem with Traditional Practice

You solve a problem on LeetCode. It passes. But do you *really* know if your solution is correct? What about:

- That edge case with empty input you didn't test?
- The subtle off-by-one error that only appears with large N?
- Whether your O(n log n) claim is actually true?

**Traditional practice leaves these questions unanswered.** This framework answers them definitively.

### What Makes Us Different

| Capability | This Framework | Typical Repos |
|:-----------|:-------------:|:-------------:|
| **Reproducible Random Tests** | ✅ Seeded generators | ❌ Manual only |
| **Custom Judge Functions** | ✅ ICPC/Codeforces style | ❌ String match |
| **Multi-Solution Benchmarking** | ✅ Compare N approaches | ❌ Single solution |
| **VS Code Integration** | ✅ Tasks, Debug, Shortcuts | ❌ CLI only |
| **Stress Testing** | ✅ Generate 1000+ cases | ❌ Limited |
| **Complexity Estimation** | ✅ Automatic Big-O | ❌ None |

### Built For Excellence

| Audience | How We Help |
|:---------|:------------|
| 🏆 **Competitive Programmers** | Train like Codeforces grandmasters — stress test until you break your code, then fix it |
| 💼 **FAANG Engineers** | Build interview confidence by proving your solutions work, not just hoping they do |
| 🎓 **CS Students** | Learn algorithms the right way — through experimentation, not memorization |
| 👨‍🏫 **Educators** | Give students industrial-grade tools to validate their understanding |
| 🔬 **Researchers** | Benchmark algorithm variants at scale with reproducible methodology |

---

## 🚀 Quick Start

### 1. Setup Environment

<details>
<summary><strong>Windows (PowerShell)</strong></summary>

```powershell
# Clone and navigate to project
cd C:\path\to\neetcode

# Install Python 3.11 (if needed)
py install 3.11

# Create and activate virtual environment
py -3.11 -m venv leetcode
leetcode\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

</details>

<details>
<summary><strong>Linux / macOS</strong></summary>

```bash
# Using pyenv (recommended)
pyenv install 3.11
pyenv local 3.11

# Create and activate virtual environment
python -m venv leetcode
source leetcode/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x run_tests.sh run_case.sh new_problem.sh
```

</details>

### 2. Create Your First Problem

```bash
# Windows
new_problem.bat 0001_two_sum

# Linux/macOS
./new_problem.sh 0001_two_sum
```

This creates:
- `solutions/0001_two_sum.py` — Your solution file
- `tests/0001_two_sum_1.in` — Test input
- `tests/0001_two_sum_1.out` — Expected output

### 3. Run Tests

```bash
# Windows
run_tests.bat 0001_two_sum

# Linux/macOS
./run_tests.sh 0001_two_sum
```

### 4. Debug in VS Code

1. Open any solution file in `solutions/`
2. Press `F5` to debug with test case #1
3. Or press `Ctrl+Shift+B` to run all tests

**That's it!** You're ready to solve problems. 🎉

---

## ✨ Key Features

| Feature | Description |
|:--------|:------------|
| 🧪 **Automated Testing** | Run multiple test cases automatically with clear pass/fail reporting and timing |
| 🎲 **Random Test Generation** | Seeded generators for reproducibility, stress test with 1000+ cases, auto-save failing cases |
| ⚖️ **Custom Judge Functions** | Validate multiple correct answers, ICPC-style validation, works without expected output |
| 📊 **Performance Analysis** | Benchmark multiple solutions, automatic time complexity estimation, side-by-side comparison |
| 🔧 **VS Code Integration** | One-click test execution, integrated debugging, custom tasks and shortcuts |
| 🧠 **Interactive Mind Maps** | Visualize algorithm patterns, track learning progress — [Explore →](https://lufftw.github.io/neetcode/mindmaps/) |

---

## 🧠 Interactive Mind Maps

Visualize algorithm patterns, problem relationships, and learning paths:

| Mind Map | Description | Links |
|:---------|:------------|:------|
| 📐 **Pattern Hierarchy** | API Kernels → Patterns → Problems | [Static](docs/mindmaps/pattern_hierarchy.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#pattern-hierarchy) |
| 👨‍👩‍👧‍👦 **Family Derivation** | Base templates → Derived variants | [Static](docs/mindmaps/family_derivation.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#family-derivation) |
| ⚡ **Algorithm Usage** | Problems by algorithm | [Static](docs/mindmaps/algorithm_usage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#algorithm-usage) |
| 🏗️ **Data Structure Usage** | Problems by data structure | [Static](docs/mindmaps/data_structure.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#data-structure-usage) |
| 🏢 **Company Coverage** | Company-specific problems | [Static](docs/mindmaps/company_coverage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#company-coverage) |
| 🗺️ **Learning Roadmaps** | NeetCode 150, Blind 75, etc. | [Static](docs/mindmaps/roadmap_paths.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#learning-roadmaps) |
| 🔗 **Problem Relations** | Related problems network | [Static](docs/mindmaps/problem_relations.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#problem-relations) |
| 🔀 **Solution Variants** | Multiple approaches | [Static](docs/mindmaps/solution_variants.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#solution-variants) |
| 📊 **Difficulty × Topics** | Topics by difficulty | [Static](docs/mindmaps/difficulty_topics.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#difficulty-topics) |

👉 **[View All Interactive Mind Maps](https://lufftw.github.io/neetcode/mindmaps/)**

---

## 📖 Usage Guide

### ⌨️ VS Code Integration

**Keyboard Shortcuts:**

| Shortcut | Action |
|:---------|:-------|
| `Ctrl+Shift+B` | Run all tests for current file |
| `F5` | Debug with test case #1 |

> **Note:** Open a solution file in `solutions/` before using shortcuts.

**Available Tasks** (`Ctrl+Shift+P` → "Tasks: Run Task"):

| Task | Description |
|:-----|:------------|
| Run all tests | Execute all test cases |
| Run case #1 / #2 / #3 | Run specific test case |
| Benchmark | Show execution times |
| Run all solutions | Compare all implementations |
| Run with generated (10) | Static + 10 generated cases |
| Run generated only | Skip static tests |
| Save failed cases | Auto-save failing inputs |

### 💻 Command Line Interface

```bash
# Run all test cases
python runner/test_runner.py <problem_name>

# Run specific test case
python runner/case_runner.py <problem_name> <case_number>

# Run with benchmarking
python runner/test_runner.py <problem_name> --benchmark

# Run all solutions
python runner/test_runner.py <problem_name> --all

# Generate random tests
python runner/test_runner.py <problem_name> --generate 10

# Estimate time complexity
python runner/test_runner.py <problem_name> --estimate
```

### 📝 Solution File Format

```python
# solutions/0001_two_sum.py
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []

def solve():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    # Parse input
    nums = list(map(int, lines[0].split(',')))
    target = int(lines[1])
    
    # Run solution
    result = Solution().twoSum(nums, target)
    print(result)

if __name__ == "__main__":
    solve()
```

### 📋 Test File Format

| Specification | Requirement |
|:--------------|:------------|
| Line Ending | **LF** (Unix format, `\n`) |
| Encoding | UTF-8 |
| File Ending | Single newline at end |
| Naming | `{number}_{name}_{case}.in/.out` |

**Input file** (`tests/0001_two_sum_1.in`):
```
2,7,11,15
9
```

**Output file** (`tests/0001_two_sum_1.out`):
```
[0, 1]
```

---

## 🔧 Advanced Features

### 🚀 Multi-Solution Benchmarking

Compare multiple approaches for the same problem:

```python
# solutions/0023_merge_k_sorted_lists.py

SOLUTIONS = {
    "default": {
        "method": "mergeKLists_heap",
        "complexity": "O(N log k)",
        "description": "Min Heap approach"
    },
    "divide": {
        "method": "mergeKLists_divide",
        "complexity": "O(N log k)",
        "description": "Divide and Conquer"
    },
    "greedy": {
        "method": "mergeKLists_greedy",
        "complexity": "O(kN)",
        "description": "Greedy comparison"
    },
}

class Solution:
    def mergeKLists_heap(self, lists):
        # Heap implementation
        pass
    
    def mergeKLists_divide(self, lists):
        # Divide & Conquer implementation
        pass
    
    def mergeKLists_greedy(self, lists):
        # Greedy implementation
        pass
```

**Run commands:**

```bash
# Run specific solution
python runner/test_runner.py 0023_merge_k_sorted_lists --method heap

# Compare all solutions
python runner/test_runner.py 0023_merge_k_sorted_lists --all --benchmark
```

**Output:**

```
============================================================
📊 Performance Comparison
============================================================
Method               Avg Time     Complexity      Pass Rate
------------------------------------------------------------
heap                    44.36ms   O(N log k)      3/3
divide                  44.48ms   O(N log k)      3/3
greedy                  44.82ms   O(kN)           3/3
============================================================
```

<details>
<summary><strong>Advanced: Wrapper Pattern for Multiple Classes</strong></summary>

When you need separate classes with the same method name:

```python
class SolutionRecursive:
    def reverseKGroup(self, head, k):
        pass  # Recursive implementation

class SolutionIterative:
    def reverseKGroup(self, head, k):
        pass  # Iterative implementation

# Wrapper functions
def solve_recursive(head, k):
    return SolutionRecursive().reverseKGroup(head, k)

def solve_iterative(head, k):
    return SolutionIterative().reverseKGroup(head, k)

SOLUTIONS = {
    "default": {"method": "solve_iterative", ...},
    "recursive": {"method": "solve_recursive", ...},
}
```

Create with template: `new_problem.bat 0025_reverse_nodes --wrapper`

</details>

### 🔀 Flexible Output Validation

For problems with multiple valid answers ("return in any order"):

**Validation Modes:**

| Mode | Description | Requires `.out` |
|:-----|:------------|:---------------:|
| `[judge]` | Custom validation with reference | ✅ |
| `[judge-only]` | Custom validation only | ❌ |
| `[exact]` | Exact string match | ✅ |
| `[sorted]` | Sort before comparison | ✅ |
| `[set]` | Set comparison | ✅ |

**JUDGE_FUNC (Recommended):**

```python
def judge(actual: list, expected, input_data: str) -> bool:
    """Validate N-Queens solution."""
    n = int(input_data.strip())
    
    # Validate each board
    for board in actual:
        if not is_valid_n_queens(board, n):
            return False
    
    # Check count if expected exists
    if expected is not None:
        return len(actual) == len(expected)
    
    return True

JUDGE_FUNC = judge
```

**COMPARE_MODE (Simple Cases):**

```python
COMPARE_MODE = "sorted"  # Options: "exact" | "sorted" | "set"
```

### 🎲 Random Test Generation

Create a generator file with the same name as your solution:

```python
# generators/0004_median_of_two_sorted_arrays.py
import random
from typing import Iterator, Optional

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases."""
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    yield "[]\n[1]"
    yield "[1]\n[]"
    
    # Random cases
    for _ in range(count - 2):
        m = random.randint(0, 1000)
        n = random.randint(0, 1000)
        nums1 = sorted(random.randint(-10**6, 10**6) for _ in range(m))
        nums2 = sorted(random.randint(-10**6, 10**6) for _ in range(n))
        yield f"{list(nums1)}\n{list(nums2)}".replace(' ', '')
```

**Usage:**

```bash
# Run static + generated tests
python runner/test_runner.py 0004_median --generate 10

# Only generated tests
python runner/test_runner.py 0004_median --generate-only 100

# Reproducible with seed
python runner/test_runner.py 0004_median --generate 10 --seed 42

# Save failing cases
python runner/test_runner.py 0004_median --generate 10 --save-failed
```

### 📈 Time Complexity Estimation

Add a complexity generator function:

```python
# generators/0004_median_of_two_sorted_arrays.py

def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n."""
    m = random.randint(0, n)
    return _generate_case(m, n - m)
```

**Run estimation:**

```bash
python runner/test_runner.py 0004_median --estimate
```

**Output:**

```
📈 Running complexity estimation...
   Sizes: [10, 20, 50, 100, 200, 500, 1000, 2000]
   n=   10: 0.0040ms
   n=  100: 0.0082ms
   n= 1000: 0.0685ms
   n= 2000: 0.1796ms

✅ Estimated: O(n log n)
   Confidence: 1.00
```

---

## 📁 Project Architecture

```
neetcode/
│
├── solutions/                 # 📝 Your solution files
│   └── 0001_two_sum.py
│
├── tests/                     # 📋 Test cases
│   ├── 0001_two_sum_1.in      # Input file
│   ├── 0001_two_sum_1.out     # Expected output
│   └── *_failed_*.in          # Auto-saved failed cases (--save-failed)
│
├── generators/                # 🎲 Random test generators (optional)
│   └── 0001_two_sum.py        # generate(count, seed) function
│
├── runner/                    # ⚙️ Test execution engine
│   ├── test_runner.py         # CLI entry point & main orchestration
│   ├── case_runner.py         # Single case runner (for debugging)
│   ├── executor.py            # Test case execution (subprocess)
│   ├── compare.py             # Output comparison (exact/sorted/set/judge)
│   ├── reporter.py            # Result formatting & benchmark display
│   ├── module_loader.py       # Dynamic module loading
│   ├── complexity_estimator.py # Time complexity estimation (big_O)
│   ├── paths.py               # Path utilities
│   ├── io_utils.py            # File I/O operations
│   └── util.py                # Re-exports (backward compatible)
│
├── templates/                 # 📄 Problem templates
│   ├── template_solution.py          # Single solution
│   ├── template_solution_multi.py    # Multi-solution (one class)
│   └── template_solution_wrapper.py  # Multi-solution (wrapper pattern)
│
├── .vscode/                   # 🔧 VS Code integration
│   ├── settings.json          # Python environment settings
│   ├── tasks.json             # Ctrl+Shift+B shortcuts
│   └── launch.json            # F5 debug configurations
│
├── docs/                      # 📚 Documentation (MkDocs)
│   ├── index.md               # Homepage (English)
│   ├── index_zh-TW.md         # Homepage (繁體中文)
│   ├── mindmaps/              # Generated mind map markdown
│   ├── patterns/              # Generated pattern documentation
│   ├── pages/                 # Generated HTML (gitignored)
│   └── stylesheets/           # Custom CSS
│
├── tools/                     # 🛠️ Utility scripts
│   ├── generate_mindmaps.py   # Generate mind maps
│   ├── generate_mindmaps.toml # Mind maps configuration
│   ├── generate_pattern_docs.py # Generate pattern docs
│   └── text_to_mindmap.py     # LLM text-to-mindmap converter
│
├── ontology/                  # 🧬 Algorithm ontology (TOML)
│   ├── api_kernels.toml       # API kernel definitions
│   ├── patterns.toml          # Pattern definitions
│   ├── algorithms.toml        # Algorithm definitions
│   ├── data_structures.toml   # Data structure definitions
│   ├── companies.toml         # Company definitions
│   ├── topics.toml            # Topic definitions
│   ├── difficulties.toml      # Difficulty levels
│   ├── families.toml          # Problem family definitions
│   └── roadmaps.toml          # Roadmap definitions
│
├── meta/                      # 📊 Problem & pattern metadata
│   ├── problems/              # Problem metadata (one TOML per problem)
│   │   └── *.toml
│   └── patterns/              # Pattern documentation sources
│       └── <pattern_name>/    # Pattern-specific markdown
│
├── roadmaps/                  # 🗺️ Learning path definitions
│   ├── neetcode_150.toml
│   ├── blind_75.toml
│   └── sliding_window_path.toml
│
├── .dev/                      # 🧪 Maintainer zone (unit tests)
│   ├── tests/                 # Unit test suite (150+ cases)
│   ├── run_tests.bat/.sh      # Run unit tests
│   ├── TESTING.md             # Testing documentation
│   └── README.md              # Maintainer guide
│
├── .github/                   # 🚀 GitHub configuration
│   └── workflows/
│       └── deploy-pages.yml   # GitHub Pages deployment
│
├── leetcode/                  # 🐍 Python virtual environment (3.11)
│
├── run_tests.bat / .sh        # Run all tests for a problem
├── run_case.bat / .sh         # Run single test case
├── new_problem.bat / .sh      # Create new problem from template
│
├── requirements.txt           # Python dependencies
├── mkdocs.yml                 # MkDocs configuration
├── pytest.ini                 # pytest configuration
├── README.md                  # This file (English)
└── README_zh-TW.md            # 繁體中文版
```

### Directory Guide

| Directory | Purpose | Target Audience |
|:----------|:--------|:----------------|
| `solutions/` | Write your solutions here | ✅ All users |
| `tests/` | Add test cases (.in/.out) | ✅ All users |
| `generators/` | Random test generators | ✅ All users |
| `runner/` | Test execution engine | 🔧 Contributors |
| `templates/` | Problem templates | ✅ All users |
| `.vscode/` | VS Code configuration | ✅ All users |
| `docs/` | MkDocs documentation | 🔧 Contributors |
| `tools/` | Documentation generators | 🔧 Contributors |
| `ontology/` | Algorithm ontology data | 🔧 Contributors |
| `meta/` | Problem/pattern metadata | 🔧 Contributors |
| `.dev/` | Unit tests (150+ cases) | 🔧 Maintainers |

> **📝 Note:** Files in `docs/mindmaps/`, `docs/patterns/`, and `docs/pages/` are auto-generated. Edit the source files in `ontology/`, `meta/`, and `tools/` instead.

---

## ❓ Frequently Asked Questions

<details>
<summary><strong>What problems does this framework solve?</strong></summary>

- Running multiple algorithm implementations automatically
- Generating reproducible random test data for stress testing
- Benchmarking solutions to identify performance differences
- Debugging LeetCode-style problems with VS Code integration
- Validating outputs using custom logic beyond simple file comparison

</details>

<details>
<summary><strong>How is this different from copying LeetCode solutions?</strong></summary>

This is not a solution collection — it's a **testing infrastructure**. You write solutions, and the framework:

1. Runs them against static test cases
2. Generates random test cases automatically
3. Validates correctness using custom judge functions
4. Benchmarks multiple solutions against each other
5. Estimates time complexity empirically

</details>

<details>
<summary><strong>Can I use this for interview preparation?</strong></summary>

Absolutely! The framework is perfect for interview prep:

- Practice writing solutions in **real LeetCode format**
- Find **edge cases you might miss** with random test generation
- See which approach is **actually faster** with benchmarking
- **Debug easily** with VS Code integration

</details>

<details>
<summary><strong>What Python version is required?</strong></summary>

Python 3.11 — matching the [LeetCode official environment](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages).

</details>

---

## 🛠️ For Contributors

### Running Unit Tests

```bash
# Activate virtual environment
leetcode\Scripts\activate  # Windows
source leetcode/bin/activate  # Linux/macOS

# Run all tests
python -m pytest .dev/tests -v

# With coverage
python -m pytest .dev/tests --cov=runner --cov-report=html
```

### Generate Mind Maps Locally

```bash
# Generate Markdown mind maps
python tools/generate_mindmaps.py

# Generate HTML (interactive) mind maps
python tools/generate_mindmaps.py --html
```

Configuration: `tools/generate_mindmaps.toml`

### Documentation

- [`.dev/README.md`](.dev/README.md) — Maintainer guide
- [`.dev/TESTING.md`](.dev/TESTING.md) — Testing documentation
- [`docs/GITHUB_PAGES_SETUP.md`](docs/GITHUB_PAGES_SETUP.md) — Deployment guide

---

## 📜 License

**MIT License** — Free for personal learning and educational use.

---

**Built with ❤️ for the competitive programming community**

# 🧩 NeetCode / LeetCode Practice Framework

**Language / 語言**: [English](README.md) | [繁體中文](README_zh-TW.md)

A complete LeetCode practice framework with multiple test cases, auto-comparison, and debug integration.

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
│   ├── test_runner.py       ← Run all .in/.out and compare
│   ├── case_runner.py       ← Run single test case (for debugging)
│   └── util.py              ← Shared utilities
│
├── solutions/               ← Solution files for each problem
│   └── 0001_two_sum.py
│
├── tests/                   ← All test cases
│   ├── 0001_two_sum_1.in
│   ├── 0001_two_sum_1.out
│   └── ...
│
├── templates/               ← Templates for new problems
│   ├── template_solution.py         ← Single solution template
│   ├── template_solution_multi.py   ← Multi-solution (one class)
│   ├── template_solution_wrapper.py ← Multi-solution (wrapper pattern)
│   └── template_test.txt
│
├── leetcode/                ← Python virtual environment (Python 3.11)
│
├── run_tests.bat            ← Windows: Run all tests
├── run_case.bat             ← Windows: Run single test
├── new_problem.bat          ← Windows: Create new problem
│
├── run_tests.sh             ← Linux/macOS: Run all tests
├── run_case.sh              ← Linux/macOS: Run single test
├── new_problem.sh           ← Linux/macOS: Create new problem
│
└── README.md
```

---

## 🚀 Quick Start

### 1. Environment Setup (First Time)

> Reference: [LeetCode Official Environment](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages)

#### Windows (PowerShell)

```powershell
# Navigate to project directory
cd /d "D:\Developer\program\python\neetcode"

# Install Python 3.11 (if not already installed)
py install 3.11

# Create virtual environment
py -3.11 -m venv leetcode

# Activate virtual environment
leetcode\Scripts\activate

# Install debugpy (for debugging)
pip install debugpy
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

# Install debugpy (for debugging)
pip install debugpy

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

## ⌨️ VS Code Shortcuts

| Shortcut | Function |
|----------|----------|
| `Ctrl+Shift+B` | Run all tests for current file |
| `F5` | Debug current file with case #1 |

> **Note**: Open a solution file in `solutions/` before using shortcuts.

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

Some LeetCode problems state **"You may return the answer in any order"** or have multiple valid answers. The test runner supports two approaches:

### Priority

```
1. JUDGE_FUNC (custom validation) - highest priority
2. COMPARE_MODE (sorted/set comparison)
3. Exact string match (default)
```

---

### Approach 1: JUDGE_FUNC (Recommended for Complex Cases)

Use **Decision Problem** approach: verify the answer is **valid**, not just **identical**.

```python
# solutions/0051_n_queens.py

def judge(actual: list, expected: list, input_data: str) -> bool:
    """
    Custom validation function.
    
    Args:
        actual: Program output (parsed as Python object if possible, otherwise raw string)
        expected: Expected output (parsed as Python object if possible, otherwise raw string)
        input_data: Input data (raw string)
    
    Returns:
        bool: Whether the answer is correct
    """
    n = int(input_data.strip())
    
    # 1. Check solution count
    if len(actual) != len(expected):
        return False
    
    # 2. Verify each solution is valid
    for board in actual:
        if not is_valid_n_queens(board, n):
            return False
    
    # 3. Check no duplicates
    return len(set(tuple(b) for b in actual)) == len(actual)

JUDGE_FUNC = judge  # Tell test_runner to use this function
```

**Benefits:**
- Validates correctness, not just string equality
- Handles multiple valid answers
- Works with any output format (strings, objects, custom formats)

---

### Approach 2: COMPARE_MODE (Simple Cases)

For simple order-independent comparisons:

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

#### Example 1: N-Queens (Object Mode)

```python
def judge(actual: list, expected: list, input_data: str) -> bool:
    n = int(input_data.strip())
    # Verify each board is valid...
    return all(is_valid_board(b, n) for b in actual)

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

---

### Applicable Problems

| Problem | Recommended Approach |
|---------|---------------------|
| N-Queens | `JUDGE_FUNC` (validate board) |
| Permutations | `COMPARE_MODE = "sorted"` |
| Subsets | `COMPARE_MODE = "sorted"` |
| Shortest Path (multiple) | `JUDGE_FUNC` (validate path) |
| Floating point | `JUDGE_FUNC` (tolerance) |
| LinkedList/Tree | `JUDGE_FUNC` (parse format) |

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
- **Installed Packages**:
  - `debugpy` - Debug support

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

## 💡 Tips

1. **Add more test cases**: Copy `.in/.out` files and change the number
   ```
   0001_two_sum_1.in → 0001_two_sum_2.in
   0001_two_sum_1.out → 0001_two_sum_2.out
   ```

2. **Debug specific test case**: Modify case number in `launch.json`

3. **Custom input format**: Define parsing logic in `solve()` function

---

## 📜 License

MIT License - Free for personal learning

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
│   ├── template_solution.py       ← Single solution template
│   ├── template_solution_multi.py ← Multi-solution template
│   └── template_test.txt
│
├── leetcode/                ← Python virtual environment (Python 3.11)
│
├── run_tests.bat            ← Windows: Run all tests
├── run_case.bat             ← Windows: Run single test
├── new_problem.bat          ← Windows: Create new problem
│
└── README.md
```

---

## 🚀 Quick Start

### 1. Environment Setup (First Time)

> Reference: [LeetCode Official Environment](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages)

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

### 2. Daily Usage (Activate Environment)

```powershell
cd /d "D:\Developer\program\python\neetcode"
leetcode\Scripts\activate
```

### 3. Create New Problem

```batch
# Single solution template
new_problem.bat 0007_reverse_integer

# Multi-solution template (supports --all, --benchmark)
new_problem.bat 0023_merge_k_lists --multi
```

This will create:
- `solutions/0007_reverse_integer.py`
- `tests/0007_reverse_integer_1.in`
- `tests/0007_reverse_integer_1.out`

### 4. Run Tests

```batch
# Run all test cases
run_tests.bat 0001_two_sum

# Run single test case
run_case.bat 0001_two_sum 1
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
        "method": "mergeKListsPriorityQueue",       # 對應的方法名稱
        "complexity": "O(N log k)",          # 時間複雜度
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

```powershell
# PowerShell
.\leetcode\Scripts\Activate.ps1

# CMD
leetcode\Scripts\activate.bat
```

### Install New Packages

```powershell
# Activate virtual environment first, then install
leetcode\Scripts\activate
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

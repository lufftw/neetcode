# 🧩 NeetCode / LeetCode 練習框架

**Language / 語言**: [English](README.md) | [繁體中文](README_zh-TW.md)

一套完整的 LeetCode 練習框架，支援多筆測資、自動比對、Debug 整合。

---

## 📑 目錄

- [專案結構](#-專案結構)

- [快速開始](#-快速開始)
  - [環境設定](#1-環境設定首次安裝)
  - [日常使用](#2-日常使用啟動環境)
  - [建立新題目](#3-建立新題目)
  - [執行測試](#4-執行測試)

- [VS Code 整合](#️-vs-code-整合)
  - [快捷鍵](#快捷鍵)
  - [Tasks](#tasksctrlshiftp--tasks-run-task)
  - [Debug 配置](#debug-配置f5--選擇)

- [解答檔案格式](#-解答檔案格式)

- [測資檔案格式](#-測資檔案格式)

- [命令列用法](#-命令列用法)

- [多解法測試與效能比較](#-多解法測試與效能比較)
  - [命令列參數](#命令列參數)
  - [如何定義多解法](#如何定義多解法)
  - [SOLUTIONS 欄位說明](#solutions-欄位說明)
  - [自定義短名稱](#自定義短名稱)
  - [Wrapper 模式](#進階使用-wrapper-函式分離多個解法類別)

- [彈性輸出比對](#-彈性輸出比對)
  - [驗證模式](#驗證模式)
  - [JUDGE_FUNC](#方式一judge_func複雜情況推薦)
  - [COMPARE_MODE](#方式二compare_mode簡單情況)
  - [JUDGE_FUNC 範例](#judge_func-範例)
  - [適用題目](#適用題目)

- [測資產生器](#-測資產生器)

- [測試結果範例](#-測試結果範例)

- [Python 環境](#-python-環境)

- [小技巧](#-小技巧)

- [License](#-license)

---

## 📁 專案結構

```
neetcode/
│
├── .vscode/                 ← VS Code 整合設定
│   ├── settings.json        ← Python 環境設定
│   ├── tasks.json           ← Ctrl+Shift+B 快捷任務
│   └── launch.json          ← F5 Debug 設定
│
├── runner/                  ← 執行器模組
│   ├── test_runner.py       ← 跑所有 .in/.out 並比對
│   ├── case_runner.py       ← 跑單一 .in 測資（Debug 用）
│   └── util.py              ← 共用工具函式
│
├── solutions/               ← 每一題的解答程式
│   └── 0001_two_sum.py
│
├── tests/                   ← 所有測資
│   ├── 0001_two_sum_1.in
│   ├── 0001_two_sum_1.out
│   └── ...
│
├── templates/               ← 新題目模板
│   ├── template_solution.py         ← 單一解法模板
│   ├── template_solution_multi.py   ← 多解法（單一類別）
│   ├── template_solution_wrapper.py ← 多解法（Wrapper 模式）
│   └── template_test.txt
│
├── leetcode/                ← Python 虛擬環境 (Python 3.11)
│
├── run_tests.bat            ← Windows: 執行所有測資
├── run_case.bat             ← Windows: 執行單一測資
├── new_problem.bat          ← Windows: 建立新題目
│
├── run_tests.sh             ← Linux/macOS: 執行所有測資
├── run_case.sh              ← Linux/macOS: 執行單一測資
├── new_problem.sh           ← Linux/macOS: 建立新題目
│
└── README.md
```

---

## 🚀 快速開始

### 1. 環境設定（首次安裝）

> 參考 [LeetCode 官方環境說明](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages)

#### Windows (PowerShell)

> **前置需求**：要使用 `py install` 指令，需要先從 [Python 官方網站](https://www.python.org/downloads/) 安裝 **Python Install Manager**。

```powershell
# 進入專案目錄
cd /d "D:\Developer\program\python\neetcode"

# 安裝 Python 3.11（如果尚未安裝）
# 注意：需要先從 https://www.python.org/downloads/ 安裝 Python Install Manager
py install 3.11

# 建立虛擬環境
py -3.11 -m venv leetcode

# 啟動虛擬環境
leetcode\Scripts\activate

# 安裝 debugpy（Debug 用）
pip install debugpy
```

#### Linux / macOS（使用 pyenv - 推薦）

> **為什麼用 pyenv？** 安裝在使用者目錄，不影響系統 Python，支援多版本管理。

```bash
# ============================================
# 步驟 1: 安裝 pyenv（僅需一次）
# ============================================

# --- macOS ---
brew install pyenv

# --- Linux (Ubuntu/Debian/Fedora 等) ---
# 先安裝相依套件：
sudo apt update && sudo apt install -y build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev curl \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# 安裝 pyenv：
curl https://pyenv.run | bash

# ============================================
# 步驟 2: 設定 shell（加入 ~/.bashrc 或 ~/.zshrc）
# ============================================
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# 重新載入 shell
source ~/.bashrc   # 或: source ~/.zshrc

# ============================================
# 步驟 3: 安裝 Python 3.11 並設定專案
# ============================================
# 進入專案目錄
cd ~/path/to/neetcode

# 安裝 Python 3.11（不影響系統 Python）
pyenv install 3.11

# 僅在此專案使用 Python 3.11
pyenv local 3.11

# 建立虛擬環境
python -m venv leetcode

# 啟動虛擬環境
source leetcode/bin/activate

# 安裝 debugpy（Debug 用）
pip install debugpy

# 設定腳本執行權限（僅需執行一次）
chmod +x run_tests.sh run_case.sh new_problem.sh
```

<details>
<summary>📋 替代方案：直接系統安裝（可能影響現有 Python）</summary>

```bash
# Ubuntu/Debian:
sudo apt update && sudo apt install python3.11 python3.11-venv

# macOS (Homebrew):
brew install python@3.11

# 然後建立 venv：
python3.11 -m venv leetcode
```

</details>

### 2. 日常使用（啟動環境）

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

### 3. 建立新題目

#### Windows

```batch
# 單一解法模板
new_problem.bat 0007_reverse_integer

# 多解法模板（單一類別，多個方法）
new_problem.bat 0023_merge_k_lists --multi

# Wrapper 模式模板（多個類別，保留 LeetCode 原始方法名稱）
new_problem.bat 0025_reverse_nodes --wrapper
```

#### Linux / macOS

```bash
# 單一解法模板
./new_problem.sh 0007_reverse_integer

# 多解法模板（單一類別，多個方法）
./new_problem.sh 0023_merge_k_lists --multi

# Wrapper 模式模板（多個類別，保留 LeetCode 原始方法名稱）
./new_problem.sh 0025_reverse_nodes --wrapper
```

這會自動建立：
- `solutions/0007_reverse_integer.py`
- `tests/0007_reverse_integer_1.in`
- `tests/0007_reverse_integer_1.out`

### 4. 執行測試

#### Windows

```batch
# 執行所有測資
run_tests.bat 0001_two_sum

# 執行單一測資
run_case.bat 0001_two_sum 1
```

#### Linux / macOS

```bash
# 執行所有測資
./run_tests.sh 0001_two_sum

# 執行單一測資
./run_case.sh 0001_two_sum 1
```

---

## ⌨️ VS Code 整合

### 快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl+Shift+B` | 執行當前檔案對應的所有測資 |
| `F5` | Debug 當前檔案的 case #1 |

> **注意**: 請先開啟 `solutions/` 中的解答檔案，再使用快捷鍵。

### Tasks（Ctrl+Shift+P → "Tasks: Run Task"）

| Task | 說明 |
|------|------|
| Run all tests for current problem | 基本測試執行 |
| Run case #1 / #2 | 執行特定測資 |
| Benchmark current problem | 顯示執行時間 |
| Run all solutions with benchmark | 比較所有解法 |
| Run with generated cases (10) | 靜態 + 10 筆生成測資 |
| Run generated only | 跳過靜態測資 |
| Run generated with seed | 可重現的生成 |
| Run generated + save failed | 儲存失敗的輸入 |
| Run all solutions + generated | 所有解法 + 生成測資 |

### Debug 配置（F5 → 選擇）

| 配置 | 說明 |
|------|------|
| Debug current problem (case #1/2/3) | Debug 特定測資 |
| Debug all tests | Debug 完整測試 |
| Benchmark current problem | 帶計時執行 |
| Debug with generated cases | 靜態 + 生成測資 |
| Debug generated only | 只用生成測資 |
| Debug generated with seed | 可重現的 debug |
| Debug all solutions + generated | 比較所有解法 + 生成 |

> 💡 **提示**：這些 tasks/配置執行的指令與 [命令列用法](#-命令列用法) 和 [測資產生器](#-測資產生器) 相同。
> 
> 範例："Benchmark current problem" 執行 `python runner/test_runner.py {problem} --benchmark`

---

## 📝 解答檔案格式

```python
# solutions/0001_two_sum.py
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # 你的解法
        pass

def solve():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    # 解析輸入
    nums = list(map(int, lines[0].split(',')))
    target = int(lines[1])
    
    sol = Solution()
    result = sol.twoSum(nums, target)
    
    # 輸出答案
    print(result)

if __name__ == "__main__":
    solve()
```

---

## 📋 測資檔案格式

### 格式規範

| 項目 | 規範 |
|------|------|
| 換行符號 | **LF** (Unix/Linux 格式，`\n`) |
| 編碼 | UTF-8 |
| 結尾 | 必須以單一換行結尾 |
| 命名規則 | `{題號}_{題目名稱}_{編號}.in/.out` |

### 輸入檔 (`.in`)
```
2,7,11,15
9

```

### 輸出檔 (`.out`)
```
[0, 1]

```

---

## 🔧 命令列用法

```bash
# 執行所有測資
python runner/test_runner.py <problem_name>

# 執行單一測資
python runner/case_runner.py <problem_name> <case_index>
```

### 範例

```bash
python runner/test_runner.py 0001_two_sum
python runner/case_runner.py 0001_two_sum 1
```

---

## 🚀 多解法測試與效能比較

當一道題目有多種解法時，可以同時測試並比較效能。

### 命令列參數

```bash
# 執行預設解法
python runner/test_runner.py 0023_merge_k_sorted_lists

# 執行指定解法
python runner/test_runner.py 0023_merge_k_sorted_lists --method heap
python runner/test_runner.py 0023_merge_k_sorted_lists --method greedy

# 執行所有解法
python runner/test_runner.py 0023_merge_k_sorted_lists --all

# 執行所有解法 + 效能比較
python runner/test_runner.py 0023_merge_k_sorted_lists --all --benchmark
```

### 如何定義多解法

在 solution 檔案中加入 `SOLUTIONS` 字典：

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
    def mergeKLists_heap(self, lists):
        # Heap 解法實作...
        pass

    def mergeKListsDivideConquer(self, lists):
        # Divide & Conquer 解法實作...
        pass

    def mergeKLists_greedy(self, lists):
        # Greedy 解法實作...
        pass

def solve():
    import os
    # 從環境變數取得要執行的解法
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    method_info = SOLUTIONS.get(method_name, SOLUTIONS['default'])
    method_func_name = method_info['method']
    
    sol = Solution()
    method_func = getattr(sol, method_func_name)
    result = method_func(...)
    print(result)
```

### SOLUTIONS 欄位說明

| 欄位 | 說明 | 必填 |
|------|------|------|
| `method` | Solution class 中對應的方法名稱 | ✅ |
| `complexity` | 時間複雜度（用於顯示比較） | ❌ |
| `description` | 解法描述 | ❌ |

### 自定義短名稱

`SOLUTIONS` 的 **key** 就是命令列使用的短名稱，可以自由定義：

```python
SOLUTIONS = {
    "default": {"method": "solve_optimal", ...},     # 預設解法
    "heap": {"method": "solve_heap", ...},           # --method heap
    "h": {"method": "solve_heap", ...},              # --method h (別名)
    "pq": {"method": "solve_priority_queue", ...},   # --method pq
    "bf": {"method": "solve_bruteforce", ...},       # --method bf
}
```

> **注意**: 
> - `default` 是預設解法，不指定 `--method` 時使用
> - 時間複雜度需由使用者自行標註，系統僅測量實際執行時間

### 進階：使用 Wrapper 函式分離多個解法類別

當實作多種解法（如遞迴 vs 迭代）時，你可能會遇到：
- 方法名稱在同一個類別內衝突
- 需要重新命名方法，偏離原本 LeetCode 的簽名

**解決方案**：使用獨立的 Solution 類別搭配 wrapper 函式。

```python
# solutions/0025_reverse_nodes_in_k_group.py

# ============================================
# 解法一：遞迴
# ============================================
class SolutionRecursive:
    def reverseKGroup(self, head, k):
        # 遞迴實作...
        pass

# ============================================
# 解法二：迭代
# ============================================
class SolutionIterative:
    def reverseKGroup(self, head, k):
        # 迭代實作...
        pass

# ============================================
# Wrapper 函式 - 整合 test_runner
# ============================================
def solve_recursive(head, k):
    """SolutionRecursive 的 wrapper。"""
    return SolutionRecursive().reverseKGroup(head, k)

def solve_iterative(head, k):
    """SolutionIterative 的 wrapper。"""
    return SolutionIterative().reverseKGroup(head, k)

# ============================================
# SOLUTIONS 定義
# ============================================
SOLUTIONS = {
    "default": {
        "method": "solve_iterative",
        "complexity": "O(N) time, O(1) space",
        "description": "迭代式原地反轉"
    },
    "recursive": {
        "method": "solve_recursive",
        "complexity": "O(N) time, O(N) space",
        "description": "遞迴反轉（使用堆疊）"
    },
    "iterative": {
        "method": "solve_iterative",
        "complexity": "O(N) time, O(1) space",
        "description": "迭代式原地反轉"
    },
}

def solve():
    import os
    import sys
    
    # 從環境變數取得解法名稱
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    method_info = SOLUTIONS.get(method_name, SOLUTIONS['default'])
    method_func_name = method_info['method']
    
    # 解析輸入
    lines = sys.stdin.read().strip().split('\n')
    # ... 解析你的輸入 ...
    
    # 直接呼叫 wrapper 函式（不透過類別）
    method_func = globals()[method_func_name]
    result = method_func(head, k)
    
    print(result)
```

**這個模式的好處：**
- 每個解法都在獨立的類別中（`SolutionRecursive`、`SolutionIterative`）
- 保留原本 LeetCode 的方法名稱（如 `reverseKGroup`、`mergeKLists`）
- 不會在同一個類別內發生方法名稱衝突
- 當題目有超過兩種解法時，擴展性佳

> **提示**：使用 `new_problem.bat <name> --wrapper`（Windows）或 `./new_problem.sh <name> --wrapper`（Linux/macOS）建立此模式的模板。

---

## 🔀 彈性輸出比對

某些 LeetCode 題目會標註 **「可以以任意順序回傳答案」** 或有多個正確答案。測試執行器支援彈性驗證，並在輸出中顯示清楚的標籤。

### 驗證模式

| 標籤 | 說明 | 需要 `.out` |
|------|------|-------------|
| `[judge]` | JUDGE_FUNC 搭配 `.out` 參考 | ✅ |
| `[judge-only]` | JUDGE_FUNC 純驗證（無 `.out`） | ❌ |
| `[exact]` | 精確字串比對 | ✅ |
| `[sorted]` | 排序後比對 | ✅ |
| `[set]` | 集合比對 | ✅ |

### 優先級

```
1. JUDGE_FUNC（自訂驗證函式）- 最高優先級
2. COMPARE_MODE（排序/集合比對）
3. 精確字串比對（預設）
```

### 測試輸出範例

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

### 方式一：JUDGE_FUNC（複雜情況推薦）

使用 **Decision Problem** 方式：驗證答案是否**正確**，而非是否**相同**。

**重要特色**：定義 `JUDGE_FUNC` 時，`.out` 檔案是**可選的**！

```python
# solutions/0051_n_queens.py

def judge(actual: list, expected, input_data: str) -> bool:
    """
    自訂驗證函式
    
    Args:
        actual: 程式輸出（若可解析則為 Python 物件）
        expected: 預期輸出，若 .out 不存在則為 None
        input_data: 輸入資料（原始字串）
    
    Returns:
        bool: 答案是否正確
    """
    n = int(input_data.strip())
    
    # 不管有沒有 expected，都要驗證解的合法性
    for board in actual:
        if not is_valid_n_queens(board, n):
            return False
    
    # 有 expected 時才檢查數量
    if expected is not None:
        if len(actual) != len(expected):
            return False
    
    # 檢查無重複
    return len(set(tuple(b) for b in actual)) == len(actual)

JUDGE_FUNC = judge  # 告訴 test_runner 使用這個函式
```

**優點：**
- 驗證正確性，而非字串相等
- 處理多個正確答案
- **`.out` 檔案可選** - 支援純驗證模式（judge-only）
- 支援任何輸出格式（字串、物件、自訂格式）

**純驗證模式（無 `.out`）的使用情境：**
- 自訂的大型測資
- 使用隨機輸入做壓力測試
- 計算預期輸出太複雜的情況

---

### 方式二：COMPARE_MODE（簡單情況）

適用於簡單的順序無關比對（需要 `.out` 檔案）：

```python
# solutions/0046_permutations.py

COMPARE_MODE = "sorted"  # 選項: "exact" | "sorted" | "set"
```

| 模式 | 說明 | 適用情境 |
|------|------|----------|
| `"exact"` | 精確比對（預設） | 大多數題目 |
| `"sorted"` | 排序後比對 | Permutations、Combinations |
| `"set"` | 集合比對（忽略重複） | 不重複元素 |

---

### JUDGE_FUNC 範例

#### 範例一：N-Queens（支援可選的 `.out`）

```python
def judge(actual: list, expected, input_data: str) -> bool:
    n = int(input_data.strip())
    
    # 永遠驗證棋盤正確性
    if not all(is_valid_board(b, n) for b in actual):
        return False
    
    # 有 .out 時也檢查數量
    if expected is not None:
        return len(actual) == len(expected)
    
    return True  # 純驗證模式：只驗證合法性

JUDGE_FUNC = judge
```

#### 範例二：LinkedList（字串模式）

```python
def judge(actual: str, expected: str, input_data: str) -> bool:
    # 解析 "1->2->3" 格式
    def parse(s):
        return s.strip().split("->") if s.strip() else []
    return parse(actual) == parse(expected)

JUDGE_FUNC = judge
```

#### 範例三：浮點數誤差

```python
def judge(actual: float, expected: float, input_data: str) -> bool:
    return abs(actual - expected) < 1e-5

JUDGE_FUNC = judge
```

#### 範例四：純驗證（Judge-Only）

```python
def judge(actual: list, expected, input_data: str) -> bool:
    """不需要預期輸出的驗證"""
    # 當 .out 不存在時，expected 為 None
    params = parse_input(input_data)
    return is_valid_solution(actual, params)

JUDGE_FUNC = judge
```

---

### 適用題目

| 題目 | 推薦方式 | 需要 `.out` |
|------|----------|-------------|
| N-Queens | `JUDGE_FUNC`（驗證棋盤） | 可選 |
| Permutations | `COMPARE_MODE = "sorted"` | ✅ |
| Subsets | `COMPARE_MODE = "sorted"` | ✅ |
| 最短路徑（多解） | `JUDGE_FUNC`（驗證路徑） | 可選 |
| 浮點數運算 | `JUDGE_FUNC`（誤差容忍） | ✅ |
| LinkedList/Tree | `JUDGE_FUNC`（解析格式） | ✅ |
| 自訂壓力測試 | `JUDGE_FUNC`（judge-only） | ❌ |

---

## 🎲 測資產生器

自動產生測資來壓力測試你的解法。

### 設定

在 `generators/` 建立與 solution 同名的檔案：

```
generators/
└── 0004_median_of_two_sorted_arrays.py
```

### Generator 模板

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
    產生測資輸入。
    
    Args:
        count: 產生幾筆測資
        seed: 隨機種子（可重現）
    
    Yields:
        str: 測資輸入（與 .in 檔案格式相同）
    """
    # Constraints
    min_m, max_m = 0, 1000
    min_n, max_n = 0, 1000
    min_val, max_val = -10**6, 10**6
    
    if seed is not None:
        random.seed(seed)
    
    # 邊界測資優先
    yield "[]\n[1]"
    yield "[1]\n[]"
    count -= 2
    
    # 隨機測資
    for _ in range(count):
        m = random.randint(min_m, max_m)
        n = random.randint(min_n, max_n)
        nums1 = sorted([random.randint(min_val, max_val) for _ in range(m)])
        nums2 = sorted([random.randint(min_val, max_val) for _ in range(n)])
        yield f"{nums1}\n{nums2}".replace(' ', '')
```

### 使用方式

```bash
# 執行 tests/ + 10 筆生成測資
python runner/test_runner.py 0004_median --generate 10

# 只執行生成測資（跳過 tests/）
python runner/test_runner.py 0004_median --generate-only 10

# 指定 seed（可重現）
python runner/test_runner.py 0004_median --generate 10 --seed 12345

# 儲存失敗的測資
python runner/test_runner.py 0004_median --generate 10 --save-failed
```

### 輸出範例

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

### 需求

| 元件 | 必要 | 說明 |
|------|------|------|
| `generators/{problem}.py` | Generator 檔案 | 需有 `generate(count, seed)` 函式 |
| `JUDGE_FUNC` in solution | ✅ | 生成測資無 `.out`，需要 judge |
| `tests/*.in` | 可選 | 靜態測資先執行 |

---

## 📊 測試結果範例

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

## 🐍 Python 環境

- **Python 版本**: 3.11（與 [LeetCode 官方環境](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages) 一致）
- **虛擬環境**: `leetcode/` (專案內)
- **已安裝套件**:
  - `debugpy` - Debug 支援

### 啟動虛擬環境

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

### 安裝新套件

#### Windows

```powershell
# 先啟動虛擬環境，再安裝
leetcode\Scripts\activate
pip install <package_name>
```

#### Linux / macOS

```bash
# 先啟動虛擬環境，再安裝
source leetcode/bin/activate
pip install <package_name>
```

---

## 💡 小技巧

1. **新增多筆測資**: 複製 `.in/.out` 檔案，修改編號即可
   ```
   0001_two_sum_1.in → 0001_two_sum_2.in
   0001_two_sum_1.out → 0001_two_sum_2.out
   ```

2. **Debug 特定測資**: 修改 `launch.json` 中的 case 編號

3. **自訂輸入格式**: 在 `solve()` 函式中自由定義解析邏輯

---

## 📜 License

MIT License - 自由使用於個人學習


# 🧩 NeetCode / LeetCode 練習框架

**Language / 語言**: [English](README.md) | [繁體中文](README_zh-TW.md)

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![VS Code](https://img.shields.io/badge/VS%20Code-Integration-007ACC.svg)](https://code.visualstudio.com/)

一套**高效能 Python LeetCode / 演算法練習框架**，支援可重現隨機測資生成、自訂 `JUDGE_FUNC` 驗證、多解法效能比較，以及完整的 VS Code Debug 工作流程整合。專為**競程**、**演算法工程**和**大規模壓力測試**設計。

> 🚀 **核心功能**：演算法自動化測試執行器 | 可重現隨機測資生成器 | Judge 函式驗證（Codeforces/ICPC 風格）| 多解法效能比較 | VS Code Debug 整合 | 壓力測試工具

---

## ⭐ 為什麼這個框架不一樣

大多數 LeetCode 專案只是解答集。**這個框架是一套完整的測試基礎設施**：

| 功能 | 此框架 | 一般 LeetCode 專案 |
|------|--------|-------------------|
| **可重現隨機測資** | ✅ 帶 Seed 的生成器 | ❌ 僅手動測資 |
| **自訂 Judge 函式** | ✅ Codeforces/ICPC 風格驗證 | ❌ 僅字串完全比對 |
| **多解法效能比較** | ✅ 自動比較 N 種解法 | ❌ 一個檔案一種解法 |
| **VS Code 整合** | ✅ Tasks、Debug、快捷鍵 | ❌ 僅命令列 |
| **壓力測試** | ✅ 生成 1000+ 筆測資 | ❌ 僅限手動測資 |
| **時間複雜度估算** | ✅ 自動 Big-O 分析 | ❌ 無此功能 |

---

## ❓ 常見問題

<details>
<summary><strong>這個框架解決什麼問題？</strong></summary>

- 自動執行多種演算法實作
- 生成大規模可重現測資進行壓力測試
- 比較不同解法的效能差異
- 使用 VS Code 整合 Debug LeetCode 風格題目
- 使用自訂邏輯驗證輸出，超越簡單的 `.out` 檔案比對

</details>

<details>
<summary><strong>這個框架適合誰？</strong></summary>

- **競程選手**：準備比賽（Codeforces、ICPC 等）
- **軟體工程師**：準備技術面試（FAANG 等）
- **學生**：修習資料結構與演算法課程
- **研究人員**：需要大規模演算法壓力測試

</details>

<details>
<summary><strong>這和單純複製 LeetCode 解答有什麼不同？</strong></summary>

這不是解答集——而是一套**測試基礎設施**。你撰寫解答，框架會：
1. 用靜態測資執行測試
2. 自動生成隨機測資
3. 用自訂 Judge 函式驗證正確性
4. 比較多種解法的效能
5. 經驗性估算時間複雜度

</details>

<details>
<summary><strong>可以用這個準備面試嗎？</strong></summary>

當然可以！這個框架非常適合面試準備，因為：
- 你可以用**真正的 LeetCode 格式**練習撰寫解答
- 隨機測資生成器幫你找到**你可能遺漏的邊界條件**
- 多解法效能比較顯示哪種方法**實際上更快**
- VS Code 整合讓 **Debug 變得簡單**

</details>

---

## 📑 目錄

- [為什麼這個框架不一樣](#-為什麼這個框架不一樣)

- [常見問題](#-常見問題)

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

- [時間複雜度估算](#-時間複雜度估算)

- [時間複雜度估算](#-時間複雜度估算)

- [測試結果範例](#-測試結果範例)

- [Python 環境](#-python-環境)

- [小技巧](#-小技巧)

- [維護者專區](#-維護者專區單元測試)

- [Runner 模組架構](#️-runner-模組架構開發者專區)

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
│   ├── test_runner.py       ← CLI 入口點
│   ├── module_loader.py     ← 載入 solution/generator 模組
│   ├── executor.py          ← 執行測試案例
│   ├── reporter.py          ← 格式化與顯示結果
│   ├── compare.py           ← 輸出比較邏輯
│   ├── paths.py             ← 路徑工具
│   ├── io_utils.py          ← 檔案 I/O 操作
│   ├── util.py              ← Re-exports（向後兼容）
│   ├── complexity_estimator.py  ← 時間複雜度估算
│   └── case_runner.py       ← 跑單一測資（Debug 用）
│
├── solutions/               ← 每一題的解答程式
│   └── 0001_two_sum.py
│
├── tests/                   ← 所有測資
│   ├── 0001_two_sum_1.in
│   ├── 0001_two_sum_1.out
│   ├── *_failed_*.in        ← 自動儲存的失敗生成測資（使用 --save-failed）
│   └── ...
│
├── generators/              ← 測資產生器（可選）
│   └── 0001_two_sum.py      ← 產生隨機測資
│
├── templates/               ← 新題目模板
│   ├── template_solution.py         ← 單一解法模板
│   ├── template_solution_multi.py   ← 多解法（單一類別）
│   ├── template_solution_wrapper.py ← 多解法（Wrapper 模式）
│   └── template_test.txt
│
├── .dev/                    ⚠️ 維護者專區 - 單元測試與開發文檔
│   ├── tests/               ← 單元測試套件 (150+ 測試案例)
│   │   ├── test_util.py            ← runner/util.py 的測試
│   │   ├── test_case_runner.py     ← runner/case_runner.py 的測試
│   │   ├── test_test_runner.py     ← runner/test_runner.py 的測試
│   │   ├── test_complexity_estimator.py  ← 複雜度估算器測試
│   │   ├── test_edge_cases.py      ← 邊界條件測試
│   │   ├── test_integration.py     ← 端到端整合測試
│   │   └── README.md               ← 測試詳細說明
│   │
│   ├── run_tests.bat        ← Windows: 運行單元測試
│   ├── run_tests.sh         ← Linux/macOS: 運行單元測試
│   │
│   ├── TESTING.md           ← 完整測試文檔
│   ├── TEST_SUMMARY.md      ← 測試套件摘要
│   └── README.md            ← 維護者指南
│
├── leetcode/                ← Python 虛擬環境 (Python 3.11)
│
├── pytest.ini               ← pytest 配置 (用於單元測試)
│
├── run_tests.bat            ← Windows: 執行所有測資
├── run_case.bat             ← Windows: 執行單一測資
├── new_problem.bat          ← Windows: 建立新題目
│
├── run_tests.sh             ← Linux/macOS: 執行所有測資
├── run_case.sh              ← Linux/macOS: 執行單一測資
├── new_problem.sh           ← Linux/macOS: 建立新題目
│
├── requirements.txt         ← Python 相依套件
└── README.md
```

> **📝 注意**: 
> - **一般使用者**：只需關注 `solutions/`, `tests/`, `runner/` 和根目錄的執行腳本
> - **專案維護者**：`.dev/` 資料夾包含單元測試和維護文檔，用於確保代碼重構不會破壞現有功能

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

# 安裝相依套件
pip install -r requirements.txt
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

# 安裝相依套件
pip install -r requirements.txt

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
# 失敗的測資會儲存到 tests/ 目錄，檔名為 {problem}_failed_{n}.in
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
| `tests/*_failed_*.in` | 自動生成 | 使用 `--save-failed` 時自動儲存失敗測資 |

---

## 📈 時間複雜度估算

使用 big_O 函式庫自動估算演算法的時間複雜度。

### 設計理念

**簡單且通用** - 只需在 generator 中新增一個函式：

| 函式 | 用途 | 必要 |
|------|------|------|
| `generate(count, seed)` | 功能測試的隨機測資 | ✅ 必要 |
| `generate_for_complexity(n)` | 複雜度估算的可控大小測資 | 可選 |

估算器內部使用 **Mock stdin** 方式：
- ✅ 通用 - 只要解答有 `solve()` 函式即可
- ✅ 無 subprocess 開銷
- ✅ 維持 stdin 抽象設計

### 使用方法

```bash
# 估算複雜度（需要 generator 中有 generate_for_complexity）
python runner/test_runner.py 0004_median_of_two_sorted_arrays --estimate

# 與其他參數組合使用
python runner/test_runner.py 0004 --all --benchmark --estimate
```

### Generator 範例

```python
# generators/0004_median_of_two_sorted_arrays.py

# 必要：隨機測資生成
def generate(count: int, seed: Optional[int] = None) -> Iterator[str]:
    """隨機大小 - 測試功能正確性"""
    for _ in range(count):
        m = random.randint(0, 1000)
        n = random.randint(0, 1000)
        yield _generate_case(m, n)


# 可選：啟用複雜度估算
def generate_for_complexity(n: int) -> str:
    """
    生成特定輸入大小的測資。
    
    對於此題，n = 總元素數量（m + n）
    """
    m = random.randint(0, n)
    return _generate_case(m, n - m)
```

### 輸出範例

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

### 需求

| 元件 | 必要 | 說明 |
|------|------|------|
| `big-O` 套件 | ✅ | `pip install big-O` |
| `generate_for_complexity(n)` | ✅ | 接收大小 `n` 並回傳測資輸入的函式 |

### 適合的題目類型

並非所有題目都適合時間複雜度估算。估算在以下情況效果最佳：

| ✅ 適合 | ❌ 不適合 |
|---------|----------|
| 輸入大小 `n` 可連續變化（10, 100, 1000...）| 輸入大小有硬性限制（如 n ≤ 9）|
| 執行時間隨輸入大小增長 | 執行時間被固定開銷主導 |
| 線性、對數、多項式複雜度 | 階乘/指數複雜度且 n 上限很小 |

**範例：**

| 題目 | 適合？ | 原因 |
|------|--------|------|
| Two Sum | ✅ | n 可以是 10 ~ 10000，O(n) 明顯增長 |
| Longest Substring | ✅ | 字串長度可大幅變化 |
| Merge k Sorted Lists | ✅ | 總元素 N 可以擴展 |
| N-Queens (0051) | ❌ | n ≤ 9（階乘爆炸），無法有意義地變化大小 |
| Rotting Oranges (0994) | ❌ | 網格大小有限，BFS 時間受網格結構主導 |
| Sudoku Solver | ❌ | 固定 9x9 網格，回溯複雜度 |

> **提示**：只有當 `n` 可以有意義地從小（10）變化到大（1000+）時，才在 generator 中加入 `generate_for_complexity(n)`。

### 向後兼容

- **解答檔案**：不需更動（需有 `solve()` 函式）
- **現有 generator**：無需更動仍可運作
- **新功能**：新增 `generate_for_complexity(n)` 以啟用估算

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
- **相依套件**: 見 `requirements.txt`

### 安裝相依套件

```bash
# 先啟動虛擬環境，然後：
pip install -r requirements.txt
```

| 套件 | 必要 | 說明 |
|------|------|------|
| `debugpy` | ✅ | VS Code Debug 支援 |
| `big-O` | 可選 | 時間複雜度估算 |

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

## 🔧 維護者專區（單元測試）

> ⚠️ **專為專案維護者和貢獻者** - 一般使用者可以跳過此部分

`.dev/` 資料夾包含完整的**單元測試套件**和維護文檔，用於確保代碼重構不會破壞現有功能。

### 測試統計

- **測試案例**: 150+ 個
- **測試覆蓋率**: 80-100%
- **測試類型**: 單元測試、邊界測試、整合測試

### 快速使用

```bash
# 1. 啟動虛擬環境
# Windows
leetcode\Scripts\activate

# Linux/Mac
source leetcode/bin/activate

# 2. 安裝測試依賴
pip install pytest pytest-cov

# 3. 運行所有單元測試
cd .dev
run_tests.bat          # Windows
./run_tests.sh         # Linux/Mac

# 4. 生成覆蓋率報告
cd ..
leetcode\Scripts\python.exe -m pytest .dev/tests --cov=runner --cov-report=html  # Windows
leetcode/bin/python -m pytest .dev/tests --cov=runner --cov-report=html  # Linux/Mac
```

### 詳細文檔

- **[.dev/README.md](.dev/README.md)** - 維護者指南
- **[.dev/TESTING.md](.dev/TESTING.md)** - 完整測試文檔
- **[.dev/TEST_SUMMARY.md](.dev/TEST_SUMMARY.md)** - 測試摘要

### 測試目的

這些測試確保：
- ✅ 重構不會破壞現有功能
- ✅ 給定相同輸入 → 永遠相同輸出
- ✅ 邊界條件（空輸入、錯誤輸入、大資料）都被覆蓋

**測試負責人**: luffdev

---

## 🏗️ Runner 模組架構（開發者專區）

> ⚠️ **供貢獻者和維護者參考** - 一般使用者可以跳過此部分

`runner/` 目錄包含模組化的測試執行元件：

### 模組總覽

```
runner/
├── test_runner.py         # CLI 入口點與主流程
├── module_loader.py       # 動態載入 solution/generator 模組
├── executor.py            # 測試案例執行（subprocess 管理）
├── reporter.py            # 結果格式化與效能報告
├── compare.py             # 輸出比較邏輯（exact/sorted/set/judge）
├── paths.py               # 路徑工具函式
├── io_utils.py            # 檔案 I/O 操作
├── util.py                # Re-exports（向後兼容）
├── complexity_estimator.py # 時間複雜度估算（big_O 整合）
└── case_runner.py         # 單一案例執行器（Debug 用）
```

### 模組職責

| 模組 | 行數 | 職責 |
|------|------|------|
| `compare.py` | ~190 | 輸出比較：`normalize_output`, `compare_outputs`, `compare_result`, `_compare_sorted`, `_compare_set` |
| `paths.py` | ~30 | 路徑建構：`get_solution_path`, `get_test_input_path`, `get_test_output_path` |
| `io_utils.py` | ~45 | 檔案操作：`read_file`, `write_file`, `file_exists`, `print_diff` |
| `module_loader.py` | ~65 | 動態匯入：`load_solution_module`, `load_generator_module` |
| `executor.py` | ~120 | 測試執行：`run_one_case`, `run_generated_case` |
| `reporter.py` | ~160 | 輸出格式：`truncate_input`, `format_validation_label`, `save_failed_case`, `print_benchmark_summary`, `run_method_tests` |
| `test_runner.py` | ~310 | CLI 與協調：參數解析、主流程 |
| `complexity_estimator.py` | ~300 | 複雜度估算：`ComplexityEstimator`，Mock stdin 方法 |
| `case_runner.py` | ~60 | 單一案例 Debug |

### 向後兼容

重構後的模組保持完整的向後兼容性：

```python
# 舊的 import 方式仍然有效：
from runner.util import normalize_output, compare_result
from runner.test_runner import run_one_case, load_solution_module

# 新的直接 import 方式（新程式碼推薦使用）：
from runner.compare import normalize_output, compare_result
from runner.executor import run_one_case
from runner.module_loader import load_solution_module
```

### 相依關係圖

```
test_runner.py (CLI 入口)
    ├── module_loader.py
    ├── executor.py ──────────┐
    ├── reporter.py ──────────┼──→ compare.py
    └── complexity_estimator.py

util.py (re-exports)
    ├── compare.py
    ├── paths.py
    └── io_utils.py
```

### 單元測試

所有模組都有 `.dev/tests/` 中的特徵測試覆蓋：

```bash
# 執行所有單元測試
leetcode\Scripts\python.exe -m pytest .dev/tests -v  # Windows
leetcode/bin/python -m pytest .dev/tests -v          # Linux/macOS
```

---

## 📜 License

MIT License - 自由使用於個人學習


# 🧩 NeetCode 練習框架

<!-- 
SEO: leetcode, algorithm, data structure, coding interview, FAANG, competitive programming, neetcode, 
     blind 75, python, mind map, pattern, dynamic programming, interview preparation, knowledge graph
AEO/GEO: 可擴展的 Python 框架，結合知識圖譜驅動學習、AI 心智圖、工業級測試與模式學習，助你精通演算法。
-->

[![GitHub stars](https://img.shields.io/github/stars/lufftw/neetcode?style=for-the-badge&logo=github&color=gold)](https://github.com/lufftw/neetcode/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/lufftw/neetcode?style=for-the-badge&logo=github&color=silver)](https://github.com/lufftw/neetcode/network)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/GPT--Powered-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/)
[![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
[![pytest](https://img.shields.io/badge/150%2B%20Tests-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](.dev/tests/)
[![PRs Welcome](https://img.shields.io/badge/PRs-歡迎-brightgreen?style=flat-square&logo=git&logoColor=white)](https://github.com/lufftw/neetcode/pulls)

---

### 🎯 停止死背。開始工程化。

**一個可擴展的 Python 框架，將 LeetCode 風格的演算法練習轉化為知識圖譜驅動、資料驅動、可測試且高效能的工作流程 — 搭配 AI 心智圖、工業級測試與模式學習，幫助開發者更快成長、更深入理解演算法。**

[📚 文件](https://lufftw.github.io/neetcode/) • [🤖 AI 心智圖](https://lufftw.github.io/neetcode/mindmaps/neetcode_ontology_ai_en.html) • [🧠 互動式心智圖](https://lufftw.github.io/neetcode/mindmaps/) • [🚀 快速開始](#-快速開始) • [📐 模式](docs/patterns/)

[English](README.md) | [繁體中文](README_zh-TW.md)

---

**Topics:** `knowledge-graph` `ai-powered` `mind-map` `pattern-recognition` `leetcode` `neetcode-150` `blind-75` `stress-testing` `algorithm-engineering` `performance-benchmarking` `data-driven-testing` `random-test-generation` `judge-function` `algorithm-debugging` `competitive-programming` `python` `vscode-integration` `test-automation` `coding-interview`

---

## 💎 核心理念

> **「精通演算法不是死背 300 道題 — 而是內化 15 個核心模式，並精準知道何時應用每一個。」**

本框架體現三大變革性原則：

### 🧬 知識圖譜架構

傳統 LeetCode 練習將問題視為孤立單元。我們建立了**互聯的本體論系統**：

- **API 核心** 定義可重用的演算法基元（`SubstringSlidingWindow`、`GridBFS`、`BacktrackExplore`）
- **模式** 將核心組合成更高層次的策略
- **問題家族** 揭示 300+ 題目之間的結構關聯
- **AI 合成** 發現人類遺漏的非顯性連結

*這是專家的思維方式 — 用抽象思考，而非記憶解答。*

### ⚙️ 生產級驗證

你的解法通過了 LeetCode 測試。但它*正確*嗎？它*最優*嗎？我們提供 **ICPC/Codeforces 等級的測試基礎設施**：

| 能力 | 驗證什麼 |
|:-----|:---------|
| 🎲 **帶 Seed 隨機生成** | 你的程式碼能處理你從未想過的測資 |
| ⚖️ **自訂 Judge 函式** | 多個正確答案都能通過 |
| 📊 **多解法效能比較** | 哪種方法*實際上*更快 |
| 📈 **經驗複雜度估算** | 驗證你宣稱的 O(n log n) |

*這是 Google 工程師的驗證方式 — 透過窮盡、可重現的測試。*

### 🤖 AI 增強理解

我們不只儲存知識 — 我們**合成洞見**：

- AI 分析整個本體論，生成**創意、互聯的心智圖**
- 多視角合成：架構師 × 教授 × 工程師 × 競賽選手
- 問題連結到 **GitHub 解答**（如有）或 **LeetCode**（後備）

*這是下一代的學習方式 — 以 AI 作為思考夥伴。*

---

## 🌟 我們的獨特之處

> 💡 **「優秀程式設計師與頂尖高手的差異，不在於選擇什麼演算法 — 而在於如何證明它是對的。」**

| 📦 其他 LeetCode 專案 | 🚀 NeetCode |
|:----------------------|:------------|
| ❌ 複製解答，祈禱能過 | ✅ **證明**你的解法是正確的 |
| ❌ 只有手動測資 | ✅ 自動生成 1000+ 筆測資 |
| ❌ 無法比較不同方法 | ✅ 並排比較 N 種解法效能 |
| ❌ 盲目背誦模式 | ✅ 用心智圖**視覺化**模式 |
| ❌ 沒有系統化學習路徑 | ✅ 結構化路線圖 (NeetCode 150, Blind 75) |

### 🧠 知識圖譜優勢

大多數人孤立地練習演算法。我們建立了**互聯的知識系統**：

| 心智圖 | 說明 | 連結 |
|:-------|:-----|:----:|
| 🤖 **AI 本體論分析** | AI 深度模式合成 | [🔗 EN](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_ai_en.html) · [🔗 中文](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_ai_zh-TW.html) |
| 📐 **模式階層** | API 核心 → 模式 → 解法 | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/pattern_hierarchy.html) |
| 👨‍👩‍👧‍👦 **家族衍生** | 基礎模板 → 衍生變體 | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/family_derivation.html) |
| ⚡ **演算法使用** | 知道哪個演算法適用於哪裡 | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/algorithm_usage.html) |
| 🏢 **公司覆蓋** | 針對特定公司精準準備 | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/company_coverage.html) |
| 🗺️ **學習路線圖** | 遵循經過驗證的路徑 (NeetCode 150, Blind 75 等) | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/roadmap_paths.html) |

**[→ 探索 10+ 互動式心智圖](https://lufftw.github.io/neetcode/mindmaps/)**

### ⚙️ 工業級測試能力

建立在 **Codeforces、ICPC 和 Google 工程實踐**的基礎上：

| 功能 | 作用 | 重要性 |
|:-----|:-----|:-------|
| 🎲 **隨機測資生成** | 帶 Seed 的生成器確保可重現 | 找出你從未想過的邊界條件 |
| ⚖️ **自訂 Judge 函式** | ICPC 風格驗證邏輯 | 多個正確答案？沒問題 |
| 📊 **多解法效能比較** | 自動比較 N 種方法 | 知道哪個*真正*更快 |
| 📈 **複雜度估算** | 經驗性 Big-O 分析 | 驗證你的理論宣稱 |
| 🔧 **VS Code 整合** | 一鍵除錯、Tasks、快捷鍵 | 像除錯真正軟體一樣除錯演算法 |

---

## 📑 目錄

- [核心理念](#-核心理念)
- [我們的獨特之處](#-我們的獨特之處)
- [為什麼選擇這個框架？](#-為什麼選擇這個框架)
- [快速開始](#-快速開始)
- [核心功能](#-核心功能)
- [互動式心智圖](#-互動式心智圖)
- [AI 心智圖生成](#-ai-心智圖生成)
- [模式文件](#-模式文件)
- [使用指南](#-使用指南)
- [進階功能](#-進階功能)
- [專案架構](#-專案架構)
- [常見問題](#-常見問題)
- [貢獻者專區](#-貢獻者專區)
- [授權條款](#-授權條款)

---

## ⭐ 為什麼選擇這個框架？

### 傳統練習的問題

你在 LeetCode 上解了一道題。通過了。但你*真的*知道你的解法是正確的嗎？那麼：

- 你沒測試的空輸入邊界條件呢？
- 只有在大 N 時才出現的微妙 off-by-one 錯誤呢？
- 你宣稱的 O(n log n) 是真的嗎？

**傳統練習無法回答這些問題。** 這個框架給你明確的答案。

### 我們的獨特之處

| 功能 | 本框架 | 一般專案 |
|:-----|:-----:|:-------:|
| **可重現隨機測資** | ✅ 帶 Seed 生成器 | ❌ 僅手動 |
| **自訂 Judge 函式** | ✅ ICPC/Codeforces 風格 | ❌ 字串比對 |
| **多解法效能比較** | ✅ 比較 N 種方法 | ❌ 單一解法 |
| **VS Code 整合** | ✅ Tasks、Debug、快捷鍵 | ❌ 僅 CLI |
| **壓力測試** | ✅ 生成 1000+ 測資 | ❌ 有限 |
| **複雜度估算** | ✅ 自動 Big-O 分析 | ❌ 無 |

### 為卓越而生

| 對象 | 我們如何幫助 |
|:-----|:------------|
| 🏆 **競程選手** | 像 Codeforces 大師一樣訓練 — 壓力測試直到程式崩潰，然後修復它 |
| 💼 **FAANG 工程師** | 透過證明你的解法有效來建立面試信心，而非只是祈禱它能過 |
| 🎓 **資工學生** | 用正確的方式學習演算法 — 透過實驗，而非死記 |
| 👨‍🏫 **教育者** | 給學生工業級工具來驗證他們的理解 |
| 🔬 **研究人員** | 用可重現的方法大規模評測演算法變體 |

---

## 🚀 快速開始

### 1. 環境設定

<details>
<summary><strong>Windows (PowerShell)</strong></summary>

```powershell
# 進入專案目錄
cd C:\path\to\neetcode

# 安裝 Python 3.11（如果需要）
py install 3.11

# 建立並啟動虛擬環境
py -3.11 -m venv leetcode
leetcode\Scripts\activate

# 安裝相依套件
pip install -r requirements.txt
```

</details>

<details>
<summary><strong>Linux / macOS</strong></summary>

```bash
# 使用 pyenv（推薦）
pyenv install 3.11
pyenv local 3.11

# 建立並啟動虛擬環境
python -m venv leetcode
source leetcode/bin/activate

# 安裝相依套件
pip install -r requirements.txt

# 設定腳本執行權限
chmod +x run_tests.sh run_case.sh new_problem.sh
```

</details>

### 2. 建立第一個題目

```bash
# Windows
new_problem.bat 0001_two_sum

# Linux/macOS
./new_problem.sh 0001_two_sum
```

這會自動建立：
- `solutions/0001_two_sum.py` — 你的解答檔案
- `tests/0001_two_sum_1.in` — 測試輸入
- `tests/0001_two_sum_1.out` — 預期輸出

### 3. 執行測試

```bash
# Windows
run_tests.bat 0001_two_sum

# Linux/macOS
./run_tests.sh 0001_two_sum
```

### 4. 在 VS Code 中除錯

1. 開啟 `solutions/` 中的任一解答檔案
2. 按 `F5` 以 test case #1 進行除錯
3. 或按 `Ctrl+Shift+B` 執行所有測試

**完成！** 你已經準備好開始解題了。🎉

---

## ✨ 核心功能

| 功能 | 說明 |
|:-----|:-----|
| 🧪 **自動化測試** | 自動執行多筆測資，清晰的通過/失敗報告與計時 |
| 🎲 **隨機測資生成** | 帶 Seed 確保可重現，支援 1000+ 筆壓力測試，自動儲存失敗測資 |
| ⚖️ **自訂 Judge 函式** | 驗證多個正確答案，ICPC 風格驗證，可不需要預期輸出 |
| 📊 **效能分析** | 多解法效能比較，自動時間複雜度估算，並排比較表格 |
| 🔧 **VS Code 整合** | 一鍵執行測試，整合除錯功能，自訂 Tasks 與快捷鍵 |
| 🧠 **互動式心智圖** | 視覺化演算法模式，追蹤學習進度 — [探索 →](https://lufftw.github.io/neetcode/mindmaps/) |

---

## 🧠 互動式心智圖

視覺化演算法模式、問題關聯和學習路徑：

### 🤖 AI 驅動的本體論分析（NEW！）

> **「讓 AI 合成人類需要數年才能內化的知識。」**

我們的 **AI 本體論分析器** 處理整個知識圖譜 — API 核心、模式、演算法、資料結構、問題家族 — 生成**創意、互聯的心智圖**，揭示人工策劃清單遺漏的洞見。

| 語言 | 說明 | 連結 |
|:-----|:-----|:-----|
| **English** | AI 合成的模式關聯 | [靜態](docs/mindmaps/neetcode_ontology_ai_en.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_ai_en.html) |
| **繁體中文** | AI 智能分析模式關聯 | [靜態](docs/mindmaps/neetcode_ontology_ai_zh-TW.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_ai_zh-TW.html) |

**特色：**
- 🧬 **深度模式合成** — AI 識別模式之間的非顯性連結
- 🎯 **智能連結** — 問題連結到 GitHub 解答（如有）或 LeetCode
- 🌐 **多語言** — 支援英文和繁體中文
- ♻️ **可重新生成** — 執行 `python tools/generate_mindmaps_ai.py` 產生新洞見

---

### 📚 精選心智圖

| 心智圖 | 說明 | 連結 |
|:-------|:-----|:-----|
| 📐 **模式階層** | API 核心 → 模式 → 問題 | [靜態](docs/mindmaps/pattern_hierarchy.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/pattern_hierarchy.html) |
| 👨‍👩‍👧‍👦 **家族衍生** | 基礎模板 → 衍生變體 | [靜態](docs/mindmaps/family_derivation.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/family_derivation.html) |
| ⚡ **演算法使用** | 依演算法分類問題 | [靜態](docs/mindmaps/algorithm_usage.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/algorithm_usage.html) |
| 🏗️ **資料結構使用** | 依資料結構分類問題 | [靜態](docs/mindmaps/data_structure.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/data_structure.html) |
| 🏢 **公司覆蓋** | 各公司常見問題 | [靜態](docs/mindmaps/company_coverage.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/company_coverage.html) |
| 🗺️ **學習路線圖** | NeetCode 150、Blind 75 等 | [靜態](docs/mindmaps/roadmap_paths.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/roadmap_paths.html) |
| 🔗 **問題關聯** | 相關問題網絡 | [靜態](docs/mindmaps/problem_relations.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/problem_relations.html) |
| 🔀 **解法變體** | 多種解法方式 | [靜態](docs/mindmaps/solution_variants.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/solution_variants.html) |
| 📊 **難度 × 主題** | 依難度分類主題 | [靜態](docs/mindmaps/difficulty_topics.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/difficulty_topics.html) |

👉 **[查看所有互動式心智圖](https://lufftw.github.io/neetcode/mindmaps/)**

---

## 📐 模式文件

> **「不要死背 200 道題。掌握 10 個模式。」**

每個 API 核心都有專屬的模式指南，包含**基礎模板**、**變體**和**可直接複製的程式碼**。

| API 核心 | 指南 | 題目 |
|:---------|:----:|:-----|
| `SubstringSlidingWindow` | [📖](docs/patterns/sliding_window.md) | LeetCode 3, 76, 159, 209, 340, 438, 567 |
| `GridBFSMultiSource` | *即將推出* | LeetCode 994, 286, 542 |
| `BacktrackingExploration` | *即將推出* | LeetCode 51, 52, 46, 78 |
| `KWayMerge` | *即將推出* | LeetCode 23, 21, 88 |
| `BinarySearchBoundary` | *即將推出* | LeetCode 4, 33, 34, 35 |

👉 **[查看所有模式指南 →](docs/patterns/README.md)**

---

## 📖 使用指南

### ⌨️ VS Code 整合

**鍵盤快捷鍵：**

| 快捷鍵 | 動作 |
|:-------|:-----|
| `Ctrl+Shift+B` | 執行當前檔案的所有測試 |
| `F5` | 以 test case #1 進行除錯 |

> **注意：** 使用快捷鍵前，請先開啟 `solutions/` 中的解答檔案。

**可用 Tasks**（`Ctrl+Shift+P` → "Tasks: Run Task"）：

| Task | 說明 |
|:-----|:-----|
| Run all tests | 執行所有測資 |
| Run case #1 / #2 / #3 | 執行特定測資 |
| Benchmark | 顯示執行時間 |
| Run all solutions | 比較所有實作 |
| Run with generated (10) | 靜態 + 10 筆生成測資 |
| Run generated only | 跳過靜態測資 |
| Save failed cases | 自動儲存失敗輸入 |

### 💻 命令列介面

```bash
# 執行所有測資
python runner/test_runner.py <problem_name>

# 執行特定測資
python runner/case_runner.py <problem_name> <case_number>

# 執行並計時
python runner/test_runner.py <problem_name> --benchmark

# 執行所有解法
python runner/test_runner.py <problem_name> --all

# 生成隨機測資
python runner/test_runner.py <problem_name> --generate 10

# 估算時間複雜度
python runner/test_runner.py <problem_name> --estimate
```

### 📝 解答檔案格式

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
    
    # 解析輸入
    nums = list(map(int, lines[0].split(',')))
    target = int(lines[1])
    
    # 執行解答
    result = Solution().twoSum(nums, target)
    print(result)

if __name__ == "__main__":
    solve()
```

### 📋 測資檔案格式

| 規格 | 要求 |
|:-----|:-----|
| 換行符號 | **LF**（Unix 格式，`\n`）|
| 編碼 | UTF-8 |
| 檔案結尾 | 以單一換行結尾 |
| 命名規則 | `{題號}_{題名}_{編號}.in/.out` |

**輸入檔**（`tests/0001_two_sum_1.in`）：
```
2,7,11,15
9
```

**輸出檔**（`tests/0001_two_sum_1.out`）：
```
[0, 1]
```

---

## 🔧 進階功能

### 🚀 多解法效能比較

比較同一題目的多種解法：

```python
# solutions/0023_merge_k_sorted_lists.py

SOLUTIONS = {
    "default": {
        "method": "mergeKLists_heap",
        "complexity": "O(N log k)",
        "description": "最小堆方法"
    },
    "divide": {
        "method": "mergeKLists_divide",
        "complexity": "O(N log k)",
        "description": "分治法"
    },
    "greedy": {
        "method": "mergeKLists_greedy",
        "complexity": "O(kN)",
        "description": "貪婪比較"
    },
}

class Solution:
    def mergeKLists_heap(self, lists):
        # 堆實作
        pass
    
    def mergeKLists_divide(self, lists):
        # 分治實作
        pass
    
    def mergeKLists_greedy(self, lists):
        # 貪婪實作
        pass
```

**執行指令：**

```bash
# 執行特定解法
python runner/test_runner.py 0023_merge_k_sorted_lists --method heap

# 比較所有解法
python runner/test_runner.py 0023_merge_k_sorted_lists --all --benchmark
```

**輸出：**

```
============================================================
📊 效能比較
============================================================
Method               Avg Time     Complexity      Pass Rate
------------------------------------------------------------
heap                    44.36ms   O(N log k)      3/3
divide                  44.48ms   O(N log k)      3/3
greedy                  44.82ms   O(kN)           3/3
============================================================
```

<details>
<summary><strong>進階：Wrapper 模式（多個類別使用相同方法名）</strong></summary>

當需要多個類別使用相同方法名稱時：

```python
class SolutionRecursive:
    def reverseKGroup(self, head, k):
        pass  # 遞迴實作

class SolutionIterative:
    def reverseKGroup(self, head, k):
        pass  # 迭代實作

# Wrapper 函式
def solve_recursive(head, k):
    return SolutionRecursive().reverseKGroup(head, k)

def solve_iterative(head, k):
    return SolutionIterative().reverseKGroup(head, k)

SOLUTIONS = {
    "default": {"method": "solve_iterative", ...},
    "recursive": {"method": "solve_recursive", ...},
}
```

使用模板建立：`new_problem.bat 0025_reverse_nodes --wrapper`

</details>

### 🔀 彈性輸出驗證

適用於有多個正確答案的題目（「可以任意順序回傳」）：

**驗證模式：**

| 模式 | 說明 | 需要 `.out` |
|:-----|:-----|:----------:|
| `[judge]` | 自訂驗證搭配參考答案 | ✅ |
| `[judge-only]` | 純自訂驗證 | ❌ |
| `[exact]` | 精確字串比對 | ✅ |
| `[sorted]` | 排序後比對 | ✅ |
| `[set]` | 集合比對 | ✅ |

**JUDGE_FUNC（推薦）：**

```python
def judge(actual: list, expected, input_data: str) -> bool:
    """驗證 N-Queens 解答。"""
    n = int(input_data.strip())
    
    # 驗證每個棋盤
    for board in actual:
        if not is_valid_n_queens(board, n):
            return False
    
    # 如果有預期答案，檢查數量
    if expected is not None:
        return len(actual) == len(expected)
    
    return True

JUDGE_FUNC = judge
```

**COMPARE_MODE（簡單情況）：**

```python
COMPARE_MODE = "sorted"  # 選項："exact" | "sorted" | "set"
```

### 🎲 隨機測資生成

建立與解答同名的生成器檔案：

```python
# generators/0004_median_of_two_sorted_arrays.py
import random
from typing import Iterator, Optional

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """生成隨機測資。"""
    if seed is not None:
        random.seed(seed)
    
    # 邊界測資優先
    yield "[]\n[1]"
    yield "[1]\n[]"
    
    # 隨機測資
    for _ in range(count - 2):
        m = random.randint(0, 1000)
        n = random.randint(0, 1000)
        nums1 = sorted(random.randint(-10**6, 10**6) for _ in range(m))
        nums2 = sorted(random.randint(-10**6, 10**6) for _ in range(n))
        yield f"{list(nums1)}\n{list(nums2)}".replace(' ', '')
```

**使用方式：**

```bash
# 執行靜態 + 生成測資
python runner/test_runner.py 0004_median --generate 10

# 只執行生成測資
python runner/test_runner.py 0004_median --generate-only 100

# 可重現的 seed
python runner/test_runner.py 0004_median --generate 10 --seed 42

# 儲存失敗測資
python runner/test_runner.py 0004_median --generate 10 --save-failed
```

### 📈 時間複雜度估算

新增複雜度生成器函式：

```python
# generators/0004_median_of_two_sorted_arrays.py

def generate_for_complexity(n: int) -> str:
    """生成特定大小 n 的測資。"""
    m = random.randint(0, n)
    return _generate_case(m, n - m)
```

**執行估算：**

```bash
python runner/test_runner.py 0004_median --estimate
```

**輸出：**

```
📈 執行複雜度估算...
   Sizes: [10, 20, 50, 100, 200, 500, 1000, 2000]
   n=   10: 0.0040ms
   n=  100: 0.0082ms
   n= 1000: 0.0685ms
   n= 2000: 0.1796ms

✅ 估算結果：O(n log n)
   信心度：1.00
```

---

## 📁 專案架構

```
neetcode/
│
├── solutions/                 # 📝 你的解答檔案
│   └── 0001_two_sum.py
│
├── tests/                     # 📋 測試案例
│   ├── 0001_two_sum_1.in      # 輸入檔
│   ├── 0001_two_sum_1.out     # 預期輸出
│   └── *_failed_*.in          # 自動儲存的失敗測資 (--save-failed)
│
├── generators/                # 🎲 隨機測資生成器（可選）
│   └── 0001_two_sum.py        # generate(count, seed) 函式
│
├── runner/                    # ⚙️ 測試執行引擎
│   ├── test_runner.py         # CLI 入口點 & 主要流程
│   ├── case_runner.py         # 單一測資執行器（除錯用）
│   ├── executor.py            # 測試案例執行（subprocess）
│   ├── compare.py             # 輸出比較（exact/sorted/set/judge）
│   ├── reporter.py            # 結果格式化 & 效能報告
│   ├── module_loader.py       # 動態模組載入
│   ├── complexity_estimator.py # 時間複雜度估算（big_O）
│   ├── paths.py               # 路徑工具
│   ├── io_utils.py            # 檔案 I/O 操作
│   └── util.py                # Re-exports（向後兼容）
│
├── templates/                 # 📄 題目模板
│   ├── template_solution.py          # 單一解法
│   ├── template_solution_multi.py    # 多解法（單一類別）
│   └── template_solution_wrapper.py  # 多解法（Wrapper 模式）
│
├── .vscode/                   # 🔧 VS Code 整合
│   ├── settings.json          # Python 環境設定
│   ├── tasks.json             # Ctrl+Shift+B 快捷任務
│   └── launch.json            # F5 除錯配置
│
├── docs/                      # 📚 文件（MkDocs）
│   ├── index.md               # 首頁（English）
│   ├── index_zh-TW.md         # 首頁（繁體中文）
│   ├── mindmaps/              # 生成的心智圖 Markdown
│   ├── patterns/              # 生成的模式文件
│   ├── pages/                 # 生成的 HTML（gitignored）
│   └── stylesheets/           # 自訂 CSS
│
├── tools/                     # 🛠️ 工具腳本
│   ├── generate_mindmaps.py   # 生成心智圖
│   ├── generate_mindmaps.toml # 心智圖配置
│   ├── generate_pattern_docs.py # 生成模式文件
│   └── text_to_mindmap.py     # LLM 文字轉心智圖
│
├── ontology/                  # 🧬 演算法本體論（TOML）
│   ├── api_kernels.toml       # API 核心定義
│   ├── patterns.toml          # 模式定義
│   ├── algorithms.toml        # 演算法定義
│   ├── data_structures.toml   # 資料結構定義
│   ├── companies.toml         # 公司定義
│   ├── topics.toml            # 主題定義
│   ├── difficulties.toml      # 難度級別
│   ├── families.toml          # 問題家族定義
│   └── roadmaps.toml          # 路線圖定義
│
├── meta/                      # 📊 問題 & 模式元資料
│   ├── problems/              # 問題元資料（每題一個 TOML）
│   │   └── *.toml
│   └── patterns/              # 模式文件來源
│       └── <pattern_name>/    # 模式專屬 Markdown
│
├── roadmaps/                  # 🗺️ 學習路徑定義
│   ├── neetcode_150.toml
│   ├── blind_75.toml
│   └── sliding_window_path.toml
│
├── .dev/                      # 🧪 維護者專區（單元測試）
│   ├── tests/                 # 單元測試套件（150+ 案例）
│   ├── run_tests.bat/.sh      # 執行單元測試
│   ├── TESTING.md             # 測試文件
│   └── README.md              # 維護者指南
│
├── .github/                   # 🚀 GitHub 配置
│   └── workflows/
│       └── deploy-pages.yml   # GitHub Pages 部署
│
├── leetcode/                  # 🐍 Python 虛擬環境（3.11）
│
├── run_tests.bat / .sh        # 執行某題目的所有測試
├── run_case.bat / .sh         # 執行單一測資
├── new_problem.bat / .sh      # 從模板建立新題目
│
├── requirements.txt           # Python 相依套件
├── mkdocs.yml                 # MkDocs 配置
├── pytest.ini                 # pytest 配置
├── README.md                  # English 版
└── README_zh-TW.md            # 本檔案（繁體中文）
```

### 目錄指南

| 目錄 | 用途 | 對象 |
|:-----|:-----|:-----|
| `solutions/` | 在這裡撰寫解答 | ✅ 所有使用者 |
| `tests/` | 新增測資（.in/.out） | ✅ 所有使用者 |
| `generators/` | 隨機測資生成器 | ✅ 所有使用者 |
| `runner/` | 測試執行引擎 | 🔧 貢獻者 |
| `templates/` | 題目模板 | ✅ 所有使用者 |
| `.vscode/` | VS Code 配置 | ✅ 所有使用者 |
| `docs/` | MkDocs 文件 | 🔧 貢獻者 |
| `tools/` | 文件生成工具 | 🔧 貢獻者 |
| `ontology/` | 演算法本體論資料 | 🔧 貢獻者 |
| `meta/` | 問題/模式元資料 | 🔧 貢獻者 |
| `.dev/` | 單元測試（150+ 案例） | 🔧 維護者 |

> **📝 注意：** `docs/mindmaps/`、`docs/patterns/`、`docs/pages/` 中的檔案都是自動生成的。請編輯 `ontology/`、`meta/`、`tools/` 中的來源檔案。

---

## ❓ 常見問題

<details>
<summary><strong>這個框架解決什麼問題？</strong></summary>

- 自動執行多種演算法實作
- 生成可重現的隨機測資進行壓力測試
- 比較解法效能找出差異
- 使用 VS Code 整合除錯 LeetCode 風格題目
- 使用自訂邏輯驗證輸出，超越簡單檔案比對

</details>

<details>
<summary><strong>這和複製 LeetCode 解答有什麼不同？</strong></summary>

這不是解答集 — 而是**測試基礎設施**。你撰寫解答，框架會：

1. 用靜態測資執行測試
2. 自動生成隨機測資
3. 用自訂 Judge 函式驗證正確性
4. 比較多種解法效能
5. 經驗性估算時間複雜度

</details>

<details>
<summary><strong>可以用來準備面試嗎？</strong></summary>

當然可以！這個框架非常適合面試準備：

- 用**真正的 LeetCode 格式**練習撰寫解答
- 用隨機測資生成找出**你可能遺漏的邊界條件**
- 用效能比較看哪種方法**實際上更快**
- 用 VS Code 整合**輕鬆除錯**

</details>

<details>
<summary><strong>需要什麼 Python 版本？</strong></summary>

Python 3.11 — 與 [LeetCode 官方環境](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages) 一致。

</details>

---

## 🛠️ 貢獻者專區

### 執行單元測試

```bash
# 啟動虛擬環境
leetcode\Scripts\activate  # Windows
source leetcode/bin/activate  # Linux/macOS

# 執行所有測試
python -m pytest .dev/tests -v

# 含覆蓋率
python -m pytest .dev/tests --cov=runner --cov-report=html
```

### 本地生成心智圖

```bash
# 生成 Markdown 心智圖
python tools/generate_mindmaps.py

# 生成 HTML（互動式）心智圖
python tools/generate_mindmaps.py --html
```

配置檔：`tools/generate_mindmaps.toml`

### 文件

- [`.dev/README.md`](https://github.com/lufftw/neetcode/blob/main/.dev/README.md) — 維護者指南
- [`.dev/TESTING.md`](https://github.com/lufftw/neetcode/blob/main/.dev/TESTING.md) — 測試文件
- [`docs/GITHUB_PAGES_SETUP.md`](docs/GITHUB_PAGES_SETUP.md) — 部署指南

---

## 📜 授權條款

**MIT License** — 可自由用於個人學習與教育用途。

---

**為競程社群用 ❤️ 打造**

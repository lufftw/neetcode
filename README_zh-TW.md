# 🧩 NeetCode 練習框架

<!-- 
SEO: leetcode, algorithm, data structure, coding interview, FAANG, competitive programming, neetcode, 
     blind 75, python, mind map, pattern, dynamic programming, interview preparation, knowledge graph
AEO/GEO: 可擴展的 Python 框架，結合知識圖譜驅動學習、AI 心智圖、工業級測試與模式學習，助你精通演算法。
-->

[![GitHub stars](https://img.shields.io/github/stars/lufftw/neetcode?style=for-the-badge&logo=github&color=gold)](https://github.com/lufftw/neetcode/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/lufftw/neetcode?style=for-the-badge&logo=github&color=silver)](https://github.com/lufftw/neetcode/network)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://github.com/lufftw/neetcode/blob/main/LICENSE)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/GPT--Powered-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/)
[![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
[![pytest](https://img.shields.io/badge/150%2B%20Tests-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://github.com/lufftw/neetcode/tree/main/.dev/tests)
[![PRs Welcome](https://img.shields.io/badge/PRs-歡迎-brightgreen?style=flat-square&logo=git&logoColor=white)](https://github.com/lufftw/neetcode/pulls)

---

**解題。遺忘。重複。讓我們改變這個循環。**

### 🎯 建立演算法直覺

**NeetCode 是一個可擴展的 Python 演算法學習與面試準備框架 — 建立直覺與模式辨識能力，將想法轉化為清晰的實作，並累積*可驗證的證據*（測試、壓力案例、效能基準、複雜度檢查），讓你的進步是真實、可重複且面試就緒的。**

- **學習可遷移技能**：建模、狀態/不變量、邊界案例、複雜度意識，以及可重用的解題模板。
- **面試就緒的練習**：限時工作流程、邊寫邊解釋、減少「小錯誤」、更強的權衡討論。
- **證明正確性與穩健性**：靜態 + 種子隨機 + 邊界案例壓力測試、自訂判斷函數、失敗重現。
- **測量與比較**：基準測試多種實作並經驗性地估算複雜度。
- **看見全貌**：本體論 + AI 心智圖揭示模式關係與學習路徑。

[📚 文件](https://lufftw.github.io/neetcode/) • [🤖 AI 心智圖](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_agent_evolved_zh-TW.html) • [🧠 互動式心智圖](https://lufftw.github.io/neetcode/mindmaps/) • [🚀 快速開始](#-快速開始) • [📐 模式](docs/patterns/README.md) • [🧪 測試與驗證](docs/runner/README.md)

[English](https://lufftw.github.io/neetcode/) | [繁體中文](https://lufftw.github.io/neetcode/index_zh-TW/)

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
| 🤖 **AI 本體論分析 (Evolved)** | 由多代理（multi-agent）流程產生 | [🔗 EN](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_agent_evolved_en.html) · [🔗 中文](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_agent_evolved_zh-TW.html) |
| 🤖 **AI 本體論分析** | AI 深度模式合成 | [🔗 EN](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_ai_en.html) · [🔗 中文](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_ai_zh-TW.html) |
| 📐 **模式階層** | API 核心 → 模式 → 解法 | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/pattern_hierarchy.html) |
| 👨‍👩‍👧‍👦 **家族衍生** | 基礎模板 → 衍生變體 | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/family_derivation.html) |
| ⚡ **演算法使用** | 知道哪個演算法適用於哪裡 | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/algorithm_usage.html) |
| 🏢 **公司覆蓋** | 針對特定公司精準準備 | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/company_coverage.html) |
| 🗺️ **學習路線圖** | NeetCode 150、Blind 75 等 | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/roadmap_paths.html) |

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
chmod +x scripts/run_tests.sh scripts/run_case.sh scripts/new_problem.sh
```

</details>

### 2. 建立第一個題目

```bash
# Windows
scripts\new_problem.bat 0001_two_sum

# Linux/macOS
./scripts/new_problem.sh 0001_two_sum
```

這會自動建立：
- `solutions/0001_two_sum.py` — 你的解答檔案
- `tests/0001_two_sum_1.in` — 測試輸入
- `tests/0001_two_sum_1.out` — 預期輸出

### 3. 執行測試

```bash
# Windows
scripts\run_tests.bat 0001_two_sum

# Linux/macOS
./scripts/run_tests.sh 0001_two_sum
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
| 🧪 **測試與驗證引擎** | ⭐ **核心功能** — 自動化測試、效能基準測試、隨機測資生成、複雜度估算。詳見 [測試與驗證指南](docs/runner/README.md) |
| 🤖 **AI 本體論分析** | AI 驅動的知識圖譜合成 — 發現人類遺漏的模式關聯 |
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
| **English (Evolved)** | Generated via a multi-agent pipeline | [靜態](docs/mindmaps/neetcode_ontology_agent_evolved_en.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_agent_evolved_en.html) |
| **繁體中文 (Evolved)** | 由多代理（multi-agent）流程產生 | [靜態](docs/mindmaps/neetcode_ontology_agent_evolved_zh-TW.md) · [互動式 ✨](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_agent_evolved_zh-TW.html) |
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

## 🤖 AI 心智圖生成

> **「讓 AI 合成人類需要數年才能內化的知識。」**

### 兩種生成模式

| 模式 | 說明 | 快速開始 |
|:-----|:-----|:---------|
| **🤖 Evolved Agent** | 多專家精煉與共識投票 | `cd tools/ai-markmap-agent && python main.py` |
| **🤖 Basic AI** | 從知識圖譜單次合成 | `python tools/generate_mindmaps_ai.py` |

### 主要特色

- 🧬 **多專家合成** — 架構師 + 教授 + 工程師視角
- 🎯 **智能連結** — GitHub 解答（如有）→ LeetCode 後備
- 🌐 **多語言** — EN / 繁體中文
- ♻️ **可重新生成** — 版本歷史自動遞增

### 輸出檔案

| 類型 | 輸出路徑 |
|:-----|:---------|
| **Evolved** | `docs/mindmaps/neetcode_ontology_agent_evolved_{lang}.md` |
| **Basic** | `docs/mindmaps/neetcode_ontology_ai_{lang}.md` |
| **HTML** | `docs/pages/mindmaps/*.html` |

> 📖 **Evolved Agent**：詳見 [`tools/ai-markmap-agent/README.md`](docs/tools/ai-markmap-agent/README.md) 了解架構、專家角色與配置。
>
> 📖 **Basic AI**：詳見 [`tools/README.md`](docs/tools/README.md) 了解配置選項。

---

## 📐 模式文件

> **「不要死背 200 道題。掌握 10 個模式。」**

每個模式提供**兩條學習路徑**：

| 路徑 | 目的 | 適合對象 |
|:-----|:-----|:---------|
| 💡 **直覺理解** | 透過故事和視覺化解釋理解「為什麼」 | 初學者、建立心智模型 |
| 🛠️ **模板** | 生產級實作與問題專屬變體 | 面試準備、快速參考 |

| API 核心 | 學習資源 | 題目 |
|:---------|:---------|:-----|
| `SubstringSlidingWindow` | 💡 [直覺理解](docs/patterns/sliding_window/intuition.md) · 🛠️ [模板](docs/patterns/sliding_window/templates.md) | LeetCode 3, 76, 159, 209, 340, 438, 567 |
| `TwoPointersTraversal` | 💡 [直覺理解](docs/patterns/two_pointers/intuition.md) · 🛠️ [模板](docs/patterns/two_pointers/templates.md) | LeetCode 1, 11, 15, 16, 21, 26, 27, 75, 88, 125, 141, 142, 167, 202, 283, 680, 876 |
| `BacktrackingExploration` | 💡 [直覺理解](docs/patterns/backtracking_exploration/intuition.md) · 🛠️ [模板](docs/patterns/backtracking_exploration/templates.md) | LeetCode 39, 40, 46, 47, 51, 77, 78, 79, 90, 93, 131, 216 |
| `GridBFSMultiSource` | *即將推出* | LeetCode 994, 286, 542 |
| `KWayMerge` | *即將推出* | LeetCode 23, 21, 88 |
| `BinarySearchBoundary` | *即將推出* | LeetCode 4, 33, 34, 35 |
| `LinkedListInPlaceReversal` | *即將推出* | LeetCode 25, 206, 92 |
| `MonotonicStack` | *即將推出* | LeetCode 84, 85, 496 |

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

**常用 Tasks**（`Ctrl+Shift+P` → "Tasks: Run Task"）：

| Task | 說明 |
|:-----|:-----|
| Run all tests | 執行所有測資 |
| Run case #1 / #2 / #3 | 執行特定測資 |
| Benchmark | 顯示執行時間 |
| Run all solutions | 比較所有實作 |
| Run with generated (10) | 靜態 + 10 筆生成測資 |

> 📖 **完整參考**：詳見 [VSCode 設定指南](docs/contributors/VSCODE_SETUP.md) 以了解全部 14 個 Tasks、11 個 Debug 配置、工作流程範例與自訂設定。

### 💻 命令列介面

> 📖 **完整參考**：詳見 [測試與驗證指南](docs/runner/README.md) 以了解完整的 CLI 選項、使用範例與進階功能。這是驅動自動化測試、效能基準測試、隨機測資生成與複雜度估算的**核心測試引擎**。

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
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "twoSum",
        "complexity": "O(n) time, O(n) space",
        "description": "Single pass with hash map",
    },
}

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
    
    # 執行解答（多型派發）
    solver = get_solver(SOLUTIONS)
    result = solver.twoSum(nums, target)
    print(result)

if __name__ == "__main__":
    solve()
```

> 📖 完整規格請參見 [`docs/SOLUTION_CONTRACT.md`](docs/SOLUTION_CONTRACT.md)。

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

使用**多型模式**比較同一題目的多種解法：

```python
# solutions/0023_merge_k_sorted_lists.py
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionHeap",
        "method": "mergeKLists",
        "complexity": "O(N log k)",
        "description": "最小堆方法"
    },
    "divide": {
        "class": "SolutionDivideConquer",
        "method": "mergeKLists",
        "complexity": "O(N log k)",
        "description": "分治法"
    },
    "greedy": {
        "class": "SolutionGreedy",
        "method": "mergeKLists",
        "complexity": "O(kN)",
        "description": "貪婪比較"
    },
}

class SolutionHeap:
    def mergeKLists(self, lists):
        # 堆實作
        pass

class SolutionDivideConquer:
    def mergeKLists(self, lists):
        # 分治實作
        pass

class SolutionGreedy:
    def mergeKLists(self, lists):
        # 貪婪實作
        pass

def solve():
    # ... 解析輸入 ...
    solver = get_solver(SOLUTIONS)
    result = solver.mergeKLists(lists)
    print(result)
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

使用模板建立：`scripts\new_problem.bat 0023_merge_k_lists --multi`

> 📖 完整 SOLUTIONS schema 和驗證規則請參見 [`docs/SOLUTION_CONTRACT.md` §B](docs/SOLUTION_CONTRACT.md#solutions-metadata)。

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

> 📖 完整 JUDGE_FUNC 簽章和驗證規則請參見 [`docs/SOLUTION_CONTRACT.md` §C](docs/SOLUTION_CONTRACT.md#validation-judge_func--compare_mode)。

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

> 📖 完整生成器規格和最佳實踐請參見 [`docs/GENERATOR_CONTRACT.md`](docs/GENERATOR_CONTRACT.md)。

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
├── runner/                    # 🧪 核心測試與驗證引擎
│   ├── test_runner.py         # CLI 入口點 & 主要流程
│   ├── case_runner.py         # 單一測資執行器（除錯用）
│   ├── executor.py            # 測試案例執行（subprocess）
│   ├── compare.py             # 輸出比較（exact/sorted/set/judge）
│   ├── reporter.py            # 結果格式化 & 效能報告
│   ├── module_loader.py       # 動態模組載入
│   ├── complexity_estimator.py # 時間複雜度估算（big_O）
│   ├── paths.py               # 路徑工具
│   ├── io_utils.py            # 檔案 I/O 操作
│   ├── util.py                # Re-exports（向後兼容）
│   └── README.md              # 快速參考指南
│
│   📖 詳見 [測試與驗證指南](docs/runner/README.md) — 驅動自動化測試、效能基準測試、隨機測資生成與複雜度估算的核心引擎
│
├── templates/                 # 📄 題目模板
│   ├── template_solution.py       # 單一解法模板
│   ├── template_solution_multi.py # 多解法（多型模式）
│   └── template_test.txt          # 測資模板
│
├── .vscode/                   # 🔧 VS Code 整合
│   ├── settings.json          # Python 環境設定
│   ├── tasks.json             # Ctrl+Shift+B 快捷任務（14 個 Tasks）
│   └── launch.json            # F5 除錯配置（11 個配置）
│
│   📖 詳見 [VSCode 設定指南](docs/contributors/VSCODE_SETUP.md) — Tasks、Debug 配置、工作流程範例
│
├── docs/                      # 📚 文件（MkDocs）
│   ├── index.md               # 首頁（English）
│   ├── index_zh-TW.md         # 首頁（繁體中文）
│   ├── contributors/          # 維護者文件
│   │   ├── README.md          # 完整維護者指南
│   │   ├── TESTING.md         # 完整測試文件
│   │   ├── VSCODE_SETUP.md    # VS Code Tasks 與 Debug 配置
│   │   ├── VIRTUAL_ENV_SETUP.md  # 虛擬環境設定
│   │   └── DOCUMENTATION_ARCHITECTURE.md  # 文件架構
│   ├── tools/                 # 工具文件
│   │   ├── README.md          # 完整工具參考
│   │   ├── ai-markmap-agent/  # AI Markmap Agent 文件
│   │   ├── mindmaps/          # 心智圖生成器文件
│   │   └── patterndocs/       # 模式文件生成器文件
│   ├── mindmaps/              # 生成的心智圖 Markdown
│   ├── patterns/              # 生成的模式文件
│   ├── pages/                 # 生成的 HTML（gitignored）
│   ├── assets/                # 文件資源（圖片、CSS、JS）
│   ├── overrides/             # MkDocs 主題覆蓋
│   ├── getting-started/       # 快速開始指南
│   └── stylesheets/           # 自訂 CSS
│
├── tools/                     # 🛠️ 工具腳本
│   ├── generate_mindmaps_ai.py    # 🤖 AI 心智圖生成器
│   ├── generate_mindmaps_ai.toml     # AI 生成配置
│   ├── generate_mindmaps.py       # 規則式心智圖生成器
│   ├── generate_mindmaps.toml     # 規則式配置
│   ├── generate_pattern_docs.py   # 生成模式文件
│   ├── generate_pattern_docs.toml # 模式文件配置
│   ├── check_solutions.py         # 解答驗證工具
│   ├── prepare_llm_input.py       # 準備 LLM 輸入資料
│   ├── text_to_mindmap.py         # 文字轉心智圖
│   ├── ai-markmap-agent/          # 🤖 AI Markmap Agent（多代理流程）
│   │   ├── main.py                # 入口點
│   │   ├── src/                   # 原始碼（代理、配置等）
│   │   ├── prompts/               # 專家提示詞
│   │   ├── config/                # 配置檔案
│   │   └── outputs/               # 生成輸出
│   ├── mindmaps/                  # 心智圖生成器模組
│   ├── patterndocs/               # 模式文件生成器模組
│   ├── shared/                    # 共用工具
│   ├── hooks/                     # Pre-commit 掛鉤
│   ├── prompts/                   # AI 提示詞管理
│   │   ├── README.md              # 提示詞文件
│   │   └── generated/             # 自動生成的提示詞
│   ├── tests/                     # 格式驗證測試
│   └── outputs/                   # 工具輸出檔案（gitignored）
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
│   ├── tests_solutions/       # 解答驗證測試
│   ├── scripts/run_tests.bat/.sh  # 執行 runner 單元測試
│   ├── run_all_tests.bat/.sh  # 執行所有單元測試
│   ├── run_tests_solutions.bat/.sh  # 執行解答測試
│   ├── TESTING.md             # 測試文件
│   ├── VIRTUAL_ENV_SETUP.md   # 虛擬環境設定指南
│   └── README.md              # 維護者指南
│
├── .github/                   # 🚀 GitHub 配置
│   └── workflows/
│       └── deploy-pages.yml   # GitHub Pages 部署
│
├── leetcode/                  # 🐍 Python 虛擬環境（3.11）
│
├── scripts/                   # 🔧 工具腳本
│   ├── new_problem.bat / .sh  # 從模板建立新題目
│   ├── run_tests.bat / .sh    # 執行某題目的所有測試
│   ├── run_case.bat / .sh     # 執行單一測資
│   └── build_docs.bat / .sh   # 建置文件網站
│
├── mkdocs_plugins/            # 🔌 MkDocs 外掛
│   └── mindmaps_lastmod.py    # 最後修改日期外掛
│
├── requirements.txt           # Python 相依套件
├── pyproject.toml             # 專案配置
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

### 文件指南

文件依**目標讀者**組織：

| 位置 | 用途 | 對象 |
|:-----|:-----|:-----|
| `docs/` | 使用者文件（發布到網站） | ✅ 使用者 |
| [`tools/README.md`](docs/tools/README.md) | 開發者工具參考 | 🔧 貢獻者 |
| `tools/*/README.md` | 模組技術細節 | 🔧 貢獻者 |
| `.dev/` | 維護者文件 | 🔧 維護者 |

**主要文件：**

| 文件 | 說明 |
|:-----|:-----|
| [`docs/SOLUTION_CONTRACT.md`](docs/SOLUTION_CONTRACT.md) | 解答檔案規格 |
| [`docs/GENERATOR_CONTRACT.md`](docs/GENERATOR_CONTRACT.md) | 生成器檔案規格 |
| [`tools/README.md`](docs/tools/README.md) | 完整工具參考 |
| [`.dev/README.md`](https://github.com/lufftw/neetcode/blob/main/.dev/README.md) | 維護者指南 |
| [`docs/contributors/DOCUMENTATION_ARCHITECTURE.md`](docs/contributors/DOCUMENTATION_ARCHITECTURE.md) | 文件架構說明 |

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

**AI 驅動（推薦）：**

```bash
# 互動模式
python tools/generate_mindmaps_ai.py

# 指定目標
python tools/generate_mindmaps_ai.py --goal interview

# 生成多語言
# 編輯 tools/generate_mindmaps_ai.toml: language = ["en", "zh-TW"]
python tools/generate_mindmaps_ai.py
```

配置檔：`tools/generate_mindmaps_ai.toml`

**規則式：**

```bash
# 生成 Markdown 心智圖
python tools/generate_mindmaps.py

# 生成 HTML（互動式）心智圖
python tools/generate_mindmaps.py --html
```

配置檔：`tools/generate_mindmaps.toml`

### 本地建置文件

> ⚠️ **選擇性功能：** 本地建置文件是**完全選擇性**的。核心 LeetCode 練習功能無需任何文件建置設定即可運作。

**推薦方法（簡單）：**

最簡單的本地建置文件方式是使用手動腳本：

```bash
# Windows
scripts\build_docs.bat

# Linux/macOS
./scripts/build_docs.sh

# 建置並本地預覽
scripts\build_docs.bat --serve  # Windows
./scripts/build_docs.sh --serve  # Linux/macOS
```

📖 **詳見 [本地建置文件（手動方法）](docs/BUILD_DOCS_MANUAL.md)** 完整指南。

**進階選項（選擇性）：**

如果你想在本地測試完全相同的 GitHub Actions 工作流程，可以使用 `act`：

📖 **詳見 [使用 Act 在本地執行 GitHub Actions](docs/ACT_LOCAL_GITHUB_ACTIONS.md)** — *注意：需要 Docker 和 act 工具。只有在你想測試 CI/CD 工作流程時才需要。*

### 文件

**核心文件：**
- [`docs/contributors/README.md`](docs/contributors/README.md) — 維護者指南
- [`docs/contributors/TESTING.md`](docs/contributors/TESTING.md) — 測試文件
- [`docs/contributors/VSCODE_SETUP.md`](docs/contributors/VSCODE_SETUP.md) — VS Code Tasks、Debug 配置、工作流程範例
- [`docs/SOLUTION_CONTRACT.md`](docs/SOLUTION_CONTRACT.md) — 解答檔案規格（SOLUTIONS dict, JUDGE_FUNC）
- [`docs/GENERATOR_CONTRACT.md`](docs/GENERATOR_CONTRACT.md) — 生成器檔案規格（generate(), edge cases, complexity）
- [`docs/ARCHITECTURE_MIGRATION.md`](docs/ARCHITECTURE_MIGRATION.md) — 多型架構遷移指南

**本地文件建置（選擇性）：**
- [`docs/BUILD_DOCS_MANUAL.md`](docs/BUILD_DOCS_MANUAL.md) — ⭐ **推薦：** 簡單的手動建置方法
- [`docs/ACT_LOCAL_GITHUB_ACTIONS.md`](docs/ACT_LOCAL_GITHUB_ACTIONS.md) — 進階：使用 act 在本地測試 CI/CD 工作流程（需要 Docker）

**部署：**
- [`docs/GITHUB_PAGES_SETUP.md`](docs/GITHUB_PAGES_SETUP.md) — 部署指南

---

## 📜 授權條款

**MIT License** — 可自由用於個人學習與教育用途。

---

**為競程社群用 ❤️ 打造**

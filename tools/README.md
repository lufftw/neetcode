# 🔧 NeetCode Tools

開發者工具集，用於檢查、驗證和生成專案內容。

---

## 📋 快速導覽

| 類別 | 工具 | 用途 |
|------|------|------|
| **檢查工具** | [`check_solutions.py`](#check_solutionspy) | 驗證解答檔案架構合規性 |
| | [`run_format_tests.py`](#run_format_testspy) | 執行格式單元測試 |
| **生成工具** | [`generate_mindmaps.py`](#generate_mindmapspy) | 規則式心智圖生成 |
| | [`generate_mindmaps_ai.py`](#generate_mindmaps_aipy) | AI 驅動心智圖生成 |
| | [`generate_pattern_docs.py`](#generate_pattern_docspy) | 模式文件生成 |
| **輔助工具** | [`text_to_mindmap.py`](#text_to_mindmappy) | 文字轉心智圖格式 |
| | [`prepare_llm_input.py`](#prepare_llm_inputpy) | 準備 LLM 輸入資料 |

---

## 🚀 快速開始

```bash
# 檢查所有解答檔案
python tools/check_solutions.py

# 生成心智圖（規則式）
python tools/generate_mindmaps.py --html

# 生成心智圖（AI）
python tools/generate_mindmaps_ai.py --goal interview

# 生成模式文件
python tools/generate_pattern_docs.py
```

---

## 📁 目錄結構

```
tools/
├── README.md                      # 本文件
├── check_solutions.py             # 解答檔案檢查器
├── run_format_tests.py            # 格式測試執行器
├── run_format_tests.bat/.sh       # 格式測試腳本
│
├── generate_mindmaps.py           # 規則式心智圖生成器
├── generate_mindmaps.toml         # 規則式配置
├── generate_mindmaps_ai.py        # AI 心智圖生成器
├── mindmap_ai_config.toml         # AI 配置
│
├── generate_pattern_docs.py       # 模式文件生成器
├── generate_pattern_docs.toml     # 模式文件配置
│
├── text_to_mindmap.py             # 文字轉心智圖
├── prepare_llm_input.py           # LLM 輸入準備
│
├── mindmaps/                      # 心智圖生成模組
│   └── README.md                  # 📖 詳細技術文件
├── patterndocs/                   # 模式文件生成模組
│   └── README.md                  # 📖 詳細技術文件
├── prompts/                       # AI 提示詞管理
│   └── README.md                  # 📖 使用說明
├── shared/                        # 共用工具
└── tests/                         # 格式測試
    └── test_solution_format.py
```

---

## 🔍 檢查工具

### `check_solutions.py`

檢查所有解答檔案是否符合 Pure Polymorphic Architecture 規範。

```bash
python tools/check_solutions.py           # 標準檢查
python tools/check_solutions.py --verbose # 顯示修復建議
```

**檢查項目：**

| 類別 | 檢查內容 |
|------|----------|
| **架構合規** | `SOLUTIONS` 字典存在、包含 `class` 欄位 |
| | 無 wrapper 函式 (`solve_*`) |
| | `solve()` 使用 `get_solver()` |
| | 正確 import: `from _runner import get_solver` |
| **格式規範** | 註解使用 `Solution 1:` 格式 |
| | 註解在 class 定義**之前** |
| **複雜度註解** | 每個解法有 `# Time: O(...)` |
| | 每個解法有 `# Space: O(...)` |

**輸出範例：**

```
============================================================
📊 Solution Format Check Summary
============================================================
Total files: 34
✅ OK: 30
⚠️ Warnings: 2
❌ Errors: 2
============================================================
```

### `run_format_tests.py`

執行格式檢查的單元測試。

```bash
python tools/run_format_tests.py           # 標準執行
python tools/run_format_tests.py --verbose # 詳細輸出
python tools/run_format_tests.py --quiet   # 安靜模式
```

### `run_format_tests.bat` / `run_format_tests.sh`

執行完整格式檢查（檢查器 + 單元測試）。

```bash
tools\run_format_tests.bat     # Windows
tools/run_format_tests.sh      # Linux/Mac
```

---

## 🧠 心智圖生成

### `generate_mindmaps.py`

規則式心智圖生成器，從 ontology 資料生成 9 種心智圖。

```bash
python tools/generate_mindmaps.py          # 生成 Markdown
python tools/generate_mindmaps.py --html   # 生成 HTML（互動式）
```

**配置檔：** `tools/generate_mindmaps.toml`

**生成類型：**

| 類型 | 說明 |
|------|------|
| `pattern_hierarchy` | API Kernel → Pattern → Problem |
| `family_derivation` | 基礎模板 → 衍生變體 |
| `algorithm_usage` | 演算法 → 題目 |
| `data_structure` | 資料結構 → 題目 |
| `company_coverage` | 公司 → 題目 |
| `roadmap_paths` | 學習路線圖 |
| `problem_relations` | 相關題目網絡 |
| `solution_variants` | 多解法變體 |
| `difficulty_topics` | 難度 × 主題矩陣 |

> 📖 **詳細技術文件：** [mindmaps/README.md](mindmaps/README.md)

### `generate_mindmaps_ai.py`

AI 驅動心智圖生成器，使用 LLM 創意生成心智圖。

```bash
# 互動模式
python tools/generate_mindmaps_ai.py

# 指定目標
python tools/generate_mindmaps_ai.py --goal interview        # 面試準備
python tools/generate_mindmaps_ai.py --goal systematic       # 系統學習
python tools/generate_mindmaps_ai.py --goal pattern_mastery  # 模式掌握

# 指定主題
python tools/generate_mindmaps_ai.py --topic sliding_window
python tools/generate_mindmaps_ai.py --topic dynamic_programming
```

**配置檔：** `tools/mindmap_ai_config.toml`

| 區段 | 可配置內容 |
|------|------------|
| `[model]` | LLM 模型、temperature、max tokens |
| `[output]` | 輸出目錄、檔名、HTML 生成 |
| `[ontology]` | 包含哪些知識圖譜資料 |
| `[problems]` | 題目篩選（難度、主題、路線圖） |
| `[links]` | GitHub repo URL、分支 |
| `[advanced]` | 輸出語言（支援多語言） |

**無 API Key？** 執行後複製 `tools/prompts/generated/mindmap_prompt.md` 到 ChatGPT/Claude。

> 📖 **詳細使用說明：** [prompts/README.md](prompts/README.md)

---

## 📐 模式文件生成

### `generate_pattern_docs.py`

從 `meta/patterns/` 來源檔案組合生成模式文件。

```bash
# 生成所有模式文件
python tools/generate_pattern_docs.py

# 生成特定模式
python tools/generate_pattern_docs.py --pattern sliding_window
```

**配置檔：** `tools/generate_pattern_docs.toml`

**來源結構：**

```
meta/patterns/sliding_window/
├── _config.toml        # 檔案順序配置（可選）
├── _header.md          # 介紹和核心概念
├── 0003_base.md        # 基礎模板題目
├── 0076_variant.md     # 變體題目
├── _comparison.md      # 模式比較表
├── _decision.md        # 決策指南
└── _templates.md       # 模板程式碼
```

> 📖 **詳細技術文件：** [patterndocs/README.md](patterndocs/README.md)

---

## 🛠️ 輔助工具

### `text_to_mindmap.py`

將純文字轉換為 Markmap 心智圖格式。

```bash
python tools/text_to_mindmap.py input.txt -o output.md
```

### `prepare_llm_input.py`

準備 LLM 輸入資料，整合 ontology 和題目資訊。

```bash
python tools/prepare_llm_input.py --output llm_input.json
```

**用途：**
- 準備 AI 分析的輸入資料
- 導出題目和模式資訊
- 生成 prompt 所需的上下文

---

## 🧪 測試

### 格式測試

```bash
# 執行格式測試
pytest tools/tests/test_solution_format.py -v

# 或使用 standalone script
python tools/run_format_tests.py
```

### 生成器測試

```bash
# 心智圖生成測試
pytest .dev/tests/test_generate_mindmaps.py -v

# 模式文件生成測試
pytest .dev/tests/test_generate_pattern_docs.py -v
```

---

## 📊 測試架構總覽

```
neetcode/
├── tools/tests/                  # 格式合規測試
│   └── test_solution_format.py
│
├── .dev/tests/                   # 元件測試（runner 模組）
│   ├── test_generate_mindmaps.py
│   ├── test_generate_pattern_docs.py
│   └── ...
│
└── .dev/tests_solutions/         # 解答正確性測試
    └── test_all_solutions.py
```

**執行所有測試：**

```bash
.dev\run_all_tests.bat    # Windows
.dev/run_all_tests.sh     # Linux/Mac
```

---

## 🔗 相關文件

| 文件 | 說明 |
|------|------|
| [SOLUTION_CONTRACT.md](../docs/SOLUTION_CONTRACT.md) | 解答檔案規格 |
| [GENERATOR_CONTRACT.md](../docs/GENERATOR_CONTRACT.md) | 生成器檔案規格 |
| [ARCHITECTURE_MIGRATION.md](../docs/ARCHITECTURE_MIGRATION.md) | 架構遷移指南 |
| [mindmaps/README.md](mindmaps/README.md) | 心智圖模組技術文件 |
| [patterndocs/README.md](patterndocs/README.md) | 模式文件模組技術文件 |
| [prompts/README.md](prompts/README.md) | AI 提示詞使用說明 |

---

## ❓ 常見問題

<details>
<summary><strong>check_solutions.py 報錯怎麼辦？</strong></summary>

**Missing Solution Comment:**
```python
# 在 class 定義之前加上：
# ============================================
# Solution 1: Hash Map
# Time: O(n), Space: O(n)
# ============================================
class Solution:
    ...
```

**Wrong Comment Format:**
```python
# 改 "Solution:" 為 "Solution 1:"
# Solution 1: Two Pointers  ✅
# Solution: Two Pointers    ❌
```

</details>

<details>
<summary><strong>如何新增心智圖類型？</strong></summary>

1. 在 `tools/mindmaps/generators/` 新增檔案
2. 實作 generator 函式
3. 註冊到 `generators/__init__.py`
4. 新增測試到 `.dev/tests/test_generate_mindmaps.py`

詳見 [mindmaps/README.md](mindmaps/README.md#adding-a-new-generator)

</details>

<details>
<summary><strong>如何新增模式文件？</strong></summary>

1. 建立目錄 `meta/patterns/<pattern_name>/`
2. 新增 `_header.md`（必要）
3. 新增題目檔案（如 `0003_base.md`）
4. 可選新增 `_config.toml` 控制順序
5. 執行 `python tools/generate_pattern_docs.py --pattern <name>`

詳見 [patterndocs/README.md](patterndocs/README.md#adding-a-new-pattern)

</details>

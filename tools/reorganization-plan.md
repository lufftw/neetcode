# Tools 目錄整理規劃文件

## 📋 目錄

1. [現狀分析](#現狀分析)
2. [整理目標](#整理目標)
3. [確定的新結構](#確定的新結構)
4. [文件分類詳情](#文件分類詳情)
5. [遷移計劃](#遷移計劃)
6. [待討論事項](#待討論事項)

---

## 現狀分析

### 當前目錄結構

```
tools/
├── 核心工具腳本（根目錄）
│   ├── check_*.py (檢查工具)
│   ├── generate_*.py (生成工具)
│   ├── sync_*.py (同步工具)
│   ├── convert_*.py (轉換工具)
│   └── 其他單一功能腳本
│
├── 模組目錄
│   ├── mindmaps/ (思維導圖生成模組)
│   ├── ai-markmap-agent/ (AI 思維導圖代理)
│   ├── ai_mindmap/ (AI 思維導圖模組)
│   ├── patterndocs/ (模式文檔生成模組)
│   ├── leetcode-api/ (LeetCode API 模組)
│   ├── docstring/ (文檔字符串模組)
│   ├── review-code/ (代碼審查模組)
│   └── doc-naming/ (文檔命名工具)
│
├── 支援目錄
│   ├── hooks/ (Git hooks)
│   ├── prompts/ (AI 提示詞管理)
│   ├── shared/ (共享工具)
│   ├── tests/ (測試文件)
│   └── outputs/ (輸出目錄)
```

### 主要問題

1. **根目錄文件過多**：大量腳本文件散落在根目錄，缺乏組織
2. **功能重疊**：多個思維導圖相關工具散落各處
3. **分類不清**：檢查、生成、同步工具混在一起
4. **支援目錄分離**：hooks/prompts/shared 與相關模組分離，容易導致路徑錯誤

---

## 整理目標

1. **按功能分類**：將相關工具組織到對應目錄
2. **模組自包含**：支援文件(hooks/prompts/shared)跟隨相關模組
3. **減少根目錄文件**：只保留 README 和暫存區
4. **暫存未歸類文件**：使用 `_staging/` 存放待整理的文件

---

## 確定的新結構

```
tools/
├── README.md
│
├── mindmaps/                      # 🗺️ 思維導圖功能（全部整合）
│   ├── core/                      # 核心模組（原 mindmaps/）
│   │   ├── __init__.py
│   │   ├── generators/
│   │   ├── config.py
│   │   ├── data.py
│   │   ├── helpers.py
│   │   ├── html.py
│   │   ├── loader.py
│   │   ├── post_processing.py
│   │   ├── templates.py
│   │   ├── toml_parser.py
│   │   └── meta/
│   │
│   ├── ai-markmap-agent/          # AI 思維導圖代理（保持原結構）
│   │   ├── main.py
│   │   ├── src/
│   │   ├── prompts/               # AI agent 專用提示詞
│   │   └── ...
│   │
│   ├── ai_mindmap/                # AI 思維導圖模組
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── data_loader.py
│   │   ├── html_generator.py
│   │   ├── openai_client.py
│   │   ├── prompt_manager.py
│   │   └── prompts.py
│   │
│   ├── hooks/                     # 思維導圖相關 hooks
│   │   └── generate_ai_mindmaps_hook.py
│   │
│   ├── prompts/                   # 思維導圖 AI 提示詞
│   │   ├── generated/
│   │   ├── prompts_config.yaml
│   │   ├── README.md
│   │   └── system-prompt.md
│   │
│   ├── shared/                    # 思維導圖共享工具
│   │   └── toml_parser.py
│   │
│   ├── tests/                     # 思維導圖測試
│   │   ├── test_post_processing.py
│   │   └── ...
│   │
│   ├── outputs/                   # 輸出目錄
│   │
│   ├── generate_mindmaps.py       # 規則式生成器（入口）
│   ├── generate_mindmaps_ai.py    # AI 生成器（入口）
│   ├── generate_mindmaps.toml     # 配置
│   ├── generate_mindmaps_ai.toml  # AI 配置
│   ├── sync_mindmap_html.py       # 同步 HTML
│   ├── convert_existing_mindmaps.py # 轉換工具
│   ├── text_to_mindmap.py         # 文本轉換
│   └── html_meta_description_generator.py  # SEO 元描述生成
│
├── pattern-docs/                  # 📚 模式文檔功能（原 patterndocs）
│   ├── __init__.py
│   ├── composer.py
│   ├── config.py
│   ├── data.py
│   ├── files.py
│   ├── kernel_extractor.py
│   ├── loader.py
│   ├── mapping.py
│   ├── problem_mapper.py
│   ├── sections.py
│   ├── toml_parser.py
│   ├── generate_pattern_docs.py   # 入口腳本（從根目錄移入）
│   └── generate_pattern_docs.toml # 配置（從根目錄移入）
│
├── review-code/                   # 🔍 代碼審查與驗證
│   ├── __init__.py
│   ├── fix_docstring.py
│   ├── test_fetcher.py
│   ├── test_leetscrape.py
│   ├── NAMING_ANALYSIS.md
│   ├── README.md
│   │
│   └── validation/                # 驗證工具（新建子目錄）
│       ├── check_solutions.py
│       ├── check_test_files.py
│       ├── check_solution_contract.py
│       ├── run_format_tests.py
│       ├── run_format_tests.bat
│       ├── run_format_tests.sh
│       └── tests/                 # 驗證相關測試
│           └── test_solution_format.py
│
├── docstring/                     # 📝 文檔字符串工具（保持現有）
│   ├── __init__.py
│   ├── formatter.py
│   └── README.md
│
├── leetcode-api/                  # 🔗 LeetCode API（保持現有）
│   ├── __init__.py
│   ├── question_api.py
│   ├── question_store.py
│   ├── question_serializer.py
│   ├── import_all_question.py
│   ├── data/
│   └── db/
│
├── maintenance/                   # 🔧 維護工具
│   └── doc-naming/                # 文檔命名工具
│
└── _staging/                      # 📦 暫存區（待整理）
    ├── sync_leetcode_data.py      # LeetCode 數據同步
    ├── fetch_leetcode_api.py      # LeetCode API 獲取
    ├── test_leetcode_api_integration.py
    ├── leetcode_api_usage_example.py
    ├── prepare_llm_input.py       # LLM 輸入準備
    └── .cache/                    # 快取目錄
```

---

## 文件分類詳情

### 1. 思維導圖功能 (mindmaps/)

將所有思維導圖相關文件整合到一個目錄：

| 原位置 | 新位置 | 說明 |
|--------|--------|------|
| `tools/mindmaps/` | `mindmaps/core/` | 核心模組重命名 |
| `tools/ai-markmap-agent/` | `mindmaps/ai-markmap-agent/` | 保持原結構 |
| `tools/ai_mindmap/` | `mindmaps/ai_mindmap/` | 保持原結構 |
| `tools/hooks/` | `mindmaps/hooks/` | Git hooks |
| `tools/prompts/` | `mindmaps/prompts/` | AI 提示詞 |
| `tools/shared/` | `mindmaps/shared/` | 共享工具 |
| `tools/outputs/` | `mindmaps/outputs/` | 輸出目錄 |
| `generate_mindmaps.py` | `mindmaps/generate_mindmaps.py` | 入口腳本 |
| `generate_mindmaps_ai.py` | `mindmaps/generate_mindmaps_ai.py` | AI 入口 |
| `sync_mindmap_html.py` | `mindmaps/sync_mindmap_html.py` | 同步工具 |
| `convert_existing_mindmaps.py` | `mindmaps/convert_existing_mindmaps.py` | 轉換工具 |
| `text_to_mindmap.py` | `mindmaps/text_to_mindmap.py` | 文本轉換 |
| `html_meta_description_generator.py` | `mindmaps/html_meta_description_generator.py` | SEO 工具 |

### 2. 模式文檔功能 (pattern-docs/)

| 原位置 | 新位置 | 說明 |
|--------|--------|------|
| `tools/patterndocs/` | `pattern-docs/` | 重命名為 kebab-case |
| `generate_pattern_docs.py` | `pattern-docs/generate_pattern_docs.py` | 入口腳本移入 |
| `generate_pattern_docs.toml` | `pattern-docs/generate_pattern_docs.toml` | 配置移入 |

### 3. 代碼審查與驗證 (review-code/)

| 原位置 | 新位置 | 說明 |
|--------|--------|------|
| `tools/review-code/*` | `review-code/` | 保持現有 |
| `check_solutions.py` | `review-code/validation/` | 移入驗證子目錄 |
| `check_test_files.py` | `review-code/validation/` | 移入驗證子目錄 |
| `check_solution_contract.py` | `review-code/validation/` | 移入驗證子目錄 |
| `run_format_tests.*` | `review-code/validation/` | 移入驗證子目錄 |
| `tests/test_solution_format.py` | `review-code/validation/tests/` | 移入驗證測試 |

### 4. 維護工具 (maintenance/)

| 原位置 | 新位置 | 說明 |
|--------|--------|------|
| `tools/doc-naming/` | `maintenance/doc-naming/` | 文檔命名工具 |

### 5. 暫存區 (_staging/)

暫時無法明確歸類的文件：

| 文件 | 可能歸屬 | 說明 |
|------|----------|------|
| `sync_leetcode_data.py` | `leetcode-api/` ? | LeetCode 數據同步 |
| `fetch_leetcode_api.py` | `leetcode-api/` ? | API 獲取 |
| `prepare_llm_input.py` | 待決定 | LLM 輸入準備 |
| `.cache/` | `_staging/` | 快取目錄 |

---

## 遷移計劃

### 階段 1：準備工作
- [x] 創建規劃文檔（本文件）
- [ ] 確認 `ai_mindmap/` 與 `ai-markmap-agent/` 的關係
- [ ] 檢查所有腳本的導入路徑依賴
- [ ] 備份當前結構

### 階段 2：創建新目錄結構
- [ ] 在 `mindmaps/` 下創建 `core/` 目錄
- [ ] 在 `review-code/` 下創建 `validation/` 目錄
- [ ] 創建 `maintenance/` 目錄
- [ ] 創建 `_staging/` 目錄

### 階段 3：移動文件（按順序）
1. [ ] 移動 `mindmaps/` 內容到 `mindmaps/core/`
2. [ ] 移動 `ai-markmap-agent/` 到 `mindmaps/`
3. [ ] 移動 `ai_mindmap/` 到 `mindmaps/`
4. [ ] 移動 `hooks/`, `prompts/`, `shared/` 到 `mindmaps/`
5. [ ] 移動生成腳本到 `mindmaps/`
6. [ ] 移動驗證工具到 `review-code/validation/`
7. [ ] 重命名 `patterndocs/` 為 `pattern-docs/` 並移入入口腳本
8. [ ] 移動 `doc-naming/` 到 `maintenance/`
9. [ ] 移動其他到 `_staging/`

### 階段 4：更新引用
- [ ] 更新所有 Python 導入路徑
- [ ] 更新 README.md 中的路徑
- [ ] 更新配置文件中的路徑
- [ ] 更新文檔引用

### 階段 5：測試和驗證
- [ ] 運行所有測試
- [ ] 驗證所有工具仍可正常運行
- [ ] 清理空目錄

---

## 待討論事項

### 1. ✅ 已決定

| 項目 | 決定 |
|------|------|
| mindmaps 結構 | 作為功能目錄整合所有相關工具 |
| validation 位置 | 放到 `review-code/` 底下 |
| html_meta_description_generator.py | 放到 `mindmaps/` |
| hooks/prompts/shared | 跟隨相關模組 |
| 暫存目錄名稱 | `_staging/`（下劃線開頭，排序時在最前） |
| doc-naming 位置 | 放到 `maintenance/` 底下 |
| patterndocs 命名 | 改為 `pattern-docs/`（統一 kebab-case） |

### 2. 🔄 待確認

| 項目 | 問題 | 建議 |
|------|------|------|
| `_staging/` 文件處理 | 後續如何處理？ | 逐步整理到適當位置或刪除 |
| `ai_mindmap/` vs `ai-markmap-agent/` | 是否有重疊？ | 需要檢查代碼確認 |
| `sync_leetcode_data.py` | 放 `leetcode-api/` 還是 `_staging/`？ | 建議放 `leetcode-api/` |

---

## 下一步行動

### ✅ 已確認的決定

| 項目 | 決定 |
|------|------|
| `mindmaps/` | 整合所有思維導圖相關工具 |
| `pattern-docs/` | 從 `patterndocs` 重命名 |
| `validation/` | 放到 `review-code/` 底下 |
| `doc-naming/` | 放到 `maintenance/` 底下 |
| `_staging/` | 暫存未歸類文件 |

### 📋 最終結構預覽

```
tools/
├── README.md
├── mindmaps/              # 思維導圖（整合）
├── pattern-docs/          # 模式文檔（重命名）
├── review-code/           # 代碼審查
│   └── validation/        # 驗證工具
├── docstring/             # 文檔字符串
├── leetcode-api/          # LeetCode API
├── maintenance/           # 維護工具
│   └── doc-naming/
└── _staging/              # 暫存區
```

### 準備開始遷移？

確認後，我將按照遷移計劃執行文件移動和路徑更新。

---

## 附錄：變更前目錄架構

> 此章節記錄整理前的完整目錄結構，供後續程式修改和路徑追蹤參考。

### 原始目錄結構

```
tools/                                    # 變更前根目錄
│
├── README.md                             # 工具說明文件
├── reorganization-plan.md                # 本規劃文件
│
├── ─────────────────────────────────     # ═══ 根目錄腳本 ═══
├── check_solutions.py                    # → review-code/validation/
├── check_test_files.py                   # → review-code/validation/
├── check_solution_contract.py            # → review-code/validation/
├── run_format_tests.py                   # → review-code/validation/
├── run_format_tests.bat                  # → review-code/validation/
├── run_format_tests.sh                   # → review-code/validation/
│
├── generate_mindmaps.py                  # → mindmaps/
├── generate_mindmaps.toml                # → mindmaps/
├── generate_mindmaps_ai.py               # → mindmaps/
├── generate_mindmaps_ai.toml             # → mindmaps/
├── sync_mindmap_html.py                  # → mindmaps/
├── convert_existing_mindmaps.py          # → mindmaps/
├── text_to_mindmap.py                    # → mindmaps/
├── html_meta_description_generator.py    # → mindmaps/
├── html_meta_description_generator.toml  # → mindmaps/
├── html-meta-description-generator.md    # → mindmaps/
├── html-meta-description-generator-zh-tw.md  # → mindmaps/
│
├── generate_pattern_docs.py              # → pattern-docs/
├── generate_pattern_docs.toml            # → pattern-docs/
│
├── sync_leetcode_data.py                 # → _staging/
├── fetch_leetcode_api.py                 # → _staging/
├── test_leetcode_api_integration.py      # → _staging/
├── leetcode_api_usage_example.py         # → _staging/
├── prepare_llm_input.py                  # → _staging/
├── leetcode-api-discussion.md            # → _staging/
├── verify-integration.md                 # → _staging/
│
├── ─────────────────────────────────     # ═══ 模組目錄 ═══
├── mindmaps/                             # → mindmaps/core/
│   ├── __init__.py
│   ├── config.py
│   ├── data.py
│   ├── helpers.py
│   ├── html.py
│   ├── loader.py
│   ├── post_processing.py
│   ├── templates.py
│   ├── toml_parser.py
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── algorithm.py
│   │   ├── company.py
│   │   ├── difficulty.py
│   │   ├── family.py
│   │   ├── pattern.py
│   │   ├── relations.py
│   │   ├── roadmap.py
│   │   └── variants.py
│   └── meta/
│       └── *.txt (13 files)
│
├── ai-markmap-agent/                     # → mindmaps/ai-markmap-agent/
│   ├── main.py
│   ├── translate_only.py
│   ├── convert_to_html.py
│   ├── convert_to_html.toml
│   ├── requirements.txt
│   ├── env.example
│   ├── config/
│   │   └── config.yaml
│   ├── src/
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   ├── consensus.py
│   │   ├── data_compressor.py
│   │   ├── data_sources.py
│   │   ├── debug_output.py
│   │   ├── graph.py
│   │   ├── leetcode_api.py
│   │   ├── post_processing.py
│   │   ├── resume.py
│   │   ├── agents/
│   │   │   ├── base_agent.py
│   │   │   ├── evaluator.py
│   │   │   ├── expert.py
│   │   │   ├── integrator.py
│   │   │   ├── planner.py
│   │   │   ├── strategist.py
│   │   │   ├── translator.py
│   │   │   └── writer.py
│   │   ├── compression/
│   │   ├── memory/
│   │   ├── output/
│   │   └── schema/
│   ├── prompts/                          # AI agent 專用提示詞
│   │   ├── compressor/
│   │   ├── evaluators/
│   │   ├── experts/
│   │   ├── generators/
│   │   ├── integrator/
│   │   ├── judges/
│   │   ├── meta/
│   │   ├── optimizers/
│   │   ├── planners/
│   │   ├── strategists/
│   │   ├── summarizer/
│   │   ├── translator/
│   │   └── writer/
│   ├── templates/
│   ├── docs/
│   ├── examples/
│   ├── outputs/
│   └── tests/
│
├── ai_mindmap/                           # → mindmaps/ai_mindmap/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── html_generator.py
│   ├── openai_client.py
│   ├── prompt_manager.py
│   └── prompts.py
│
├── patterndocs/                          # → pattern-docs/ (重命名)
│   ├── __init__.py
│   ├── composer.py
│   ├── config.py
│   ├── data.py
│   ├── files.py
│   ├── kernel_extractor.py
│   ├── loader.py
│   ├── mapping.py
│   ├── problem_mapper.py
│   ├── sections.py
│   └── toml_parser.py
│
├── review-code/                          # → review-code/ (保持)
│   ├── __init__.py
│   ├── fix_docstring.py
│   ├── test_fetcher.py
│   ├── test_leetscrape.py
│   ├── NAMING_ANALYSIS.md
│   └── README.md
│
├── docstring/                            # → docstring/ (保持)
│   ├── __init__.py
│   ├── formatter.py
│   └── README.md
│
├── leetcode-api/                         # → leetcode-api/ (保持)
│   ├── __init__.py
│   ├── question_api.py
│   ├── question_store.py
│   ├── question_serializer.py
│   ├── import_all_question.py
│   ├── data/
│   └── db/
│
├── doc-naming/                           # → maintenance/doc-naming/
│   ├── fix_html_references.py
│   ├── fix_patterndocs_readme.py
│   ├── fix_readme_filenames.py
│   ├── fix_remaining_references.py
│   ├── rename_docs_to_kebab_case.py
│   ├── rename_mapping.json
│   ├── rename_mapping.txt
│   ├── rename_md_files.py
│   ├── rename_mindmap_html_files.py
│   ├── rename_mindmap_html.py
│   ├── update_html_references.py
│   └── verify_all_renames.py
│
├── ─────────────────────────────────     # ═══ 支援目錄 ═══
├── hooks/                                # → mindmaps/hooks/
│   └── generate_ai_mindmaps_hook.py
│
├── prompts/                              # → mindmaps/prompts/
│   ├── README.md
│   ├── prompts_config.yaml
│   ├── system-prompt.md
│   └── generated/
│
├── shared/                               # → mindmaps/shared/
│   └── toml_parser.py
│
├── tests/                                # → mindmaps/tests/ + review-code/validation/tests/
│   ├── __init__.py
│   ├── test_post_processing.py           # → mindmaps/tests/
│   └── test_solution_format.py           # → review-code/validation/tests/
│
├── outputs/                              # → mindmaps/outputs/
│   └── debug/
│
└── .cache/                               # → _staging/.cache/
    ├── leetcode_problems.json
    └── leetcode_cache_meta.json
```

### 路徑變更對照表

| 原路徑 | 新路徑 | 變更類型 |
|--------|--------|----------|
| `tools/mindmaps/` | `tools/mindmaps/core/` | 移動+重命名 |
| `tools/ai-markmap-agent/` | `tools/mindmaps/ai-markmap-agent/` | 移動 |
| `tools/ai_mindmap/` | `tools/mindmaps/ai_mindmap/` | 移動 |
| `tools/patterndocs/` | `tools/pattern-docs/` | 重命名 |
| `tools/doc-naming/` | `tools/maintenance/doc-naming/` | 移動 |
| `tools/hooks/` | `tools/mindmaps/hooks/` | 移動 |
| `tools/prompts/` | `tools/mindmaps/prompts/` | 移動 |
| `tools/shared/` | `tools/mindmaps/shared/` | 移動 |
| `tools/tests/` | 分散到各模組 | 拆分 |
| `tools/outputs/` | `tools/mindmaps/outputs/` | 移動 |
| `tools/.cache/` | `tools/_staging/.cache/` | 移動 |
| `tools/check_*.py` | `tools/review-code/validation/` | 移動 |
| `tools/run_format_tests.*` | `tools/review-code/validation/` | 移動 |
| `tools/generate_mindmaps*.py` | `tools/mindmaps/` | 移動 |
| `tools/generate_pattern_docs.*` | `tools/pattern-docs/` | 移動 |
| `tools/sync_mindmap_html.py` | `tools/mindmaps/` | 移動 |
| `tools/html_meta_description_generator.*` | `tools/mindmaps/` | 移動 |

### Python 導入路徑變更

```python
# ═══ mindmaps 相關 ═══
# 變更前
from mindmaps import load_ontology
from mindmaps.generators import pattern
from ai_mindmap import openai_client

# 變更後
from mindmaps.core import load_ontology
from mindmaps.core.generators import pattern
from mindmaps.ai_mindmap import openai_client

# ═══ patterndocs 相關 ═══
# 變更前
from patterndocs import composer

# 變更後（需處理 kebab-case 問題）
# 方案 A：使用 importlib
import importlib
pattern_docs = importlib.import_module('pattern-docs')

# 方案 B：在 pattern-docs 內保持 patterndocs 作為模組名
from pattern_docs import composer  # 如果內部用 pattern_docs
```

### 需要更新的配置文件

| 文件 | 需要更新的內容 |
|------|----------------|
| `tools/README.md` | 目錄結構說明 |
| `tools/mindmaps/generate_mindmaps.toml` | 相對路徑 |
| `tools/mindmaps/generate_mindmaps_ai.toml` | 相對路徑 |
| `tools/pattern-docs/generate_pattern_docs.toml` | 相對路徑 |
| `tools/mindmaps/hooks/generate_ai_mindmaps_hook.py` | 導入路徑 |
| `docs/tools/README.md` | 工具文檔路徑引用 |
| `.github/workflows/*.yml` | CI/CD 腳本路徑（如有）|

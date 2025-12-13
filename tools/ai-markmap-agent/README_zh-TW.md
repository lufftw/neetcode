# AI Markmap Agent

> 使用 LangGraph 進行 Markmap 改進的多專家精進系統。

[![LangGraph](https://img.shields.io/badge/LangGraph-v1.0.4-blue)](https://github.com/langchain-ai/langgraph)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 目錄

- [概述](#概述)
- [核心理念](#核心理念)
- [系統架構](#系統架構)
- [工作流程](#工作流程)
- [安裝](#安裝)
- [使用方式](#使用方式)
- [配置](#配置)
- [專家角色](#專家角色)
- [專案結構](#專案結構)

---

## 概述

本系統透過多專家審查與共識討論來精進現有的高品質 Markmap。不從零開始生成，而是從基準 Markmap 出發，透過領域專家分析進行改進。

### 核心特點

| 特點 | 說明 |
|------|------|
| **精進模式** | 從高品質基準出發，而非從零創建 |
| **領域專家** | 架構師、教授、工程師的專業視角 |
| **共識投票** | 程式化多數決（需 2/3 同意） |
| **自然語言** | 建議以自然語言表達，非固定格式 |
| **高效 API** | 僅需 2N + 1 次呼叫（N = 專家數量） |

---

## 核心理念

### 「精進，而非創造」

| 舊做法 | 新做法 |
|--------|--------|
| 從資料創建結構 | 從高品質基準出發 |
| YAML 中間格式 | 直接操作 Markmap |
| 通用策略師角色 | 領域專精專家 |
| AI 整合建議 | 程式化共識計算 |

### 為什麼精進更好

1. **品質保留** - 不重新發明已經很好的部分
2. **聚焦討論** - 專家討論「如何改進」，而非「如何創建」
3. **自然語言** - AI 最擅長理解和生成自然文字
4. **高效** - 更少 API 呼叫，更快迭代

---

## 系統架構

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI Markmap Agent                                      │
│                   精進模式 — 2 輪全面討論                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 0: 載入基準                                                          │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                             │
│  ┌─────────────────────────────────┐                                        │
│  │ 基準 Markmap                    │                                        │
│  │ (如：neetcode_ontology_ai.md)   │                                        │
│  └───────────┬─────────────────────┘                                        │
│              │                                                              │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 1: 獨立審查（N 個並行 API 呼叫）                                     │
│  ════════════════════════════════════════════════════════════════════════  │
│              │                                                              │
│   ┌──────────┴──────────┬──────────────────┐                               │
│   ▼                     ▼                  ▼                               │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│   │ 🏗️ 架構師   │    │ 📚 教授     │    │ ⚙️ 工程師   │                 │
│   │ 5-10 建議   │    │ 5-10 建議   │    │ 5-10 建議   │                 │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                 │
│          │                   │                   │                         │
│          └───────────────────┼───────────────────┘                         │
│                              │                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 2: 全面討論（N 個並行 API 呼叫）                                     │
│  ════════════════════════════════════════════════════════════════════════  │
│                              │                                             │
│   每位專家看到所有建議，投票：✅ / ⚠️ / ❌                                 │
│   每位專家輸出最終採納清單                                                  │
│                              │                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 3: 共識計算（程式，非 AI）                                           │
│  ════════════════════════════════════════════════════════════════════════  │
│                              │                                             │
│   多數決：需 2/3（≥67%）同意                                               │
│   ✅ 採納：A1, A3, P1, E1, E4                                              │
│   ❌ 否決：A2, P2, P3, E2, E3                                              │
│                              │                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 4: 寫作（1 次 API 呼叫）                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│                              │                                             │
│   將採納的改進應用到基準 → 精進後的 Markmap                                 │
│                              │                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 5-6: 翻譯與後處理                                                    │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### API 呼叫效率

| 專家數 (N) | API 呼叫 | 等待批次 |
|------------|----------|----------|
| 3（預設）  | 7        | 3（固定）|
| 5          | 11       | 3（固定）|
| 7          | 15       | 3（固定）|

---

## 工作流程

### Phase 0: 載入基準

載入現有的高品質 Markmap 作為起點。

### Phase 1: 獨立審查

每位專家獨立審查基準並提出 5-10 條改進建議：
- 無群體影響
- 自然語言建議
- 聚焦其領域專長

### Phase 2: 全面討論

每位專家：
1. 看到所有專家的所有建議
2. 對每條建議投票（✅ 同意 / ⚠️ 修改 / ❌ 反對）
3. 輸出最終採納清單

### Phase 3: 共識計算

**程式化，非 AI：**
- 計算每條建議的票數
- ≥67%（2/3）同意則採納
- 否則拒絕

### Phase 4: 寫作

將採納的改進精準應用到基準：
- 最小化改動
- 保留現有品質
- 驗證連結和格式

### Phase 5-6: 後處理

- 翻譯（en → zh-TW）
- 連結驗證
- HTML 生成

---

## 安裝

```bash
# 建立虛擬環境
python -m venv venv

# 啟動 (Windows)
.\venv\Scripts\activate

# 啟動 (Unix/macOS)
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

---

## 使用方式

### 基本用法

```bash
# 使用預設基準執行
python main.py

# 指定基準檔案
python main.py --baseline path/to/markmap.md

# 試執行（僅載入資料）
python main.py --dry-run
```

### API 金鑰

API 金鑰在執行時輸入，**永不儲存**：

```bash
python main.py

# 會提示輸入：
# Enter OPENAI API Key: ********
#   ✓ OPENAI API key accepted
```

跳過 API 金鑰提示：

```bash
python main.py --no-openai
python main.py --no-anthropic
```

---

## 配置

所有設定在 `config/config.yaml`。

### 專家配置

```yaml
experts:
  enabled:
    - "architect"
    - "professor"
    - "engineer"
  
  suggestions:
    min_per_expert: 5
    max_per_expert: 10
  
  definitions:
    architect:
      name: "Top Software Architect"
      emoji: "🏗️"
      model: "gpt-4o"
      focus_areas:
        - "API Kernel 抽象"
        - "Pattern 關係"
        - "程式碼模板複用性"
```

### 精進範圍

控制可以修改的內容：

```yaml
refinement_scope:
  allowed_changes:
    structure:
      enabled: true
      max_depth_change: 1
    content:
      add_content: true
      remove_content: true
      modify_content: true
    problems:
      add_problems: true
      remove_problems: false  # 保守設定
      reorder_problems: true
```

### 工作流程設定

```yaml
workflow:
  discussion_rounds: 2
  parallel_execution: true
  consensus_threshold: 0.67  # 需 2/3 同意
```

---

## 專家角色

### 🏗️ 頂級軟體架構師

**專注**：API 設計、模組化、系統映射

**審查重點**：
- 乾淨的 API Kernel 抽象
- Pattern 可組合性
- 程式碼模板複用性
- 系統設計關聯

### 📚 傑出演算法教授

**專注**：正確性、教學法、理論

**審查重點**：
- 概念準確性
- 學習順序
- 複雜度分析
- 不變量描述

### ⚙️ 資深首席工程師

**專注**：實用價值、面試、權衡

**審查重點**：
- 面試頻率
- 實際應用
- 權衡說明
- 知識可發現性

---

## 專案結構

```
ai-markmap-agent/
├── config/
│   └── config.yaml              # 主配置
├── prompts/
│   ├── experts/                 # 專家提示
│   │   ├── architect_persona.md
│   │   ├── architect_behavior.md
│   │   ├── professor_persona.md
│   │   ├── professor_behavior.md
│   │   ├── engineer_persona.md
│   │   ├── engineer_behavior.md
│   │   └── discussion_behavior.md
│   └── writer/
│       ├── writer_persona.md
│       ├── writer_behavior.md
│       └── markmap_format_guide.md
├── src/
│   ├── agents/
│   │   ├── base_agent.py        # 基礎 Agent 類
│   │   ├── expert.py            # 專家 Agents
│   │   ├── writer.py            # 寫作 Agent
│   │   └── translator.py        # 翻譯 Agent
│   ├── consensus.py             # 共識計算（程式）
│   ├── graph.py                 # LangGraph 工作流程
│   ├── config_loader.py         # 配置載入
│   └── ...
├── main.py                      # 程式入口
└── README.md
```

---

## 模組職責

| 模組 | 職責 |
|------|------|
| `expert.py` | 領域專精專家 Agents |
| `consensus.py` | 程式化多數決投票 |
| `writer.py` | 精進模式寫作器 |
| `graph.py` | LangGraph 工作流程編排 |
| `config_loader.py` | 配置管理 |

---

## 授權

MIT License - 詳見 [LICENSE](LICENSE)。

---

## 相關資源

- [LangGraph 文件](https://langchain-ai.github.io/langgraph/)
- [LangChain 文件](https://python.langchain.com/)
- [Markmap](https://markmap.js.org/)

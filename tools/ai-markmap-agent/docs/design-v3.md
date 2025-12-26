# AI Markmap Agent - Design V3

## Overview

本文件描述 AI Markmap Agent 的第三版設計，核心改進是：

**「討論概念，不討論格式」**

| V2 做法 | V3 做法 |
|---------|---------|
| Agents 討論完整的 Markdown | Agents 討論 **Structure Specification** |
| 每輪傳遞完整 Markmap (含 URL) | 只傳遞結構規格 (問題 ID 引用) |
| 討論陷入格式細節 | 聚焦內容策略和組織方式 |
| 過程與產品混在一起 | 嚴格分離：Structure Spec ≠ 最終 Markmap |

---

## Architecture V3

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI Markmap Agent V3                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│  概念層 (Concept Layer) - 討論「要什麼」，不討論「怎麼呈現」                │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                             │
│  Phase 1: Structure Generation                                              │
│  ┌──────────────┐  ┌──────────────┐                                        │
│  │  Generalist  │  │  Specialist  │                                        │
│  │   Planner    │  │   Planner    │                                        │
│  └──────┬───────┘  └──────┬───────┘                                        │
│         │                 │                                                 │
│         ▼                 ▼                                                 │
│  ┌─────────────────────────────────┐                                       │
│  │     Structure Specifications    │  ← YAML 格式，只有概念/引用           │
│  └─────────────┬───────────────────┘                                       │
│                │                                                            │
│  Phase 2: Content Strategy Optimization (×N rounds)                        │
│  ┌─────────────▼───────────────────┐                                       │
│  │      Content Strategists        │  討論內容策略，不討論格式             │
│  │  ┌─────────┐ ┌─────────┐ ┌────┐ │                                       │
│  │  │Architect│ │Professor│ │ UX │ │                                       │
│  │  │Strategist│ │Strategist│ │Strategist│ │                               │
│  │  └────┬────┘ └────┬────┘ └─┬──┘ │                                       │
│  │       └───────────┼────────┘    │                                       │
│  │                   ▼             │                                       │
│  │           ┌────────────┐        │                                       │
│  │           │ Integrator │        │  整合建議，更新 Structure Spec        │
│  │           └─────┬──────┘        │                                       │
│  └─────────────────┼───────────────┘                                       │
│                    │                                                        │
│  Phase 3: Evaluation                                                        │
│  ┌─────────────────▼───────────────┐                                       │
│  │     Structure Evaluators        │  評估 Structure Spec（非 Markdown）   │
│  │  ┌──────────┐  ┌──────────┐     │                                       │
│  │  │Evaluator │  │Evaluator │     │                                       │
│  │  │    A     │  │    B     │     │                                       │
│  │  └────┬─────┘  └────┬─────┘     │                                       │
│  │       └──────┬──────┘           │                                       │
│  │              ▼                  │                                       │
│  │    ┌──────────────────┐         │                                       │
│  │    │ Final Structure  │         │  最終結構規格 + 改進建議              │
│  │    │  Specification   │         │                                       │
│  │    └────────┬─────────┘         │                                       │
│  └─────────────┼───────────────────┘                                       │
│                │                                                            │
│  ════════════════════════════════════════════════════════════════════════  │
│  格式化層 (Formatting Layer) - 負責「怎麼呈現」                             │
│  ════════════════════════════════════════════════════════════════════════  │
│                │                                                            │
│  Phase 4: Markmap Rendering                                                 │
│  ┌─────────────▼───────────────────┐                                       │
│  │       Markmap Writer            │                                       │
│  │                                 │                                       │
│  │  Inputs:                        │                                       │
│  │  • Final Structure Spec (★)    │  ← 結構規格                            │
│  │  • Evaluator Feedback           │  ← 改進建議                            │
│  │  • Problem Metadata (★)         │  ← 完整問題資料                        │
│  │  • Markmap Format Guide         │  ← 格式能力參考                        │
│  │                                 │                                       │
│  │  Output:                        │                                       │
│  │  • Complete Markmap Markdown    │  ← 唯一產生 Markdown 的地方           │
│  │                                 │                                       │
│  └─────────────┬───────────────────┘                                       │
│                │                                                            │
│  Phase 5: Translation (if needed)                                          │
│  ┌─────────────▼───────────────────┐                                       │
│  │        Translator               │                                       │
│  └─────────────┬───────────────────┘                                       │
│                │                                                            │
│  Phase 6: Output                                                           │
│  ┌─────────────▼───────────────────┐                                       │
│  │   Final Markmaps (.md + .html)  │                                       │
│  └─────────────────────────────────┘                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Concept: Structure Specification

### What is Structure Specification?

Structure Specification (結構規格) 是一個 YAML 格式的中間表示，用於描述 Markmap 的**內容和組織方式**，但**不包含格式細節**。

### Key Principles

| 原則 | 說明 |
|------|------|
| **只包含概念** | 描述「要什麼內容」，不描述「怎麼呈現」 |
| **使用 ID 引用** | 問題只記錄 ID，不記錄完整資訊 |
| **無 Markdown** | 完全沒有 Markdown 語法 |
| **無 URL** | 不包含任何連結 |
| **可選 format_hints** | 少數需要指定格式的情況使用 |

### Structure Specification Schema

```yaml
# =============================================================================
# Structure Specification Schema V1
# =============================================================================
# 這是 Agents 討論的對象，不是最終產品

# 基本資訊
metadata:
  title: "NeetCode Algorithm Patterns"
  description: "A comprehensive guide to algorithm patterns"
  version: "1.0"
  generated_by: "generalist"  # or "specialist"

# -----------------------------------------------------------------------------
# 組織策略 (Organization Strategy)
# -----------------------------------------------------------------------------
# 這是高層決策，影響整個 Markmap 的結構

organization:
  # 主要分組方式
  # Options: "pattern" | "difficulty" | "topic" | "progress" | "custom"
  primary_grouping: "pattern"
  
  # 次要分組方式 (optional)
  secondary_grouping: "difficulty"
  
  # 問題顯示選項
  display_options:
    show_complexity: true       # 顯示時間/空間複雜度
    show_difficulty: true       # 顯示難度標籤
    show_progress: true         # 顯示完成狀態
    show_topics: false          # 顯示 LeetCode topics
  
  # 特殊區段
  include_sections:
    learning_paths: true        # 包含學習路徑
    progress_summary: true      # 包含進度統計
    quick_reference: false      # 包含快速參考表

# -----------------------------------------------------------------------------
# 內容結構 (Content Structure)
# -----------------------------------------------------------------------------
# 定義每個 section 及其內容

sections:
  # 每個 section 定義一個分類
  - id: "two_pointers"
    name: "Two Pointers"
    importance: "core"          # core | intermediate | advanced | optional
    
    # 內容策略
    content:
      # 問題列表 (只記錄 ID)
      problems:
        - id: "0125"            # Valid Palindrome
          role: "foundation"    # foundation | practice | challenge
        - id: "0167"            # Two Sum II
          role: "practice"
        - id: "0015"            # 3Sum
          role: "challenge"
        - id: "0011"            # Container With Most Water
          role: "challenge"
      
      # 學習順序 (optional)
      learning_order: ["0125", "0167", "0015", "0011"]
      
      # 子分類 (optional)
      subcategories:
        - name: "Opposite Direction"
          problems: ["0125", "0167", "0011"]
        - name: "Same Direction"
          problems: ["0026", "0027"]
    
    # 格式提示 (optional，只在必要時使用)
    format_hints:
      should_fold: false        # 是否預設摺疊
      use_table: false          # 是否使用表格呈現
      highlight_level: "normal" # normal | emphasized | de-emphasized
    
    # 決策記錄 (internal，不會出現在最終產品)
    _decisions:
      - "Split into Opposite/Same Direction for clarity"
      - "Start with Easy problems for learning progression"

  - id: "sliding_window"
    name: "Sliding Window"
    importance: "core"
    content:
      problems:
        - id: "0003"
          role: "foundation"
        - id: "0076"
          role: "challenge"
        - id: "0424"
          role: "practice"
        - id: "0567"
          role: "practice"
      subcategories:
        - name: "Fixed Size Window"
          problems: ["0643", "1343"]
          description: "Window size is fixed"
        - name: "Dynamic Size Window"
          problems: ["0003", "0076", "0424", "0567"]
          description: "Window size varies based on conditions"
    format_hints:
      should_fold: true         # 問題多，建議摺疊
  
  - id: "binary_search"
    name: "Binary Search"
    importance: "core"
    content:
      problems:
        - id: "0704"
          role: "foundation"
        - id: "0033"
          role: "challenge"
        - id: "0153"
          role: "practice"

# -----------------------------------------------------------------------------
# 學習路徑 (Learning Paths) - Optional
# -----------------------------------------------------------------------------
# 定義推薦的學習順序

learning_paths:
  - id: "beginner_path"
    name: "Beginner's Path"
    description: "Start here if you're new to algorithm patterns"
    steps:
      - section: "two_pointers"
        problems: ["0125", "0167"]
        milestone: "Understand basic two pointer technique"
      - section: "sliding_window"
        problems: ["0003"]
        milestone: "Understand dynamic window"
      - section: "binary_search"
        problems: ["0704"]
        milestone: "Master basic binary search"
  
  - id: "advanced_path"
    name: "Advanced Challenges"
    description: "For those ready for harder problems"
    steps:
      - section: "two_pointers"
        problems: ["0015", "0011"]
      - section: "sliding_window"
        problems: ["0076"]

# -----------------------------------------------------------------------------
# 進度摘要 (Progress Summary) - Optional
# -----------------------------------------------------------------------------
# 用於生成統計表格

progress_summary:
  enabled: true
  group_by: "section"           # section | difficulty | pattern
  show_percentage: true

# -----------------------------------------------------------------------------
# 內部記錄 (Internal) - 不會出現在最終產品
# -----------------------------------------------------------------------------
_internal:
  # 決策日誌
  decision_log:
    - round: 1
      decision: "Use pattern-first organization"
      rationale: "Better for learning progression"
      source: "architect_strategist"
    - round: 2
      decision: "Split Two Pointers into subcategories"
      rationale: "Too many problems in one section"
      source: "ux_strategist"
  
  # 被拒絕的建議
  rejected_suggestions:
    - suggestion: "Organize by difficulty first"
      reason: "Loses pattern coherence"
      source: "round_1"
  
  # 版本歷史
  version_history:
    - version: "0.1"
      changes: "Initial structure from generalist"
    - version: "0.2"
      changes: "Added subcategories per architect suggestion"
    - version: "1.0"
      changes: "Final version after evaluation"
```

---

## Token Efficiency Comparison

假設討論 50 個問題，3 輪優化：

### V2: 傳遞完整 Markdown

```markdown
## Two Pointers
- [x] [LC-125 Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py) ✓
  - Time: $O(n)$ | Space: $O(1)$
- [ ] [LC-167 Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
  - Time: $O(n)$ | Space: $O(1)$
... (50 problems × ~200 chars each = ~10,000 chars per round)
```

**估計 Token**: ~15,000 tokens × 3 rounds = **~45,000 tokens**

### V3: 傳遞 Structure Spec

```yaml
sections:
  - id: "two_pointers"
    problems: ["0125", "0167", "0015", "0011"]
  - id: "sliding_window"
    problems: ["0003", "0076", "0424"]
... (50 problem IDs × ~10 chars = ~500 chars per round)
```

**估計 Token**: ~3,000 tokens × 3 rounds = **~9,000 tokens**

| 項目 | V2 | V3 | 節省 |
|------|----|----|------|
| 每輪 Token | ~15,000 | ~3,000 | **80%** |
| 3 輪總計 | ~45,000 | ~9,000 | **80%** |
| API 成本 | $0.90 | $0.18 | **$0.72** |

---

## Data Input Strategy

### Available Data Sources

| 資料類型 | 說明 | 大小 | 路徑 |
|----------|------|------|------|
| **Ontology** | 分類法定義（patterns, algorithms, data_structures） | 小 | `ontology/*.toml` |
| **Problem List** | 問題 ID + 標題 + 所屬 pattern | 中 | `meta/problems/*.toml` |
| **Problem Metadata (Full)** | 完整資訊（URL, complexity, solution_file） | 大 | `meta/problems/*.toml` |
| **Roadmaps** | 學習路徑定義 | 小 | `roadmaps/*.toml` |
| **Pattern Docs** | 各 pattern 的完整說明文件 | 大 | `docs/patterns/*.md` |

### Pattern Docs 包含的關鍵資訊

Pattern Docs（如 `docs/patterns/sliding_window.md`）包含非常豐富的資訊：

| 資訊類型 | 範例 | 對 Markmap 的價值 |
|----------|------|-------------------|
| **Sub-Pattern 分類** | Two Pointers → Opposite / Same-Direction / Fast-Slow | 決定 Markmap 的子分類結構 |
| **Base Template 關係** | LC-3 是 Sliding Window 的 base template | 決定學習順序和問題角色 |
| **Variation Delta** | "Delta from Base: Replace X with Y" | 理解問題之間的遞進關係 |
| **Comparison Table** | 各變體的對比表 | 可直接用於 Markmap |
| **Decision Flowchart** | 何時使用這個 pattern | 學習路徑設計參考 |
| **LeetCode Mapping** | 按 sub-pattern 分組的題目 | 直接影響問題分組 |

### Data Input Per Phase

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Data Input Strategy                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Phase 1: PLANNER                                                    │   │
│  │                                                                     │   │
│  │ INPUT:                                                              │   │
│  │   ✅ Ontology (完整)      - 需要知道有哪些分類可用                  │   │
│  │   ✅ Problem List (簡化)  - ID + 標題 + pattern，無 URL/complexity  │   │
│  │   ✅ Roadmaps (完整)      - 需要知道有哪些學習路徑                  │   │
│  │   ✅ Pattern Docs (完整)  - 需要知道 sub-pattern 結構 ⭐            │   │
│  │   ❌ Full Problem Metadata                                          │   │
│  │                                                                     │   │
│  │ 為什麼：Planner 需要知道 pattern 的內部結構來設計 Markmap          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Phase 2: STRATEGISTS (Divergent + Convergent)                       │   │
│  │                                                                     │   │
│  │ INPUT:                                                              │   │
│  │   ✅ Current Structure Spec     - 來自 Planner                      │   │
│  │   ✅ Pattern Docs (摘要版)      - sub-pattern + comparison table ⭐ │   │
│  │   ⚠️ Ontology (可選)            - 如果需要參考分類                  │   │
│  │   ❌ Problem List               - 不需要，已在 Spec 中              │   │
│  │   ❌ Full Problem Metadata                                          │   │
│  │                                                                     │   │
│  │ 為什麼：Strategists 需要參考 pattern 結構來驗證/建議分類            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Phase 2: INTEGRATOR                                                 │   │
│  │                                                                     │   │
│  │ INPUT:                                                              │   │
│  │   ✅ All Strategist Responses   - 所有創意和建議                    │   │
│  │   ✅ Current Structure Spec     - 需要知道現狀                      │   │
│  │   ❌ 所有原始資料               - 不需要                            │   │
│  │                                                                     │   │
│  │ 為什麼：專注於「整合意見」，不需要原始資料                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Phase 3: EVALUATOR                                                  │   │
│  │                                                                     │   │
│  │ INPUT:                                                              │   │
│  │   ✅ Final Structure Spec       - 最終結構規格                      │   │
│  │   ⚠️ Pattern Docs (可選)        - 驗證分類是否正確                  │   │
│  │   ❌ Problem Metadata                                               │   │
│  │                                                                     │   │
│  │ 為什麼：評估結構品質，不需要問題細節                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Phase 4: WRITER ⭐ (唯一需要完整資料)                                │   │
│  │                                                                     │   │
│  │ INPUT:                                                              │   │
│  │   ✅ Final Structure Spec       - 結構規格                          │   │
│  │   ✅ Evaluator Feedback         - 改進建議                          │   │
│  │   ✅ Full Problem Metadata ⭐   - 完整問題資料 (URL, complexity)    │   │
│  │   ✅ Pattern Docs (完整) ⭐     - 用於正確命名和 comparison table   │   │
│  │   ✅ Markmap Format Guide       - 格式參考                          │   │
│  │                                                                     │   │
│  │ 為什麼：Writer 需要完整資料來生成正確的 URL、complexity、命名       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pattern Docs: Full vs Summary Version

#### Full Version (給 Planner + Writer)

完整的 `docs/patterns/*.md` 文件，包含所有細節：
- Core Concepts
- Base Template + Variations
- Complete implementations
- Comparison tables
- Decision flowcharts

#### Summary Version (給 Strategists)

從完整版提取關鍵資訊，減少 Token 使用：

```yaml
# Pattern Summary for Strategists

sliding_window:
  sub_patterns:
    - name: "Maximize Window"
      description: "Find longest/largest valid window"
      problems: ["0003", "0340", "0424"]
    - name: "Minimize Window"
      description: "Find shortest valid window"
      problems: ["0076", "0209"]
    - name: "Fixed Size Window"
      description: "Window size is predetermined"
      problems: ["0567", "0438"]
  
  base_template: "0003"
  
  decision_hints:
    use_when: ["contiguous subarray", "incremental property"]
    avoid_when: ["non-contiguous", "non-local boundaries"]

two_pointers:
  sub_patterns:
    - name: "Opposite Pointers"
      description: "Start at both ends, move toward center"
      problems: ["0011", "0015", "0125", "0167", "0680"]
    - name: "Same-Direction (Writer)"
      description: "Both pointers move forward, one reads one writes"
      problems: ["0026", "0027", "0283"]
    - name: "Fast-Slow"
      description: "Different speeds for cycle detection"
      problems: ["0141", "0142", "0202", "0876"]
    - name: "Partitioning"
      description: "Divide array into regions"
      problems: ["0075"]
    - name: "Merge"
      description: "Merge sorted sequences"
      problems: ["0021", "0088"]
  
  base_template: "0167"
```

### Data Input Summary Table

| 階段 | Ontology | Problems | Roadmaps | Pattern Docs | Full Metadata |
|------|----------|----------|----------|--------------|---------------|
| **Planner** | ✅ 完整 | ✅ 簡化 | ✅ 完整 | ✅ 完整 | ❌ |
| **Strategist** | ⚠️ 可選 | ❌ | ❌ | ✅ 摘要版 | ❌ |
| **Integrator** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Evaluator** | ⚠️ 可選 | ❌ | ❌ | ⚠️ 可選 | ❌ |
| **Writer** | ❌ | ❌ | ❌ | ✅ 完整 | ✅ 完整 |

### Why This Strategy?

1. **減少 Token** - 中間階段不需要重複傳遞大量資料
2. **職責清晰** - 每個階段專注於自己的任務
3. **避免干擾** - 太多細節會讓 AI 分心
4. **Pattern 結構可見** - Planner 和 Strategists 都能看到 pattern 的內部結構

### Config Example

```yaml
# config.yaml

data_input:
  planner:
    include:
      - ontology: "full"
      - problems: "summary"        # ID, title, pattern, has_solution
      - roadmaps: "full"
      - pattern_docs: "full"       # 完整的 pattern 文檔
    exclude:
      - problem_metadata_full
  
  strategist:
    include:
      - structure_spec: "current"
      - pattern_docs: "summary"    # 只有 sub-pattern 摘要
      - ontology: "optional"
    exclude:
      - problems
      - roadmaps
      - problem_metadata_full
  
  integrator:
    include:
      - strategist_responses: "all"
      - structure_spec: "current"
    exclude:
      - all_original_data
  
  evaluator:
    include:
      - structure_spec: "final"
      - pattern_docs: "optional"   # 用於驗證
    exclude:
      - problem_metadata_full
  
  writer:
    include:
      - structure_spec: "final"
      - evaluator_feedback: "all"
      - problem_metadata: "full"   # 完整問題資料
      - pattern_docs: "full"       # 完整 pattern 文檔
      - format_guide: "full"
```

---

## Phase Details

### Phase 1: Structure Generation

**輸入**:
- Ontology (完整)
- Problem List (簡化 - ID, title, pattern, has_solution)
- Roadmaps (完整)
- Pattern Docs (完整) ⭐

**輸出**:
- Structure Specification (YAML)

**改變 from V2**:
- 不再產生 Markdown
- 產生 Structure Spec

**Planner Prompt 重點**:
```
You are a Structure Planner. Your job is to design the ORGANIZATION
and CONTENT STRATEGY for a Markmap, NOT the final formatting.

Output a Structure Specification in YAML format that describes:
1. How to organize the content (by pattern, difficulty, etc.)
2. Which problems to include and their roles
3. Learning progression recommendations

DO NOT output any Markdown. DO NOT include URLs.
Only output the Structure Specification.
```

### Phase 2: Content Strategy Optimization

**輸入**:
- Current Structure Specification
- Pattern Docs (摘要版) ⭐ - sub-pattern 結構和對應問題
- Other strategists' suggestions (in debate mode)
- Ontology (可選)

**輸出**:
- Updated Structure Specification
- Decision rationale (stored in `_internal`)

**改變 from V2**:
- Optimizers 改名為 Content Strategists
- 討論內容策略，不討論格式
- 沒有 Markdown 輸出
- 可參考 Pattern Docs 驗證分類

**Strategist Prompt 重點**:
```
You are a Content Strategist. Analyze the Structure Specification and
suggest improvements to the CONTENT ORGANIZATION, not the formatting.

You have access to Pattern Docs summaries that show:
- Sub-pattern classifications (e.g., Two Pointers → Opposite/Same-Direction/Fast-Slow)
- Base template and variation relationships
- Which problems belong to which sub-pattern

Focus on:
- Is the grouping logical and aligned with Pattern Docs?
- Are problems correctly categorized under the right sub-pattern?
- Is the learning progression smooth?
- Are important patterns or sub-patterns missing?

DO NOT suggest formatting changes (checkboxes, bold, etc.)
Those are handled by the Writer in the final phase.
```

### Phase 3: Evaluation

**輸入**:
- All Structure Specifications (from different generators/rounds)

**輸出**:
- Selected best Structure Specification
- Improvement suggestions (content-level, not formatting)

**改變 from V2**:
- Judges 改名為 Evaluators
- 評估 Structure Spec，不是 Markdown
- 建議是內容層面的

### Phase 4: Markmap Rendering

**輸入**:
1. **Final Structure Specification** - 最終結構規格
2. **Evaluator Feedback** - 改進建議
3. **Full Problem Metadata** - 完整問題資料 (★ 此時才載入)
4. **Pattern Docs (完整)** ⭐ - 用於正確命名和 comparison table
5. **Markmap Format Guide** - 格式能力參考

**輸出**:
- Complete Markmap Markdown

**Writer 使用 Pattern Docs 來**:
- 使用正確的 sub-pattern 命名（如 "Opposite Pointers" 而非 "Two End"）
- 可能引用或嵌入 Comparison Table
- 確保術語和分類與文檔一致

**Writer 職責**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Writer Rendering Process                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input: Structure Specification + Metadata                      │
│         ↓                                                       │
│  Step 1: 解析 Structure Spec                                    │
│         • 讀取 organization 策略                                │
│         • 讀取 sections 定義                                    │
│         • 讀取 format_hints                                     │
│         ↓                                                       │
│  Step 2: 查詢 Metadata                                          │
│         • 根據 problem ID 獲取完整資訊                          │
│         • title, slug, difficulty, complexity, solution_file    │
│         ↓                                                       │
│  Step 3: 生成 URL                                               │
│         • 有 solution_file → GitHub URL                         │
│         • 無 solution_file → LeetCode URL                       │
│         ↓                                                       │
│  Step 4: 套用格式                                               │
│         • YAML frontmatter                                      │
│         • Checkboxes ([x] / [ ])                                │
│         • KaTeX ($O(n)$)                                        │
│         • Fold (<!-- markmap: fold -->)                         │
│         • Tables (if format_hint says so)                       │
│         ↓                                                       │
│  Step 5: 應用 Evaluator 建議                                    │
│         • 結構調整                                              │
│         • 命名優化                                              │
│         ↓                                                       │
│  Output: Complete Markmap Markdown                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## format_hints Usage

`format_hints` 用於少數確實需要指定格式的情況。

### When to Use format_hints

| 情況 | format_hint | 說明 |
|------|-------------|------|
| 問題太多 | `should_fold: true` | 預設摺疊避免過長 |
| 需要比較表 | `use_table: true` | 用表格呈現 |
| 重點章節 | `highlight_level: emphasized` | 視覺強調 |
| 次要內容 | `highlight_level: de-emphasized` | 視覺弱化 |

### When NOT to Use format_hints

這些由 Writer 自動處理，不需要 hint：
- Checkbox ([x] / [ ]) - 根據 has_solution 自動決定
- Complexity ($O(n)$) - 根據 display_options 和 metadata 自動加入
- Links - 自動生成
- Bold/Italic - Writer 決定

### Example

```yaml
sections:
  - id: "sliding_window"
    name: "Sliding Window"
    content:
      problems: ["0003", "0076", "0424", "0567", "0239", "0480"]
    format_hints:
      should_fold: true    # ✓ 6+ problems, suggest folding
      use_table: false     # Default, don't need to specify
```

---

## Agent Role Changes

### V2 → V3 Mapping

| V2 Role | V3 Role | 改變 |
|---------|---------|------|
| Generator | Structure Planner | 產出 Structure Spec，不是 Markdown |
| Optimizer | Content Strategist | 討論內容策略，不討論格式 |
| Summarizer | Integrator | 整合建議，更新 Structure Spec |
| Judge | Evaluator | 評估 Structure Spec，不是 Markdown |
| Writer | Markmap Renderer | 唯一產生 Markdown 的角色 |

### New Prompt Focus

**Content Strategists 不再討論**:
- ❌ "Use bold for difficulty"
- ❌ "Add checkboxes"
- ❌ "Use this URL format"
- ❌ "The markdown should look like..."

**Content Strategists 專注討論**:
- ✓ "Two Pointers should be split into subcategories"
- ✓ "Learning order should be Easy → Medium → Hard"
- ✓ "This problem belongs to Sliding Window, not Two Pointers"
- ✓ "Add a progress summary section"

---

## Strict Output Separation

### Problem in V2

V2 的 Summarizer 輸出混合了過程和產品：

```markdown
# Round 1 Summary                    ← 過程記錄 (不該出現在最終產品)

## Optimizer Suggestions Summary     ← 過程記錄
...

## Unified Markmap                   ← 產品 (被埋在過程記錄裡)
...

## Change Log                        ← 過程記錄
```

### Solution in V3

嚴格分離：

```yaml
# Integrator Output - 兩個獨立部分

# Part 1: Process Record (for logging/debugging only)
_internal:
  decision_log: [...]
  rejected_suggestions: [...]

# Part 2: Product (the actual Structure Spec)
metadata:
  title: "..."
sections:
  - id: "..."
    ...
```

**規則**: 任何以 `_` 開頭的欄位都是內部記錄，Writer 會忽略。

---

## Validation Rules

在 Pipeline 各階段加入驗證：

### After Structure Planner

```python
def validate_structure_spec(spec: dict) -> bool:
    """確保是有效的 Structure Spec"""
    required_keys = ["metadata", "organization", "sections"]
    for key in required_keys:
        if key not in spec:
            return False
    
    # 不該有 Markdown
    spec_str = yaml.dump(spec)
    if "```" in spec_str or "- [x]" in spec_str:
        return False
    
    # 不該有 URL
    if "http://" in spec_str or "https://" in spec_str:
        return False
    
    return True
```

### After Markmap Renderer (Writer)

```python
def validate_final_output(output: str) -> bool:
    """確保最終輸出是純 Markmap，無過程記錄"""
    forbidden_patterns = [
        r"Round \d+ Summary",
        r"Optimizer Suggestions",
        r"Consensus Adopted",
        r"Conflicts Resolved",
        r"Change Log",
        r"_internal",
        r"_decisions"
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, output):
            return False
    return True
```

---

## Configuration Changes (V3)

```yaml
# =============================================================================
# AI Markmap Agent Configuration V3
# =============================================================================

# -----------------------------------------------------------------------------
# Workflow Configuration
# -----------------------------------------------------------------------------
workflow:
  optimization_rounds: 3
  
  # V3: Renamed for clarity
  strategist_count: 3       # was: optimizer_count
  evaluator_count: 2        # was: judge_count
  
  # Evaluation settings (simplified, no debate needed)
  enable_evaluation_discussion: true
  max_evaluation_rounds: 2

# -----------------------------------------------------------------------------
# Model Configuration
# -----------------------------------------------------------------------------
models:
  # Phase 1: Structure Planning
  structure_planner:
    generalist:
      model: "gpt-4o"
      persona_prompt: "prompts/planners/generalist-planner-persona.md"
      behavior_prompt: "prompts/planners/generalist-planner-behavior.md"
      temperature: 0.7
    specialist:
      model: "gpt-4o"
      persona_prompt: "prompts/planners/specialist-planner-persona.md"
      behavior_prompt: "prompts/planners/specialist-planner-behavior.md"
      temperature: 0.5

  # Phase 2: Content Strategy
  content_strategist:
    - id: "architect_strategist"
      name: "Architecture Strategist"
      model: "gpt-4o"
      persona_prompt: "prompts/strategists/architect-strategist-persona.md"
      behavior_prompt: "prompts/strategists/architect-strategist-behavior.md"
      focus: "structure_modularity"
    
    - id: "professor_strategist"
      name: "Academic Strategist"
      model: "gpt-4o"
      persona_prompt: "prompts/strategists/professor-strategist-persona.md"
      behavior_prompt: "prompts/strategists/professor-strategist-behavior.md"
      focus: "correctness_completeness"
    
    - id: "ux_strategist"
      name: "UX Strategist"
      model: "gpt-4o"
      persona_prompt: "prompts/strategists/ux-strategist-persona.md"
      behavior_prompt: "prompts/strategists/ux-strategist-behavior.md"
      focus: "user_experience"

  # Phase 2: Integration
  integrator:
    model: "gpt-4o"
    persona_prompt: "prompts/integrator/integrator-persona.md"
    behavior_prompt: "prompts/integrator/integrator-behavior.md"
    temperature: 0.5

  # Phase 3: Evaluation
  evaluator:
    - id: "structure_evaluator"
      name: "Structure Evaluator"
      model: "gpt-4o"
      behavior_prompt: "prompts/evaluators/structure-evaluator-behavior.md"
      criteria:
        - "logical_organization"
        - "appropriate_depth"
        - "balanced_sections"
    
    - id: "content_evaluator"
      name: "Content Evaluator"
      model: "gpt-4o"
      behavior_prompt: "prompts/evaluators/content-evaluator-behavior.md"
      criteria:
        - "coverage"
        - "learning_progression"
        - "practical_value"

  # Phase 4: Rendering (unchanged from V2)
  writer:
    model: "gpt-4o"
    persona_prompt: "prompts/writer/writer-persona.md"
    behavior_prompt: "prompts/writer/writer-behavior.md"
    format_guide: "prompts/writer/markmap-format-guide.md"
    temperature: 0.5
    max_tokens: 8192
```

---

## File Structure Changes

```
prompts/
├── planners/                       # NEW (was generators/)
│   ├── generalist-planner-persona.md
│   ├── generalist-planner-behavior.md
│   ├── specialist-planner-persona.md
│   └── specialist-planner-behavior.md
├── strategists/                    # NEW (was optimizers/)
│   ├── architect-strategist-persona.md
│   ├── architect-strategist-behavior.md
│   ├── professor-strategist-persona.md
│   ├── professor-strategist-behavior.md
│   ├── ux-strategist-persona.md
│   └── ux-strategist-behavior.md
├── integrator/                     # NEW (was summarizer/)
│   ├── integrator-persona.md
│   └── integrator-behavior.md
├── evaluators/                     # NEW (was judges/)
│   ├── structure-evaluator-behavior.md
│   └── content-evaluator-behavior.md
└── writer/                         # UNCHANGED
    ├── writer-persona.md
    ├── writer-behavior.md
    └── markmap-format-guide.md
```

---

## Migration from V2

### Step 1: Create Structure Spec Schema

1. 定義完整的 Structure Specification YAML schema
2. 建立驗證函數

### Step 2: Rewrite Prompts

1. Planners: 產出 Structure Spec，不是 Markdown
2. Strategists: 討論內容策略，不是格式
3. Integrator: 整合成 Structure Spec，不混入過程記錄
4. Evaluators: 評估 Structure Spec
5. Writer: 讀取 Structure Spec + Metadata → Markdown

### Step 3: Update Pipeline Code

1. 修改 state.py 加入 Structure Spec 類型
2. 修改 graph.py 調整節點流程
3. 加入驗證步驟

### Step 4: Test

1. 驗證每個階段的輸出格式
2. 確認最終輸出無過程記錄
3. 比較 Token 使用量

---

## Summary

| 項目 | V2 | V3 |
|------|----|----|
| 討論對象 | 完整 Markdown | Structure Specification |
| 中間格式 | Markdown | YAML (概念層) |
| URL 處理 | 每階段都有 | 只在 Writer |
| Token 效率 | 較低 | 節省 ~80% |
| 過程/產品分離 | 混合 | 嚴格分離 |
| 格式討論 | 分散 | 集中在 Writer |
| Agent 角色 | Optimizer/Judge | Strategist/Evaluator |

---

## Scalable N-Strategist Architecture

V3 設計支援**任意數量的 Strategists**，從 3 個到 7 個甚至更多，流程會自動適應。

### Core Principle

```
N = len(config.models.content_strategist)  # 自動計算，不需手動設定

Round 1: N 個 strategists 並行執行
    ↓
Integrator: 自動處理 N 個意見 → 識別共識/衝突
    ↓
Round 2+: 只有「相關」的 strategists 參與 (動態決定)
    ↓
Early Stop: 無衝突時跳過後續輪次
```

### Scalable Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Scalable Multi-Strategist Architecture                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Config: N strategists (自動從 content_strategist 陣列計算)                 │
│                                                                             │
│  ═══════════════════════════════════════════════════════════════════════   │
│  Round 1: Breadth Exploration (ALL strategists, PARALLEL)                   │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐      ┌────────┐             │
│   │  S[1]  │ │  S[2]  │ │  S[3]  │ │  S[4]  │ ...  │  S[N]  │             │
│   └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘      └───┬────┘             │
│       │          │          │          │               │                   │
│       └──────────┴──────────┴──────────┴───────────────┘                   │
│                              │                                              │
│                              ▼                                              │
│                    ┌──────────────────┐                                     │
│                    │    Integrator    │                                     │
│                    │                  │                                     │
│                    │  • 收集 N 個意見  │                                     │
│                    │  • 識別共識       │  (≥ threshold 同意)                 │
│                    │  • 識別衝突       │  (< threshold 同意)                 │
│                    │  • 標記相關者     │                                     │
│                    └────────┬─────────┘                                     │
│                             │                                               │
│            ┌────────────────┼────────────────┐                              │
│            ▼                ▼                ▼                              │
│      ┌──────────┐    ┌───────────┐    ┌───────────┐                        │
│      │ 共識 ✓   │    │ 衝突 A    │    │ 衝突 B    │                        │
│      │ (採納)   │    │ (待討論)  │    │ (待討論)  │                        │
│      └──────────┘    └───────────┘    └───────────┘                        │
│                             │                │                              │
│  ═══════════════════════════════════════════════════════════════════════   │
│  Round 2+: Focused Resolution (ONLY relevant strategists)                  │
│  ═══════════════════════════════════════════════════════════════════════   │
│                             │                │                              │
│                             ▼                ▼                              │
│           ┌─────────────────────┐  ┌─────────────────────┐                 │
│           │ 衝突 A 討論          │  │ 衝突 B 討論          │  ← 可並行      │
│           │ 只有 S[1], S[3], S[5]│  │ 只有 S[2], S[4]     │                 │
│           │ 參與 (動態決定)      │  │ 參與                 │                 │
│           └──────────┬──────────┘  └──────────┬──────────┘                 │
│                      │                        │                             │
│                      ▼                        ▼                             │
│               ┌────────────┐           ┌────────────┐                       │
│               │  決議 A ✓  │           │  決議 B ✓  │                       │
│               └────────────┘           └────────────┘                       │
│                      │                        │                             │
│  ═══════════════════════════════════════════════════════════════════════   │
│  Early Stop / Arbitration                                                   │
│  ═══════════════════════════════════════════════════════════════════════   │
│                      │                        │                             │
│                      └────────────┬───────────┘                             │
│                                   │                                         │
│                    (如果還有未解決衝突 && 超過 max_rounds)                   │
│                                   ▼                                         │
│                          ┌─────────────────┐                                │
│                          │   Arbitrator    │                                │
│                          │ (最終決策者)    │                                │
│                          └────────┬────────┘                                │
│                                   │                                         │
│                                   ▼                                         │
│                       Final Structure Spec                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Dynamic Consensus Calculation

共識門檻根據 N 動態計算：

```python
def calculate_consensus(
    suggestions: List[Suggestion], 
    threshold: float = 0.8
) -> ConsensusResult:
    """
    計算 N 個 strategists 的共識
    
    Args:
        suggestions: N 個 strategist 的建議
        threshold: 共識門檻 (0.0 - 1.0)
    
    Examples:
        N=3, threshold=0.8 → 需要 3 人同意 (ceil(3 * 0.8) = 3)
        N=4, threshold=0.8 → 需要 4 人同意 (ceil(4 * 0.8) = 4)
        N=5, threshold=0.8 → 需要 4 人同意 (ceil(5 * 0.8) = 4)
        N=6, threshold=0.8 → 需要 5 人同意 (ceil(6 * 0.8) = 5)
        N=7, threshold=0.8 → 需要 6 人同意 (ceil(7 * 0.8) = 6)
    """
    n = len(suggestions)
    required_agreement = ceil(n * threshold)
    
    # 收集所有討論的 topic
    all_topics = set()
    for s in suggestions:
        all_topics.update(s.topics)
    
    consensus = []
    conflicts = []
    
    for topic in all_topics:
        # 收集每個 strategist 對此 topic 的立場
        positions = {}
        for s in suggestions:
            if topic in s.positions:
                positions[s.id] = s.positions[topic]
        
        # 按立場分組
        position_groups = defaultdict(list)
        for strategist_id, position in positions.items():
            position_groups[position].append(strategist_id)
        
        # 找出最多人支持的立場
        max_agreement = max(len(v) for v in position_groups.values())
        
        if max_agreement >= required_agreement:
            # ✓ 達成共識
            winning = max(position_groups.items(), key=lambda x: len(x[1]))
            consensus.append({
                "topic": topic,
                "decision": winning[0],
                "agreed_by": winning[1],
                "agreement_ratio": max_agreement / n
            })
        else:
            # ✗ 有衝突，需要進一步討論
            conflicts.append({
                "id": f"conflict_{len(conflicts) + 1}",
                "topic": topic,
                "positions": positions,
                "relevant_strategists": list(positions.keys())
            })
    
    return ConsensusResult(consensus=consensus, conflicts=conflicts)
```

### Integrator Output Schema

```yaml
# Integrator 輸出格式
round_result:
  round_number: 1
  
  # 所有人都同意的部分 → 直接採納
  consensus:
    - topic: "primary_grouping"
      decision: "pattern"
      agreed_by: ["architect", "professor", "ux", "learning"]
      agreement_ratio: 1.0
    
    - topic: "include_learning_paths"
      decision: true
      agreed_by: ["professor", "ux", "learning"]
      agreement_ratio: 0.75
  
  # 有分歧的部分 → 進入下一輪討論
  conflicts:
    - id: "conflict_1"
      topic: "Should Two Pointers have subcategories?"
      positions:
        architect: "yes_split_by_direction"
        professor: "no_keep_flat"
        ux: "yes_split_by_direction"
        learning: "yes_split_by_difficulty"
      relevant_strategists: ["architect", "professor", "ux", "learning"]
      
    - id: "conflict_2"
      topic: "Include progress summary table?"
      positions:
        architect: "no"
        ux: "yes"
      relevant_strategists: ["architect", "ux"]  # professor 和 learning 沒意見
  
  # 更新後的 Structure Spec (含已採納的共識)
  updated_structure_spec:
    metadata: { ... }
    organization:
      primary_grouping: "pattern"  # 已採納共識
    sections: [ ... ]
```

### Focused Discussion Prompt (Round 2+)

```markdown
# Focused Discussion: Conflict Resolution

## Context
Round 1 reached consensus on most points. However, there are 
unresolved conflicts that need your input.

## ✓ Already Decided (DO NOT REDISCUSS)
1. Use pattern-first organization
2. Include learning paths
3. Show complexity for solved problems

## ⚠️ Conflict for Your Input

**Topic**: Should Two Pointers have subcategories?

**Current Positions**:
| Strategist | Position | Rationale |
|------------|----------|-----------|
| Architect | Split by direction | Better modularity |
| Professor | Keep flat | Simpler mental model |
| UX | Split by direction | Easier navigation |
| Learning | Split by difficulty | Better progression |

**Your Task**:
Provide your FINAL position. You may:
1. Maintain your position with stronger arguments
2. Change to support another position
3. Propose a compromise

**Output Format**:
```yaml
final_position: "your_choice"
reasoning: "why this is the best choice"
compromise_proposal: "optional - if you have a middle ground"
```
```

### Efficiency Analysis by N

| N | Round 1 | Round 2 (worst) | Round 3 | Total (worst) | Total (best) | 並行後時間 |
|---|---------|-----------------|---------|---------------|--------------|-----------|
| 3 | 3 並行 + 1 | ~4 | 1 | 9 | 5 | ~40s |
| 4 | 4 並行 + 1 | ~6 | 1 | 12 | 6 | ~50s |
| 5 | 5 並行 + 1 | ~8 | 1 | 15 | 7 | ~60s |
| 6 | 6 並行 + 1 | ~10 | 1 | 18 | 8 | ~70s |
| 7 | 7 並行 + 1 | ~12 | 1 | 21 | 9 | ~80s |

**關鍵優化**：
- Round 1 的 N 個調用是**並行**的，時間 ≈ 單次調用
- Round 2+ 的衝突處理也可以**並行**
- 早停機制：無衝突時跳過後續輪次

### Scalable Config Example

```yaml
# config.yaml - 可自由增減 strategists

workflow:
  # 最大討論輪數 (早停時可能更少)
  max_discussion_rounds: 3
  
  # 共識門檻：多少比例同意算共識
  # N=5 時，0.8 表示至少 4 人同意
  consensus_threshold: 0.8
  
  # 是否允許並行處理多個衝突
  parallel_conflict_resolution: true
  
  # 仲裁設定
  arbitration:
    enabled: true
    # 仲裁者優先採用哪個 strategist 的建議
    priority_order: ["professor", "architect", "ux"]

models:
  content_strategist:
    # === 核心 Strategists (建議保留) ===
    
    - id: "architect"
      name: "Architecture Strategist"
      focus: "structure_modularity"
      model: "gpt-4o"
      persona_prompt: "prompts/strategists/architect-persona.md"
      behavior_prompt: "prompts/strategists/architect-behavior.md"
    
    - id: "professor"
      name: "Academic Strategist"
      focus: "correctness_completeness"
      model: "gpt-4o"
      persona_prompt: "prompts/strategists/professor-persona.md"
      behavior_prompt: "prompts/strategists/professor-behavior.md"
    
    - id: "ux"
      name: "UX Strategist"
      focus: "user_experience"
      model: "gpt-4o"
      persona_prompt: "prompts/strategists/ux_persona.md"
      behavior_prompt: "prompts/strategists/ux_behavior.md"
    
    # === 可選 Strategists (取消註解啟用) ===
    
    # - id: "learning"
    #   name: "Learning Path Strategist"
    #   focus: "learning_progression"
    #   description: "專注於學習順序、難度曲線、里程碑設計"
    #   model: "gpt-4o"
    #   persona_prompt: "prompts/strategists/learning_persona.md"
    #   behavior_prompt: "prompts/strategists/learning_behavior.md"
    
    # - id: "practical"
    #   name: "Practical Application Strategist"
    #   focus: "real_world_usage"
    #   description: "專注於實際應用、面試準備、常見題型"
    #   model: "gpt-4o"
    #   persona_prompt: "prompts/strategists/practical_persona.md"
    #   behavior_prompt: "prompts/strategists/practical_behavior.md"
    
    # - id: "efficiency"
    #   name: "Cognitive Load Strategist"
    #   focus: "cognitive_efficiency"
    #   description: "專注於認知負擔、資訊密度、可讀性"
    #   model: "gpt-4o"
    #   persona_prompt: "prompts/strategists/efficiency_persona.md"
    #   behavior_prompt: "prompts/strategists/efficiency_behavior.md"
    
    # - id: "accessibility"
    #   name: "Accessibility Strategist"
    #   focus: "universal_access"
    #   description: "專注於無障礙設計、國際化、多元學習者"
    #   model: "gpt-4o"
    #   persona_prompt: "prompts/strategists/accessibility_persona.md"
    #   behavior_prompt: "prompts/strategists/accessibility_behavior.md"
```

### Recommended Strategist Roles

| ID | 名稱 | Focus | 適用場景 |
|----|------|-------|----------|
| `architect` | Architecture | 結構、模組化、層級 | **必選** - 確保結構清晰 |
| `professor` | Academic | 正確性、完整性 | **必選** - 確保內容正確 |
| `ux` | UX | 使用者體驗、導航 | **必選** - 確保易用性 |
| `learning` | Learning Path | 學習順序、難度曲線 | 教學導向的 Markmap |
| `practical` | Practical | 實際應用、面試準備 | 面試準備導向 |
| `efficiency` | Efficiency | 認知負擔、資訊密度 | 大型 Markmap |
| `accessibility` | Accessibility | 無障礙、國際化 | 公開發布的 Markmap |

### Pipeline Pseudocode

```python
class ScalableDiscussionOrchestrator:
    def __init__(self, config):
        # 自動從 config 讀取 strategists 列表
        self.strategists = config.models.content_strategist
        self.n = len(self.strategists)
        self.max_rounds = config.workflow.max_discussion_rounds
        self.threshold = config.workflow.consensus_threshold
        self.parallel_conflicts = config.workflow.parallel_conflict_resolution
    
    async def run(self, initial_spec: StructureSpec) -> StructureSpec:
        current_spec = initial_spec
        
        # ═══════════════════════════════════════════════════════════
        # Round 1: All N strategists in parallel
        # ═══════════════════════════════════════════════════════════
        suggestions = await self.run_all_parallel(current_spec)
        
        # Integrate and identify consensus/conflicts
        result = await self.integrator.process(suggestions, self.threshold)
        current_spec = result.updated_structure_spec
        
        # Early stop if no conflicts
        if not result.conflicts:
            logger.info("Round 1: Full consensus reached, skipping further rounds")
            return current_spec
        
        # ═══════════════════════════════════════════════════════════
        # Round 2+: Focused resolution
        # ═══════════════════════════════════════════════════════════
        for round_num in range(2, self.max_rounds + 1):
            logger.info(f"Round {round_num}: {len(result.conflicts)} conflicts to resolve")
            
            if self.parallel_conflicts:
                # 並行處理所有衝突
                resolutions = await self.resolve_conflicts_parallel(result.conflicts)
            else:
                # 串行處理
                resolutions = await self.resolve_conflicts_serial(result.conflicts)
            
            # 更新 spec 和剩餘衝突
            current_spec, remaining_conflicts = self.apply_resolutions(
                current_spec, resolutions
            )
            
            # Early stop if all resolved
            if not remaining_conflicts:
                logger.info(f"Round {round_num}: All conflicts resolved")
                break
            
            result.conflicts = remaining_conflicts
        
        # ═══════════════════════════════════════════════════════════
        # Arbitration: If still conflicts after max rounds
        # ═══════════════════════════════════════════════════════════
        if result.conflicts:
            logger.warning(f"Arbitration needed for {len(result.conflicts)} conflicts")
            for conflict in result.conflicts:
                decision = await self.arbitrator.decide(conflict)
                current_spec = self.apply_decision(current_spec, conflict, decision)
        
        return current_spec
    
    async def run_all_parallel(self, spec: StructureSpec) -> List[Suggestion]:
        """並行執行所有 N 個 strategists"""
        tasks = [
            self.call_strategist(s, spec) 
            for s in self.strategists
        ]
        return await asyncio.gather(*tasks)
    
    async def resolve_conflicts_parallel(
        self, conflicts: List[Conflict]
    ) -> List[Resolution]:
        """並行處理多個衝突"""
        tasks = [
            self.resolve_single_conflict(c) 
            for c in conflicts
        ]
        return await asyncio.gather(*tasks)
    
    async def resolve_single_conflict(self, conflict: Conflict) -> Resolution:
        """只邀請相關 strategists 討論單一衝突"""
        relevant_ids = conflict.relevant_strategists
        
        if len(relevant_ids) == 1:
            # 只有一人有意見 → 直接採納
            return Resolution(
                conflict_id=conflict.id,
                decision=conflict.positions[relevant_ids[0]],
                method="single_opinion"
            )
        
        # 多人有意見 → 聚焦討論
        relevant_strategists = [
            s for s in self.strategists if s.id in relevant_ids
        ]
        
        focused_suggestions = await asyncio.gather(*[
            self.call_strategist_focused(s, conflict)
            for s in relevant_strategists
        ])
        
        # 檢查是否達成共識
        return self.check_resolution(conflict, focused_suggestions)
```

---

## Appendix A: Complete Structure Spec Example

見 `examples/structure_spec_example.yaml`

## Appendix B: Strategist Prompt Templates

見 `prompts/strategists/` 目錄



# AI Markmap Agent - Design V2

## Overview

本文件描述 AI Markmap Agent 的第二版設計，重點改進包括：
1. 延遲連結處理（減少 prompt 負擔）
2. 多人評審與辯論機制
3. 專職 Markmap 撰寫員產出最終版本

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI Markmap Agent V2                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Phase 1: Baseline Generation                                               │
│  ┌──────────────┐  ┌──────────────┐                                        │
│  │  Generalist  │  │  Specialist  │  (per language with mode="generate")   │
│  └──────┬───────┘  └──────┬───────┘                                        │
│         │                 │                                                 │
│         ▼                 ▼                                                 │
│  ┌─────────────────────────────────┐                                       │
│  │    Baseline Markmaps (Draft)    │  ← 不含具體連結，只有問題 ID/標題     │
│  └─────────────┬───────────────────┘                                       │
│                │                                                            │
│  Phase 2: Optimization Rounds (×N)                                         │
│  ┌─────────────▼───────────────────┐                                       │
│  │         Optimizers (3+)         │  討論結構、分類、命名                  │
│  │  ┌─────────┐ ┌─────────┐ ┌────┐ │                                       │
│  │  │Architect│ │Professor│ │API │ │                                       │
│  │  └────┬────┘ └────┬────┘ └─┬──┘ │                                       │
│  │       └───────────┼────────┘    │                                       │
│  │                   ▼             │                                       │
│  │           ┌────────────┐        │                                       │
│  │           │ Summarizer │        │                                       │
│  │           └─────┬──────┘        │                                       │
│  └─────────────────┼───────────────┘                                       │
│                    │                                                        │
│  Phase 3: Evaluation & Debate                                              │
│  ┌─────────────────▼───────────────┐                                       │
│  │     Judges / Debaters (2+)      │  評分、辯論、選出最佳版本             │
│  │  ┌──────────┐  ┌──────────┐     │                                       │
│  │  │ Judge A  │  │ Judge B  │ ... │  (數量可配置)                         │
│  │  └────┬─────┘  └────┬─────┘     │                                       │
│  │       └──────┬──────┘           │                                       │
│  │              ▼                  │                                       │
│  │    ┌──────────────────┐         │                                       │
│  │    │  Debate Rounds   │         │  多輪辯論達成共識                     │
│  │    └────────┬─────────┘         │                                       │
│  │             ▼                   │                                       │
│  │    ┌──────────────────┐         │                                       │
│  │    │ Selected Winner  │         │  選出最佳 Markmap 結構                │
│  │    └────────┬─────────┘         │                                       │
│  └─────────────┼───────────────────┘                                       │
│                │                                                            │
│  Phase 4: Final Markmap Writing                                            │
│  ┌─────────────▼───────────────────┐                                       │
│  │      Markmap Writer (NEW)       │                                       │
│  │                                 │                                       │
│  │  Inputs:                        │                                       │
│  │  • Selected Markmap structure   │                                       │
│  │  • Judge feedback & suggestions │                                       │
│  │  • Problem metadata (★)         │  ← 此時才讀取 metadata                │
│  │  • Markmap format guide         │  ← 提示 markmap 完整格式能力          │
│  │                                 │                                       │
│  │  Responsibilities:              │                                       │
│  │  • Apply judge suggestions      │                                       │
│  │  • Generate proper links:       │                                       │
│  │    - GitHub solution (if exists)│                                       │
│  │    - LeetCode problem (fallback)│                                       │
│  │  • Apply Markmap formatting     │                                       │
│  │    - YAML frontmatter           │                                       │
│  │    - Checkboxes, KaTeX, etc.    │                                       │
│  │                                 │                                       │
│  └─────────────┬───────────────────┘                                       │
│                │                                                            │
│  Phase 5: Translation (if needed)                                          │
│  ┌─────────────▼───────────────────┐                                       │
│  │        Translator               │  mode="translate" 的語言              │
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

## Phase Details

### Phase 1: Baseline Generation

與 V1 相同，但有一個重要改變：

**Draft Mode（草稿模式）**
- 生成時**不處理具體連結**
- 只使用問題 ID 和標題作為佔位符
- 減少 prompt 中的 metadata 負擔

```markdown
## Two Pointers
- [ ] LC-125 Valid Palindrome
- [ ] LC-167 Two Sum II
```

### Phase 2: Optimization Rounds

與 V1 相同：
- 多個 Optimizer 提供建議
- Summarizer 整合建議並產出改進版本
- 可配置輪數

**重點：此階段仍使用 Draft Mode，不處理連結**

### Phase 3: Evaluation & Debate (改進)

#### 3.1 Judges（評審）

評審負責評分和選擇最佳版本。

**配置結構：**
```yaml
models:
  judges:
    - id: "judge_structure"
      name: "Structure Judge"
      model: "gpt-4o"
      persona_prompt: "prompts/judges/judge_structure_persona.md"
      behavior_prompt: "prompts/judges/judge_structure_behavior.md"
      temperature: 0.4
      criteria:
        - "hierarchy_quality"
        - "logical_grouping"
        - "depth_balance"
    
    - id: "judge_completeness"
      name: "Completeness Judge"
      model: "gpt-4o"
      persona_prompt: "prompts/judges/judge-completeness-persona.md"
      behavior_prompt: "prompts/judges/judge-completeness-behavior.md"
      temperature: 0.4
      criteria:
        - "coverage"
        - "practical_value"
        - "learning_path"
    
    # 可繼續添加更多評審...
```

#### 3.2 Debate（辯論）

評審之間進行辯論以達成共識。

**配置結構：**
```yaml
workflow:
  # Debate settings
  enable_debate: true
  max_debate_rounds: 3
  debate_consensus_threshold: 0.8  # 80% 同意即達成共識
```

**辯論流程：**
1. 每位評審獨立評分
2. 若評分差異大，進入辯論
3. 評審交換意見、反駁、調整評分
4. 達成共識或達到最大輪數
5. 產出：選出的最佳版本 + 改進建議清單

#### 3.3 Output

```python
{
    "selected_markmap": "...",           # 選出的最佳 Markmap
    "judge_feedback": [                  # 評審反饋
        {
            "judge_id": "judge_structure",
            "score": 85,
            "strengths": ["...", "..."],
            "improvements": ["...", "..."]
        },
        # ...
    ],
    "consensus_suggestions": [           # 共識改進建議
        "Add more examples under DP section",
        "Split 'Arrays' into sub-categories",
        # ...
    ]
}
```

### Phase 4: Final Markmap Writing (NEW)

這是**新增的關鍵階段**，由專職的 Markmap Writer 負責。

#### 4.1 Markmap Writer

**配置結構：**
```yaml
models:
  writer:
    model: "gpt-4o"
    persona_prompt: "prompts/writer/writer-persona.md"
    behavior_prompt: "prompts/writer/writer-behavior.md"
    temperature: 0.5
    max_tokens: 8192
```

#### 4.2 Inputs

Writer 接收以下輸入：

1. **Selected Markmap** - Phase 3 選出的最佳結構
2. **Judge Feedback** - 評審的改進建議（★ 必須根據這些建議優化）
3. **Consensus Suggestions** - 評審辯論後達成的共識改進項目
4. **Problem Metadata** - 完整的問題資料（★ 此時才載入）
5. **Markmap Format Guide** - Markmap 格式能力說明

#### 4.3 Writer 的優化職責

Writer **必須根據 Evaluation & Debate 的意見進行優化**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    Writer 優化流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input: Selected Markmap (from Judges)                          │
│         ↓                                                       │
│  Step 1: 分析評審反饋                                           │
│         • 讀取每位評審的 strengths (保留)                       │
│         • 讀取每位評審的 improvements (必須改進)                │
│         • 讀取 consensus_suggestions (優先改進)                 │
│         ↓                                                       │
│  Step 2: 應用改進建議                                           │
│         • 結構調整 (如：拆分過大的節點)                         │
│         • 命名優化 (如：更清晰的分類名稱)                       │
│         • 深度平衡 (如：避免過深或過淺)                         │
│         • 補充缺失 (如：增加遺漏的 pattern)                     │
│         ↓                                                       │
│  Step 3: 套用 Metadata                                          │
│         • 根據 problem metadata 生成正確連結                    │
│         • GitHub solution (if exists) / LeetCode (fallback)     │
│         • 加入 difficulty, complexity 等資訊                    │
│         ↓                                                       │
│  Step 4: 套用 Markmap 格式                                      │
│         • YAML frontmatter                                      │
│         • Checkboxes, KaTeX, fold, tables                       │
│         ↓                                                       │
│  Output: Final Optimized Markmap                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**範例 - 評審建議與 Writer 處理：**

| 評審建議 | Writer 處理方式 |
|----------|-----------------|
| "Two Pointers section is too flat" | 拆分為 "Opposite Direction" 和 "Same Direction" 子分類 |
| "Missing complexity annotations" | 加入 `Time: $O(n)$` KaTeX 標註 |
| "Hard problems should be highlighted" | 使用 **Hard** 粗體標記 |
| "Section too long, hard to navigate" | 加入 `<!-- markmap: fold -->` 折疊 |
| "Inconsistent naming convention" | 統一使用 "LC-XXX Title" 格式 |

#### 4.3 Link Generation Logic

```python
def generate_link(problem: dict) -> str:
    """
    Generate appropriate link for a problem.
    
    Priority:
    1. GitHub solution (if exists)
    2. LeetCode problem page (fallback)
    """
    if problem.get("solution_file"):
        # Has solution in our repo
        return f"https://github.com/lufftw/neetcode/blob/main/{problem['solution_file']}"
    else:
        # Use LeetCode link
        return f"https://leetcode.com/problems/{problem['slug']}/"
```

#### 4.4 Markmap Format Guide

Writer 會收到 Markmap 的完整格式能力說明：

```markdown
# Markmap Format Guide

## YAML Frontmatter
---
title: markmap
markmap:
  colorFreezeLevel: 2
---

## Supported Features

### Links
- [Website](https://markmap.js.org/)
- [GitHub](https://github.com/gera2ld/markmap)

### Text Formatting
- **strong** ~~del~~ *italic* ==highlight==
- `inline code`

### Checkboxes (Progress Tracking)
- [x] Completed problem
- [ ] Pending problem

### KaTeX Math
- Time: $O(n)$
- Space: $O(1)$
- Complex: $x = {-b \pm \sqrt{b^2-4ac} \over 2a}$

### Folding (for dense sections)
- Dense Section <!-- markmap: fold -->
  - Item 1
  - Item 2
  - ...

### Code Blocks
```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
```

### Tables
| Difficulty | Count |
|------------|-------|
| Easy       | 50    |
| Medium     | 75    |
| Hard       | 25    |

### Images
![Logo](https://markmap.js.org/favicon.png)

### Ordered Lists
1. First step
2. Second step
3. Third step

### Long Text Wrapping
- Use `maxWidth` option for very very very long text
```

#### 4.5 Output

完整的 Markmap Markdown，包含：
- YAML frontmatter
- 正確的連結（GitHub / LeetCode）
- 適當的格式（checkboxes, KaTeX, fold）
- 評審建議的改進

### Phase 5: Translation

與 V1 相同，對 `mode="translate"` 的語言進行翻譯。

### Phase 6: Post-Processing (程式處理，非 LLM)

在儲存前，程式會自動進行文字替換，減少 LLM prompt 負擔：

```yaml
post_processing:
  text_replacements:
    # Replace "LC" abbreviation with full "LeetCode"
    - pattern: "\\bLC[-\\s]?(\\d+)"
      replacement: "LeetCode \\1"
```

**範例轉換：**
| 輸入 | 輸出 |
|------|------|
| `LC-125` | `LeetCode 125` |
| `LC 125` | `LeetCode 125` |
| `LC125` | `LeetCode 125` |

**為什麼用程式處理？**
- LLM 可能不一致（有時 LC，有時 LeetCode）
- 減少 prompt 中的格式指令
- 100% 保證一致性

### Phase 7: Output

產出最終的 `.md` 和 `.html` 檔案。

---

## Configuration Schema (V2)

```yaml
# =============================================================================
# AI Markmap Agent Configuration V2
# =============================================================================

# -----------------------------------------------------------------------------
# Workflow Configuration
# -----------------------------------------------------------------------------
workflow:
  # Optimization rounds
  optimization_rounds: 3
  
  # Judge/Debate settings
  judge_count: 2                    # Minimum 2 judges required
  enable_debate: true
  max_debate_rounds: 3
  debate_consensus_threshold: 0.8   # 80% agreement = consensus
  
  # Other settings...

# -----------------------------------------------------------------------------
# Model Configuration
# -----------------------------------------------------------------------------
models:
  # Generators (Phase 1)
  generalist:
    en:
      model: "gpt-4o"
      persona_prompt: "prompts/generators/generalist-persona.md"
      behavior_prompt: "prompts/generators/generalist-behavior.md"
      temperature: 0.7
    zh:
      model: "gpt-4o"
      # ... same structure

  specialist:
    # ... same structure as generalist

  # Optimizers (Phase 2)
  optimizer:
    - id: "optimizer_architect"
      name: "The Software Architect"
      model: "gpt-4o"
      persona_prompt: "prompts/optimizers/optimizer_architect-persona.md"
      behavior_prompt: "prompts/optimizers/optimizer_architect-behavior.md"
      temperature: 0.6
      focus: "architecture_modularity"
    
    - id: "optimizer_professor"
      # ...
    
    - id: "optimizer_apidesigner"
      # ...

  # Summarizer (Phase 2)
  summarizer:
    model: "gpt-4o"
    persona_prompt: "prompts/summarizer/summarizer-persona.md"
    behavior_prompt: "prompts/summarizer/summarizer-behavior.md"
    temperature: 0.5

  # Judges (Phase 3) - CONFIGURABLE COUNT
  judges:
    - id: "judge_structure"
      name: "Structure Judge"
      model: "gpt-4o"                    # Can use different model
      persona_prompt: "prompts/judges/judge_structure_persona.md"
      behavior_prompt: "prompts/judges/judge_structure_behavior.md"
      temperature: 0.4
      criteria:
        - "hierarchy_quality"
        - "logical_grouping"
    
    - id: "judge_completeness"
      name: "Completeness Judge"
      model: "gpt-4o-mini"               # Can use different model
      persona_prompt: "prompts/judges/judge-completeness-persona.md"
      behavior_prompt: "prompts/judges/judge-completeness-behavior.md"
      temperature: 0.4
      criteria:
        - "coverage"
        - "practical_value"
    
    # Add more judges as needed...

  # Markmap Writer (Phase 4) - NEW
  writer:
    model: "gpt-4o"
    persona_prompt: "prompts/writer/writer-persona.md"
    behavior_prompt: "prompts/writer/writer-behavior.md"
    format_guide: "prompts/writer/markmap-format-guide.md"  # Markmap 格式說明
    temperature: 0.5
    max_tokens: 8192

  # Translator (Phase 5)
  # ... (same as V1)

# -----------------------------------------------------------------------------
# Data Sources (unchanged from V1)
# -----------------------------------------------------------------------------
data_sources:
  # ...

# -----------------------------------------------------------------------------
# Output Configuration (unchanged from V1)
# -----------------------------------------------------------------------------
output:
  # ...
```

---

## Key Design Decisions

### 1. 延遲連結處理

**問題**：在每個階段都處理連結會增加 prompt 負擔
**解決**：只在 Phase 4 (Writer) 才處理連結

**優點**：
- 減少前期 prompt 大小
- Optimizer 和 Judge 可專注於結構
- Writer 有完整 context 做最佳連結決策

### 2. 可配置的評審數量

**問題**：固定的評審可能不夠靈活
**解決**：在 config 中配置評審數量和個別模型

**優點**：
- 可根據需求增減評審
- 不同評審可用不同模型（成本/品質權衡）
- 易於擴展新的評審角色

### 3. 辯論機制

**問題**：評審可能有分歧
**解決**：多輪辯論達成共識

**流程**：
1. 獨立評分
2. 比較分數差異
3. 分歧大 → 進入辯論
4. 交換意見、反駁
5. 重新評分
6. 達成共識或最大輪數

### 4. 專職 Writer

**問題**：最終輸出需要處理多項細節
**解決**：新增專職 Markmap Writer

**職責**：
- 應用評審建議
- 生成正確連結
- 套用 Markmap 格式
- 產出最終版本

---

## File Structure

```
prompts/
├── generators/
│   ├── generalist-persona.md
│   ├── generalist-behavior.md
│   ├── specialist-persona.md
│   └── specialist-behavior.md
├── optimizers/
│   ├── optimizer-architect-persona.md
│   ├── optimizer-architect-behavior.md
│   ├── optimizer-professor-persona.md
│   ├── optimizer-professor-behavior.md
│   ├── optimizer-apidesigner-persona.md
│   └── optimizer-apidesigner-behavior.md
├── summarizer/
│   ├── summarizer-persona.md
│   └── summarizer-behavior.md
├── judges/                          # Configurable judges
│   ├── judge_structure_persona.md
│   ├── judge_structure_behavior.md
│   ├── judge-completeness-persona.md
│   ├── judge-completeness-behavior.md
│   └── ...                          # Add more as needed
└── writer/                          # NEW
    ├── writer-persona.md
    ├── writer-behavior.md
    └── markmap-format-guide.md      # Markmap 格式能力說明
```

---

## Example Output

最終 Markmap 輸出範例：

```markdown
---
title: NeetCode Algorithm Patterns
markmap:
  colorFreezeLevel: 2
---

# NeetCode Algorithm Patterns

## Two Pointers <!-- markmap: fold -->

### Opposite Direction
- [x] [LC-125 Valid Palindrome](https://github.com/lufftw/neetcode/blob/main/solutions/0125_valid_palindrome.py) ✓
  - Time: $O(n)$ | Space: $O(1)$
- [ ] [LC-167 Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
  - Time: $O(n)$ | Space: $O(1)$

### Same Direction
- [x] [LC-26 Remove Duplicates](https://github.com/lufftw/neetcode/blob/main/solutions/0026_remove_duplicates.py) ✓
- [ ] [LC-27 Remove Element](https://leetcode.com/problems/remove-element/)

## Sliding Window <!-- markmap: fold -->

### Fixed Size
- [x] [LC-643 Maximum Average Subarray I](https://github.com/lufftw/neetcode/blob/main/solutions/0643_max_avg_subarray.py) ✓

### Dynamic Size
- [x] [LC-3 Longest Substring Without Repeating Characters](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring.py) ✓
  - Time: $O(n)$ | Space: $O(min(m,n))$
- [ ] [LC-76 Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)
  - **Hard** | Time: $O(m+n)$

## Progress Summary

| Category | Solved | Total | Progress |
|----------|--------|-------|----------|
| Two Pointers | 2 | 4 | 50% |
| Sliding Window | 2 | 3 | 67% |
```

---

## Migration from V1

1. 更新 `config.yaml` 加入 `writer` 設定
2. 新增 `prompts/writer/` 目錄和檔案
3. 修改 `graph.py` 加入 Phase 4 (Writer) 節點
4. 修改 Generators 使用 Draft Mode（不含連結）
5. 測試完整流程

---

## Summary

V2 設計的核心改進：

| 項目 | V1 | V2 |
|------|----|----|
| 連結處理 | 每個階段 | 只在 Writer 階段 |
| 評審數量 | 固定 2 個 | 可配置 (≥2) |
| 評審模型 | 相同 | 可個別設定 |
| 辯論機制 | 簡單 | 多輪辯論 + 共識 |
| 最終產出 | Summarizer | 專職 Writer |
| Markmap 格式 | 基本 | 完整格式指南 |


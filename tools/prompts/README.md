# 🧠 AI Mind Map Generation

使用 LLM 根據 ontology 資料生成 LeetCode 練習心智圖。

---

## 🚀 全自動 AI 生成

AI 自動讀取所有 ontology 和題目資料，創意生成 Markmap 心智圖。

```bash
# 互動模式（選擇生成類型）
python tools/generate_mindmaps_ai.py

# 指定目標
python tools/generate_mindmaps_ai.py --goal interview      # 面試準備
python tools/generate_mindmaps_ai.py --goal systematic     # 系統學習
python tools/generate_mindmaps_ai.py --goal quick_review   # 快速複習
python tools/generate_mindmaps_ai.py --goal pattern_mastery # 模式掌握

# 指定主題
python tools/generate_mindmaps_ai.py --topic sliding_window
python tools/generate_mindmaps_ai.py --topic dp

# 指定風格
python tools/generate_mindmaps_ai.py --style creative
python tools/generate_mindmaps_ai.py --style minimal
python tools/generate_mindmaps_ai.py --style academic
```

### 配置檔案

編輯 `tools/generate_mindmaps_ai.toml` 可自訂：
- 使用的 LLM 模型
- 輸出目錄和檔名
- 要包含的 ontology 資料
- 題目篩選條件
- 連結格式（GitHub / LeetCode）
- 輸出語言（支援多語言同時生成）

---

## 📋 無 API Key？手動複製 Prompt

如果沒有 API key，可以手動複製 prompt 到 ChatGPT/Claude 網頁版：

1. **執行生成器**（會在調用 API 前保存 prompt）：
   ```bash
   python tools/generate_mindmaps_ai.py
   ```

2. **複製生成的 prompt**：
   - 打開 `tools/prompts/generated/mindmap_prompt.md`
   - 複製全部內容到 ChatGPT/Claude

3. **貼上 AI 輸出**：
   - 將 AI 回應保存為 `.md` 檔案
   - 使用 Markmap 預覽

---

## 📊 生成目標

| 目標 | 說明 | 參數 |
|------|------|------|
| 🎯 面試準備 | 高頻題目、公司偏好、面試技巧 | `--goal interview` |
| 📚 系統學習 | 按難度和依賴排序的學習路線 | `--goal systematic` |
| ⚡ 快速複習 | 精簡核心內容，面試前瀏覽 | `--goal quick_review` |
| 🔬 模式掌握 | 深入 Pattern 分析與關聯 | `--goal pattern_mastery` |
| 🎨 創意生成 | AI 自由發揮 | `--goal creative` |

---

## 🔗 連結生成規則

生成的心智圖會**自動**為題目添加連結（後處理）：

| 情況 | 連結類型 |
|------|----------|
| 題目有解答 | `[LeetCode X - Title](url) \| [Solution](github_url)` |
| 題目無解答 | `[LeetCode X - Title](leetcode_url)` |

> **Note**: LLM 只需輸出 `LeetCode {number}` 格式，後處理會自動添加標題和連結。

---

## 📁 檔案結構

```
tools/
├── generate_mindmaps_ai.py      # 主程式
├── generate_mindmaps_ai.toml    # 配置檔案
└── prompts/
    ├── README.md                # 本說明文件
    ├── system_prompt.md         # System Prompt（可自訂）
    ├── prompts_config.yaml      # Prompt 配置（語言、目標、風格）
    └── generated/
        └── mindmap_prompt.md    # 自動生成的 prompt（供手動使用）
```

## 🛠️ 自訂 Prompt

### System Prompt

編輯 `tools/prompts/system_prompt.md` 可修改 LLM 的角色設定和行為規則。

支援變數替換：
- `{{LANGUAGE_INSTRUCTION}}` - 會被替換為對應語言的指示

### Prompts Config

編輯 `tools/prompts/prompts_config.yaml` 可修改：

```yaml
# 語言指示
language_instructions:
  en: "Generate in English..."
  zh-TW: "以繁體中文生成..."

# 目標類型
goal_prompts:
  interview: "Generate an interview-focused..."
  creative: "Creatively generate..."

# 風格類型
style_prompts:
  academic: "Academic rigor..."
  minimal: "Minimalist style..."
```

---

## 👁️ Markmap 預覽

1. **VSCode 擴充功能**（推薦）
   - 安裝 [Markmap](https://marketplace.visualstudio.com/items?itemName=gera2ld.markmap-vscode)
   - 開啟 `.md` 檔案後點擊 markmap 圖示

2. **線上預覽**
   - [markmap.js.org/repl](https://markmap.js.org/repl)

3. **生成 HTML**
   - 在 `generate_mindmaps_ai.toml` 中設定 `generate_html = true`
   - 輸出到 `docs/pages/mindmaps/`

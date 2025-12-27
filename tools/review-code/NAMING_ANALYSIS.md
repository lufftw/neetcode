# 命名審核與位置調整分析

> **Status: RESOLVED** ✅
> 
> This analysis led to the creation of `tools/docstring/` domain module.
> See [docs/tools/docstring/refactor.md](../../docs/tools/docstring/refactor.md) for the final design rationale.
> 
> **Implementation completed:**
> - `leetscrape_fetcher.py` → `tools/docstring/formatter.py`
> - New `tools/docstring/` directory as dedicated domain
> - Updated imports in `fix_docstring.py`

---

## 現狀分析

### 當前結構

```
tools/review-code/
├── fix_docstring.py          # 主工具：修復 docstring
├── leetscrape_fetcher.py     # 數據提取與格式化模組
├── test_fetcher.py           # 測試腳本
├── test_leetscrape.py        # 測試腳本
└── README.md                 # 文檔

tools/leetcode-api/
├── question_api.py           # 統一數據接口（SQLite + LeetScrape）
├── question_store.py         # SQLite 存儲
└── question_serializer.py    # 格式轉換
```

### 問題識別

#### 1. 命名問題：`leetscrape_fetcher.py`

**當前名稱的問題：**
- ❌ 名稱暗示直接使用 `leetscrape` 庫，但實際上：
  - 使用 `question_api`（統一接口）
  - `question_api` 內部才使用 LeetScrape（作為後備）
  - 主要功能是**提取和格式化**，而非直接獲取

**實際功能：**
- ✅ 從 `Question` 對象提取描述、約束、示例等
- ✅ 格式化為符合 `README.md` 規範的 docstring 數據
- ✅ HTML 解析與文本提取
- ✅ 格式化 Topics、Hints、Follow-ups 等

#### 2. 位置問題

**當前位置：`tools/review-code/`**
- ✅ 與 `fix_docstring.py` 在同一目錄，便於使用
- ✅ 符合工具模組的組織方式
- ⚠️ 但名稱可能讓人誤以為是 `leetcode-api` 的一部分
- ⚠️ **如果作為通用 API 開放，放在 `review-code` 目錄下會顯得奇怪**
  - `review-code` 暗示這是「審核代碼」的工具
  - 其他工具使用時，從 `review-code` 導入格式化 API 語義不清
  - 例如：`from tools.review_code import docstring_formatter` 看起來像審核工具，而非格式化工具

## 建議方案

### 方案 A：重命名為更準確的名稱（推薦）

**選項 1：`docstring_formatter.py`** ⭐ 推薦
- ✅ 清楚表達功能：格式化 docstring 數據
- ✅ 與 `fix_docstring.py` 的命名風格一致
- ✅ 不依賴具體實現細節（LeetScrape）

**選項 2：`docstring_extractor.py`**
- ✅ 強調提取功能
- ⚠️ 但「格式化」也是重要功能

**選項 3：`docstring_data.py`**
- ✅ 通用且簡潔
- ⚠️ 但可能過於泛化

**選項 4：`docstring_builder.py`**
- ✅ 強調構建功能
- ⚠️ 但實際構建在 `DocstringBuilder` 類中（`fix_docstring.py`）

### 方案 B：保持名稱但更新文檔

如果保持 `leetscrape_fetcher.py`：
- 更新模組文檔，明確說明：
  - 使用 `question_api` 而非直接使用 LeetScrape
  - 主要功能是提取和格式化
  - LeetScrape 只是底層實現細節

### 方案 C：移動到 `leetcode-api` 並重命名

**新位置：`tools/leetcode-api/docstring_formatter.py`**
- ✅ 與數據相關模組放在一起
- ✅ 作為 API 模組的一部分，語義清晰
- ⚠️ 但會增加 `fix_docstring.py` 的導入路徑複雜度
- ⚠️ `leetcode-api` 主要負責數據獲取，格式化可能不太適合

### 方案 D：移動到 `shared` 目錄（推薦用於通用 API）⭐

**新位置：`tools/shared/docstring_formatter.py`**
- ✅ **最適合作為通用 API**：`shared` 目錄專門存放共享工具
- ✅ 語義清晰：`from tools.shared import docstring_formatter`
- ✅ 與現有 `shared/toml_parser.py` 的組織方式一致
- ✅ 可以被多個工具使用（`review-code`、`generate_pattern_docs`、未來工具等）
- ⚠️ 需要更新 `fix_docstring.py` 的導入路徑

### 方案 E：創建專用目錄（如果未來會擴展）

**新位置：`tools/docstring/docstring_formatter.py`**
- ✅ 專門處理 docstring 相關功能
- ✅ 未來可以擴展更多 docstring 工具（如 `docstring_validator.py`）
- ⚠️ 可能過度設計（如果只有一個模組）
- ⚠️ 需要創建新目錄和 `__init__.py`

## 推薦方案

### 🎯 場景 1：僅供 `review-code` 工具使用

**方案 A - 選項 1：重命名為 `docstring_formatter.py`（保持位置）**

**理由：**
1. **語義準確**：清楚表達模組功能（格式化 docstring 數據）
2. **命名一致**：與 `fix_docstring.py` 的命名風格一致
3. **實現無關**：不依賴具體的數據獲取方式（LeetScrape）
4. **易於理解**：新開發者能快速理解模組用途

**需要修改的文件：**
- `tools/review-code/leetscrape_fetcher.py` → `docstring_formatter.py`
- `tools/review-code/fix_docstring.py`（導入語句）
- `tools/review-code/test_fetcher.py`（導入語句）
- `tools/review-code/README.md`（文檔更新）

**影響範圍：**
- 僅影響 `tools/review-code/` 目錄內的導入

---

### 🎯 場景 2：作為通用 API 開放給其他工具使用 ⭐ 推薦

**方案 D：移動到 `shared` 目錄並重命名**

**理由：**
1. **語義清晰**：`from tools.shared import docstring_formatter` 清楚表達這是共享工具
2. **組織一致**：與 `shared/toml_parser.py` 的組織方式一致
3. **易於發現**：其他開發者知道在 `shared` 目錄找共享工具
4. **擴展性好**：未來其他工具可以輕鬆使用此 API

**新結構：**
```
tools/
├── shared/
│   ├── toml_parser.py
│   └── docstring_formatter.py  ← 新位置
└── review-code/
    ├── fix_docstring.py         ← 使用 shared.docstring_formatter
    └── ...
```

**需要修改的文件：**
- `tools/review-code/leetscrape_fetcher.py` → `tools/shared/docstring_formatter.py`
- `tools/review-code/fix_docstring.py`（導入語句改為 `from tools.shared import docstring_formatter`）
- `tools/review-code/test_fetcher.py`（導入語句）
- `tools/review-code/README.md`（文檔更新）
- `tools/shared/__init__.py`（如果不存在，需要創建）

**影響範圍：**
- 導入路徑改變，但語義更清晰
- 其他工具可以輕鬆使用此 API

## 實施步驟

### 如果採用場景 1（僅供 review-code 使用）：

1. **重命名文件**
   ```bash
   git mv tools/review-code/leetscrape_fetcher.py tools/review-code/docstring_formatter.py
   ```

2. **更新導入語句**
   - `fix_docstring.py`: `from docstring_formatter import get_full_docstring_data`
   - `test_fetcher.py`: `from docstring_formatter import get_description_and_constraints`

3. **更新文檔**
   - `tools/review-code/README.md`
   - 模組內部的 docstring

4. **更新測試**
   - 確保測試腳本仍能正常運行

---

### 如果採用場景 2（作為通用 API）⭐ 推薦：

1. **移動並重命名文件**
   ```bash
   git mv tools/review-code/leetscrape_fetcher.py tools/shared/docstring_formatter.py
   ```

2. **確保 `shared` 目錄有 `__init__.py`**
   ```bash
   # 如果不存在，創建
   touch tools/shared/__init__.py
   ```

3. **更新導入語句**
   - `fix_docstring.py`: 
     ```python
     import sys
     from pathlib import Path
     _SHARED_PATH = Path(__file__).parent.parent / "shared"
     if str(_SHARED_PATH) not in sys.path:
         sys.path.insert(0, str(_SHARED_PATH))
     from docstring_formatter import get_full_docstring_data
     ```
   - 或更簡潔的方式（如果 `tools` 在 Python path 中）：
     ```python
     from tools.shared.docstring_formatter import get_full_docstring_data
     ```
   - `test_fetcher.py`: 同樣更新導入

4. **更新文檔**
   - `tools/review-code/README.md` - 說明使用共享 API
   - `tools/shared/README.md`（可選）- 說明共享工具的使用
   - 模組內部的 docstring - 更新為「通用 API」的描述

5. **更新測試**
   - 確保測試腳本仍能正常運行
   - 考慮在 `tools/shared/` 下添加測試

6. **API 文檔化**
   - 在模組 docstring 中明確說明這是通用 API
   - 提供使用範例

## 其他考慮

### 測試文件命名

當前：
- `test_fetcher.py` - 測試 `leetscrape_fetcher`
- `test_leetscrape.py` - 測試 `leetscrape` 庫本身

建議：
- `test_docstring_formatter.py` - 測試格式化模組
- `test_leetscrape.py` - 保持不變（測試外部庫）

### 模組內部類/函數命名

當前模組導出的主要函數：
- `get_full_docstring_data()` ✅ 命名清晰
- `get_description_and_constraints()` ✅ 命名清晰（向後兼容）

這些函數名稱已經很好，無需修改。

## 結論

### 如果僅供 `review-code` 使用：
**推薦：重命名為 `docstring_formatter.py`（保持位置）**

### 如果作為通用 API 開放 ⭐ 強烈推薦：
**推薦：移動到 `tools/shared/docstring_formatter.py`**

**理由：**
1. **語義清晰**：`shared` 目錄明確表達這是共享工具
2. **組織一致**：與現有 `shared/toml_parser.py` 的組織方式一致
3. **易於發現**：其他開發者知道在 `shared` 目錄找共享工具
4. **專業性**：作為 API 模組，放在 `shared` 比放在工具目錄更合適
5. **未來擴展**：如果未來需要更多 docstring 相關工具，可以考慮創建 `docstring/` 子目錄

**使用範例：**
```python
# 其他工具可以這樣使用
from tools.shared.docstring_formatter import get_full_docstring_data

data = get_full_docstring_data("two-sum")
# 使用格式化後的數據...
```

這是最準確、最清晰的命名和組織方式，能讓開發者快速理解模組的實際功能，而不會被「leetscrape」這個實現細節誤導，同時作為通用 API 的定位也非常清晰。


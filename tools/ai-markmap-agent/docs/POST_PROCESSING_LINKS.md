# 後處理連結處理說明

## 概述

後處理模組 (`post_processing.py`) 負責將 AI 生成的 mindmap 內容中的 LeetCode 問題引用轉換為標準化的連結格式。

## 連結格式

### 目標格式

```
[LeetCode 11](leetcode_url) | [Solution](github_url)
```

**特點：**
- 只使用題號，不包含標題
- 格式簡潔統一
- 自動添加 GitHub solution 連結（如果有）

### 處理的輸入格式

後處理會處理以下多種 AI 可能產生的格式：

1. **純文字格式**
   - `LeetCode 11`
   - `LeetCode 11 - Container With Most Water`
   - `LC 11`

2. **Markdown 連結格式**
   - `[LeetCode 11](url)`
   - `[LeetCode 11 - Container With Most Water](url)`
   - `[LC 11](url)`

3. **錯誤的 URL**
   - `[LeetCode 11](wrong_url)` → 自動修正為正確的 URL

## 處理流程

### 步驟 1: 文字替換

- `LC 11` → `LeetCode 11`
- `LC-11` → `LeetCode 11`
- `LeetCode11` → `LeetCode 11`

### 步驟 2: 連結轉換

將純文字或現有連結轉換為標準格式：

**輸入：**
```
LeetCode 11 - Container With Most Water
```

**輸出：**
```
[LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/)
```

### 步驟 3: URL 正規化

確保所有 LeetCode URL 使用正確的格式：
- 移除檔案名稱格式的 slug（如 `0011_container_with_most_water`）
- 轉換為標準 slug（如 `container-with-most-water`）
- 確保以 `/description/` 結尾

### 步驟 4: 添加 GitHub Solution 連結

如果問題有對應的 solution 檔案，自動添加 GitHub 連結：

**輸入：**
```
[LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/)
```

**輸出：**
```
[LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
```

## 資料來源

### 本地 TOML 檔案

從 `meta/problems/` 目錄載入問題元資料，包含：
- 問題標題
- Solution 檔案路徑
- 其他元資料

### LeetCode API 快取

從 `tools/.cache/leetcode_problems.json` 載入：
- LeetCode URL
- Slug
- 問題標題（作為補充）

**優先順序：**
1. 本地 TOML 資料（優先）
2. API 快取資料（補充）

## 對比檔案

每次執行後處理後，會自動生成對比檔案：

**位置：** `outputs/final/post_processing_comparison_{timestamp}.md`

**內容：**
- Before: 原始內容（AI 生成）
- After: 後處理後的內容

**用途：**
- 檢查後處理效果
- 驗證連結是否正確生成
- 比較處理前後的差異

## 範例

### 範例 1: 純文字轉換

**Before:**
```markdown
- LeetCode 11 - Container With Most Water
- LeetCode 3 - Longest Substring
```

**After:**
```markdown
- [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
```

### 範例 2: 修正錯誤 URL

**Before:**
```markdown
- [LeetCode 11](https://leetcode.com/problems/0011_container_with_most_water/)
```

**After:**
```markdown
- [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
```

### 範例 3: 處理多種格式

**Before:**
```markdown
- LC 11
- LeetCode 11 - Container With Most Water
- [LeetCode 11](wrong_url)
```

**After:**
```markdown
- [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
- [LeetCode 11](https://leetcode.com/problems/container-with-most-water/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0011_container_with_most_water.py)
```

## 配置

後處理行為由 `config/config.yaml` 中的 `workflow.post_processing` 配置控制：

```yaml
workflow:
  post_processing:
    text_replacements:
      - pattern: "\\bLC[-\\s]?(\\d+)"
        replacement: "LeetCode \\1"
```

## 相關檔案

- `src/post_processing.py` - 後處理主模組
- `src/leetcode_api.py` - LeetCode API 資料載入
- `src/graph.py` - 工作流程整合
- `tools/sync_leetcode_data.py` - API 資料同步工具

## 注意事項

1. **格式簡化**：只使用題號，不包含標題，因為 AI 產生的格式很多元
2. **自動補充**：如果本地資料缺少 URL，自動從 API 快取補充
3. **對比檔案**：每次執行都會生成對比檔案，方便檢查效果
4. **向後相容**：不影響現有功能，只做補充和標準化

